#! /usr/bin/env python
#_*_ coding:utf-8 _*_

"""

= NAME

parseXMLmod.py

= AUTHOR

Arnaud MENG M2BI (Paris 7 Diderot)

= DESCRIPTION

A Python module for XML file parsing

= DATE

06/2014

= FUNCTIONS

parse_reads_files_names(config_file)
parse_trinity_parameters(config_file)
parse_vo_parameters(config_file)

"""

#   IMPORTS --------------------------------------------------------------------

from xml.dom import minidom

#   DIRECTORIES ----------------------------------------------------------------

"""
A function to parse working directory path.
Returns one string.
"""
def parse_working_directory(config_file):
        
    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving assembler XML nodes
    directories = xml.getElementsByTagName('directories')
    
    for node in directories:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('directory')

        return param_list[0].attributes['working-directory'].value

"""
A function to parse data directory path.
Returns one string.
"""
def parse_data_directory(config_file):
        
    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving assembler XML nodes
    directories = xml.getElementsByTagName('directories')
    
    for node in directories:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('directory')

        return param_list[1].attributes['in-file'].value

#   PREPROCESSING --------------------------------------------------------------

"""
A function to parse data fastx_trimmer options
Returns 2 char.
"""
def parse_fastx_trimmed_option(config_file):
    
    
    # Parsing config XML file
    xml = minidom.parse(config_file)
        
    # Retrieving assembler XML nodes
    preprocess = xml.getElementsByTagName('preprocess')
    
    for node in preprocess:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('parameter')
    
        # TRINITY
        if node.getAttribute('name') == "fastx-trimmed":
            
            fastx_min_qual = param_list[0].attributes['min-quality'].value

    return fastx_min_qual

#   ASSEMBLY -------------------------------------------------------------------

"""
A function to parse reads files names.
Returns two strings of reads files names.
Current version only supports exactly two files.
"""
def parse_reads_files_names(config_file):
        
    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving assembler XML nodes
    files = xml.getElementsByTagName('files')
    
    for node in files:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('file')

        return param_list[0].attributes['left'].value, param_list[1].attributes['right'].value

"""
A function to parse Trinity assembler parameters.
Returns a dictionnary of Trinity assembler parameters.
"""
def parse_trinity_parameters(config_file):
    
    # Trinity parameters dictionnary
    trinity_param = {}
    
    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving assembler XML nodes
    assembler = xml.getElementsByTagName('assembler')
    
    for node in assembler:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('parameter')
    
        # TRINITY
        if node.getAttribute('name') == "trinity":
        
            trinity_param["seqtype"] = param_list[0].attributes['file-format'].value
            trinity_param["jm"] = param_list[1].attributes['max-ram'].value
            trinity_param["cpu"] = param_list[2].attributes['max-cpu'].value
            trinity_param["output"] = param_list[3].attributes['output'].value
            trinity_param["sslibtype"] = param_list[4].attributes['orientation'].value
            
    return trinity_param
    
    
"""
A function to parse Velvet/Oases assembler parameters
Returns a dictionnary of Velvet/Oases assembler parameters.

"""
def parse_vo_parameters(config_file):
    
    # Velvet/Oases parameters dictionnary
    vo_param = {}
    
    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving assembler XML nodes
    assembler = xml.getElementsByTagName('assembler')
    
    for node in assembler:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('parameter')

        # Velvet/Oases
        if node.getAttribute('name') == "velvet-oases":
        
            programs = node.getElementsByTagName('program')
        
            for program in programs:
            
                if program.getAttribute('name') == "velveth":
                
                    vo_param["fileformat"] = param_list[0].attributes['file-format'].value 
                    vo_param["readtype"] = param_list[1].attributes['read-type'].value  
                    vo_param["filelayout"] = param_list[2].attributes['file-layout'].value   
                    vo_param["strandspecific"] = param_list[3].attributes['orientation'].value
                
                elif program.getAttribute('name') == "oases":
                
                    vo_param["insertlength"] = param_list[4].attributes['insert-length'].value
                    vo_param["nodecoverage"] = param_list[5].attributes['node-coverage'].value
                
                elif program.getAttribute('name') == "oases-pipeline":
                
                    vo_param["mink"] = param_list[6].attributes['min-k'].value
                    vo_param["maxk"] = param_list[7].attributes['max-k'].value
                    vo_param["stepk"] = param_list[8].attributes['step-k'].value
                    vo_param["output"] = param_list[9].attributes['output'].value
                    
    return vo_param
