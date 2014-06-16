#! /usr/bin/env python
#_*_ coding:utf-8 _*_

"""

= NAME

pipeline.py

= AUTHOR

Arnaud MENG M2BI (Paris 7 Diderot)

= DESCRIPTION

A Python utility to proceed de novo transcriptomic assembly and analysis

= DATE

06/2014

"""

#   IMPORTS --------------------------------------------------------------------

# testetsttshjfzekfbzkjfblkzabf

import os, sys
import datetime
import time
import argparse

# Add /src/ directory to Python path | Edit if needed
sys.path.append("/home/meng/Pipeline/src")

# Custom modules
import fastqmod
import parsexmlmod as px
import commandlinegeneratormod as clg
import computerressourcesmod as cr
import commandlinelauncher as cll

#   FUNCTION -------------------------------------------------------------------

'''
A function to generate a summary file containing basics reads files informations
'''
def generate_summary(r1, r2, r1_reads_number, r2_reads_number):
    
    outsummary = open("data_summary.txt","w")
    outsummary.write('''
    ******************************************************\n
    READS FILES BASICS INFORMATIONS\n
    ******************************************************\n\n''')

    outsummary.write("Number of reads file-1 : " +  str(r1_reads_number) + "\n")
    outsummary.write("Number of reads file-2 : " +  str(r2_reads_number) + "\n")
    outsummary.write("Total number of reads  : " +  str(r1_reads_number+r2_reads_number) + "\n\n")
    
    r1_reads_length_list = fastqmod.readslength(r1)
    r2_reads_length_list = fastqmod.readslength(r2)
    r1_average_reads_length = sum(r1_reads_length_list) / len(r1_reads_length_list)
    r2_average_reads_length = sum(r2_reads_length_list) / len(r2_reads_length_list)
    
    outsummary.write("Average reads length file-1 : " +  str(r1_average_reads_length) + "\n")
    outsummary.write("Average reads length file-2 : " +  str(r2_average_reads_length) + "\n")
    outsummary.write("Total Average reads length  : " +  str((r1_average_reads_length+r2_average_reads_length)/2) + "\n\n")
    
    r1_gc_percentage =  fastqmod.percentgc(r1)
    r2_gc_percentage =  fastqmod.percentgc(r2)
    outsummary.write("GC percentage file-1 : " +  str(r1_gc_percentage) + "\n")
    outsummary.write("GC percentage file-2 : " +  str(r2_gc_percentage) + "\n")
    outsummary.write("Total GC percentage  : " +  str((r1_gc_percentage+r2_gc_percentage)/2) + "\n\n")
    



#   OPTIONS --------------------------------------------------------------------

parser=argparse.ArgumentParser(
    description='''A Python utility to proceed de novo transcriptomic assembly and analysis.''',
    epilog="""Arnaud MENG""")

parser.add_argument('--datasummary', 
                    type=str, 
                    action='store', 
                    default="no", 
                    help='Generate "summary.txt" : basics informations of reads files')  

args=parser.parse_args()


# Execution starts
start_time = time.time()

#   LOADING CONFIG FILE --------------------------------------------------------

print "[" + str(round(time.time()-start_time)) + "sec] Loading XML config file"

config_file = open("config.xml","r")

#   CONFIG FILE PARSING --------------------------------------------------------

print "[" + str(round(time.time()-start_time)) + "sec] Parsing directories parameters"

# Working directory
config_file.seek(0)
working_directory = px.parse_working_directory(config_file)

# Setting working directoty
if not os.path.exists(working_directory):
    os.makedirs(working_directory)
    
# Define as current directory
os.chdir(working_directory)
    
# Infile data directory
config_file.seek(0)
data_directory = px.parse_data_directory(config_file)

print "[" + str(round(time.time()-start_time)) + "sec] Parsing assemblers parameters"

# Reads files names
config_file.seek(0)
reads_file_1, reads_file_2 = px.parse_reads_files_names(config_file)

# Adding path to reads files names
reads_file_1 = data_directory + reads_file_1
reads_file_2 = data_directory + reads_file_2

# Trinity parameters
config_file.seek(0)
trinity_params = px.parse_trinity_parameters(config_file)

# Velvet/Oases parameters
config_file.seek(0)
vo_params = px.parse_vo_parameters(config_file)

#   PREPROCESSING READS FILES --------------------------------------------------

print "[" + str(round(time.time()-start_time)) + "sec] Preprocessing reads files"

# Loading reads files
r1 = open(reads_file_1,"r")
r2 = open(reads_file_2,"r")

# Counting reads number
r1_reads_number = fastqmod.readcount(r1)
r2_reads_number = fastqmod.readcount(r2)

# Summary option 
summary_option = args.datasummary
if summary_option == "yes":    
    print "[" + str(round(time.time()-start_time)) + "sec] Summaring"
    generate_summary(r1, r2, r1_reads_number, r2_reads_number)
    
# Reads Trimming
fastx_min_qual, fastx_percent_of_bases = px.parse_fastx_trimmed_option(config_file)
# fastqmod.fastx_quality_filter(r1, fastx_min_qual, fastx_percent_of_bases)

    
config_file.close()    
    
#   CHECKING COMPUTING RESSOURCES ----------------------------------------------

print "[" + str(round(time.time()-start_time)) + "sec] Checking computing ressources"    

# Checking CPU number 
number_of_cpus_available = cr.available_cpu_count()

if int(trinity_params["cpu"]) > number_of_cpus_available:
    sys.exit("ERROR : number of CPUs (" +\
              trinity_params["cpu"] +\
              ") exceeds maximum number of CPUs available (" +\
              str(number_of_cpus_available) + ")")

# Checking RAM amount
amount_of_ram = cr.available_memory_amount()

"""
Trinity : 1Go/million reads
VO      : 2Go/million reads
"""
expected_amount_of_ram_needed = cr.expected_both_assembler_ram(r1_reads_number, r2_reads_number)

if expected_amount_of_ram_needed > int(amount_of_ram["free"])/1000000:
    sys.exit("ERROR : Available amout of RAM needed for assemblies (" +\
              str(expected_amount_of_ram_needed) +\
              ") exceeds free amount of RAM available (" +\
              amount_of_ram["free"] + ")")

#   COMMAND LINE GENERATION ----------------------------------------------------

print "[" + str(round(time.time()-start_time)) + "sec] Generating command lines"

# Trinity 
trinity_command_line = clg.generate_trinity_command_line(reads_file_1, reads_file_2, trinity_params)

# Velvet/Oases
vo_command_line = clg.generate_vo_command_line(reads_file_1, reads_file_2, vo_params)

#   LAUNCHING ASSEMBLY ---------------------------------------------------------

print "[" + str(round(time.time()-start_time)) + "sec] Launching assembly"

cll.launch_command_line(trinity_command_line)
cll.launch_command_line(vo_command_line)

print "[" + str(round(time.time()-start_time)) + "sec] END"
