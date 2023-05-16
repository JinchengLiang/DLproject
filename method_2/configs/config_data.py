
DATA_CONFIG = {
    'bar': 8,
    'ts_per_bar': 16,
    'feature_size': 800,    # (freq_up-freq_low+2)*ts_per_bar+ts_per_bar
    'freq_up': 95,
    'freq_low': 48,
    'testset_ratio': 0.1,
    'data_tpb': 4,
    'tt_num': 3600,  # The tt samples num for training
    'data_path': "../data/",
    'ch_data_path':"../dataset/ChMusicMIDI8bar/",
    'tt_data_path':"../dataset/LakhMIDI/",
    'debug_data_path': "../dataset/debug/",
    'ch_npy': "ch_m.npy",
    'tt_npy': "tt_m.npy"
}
