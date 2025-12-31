import numpy as np

def relu(x):
  return max(0,x)

class Couche():
  def __init__(self, nb_entrees, nb_neurones):
    self.weight = np.random.randn(nb_entrees,nb_neurones)
    self.biais = np.zeros((1,nb_neurones))

class Neurone():
  def __init__(self):
    self.weight = np.random.randn(1,3)
    self.biais = np.zeros((1,3))

  def prediction(self, x):
    predi = (x * self.weight)+self.biais
    return relu(predi), predi
  
  def calculer_erreur(self, prediction, cible):
    erreur = (prediction - cible)**2
    return erreur
  
  def calculer_gradients(self, x, z, prediction, cible):
    grad_w = 2*(prediction-cible)*x
    grad_b = 2*(prediction-cible)
    if z <= 0:
      return (0,0)
    else:
      return grad_w, grad_b
  
  def apprendre(self, x, cible, lr):
    sortie, z = self.prediction(x)
    grad_w, grad_b = self.calculer_gradients(x,z,sortie,cible)
    self.weight -= lr * grad_w
    self.biais -= lr * grad_b
    return self.weight, self.biais
  

# n = Neurone()
# print(n.weight)  # Pour voir le poids aléatoire
# print(n.prediction(2))  # Entrée = 2

# n = Neurone()
# print(f"Poids initial : {n.weight}")

# # On entraîne plusieurs fois avec entrée=3, cible=6
# for i in range(1000):
#     n.apprendre(x=3, cible=6, lr=0.001)

# print(f"Poids final : {n.weight}")
# print(f"Test : n.prediction(3) = {n.prediction(3)}")
# print(f"Test : n.prediction(5) = {n.prediction(5)}")

n = Neurone()
print(f"Poids initial : {n.weight}, Biais initial : {n.biais}")

# Entraînement avec plusieurs exemples
for i in range(1000):
    n.apprendre(x=1, cible=5, lr=0.01)   # 2×1 + 3 = 5
    n.apprendre(x=2, cible=7, lr=0.01)   # 2×2 + 3 = 7
    n.apprendre(x=4, cible=11, lr=0.01)  # 2×4 + 3 = 11

print(f"Poids final : {n.weight}, Biais final : {n.biais}")
print(f"Test : n.prediction(3) = {n.prediction(3)}")  # Devrait être ~9