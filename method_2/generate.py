import torch
from model.vae import VAE_one_hot, VAE_attention
from configs import config_data, config_vae_one_hot
import numpy as np
from utils.pianoroll2midi import pianoroll2midi
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = VAE_one_hot(DATA_CONFIG=config_data.DATA_CONFIG, MODEL_CONFIG=config_vae_one_hot.MODEL_CONFIG, device=device)
model = model.float().to(device)
model_para = torch.load('paper_outputs_conditional_one_hot/bata_0.7_en_layer_2_ratio_1.0_05_16__22_52/presents/loss_min.pt')
model.load_state_dict(model_para)
model.eval()

gen_num = 600

# ch_data = np.load(config_data.DATA_CONFIG['data_path'] + config_data.DATA_CONFIG['ch_npy'])
# indices = torch.randperm(ch_data.shape[0])[:gen_num]
# select_data = ch_data[indices]
# select_data = torch.from_numpy(select_data).float().to(device)

sample_num = 2
y = np.zeros((sample_num, 2))
y[:, 1] = 1

for i in range(gen_num):
    # _,_,mem = model.encode(select_data)
    # random_index = torch.randint(0, 256, (1,)).to(device)
    # # Use torch.index_select() to sample one tensor
    # sampled_tensor = torch.index_select(mem, 0, random_index).to(device)
    # # Alternatively, use indexing with random indices
    # sampled_tensor = mem[random_index].to(device)
    # # Reshape the tensor to (1, 3200)
    # sampled_tensor = sampled_tensor.unsqueeze(0).to(device)

    gen_m1, gen_mr1 = model.generate(sample_num=sample_num, y=y)

    gen_path = 'C:/Users/13516/Desktop/2023 Spring/ECE-GY 6953 Deep Learning/DLproject/method_2/' \
               'paper_outputs_conditional_one_hot/bata_0.7_en_layer_2_ratio_1.0_05_16__22_52/gen8bar/'
    gen_file = 'gen' + time.strftime("_%m_%d__%H_%M_", time.localtime()) + str(i)
    pianoroll2midi(gen_m1, gen_mr1, gen_path, gen_file)

