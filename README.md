# DLproject

Create config_data.py file below method2/config/, modify the path based on your own situation: 
![image](https://user-images.githubusercontent.com/121146314/236586335-9dbfde83-c20b-47f4-9850-99b913324ff2.png)
(p.s. I am not quite sure if the parameters are correct now.) 

## Data Processing
mid files -> utils/data_processing.py -> *.npy

They first crop the first DATA_CONFIG['bar'] bars from original data and compress them to bar\*ts_per_bar ticks, the compression_ratio=origin_tick_per_beat/data_tick_per_beat. Then get the pianoroll metric m (bar\*ts_per_bar x freq_range) and mr (containing the begin tick of notes). Finally concatenate m and mr based on the order of bars. The variable name is called 'bar_sample'.

The .npy file contains the 'bar_sample'. There are two .npy files used as inputs of the model, one is the source data which have no label and the other is chmusic data.

There should be a pre-process of the data, especially the chmusic, to crop the blank at the beginning of mid files.

## Training
The config files are in configs folder.
To implement the method2, run methods_2/train_classifier.py to train the classifier. Then run methods_2/train_one_hot.py to train the VAE.
