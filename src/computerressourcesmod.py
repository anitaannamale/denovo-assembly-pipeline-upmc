#! /usr/bin/env python
#_*_ coding:utf-8 _*_

"""

= NAME

computerressourcesmod.py

= AUTHOR

Arnaud MENG M2BI (Paris 7 Diderot)

= DESCRIPTION

A Python module to retrieve computer ressources informations (CPU number and RAM).

= DATE

06/2014

= FUNCTION

available_cpu_count()
available_memory_amount()
expected_trinity_ram(r1_reads_number, r2_reads_number)
expected_vo_ram(r1_reads_number, r2_reads_number)
expected_both_assembler_ram(r1_reads_number, r2_reads_number)

"""

#   IMPORTS --------------------------------------------------------------------

import os
import re
import subprocess

#   FUNCTIONS ------------------------------------------------------------------

def available_cpu_count():
    """
    Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    source : http://stackoverflow.com/questions/1006289/how-to-find-out-the-number-of-cpus-in-python
    """

    # cpuset
    # cpuset may restrict the number of *available* processors

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    raise Exception('Can not determine number of CPUs on this system')


def available_memory_amount():
    """
    Get node total memory and memory usage
    source : http://stackoverflow.com/questions/17718449/determine-free-ram-in-python
    """
    with open('/proc/meminfo', 'r') as mem:
        ret = {}
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                ret['total'] = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
        ret['free'] = tmp
        ret['used'] = int(ret['total']) - int(ret['free'])
    return ret

"""
Predict the amount of RAM needed for Trinity assembly
"""
def expected_trinity_ram(r1_reads_number, r2_reads_number):
    return ((int(r1_reads_number) + int(r2_reads_number)) / 1000000) * 1

"""
Predict the amount of RAM needed for VO assembly
"""
def expected_vo_ram(r1_reads_number, r2_reads_number):
    return ((int(r1_reads_number) + int(r2_reads_number)) / 1000000) * 2
    
"""
Predict the amount of RAM needed for both Trinity and VO assemblies
"""
def expected_both_assembler_ram(r1_reads_number, r2_reads_number):
    trinity_ram = expected_trinity_ram(r1_reads_number, r2_reads_number) 
    vo_ram = expected_vo_ram(r1_reads_number, r2_reads_number) 
    return trinity_ram + vo_ram
