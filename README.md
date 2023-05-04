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
functional. One of the benefits is to take advantage of a more recent
update to avoid failures on a color problem (inverse_grey).


## PatientNameToPath tool

Not necessary if you do not work with a process of reconciliation with Aria.


## PatientNameToPath tool
