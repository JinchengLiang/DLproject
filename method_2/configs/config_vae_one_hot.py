
MAIN_CONFIG = {
    'model_module' : 'model.vae',
    'model' : 'VAE_one_hot',
    # 'pertrain_model' : '/nas2/annahung/project/anna_jam_v2/outputs/2019_06_04__06_31/presents/ep_99.pt',
    'trainer_module' : 'trainer.vae',
    # 'trainer' : 'VAETrainer',
    'trainer' : 'VAETrainer_no_pcd_one_hot',
    'classifier_module' : 'model.classifier',
    # 'classifier' : 'classifier_binary',
    'classifier' : 'classifier',
    'pretrain_model_c' :
        'C:/Users/13516/Desktop/2023 Spring/ECE-GY 6953 Deep Learning/FinalProject/jazz_melody_generation/method_2/classifier/2023_05_05__18_13/presents/loss_min.pt',

    'package_path' : '/nas2/annahung/project/anna_jam_v2/',

}


MODEL_CONFIG = {

'vae': {
    'encoder' : {
        'hidden_m': 256, 
        'direction' : True,
        'num_of_layer' : 2,
        'gru_dropout_en' : None
        },

    'decoder' : {
        'direction' : False,
        'num_of_layer' : 1,
        'gru_dropout_de' : None,
        'teacher_forcing_ratio' : 1.0

        }

},
'classifier': {
    'hidden_m': 256,
    'bidirectional' : 2,
    'num_layers_en' : 2
}
    
}


TRAIN_CONFIG = {
'batch_size' : 256, 
'epochs' : 5,
'vae' : {
    'lr_vae' : 0.001,
    'lr_step1':40,
    'lr_step2':60,
    'lr_gamma':1,
    'loss_beta' : 0.7,

}


}













