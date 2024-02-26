#Please run snippets.py first to create chunks
#This code selects a percentage of the data to be used to train ML model and retains the rest for testing. 
#Currently we are Fourier transforming the data, can just keep the data in its normal form 
# (will probably be the next thing I try).

from scipy.fft import rfft
import pandas as pd
import os
import numpy as np
import random

#We have an issue where where snippets can have different lengths
#if we feed in our snippets as FFTs then this isn't an issue? - maybe something to try

#out of all of the snippets we have created, this function selects percentage% of the files from each folder
#to be used as training data
#several modes for different models
#mode "FT" - signals are converted into FFTs
#mode "raw" - keep data in raw voltage values
#returns 4 lists: training data signals, training data conditions, then test data signals and test data conditions
def selectTrainingData(percentage,mode):
    #if no chunks of ECG data created from "snippets.py", then run snippets
    if os.path.isdir("Chunks")!=True:
        import snippets

    #print proportions of data used as training or test data
    print("Training Data: {trainingpercent}% \nTest Data: {testpercent}%".format(trainingpercent=percentage,testpercent=100-percentage))
    if percentage>100 or percentage<=0:
        raise ValueError("Cannot select {percentage}% of data to train model".format(percentage=str(percentage)))

    trainingFiles_snippets=[]
    trainingFiles_conditions=[]
    testFiles_snippets=[]
    testFiles_conditions=[]
    #for each condition
    conditions=os.listdir("Chunks")
    #randomise which order the conditions they are fed into model
    random.shuffle(conditions)
    for folderName in conditions:
        #search the folder for that condition
        folder=os.listdir(r"Chunks\{folderName}".format(folderName=folderName))
        #randomise which data is used in the training dataset
        random.shuffle(folder)
        #calculate number of files to use
        filesToUse=percentage/100*len(folder)//1+1
        #loop through all snippets for that condition
        for i in range(len(folder)):
            snippetAsDataFrame=pd.read_csv(r"Chunks\{folderName}\{filename}".format(folderName=folderName, filename=folder[i]),usecols=[1])
            #i+1 is the number of files that will have been selected if we include this index in the training set
            #if it is greater than the number of files we intend to use, don't add it to the training set
            if i+1>filesToUse:
                if mode=="FT":
                    testFiles_snippets.append(rfft(snippetAsDataFrame[snippetAsDataFrame.columns[0]].to_numpy(dtype=object))[10:510])
                    testFiles_conditions.append(folderName)
                elif mode=="raw":
                    testFiles_snippets.append(snippetAsDataFrame[snippetAsDataFrame.columns[0]].to_numpy(dtype=object)[0:500])
                    testFiles_conditions.append(folderName)
            #else add to training set
            else:
                if mode=="FT":
                    trainingFiles_snippets.append(rfft(snippetAsDataFrame[snippetAsDataFrame.columns[0]].to_numpy(dtype=object))[10:510])
                    trainingFiles_conditions.append(folderName)
                elif mode=="raw":
                    trainingFiles_snippets.append(snippetAsDataFrame[snippetAsDataFrame.columns[0]].to_numpy(dtype=object)[0:500])
                    trainingFiles_conditions.append(folderName)
        #Progress indicator - prints message when snippets for a condition have been sorted into training and test sets
        print("'{folderName}' training data selected".format(folderName=folderName))
    
    return trainingFiles_snippets,trainingFiles_conditions,testFiles_snippets,testFiles_conditions