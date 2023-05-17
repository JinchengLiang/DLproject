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
model_path = 'paper_outputs_conditional_one_hot/bata_0.7_en_layer_2_ratio_1.0/'
model_para = torch.load(model_path + 'presents/loss_min.pt')
model.load_state_dict(model_para)

gen_num = 10
sample_num = 2
y = np.zeros((sample_num, 2))
y[:, 1] = 1

timestamp = time.strftime("_%m_%d__%H_%M_", time.localtime())
gen_path ='../dataset/generation/'
'''if os.path.exists(gen_path):
    # Folder exists, so delete it and its contents
    shutil.rmtree(gen_path)
    print(f"The folder '{gen_path}' has been deleted.")
else:
    print(f"The folder '{gen_path}' does not exist.")'''
os.makedirs(gen_path, exist_ok=True)
print(f"The folder '{gen_path}' was created.")

for i in range(gen_num):
    gen_m1, gen_mr1 = model.generate(sample_num=sample_num, y=y)

    gen_file = 'gen' + timestamp + str(i)
    pianoroll2midi(gen_m1, gen_mr1, gen_path, gen_file)

