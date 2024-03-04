# Playing with MLPNN from scikit-learn  
# This will automatically run snippets.py first to create chunks
# mainly following this https://www.educative.io/answers/implement-neural-network-for-classification-using-scikit-learn

from sklearn.linear_model import LinearRegression
from sklearn import neural_network as nn
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
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

#enter a mode in command line
#if no mode is entered, default to "FT" as this works
try:
    mode=sys.argv[2]
except IndexError:
    mode="FT"

#enter a model type in command line
#if no model type is entered, default to "MLP" as this works
try:
    model_type=sys.argv[3]
except IndexError:
    model_type="LR"


#creates training data and test data
trainingFiles_snippets,trainingFiles_conditions,testFiles_snippets,testFiles_conditions=selectTrainingData(percentage,mode)

#-------------------------------------------------------------------------
#FT mode checks

#looking at what the FTs look like
def plotFT(number):
    plt.plot(np.arange(len(trainingFiles_snippets[number])),np.abs(trainingFiles_snippets[number]))
    plt.title("Fourier Transform of {condition} signal (index:{index})".format(condition=trainingFiles_conditions[number],index=number))
    plt.ylabel("Absolute value of Fourier Transform")
    plt.xlabel("Scaled Frequency")
    plt.grid()
    plt.show()

#plot some FTs (comment this out if you don't want to see the plots)
'''
if mode=="FT":
    for i in random.sample(range(len(trainingFiles_snippets)),10):
        plotFT(int(i))
'''
#You should not see this print message - if you do then some of the snippets aren't long enough
#if mode=="FT":
#    for i in range(len(trainingFiles_snippets)):
#        if len(trainingFiles_snippets[i])<500:
#            print("Fail : " + str(len(trainingFiles_snippets[i])))

#------------------------------------------------------------------------------------

#turn conditions into numbers - so we can map snippets onto numbers
#https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
le = LabelEncoder()
le.fit(os.listdir("Chunks"))

#Form model  with its model_type
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
elif model_type == "GP":  # take forever to run
    model=GaussianProcessClassifier()
elif model_type == "DT":
    model=DecisionTreeClassifier()
elif model_type == "LR":
    model=LinearRegression()
else:
    raise NameError("Unsupported model type")

#train the model (can feed the data in multiple times if you want)
model.fit(np.abs(trainingFiles_snippets),le.transform(trainingFiles_conditions))

#test model 
predictedConditions=model.predict(np.abs(testFiles_snippets))
#calculate accuracy
accuracy=accuracy_score(y_true=le.transform(testFiles_conditions),y_pred=predictedConditions)*100
print("Accuracy of " + model_type + " Model: " + str(round(accuracy,2)) +"%")

#compare to just guessing N every time
accuracy=accuracy_score(y_true=le.transform(testFiles_conditions),y_pred=le.transform(["N"]*len(testFiles_conditions)))*100
print("Accuracy of guessing N every time: "+ str(round(accuracy,2)) +"%")
