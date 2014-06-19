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
* [Bowtie] - An ultrafast, memory-efficient short read aligner.
* [SAMTools] - Provides various tools for manipulating alignments in the SAM/BAM format.
* [Python] - A widely used general-purpose, high-level programming language
* [Trimmomatic] - A fast, multithreaded command line tool that can be used to trim and crop Illumina (FASTQ) data as well as to remove adapters. 

Installs
--------------
### Python 2.7 & 3.0 

Installed via Synaptic

### Trinity

* Trinity prerequisites : 

##### [Java]
```sh
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer
```
##### [Bowtie] & [Bowtie2]

Installed via Synaptic

##### [SAMTools]

Installed via Synaptic


* Download Trinity : https://sourceforge.net/projects/trinityrnaseq/files/
* Installation command lines : 
```sh
cd <trinityrnaseq_r20131110 location>
make 
```
* Configure Trinity :

1. Open Trinity.pl script in Gedit
2. Find (Ctrl+F) 'my $CPU_MAX='
3. Change $CPU_MAX value to maximum CPU number
4. Save changes

* Add to $PATH : 
```sh
echo 'export PATH=$PATH:~/path_to_Trinity_folder/trinityrnaseq_r20131110' >> ~/.bashrc
```
* _More compilation informations_ : http://trinityrnaseq.sourceforge.net/#installation

### Velvet

* Download : http://www.ebi.ac.uk/~zerbino/velvet/velvet_latest.tgz
* Installation command lines : 
```sh
cd <velvet_latest.tgz location>
tar -zxvf velvet_latest.tgz
cd velvet_1.2.10
make
```
* Add to $PATH : 
```sh
echo 'export PATH=$PATH:~/path_to_Velvet_folder/velvet_1.2.10' >> ~/.bashrc
```
* _More compilation informations_ : https://www.ebi.ac.uk/~zerbino/velvet/Manual.pdf

### Oases

* Download : http://www.ebi.ac.uk/~zerbino/oases/oases_latest.tgz 
* Installation command lines : 
```sh
cd <oases_latest.tgz location>
tar -zxvf oases_latest.tgz
cd oases_oases_0.2.8
make 
```
* Add to $PATH : 
```sh
echo 'export PATH=$PATH:~/path_to_Oases_folder/oases_0.2.8' >> ~/.bashrc
```
* _More compilation informations_ : https://www.ebi.ac.uk/~zerbino/oases/OasesManual.pdf

### Fastx-toolkit
Installed via Synaptic

### Trimmomatic
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

[Python]:https://www.python.org/
[Java]:http://www.java.com/fr/
[Bowtie]:http://bowtie-bio.sourceforge.net/index.shtml
[Bowtie2]:http://bowtie-bio.sourceforge.net/index.shtml
[SAMTools]:http://samtools.sourceforge.net/
[Trinity]:http://trinityrnaseq.sourceforge.net/
[Velvet]:http://www.ebi.ac.uk/~zerbino/velvet/
[Oases]:https://www.ebi.ac.uk/~zerbino/oases/
[Fastx-toolkit]:http://hannonlab.cshl.edu/fastx_toolkit/
[Trimmomatic]:http://www.usadellab.org/cms/?page=trimmomatic
