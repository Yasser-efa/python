import numpy as np

# ========== image très ambiguë (Image qui ressemble autant à un 0 qu'à un 1) =========== 
image_vraiment_ambigue = np.array([
    [0, 1, 1, 0],  # Haut du 0
    [1, 0, 1, 0],  # Côté gauche du 0 + colonne du 1
    [1, 0, 0, 1],  # Bas du 0
    [0, 1, 1, 0]
])

# ========== 5 images de "0" (avec légères variations) ==========
zero_1 = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

zero_2 = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

zero_3 = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 1, 0, 1],  # Pixel bruité
    [0, 1, 1, 0]
])

zero_4 = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

zero_5 = np.array([
    [1, 1, 1, 0],  # Variation haut
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

# ========== 5 images de "1" (avec légères variations) ==========
un_1 = np.array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
])

un_2 = np.array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
])

un_3 = np.array([
    [0, 1, 0, 0],  # Décalé à gauche
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
])

un_4 = np.array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [1, 0, 1, 0]  # Pixel bruité en bas
])

un_5 = np.array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
])

# Images de test (jamais vues pendant l'entraînement)
test_zero_1 = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 1, 0, 1],  # Bruit
    [0, 1, 1, 0]
])

test_zero_2 = np.array([
    [1, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 1]  # Bruit
])

test_un_1 = np.array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],  # Bruit
    [0, 0, 1, 0]
])

test_un_2 = np.array([
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0]
])

images_test = np.array([test_zero_1, test_zero_2, test_un_1, test_un_2])
labels_test = np.array([0, 0, 1, 1])

# ========== Combinaison en dataset ==========
images_entrainement = np.array([
    zero_1, zero_2, zero_3, zero_4, zero_5,
    un_1, un_2, un_3, un_4, un_5
])

labels_entrainement = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

# =========== fonctions ============
def preparer_donnees(images, labels):
    """
    Transforme les données en format matriciel
    
    Paramètres:
        images: array numpy (nb_images, hauteur, largeur)
        labels: array numpy (nb_images,)
    
    Retourne:
        X: array (nb_images, nb_pixels) - images aplaties
        y: array (nb_images, nb_classes) - labels en one-hot
    """
    X = images.reshape(images.shape[0], -1)

    nb_classes = len(np.unique(labels))
    y = np.eye(nb_classes)[labels]

    return X, y



# =========== Classifieur Chiffres ===========

class ClassifieurChiffres():
  def __init__(self):
    self.pixels = {}

  def entrainer(self, image, label):
    for i in range(4):
      for j in range(4):
        compteur_0 = 0
        compteur_1 = 0

        for idx in range(len(image)):
          if image[idx][i, j] == 1:
            if label[idx] == 0:
              compteur_0 += 1
            else:  # label == 1
              compteur_1 += 1
        
        self.pixels[i, j] = (compteur_0, compteur_1)  # 2 catégories seulement
  
  def extraire_poids(self):
    """ Converti self.pixel en matrice W de dimensions (16, 2) """
    W = np.zeros((16,2))

    for pos, counts in self.pixels.items():
      i, j = pos
      index = i*4 + j
      
      count_0, count_1 = counts
      W[index, 0] = count_0
      W[index, 1] = count_1
    return W
      

  def softmax(self, scores):
    """Converti des scores en probabilités"""
    exp_scores = np.exp(scores)
    return exp_scores / np.sum(exp_scores)

  def predire(self, image, return_probas=False):
    nbcategories = len(self.pixels[(0,0)])
    scores = [0] * nbcategories

    for i in range(4):
      for j in range(4):
        if image[i, j] == 1:
          counts = self.pixels[(i, j)]
          for idx, count in enumerate(counts):
            scores[idx] += count
    if return_probas:
      probas = self.softmax(scores)
      return np.argmax(probas), probas
    else:
      return np.argmax(scores)
    
  def evaluer(self, image_test, label_test):
    correct = 0
    total = len(image_test)
      
    for idx in range(len(image_test)):
      prediction = self.predire(image_test[idx])
      if prediction == label_test[idx]:
        correct += 1
      
    precision = correct / total
    print(f"Précision: {precision:.1%} ({correct}/{total})")
    return precision
  
  def pixels_importants(self, top_n=5):
    pixels_pour_0 = []
    pixels_pour_1 = []
    
    # Boucle sur self.pixels
    for pos, counts in self.pixels.items():
        diff_0 = counts[0] - counts[1]  # Force pour catégorie 0
        diff_1 = counts[1] - counts[0]  # Force pour catégorie 1
        
        pixels_pour_0.append((pos, diff_0, counts[0], counts[1]))  # Ajoute aussi les counts
        pixels_pour_1.append((pos, diff_1, counts[1], counts[0]))
    
    # Trier par différence (2ème élément = index [1])
    pixels_pour_0.sort(key=lambda x: x[1], reverse=True)
    pixels_pour_1.sort(key=lambda x: x[1], reverse=True)
    
    # Afficher top_n pour catégorie 0
    print("Pixels caractéristiques du '0' :")
    for i in range(top_n):
        pos, diff, count_0, count_1 = pixels_pour_0[i]
        print(f"  Position {pos}: {count_0}x dans '0', {count_1}x dans '1' → diff = {diff}")
    
    # Afficher top_n pour catégorie 1
    print("\nPixels caractéristiques du '1' :")
    for i in range(top_n):
        pos, diff, count_1, count_0 = pixels_pour_1[i]
        print(f"  Position {pos}: {count_1}x dans '1', {count_0}x dans '0' → diff = {diff}")
  def predire_matriciel(self, image):
    """
    Prédiction avec opération matricielle (sans boucles)
    
    Paramètres:
        image: array (4, 4) - une seule image
    
    Retourne:
        prediction: int (0 ou 1)
    """
    # Étape 1 : Aplatir l'image (4,4) → (16,)
    x = np.reshape(image, -1)
    
    # Étape 2 : Extraire les poids
    W = self.extraire_poids()
    
    # Étape 3 : Calcul matriciel
    scores = x @ W  # x · W
    
    # Étape 4 : Retourner la catégorie avec le score max
    return np.argmax(scores)


#          /////////////////// PROGRAMME PRINCIPAL ////////////////////////////


# 1. Créer et entraîner
detecteur = ClassifieurChiffres()
detecteur.entrainer(images_entrainement, labels_entrainement)

print("=== TESTS AVEC PROBABILITÉS ===\n")

# Test sur zero_1
pred, probas = detecteur.predire(zero_1, return_probas=True)
print(f"Image zero_1:")
print(f"  Prédiction: {pred}")
print(f"  Probabilités: 0={probas[0]:.1%}, 1={probas[1]:.1%}")
print(f"  Confiance: {probas[pred]:.1%}\n")

# Test sur un_1
pred, probas = detecteur.predire(un_1, return_probas=True)
print(f"Image un_1:")
print(f"  Prédiction: {pred}")
print(f"  Probabilités: 0={probas[0]:.1%}, 1={probas[1]:.1%}")
print(f"  Confiance: {probas[pred]:.1%}\n")

# Test sur image ambiguë
image_ambigue = np.array([
    [0, 1, 1, 0],
    [1, 1, 1, 1],  # Mélange de patterns
    [1, 0, 1, 1],
    [0, 1, 1, 0]
])
pred, probas = detecteur.predire(image_ambigue, return_probas=True)
print(f"Image ambiguë:")
print(f"  Prédiction: {pred}")
print(f"  Probabilités: 0={probas[0]:.1%}, 1={probas[1]:.1%}")
print(f"  Confiance: {probas[pred]:.1%} ← Moins sûr !\n")

print("=======================================")
detecteur.evaluer(images_test, labels_test)

print("=======================================")

pred, probas = detecteur.predire(image_vraiment_ambigue, return_probas=True)
print(f"Image mixte:")
print(f"  Prédiction: {pred}")
print(f"  Probabilités: 0={probas[0]:.1%}, 1={probas[1]:.1%}")
print(f"  Confiance: {probas[pred]:.1%}")

print("=======================================")
print("=======================================")

# ========== TEST DE PRÉPARATION DES DONNÉES ==========
print("\n" + "=" * 50)
print("TEST DE PRÉPARATION DES DONNÉES")
print("=" * 50)

X_train, y_train = preparer_donnees(images_entrainement, labels_entrainement)
X_test, y_test = preparer_donnees(images_test, labels_test)

print(f"\nConversion réussie !")
print(f"X_train shape: {X_train.shape}")  # (10, 16)
print(f"y_train shape: {y_train.shape}")  # (10, 2)
print(f"X_test shape: {X_test.shape}")    # (4, 16)
print(f"y_test shape: {y_test.shape}")    # (4, 2)

print(f"\nPremière image (zero_1) :")
print(f"Original (4×4) :")
print(zero_1)
print(f"\nAplatie (16 pixels) :")
print(X_train[0])
print(f"\nLabel original: {labels_entrainement[0]}")
print(f"Label one-hot: {y_train[0]}")

print(f"\nSixième image (un_1) :")
print(f"Label original: {labels_entrainement[5]}")
print(f"Label one-hot: {y_train[5]}")

print(f"\nTous les labels one-hot :")
for i in range(len(y_train)):
    cat = "0" if labels_entrainement[i] == 0 else "1"
    print(f"Image {i} (catégorie {cat}): {y_train[i]}")

print(f"\nVérification (chaque ligne doit sommer à 1.0) :")
print(f"Sommes: {y_train.sum(axis=1)}")

print("=======================================")

detecteur.pixels_importants(top_n=5)

W = detecteur.extraire_poids()
print(f"Shape de W: {W.shape}")  # (16, 2)
print(f"\nPremières lignes de W:")
print(W[:5])  # Affiche les 5 premières lignes

# Comparaison des deux méthodes
print("=== COMPARAISON BOUCLES vs MATRICIEL ===\n")

pred_boucles = detecteur.predire(zero_1)
pred_matriciel = detecteur.predire_matriciel(zero_1)

print(f"zero_1:")
print(f"  Avec boucles: {pred_boucles}")
print(f"  Matriciel: {pred_matriciel}")
print(f"  Identique ? {pred_boucles == pred_matriciel} \n")

pred_boucles = detecteur.predire(un_1)
pred_matriciel = detecteur.predire_matriciel(un_1)

print(f"un_1:")
print(f"  Avec boucles: {pred_boucles}")
print(f"  Matriciel: {pred_matriciel}")
print(f"  Identique ? {pred_boucles == pred_matriciel} ")