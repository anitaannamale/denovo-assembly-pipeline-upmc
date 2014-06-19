#! /usr/bin/env python
#_*_ coding:utf-8 _*_

"""

= NAME

commandlinegeneratormod.py

= AUTHOR

Arnaud MENG M2BI (Paris 7 Diderot)

= DESCRIPTION

A Python module to generate command lines for several programs

= DATE

06/2014

"""

#   IMPORTS --------------------------------------------------------------------

import sys

#   FUNCTIONS ------------------------------------------------------------------


"""
A function to check if mandatory parameter is filled.
Takes in argument : parameters dictionnary and the key to check.
Stops the program if a parameter is not filled.
"""
def check_parameter_not_blank(dic, key):
    if not dic[key]:
        sys.exit("ERROR : " + key + " parameter must be filled in config.xml !")
    

"""
A function to generate Trinity assembler command line.
"""
def generate_trinity_command_line(readsfile1, readsfile2, paramsdic):
    
    # Checking mandatory parameters
    check_parameter_not_blank(paramsdic,"seqtype")
    check_parameter_not_blank(paramsdic,"jm")
    if not readsfile1 or not readsfile2:
        sys.exit("ERROR : You must specify reads files names !")
    
    # Declaration
    command_line = "Trinity.pl"
    
    # Formating required parameters 
    seqtype_par        = "--seqType "     + paramsdic["seqtype"]
    jm_par             = "--JM "          + paramsdic["jm"] + "G"
    left_par           = "--left "        + readsfile1
    right_par          = "--right "       + readsfile2
    
    # Formating optional parameters
    sslibtype_par = ""
    cpu_par = ""
    output_par = ""
    
    if paramsdic["sslibtype"]:
        sslibtype_par = "--SS_lib_type " + paramsdic["sslibtype"]
    
    if paramsdic["cpu"]:
        cpu_par = "--CPU " + paramsdic["cpu"]
    
    if paramsdic["output"]: 
        output_par = "--output " + paramsdic["output"]
    
    # Formating complete command line
    command_line = ("%s %s %s %s %s %s %s %s")%(command_line,
                                                seqtype_par,
                                                jm_par,
                                                left_par,
                                                right_par,
                                                sslibtype_par,
                                                cpu_par,
                                                output_par)
        
    return command_line


#   TRINITY --------------------------------------------------------------------

"""
A function to generate Velvet/Oases assembler command line.
"""
def generate_vo_command_line(readsfile1, readsfile2, paramsdic):
    
    # Checking mandatory parameters
    check_parameter_not_blank(paramsdic,"fileformat")
    check_parameter_not_blank(paramsdic,"filelayout")
    check_parameter_not_blank(paramsdic,"readtype")
    if not readsfile1 or not readsfile2:
        sys.exit("ERROR : You must specify reads files names !")
    
    # Declaration
    command_line = "oases_pipeline.py"
    
    # Formating velveth parameters
    fileformat_par      = paramsdic["fileformat"]
    failelayout_par     = paramsdic["filelayout"]
    readtype_par        = paramsdic["readtype"]
    
    strandspecific_par = ""
    if paramsdic["strandspecific"]:
        strandspecific_par = paramsdic["strandspecific"]
    
    left_par            = readsfile1
    right_par           = readsfile2

    velveth_command_line = ('-d " %s %s %s %s %s %s "')%(fileformat_par,
                                                         failelayout_par,
                                                         readtype_par,
                                                         strandspecific_par,
                                                         left_par,
                                                         right_par)
    
    # Formating oases parameters
    insertlength_par = ""
    nodecoverage_par = ""
    
    if paramsdic["insertlength"]:
        insertlength_par = "-ins_length " + paramsdic["insertlength"]
    
    if paramsdic["nodecoverage"]:
        nodecoverage_par = "-cov_cutoff " + paramsdic["nodecoverage"]
        
    if insertlength_par or nodecoverage_par:
        oases_command_line = ('-p " %s %s "')%(insertlength_par, nodecoverage_par)
    else:
        oases_command_line = ""
        
    # Formating oases_pipeline.py parameters 
    kmin_par               = "-m "     + paramsdic["mink"]
    kmax_par               = "-M "     + paramsdic["maxk"]
    step_par               = "-s "     + paramsdic["stepk"]
    output_par             = "-o "     + paramsdic["output"]
    clean_par              = "-c"
    
    command_line = command_line + (" %s %s %s %s %s %s %s")%(kmin_par,
                                                             kmax_par,
                                                             step_par,
                                                             output_par,
                                                             velveth_command_line,
                                                             oases_command_line,
                                                             clean_par)
    
    return command_line
