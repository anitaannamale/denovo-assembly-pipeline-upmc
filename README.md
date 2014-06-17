upmc-denovo-assembly-pipeline
=============================

This pipeline is a tool to proceed de novo transcriptome assembly and few analysis.

/!\ This current version IS NOT fonctional at the moment !

Version
----

1.0

Tech
-----------

upmc-denovo-assembly-pipeline uses a number of open source projects to work properly:

* [Trinity] - A de novo transcriptome assembly program.
* [Velvet] - A de novo genome assembly program.
* [Oases] - A Velvet extention for de novo transcriptome assembly.
* [Fastx-toolkit] - A set of tools for FASTQ files treatment.

Installs
--------------
### Trinity
### Velvet
* Download : http://www.ebi.ac.uk/~zerbino/velvet/velvet_latest.tgz
```sh
cd <tgz_location>
tar -zxvf velvet_latest.tgz
cd <velvet_directory>
make 
```

_More compilation informations_ : https://www.ebi.ac.uk/~zerbino/velvet/Manual.pdf

### Oases
### Fastx-toolkit
Installed via Synaptic


Run
--------------

```sh
python pipeline.py
```


#### Setting configuration file : config.xml 

* Set working directory path
* Set infiles (reads files)
* Assembler parameters


**Free Software, Hell Yeah!**

[Trinity]:http://trinityrnaseq.sourceforge.net/
[Velvet]:http://www.ebi.ac.uk/~zerbino/velvet/
[Oases]:https://www.ebi.ac.uk/~zerbino/oases/
[Fastx-toolkit]:http://hannonlab.cshl.edu/fastx_toolkit/
