#Gives us mean and sample standard deviation of accuracies, precisions and recall for each model
#please read what these numbers mean: https://scikit-learn.org/stable/modules/model_evaluation.html
#Will help us analyse where models are good and bad
#Also calculating a mean of precisions is a bit dubious (as discussed below)
import pandas as pd
import sys 
import os
import matplotlib.pyplot as plt
import numpy as np

try:
    percentage=sys.argv[1]
except:
    percentage=80

if os.path.isdir(r"Plots for poster/Plots")!=True:
    os.mkdir(r"Plots for poster/Plots")

#create a dict for each condition
conditions=os.listdir("Chunks")
conditionsdict={condition:{} for condition in conditions}
for condition in conditions:
    ((conditionsdict[condition])["Precision Means"])={}
    ((conditionsdict[condition])["Precision SD"])={}
    ((conditionsdict[condition])["Recall Means"])={}
    ((conditionsdict[condition])["Recall SD"])={}

accuracydata=pd.read_csv("Accuracies{percentage}.csv".format(percentage=str(percentage)))
print("After {iterations} iterations:\nAccuracy Statistics".format(iterations=len(accuracydata)))
for model_type in accuracydata.columns:
    #fine to calculate mean accuracy in this way
    #For the same percentage of training data, same number of test sets will be selected for each iteration
    #so accuracy for each iteration is (correctly assigned test sets)/(number of test sets per iteration).
    #So mean of the accuracies is 1/iterations*( sum of ((correctly assigned test sets)/(number of test sets per iteration)))
    #Since denominators are the same in the sum of ((correctly assigned test sets)/(number of test sets per iteration)),
    #then the sum is (total correctly assigned test sets)/(number of test sets per iteration)
    #and mean is (total correctly assigned test sets)/(total number of test sets)
    #so it is as if we calculated accuracy for alls iterations summed up
    print("{model} - Mean: {mean}%, SD: {sd}%".format(model=model_type,mean=round(accuracydata[model_type].mean(axis=0),2),sd=round(accuracydata[model_type].std(axis=0),2)))

print("\n")

for model_type in accuracydata.columns:
    precisiondata=pd.read_csv("Precision Data/Precisions{model}{percentage}.csv".format(model=model_type,percentage=str(percentage)))
    recalldata=pd.read_csv("Recall Data/Recalls{model}{percentage}.csv".format(model=model_type,percentage=str(percentage)))
    print("{model} - After {iterations} iterations".format(model=model_type,iterations=len(precisiondata)))
    #for precision data calculating the mean is a bit questionable, as they might not be equally weighted
    # since model might not predict same number of that condition each iteration
    precisionstats=pd.DataFrame({"Mean":precisiondata.mean(),"SD": precisiondata.std()})
    print("Precision statistics:")
    print(precisionstats.T.round(2).to_string(index=True))
    
    #as per accuracies, calculating mean for recalls is fine as 
    # there should be same number of files for each condition for the same percentage
    recallstats=pd.DataFrame({"Mean":recalldata.mean(), "SD": recalldata.std()})
    print("Recall statistics:")
    print(recallstats.T.round(2).to_string(index=True))
    print("\n")
    for condition in conditions:
        ((conditionsdict[condition])["Precision Means"])[model_type]=precisiondata[condition].mean()
        ((conditionsdict[condition])["Precision SD"])[model_type]=precisiondata[condition].std()
        ((conditionsdict[condition])["Recall Means"])[model_type]=recalldata[condition].mean() 
        ((conditionsdict[condition])["Recall SD"])[model_type]=recalldata[condition].std()

#create model recall and precision plot for all conditions
for condition in conditions:
    plt.figure()
    xs=np.arange(len(((conditionsdict[condition])["Precision Means"]).keys()))
    plt.ylim(0,110)
    width=1
    plt.bar(3*xs,((conditionsdict[condition])["Precision Means"]).values(),width=width,ec="Black",color="CornflowerBlue",label="Precision Means")
    plt.bar(3*xs+width,((conditionsdict[condition])["Recall Means"]).values(),width=width,ec="Black",color="orange",label="Recall Means")
    count=0
    #if precision is nan i.e. model never guessed this condition, replace with black crossed hatched bar
    for i in ((conditionsdict[condition])["Precision Means"]).values():
        if np.isnan(i)==True:
            plt.bar(3*count,110,width=width,color="white",hatch="//",label="Model never guesses {condition}".format(condition=condition))
        count+=1
    plt.title("{condition} - Recall and Precision Data for each Model".format(condition=condition))
    plt.xticks((3*xs+(3*xs+width))/2,((conditionsdict[condition])["Precision Means"]).keys())
    plt.legend()
    plt.savefig(r"Plots for poster/Plots/{condition}_PrecisionandRecall".format(condition=condition),dpi=1000)
    plt.close()