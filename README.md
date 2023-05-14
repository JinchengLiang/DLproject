# DLproject

## data_div.py
To split each MIDI file in a dataset to several MIDI files according to bar count per file.
```commandline
python data_div.py --setdir <path/to/dataset/directory> --outdir <path/to/outfiles/directory> --num_bar <num_bar>
```
For example
```commandline
python data_div.py --setdir ./dataset/ChMusicMIDI --outdir ./dataset/ChMusicMIDI8bar --num_bar 8
```


