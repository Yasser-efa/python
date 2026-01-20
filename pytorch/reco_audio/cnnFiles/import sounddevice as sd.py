import sounddevice as sd
import numpy as np
# print(sd.query_devices())
print("Enregistrement 2 secondes...")
audio = sd.rec(int(2 * 16000), samplerate=16000, channels=1, dtype='float32', device=2)
sd.wait()
print(f"Volume max capté: {np.max(np.abs(audio)):.4f}")