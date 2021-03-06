#! /usr/bin/env python
#_*_ coding:utf-8 _*_

"""

= NAME

commandLineGeneratormod.py

= AUTHOR

Arnaud MENG M2BI (Paris 7 Diderot)

= DESCRIPTION

A Python module to launch command lines

= DATE

06/2014

= FUNCTION

"""

#   IMPORTS --------------------------------------------------------------------

import shlex, subprocess
import time,sys
import re

#   FUNCTIONS ------------------------------------------------------------------

"""
Function to format parameters as a list ready to be use by subprocess.Popen()
"""
def define_args(command_line):
    
    return shlex.split(command_line)

"""
Function to launch command line 
"""    
def launch_command_line(command_line):
    
    # Retrieve splitted args
    args = define_args(command_line)
        
    # Defining stdout and stderr file names
    if args[0] == "Trinity.pl":
        stdout_name = "stdout_trinity.txt"
        stderr_name = "stderr_trinity.txt"
    elif args[0] == "oases_pipeline.py":
        stdout_name = "stdout_vo.txt"
        stderr_name = "stderr_vo.txt"
    elif re.match(".*\/generateBAM.py$" ,args[0]) is not None:
        stdout_name = "stdout_bam_generation.txt"
        stderr_name = "stderr_bam_generation.txt"
    else:
        stdout_name = "stdout.txt"
        stderr_name = "stderr.txt"
    
    # Launching command line
    with open(stdout_name,"wb") as out, open(stderr_name,"wb") as err:
        
        try:
            p = subprocess.Popen(args, 
                                 stdout=out,
                                 stderr=err)
            # Waiting for subprocess to terminate
            p.wait()
            
            # If subprocess succefully finished
            if p.returncode == 0:
                pass
            
        except CalledProcessError as e:
            print (e.returncode)
