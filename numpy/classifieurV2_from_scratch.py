import numpy as np

# ========== DATASET (fourni) ==========

zero_1 = np.array([[0, 1, 1, 0],
                   [1, 0, 0, 1],
                   [1, 0, 0, 1],
                   [0, 1, 1, 0]])

zero_2 = np.array([[0, 1, 1, 0],
                   [1, 0, 0, 1],
                   [1, 0, 0, 1],
                   [0, 1, 1, 0]])

zero_3 = np.array([[0, 1, 1, 0],
                   [1, 0, 0, 1],
                   [1, 1, 0, 1],
                   [0, 1, 1, 0]])

zero_4 = np.array([[0, 1, 1, 0],
                   [1, 0, 0, 1],
                   [1, 0, 0, 1],
                   [0, 1, 1, 0]])

zero_5 = np.array([[1, 1, 1, 0],
                   [1, 0, 0, 1],
                   [1, 0, 0, 1],
                   [0, 1, 1, 0]])

un_1 = np.array([[0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]])

un_2 = np.array([[0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]])

un_3 = np.array([[0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]])

un_4 = np.array([[0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [1, 0, 1, 0]])

un_5 = np.array([[0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]])

images_entrainement = np.array([zero_1, zero_2, zero_3, zero_4, zero_5,
                                 un_1,  un_2,   un_3,   un_4,   un_5])
labels_entrainement = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

test_zero_1 = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 1, 0]])
test_zero_2 = np.array([[1, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 1]])

test_un_1 = np.array([[0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 1, 0]])
test_un_2 = np.array([[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]])

images_test = np.array([test_zero_1, test_zero_2, test_un_1, test_un_2])
labels_test = np.array([0, 0, 1, 1])

print("Dataset chargé !")
print(f"Entraînement : {images_entrainement.shape}")
print(f"Test : {images_test.shape}")

# ========== Classifieur Images ==========

class ClassifieurChiffres:
    def __init__(self):
        self.pixels = {}
    
    def entrainer(self, images, labels):
        for i in range(4):
            for j in range(4): # preparer les deux premieres boucles donc i, j
                compteur_0 = 0
                compteur_1 = 0
                for idx in range(len(images)):
                    if images[idx][i, j] == 1: # les (i, j) utiliser pour l'image 1 (qui est -> idx)
                        if labels[idx] == 1:
                            compteur_1 += 1
                        else:
                            compteur_0 += 1
                self.pixels[(i, j)] = (compteur_0, compteur_1)

    
    def predire(self, image):
        score_0 = 0
        score_1 = 0
        
        for i in range(4):
            for j in range(4):
                if image[i, j] == 1:
                    # TODO: Récupérer les compteurs de cette position
                    count_0, count_1 = self.pixels[(i,j)]
                    
                    # TODO: Ajouter aux scores
                    score_0 += count_0
                    score_1 += count_1
        
        # TODO: Retourner 0 ou 1 selon qui a le plus grand score
        if score_0 > score_1 :
            return 0
        else:
            return 1
    
    def evaluer(self, images, labels):
        correct = 0
        total = len(images)
        for idx in range(len(images)):
            prediction = self.predire(images[idx])

            if prediction == labels[idx]:
                correct+=1          

        precision = (correct / total)
        print(f"Précision de {precision:.1%} ({correct}/{total})")
        return precision
    
# Test
detecteur = ClassifieurChiffres()
detecteur.entrainer(images_entrainement, labels_entrainement)

print("Entraînement terminé !")
print(f"Position (0, 1): {detecteur.pixels[(0, 1)]}")
print(f"Position (2, 2): {detecteur.pixels[(2, 2)]}")
print(f"Nombre de positions: {len(detecteur.pixels)}")


print("\n" + "="*50)
print("TEST COMPLET DU CLASSIFICATEUR")
print("="*50)

# Entraînement
detecteur = ClassifieurChiffres()
detecteur.entrainer(images_entrainement, labels_entrainement)
print("✅ Entraînement terminé !")

# Tests individuels
print("\n=== PRÉDICTIONS INDIVIDUELLES ===")
pred = detecteur.predire(zero_1)
print(f"zero_1 → {pred} (attendu: 0) {'✅' if pred == 0 else '❌'}")

pred = detecteur.predire(un_1)
print(f"un_1 → {pred} (attendu: 1) {'✅' if pred == 1 else '❌'}")

# Évaluation complète
print("\n=== ÉVALUATION SUR JEU DE TEST ===")
detecteur.evaluer(images_test, labels_test)

print("\n🎉 Classificateur terminé !")

# Position (0, 1): (5, 1)  # ou similaire
# Position (2, 2): (0, 5)  # ou similaire
# Nombre de positions: 16