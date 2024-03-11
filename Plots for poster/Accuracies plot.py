#contains a tool for plotting the histogram for the 3 best ML Models 
import matplotlib.pyplot as plt
import pandas as pd
import sys

try:
    percentage=sys.argv[1]
except:
    percentage=80

#make sure you are in the main project directory not this directory
accuracies=pd.read_csv("Accuracies{percentage}.csv".format(percentage=str(percentage)))
axes=accuracies[["MLP","SVM","KNN"]].plot.hist(subplots=True,bins=40,sharex=True,ec="black",xlabel="Accuracy (%)",alpha=0.5)
axis=accuracies[["MLP","SVM","KNN"]].plot.hist(sharex=True,bins=40,ec="black",xlabel="Accuracy (%)",alpha=0.5)

i=0
for ax in axes:
    bottom,top=ax.get_ylim()
    ax.axvline(accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),color="k",linestyle="dotted",alpha=0.7)
    ax.text(x=accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),y=bottom+0.65*(top-bottom),s="Mean:   {mean}%".format(mean=round(accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),2)),horizontalalignment="center")
    bottom,top=axis.get_ylim()
    axis.axvline(accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),color="k",linestyle="dotted",alpha=0.7)
    axis.text(x=accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),y=bottom+1.02*(top-bottom), s="{mean}%".format(mean=round(accuracies[["MLP","SVM","KNN"][i]].mean(axis=0),2)),horizontalalignment="center")
    i+=1

plt.show()
