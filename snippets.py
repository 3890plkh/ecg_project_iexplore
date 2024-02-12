#The intention of this script is to create small snippets of ecg pulses 
#that have been described as being characteristic of a certain condition in the database

#please refer to the following resources for understanding the output of this script:
# Code for dealing with annotations: https://wfdb.readthedocs.io/en/latest/io.html#wfdb-annotations
# What each annotation means (please take note of this): https://archive.physionet.org/physiobank/annotations.shtml
# Online way to view annotations (need to select mitdb database and "show annotations as text"): https://archive.physionet.org/cgi-bin/atm/ATM

import wfdb as wfdb
import os
import numpy as np
import pandas as pd
from collections import Counter

#takes an index of start and end of heart rhythm then converts to csv 
def convertToSnippet(samplefrom,sampleto,sig,fields,condition,patient):
    #create empty dict
    data = {}
    #convert sample number to time assuming equal time intervals
    data["time"]=np.linspace(start=0,stop=(sampleto-samplefrom)/fields["fs"],num=sampleto-samplefrom)
    #for every channel
    for i in range(len(fields["sig_name"])):
        #create a column for that channel
        data["{channel}".format(channel=fields["sig_name"][i])]=sig[samplefrom:sampleto,i]
    #create data frame of the signals
    data=pd.DataFrame.from_dict(data)
    #if folder chunks doesn't exist create one
    if os.path.isdir(r"Chunks")!=True:
        os.mkdir("Chunks")
    #if folder for that condition doesn't exist, create one
    if os.path.isdir(r"Chunks\{condition}".format(condition=condition))!=True:
        os.mkdir(r"Chunks\{condition}".format(condition=condition))
    #if there already is a snippet for this heart condition for this patient, pandas to_csv overwrites it
    #need to add a number
    count=1
    for file in os.listdir(r"Chunks\{condition}".format(condition=condition)):
        #if this patient already has snippet in file
        if str(patient) in file:
            count+=1
    #coverts dataframe to csv and saves in path specified 
    data.to_csv(path_or_buf=r"Chunks\{condition}\{patient}({count}).csv".format(patient=patient,condition=condition,count=count),sep=",",index=False)


#go through each patient file
for patient in [100,101,102,103,104,105,106,107,108,109,111,112,113,114,115,116,117,118,119,121,122,123,124,200,201,202,203,205,207,208,209,210,212,213,214,215,217,219,220,221,222,223,228,230,231,232,233,234]:
    #find the sample and annotation file
    sig,fields= wfdb.rdsamp(str(patient), pn_dir="mitdb")
    ann=wfdb.rdann(str(patient) , extension="atr", pn_dir="mitdb" , return_label_elements=["symbol"])
        
    #this is a test to see if we create the correct number of snippets of each condition for each patient
    print(Counter(ann.aux_note).keys())
    print(Counter(ann.aux_note).values())
        
    #search through the aux notes to find when a new heart beat rhythm has started
    #index where heartbeat rhythm starts and ends
    startIndex=0
    endIndex=0
    for i in range(len(ann.aux_note)):
        #if the heart beat rhythm is deemed to have changed, then aux_note isn't an empty string
        if ann.aux_note[i]!="":
            #if we are at start of data, this is an edge case
            if i==0:
                continue
            #if the heart rhythm is in middle of data set
            else:
                #the index before i is the last sample where we are in previous type of rhythm 
                endIndex=i-1
                #this is the sample number where previous type of rhythm starts and ends
                startsample=ann.sample[startIndex]
                endsample=ann.sample[endIndex]
                #code for the type of heart beat
                condition=(ann.aux_note[startIndex].replace("(","")).replace("\x00","")
                #create snippet
                convertToSnippet(startsample,endsample,sig,fields,condition,patient)
                #then set start index to be i where different aux_note has been read
                startIndex=i
        #if we reach the end of the data, set endIndex to be i 
        elif i==len(ann.aux_note)-1:
            endIndex=i
            #this is the sample number where this last type of rhythm starts and ends
            startsample=ann.sample[startIndex]
            endsample=ann.sample[endIndex]
            #code for the type of heart beat
            condition=(ann.aux_note[startIndex].replace("(","")).replace("\x00","")
            #create snippet
            convertToSnippet(startsample,endsample,sig,fields,condition,patient)

#thanks to a slight formatting anomaly where first sample is bad so wasn't labeled
#record 106 creates a ghost file in the chunks folder with 0 entries, so need to delete this
for file in os.listdir("Chunks"):
    if "106" in file:
        os.remove(r"Chunks\{file}".format(file=file))