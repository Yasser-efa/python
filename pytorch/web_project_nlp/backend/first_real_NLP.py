from torchviz import make_dot
import json
import argparse
import os
import pandas as pd
import torch
import torch.nn as nn 
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# ============================================================================
# CONSTANTES
# ============================================================================

MODEL_PATH = "training_data/firstnlp.pth"
MODEL_PATH_LSTM = "training_data/firstnlp_lstm.pth"
VOCAB_PATH = "training_data/word_to_idx.json"

# ============================================================================
# FONCTIONS DE PREPROCESSING (importables)
# ============================================================================

def text_to_sequence(text, word_to_idx):
    words = str(text).lower().split()
    return [word_to_idx.get(word, 0) for word in words]

def pad_sequence(sequence, max_len):
    if len(sequence) < max_len:
        sequence.extend([0] * (max_len - len(sequence)))
    elif len(sequence) > max_len:
        sequence = sequence[:max_len]
    return sequence

# ============================================================================
# MODÈLES (importables)
# ============================================================================

class FirstNLP(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size + 1, 128)
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


class FirstNLP_LSTM(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size + 1, 128)
        self.lstm = nn.LSTM(128, 128, batch_first=True)
        self.hid1 = nn.Linear(128, 64)
        self.hid2 = nn.Linear(64, 32)
        self.hid3 = nn.Linear(32, 3)

    def forward(self, x):
        x = self.embedding(x)
        _, (h_n, _) = self.lstm(x)
        h_n = h_n.squeeze(0)
        x = self.hid1(h_n)
        x = F.relu(x)
        x = self.hid2(x)
        x = F.relu(x)
        x = self.hid3(x)
        return x

# ============================================================================
# FONCTIONS TRAIN / TEST (importables)
# ============================================================================

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


def test_self(model, sentence, word_to_idx):
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


# ============================================================================
# EXÉCUTION (seulement si lancé directement)
# ============================================================================

if __name__ == "__main__":
    
    # === PARSER ===
    parser = argparse.ArgumentParser(description="First NLP Trainer / Tester")
    parser.add_argument("--train", action="store_true", help="Entraîner le modèle")
    parser.add_argument("--test", action="store_true", help="Tester le modèle")
    parser.add_argument("--test_self", action="store_true", help="Tester le modèle avec tes propres phrases")
    parser.add_argument("--train_lstm", action="store_true", help="Entraîner le modèle LSTM")
    parser.add_argument("--test_lstm", action="store_true", help="Tester le modèle LSTM")
    parser.add_argument("--test_self_lstm", action="store_true", help="Tester le modèle LSTM avec tes propres phrases")
    args = parser.parse_args()

    # === CHARGEMENT DES DONNÉES ===
    df = pd.read_csv('training_data/twitter_training.csv', header=None)
    df.columns = ['id', 'entity', 'sentiment', 'text']
    df = df[df['sentiment'] != 'Irrelevant']

    tv = pd.read_csv('training_data/twitter_validation.csv', header=None)
    tv.columns = ['id', 'entity', 'sentiment', 'text']
    tv = tv[tv['sentiment'] != 'Irrelevant']

    # === VOCABULAIRE : CRÉER OU CHARGER ===
    if args.train or args.train_lstm:
        all_words = []
        for txt in df['text']:
            words = str(txt).lower().split()
            all_words.extend(words)
        unique_words = list(set(all_words))
        word_to_idx = {word: idx + 1 for idx, word in enumerate(unique_words)}
        
        with open(VOCAB_PATH, 'w') as f:
            json.dump(word_to_idx, f)
        print("Vocabulaire créé et sauvegardé")

    elif args.test or args.test_self or args.test_lstm or args.test_self_lstm:
        with open(VOCAB_PATH, 'r') as f:
            word_to_idx = json.load(f)
        print("Vocabulaire chargé")

    else:
        print(" --train / --test / --test_self \n or \n --train_lstm / --test_lstm / --test_self_lstm")
        exit()

    # === PREPROCESSING ===
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

    # === CRÉATION DES MODÈLES ===
    vocab_size = len(word_to_idx)
    
    model = FirstNLP(vocab_size)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model_lstm = FirstNLP_LSTM(vocab_size)
    optimizer_lstm = optim.Adam(model_lstm.parameters(), lr=0.001)

    criterion = nn.CrossEntropyLoss()

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
            test_self(model, sentence, word_to_idx)

    if args.train_lstm:
        print("Entraînement du modèle LSTM")
        train(model_lstm, dataloader_df, criterion, optimizer_lstm, epochs=52)
        torch.save(model_lstm.state_dict(), MODEL_PATH_LSTM)
        print("Modèle LSTM sauvegardé")

    if args.test_lstm:
        if not os.path.exists(MODEL_PATH_LSTM):
            print("Aucun modèle LSTM sauvegardé trouvé")
        else:
            print("Chargement du modèle LSTM")
            model_lstm.load_state_dict(torch.load(MODEL_PATH_LSTM))
            test(model_lstm, dataloader_tv)

    if args.test_self_lstm:
        if not os.path.exists(MODEL_PATH_LSTM):
            print("Aucun modèle LSTM sauvegardé trouvé")
        else:
            print("Chargement du modèle LSTM")
            model_lstm.load_state_dict(torch.load(MODEL_PATH_LSTM))
            sentence = input("Veuillez entrer une phrase svp: ")
            test_self(model_lstm, sentence, word_to_idx)