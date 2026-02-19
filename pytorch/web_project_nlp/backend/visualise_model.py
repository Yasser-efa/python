
import torch
import json
from torchviz import make_dot
from first_real_NLP import FirstNLP, FirstNLP_LSTM
import os

# Obtenir le dossier du script actuel
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VOCAB_PATH = os.path.join(SCRIPT_DIR, "training_data", "word_to_idx.json")

with open(VOCAB_PATH, 'r') as f:
    word_to_idx = json.load(f)

vocab_size = len(word_to_idx)
print(f"Vocab size: {vocab_size}")

model = FirstNLP(vocab_size)

dummy_input = torch.randint(0, vocab_size, (1, 50))
output = model(dummy_input)
print(f"Output shape: {output.shape}")

# Visualisation
dot = make_dot(output, params=dict(model.named_parameters()))
dot.save("firstnlp_graph.dot")
print("Graphe sauvegardé dans firstnlp_graph.dot")
print("Ouvre-le sur https://dreampuf.github.io/GraphvizOnline/")
print("Graphe sauvegardé dans firstnlp_graph.png")