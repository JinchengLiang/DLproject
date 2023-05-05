# import pretty_midi
# import pypianoroll
# from pypianoroll import Multitrack, Track
#
# # Load MIDI file
# midi_data = pretty_midi.PrettyMIDI('Take_Me.mid')
#
# # Get time signature changes
# time_signature_changes = midi_data.time_signature_changes
#
# # Iterate through time signature changes
# for i, ts in enumerate(time_signature_changes):
#     # Get the time of the current time signature change
#     time = ts.time
#     # Calculate the bar number based on the time signature changes
#     bar = i + time // ts.numerator
#     print(f"Bar {bar+1}: {ts.numerator}/{ts.denominator}")
#
# # Assume first time signature change is the main one
# main_time_signature = time_signature_changes[0]
#
# # Calculate the number of time steps per bar
# steps_per_bar = main_time_signature.numerator * midi_data.resolution
#
# print(f"Time steps per bar: {steps_per_bar}")
#
# # Get the lowest and highest MIDI notes in the file
# lowest_note = 127
# highest_note = 0
# for instrument in midi_data.instruments:
#     for note in instrument.notes:
#         if note.pitch < lowest_note:
#             lowest_note = note.pitch
#         elif note.pitch > highest_note:
#             highest_note = note.pitch
#
# # Calculate the pitch range
# pitch_range = highest_note - lowest_note + 1
#
# print(f"Pitch range: {pitch_range}")
#
# # Print the time steps per beat and time steps per bar
# print(f"Time steps per beat: {midi_data.resolution}")
#
#
# # # Get time division and ticks per beat
# # time_division = midi_data.time_signature_changes[0].denominator
# # ticks_per_beat = midi_data.tick_to_time(1) * time_division
# #
# # # Set time resolution to 16 time steps per bar (4 time steps per beat)
# # time_steps_per_bar = 16
# # ticks_per_bar = ticks_per_beat * 4
# # # beat_resolution = int(ticks_per_bar / time_steps_per_bar)
# # beat_resolution = 64
# #
# # # Set pitch range to 48 (from C3 to B6)
# # pitch_range = range(48, 96)
# #
# # # Create pianoroll
# # # pianoroll = midi_data.get_piano_roll(fs=beat_resolution, times=None, pedal=False, pitch_bend=False)[pitch_range, :time_steps_per_bar*4]
# # pianoroll = midi_data.get_piano_roll(fs=beat_resolution, times=None)[pitch_range, :time_steps_per_bar*4]
# #
# # # Create a pypianoroll Track object
# # track = Track(pianoroll=pianoroll, program=0, is_drum=False)
# #
# # # Create a pypianoroll Multitrack object
# # multitrack = Multitrack(tracks=[track], tempo=midi_data.estimate_tempo(), resolution=beat_resolution)
# #
# # print(multitrack)
#
# multitrack = pypianoroll.read("Take_Me.mid")
# # multitrack.trim(0, 12*multitrack.resolution)
# # multitrack.binarize()
# multitrack_ch = pypianoroll.read("1.3_basic_pitch.mid")
#
# print(multitrack)
# pypianoroll.write('test_Take_Me.mid', multitrack)

# import os
#
# midi_files = []
# for root, dirs, files in os.walk('C:/Users/13516/Downloads/archive'):
#     for file in files:
#         if file.endswith(".mid") or file.endswith(".midi"):
#             midi_files.append(os.path.join(root, file))
# print(len(midi_files))

import os
import glob
import shutil

midi_files = []
for root, dirs, files in os.walk('C:/Users/13516/Desktop/2023 Spring/ECE-GY 6953 Deep Learning/FinalProject/jazz_melody_generation/data/tt'):
    for file in files:
        if file.endswith(".mid") or file.endswith(".midi"):
            midi_files.append(os.path.join(root, file))

print(len(midi_files))
# destination_dir = "C:/Users/13516/Desktop/2023 Spring/ECE-GY 6953 Deep Learning/FinalProject/jazz_melody_generation/data/tt"
# if not os.path.exists(destination_dir):
#     os.makedirs(destination_dir)
#
# i = 0
# for file_path in midi_files:
#     try:
#
#         file_name = os.path.basename(file_path)
#         destination_path = os.path.join(destination_dir, f"tt_{i}.mid")
#         shutil.copyfile(file_path, destination_path)
#         i += 1
#     except:
#         print(file_path)
#         continue
