import torch
import numpy as np
import librosa
import sounddevice as sd
from train import AudioCNN
from dataset import CLASSES, N_MELS, SAMPLE_RATE

# === CONFIG ===
MODEL_PATH = "reco_audio/cnnFiles/model_data/audio_model.pth"
DURATION = 1  # secondes

# === CHARGER LE MODÈLE ===
model = AudioCNN()
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()
print("Modèle chargé !")
print(f"Classes: {CLASSES}")
print("=" * 40)

def record_audio():
    """Enregistre 1 seconde d'audio depuis le micro"""
    print("\n🎤 Parle maintenant...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32', device=2)
    sd.wait()
    return audio.flatten()

def predict(audio):
    """Prédit le mot à partir de l'audio"""
    # Créer le spectrogramme
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=N_MELS)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # Convertir en tensor
    tensor = torch.tensor(mel_spec_db, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    
    # Prédiction
    with torch.no_grad():
        output = model(tensor)
        probas = torch.softmax(output, dim=1)
        pred_idx = output.argmax(dim=1).item()
        confidence = probas[0][pred_idx].item() * 100
    
    return CLASSES[pred_idx], confidence

# === BOUCLE PRINCIPALE ===
if __name__ == "__main__":
    print("\nDis 'yes', 'no', 'stop' ou 'go'")
    print("Appuie sur Ctrl+C pour quitter\n")
    
    while True:
        try:
            input("Appuie sur ENTER pour enregistrer...")
            audio = record_audio()
            word, confidence = predict(audio)
            print(f"✅ Prédit: '{word}' (confiance: {confidence:.1f}%)\n")
        except KeyboardInterrupt:
            print("\n\nAu revoir !")
            break
