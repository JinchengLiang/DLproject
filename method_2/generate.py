import os
import shutil

import torch
from model.vae import VAE_one_hot
from configs import config_data, config_vae_one_hot
import numpy as np
from utils.pianoroll2midi import pianoroll2midi
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = VAE_one_hot(DATA_CONFIG=config_data.DATA_CONFIG, MODEL_CONFIG=config_vae_one_hot.MODEL_CONFIG, device=device)
model = model.to(device)
model_para = torch.load('paper_outputs_conditional_one_hot/bata_0.7_en_layer_2_ratio_1.0_05_15__00_27/presents/loss_min.pt')
model.load_state_dict(model_para)

gen_num = 10
sample_num = 2
y = np.zeros((sample_num, 2))
y[:, 1] = 1

for i in range(gen_num):
    gen_m1, gen_mr1 = model.generate(sample_num=sample_num, y=y)

    gen_path = '../dataset/generation/'
    gen_file = 'gen' + time.strftime("_%m_%d__%H_%M_", time.localtime()) + str(i)
    if os.path.exists(gen_path) and i==0:
        shutil.rmtree(gen_path)
    os.makedirs(os.path.join(gen_path), exist_ok=True)
    pianoroll2midi(gen_m1, gen_mr1, gen_path, gen_file)

