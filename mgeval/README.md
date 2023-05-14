# mgeval
## Conference
- ### [mgeval](https://github.com/RichardYang40148/mgeval/blob/master/demo.ipynb)

### Updata
- version from python2 to python3
- python-midi
```commandline
pip install git+https://github.com/vishnubob/python-midi@feature/python3
```

## demo.ipynb

### Upload files

- [setup.py](https://github.com/vishnubob/python-midi/blob/master/setup.py)

- [mgeval_src.zip](https://github.com/JinchengLiang/DLproject/blob/Shaomin/mgeval/mgeval_src.zip)

- dataset1: [ChMusicMIDI.zip](https://github.com/JinchengLiang/DLproject/blob/Shaomin/dataset/ChMusicMIDI.zip)

- dataset2: [gen8bar.zip](https://github.com/JinchengLiang/DLproject/blob/Shaomin/dataset/gen8bar.zip)

## __main__.py

To evaluate two datasets.

```commandline
python . --set1dir <path/to/first/sample/directory> --set2dir <path/to/second/sample/directory> --outfile <output_filename> --num-bar <num_bar>
```
For example:
```commandline
python . --set1dir ../dataset/gen8bar --set2dir ../dataset/ChMusicMIDI8bar --outfile main_output --num_bar 8
```



