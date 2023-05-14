import os
from argparse import ArgumentParser

from midiutil import MIDIFile
import glob
from copy import deepcopy
import sys
from method_2.utils.midi_io.src.core_midi import midi_parser

parser = ArgumentParser()
parser.add_argument('--setdir', required=True, type=str,
                    help='Path (absolute) to the dataset (folder)')

parser.add_argument('--outdir', required=True, type=str,
                    help='Path (absolute) where the output dataset will be stored')

parser.add_argument('--num_bar', required=True, type=int,
                    help='Number of bars to account for during processing')

args = parser.parse_args()

mid_set = glob.glob(os.path.join(args.setdir, '*.mid'))

if not any(mid_set):
  print("Error: sample set is empty")
  exit()

num_mid_file = 0
for mid_file in mid_set:
    filename = os.path.basename(mid_file)
    filename_without_ext = os.path.splitext(filename)[0]
    mid = midi_parser.MidiFile(mid_file)
    notes = mid.instruments[0].notes
    ticks_num_bar = mid.ticks_per_beat * 4 * args.num_bar
    div_mids = {}
    for note in notes:
        start_bar = note.start // ticks_num_bar
        end_bar = note.end // ticks_num_bar
        if start_bar == end_bar:    # This note is all in one 8 bars
            new_note = deepcopy(note)
            new_note.start = new_note.start - start_bar * ticks_num_bar
            new_note.end = new_note.end - start_bar * ticks_num_bar
            if start_bar not in div_mids.keys():
                div_mids[start_bar] = [new_note]
            else:
                div_mids[start_bar].append(new_note)
        else:
            assert 0 <= end_bar-start_bar < ticks_num_bar
            new_note0 = deepcopy(note)
            new_note0.start = new_note0.start - start_bar * ticks_num_bar
            new_note0.end = ticks_num_bar - 1

            new_note1 = deepcopy(note)
            new_note1.start = 0
            new_note1.end = new_note1.end - (start_bar + 1) * ticks_num_bar
            if start_bar not in div_mids.keys():
                div_mids[start_bar] = [new_note0]
            else:
                div_mids[start_bar].append(new_note0)
            if start_bar + 1 not in div_mids.keys():
                div_mids[start_bar + 1] = [new_note1]
            else:
                div_mids[start_bar + 1].append(new_note1)

    for bar, note_list in div_mids.items():
        track = 0
        channel = 0
        tempo = 120  # In BPM

        new_midi = MIDIFile(1, deinterleave=False, eventtime_is_ticks=True)  # One track, defaults to format 1 (tempo track
        # automatically created)
        new_midi.addTempo(track, 0, tempo)
        for note in note_list:
            new_midi.addNote(track, channel, note.pitch, note.start, note.end-note.start, note.velocity)

        outfilename = f"{filename_without_ext}_{bar}.mid"
        outfilepath = os.path.join(args.outdir, outfilename)
        # create directory if it does not exist
        os.makedirs(os.path.dirname(outfilepath), exist_ok=True)
        with open(outfilepath, "wb") as output_file:
            new_midi.writeFile(output_file)
        num_mid_file += 1

    #print("debug")

print(f'num_mid_file = {num_mid_file}')
