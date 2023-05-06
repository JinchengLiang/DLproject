# DLproject

Create config_data.py file below method2/config/, modify the path based on your own situation: 
![image](https://user-images.githubusercontent.com/121146314/236586335-9dbfde83-c20b-47f4-9850-99b913324ff2.png)
(p.s. I am not quite sure if the parameters are correct now.) 

## Data Processing
mid files -> utils/data_processing.py -> *.npy

The .npy file contains the pianoroll metrics. There are two .npy files used as inputs of the model, one is the source data which have no label and the other is chmusic data.

## Training
The config files are in configs folder.
To implement the method2, run methods_2/train_classifier.py to train the classifier. Then run methods_2/train_one_hot.py to train the VAE.
