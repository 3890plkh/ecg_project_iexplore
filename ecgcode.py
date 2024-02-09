# code to see what the wfdb module does, it's a bit messy
# Please read the docs: https://wfdb.readthedocs.io/en/latest/

import wfdb as wfdb
import pandas as pd
import os
import matplotlib.pyplot as plt

#plots first 2000 samples for a given patient
def plot(patient):
    record=wfdb.rdrecord(record_name=patient ,pn_dir="mitdb",sampfrom=0,sampto=2000)
    ann=wfdb.rdann(patient,extension="atr" ,sampfrom=0, sampto=2000, pn_dir="mitdb",shift_samps=True)
    #they have their own plotter function
    wfdb.plot_items(record.p_signal, ann_samp=[ann.sample, ann.sample],time_units="seconds",fs=1000,ecg_grids="all",sig_units=["mV","mV"], title="Patient {patient}".format(patient=patient))
    print(ann.aux_note)

#messing about with annotation files
def annotations(patient):
    #reads annotation from mitdb database
    ann=wfdb.rdann(patient,extension="atr" , pn_dir="mitdb" , return_label_elements=["symbol"])
    #returns sample number associated with each annotation
    print(ann.sample)
    #this contains information about heart rhythm changes, used in snippets.py
    print(ann.aux_note)

#MUST RUN "snippets.py" BEFORE USING THIS
#produces a plot of both channels of a snippet of a given heart condition 
def plotCondition(Condition,starttime,finishtime):
    file=os.listdir(r"Chunks\{Condition}".format(Condition=Condition))[9]
    data=pd.read_csv(r"Chunks\{Condition}\{file}".format(Condition=Condition,file=file))
    #can change parameters of what part of snippet you want to plot depending on the file
    datachunk=data[(data["time"]<finishtime) & (data["time"]>starttime)]
    #create figure containing 2 graphs
    fig, ((ax1),(ax2))=plt.subplots(nrows=len(data.columns)-1,ncols=1,sharex=True)

    #plot each channel
    ax1.plot(datachunk["time"],datachunk["MLII"])
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Channel: MLII")
    ax1.grid()

    ax2.plot(datachunk["time"],datachunk["V1"])
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Channel: V1")
    ax2.grid()

    #title tells you which file was plotted
    fig.suptitle("{Condition} - {file}".format(Condition=Condition,file=file))
    plt.show()

#plot("203")
#annotations("203")

plotCondition("AFIB",1,6)