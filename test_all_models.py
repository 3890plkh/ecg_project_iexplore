# Train all models on same data
# Run snippets.py first to create chunks
# mainly following this https://www.educative.io/answers/implement-neural-network-for-classification-using-scikit-learn

from sklearn import neural_network as nn
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
import os
import sys
import pandas as pd
from trainingDataSelector import *
import matplotlib.pyplot as plt
import time

#enter a percentage in command line
#if no percentage is entered in the command line, default to 80 percent of data to be used as training data
try:
    percentage=int(sys.argv[1])
except IndexError:
    percentage=80

#enter number of iterations in command line                         
#if no number is entered, default to 1
try:                      
    iterations=int(sys.argv[2])    
    if iterations<0:
        raise ValueError("Please input a positive number")                                                                                                                                        
except:
    iterations=1

#create dict to store accuracy for each model
#dict needs to be an empty array
models=["MLP","SVM","SGD","KNN","NC","DT"]
# copied from last comment on: https://stackoverflow.com/questions/34010312/appending-to-one-python-dictionary-key-appends-to-all-for-some-reason
accuracies= {key:[] for key in models}
precisionScores= {key:[] for key in models}
recallScores= {key:[] for key in models}
times={key:0 for key in models}

if os.path.isdir("Precision Data")==False:
    os.mkdir("Precision Data")
if os.path.isdir("Recall Data")==False:
    os.mkdir("Recall Data")

#turn conditions into numbers - so we can map snippets onto numbers
#https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
le = LabelEncoder()
if os.path.isdir("Chunks")==False:
    import snippets
le.fit(os.listdir("Chunks"))

#for rach iteration - create training data and train all models on that data
for i in range(iterations):
    print("Iteration " + str(i+1) + ":")
    #select training data - should be consistent for the iteration
    trainingFiles_snippets,trainingFiles_conditions,testFiles_snippets,testFiles_conditions=selectTrainingData(percentage)

    #For each model_type - ignore GaussianProcess for now - it takes a while
    for model_type in models:
        starttime=time.time()
        if model_type == "MLP":
            #default settings for the first MLPNN model - try playing around with it
            model=nn.MLPClassifier(activation="logistic",verbose=False,shuffle=True,learning_rate="adaptive",max_iter=1000)
            # verbose is turned off for consistency
        elif model_type == "SVM":
            model=svm.SVC()
        elif model_type == "SGD":
            model=SGDClassifier()
        elif model_type == "KNN":
            model=KNeighborsClassifier()
        elif model_type == "NC":  # low score
            model=NearestCentroid()
        elif model_type == "DT":
            model=DecisionTreeClassifier()

        #train the model (can feed the data in multiple times if you want)
        model.fit(np.abs(trainingFiles_snippets),le.transform(trainingFiles_conditions))

        endtime=time.time()
        times[model_type]+=(endtime-starttime)

        #test model 
        predictedConditions=model.predict(np.abs(testFiles_snippets))
        #calculate accuracy
        accuracy=accuracy_score(y_true=le.transform(testFiles_conditions),y_pred=predictedConditions)*100
        precisionScore=precision_score(y_true=le.transform(testFiles_conditions),y_pred=predictedConditions,average=None,zero_division=np.nan)*100
        recallScore=recall_score(y_true=le.transform(testFiles_conditions),y_pred=predictedConditions,average=None)*100
        #append accuracy score to the dict
        accuracies[model_type].append(accuracy)
        precisionScores[model_type].append(precisionScore)
        recallScores[model_type].append(recallScore)

        #progress report
        print("Iteration " + str(i+1) + " - Model " + model_type + " accuracy: " + str(accuracy))

accuracies=pd.DataFrame.from_dict(accuracies)
#if accuracy.csv exists append new data to end without adding header
accuracies.to_csv("Accuracies{percentage}.csv".format(percentage=str(percentage)),mode="a",sep=",",header= not os.path.isfile("Accuracies{percentage}.csv".format(percentage=str(percentage))),index=False)

#save precision and recall data
if iterations!=0:
    for model_type in models:
        #get precisions for every condition for that model
        precisionforModeltype=pd.DataFrame(precisionScores[model_type],columns=le.inverse_transform(range(len(precisionScores[model_type][0]))))
        precisionforModeltype.to_csv("Precision Data/Precisions{model}{percentage}.csv".format(model=model_type,percentage=str(percentage)),mode="a",sep=",",header= not os.path.isfile("Precision Data/Precisions{model}{percentage}.csv".format(model=model_type,percentage=str(percentage))),index=False)
        #get recalls for every condition for that model
        recallsforModeltype=pd.DataFrame(recallScores[model_type],columns=le.inverse_transform(range(len(recallScores[model_type][0]))))
        recallsforModeltype.to_csv("Recall Data/Recalls{model}{percentage}.csv".format(model=model_type,percentage=str(percentage)),mode="a",sep=",",header= not os.path.isfile("Recall Data/Recalls{model}{percentage}.csv".format(model=model_type,percentage=str(percentage))),index=False)

#total time taken to train each model
print("Total time to train {iterations} versions of each model".format(iterations=iterations))
print(times)

#create a histogram of all accuracy data 
edges=np.linspace(20,95,101,endpoint=True)
data=pd.read_csv("Accuracies{percentage}.csv".format(percentage=str(percentage)),sep=",")
for model in data.columns:
    plt.hist(data[model],bins=edges,label="{model}".format(model=model),alpha=0.8,histtype="bar",ec="black",stacked=False)

#testing accuracy if you just guessed N every time
total=0
for folder in os.listdir("Chunks"):
    total+=len(os.listdir(r"Chunks/{folder}".format(folder=folder)))

percentN=len(os.listdir("Chunks/N"))/total*100
plt.axvline(x=percentN, linestyle="--",label="Accuracy from guessing N everytime")

plt.grid()
plt.ylabel("Frequency")
plt.xlabel("Accuracy (%)")
plt.legend()
plt.title("Accuracy of selected different ML models trained on {iterations} different training datasets".format(iterations=len(data)))
plt.show()
