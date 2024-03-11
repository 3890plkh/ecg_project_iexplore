#Gives us mean and sample standard deviation of accuracies, precisions and recall for each model
#please read what these numbers mean: https://scikit-learn.org/stable/modules/model_evaluation.html
#Will help us analyse where models are good and bad
#Also calculating a mean of precisions is a bit dubious (as discussed below)
import pandas as pd
import sys 

try:
    percentage=sys.argv[1]
except:
    percentage=80

#
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
    recallstats=pd.DataFrame({"Mean":recalldata.mean(), "SD": precisiondata.std()})
    print("Recall statistics:")
    print(recallstats.T.round(2).to_string(index=True))
    print("\n")
