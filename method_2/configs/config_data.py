import os

DATA_CONFIG = {
    'bar': 4,
    'ts_per_bar': 16,
    'feature_size': 800,    # (freq_up-freq_low+2)*ts_per_bar+ts_per_bar
    'freq_up': 95,
    'freq_low': 48,
    'testset_ratio': 0.2,
    'data_tpb': 4,
    'data_path': os.path.join("..", "..", "dataset"),
    'ch_data_path': os.path.join("..", "..", "dataset", "ChMusicMIDI8bar"),
    'tt_data_path': os.path.join("..", "..", "dataset", "tt"),
    'debug_data_path': os.path.join("..", "..", "dataset", "debug"),
    'ch_npy': "ch_m_0508.npy",
    'tt_npy': "tt_m_0508.npy"
}
