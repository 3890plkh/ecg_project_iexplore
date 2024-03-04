# This is a script that downloads all data from the MIT-BIH Arrhythmia Database and converts it to a CSV format 

import wfdb as wfdb
import pandas as pd
import numpy as np
import os

# Go through all patient records
for patient in [100,101,102,103,104,105,106,107,108,109,111,112,113,114,115,116,117,118,119,121,122,123,124,200,201,202,203,205,207,208,209,210,212,213,214,215,217,219,220,221,222,223,228,230,231,232,233,234]:
    #read both the signal (which is a 2D array) and the fields to tell us the info about the data and patient
    sig,fields= wfdb.rdsamp(str(patient), pn_dir="mitdb")
    #create empty dict
    data = {}
    #convert sample number to time assuming equal time intervals
    data["time"]=np.linspace(start=0,stop=fields["sig_len"]/fields["fs"],num=fields["sig_len"])
    #for every channel
    for i in range(len(fields["sig_name"])):
        #create a column for that channel
        data["{channel}".format(channel=fields["sig_name"][i])]=sig[:,i]
    #create data frame of the signals
    data=pd.DataFrame.from_dict(data)
    #if folder "Patient data" doesn't exist create one
    if os.path.isdir("Patient data")!=True:
        os.mkdir("Patient data")
    #coverts dataframe to csv and saves in path specified (change path if required)
    data.to_csv(path_or_buf=r"Patient data/{patient}.csv".format(patient=patient),sep=",",index=False)