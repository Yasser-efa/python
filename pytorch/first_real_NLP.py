import pandas as pd
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
print(word_to_idx['yo'])

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
    zeros_to_remove = len(sequence) - max_len
    sequence = sequence[:max_len]
  return sequence

print(pad_sequence([1, 2, 3], 6))        # Trop court → devrait donner [1, 2, 3, 0, 0, 0]
print(pad_sequence([1, 2, 3, 4, 5], 3))  # Trop long → devrait donner [1, 2, 3]
print(pad_sequence([1, 2, 3], 3))        # Pile la bonne taille → [1, 2, 3]