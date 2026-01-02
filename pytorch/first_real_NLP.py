import json
import argparse
import os
import pandas as pd
import torch
import torch.nn as nn 
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

MODEL_PATH = "pytorch/training_data/firstnlp.pth"
VOCAB_PATH = "pytorch/emotionNLP_data/word_to_idx.json"

# === PARSER EN PREMIER ===
parser = argparse.ArgumentParser(description="First NLP Trainer / Tester")
parser.add_argument("--train", action="store_true", help="Entraîner le modèle")
parser.add_argument("--test", action="store_true", help="Tester le modèle")
parser.add_argument("--test_self", action="store_true", help="Tester le modèle avec tes propres phrases")
args = parser.parse_args()

# === CHARGEMENT DES DONNÉES ===
df = pd.read_csv('pytorch/emotionNLP_data/twitter_training.csv', header=None)
df.columns = ['id', 'entity', 'sentiment', 'text']
df = df[df['sentiment'] != 'Irrelevant']

tv = pd.read_csv('pytorch/emotionNLP_data/twitter_validation.csv')
tv.columns = ['id', 'entity', 'sentiment', 'text']
tv = tv[tv['sentiment'] != 'Irrelevant']

# === VOCABULAIRE : CRÉER OU CHARGER ===
if args.train:
    all_words = []
    for txt in df['text']:
        words = str(txt).lower().split()
        all_words.extend(words)
    unique_words = list(set(all_words))
    word_to_idx = {word: idx+1 for idx, word in enumerate(unique_words)}
    
    with open(VOCAB_PATH, 'w') as f:
        json.dump(word_to_idx, f)
    print("Vocabulaire créé et sauvegardé")

elif args.test:
    with open(VOCAB_PATH, 'r') as f:
        word_to_idx = json.load(f)
    print("Vocabulaire chargé")

elif args.test_self:
  with open(VOCAB_PATH, 'r') as f:
    word_to_idx = json.load(f)
  print("Vocabulaire chargé")

else:
    print("--train / --test / --test_self")
    exit()

# === PREPROCESSING (avec le bon word_to_idx) ===
def text_to_sequence(text, word_to_idx):
    words = str(text).lower().split()
    return [word_to_idx.get(word, 0) for word in words]

def pad_sequence(sequence, max_len):
    if len(sequence) < max_len:
        sequence.extend([0] * (max_len - len(sequence)))
    elif len(sequence) > max_len:
        sequence = sequence[:max_len]
    return sequence

df['sequence'] = df['text'].apply(lambda x: text_to_sequence(x, word_to_idx))
df['sequence'] = df['sequence'].apply(lambda x: pad_sequence(x, 50))
df['sentiment'] = df['sentiment'].map({'Positive': 0, 'Negative': 1, 'Neutral': 2})

tv['sequence'] = tv['text'].apply(lambda x: text_to_sequence(x, word_to_idx))
tv['sequence'] = tv['sequence'].apply(lambda x: pad_sequence(x, 50))
tv['sentiment'] = tv['sentiment'].map({'Positive': 0, 'Negative': 1, 'Neutral': 2})

# === TENSORS ET DATALOADERS ===
sequences_tensor_df = torch.tensor(df['sequence'].tolist())
sentiments_tensor_df = torch.tensor(df['sentiment'].tolist())
sequences_tensor_tv = torch.tensor(tv['sequence'].tolist())
sentiments_tensor_tv = torch.tensor(tv['sentiment'].tolist())

dataloader_df = DataLoader(TensorDataset(sequences_tensor_df, sentiments_tensor_df), batch_size=32, shuffle=True)
dataloader_tv = DataLoader(TensorDataset(sequences_tensor_tv, sentiments_tensor_tv), batch_size=32, shuffle=True)

# === MODÈLE ===
class FirstNLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(len(word_to_idx)+1, 128)
        self.hid1 = nn.Linear(128, 64)
        self.hid2 = nn.Linear(64, 32)
        self.hid3 = nn.Linear(32, 3)

    def forward(self, x):
        x = self.embedding(x)
        x = torch.mean(x, dim=1)
        x = self.hid1(x)
        x = F.relu(x)
        x = self.hid2(x)
        x = F.relu(x)
        x = self.hid3(x)
        return x

model = FirstNLP()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# === FONCTIONS TRAIN/TEST ===
def train(model, dataloader, criterion, optimizer, epochs):
    model.train()
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(dataloader):
            output = model(data)
            loss = criterion(output, target)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch_idx % 100 == 0:
                print(f'Epoch {epoch} [{batch_idx * len(data)}/{len(dataloader.dataset)}] Loss: {loss.item():.4f}')

def test(model, dataloader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for data, target in dataloader:
            output = model(data)
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()
    accuracy = 100. * correct / len(dataloader.dataset)
    print(f'Précision: {correct}/{len(dataloader.dataset)} ({accuracy:.2f}%)')

# === FONCTION TEST SUR MES PHRASES ===
def test_self(model, sentence):
  model.eval()
  sentence = text_to_sequence(sentence, word_to_idx)
  sentence = pad_sequence(sentence, 50)
  sentence = torch.tensor(sentence).unsqueeze(0)
  with torch.no_grad():
    output = model(sentence)   
    pred = output.argmax(dim=1)
  if pred == 0:
    pred = "Positive"
  elif pred == 1:
    pred = "Negative"
  else:
    pred = "Neutral"
  print(f"Prédiction de l'ia: {pred}")


# === EXÉCUTION ===
if args.train:
    print("Entraînement du modèle")
    train(model, dataloader_df, criterion, optimizer, epochs=50)
    torch.save(model.state_dict(), MODEL_PATH)
    print("Modèle sauvegardé")

if args.test:
  if not os.path.exists(MODEL_PATH):
    print("Aucun modèle sauvegardé trouvé")
  else:
    print("Chargement du modèle")
    model.load_state_dict(torch.load(MODEL_PATH))
    test(model, dataloader_tv)

if args.test_self:
  if not os.path.exists(MODEL_PATH):
    print("Aucun modèle sauvegardé trouvé")
  else:
    print("Chargement du modèle")
    model.load_state_dict(torch.load(MODEL_PATH))
    sentence = input("Veuillez entrer une phrase svp: ")
    test_self(model, sentence)
