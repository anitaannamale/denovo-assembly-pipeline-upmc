upmc-denovo-assembly-pipeline
=============================

This pipeline is a tool to proceed de novo transcriptome assembly and few analysis.

/!\ This current version IS NOT fonctional for the moment !

Version
----

1.0

Tech
-----------

upmc-denovo-assembly-pipeline uses a number of open source projects to work properly:

* [Trinity] - A de novo transcriptome assembly program.
* [Velvet] - A de novo genome assembly program.
* [Oases] - A Velvet extention for de novo transcriptome assembly.

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

