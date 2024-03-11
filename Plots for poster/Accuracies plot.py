#contains a tool for plotting the histogram for the 3 best ML Models 
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

try:
    percentage=sys.argv[1]
except:
    percentage=80

if os.path.isdir(r"Plots for poster/Plots")!="True":
    os.mkdir(r"Plots for poster/Plots")

#make sure you are in the main project directory not this directory
accuracies=pd.read_csv("Accuracies{percentage}.csv".format(percentage=str(percentage)))
axes=accuracies[["MLP","SVM","KNN"]].plot.hist(subplots=True,bins=60,sharex=True,ec="black",xlabel="Accuracy (%)",alpha=0.5)

i=0
for ax in axes:
    bottom,top=ax.get_ylim()
    ax.axvline(accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),color="k",linestyle="dotted",alpha=0.7)
    ax.text(x=accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),y=bottom+0.65*(top-bottom),s="Mean:   {mean}%".format(mean=round(accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),2)),horizontalalignment="center")
    i+=1
    
plt.savefig(r"Plots for poster/Plots/hist_accuracies_sep.png",dpi=1000)
plt.show()

axis=accuracies[["MLP","SVM","KNN"]].plot.hist(sharex=True,bins=60,ec="black",xlabel="Accuracy (%)",alpha=0.5)
bottom,top=axis.get_ylim()
for model in ["MLP","SVM","KNN"]:
    axis.axvline(accuracies[model].mean(axis=0),color="k",linestyle="dotted",alpha=0.7)
    axis.text(x=accuracies[model].mean(axis=0),y=bottom+1.02*(top-bottom), s="{mean}%".format(mean=round(accuracies[model].mean(axis=0),2)),horizontalalignment="center")
plt.savefig(r"Plots for poster/Plots/hist_accuracies.png",dpi=1000)
plt.show()

