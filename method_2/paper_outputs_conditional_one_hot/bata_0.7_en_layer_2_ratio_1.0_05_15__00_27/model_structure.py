VAE_one_hot (
  (BGRUm): GRU(800, 256, num_layers=2, batch_first=True, bidirectional=True)
  (BGRUm2): GRU(256, 256, batch_first=True)
  (hid2mean): Linear(in_features=2048, out_features=256, bias=True)
  (hid2var): Linear(in_features=2048, out_features=256, bias=True)
  (lat2hidm): Linear(in_features=258, out_features=256, bias=True)
  (outm): Linear(in_features=256, out_features=800, bias=True)
)classifier (
  (BGRUm): GRU(800, 256, num_layers=2, batch_first=True, bidirectional=True)
  (hid2label): Linear(in_features=2048, out_features=2, bias=True)
)