# DLproject

## mgeval

### [demo.ipynb](https://github.com/JinchengLiang/DLproject/blob/Shaomin/mgeval/demo.ipynb)

#### Upload files

[setup.py](https://github.com/vishnubob/python-midi/blob/master/setup.py)

[mgeval_src.zip](https://github.com/JinchengLiang/DLproject/blob/Shaomin/mgeval/mgeval_src.zip)

dataset1: [ChMusicMIDI.zip](https://github.com/JinchengLiang/DLproject/blob/Shaomin/dataset/ChMusicMIDI.zip)

dataset2: [gen8bar.zip](https://github.com/JinchengLiang/DLproject/blob/Shaomin/dataset/gen8bar.zip)

### __main__.py

You can run mgeval as a standalone module with the following command on the root directory:
```linux
python . --set1dir <path/to/first/sample/directory> --set2dir <path/to/second/sample/directory> --outfile <output_filename> --num-bar <num_bar>
```
For example:
```commandline
python3 . --set1dir ../dataset/gen8bar --set2dir ../dataset/ChMusicMIDI --outfile main_output --num_bar 150
```
Note: num_bar >= max(actual_bar)