import glob
import os

import mido

# Set the number of bars per MIDI file
bars_per_file = 8

set = glob.glob(os.path.join('..', 'dataset', 'ChMusicMIDI', '*.mid'))
if not any(set):
  print("Error: sample set it empty")
  exit()

for j in range(len(set)):
    # Load the MIDI file
    midi_file = mido.MidiFile(set[j])

    # Calculate the total number of bars in the MIDI file
    total_bars = sum([msg.time for msg in midi_file if isinstance(msg, mido.MetaMessage) and msg.type == 'time_signature'])

    # Calculate the number of MIDI files needed
    num_files = total_bars // bars_per_file + int(total_bars % bars_per_file != 0)

    # Split the MIDI file into several files
    for i in range(num_files):
        # Create a new MIDI file
        new_file = mido.MidiFile(type=1)

        # Calculate the starting and ending ticks for the current file
        start_tick = i * bars_per_file * midi_file.ticks_per_beat * 4
        end_tick = min((i + 1) * bars_per_file * midi_file.ticks_per_beat * 4, midi_file.length)

        # Copy the MIDI messages from the original file to the new file
        for msg in midi_file:
            if msg.time > 0:
                # Update the time of the message based on the new file's starting tick
                msg.time = max(0, msg.time - start_tick)
            if msg.time == 0 and start_tick <= msg.time < end_tick:
                # Add the message to the new file if it falls within the current file's range
                new_file.tracks[msg.channel].append(msg)

        # Save the new MIDI file
        new_file.save(f'output/file_{j}_{i}.mid')
        #new_file.save(os.path.join('..', 'dataset', 'ChMusicMIDI8bar', f'file_{j}_{i}.mid'))
        print("done")
