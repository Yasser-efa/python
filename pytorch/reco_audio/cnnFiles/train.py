import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from dataset import AudioDataset
from torch.utils.data import random_split, DataLoader

if __name__ == "__main__":
  ds = AudioDataset()
  train_dataset, test_dataset = random_split(ds, [7604,1900])

  train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
  test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

class AudioCNN(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv2d0 = nn.Conv2d(1, 128, kernel_size=3)
    self.conv2d1 = nn.Conv2d(128, 64, kernel_size=3)
    self.conv2d2 = nn.Conv2d(64, 32, kernel_size=3)

    self.maxPool = nn.MaxPool2d(2, 2)
    self.lin0 = nn.Linear(384, 128)
    self.lin1 = nn.Linear(128, 32)
    self.output = nn.Linear(32, 4)

  def forward(self, x):
    # Conv2d → ReLU → MaxPool2d
    x = self.maxPool(F.relu(self.conv2d0(x)))
    x = self.maxPool(F.relu(self.conv2d1(x)))
    x = self.maxPool(F.relu(self.conv2d2(x)))

    # Flatten
    x = x.view(x.size(0), -1)

    # Linear → Relu → Linear → Relu → Output (4 classes (yes/no/stop/go))
    x = self.lin0(x)
    x = F.relu(x)
    x = self.lin1(x)
    x = F.relu(x)
    x = self.output(x)

    return x
  

if __name__ == "__main__":
  model = AudioCNN()
  if os.path.exists("reco_audio/cnnFiles/model_data/audio_model.pth"):
    model.load_state_dict(torch.load("reco_audio/cnnFiles/model_data/audio_model.pth"))
    
  criterion = nn.CrossEntropyLoss()

  optimizer = optim.Adam(model.parameters(), lr=0.001)

def train(model, epochs, optimizer, criterion):
  model.train()
  for epoch in range(epochs):
    for batch_x, batch_y in train_loader:
      # Forward pass
      optimizer.zero_grad()
      output = model(batch_x)
      loss = criterion(output, batch_y)

      # Backward pass
      loss.backward()
      optimizer.step()
    print(f"Epoch: {epoch}\nLoss: {loss.item():.4f}")
      

def test(model, test_loader):
  model.eval()
  correct = 0
  with torch.no_grad():
    for batch_x, batch_y in test_loader:
      output = model(batch_x)
      pred = output.argmax(dim=1)
      correct += pred.eq(batch_y).sum().item()
      
  precision = 100. * correct / len(test_loader.dataset)
  print(f"Précision de {precision:.2f}% ({correct}/{len(test_loader.dataset)})")

if __name__ == "__main__":
  train(model, 23, optimizer, criterion)
  torch.save(model.state_dict(), "reco_audio/cnnFiles/model_data/audio_model.pth")

  test(model, test_loader)
