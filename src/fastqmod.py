#! /usr/bin/env python
#_*_ coding:utf-8 _*_

"""

= NAME

fastqmod.py

= AUTHOR

Arnaud MENG M2BI (Paris 7 Diderot)

= DESCRIPTION

A Python module for simple FASTQ file analysis

= DATE

05/2014

= FUNCTIONS

with :
f = open("filename.fastq","r")

"""

#   IMPORTS --------------------------------------------------------------------

import re
import os
import subprocess

#   ILLUMINA QUALITY SCORES ----------------------------------------------------
# source : http://drive5.com/usearch/manual/quality_score.html

iqs = {}
iqs.setdefault
iqs['"'] = [1,0.79433]
iqs['#'] = [2,0.63096]
iqs['$'] = [3,0.50119]
iqs['%'] = [4,0.39811]
iqs['&'] = [5,0.31623]
iqs["'"] = [6,0.25119]
iqs['('] = [7,0.19953]
iqs[')'] = [8,0.15849]
iqs['*'] = [9,0.12589]
iqs['+'] = [10,0.1000]
iqs[','] = [11,0.07943]
iqs['-'] = [12,0.06310]
iqs['.'] = [13,0.05012]
iqs['/'] = [14,0.03981]
iqs['0'] = [15,0.03162]
iqs['1'] = [16,0.02512]
iqs['2'] = [17,0.01995]
iqs['3'] = [18,0.01585]
iqs['4'] = [19,0.01259]
iqs['5'] = [20,0.01000]
iqs['6'] = [21,0.00794]
iqs['7'] = [22,0.00631]
iqs['8'] = [23,0.00501]
iqs['9'] = [24,0.00398]
iqs[':'] = [25,0.00316]
iqs[';'] = [26,0.00251]
iqs['<'] = [27,0.00200]
iqs['='] = [28,0.00158]
iqs['>'] = [29,0.00126]
iqs['?'] = [30,0.00100]
iqs['@'] = [31,0.00079]
iqs['A'] = [32,0.00063]
iqs['B'] = [33,0.00050]
iqs['C'] = [34,0.00040]
iqs['D'] = [35,0.00032]
iqs['E'] = [36,0.00025]
iqs['F'] = [37,0.00020]
iqs['G'] = [38,0.00016]
iqs['H'] = [39,0.00013]
iqs['I'] = [40,0.00010]
iqs['J'] = [41,0.00008]



#   FUNCTIONS ------------------------------------------------------------------

"""
A function to retrieve the number of sequences (reads)
"""
def readcount(fin):
    
    seqcount = 0 
    
    regex = re.compile("^@")

    
    # Retrieving all file lines as a list of lines
    lines = fin.readlines()
    fin.seek(0)
    
    # For each line, looking for sequence type line 
    for line in lines:
        match = regex.search(line)
        if match != None:
            seqcount += 1
            
    return seqcount

"""
A function to retrieve all reads length as a list
"""
def readslength(fin):
    
    lengthlist = []
    
    regex = re.compile("^[ATGC]+$")
    
    # Retrieving all file lines as a list of lines
    lines = fin.readlines()
    fin.seek(0)

    # For each line, looking for sequence type line 
    for line in lines:
        match = regex.search(line)
        # Appening each sequence line length to a list
        if match != None:
            lengthlist.append(len(line))
    
    return lengthlist


"""
A function that return the GC percentage of all reads
"""
def percentgc(fin):
    
    total_nuc = 0.0
    g_count = 0.0
    c_count = 0.0
    
    regex = re.compile("^[ATGC]+$")
    # Retrieving all file lines as a list of lines
    lines = fin.readlines()
    fin.seek(0)
    
    # For each line, looking for sequence type line 
    for line in lines:
        match = regex.search(line)
        # Appening each sequence line length to a list
        if match != None:
            total_nuc += len(line)
            g_count += line.count("G")
            c_count += line.count('C')

    return round(((g_count + c_count)/total_nuc) * 100.0, 2)
    
"""
A function to calculate mean quality score of each read
return a list of list of mean scores associated to their read sequence :
[['seq1',score],['seq2',score],...]
"""
def decodereadquality(f):
    
    listofqual = []
        
    while True:
        
        # Retriving informations for each read
        try:
            seq_id = f.next().strip("\n")
            seq    = f.next().strip("\n")
            spacer = f.next().strip("\n")
            qual   = f.next().strip("\n")
            
            # Decoding the encoded score 
            decodedqual = [iqs[x][0] for x in list(qual)]
            
            # Calculating mean score of the read
            meanqual = sum(decodedqual) / len(seq)
            
            listofqual.append([seq,meanqual])
            
        except StopIteration:
            break
    
    f.seek(0)
    
    return listofqual

"""
A function to trim bad quality reads
TO USE THIS FUNCTION FASTX TOOLKIT HAS TO BE INSTALLED !
WEB : http://hannonlab.cshl.edu/fastx_toolkit/index.html
inputs : opened reads file (f) / minimum quality of bases within reads sequences
returns the names of the output files generated   
"""
def fastx_quality_filter(f, min_qual):
    
    # Formating input & output files names 
    input_filename = f.name
    filename, file_extention = os.path.splitext(input_filename)
    output_filename = filename + ".trimmed" + file_extention
    
    args = ['fastq_quality_trimmer',
            '-t',
            min_qual,
            '-i',
            input_filename,
            '-o',
            output_filename,
            '-Q33']
        
    # Launching command line
    with open("fastx_trimmer.out","wb") as out, open("fastx_trimmer.err","wb") as err:
        
        try:
            p = subprocess.Popen(args, 
                                 stdout=out,
                                 stderr=err)
            # Waiting for subprocess to terminate
            p.wait()
            
            # If subprocess succefully finished
            if p.returncode == 0:
                pass
            
        except subprocess.CalledProcessError as e:
            print (e.returncode)
    
    return output_filename

"""
A function to trim bad quality reads
TO USE THIS FUNCTION TRIMMOMATIC HAS TO BE INSTALLED !
WEB : http://www.usadellab.org/cms/?page=trimmomatic
inputs : opened reads file (f) / trimmomatic parameters dictionnary
returns the names of the output files generated   

Trimmomatic parameters dictionnary format : 

{'phred': '33', 
 'sw-size': '4', 
 'minlen': '40', 
 'sw-quality': '15', 
 'leading': '3', 
 'mi-strictness': '0.5', 
 'trailing': '3', 
 'mi-length': '40',
 'threads': '8',
 'trimpath': '/usr/share/java/trimmomatic.jar'}

sw : sliding window
mi : maxinfo

"""
def trimmomatic_trimming(reads_filename_1, reads_filename_2, trim_params_dic):
    
    # Formating input & output files names 
    input1 = reads_filename_1.name
    input2 = reads_filename_2.name
    
    filename1, file_extention1 = os.path.splitext(input1)
    filename2, file_extention2 = os.path.splitext(input2)
    
    output_paired_1 = filename1 + ".paired" + file_extention1
    output_paired_2 = filename2 + ".paired" + file_extention2
    
    output_unpaired_1 = filename1 + ".unpaired" + file_extention1
    output_unpaired_2 = filename2 + ".unpaired" + file_extention2
    
    # Formating options
    phred_option            = "-phred" + trim_params_dic['phred']
    leading_option          = "LEADING:" + trim_params_dic['leading']
    trailing_option         = "TRAILING:" + trim_params_dic['trailing']
    slidingwindow_option    = "SLIDINGWINDOW:" + \
                            trim_params_dic['sw-size'] + \
                            ":" + \
                            trim_params_dic['sw-quality']
    maxinfo_option          = "MAXINFO:" + \
                            trim_params_dic['mi-length'] + \
                            ":" + \
                            trim_params_dic['mi-strictness']
    minlen_option           = "MINLEN:" + trim_params_dic['minlen']
    
    args = ['java',
            '-jar',
            trim_params_dic['trimpath'],
            'PE',
            '-threads',
            trim_params_dic['threads'],
            phred_option,
            input1,
            input2,
            output_paired_1,
            output_unpaired_1,
            output_paired_2,
            output_unpaired_2,
            leading_option,
            trailing_option,
            slidingwindow_option,
            maxinfo_option,
            minlen_option]
    
    # Launching command line
    command_line = ' '.join(args)
    os.system(command_line + "> ./trimmomatic.log 2>&1")
    
    return output_paired_1, output_paired_2

