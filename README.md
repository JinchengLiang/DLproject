# DLproject
## Reference
- ### [jazz_melody_generation](https://github.com/annahung31/jazz_melody_generation)
### Updata
- version from python2 to python3
- python-midi
```commandline
pip install git+https://github.com/vishnubob/python-midi@feature/python3
```

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

## datasets
[Lakh MIDI](https://paperswithcode.com/dataset/lakh-midi-dataset)

[ChMusic](https://paperswithcode.com/dataset/chmusic)

[ChMusicMIDI, ChMusicMIDI8bar, gen8bar](https://github.com/JinchengLiang/DLproject/tree/Shaomin/dataset)



