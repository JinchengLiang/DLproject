import mido
import numpy as np
from utils.midi_io.src.core_midi import midi_parser
from utils.write_midi import *
import ipdb


def get_main_instrument(instruments):
    main_instrument = -1
    if len(instruments) == 1:
        main_instrument = 0
    else:
        for i in range(len(instruments)):
            if instruments[i].name == "Vocal" or instruments[i].name == "vocal":
                main_instrument = i
                break
    return main_instrument


def get_notes(midi, freq_up, freq_low):
    '''
    midi.max_tick represents the length.
    instruments.notes (start, end, pitch, velocity)
    '''
    note_groups = []
    # main_instrument = get_main_instrument(midi.instruments)
    # if main_instrument == -1:
    #     return -1

    # sort the instruments notes by pitch numbers and note length, then select the best one based on their average rank
    pitch_num = []
    note_len = []
    for i in range(len(midi.instruments)):
        tmp_note_group = []
        notes = midi.instruments[i].notes
        crop_left = notes[round(len(notes)/2)].start  # crop the blank at the beginning, the beginning often no reference value
        sum_len = 0
        pitch_record = []
        for note in notes[round(len(notes)/2):]:
            if freq_low <= note.pitch <= freq_up:
                sum_len += (note.end - note.start)
                if note.pitch not in pitch_record:
                    pitch_record.append(note.pitch)
                tmp_note_group.append([note.start - crop_left, note.end - note.start, note.pitch, note.velocity])

        note_groups.append(tmp_note_group)
        pitch_num.append((i, len(pitch_record)))
        note_len.append((i, sum_len))
    pitch_num.sort(key=lambda x: x[1], reverse=True)
    note_len.sort(key=lambda x: x[1], reverse=True)
    aver_rank = []
    for i in range(len(pitch_num)):
        in_index = pitch_num[i][0]
        note_rank = [v for v, _ in note_len].index(in_index)
        av_rank = float((2*(i+1) + (note_rank+1)) / 2)
        aver_rank.append((in_index, av_rank))
    aver_rank.sort(key=lambda x: x[1])
    for ins, _ in aver_rank:
        if not midi.instruments[ins].is_drum:
            return note_groups[ins]




def resolution_transfer(note_group, original_tpb, data_tpb, bar, ts_per_bar):
    transfer_ratio = round(original_tpb/data_tpb)   # origin_tick_per_beat/data_tick_per_beat compressed ratio

    a_note = note_group[0]
    note_on = a_note[0]
    dur = a_note[1]
    pitch = a_note[2]
    where_note = round(note_on/transfer_ratio)
    duration = round(dur/transfer_ratio)

    where_note_group = []
    dur_group = []
    pitch_group = []
    for i in range(len(note_group)):
        a_note = note_group[i]
        note_on = a_note[0]
        dur = a_note[1]
        pitch = a_note[2]
        where_note = round(note_on/transfer_ratio)
        duration = round(dur/transfer_ratio)
        # compress the original data to bar*ts_per_bar ticks. ts_per_bar=ticks_per_bar.
        if where_note >= (bar*ts_per_bar-1):
            break
        else:
            where_note_group.append(where_note)
            dur_group.append(duration)
            pitch_group.append(pitch)

    return where_note_group, dur_group, pitch_group




def note2pianoroll(note_group,where_note_group,pitch_group,
                   freq_range, freq_low, freq_up, rest_dim, bar, ts_per_bar):

    if where_note_group[0] != 0:
        where_note_group = [0] + where_note_group   #一開始補上休止符
        pitch_group      = [0] + pitch_group

    mr = np.zeros((ts_per_bar*bar,1))
    for i in range(len(where_note_group)):
        mr[where_note_group[i]] = 1


    m  = np.zeros((ts_per_bar*bar,freq_range))
    for i in range(len(pitch_group)):
        st = where_note_group[i]
        if i == (len(pitch_group)-1):
            ed = ts_per_bar*bar
        else:
            ed = where_note_group[i+1]
        pitch = pitch_group[i]
        if pitch == 0:
            m[st:ed, rest_dim] = 1
        elif freq_low <= pitch <= freq_up:
    #         print(pitch,pitch-freq_low)
            m[st:ed, pitch-freq_low] = 1
        else:
            continue

    return m, mr

def midi2pianoroll(filename):
    midi = midi_parser.MidiFile(filename)
    original_tpb = midi.ticks_per_beat
    bar = 4
    ts_per_bar = 16
    rest_dim = 48
    freq_up = 95
    freq_low = 48   #48 ~ 95
    freq_range = freq_up - freq_low + 2
    data_tpb = 4
    note_group = get_notes(midi)
    where_note_group, dur_group, pitch_group = resolution_transfer(note_group, original_tpb, data_tpb, bar, ts_per_bar)
    m, mr = note2pianoroll(note_group,where_note_group,pitch_group,freq_range, freq_low, freq_up, rest_dim, bar, ts_per_bar)
    return m,mr


if __name__ == '__main__':
    #get midi notes
    filename =  '/nas2/ai_music_database/jazz_freejammaster/split/AI_Jazz_freejammaster_01_split_0.mid'
    m,mr = midi2pianoroll(filename)

    for i in range(49): 
        if sum(m[:,i]) > 0 : 
            print('pitch: ',i, 'sum: ',sum(m[:,i]) )  


    ipdb.set_trace()




