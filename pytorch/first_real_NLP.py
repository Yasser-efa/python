import pandas as pd

df = pd.read_csv('emotionNLP/twitter_training.csv', header=None)
df.columns = ['id', 'entity', 'sentiment', 'text']
df = df[df['sentiment'] != 'Irrelevant']

text = df['text'].iloc[0]
all_words = []
for text in df['text']:
    words = str(text).lower().split()
    all_words.extend(words)

unique_words = list(set(all_words))
word_to_idx = {word: idx for idx, word in enumerate(unique_words)}
print(word_to_idx['hey'])
print(word_to_idx['yo'])
