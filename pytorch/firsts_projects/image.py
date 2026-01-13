from collections import Counter
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import WeightedRandomSampler
from torch.utils.data import random_split

# PC fixe: C:\Users\PC\Desktop\numpy_debut-20251222T134512Z-3-001\numpy_debut\processed_data
# PC portable: C:\Users\yasse\OneDrive\Bureau\numpy_debut\pytorch\train_files\processed_data

pth = r"C:\Users\PC\Desktop\numpy_debut-20251222T134512Z-3-001\numpy_debut\processed_data"
dataset = ImageFolder(pth)
transform = transforms.ToTensor()
dataset = ImageFolder(pth, transform=transform)

image, label = dataset[25000]
# Après le split
train, test = random_split(dataset, [39823, 9956])

# Compter les labels du TRAIN set seulement
train_labels = [dataset[i][1] for i in train.indices]
class_counts = Counter(train_labels)
# print("Distribution train:", class_counts)

# Calculer les poids pour chaque échantillon du train set
weights = [1.0 / class_counts[label] for label in train_labels]

# Créer le sampler
sampler = WeightedRandomSampler(weights, num_samples=len(weights), replacement=True)

# DataLoader avec sampler (PAS de shuffle)
train_loader = DataLoader(train, batch_size=64, sampler=sampler)
test_loader = DataLoader(test, batch_size=64, shuffle=False)



class EmotionNet(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv1 = nn.Conv2d(3, 32, 3)
    self.conv2 = nn.Conv2d(32, 64, 3)
    self.pool = nn.MaxPool2d(2, 2)

    #   formule: taille_sortie = taille_entrée - kernel_size + 1
    #   Après conv1 : 96 → 94
    #   Après pool  : 94 → 47
    #   Après conv2 : 47 → 45
    #   Après pool  : 22 → 22
    self.lin1 = nn.Linear(64*22*22, 128)
    self.lin2 = nn.Linear(128, 7)

  def forward(self, x, verbose=False):
    if verbose:
      print("Avant:", x.shape)
    
    x = self.conv1(x)
    if verbose:
      print("Après conv 1:", x.shape)

    x = F.relu(x)
    if verbose:
      print("Après ReLU:", x.shape)

    x = self.pool(x)
    if verbose:
      print("Après pooling 1:", x.shape)

    x = self.conv2(x)
    if verbose:
      print("Après conv 2:", x.shape)

    x = F.relu(x)
    if verbose:
      print("Après ReLU:", x.shape)

    x = self.pool(x)
    if verbose:
      print("Après pooling 2:", x.shape)

    x = torch.flatten(x, 1)
    if verbose:
      print("Après flatten:", x.shape)
    
    x = self.lin1(x)
    if verbose:
      print("Après lin1:", x.shape)
    x = F.relu(x)
    if verbose:
      print("Après ReLU:", x.shape)

    x = self.lin2(x)
    if verbose:
      print("Après lin2:", x.shape)

    return x
  
  
model = EmotionNet()


image, label = train[0]
image = image.unsqueeze(0)  # Ajoute dimension batch : (3,96,96) → (1,3,96,96)
# output = model(image, verbose=True)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train(model, train_loader, criterion, optimizer, epochs):
  model.train()

  for batch_idx, (data, target) in enumerate(train_loader):
    output = model(data)
    loss = criterion(output, target)

    optimizer.zero_grad()  # Réinitialiser gradients
    loss.backward()        # Calculer gradients
    optimizer.step()       # Mettre à jour poids

    # Afficher progression toutes les 100 batches
    if batch_idx % 100 == 0:
      print(f"Epoch {epochs} [{batch_idx * len(data)}/{len(train_loader.dataset)}] Loss: {loss.item():.4f}")

def test(model, test_loader):
  model.eval()
  corr = 0

  with torch.no_grad():
    for batch_idx, (data, target) in enumerate(test_loader):
      output = model(data)
      pred = output.argmax(dim=1)
      corr += (pred == target).sum()
  print(f"Bonnes prédictions: {(corr / len(test_loader.dataset)):.1%} ({corr}/{len(test_loader.dataset)})")
# print(len(test_loader.dataset))
for epoch in range(1, 6): 
  train(model, train_loader, criterion, optimizer, epochs=epoch)
  test(model, test_loader)

torch.save(model.state_dict(), 'emotion_model_balanced.pth')
print("Modèle sauvegardé !")
# print(dataset.classes)