# DLproject
## Abstract
We present the transfer learning approach for automatic traditional Chinese music melody generation, inspired by [jazz_melody_generation](https://github.com/annahung31/jazz_melody_generation). We made improvements to the model to make it effective on traditional Chinese music with fewer datasets and also replaced the component in the model with the popular artiecture such as transformer.

## Datasets
[Lakh MIDI](https://paperswithcode.com/dataset/lakh-midi-dataset) for source data.

[ChMusic](https://paperswithcode.com/dataset/chmusic) for target data.

## Data Process
Modify the config of data in ```config_data.py```. Run ```data_processing.py``` to obtain the input metric which is saved in a ```.npy``` file. The type of the original data should be ```.midi```, please convert your data to ```.midi``` first if necessary.

## Train the Classifier
Train the classifier by runing ```train_classifier.py```. The hyperparameters can be modified in ```config_classifier.py```.

## Train the VAE
Train the VAE by runing ```train_one_hot.py```. The hyperparameters can be modified in ```config_vae_one_hot.py```.
For the VAE with GRU, the hyperparameter ```model``` should be ```VAE_one_hot```.
For the VAE with transformer, the hyperparameter ```model``` should be ```VAE_attention```.

## Generate
Generate music by running ```generate.py```. When generating Chinesem music melody, ```y=[0,1]```. Otherwise, ```y=[1,0]```.



## data_div.py
To split each MIDI file in a dataset to several MIDI files according to bar count per file.
```commandline
python data_div.py --setdir <path/to/dataset/directory> --outdir <path/to/outfiles/directory> --num_bar <num_bar>
```
For example
```commandline
python data_div.py --setdir ./dataset/ChMusicMIDI --outdir ./dataset/ChMusicMIDI8bar --num_bar 8
```

## mgeval
### Reference
- #### [mgeval](https://github.com/RichardYang40148/mgeval/blob/master/demo.ipynb)

### Update
- version from python2 to python3
- python-midi
```commandline
pip install git+https://github.com/vishnubob/python-midi@feature/python3
```

### demo.ipynb

#### Upload files

- [setup.py](https://github.com/vishnubob/python-midi/blob/master/setup.py)

- [mgeval_src.zip](https://github.com/JinchengLiang/DLproject/tree/Shaomin/mgeval)

- dataset1: [ChMusicMIDI.zip](https://github.com/JinchengLiang/DLproject/tree/Shaomin/dataset)

- dataset2: [gen8bar.zip](https://github.com/JinchengLiang/DLproject/tree/Shaomin/dataset)

### __main__.py

To evaluate two datasets.

```commandline
python . --set1dir <path/to/first/sample/directory> --set2dir <path/to/second/sample/directory> --outdir <output_dirname> --num-bar <num_bar>
```
For example:
```commandline
python . --set1dir ../dataset/gen8bar --set2dir ../dataset/ChMusicMIDI8bar --outdir main_output --num_bar 8
```
If you use defualt values, you can just run __main__.py.

### main_output

The outputs of the best model in our experience are in `main_output` directory.



[ChMusicMIDI, ChMusicMIDI8bar, gen8bar](https://github.com/JinchengLiang/DLproject/tree/Shaomin/dataset)



