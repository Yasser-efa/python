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

print(df['sequence'].apply(len).head(10))