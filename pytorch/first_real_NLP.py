import pandas as pd
import torch
import torch.nn as nn 
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import TensorDataset, DataLoader

# df -> DataFrame
df = pd.read_csv('pytorch/emotionNLP_data/twitter_training.csv', header=None)
df.columns = ['id', 'entity', 'sentiment', 'text']
df = df[df['sentiment'] != 'Irrelevant']

# ajout de twitter_validaiton.csv (tv)
tv = pd.read_csv('pytorch/emotionNLP_data/twitter_validation.csv')
tv.columns = ['id', 'entity', 'sentiment', 'text']
tv = tv[tv['sentiment'] != 'Irrelevant']

all_words = []
def prepare_text(text, all_words):
  for txt in text:
    words = str(txt).lower().split()
    all_words.extend(words)
  return all_words
unique_words = list(set(prepare_text(df['text'], all_words)))

word_to_idx = {word: idx+1 for idx, word in enumerate(unique_words)}

def text_to_sequence(text, word_to_idx):
  sequence = []
  words = str(text).lower().split()
  for word in words:
    sequence.append(word_to_idx.get(word, 0))
  return sequence

df['sequence'] = df['text'].apply(lambda x: text_to_sequence(x, word_to_idx=word_to_idx))
tv['sequence'] = tv['text'].apply(lambda x: text_to_sequence(x, word_to_idx=word_to_idx))


# longueur = df['sequence'].apply(len)


def pad_sequence(sequence, max_len):
  if len(sequence) < max_len:
    remaining_0 = max_len - len(sequence)
    sequence.extend([0]*remaining_0)
  elif len(sequence) > max_len:
    sequence = sequence[:max_len]
  return sequence


df['sequence'] = df['sequence'].apply(lambda x: pad_sequence(x, 50))
df['sentiment'] = df['sentiment'].map({'Positive': 0, 'Negative': 1, 'Neutral': 2})

tv['sequence'] = tv['sequence'].apply(lambda x: pad_sequence(x, 50))
tv['sentiment'] = tv['sentiment'].map({'Positive': 0, 'Negative': 1, 'Neutral': 2})


sequences_df = df['sequence'].tolist()
sequences_tensor_df = torch.tensor(sequences_df)

sentiments_df = df['sentiment'].tolist()
sentiments_tensor_df = torch.tensor(sentiments_df)

sequences_tv = tv['sequence'].tolist()
sequences_tensor_tv = torch.tensor(sequences_tv)

sentiments_tv = tv['sentiment'].tolist()
sentiments_tensor_tv = torch.tensor(sentiments_tv)

dataset_df = TensorDataset(sequences_tensor_df, sentiments_tensor_df)
dataloader_df = DataLoader(dataset_df, batch_size=32, shuffle=True)

dataset_tv = TensorDataset(sequences_tensor_tv, sentiments_tensor_tv)
dataloader_tv = DataLoader(dataset_tv, batch_size=32, shuffle=True)

class FirstNLP(nn.Module):
  def __init__(self):
    super().__init__()
    self.embedding = nn.Embedding(len(word_to_idx), 128)
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
