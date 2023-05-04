#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
To extract the task for all groups of radio-oncology department
"""

import os
import sys
import shutil
import tarfile
import glob

from datetime import timedelta, datetime, date, time

import ariaDatabaseConnector as aria
from pymedphys._experimental.pinnacle import PinnacleExport, PinnaclePlan



def print_date(date):
    if date != None:
        print(f'#{date.strftime("%Y-%m-%d")}',end='')
    else:
        print('#None',end='')
    return



def print_data(element):
    print("%s#%s#%s#%s" %
          ( element.PatientId,
            element.LastName,
            element.FirstName,
            element.Sex.strip(' ')
           ),
          end=''
          )
    print_date(element.DateOfBirth)
    print_date(element.DeathDate)
    print()



def fetch_PatientInfo(PID):
    """ Recherche dans Aria le patient correspondant au PID """
    
    req = """
    SET ROWCOUNT 1000
    SELECT
        Patient.PatientId,
        Patient.LastName,
        Patient.FirstName,
        Patient.DateOfBirth,
        PatientParticular.DeathDate,
        Patient.Sex
    FROM
        Patient
        INNER JOIN PatientParticular
        ON PatientParticular.PatientSer = Patient.PatientSer
    WHERE
       (Patient.PatientId = '%s')
    """ % PID
    
    all = aria.readRequest(req, database='VARIAN')
    if all:
        return all[0]
    else:
        return None



def erase(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    


def move(filename, dir):
    fileshort=os.path.basename(filename)
    full_path = os.path.join(dir, fileshort)
    shutil.move(filename, full_path)


    
def extract_patient(filename, directory):
    tar = tarfile.open(filename)
    tar.extractall(path=directory)
    tar.close()

    institution = os.path.join(directory, 'Institution')
    
    with open(institution) as file:
        lines = file.readlines()
        
    path = None
    patientname = None
    
    for line in lines:
        if "PatientPath" in line:
            path = line.split('=')[1].split('"')[1]
        if "\tName = " in line:
            patientname = line.split('=')[1].split('"')[1]
    if patientname:
        patientname = patientname.replace(" ","_")
    return (os.path.join(directory, path), patientname)



def export_all_to_DICOM(path, dest):
    os.makedirs(dest, exist_ok = True)
    pinnacle = PinnacleExport(path, logger=None)

    for image in pinnacle.images:
        pinnacle.export_image(image=image, export_path=dest)
                    
    for plan in pinnacle.plans:
        print(plan.plan_info['PlanName'])
        print(plan._path)
        pplan = PinnaclePlan(pinnacle, plan._path, plan.plan_info)
        ptrials=pplan.trials
        for i, trial in enumerate(ptrials):
            print(i, "---", trial['Name'])
            pinnacle.export_struct(pplan, export_path=dest)
            pinnacle.export_plan(pplan, export_path=dest)
            pinnacle.export_dose(pplan, export_path=dest)
            print()
        print()
    success = True
    return success


        
def makedir(inputdir, subdir):
    directory = os.path.join(inputdir, subdir)
    os.makedirs(directory, exist_ok = True)
    return directory



def browse(inputdir, withAria):
    filenames = glob.glob(os.path.join(inputdir, "*.tar"))

    tempodir = makedir(inputdir, "tempo")
    dcddir = makedir(inputdir, "dcd")
    donedir = makedir(inputdir, "done")
    unknowndir = makedir(inputdir, "unknown")
    faileddir = makedir(inputdir, "failed")
    DICOMdir = makedir(inputdir, "DICOM")

    for filename in filenames:
        path, patientname = extract_patient(filename, tempodir)
        
        if withAria:
            from patientNameToPath import patientNameToPath
            PID=filename.split('_')[-2]
            element=fetch_PatientInfo(PID)
            if not(element): # No such PID in Aria
                move(filename,unknowndir)
                continue
            else:
                patientdcm = patientNameToPath(element.LastName,
                                               element.FirstName,
                                               element.PatientId)
            if element.DeathDate:   # Patient DCD
                move(filename,dcddir)
                continue
        else:
            patientdcm = patientname

        if not(path): 
            sys.stderr.write( f"\nThe tarfile {filename}")
            sys.stderr.write( f"do not look like produced by Pinnacle!\n" )
            sys.exit(1)
        else:
            dest = os.path.join(DICOMdir, patientdcm)
            try:
                success = export_all_to_DICOM(path, dest)
            except:
                success = False
            erase(tempodir)
            
            if not( success):
                move(filename,faileddir)
                move(dest,faileddir)
                continue
           
            move(filename,donedir)
    
def usage():
    sys.stderr.write("\nFatal error: one need a directory name\n")
    sys.stderr.write("\nUsage:\n")
    sys.stderr.write("ConvertFromPinnacle.py batchdirectory [withAria]\n\n")
    sys.exit(1)
            
if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) < 2 :
        usage()
    elif len(sys.argv) > 3 :
        usage()
    else:
        inputdir=sys.argv[1]

        if len(sys.argv) == 3 :
            withAria = (sys.argv[2] == 'withAria')
            print("\nConverting in a directory consolidated with Aria...\n")
        else:
            withAria = False
            
        browse(inputdir, withAria)
        
        
        


                    
