# ECG Project (Imperial I-Explore)

This is the project code for analysis of ECG data from the MIT-BIH Arrhythmia Database (can be found here: https://physionet.org/content/mitdb/1.0.0/). 

This repository contains the following code:
* mplnn_test0.py - first attempt at creating a working ML model. The ECG signals are fed in as a Fourier transforms. You can specify what percentage of the data should be used for training the ML model from the command line (if you don't specify a percentage, 80% of the data will be used for training as default).
* test_all_models.py - Randomises which files to use as training data. Trains all models using that same data and calculate accuracy, precision and recall scores for each model. The code can create multiple random training datasets and train all models on each of these datasets. Plots a histogram of the accuracy scores.
* Plots for poster\Accuracies plot.py - plots histograms of the accuracies data for the MLP, KNN and SVM models. Saves plots as .png file in Plots for poster\Plots.
* Plots for poster\Model stats.py - calculate mean precision and recall scores for different models and plots the precision and recall scores of each model for each condition. Saves plots as .png file in Plots for poster\Plots.

## What the Aims of the Project are

The potential aims of the project are to:
- do some basic ECG analysis (e.g. heart rate)
- train an ML model to detect heart defects from ECG data

## Prerequisites

You will need to download the wdfb Python package to be able to deal with the format the ECG signals are stored in [1][2]. Also we are currently intending on using the multi-layered perceptron neural network (MLPNN) model from the python module scikit-learn for classification of ECG signals [3]. To install both modules, run the command: 
```
pip install wfdb scikit-learn
```
in your terminal.

Documentation for wfdb module is available here: https://wfdb.readthedocs.io/en/latest/

Documentation for the MLPNN model is available here: https://scikit-learn.org/stable/modules/neural_networks_supervised.html#multi-layer-perceptron

Will also need the standard Python data processing libraries (numpy, pandas, scipy, matplotlib etc.). If you do not have these installed just run the above command but with whatever module you need to install.

## Running the Code
You just need to run the mlpnn_test0.py or the test_all_models.py script, it should run all of the other necessary scripts from this repository for you.

You can input command line arguments for both scripts.

For mlpnn_test0.py, after the script name, you are able to specify the command line arguments:
```
percentage model_type
```
percentage specifies the % of data to be used for training the model. You can see all of the possible options for the ML models in the code. Default parameters that will be used if none are specified are 80 MLP.

For test_all_models.py, after the script name, you are able to specify the command line arguments :
```
percentage iterations
```
percentage specifies the % of data to be used for training the model, iterations specifies which how many random datasets are generated. Default parameters that will be used if none are specified are 80 1.

## Notice
Contains information from MIT-BIH Arrhythmia Database (https://physionet.org/content/mitdb/1.0.0/) which is made available under the ODC Attribution License (https://physionet.org/content/mitdb/view-license/1.0.0/).

## References
1. Xie, Chen, et al. "Waveform Database Software Package (WFDB) for Python" (version 4.1.0). PhysioNet (2023), https://doi.org/10.13026/9njx-6322.
2. Goldberger, A., et al. "PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220." (2000).
3. Scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011