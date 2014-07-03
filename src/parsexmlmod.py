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

"""

#   IMPORTS --------------------------------------------------------------------

from xml.dom import minidom
from xml.etree.ElementTree import ElementTree

#   DIRECTORIES ----------------------------------------------------------------

"""
A function to parse working directory path.
Returns one string.
"""
def parse_working_directory(config_file):
        
    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving directories XML nodes
    directories = xml.getElementsByTagName('directories')
    
    for node in directories:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('directory')

        return param_list[0].attributes['working-directory'].value

"""
A function to parse working directory path.
Returns one string.
ElementTree version
"""
def parse_working_directory_ET(tree):

    # Retrieving directory XML nodes
    for node in tree.iter('directory'):
        
        # Finding directory node of working directory
        if node.attrib.get('working-directory'): 
            return node.attrib.get('working-directory')
    
"""
A function to parse data directory path.
Returns one string.
"""
def parse_data_directory(config_file):
        
    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving directories XML nodes
    directories = xml.getElementsByTagName('directories')
    
    for node in directories:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('directory')

        return param_list[1].attributes['in-file'].value

"""
A function to parse data directory path.
Returns one string.
ElementTree version
"""
def parse_data_directory_ET(tree):
        
    # Retrieving directory XML nodes
    for node in tree.iter('directory'):
        
        # Finding directory node of working directory
        if node.attrib.get('in-file'): 
            return node.attrib.get('in-file')

#   PREPROCESSING --------------------------------------------------------------

"""
A function to parse data fastx_trimmer options
Returns 1 char.
"""
def parse_fastx_trimmed_option(config_file):
    
    # Parsing config XML file
    xml = minidom.parse(config_file)
        
    # Retrieving preprocess XML nodes
    preprocess = xml.getElementsByTagName('preprocess')
    
    for node in preprocess:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('parameter')
    
        # Fastx
        if node.getAttribute('name') == "fastx-trimmed":
            
            fastx_min_qual = param_list[0].attributes['min-quality'].value

    return fastx_min_qual
    
"""
A function to parse data fastx_trimmer options
Returns 1 char.
ElementTree version
"""
def parse_fastx_trimmed_option_ET(tree):
    
    # Retrieving preprocess XML nodes
    for node in tree.findall('./preprocesses/preprocess'):
    
        # Retrieving all Fastx parameters
        if node.attrib['name'] == 'fastx-trimmed':
            for child in node.findall('./parameters/parameter'):
                
                if child.attrib.get('min-quality'):
                    return child.attrib.get('min-quality')

"""
A function to parse Trimmomatic parameters from XML file
ElementTree version
"""
def parse_trimmomatic_option_ET(tree):
    
    # Trinity parameters dictionnary
    trimmomatic_param = {}
    
    # Optional parameters
    trimmomatic_param["leading"] = "3"
    trimmomatic_param["trailing"] = "3"
    trimmomatic_param["sw-size"] = "4"
    trimmomatic_param["sw-quality"] = "15"
    trimmomatic_param["mi-length"] = ""
    trimmomatic_param["mi-strictness"] = "0.5"

    # Retrieving preprocess XML nodes
    for node in tree.findall('./preprocesses/preprocess'):
    
        # Retrieving all Fastx parameters
        if node.attrib['name'] == 'trimmomatic':
            for child in node.findall('./parameters/parameter'):
                
                # Mandatory parameters
                if child.attrib.get('trimmomatic-path'):
                    trimmomatic_param["trimpath"] = child.attrib.get('trimmomatic-path')
                if child.attrib.get('phred-encoding'):
                    trimmomatic_param["phred"] = child.attrib.get('phred-encoding')
                if child.attrib.get('min-read-length'):
                    trimmomatic_param["minlen"] = child.attrib.get('min-read-length')
                    
                # Optional parameters
                if child.attrib.get('threads-number'):
                    trimmomatic_param["threads"] = child.attrib.get('threads-number')
                if child.attrib.get('leading-quality-threshold'):
                    trimmomatic_param["leading"] = child.attrib.get('leading-quality-threshold')
                if child.attrib.get('trailing-quality-threshold'):
                    trimmomatic_param["trailing"] = child.attrib.get('trailing-quality-threshold')
                if child.attrib.get('sliding-window-size'):
                    trimmomatic_param["sw-size"] = child.attrib.get('sliding-window-size')
                if child.attrib.get('sliding-window-quality'):
                    trimmomatic_param["sw-quality"] = child.attrib.get('sliding-window-quality')
                if child.attrib.get('target-length'):
                    trimmomatic_param["mi-length"] = child.attrib.get('target-length')
                if child.attrib.get('target-strictness'):
                    trimmomatic_param["mi-strictness"] = child.attrib.get('target-strictness')
                
    return trimmomatic_param

#   ASSEMBLY -------------------------------------------------------------------

"""
A function to parse reads files names.
Returns two strings of reads files names.
Current version only supports exactly two files.
"""
def parse_reads_files_names(config_file):

    # Parsing config XML file
    xml = minidom.parse(config_file)
    
    # Retrieving files XML nodes
    files = xml.getElementsByTagName('files')
    
    for node in files:
    
        # Retrieving all parameters
        param_list = node.getElementsByTagName('file')

        return param_list[0].attributes['left'].value, param_list[1].attributes['right'].value

"""
A function to parse reads files names.
Returns two strings of reads files names.
Current version only supports exactly two files.
ElementTree version
"""
def parse_reads_files_names_ET(tree):
    
    # Retrieving files XML nodes
    for node in tree.find('./assembly/files'):
    
        # Retrieving reads files names
        if node.attrib.get('left'):
            left = node.attrib.get('left')
        if node.attrib.get('right'):
            right = node.attrib.get('right')
            
    return left, right

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
            trinity_param["sslibtype"] = param_list[3].attributes['orientation'].value
            
    return trinity_param

"""
A function to parse Trinity assembler parameters.
Returns a dictionnary of Trinity assembler parameters.
ElementTree version
"""
def parse_trinity_parameters_ET(tree):
    
    # Trinity parameters dictionnary
    trinity_param = {}
    
    # Optional parameters
    trinity_param["cpu"] = "1"
    trinity_param["sslibtype"] = ""
    
    # Retrieving assembler XML nodes
    for node in tree.findall('./assembly/assembler'):
    
        # Retrieving all Trinity parameters
        if node.attrib['name'] == 'trinity':
            for child in node.findall('./parameters/parameter'):
                
                # Madatory parameters
                if child.attrib.get('file-format'):
                    trinity_param["seqtype"] = child.attrib.get('file-format')
                if child.attrib.get('max-ram'):
                    trinity_param["jm"] = child.attrib.get('max-ram')
                    
                # Optional parameters
                if child.attrib.get('max-cpu'):
                    trinity_param["cpu"] = child.attrib.get('max-cpu')
                if child.attrib.get('orientation'):
                    trinity_param["sslibtype"] = child.attrib.get('orientation')
                
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
                    
    return vo_param

"""
A function to parse Velvet/Oases assembler parameters
Returns a dictionnary of Velvet/Oases assembler parameters.
ElementTree version
"""
def parse_vo_parameters_ET(tree):
    
    # Velvet/Oases parameters dictionnary
    vo_param = {}
    
    # Optional parameter
    vo_param["strandspecific"] = ""
    vo_param["insertlength"] = ""
    vo_param["nodecoverage"] = "" 
    
    # Retrieving all program nodes 
    for node in tree.findall('./assembly/assembler/program'):
    
        # Retrieving all velveth parameters
        if node.attrib['name'] == 'velveth':
            for child in node.findall('./parameters/parameter'):
                
                # Mandatory parameters
                if child.attrib.get('file-format'):
                    vo_param["fileformat"] = child.attrib.get('file-format')
                if child.attrib.get('read-type'):
                    vo_param["readtype"] = child.attrib.get('read-type')
                if child.attrib.get('file-layout'):
                    vo_param["filelayout"] = child.attrib.get('file-layout')
                
                # Optional parameter
                if child.attrib.get('orientation'):
                    vo_param["strandspecific"] = child.attrib.get('orientation')
                    
        # Retrieving all oases parameters
        if node.attrib['name'] == 'oases':
            for child in node.findall('./parameters/parameter'):
                
                # Optional parameters
                if child.attrib.get('insert-length'):
                    vo_param["insertlength"] = child.attrib.get('insert-length')
                if child.attrib.get('node-coverage'):
                    vo_param["nodecoverage"] = child.attrib.get('node-coverage')
                    
        # Retrieving all oases_pipeline parameters
        if node.attrib['name'] == 'oases-pipeline':
            for child in node.findall('./parameters/parameter'):
                
                # Mandatory parameters
                if child.attrib.get('min-k'):
                    vo_param["mink"] = child.attrib.get('min-k')
                if child.attrib.get('max-k'):
                    vo_param["maxk"] = child.attrib.get('max-k')
                if child.attrib.get('step-k'):
                    vo_param["stepk"] = child.attrib.get('step-k')

    return vo_param

#   MAPPING --------------------------------------------------------------------

"""
A function to parse mapping parameters (generateBAM.py).
ElementTree version
"""
def parse_mapping_parameters_ET(tree):
    
    # Mapping parameters dictionnary
    mapping_param = {}

   # Retrieving all program nodes 
    for node in tree.findall('./mapping/parameters/parameter'):
    
        # Retrieving all generateBAM.py parameters
        if node.attrib.get('mapping-program'):
            mapping_param["mapper"] = node.attrib.get('mapping-program')
            
    return mapping_param
