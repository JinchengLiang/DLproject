
import json
from argparse import ArgumentParser
import midi
import glob
import copy
import os
import numpy as np
import pretty_midi
from pprint import pprint
import pickle
from mgeval_src import core, utils
from sklearn.model_selection import LeaveOneOut

set1 = glob.glob(os.path.join('..', 'dataset', 'ChMusicMIDI', '*'))
set2 = glob.glob(os.path.join('..', 'dataset', 'gen8bar', '*'))

print('Evaluation sets (sample and baseline):')
# print(set1)
# print(set2)

if not any(set1):
  print("Error: sample set it empty")
  exit()

if not any(set2):
  print("Error: baseline set it empty")
  exit()

for i in range(1):
    _file = set2[i]
    pattern = midi.read_midifile(_file)
    print(f'pattern.format = {pattern.format}')
    print(f'pattern.resolution = {pattern.resolution}')
    for i, track in enumerate(pattern):
        print(f'pattern[{i}]--------------------')
        end = min(len(pattern[i]), 5) + 1
        print(pattern[i][:end])

    pm_object = pretty_midi.PrettyMIDI(_file)
    print(pm_object)
    print(f'pm_object.instruments = {pm_object.instruments}')
    piano_roll = pm_object.instruments[0].get_piano_roll(fs=100)
    piano_roll = np.transpose(piano_roll, (1, 0))
    print(f'piano_roll = \n{piano_roll}')
    print(f"piano_roll[piano_roll > 0] = {piano_roll[piano_roll > 0]}")
