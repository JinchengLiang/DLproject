from midiutil import MIDIFile
import glob
from copy import deepcopy
from method_2.utils.midi_io.src.core_midi import midi_parser

mid_set = glob.glob('C:/Users/13516/Desktop/2023 Spring/ECE-GY 6953 Deep Learning/DLproject/data/ch/Musics/*.mid')

num_bar = 8

for mid_file in mid_set:
    file_name = mid_file.split('/')[-1].split('\\')[-1].split('.mid')[0]
    mid = midi_parser.MidiFile(mid_file)
    notes = mid.instruments[0].notes
    ticks_num_bar = mid.ticks_per_beat * 4 * num_bar
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

        new_midi = MIDIFile(1, deinterleave=False, ticks_per_quarternote=mid.ticks_per_beat, eventtime_is_ticks=True)  # One track, defaults to format 1 (tempo track
        # automatically created)
        new_midi.addTempo(track, 0, tempo)
        new_midi.addTimeSignature(track=0, time=0, numerator=4, denominator=4, clocks_per_tick=mid.ticks_per_beat)
        pre_start = -1
        for note in note_list:
            if note.start > pre_start:
                new_midi.addNote(track, channel, note.pitch, note.start, note.end-note.start, note.velocity)
                pre_start = note.start

        try:
            with open(f"C:/Users/13516/Desktop/2023 Spring/ECE-GY 6953 Deep Learning/DLproject/data/ch/div_bar/"
                      f"{file_name}_{bar}.mid", "wb") as output_file:
                new_midi.writeFile(output_file)
        except Exception as e:
            print(f"{file_name}_{bar}.mid failed")
            print(e)

    # print("debug")


