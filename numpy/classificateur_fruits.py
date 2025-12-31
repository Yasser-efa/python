import numpy as np

# ========== DATASET D'ENTRAÎNEMENT (crée par Claude) ==========
# Format : [poids_en_grammes, couleur_rouge_sur_10]

pommes = np.array([
    [150, 8],  # Pomme 1 : lourde, très rouge
    [160, 9],  # Pomme 2 : lourde, très rouge
    [155, 7],  # Pomme 3 : lourde, rouge
    [145, 8]   # Pomme 4 : lourde, très rouge
])

bananes = np.array([
    [120, 2],  # Banane 1 : légère, peu rouge (jaune)
    [125, 1],  # Banane 2 : légère, peu rouge
    [118, 3],  # Banane 3 : légère, peu rouge
    [122, 2]   # Banane 4 : légère, peu rouge
])

print("=== DATASET D'ENTRAÎNEMENT ===")
print("Pommes [poids, couleur_rouge] :")
print(pommes)
print("\nBananes [poids, couleur_rouge] :")
print(bananes)

# ========== FRUITS À TESTER ==========
fruit_inconnu_1 = np.array([140, 5])  # Ambigu
fruit_inconnu_2 = np.array([165, 9])  # Clairement pomme
fruit_inconnu_3 = np.array([115, 1])  # Clairement banane

print("\n=== FRUITS À CLASSIFIER ===")
print(f"Fruit 1 : poids={fruit_inconnu_1[0]}g, rouge={fruit_inconnu_1[1]}/10")
print(f"Fruit 2 : poids={fruit_inconnu_2[0]}g, rouge={fruit_inconnu_2[1]}/10")
print(f"Fruit 3 : poids={fruit_inconnu_3[0]}g, rouge={fruit_inconnu_3[1]}/10")

class ClassifieurFruits:
    def __init__(self):
      # TODO: Quoi stocker ?
      self.pommes = None
      self.bananes = None

    def entrainer(self, pommes, bananes):
      # TODO: Stocker les données d'entraînement
      self.pommes = pommes
      self.bananes = bananes
    
    def calculer_distance(self, fruit1, fruit2):
      # TODO: Calculer la distance euclidienne
      distance = np.sqrt((fruit1[0] - fruit2[0])**2 + (fruit1[1] - fruit2[1])**2)
      return distance
    
    def predire(self, fruit_inconnu):
      # TODO: Trouver le fruit le plus proche
      distance_pommes = []
      distance_bananes = []

      for i in range(len(self.pommes)):
        dist = self.calculer_distance(fruit_inconnu, self.pommes[i])
        distance_pommes.append(dist)

      for i in range(len(bananes)):
        dist = self.calculer_distance(fruit_inconnu, self.bananes[i])
        distance_bananes.append(dist)
        
      if np.min(distance_bananes) < np.min(distance_pommes):
        print(f"Plus proche de la banane car {np.min(distance_bananes):.2f} < {np.min(distance_pommes):.2f}")
        return "banane"
      else:
        print(f"Plus proche de la pomme car {np.min(distance_bananes):.2f} > {np.min(distance_pommes):.2f}")
        return "pomme"

# Test
detecteur = ClassifieurFruits()
detecteur.entrainer(pommes, bananes)

print("\n=== PRÉDICTIONS ===")
pred1 = detecteur.predire(fruit_inconnu_1)
print(f"Fruit 1 → {pred1}\n")

pred2 = detecteur.predire(fruit_inconnu_2)
print(f"Fruit 2 → {pred2}\n")

pred3 = detecteur.predire(fruit_inconnu_3)
print(f"Fruit 3 → {pred3}")