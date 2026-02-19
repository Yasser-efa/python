import librosa
import numpy as np
import os
import torch

dataset = torch.utils.data.Dataset

CLASSES = ['go', 'no', 'stop', 'yes']
N_MELS = 64
SAMPLE_RATE = 16000

DICTIONNARY_LABEL = {
  'go': 0,
  'no': 1,
  'stop': 2,
  'yes': 3
}

class AudioDataset(dataset):
  def __init__(self):
    self.base = "reco_audio/training_dataset"
    self.fichiers = os.listdir(self.base)
    self.dic = {}

    # Créer un dictionnaire sous forme de {i: [fichier, label(go/stop/..)]}
    i = 0
    for f in self.fichiers:
      if os.path.isdir(f"{self.base}/{f}"):
        sousfichiers = os.listdir(f"{self.base}/{f}")
        for wav in sousfichiers:
          self.dic[i] = [f"{self.base}/{f}/{wav}", f]
          i+=1

  def __len__(self):
    return len(self.dic)

  def __getitem__(self, index):
    pth, label = self.dic[index]
    y, sr = librosa.load(pth, sr=16000)

    # Comme il y a des audio qui font + de 1 sec et - de 1 sec alors on va padder et truncer pour obtenir exactement 1 seconde et avoir à la fin une shape de [1, 64, 32]
    if len(y) < 16000:
      y = np.pad(y, (0, 16000 - len(y)), mode="constant", constant_values=0.0)
    elif len(y) > 16000:
      y = y[:16000]

    # Transformer le .wav en spectrogramme
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=64)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    # Transformer en tensor et ajouter une dimension pour le channel
    tensor = torch.tensor(mel_spec_db, dtype=torch.float32).unsqueeze(0)
    return tensor, DICTIONNARY_LABEL[label]
  
ds = AudioDataset()
spec, label = ds[0]