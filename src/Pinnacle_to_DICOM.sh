#!/bin/bash

for i in data/*; do
    line=`./src/InfoPatientPID.py $i;`
    PID=`echo ${line} | cut -f 1 -d '#'`
    LastName=`echo ${line} | cut -f 2 -d '#'`
    FirstName=`echo ${line} | cut -f 3 -d '#'`
    #echo ${line} | tr '\t' '#'
    outdir=./out/${LastName}_${FirstName}__$PID
    echo $line | tr '#' '\t'
    #pymedphys experimental pinnacle export -l $i > xxx
    cat xxx
    echo
    echo
    #pymedphys experimental pinnacle export -t Trial_1 $i -o $outdir
done

