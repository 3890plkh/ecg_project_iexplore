#Gives us mean and sample standard deviation of accuracies for each model
import pandas as pd

data=pd.read_csv("Accuracies80.csv")
print("After {iterations} iterations".format(iterations=len(data)))
for model_type in data.columns:    
    print("{model} - Mean: {mean}%, SD: {sd}%".format(model=model_type,mean=round(data[model_type].mean(axis=0),2),sd=round(data[model_type].std(axis=0),2)))
