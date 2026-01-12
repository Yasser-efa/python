import json
from first_real_NLP import FirstNLP_LSTM, text_to_sequence, pad_sequence
import torch
from flask import Flask, request, send_file

with open("pytorch/web_project_nlp/backend/training_data/word_to_idx.json", 'r') as f:
    word_to_idx = json.load(f)

model = FirstNLP_LSTM(vocab_size=len(word_to_idx))

model.load_state_dict(torch.load("pytorch/web_project_nlp/backend/training_data/firstnlp_lstm.pth"))
app = Flask(__name__)

@app.route("/home")
def home():
    return send_file("../frontend/index.html")

@app.route("/predict", methods=["POST"])
def predict():
    model.eval()
    user_txt = request.form["user_text"]
    user_txt = text_to_sequence(user_txt, word_to_idx)
    user_txt = pad_sequence(user_txt, 50)
    user_txt = torch.tensor(user_txt).unsqueeze(0)
    with torch.no_grad():
        output = model(user_txt)   
        pred = output.argmax(dim=1)
    if pred == 0:
        pred = "Positive"
    elif pred == 1:
        pred = "Negative"
    else:
        pred = "Neutral"
    return pred
app.run()