import mido
import numpy as np
import torch
from torchvision.utils import save_image
# from utils.midi_io.src.core_midi import midi_parser
# from utils.write_midi import *
import glob
import ipdb
from utils.midi2pianoroll import get_notes, resolution_transfer, note2pianoroll, div_notes, div_notes_one_bar, check_quality, resolution_compress, get_pianoroll
from utils.pianoroll2midi import p2m_get_notes, save2midi, pianoroll2midi
from configs.config_data import DATA_CONFIG

# from midi_io.src.core_midi import midi_parser
from utils.write_midi import *

def shape_to_bar_sample(m,mr,ts_per_bar, freq_range, bar):
    #reshape to leadsheetVAE
    #each sample reshape to (4,800)  4 bar, each_beat=200 ticks, concat 4 beat

    # 800 = 49*16 + 16
    # cut the m and mr to 4 pieces, and concatenate m piece and corresponding mr piece to get a bar.
    #reshape to (1,64*freq_range)
    m1 = m.reshape((1,-1), order='C')
    #reshape to (1,64)
    mr1 = mr.reshape((1,-1), order='C')
    bar_sample = []
    for i in range(bar):
        st = freq_range*ts_per_bar*i
        ed = freq_range*ts_per_bar*(i+1)
        st_r = 1*ts_per_bar*i
        ed_r = 1*ts_per_bar*(i+1)
        one_bar = np.concatenate((m1[:,st:ed],mr1[:,st_r:ed_r]),axis=1)
        bar_sample.append(one_bar)
    bar_sample = np.asarray(bar_sample)
    bar_sample = bar_sample.reshape(bar_sample.shape[0],bar_sample.shape[2])
    return bar_sample

def shape_to_pianoroll(bar_sample, freq_range,ts_per_bar):
        # reshape back to pianoroll
        m = bar_sample[:,:freq_range*ts_per_bar]
        m1 = m.reshape((bar,ts_per_bar,freq_range),order='C')

        mr = bar_sample[:,freq_range*ts_per_bar:]
        mr1 = mr.reshape((bar,ts_per_bar,1),order='C')

        return m1, mr1

def check_data_quality(where_note_group, pitch_group, bar, ts_per_bar):
    # must have more than 2 pitchs, must not have a single constant pitch longer than 75%
    if len(pitch_group) < 3:
        return False

    real_pitch = []
    total_len = bar * ts_per_bar
    duration = 0
    for i in range(len(where_note_group)-1):
        dur = where_note_group[i+1]-where_note_group[i]
        duration += dur
        if dur > float(0.75 * total_len):
            for note_time in where_note_group[:i] + where_note_group[i+2:]:
                if where_note_group[i] < note_time < where_note_group[i+1]:
                    return True
            return False
        if dur > 0 and pitch_group[i] not in real_pitch:
            real_pitch.append(pitch_group[i])
    if duration < float(0.5 * total_len) or len(real_pitch) < 3:
        return False
    else:
        return True


def get_data(bar,
            pieces_file_path,
            save_path,
            save_filename,
            ts_per_bar,
            rest_dim,
            freq_up,
            freq_low, 
            freq_range,
            data_tpb,
            data_style):
    data_x = []


    for filename in pieces_file_path:
        song_name = filename.split('/')[-1].split('\\')[-1].split('.mid')[0]

        try:
            midi = midi_parser.MidiFile(filename)
            # original_tpb = midi.ticks_per_beat

            note_group = get_notes(midi)    # note_group [start, length, pitch, velocity]
            if note_group is False:
                continue
            # divide the notes by certain bars.
            notes_bars = div_notes(note_group, midi.ticks_per_beat, bar)
            # notes_one_bar = div_notes_one_bar(note_group, midi.ticks_per_beat)
            note_starts = resolution_compress(notes_bars, midi.ticks_per_beat, data_tpb)
            check_quality(notes_bars, note_starts, bar, freq_up, freq_low, ts_per_bar, data_style)
            for k in note_starts.keys():
                m, mr = get_pianoroll(notes_bars[k], note_starts[k], ts_per_bar, bar, freq_range, freq_low, rest_dim)
                bar_sample = shape_to_bar_sample(m, mr, ts_per_bar, freq_range, bar)
                save_image(torch.from_numpy(m).type(torch.FloatTensor),
                           DATA_CONFIG['data_path'] + data_style + '/output/' + song_name + '_' + str(k) + '_m.png')

                data_x.append(bar_sample)
            # where_note_group, dur_group, pitch_group = resolution_transfer(note_group, original_tpb, data_tpb, bar, ts_per_bar)
            '''
            if not check_data_quality(where_note_group, pitch_group, bar, ts_per_bar):
                continue
            m, mr = note2pianoroll(note_group,where_note_group,pitch_group,freq_range, freq_low, freq_up, rest_dim, bar, ts_per_bar)
            # m 64 length * 49 pitch , mr 64 the start of node
            bar_sample = shape_to_bar_sample(m, mr, ts_per_bar, freq_range, bar)
            m1, mr1 = shape_to_pianoroll(bar_sample, freq_range,ts_per_bar)
            # m1 4bar*16*49, mr1 4bar*16
            mr1 = mr1.reshape(-1,1)
            m1 = m1.reshape(-1,49)
            # finally m1==m, mr1==mr, seems just check code
            assert m1.all() == m.all()
            assert mr1.all() == mr.all()

            save_image(torch.from_numpy(m).type(torch.FloatTensor),
                       DATA_CONFIG['data_path'] + data_style + '/output/' + song_name + '_m.png')

            # save_image(torch.from_numpy(m1).type(torch.FloatTensor),DATA_CONFIG['data_path'] + 'tt/output/tt_m1_'+ song_name +'.png')
            # pianoroll2midi(m,mr,'./output/TT_m_', song_name +'.mid')
            # pianoroll2midi(m1,mr1,'./output/TT_m1_', song_name +'.mid')
            data_x.append(bar_sample)
            '''
        except Exception as e:
            print(f"{song_name}: {e}")
            continue

    data_x = np.asarray(data_x)
    print(data_x.shape, ' saved.')
    np.save(save_path + save_filename, data_x)


def get_data_CNN(bar,
            pieces_file_path,
            save_path,
            save_filename,
            ts_per_bar,
            rest_dim,
            freq_up,
            freq_low, 
            freq_range,
            data_tpb):
    data_x = []
    for filename in pieces_file_path:
        song_name = filename.split('.')[0].split('/')[5:]
        seperator = '_'
        song_name = seperator.join(song_name)
        try:
            midi = midi_parser.MidiFile(filename)
            original_tpb = midi.ticks_per_beat

            note_group = get_notes(midi)
            where_note_group, dur_group, pitch_group = resolution_transfer(note_group, original_tpb, data_tpb, bar, ts_per_bar)
            m, mr = note2pianoroll(note_group,where_note_group,pitch_group,freq_range, freq_low, freq_up, rest_dim, bar, ts_per_bar)
            m1, mr1 = shape_to_pianoroll(bar_sample, freq_range,ts_per_bar)
            mr1 = mr1.reshape(-1,1)
            m1 = m1.reshape(-1,49)
            # save_image(torch.from_numpy(m1).type(torch.FloatTensor),'./output/TT_m1_'+ song_name +'.png')
            # pianoroll2midi(m,mr,'./output/TT_m_', song_name +'.mid')
            # pianoroll2midi(m1,mr1,'./output/TT_m1_', song_name +'.mid')
            save_image(torch.from_numpy(m1).type(torch.FloatTensor), DATA_CONFIG['data_path'] + 'ChMusic/output/TT_m1_' + song_name + '.png')
            pianoroll2midi(m, mr, DATA_CONFIG['data_path'] + 'ChMusic/output/TT_m_', song_name + '.mid')
            pianoroll2midi(m1, mr1, DATA_CONFIG['data_path'] + 'ChMusic/output/TT_m1_', song_name + '.mid')
            data_x.append(m1)
        except:
            continue
    data_x = np.asarray(data_x)
    print(data_x.shape, ' saved.')
    np.save(save_path + save_filename, data_x)


if __name__ == '__main__':

    # choose ch data or tt data or debug data
    data_style = 'ch'
    if data_style == 'ch':
        pieces_file_path = glob.glob(DATA_CONFIG['ch_data_path'] + '*.mid')
        save_filename = DATA_CONFIG['ch_npy']
    elif data_style == 'tt':
        pieces_file_path = glob.glob(DATA_CONFIG['tt_data_path'] + '*.mid')
        save_filename = DATA_CONFIG['tt_npy']
    elif data_style == 'debug':
        pieces_file_path = glob.glob(DATA_CONFIG['debug_data_path'] + '*.mid')
        save_filename = 'debug_m.npy'

    bar = DATA_CONFIG['bar']
    ts_per_bar = DATA_CONFIG['ts_per_bar']
    freq_up = DATA_CONFIG['freq_up']
    freq_low = DATA_CONFIG['freq_low']
    data_tpb = DATA_CONFIG['data_tpb']
    save_path = DATA_CONFIG['data_path']    # where the .npy save
    freq_range = freq_up - freq_low + 2
    rest_dim = 48   # the pitch number when pitch == 0 (tick 0 ~ the first tick in note). the last index in pianoroll

    get_data(bar=bar,
             pieces_file_path=pieces_file_path,
             save_path=save_path,
             save_filename=save_filename,
             ts_per_bar=ts_per_bar,
             rest_dim=rest_dim,
             freq_up=freq_up,
             freq_low=freq_low,
             freq_range=freq_range,
             data_tpb=data_tpb,
             data_style=data_style)
