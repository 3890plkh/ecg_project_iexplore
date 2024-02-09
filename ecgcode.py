#code to see what the wfdb module does

import wfdb as wfdb
from wfdb import processing
import pandas as pd
import os
import matplotlib.pyplot as plt

#plots first 2000 samples for a given patient
def plot(patient):
    record=wfdb.rdrecord(record_name=patient ,pn_dir="mitdb",sampfrom=0,sampto=2000)
    ann=wfdb.rdann(patient,extension="atr" ,sampfrom=0, sampto=2000, pn_dir="mitdb",shift_samps=True)
    wfdb.plot_items(record.p_signal, ann_samp=[ann.sample, ann.sample],time_units="seconds",fs=1000,ecg_grids="all",sig_units=["mV","mV"], title="Patient {patient}".format(patient=patient))
    print(ann.aux_note)

#messing about with annotation files
def annotations(patient):
    ann=wfdb.rdann(patient,extension="atr" , pn_dir="mitdb" , return_label_elements=["symbol"])
    print(ann.sample)

#MUST RUN "snippets.py" BEFORE USING THIS
def plotCondition(Condition):
    file=os.listdir(r"Chunks\{Condition}".format(Condition=Condition))[0]
    data=pd.read_csv(r"Chunks\{Condition}\{file}".format(Condition=Condition,file=file),usecols=[0,1])
    #can change parameters of what times you want to plot depending on the file
    datachunk=data[(data["time"]<1.5) & (data["time"]>0)]
    #plots one channel
    plt.plot(datachunk["time"],datachunk["MLII"],)
    #title tells you which file was plotted
    plt.title("{Condition} - {file}".format(Condition=Condition,file=file))
    plt.grid()
    plt.show()

#plot("203")


#sig1,fields1=wfdb.rdsamp(record_name="100" ,pn_dir="mitdb",sampfrom=0,sampto=2000)
#sig2,fields2=wfdb.rdsamp(record_name="100" ,pn_dir="mitdb",sampfrom=1,sampto=2000)
#print(len(sig1),len(sig2))

#annotations("203")

plotCondition("VT")



