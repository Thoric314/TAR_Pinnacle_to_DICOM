# Introduction


For the moment the Pinnacle system is still functional. However,
there is no longer a contract between HFR and Philips to keep
Pinnacle in working order. So we need to find a solution
for all the patients who are still in the Pinnacle system.


Note: All these patients are regularly saved as a
tar file (Tape ARchive). This is the standard archiving format under
all Unix systems (including SunOs on which Pinnacle runs and also Linux

also Linux which we know well at HFR).


The idea is to convert these tar files that exist in a form
of a tar file to a Pinnacle patient.


The chance is that Australian physicists have worked to
to design a python tool that does just this conversion work.


This document explains the steps taken at the HFR to:


- validate the conversion tool,

- automate the conversions for patients who need it and

- transfer these DICOM files to Velocity in order to maintain the data

    necessary data to the clinic.


Note that in the past when converting from CADPLAN to

Pinnacle, the CADPLAN archives have not been recovered. All the

plans from this period (before 2006-2007) are lost. It was not

possible to transform these data in proprietary format to the

standard DICOM format. Here we hope that for Pinnacle nothing will be

lost (from 2006-2007 all plans should finally be available in Velocity at least for

accessible in Velocity at least for patients who are supposed to be alive

during this year 2023).


The different steps are:


- Establish a list of patients still presumed alive

- For each of these patients, convert all plans to DICOM

- For officially deceased patients, only the tar

    files are kept

- After the DICOM conversion, the resulting files are transferred to

    VelocityGRID for automatic import



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



