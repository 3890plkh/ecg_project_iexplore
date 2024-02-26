#Playing with MLPNN from scikit-learn  
#This will automatically run snippets.py first to create chunks
# mainly following this https://www.educative.io/answers/implement-neural-network-for-classification-using-scikit-learn

from sklearn import neural_network as nn
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import os
import sys
from trainingDataSelector import *
import matplotlib.pyplot as plt

#We have an issue where where snippets can have different lengths
#if we feed in our snippets as FFTs then this isn't an issue? - maybe something to try

#enter a percentage in command line
#if no percentage is entered in the command line, default to 80 percent of data to be used as training data 
try:
    percentage=int(sys.argv[1])
except IndexError:
    percentage=80

#creates training data and test data
trainingFiles_snippets,trainingFiles_conditions,testFiles_snippets,testFiles_conditions=selectTrainingData(percentage)

#looking at what the FTs look like
def plotFT(number):
    plt.plot(np.arange(len(trainingFiles_snippets[number])),np.abs(trainingFiles_snippets[number]))
    plt.title("Fourier Transform of {condition} signal (index:{index})".format(condition=trainingFiles_conditions[number],index=number))
    plt.ylabel(r"$\log_{10}$ of Absolute value of Fourier Transform")
    plt.xlabel("Scaled Frequency")
    plt.grid()
    plt.show()

#plot some FTs
for i in np.linspace(10,len(trainingFiles_conditions)-15,num=14,endpoint=False):
    plotFT(int(i//1))

#turn conditions into numbers - so we can map snippets onto numbers
#https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
le = LabelEncoder()
le.fit(os.listdir("Chunks"))

#default settings for the first MLPNN model
model=nn.MLPClassifier(activation="tanh",verbose=True)

#You should not see this print message - if you do then some of the snippets aren't long enough
for i in range(len(trainingFiles_snippets)):
    if len(trainingFiles_snippets[i])<500:
        print("Fail : " + str(len(trainingFiles_snippets[i])))

#train the model
model.fit(np.abs(trainingFiles_snippets),le.transform(trainingFiles_conditions))

#test model 
predictedConditions=model.predict(np.abs(testFiles_snippets))
#calculate accuracy
accuracy=accuracy_score(y_true=le.transform(testFiles_conditions),y_pred=predictedConditions)*100
print("Accuracy of Model: " + str(accuracy))

#compare to just guessing N everytime
accuracy=accuracy_score(y_true=le.transform(testFiles_conditions),y_pred=le.transform(["N"]*len(testFiles_conditions)))*100
print("Guessing N everytime: "+ str(accuracy))