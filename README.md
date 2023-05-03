# Introduction


A lot of Pinnacle system are still functional. However, there will no
longer have development under Pinnacle and a lot of radiation oncology
centres need to go away from Pinnacle since the disinterest of
Philips Medical System.

This script here is dedicated to the conversion of Pinnacle TARFile to
DICOM. 
 
The tar files are created by Pinnacle containing one patient per tar
file.

The chance is that Australian physicists (*pymedphys* see below) have
worked to to design a python tool that does just this.


The different steps are:

- For each of these patients, convert all plans to DICOM



# Python tools for converting



## Create the environment for the conversion


    conda create -n pymedphys python=3.10


followed by a 


    conda activate pymedphys


Note: python 3.10 contains the **tarfile** library which will be important

for unpacking Pinnacle archives. In fact any python

>= 3.5 contains **tarfile**.



## pymedphys


<https://github.com/pymedphys/pymedphys>


installed with :


    $ pip install pymedphys[user]==0.39.3



## The pymedphys command


    $ pymedphys experimental pinnacle export data/PatientName_Firstname_PID_psqlNumber.tar -o out/



## poetry (optional)


It is necessary to install **poetry** to be able to work around a
color name problem for DICOM structures. In Pinnacle, it was allowed
for a long time to choose as color "inverse_grey". This name
corresponds to a color gradient. **poetry** tool allows to install the
GitHub version of **pymedphys**.  It is intended for developers who
want to contribute to pymedphys, and and also to users who want to
take advantage of unpublished (not yet released) unpublished (not yet
released).


<https://python-poetry.org/docs/>


installed with (being in the **pymedphys** environment of course):


    $ pip install poetry


To install pymedphys itself, you need to be in the GitHub directory of
pymedphys and run the following commands:


    $ poetry install -E all

    $ poetry run pre-commit install

    $ poetry run pymedphys dev tests


The last command allows you to see if the current version is

functional. For the HFR, it allowed to benefit from the taking into account of

structures colored in "inverse_grey".



## Python script to specify


If the patient is : 


1. known

    

    a. alive

    

    b. deceased


2. unknown



## PatientNameToPath tool


I installed the HFR-Radio-oncology tool with the following commands

while being in the conda **pymedphys** environment. For the other

centers, this is not possible, but not necessary either. The

necessary information is contained in the tar file anyway.

file anyway. It is just a matter of us (HFR) keeping our common vocabulary

quickly adaptable common vocabulary.


    $ git clone http://172.27.52.40:3000/HFR/patientNameToPath.git

    pip install patientNameToPath/



# Python routine to unpack and convert a TAR file to DICOM



## Decompress the tar in a local temporary tree



## Determining the patient



## Create target directory



## Conversion to DICOM



## Destroying the temporary directory



# Bash tools (very HFR, not applicable elsewhere)



# DONE Make the python script that launches the conversion for a given patient



# DONE Do the python script that checks if the patient is known to be dead. This is to avoid converting it for nothing.



# DONE Use all plans for export (normally only one plan is exported)



# TODO How to archive all these patients


1.  For the moment, we will put them in a defined directory and

    create a directory for each patient within this directory

    called by the usual format:


2.  There are no backups in Velocity, so the data can be deleted



