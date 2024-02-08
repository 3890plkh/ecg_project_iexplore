# ECG Project (Imperial I-Explore)

This is the project code for analysis of ECG data from the MIT-BIH Arrhythmia Database (can be found here: https://physionet.org/content/mitdb/1.0.0/). To read the data you will need to run the downloadall.py script which converts all of the data into a .csv format. There is also a script called snippets.py which creates snippets of ECG pulses of different types of heart conditions. How the heart condition is determined is from the annotations provided in the MIT-BIH Arrhythmia Database.

## What the Aims of the Project are

The potential aims of the project are to:
- do some basic ECG analysis (e.g. heart rate)
- train an ML model to detect heart defects from ECG data

## Prerequisites

You will need to download the wdfb Python package [1][2]. To install, run the command: 
```
pip install wfdb
```
in your terminal.

Documentation is available here: https://wfdb.readthedocs.io/en/latest/

Will also need the standard Python data processing libraries (numpy, pandas, scipy, matplotlib etc.). If you do not have these installed just run the above command but with whatever module you need to install.

## Notice
Contains information from MIT-BIH Arrhythmia Database (https://physionet.org/content/mitdb/1.0.0/) which is made available under the ODC Attribution License (https://physionet.org/content/mitdb/view-license/1.0.0/).

## References
1. Xie, C., McCullum, L., Johnson, A., Pollard, T., Gow, B., & Moody, B. (2023). Waveform Database Software Package (WFDB) for Python (version 4.1.0). PhysioNet. https://doi.org/10.13026/9njx-6322.
2. Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.






