MAIN_CONFIG={'trainer_module': 'trainer.classifier', 'trainer': 'ClassifierTrainer', 'classifier_module': 'model.classifier', 'classifier': 'classifier'}
MODEL_CONFIG={'classifier': {'hidden_m': 256, 'bidirectional': 2, 'num_layers_en': 2}}
TRAIN_CONFIG={'batch_size': 256, 'epochs': 5, 'lr': 1e-05, 'lr_step1': 10, 'lr_step2': 30, 'lr_gamma': 0.1}