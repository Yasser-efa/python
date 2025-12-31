from sklearn.datasets import fetch_openml
import numpy as np

mnist = fetch_openml('mnist_784', version=1, as_frame=False)
X = mnist.data # Shape: (7000, 784)
y = mnist.target # Shape: (7000,)

X = X / 255

def one_hot(label):
  vect = np.zeros(10)
  vect[int(label)] = 1
  return vect


class MNIST_mlp():
  def __init__(self):
    self.weight_InputToHiddenLayer = np.random.rand(784, 64) * 0.1
    self.biais_HiddenLayer = np.random.rand(64,) * 0.1

    self.weight_HiddenLayerToOutput = np.random.rand(64, 10) * 0.1
    self.biais_Output = np.random.rand(10) * 0.1

  def sigmoid(self,x):
    return 1 / (1+np.exp(-x))

  def forward(self, input):
    hidden = (input @ self.weight_InputToHiddenLayer) + self.biais_HiddenLayer # (7000, 784)*(784,64) = (7000,64)
    hidden = self.sigmoid(hidden)

    output = (hidden @ self.weight_HiddenLayerToOutput) + self.biais_Output
    return hidden, self.sigmoid(output)
  
  def backward(self, input, hidden, output, cible):
    delta_output = (output - cible) * output * (1 - output)
    delta_hidden = (delta_output @ self.weight_HiddenLayerToOutput.T) * hidden * (1-hidden)

    grad_w_hidden_to_output = delta_output.reshape(1,10) * hidden.reshape(64, 1)
    grad_b_output = delta_output

    grad_w_input_to_hidden = input.reshape(784, 1) * delta_hidden.reshape(1, 64)
    grad_b_hidden = delta_hidden

    return grad_w_input_to_hidden, grad_b_hidden, grad_w_hidden_to_output, grad_b_output
  
  def update(self, grad_w_hiddenToOutput, grad_b_output, grad_w_inputToHidden, grad_b_hidden, lr):
    self.weight_HiddenLayerToOutput -= (lr*grad_w_hiddenToOutput)
    self.biais_Output -= (lr*grad_b_output)

    self.weight_InputToHiddenLayer -= (lr*grad_w_inputToHidden)
    self.biais_HiddenLayer -= (lr*grad_b_hidden)

  def train(self, X, y, lr, epochs):
    for i in range(epochs):
      for j in range(len(X)):
        hidden, output = self.forward(X[j])
        cible = one_hot(y[j])
        gradWinpToHid, gradBhid, gradWhidToOut, gradBout = self.backward(X[j], hidden, output, cible)
        self.update(gradWhidToOut, gradBout, gradWinpToHid, gradBhid, lr)

mnist_mlp = MNIST_mlp()
mnist_mlp.train(X[:5000], y[:5000], lr=0.5, epochs=5)

# Teste sur des images que le réseau n'a PAS vues pendant l'entraînement
correct = 0
for i in range(5000, 5500):  # Images 5000 à 5500
    hidden, output = mnist_mlp.forward(X[i])
    prediction = np.argmax(output)
    if prediction == int(y[i]):
        correct += 1

print(f"Précision: {correct/500*100}%")
