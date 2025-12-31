import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F

class EmotionNet(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv1 = nn.Conv2d(3, 32, 3)
    self.conv2 = nn.Conv2d(32, 64, 3)
    self.pool = nn.MaxPool2d(2, 2)
    self.lin1 = nn.Linear(64*22*22, 128)
    self.lin2 = nn.Linear(128, 7)

  def forward(self, x):
    x = self.pool(F.relu(self.conv1(x)))
    x = self.pool(F.relu(self.conv2(x)))
    x = torch.flatten(x, 1)
    x = F.relu(self.lin1(x))
    x = self.lin2(x)
    return x

# Charger le modèle
model = EmotionNet()
model.load_state_dict(torch.load('emotion_model.pth'))
model.eval()

# Liste des émotions (dans l'ordre du dataset)
emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

print("Modèle chargé !")