import pandas as pd
import torch
import torch.nn as nn 
from torchvision import datasets, transforms
from torch.utils.data import TensorDataset, DataLoader

# df -> DataFrame
df = pd.read_csv('pytorch/emotionNLP_data/twitter_training.csv', header=None)
df.columns = ['id', 'entity', 'sentiment', 'text']
df = df[df['sentiment'] != 'Irrelevant']

text = df['text'].iloc[0]
all_words = []
for text in df['text']:
    words = str(text).lower().split()
    all_words.extend(words)

unique_words = list(set(all_words))
word_to_idx = {word: idx+1 for idx, word in enumerate(unique_words)}

def text_to_sequence(text, word_to_idx):
  sequence = []
  words = str(text).lower().split()
  for word in words:
    sequence.append(word_to_idx.get(word, 0))
  return sequence

df['sequence'] = df['text'].apply(lambda x: text_to_sequence(x, word_to_idx=word_to_idx))


longueur = df['sequence'].apply(len)


def pad_sequence(sequence, max_len):
  if len(sequence) < max_len:
    remaining_0 = max_len - len(sequence)
    sequence.extend([0]*remaining_0)
  elif len(sequence) > max_len:
    sequence = sequence[:max_len]
  return sequence


df['sequence'] = df['sequence'].apply(lambda x: pad_sequence(x, 50))
df['sentiment'] = df['sentiment'].map({'Positive': 0, 'Negative': 1, 'Neutral': 2})

sequences = df['sequence'].tolist()
sequences_tensor = torch.tensor(sequences)

sentiments = df['sentiment'].tolist()
sentiments_tensor = torch.tensor(sentiments)

dataset = TensorDataset(sequences_tensor, sentiments_tensor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)