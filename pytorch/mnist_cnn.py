import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Télécharger MNIST
transform = transforms.ToTensor()
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
# DataLoader (batches)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

class MNISTNet(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
    self.pool = nn.MaxPool2d(2, 2)
    # Partie dense (MLP)
    # Après conv (28→26) et pool (26→13) : shape = (32, 13, 13)
    self.fc1 = nn.Linear(32*13*13, 128)
    self.fc2 = nn.Linear(128, 10)

  def forward(self, x):
    # Conv → ReLU → Pool
    x = self.pool(F.relu(self.conv1(x)))
    
    # Flatten
    x = x.view(x.size(0), -1)  # (batch, 32*13*13)
    
    # Couches denses
    x = F.relu(self.fc1(x))
    x = self.fc2(x)  # Pas de softmax (la loss le fait)
    
    return x
  
model = MNISTNet()
  
criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(model.parameters(), lr=0.001)
  
def train(model, train_loader, criterion, optimizer, epoch):
  model.train()  # Mode entraînement
  
  for batch_idx, (data, target) in enumerate(train_loader):
    # 1. Forward pass
    output = model(data)
    loss = criterion(output, target)
    
    # 2. Backward pass
    optimizer.zero_grad()  # Réinitialiser gradients
    loss.backward()        # Calculer gradients
    optimizer.step()       # Mettre à jour poids
    
    # Afficher progression toutes les 100 batches
    if batch_idx % 100 == 0:
      print(f'Epoch {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)}] Loss: {loss.item():.4f}')

# Lancer 1 epoch
# train(model, train_loader, criterion, optimizer, epoch=1)
def test(model, test_loader):
    model.eval()  # Mode évaluation
    correct = 0
    
    with torch.no_grad():  # Pas besoin de gradients pour tester
        for data, target in test_loader:
            output = model(data)
            pred = output.argmax(dim=1)  # Prédiction = classe avec score max
            correct += pred.eq(target).sum().item()
    
    accuracy = 100. * correct / len(test_loader.dataset)
    print(f'Précision: {correct}/{len(test_loader.dataset)} ({accuracy:.2f}%)')

# # Tester après 1 epoch
test(model, test_loader)
# Entraîner 3 epochs de plus
for epoch in range(2, 5):
    train(model, train_loader, criterion, optimizer, epoch)
    test(model, test_loader)

# Sauvegarder
torch.save(model.state_dict(), 'mnist_cnn.pth')
print("Modèle sauvegardé !")

# Pour le recharger plus tard :
# model = MNISTNet()
# model.load_state_dict(torch.load('mnist_cnn.pth'))