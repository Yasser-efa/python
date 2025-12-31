import numpy as np

# Dataset pour AND
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

y = np.array([0, 1, 1, 0])

# Initialise 2 poids et 1 biais avec des valeurs aléatoires
# Comment tu ferais ?

class PerceptronAND():
  def __init__(self):
    self.weight = np.random.rand(2)
    self.biais = np.random.rand()

  def sigmoid(self, x):
    return 1 / (1 + np.exp(-x))
  
  def forward_pass(self, input):
    somme = (input @ self.weight) + self.biais
    return self.sigmoid(somme)
  
  def calculer_err(self, pred, cible):
    return (pred - cible)**2
  
  def calculer_gradients(self, input, prediction, cible):
    delta = (prediction - cible) * prediction * (1 - prediction)

    grad_w = delta * input
    grad_b = delta

    return grad_w, grad_b
  
  def mettre_a_jour(self, grad_w, grad_b, lr):
    self.weight -= (lr * grad_w)
    self.biais -= (lr * grad_b)

  def entrainer(self, X, y, lr, epochs):
    # À toi de jouer
    for i in range(epochs):
      for j in range(len(X)):
        pred = self.forward_pass(X[j])
        err = self.calculer_err(pred, y[j])
        grad_w, grad_b = self.calculer_gradients(X[j], pred, y[j])
        self.mettre_a_jour(grad_w, grad_b, lr)

# Crée ton perceptron
perceptron = PerceptronAND()

# Teste avec un input
prediction = perceptron.forward_pass(X)

print("Avant l'entrainement du perceptron:")

print(f"Poids: {perceptron.weight}")
print(f"Biais: {perceptron.biais}")
print(f"Input: {X}")
print(f"Prédiction: {prediction}")
print(f"Réel: {y}")

print("Après l'entrainement du perceptron:")

print("entrainement avec 1000 epochs...")
perceptron.entrainer(X,y,0.5,1000)
print(f"Poids: {perceptron.weight}")
print(f"Biais: {perceptron.biais}")
print(f"Input: {X}")
prediction_upd = perceptron.forward_pass(X)
print(f"Prédiction: {prediction_upd}")
print(f"Réel: {y}")