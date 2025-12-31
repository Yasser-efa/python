import numpy as np

class MLP:
    def __init__(self):
        # Poids et biais INPUT → CACHÉE
      self.weight_InputToHiddenLayer = np.random.rand(2,2)
      self.biais_HiddenLayer = np.random.rand(2,)
        # Poids et biais CACHÉE → SORTIE
      self.weight_HiddenLayerToOutput = np.random.rand(2,1)
      self.biais_Output = np.random.rand()

    def sigmoid(self, x):
      return 1 / (1 + np.exp(-x))

    def forward(self, input):
      hidden = (input @ self.weight_InputToHiddenLayer) + self.biais_HiddenLayer
      hidden = self.sigmoid(hidden)

      output = (hidden @ self.weight_HiddenLayerToOutput) + self.biais_Output
      return hidden, self.sigmoid(output)
    
    def backward(self, input, hidden, output, cible):
      delta_output = (output - cible) * output * (1 - output)
      delta_hidden = (delta_output @ self.weight_HiddenLayerToOutput.T) * hidden * (1 - hidden)

    # Gradients couche CACHÉE → SORTIE
      grad_w_hidden_to_output = delta_output * hidden.reshape(2,1)
      grad_b_output = delta_output
    
    # Gradients couche INPUT → CACHÉE
      grad_w_input_to_hidden = delta_hidden * input
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
          gradWinpToHid, gradBhid, gradWhidToOut, gradBout = self.backward(X[j], hidden, output, y[j])
          self.update(gradWhidToOut, gradBout, gradWinpToHid, gradBhid, lr)

       

mlp = MLP()

X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

y = np.array([0, 1, 1, 0])  # XOR

print("Avant entraînement:")
for i in range(len(X)):
    hidden, output = mlp.forward(X[i])
    print(f"{X[i]} → {output}")

mlp.train(X, y, lr=0.5, epochs=10000)

print("\nAprès entraînement:")
for i in range(len(X)):
    hidden, output = mlp.forward(X[i])
    print(f"{X[i]} → {output}")