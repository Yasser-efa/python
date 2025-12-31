import numpy as np

# Dataset pour AND
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

y = np.array([0, 0, 0, 1])

class PerceptronAND():
  def __init__(self):
    self.weight = np.random.rand(2)
    self.biais = np.random.rand()

  def sigmoid(self, x):
    return 1/(1-np.exp(-x))
  
  def forward_pass(self,input):
    somme = (input @ self.weight) + self.biais
    return self.sigmoid(somme)

  def calculer_err(self, pred, cible):
    return (pred - cible)**2
    
  def calculer_grad(self, input, pred, cible):
    delta = (pred - cible) * pred * (1 - pred)

    grad_w = delta * input
    grad_b = delta

    return grad_w, grad_b