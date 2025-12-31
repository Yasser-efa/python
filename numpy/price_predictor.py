import numpy as np

# Surface des maisons (en m²)
surfaces = np.array([50, 60, 80, 100, 120, 150])

# Prix des maisons (en milliers d'€)
prix_arr = np.array([150, 180, 240, 300, 360, 450])

print("Dataset d'entraînement :")
for i in range(len(surfaces)):
    print(f"Maison {i+1}: {surfaces[i]}m² → {prix_arr[i]}k€")




## 🧠 Concept : Régression linéaire simple

# **Idée :** Trouver la relation entre surface et prix

# prix ≈ coefficient × surface

# TODO: Divise chaque prix par sa surface
# Calcule la moyenne de ces ratios
# C'est ton coefficient !

# Indice : prix[i] / surfaces[i] pour chaque maison

prix_surf = prix_arr / surfaces
print("Méthode vectorisée:", prix_surf)
coef = np.mean(prix_surf)
print(prix_surf)
# TODO: Prédire le prix d'une maison de 90m²
# Formule : prediction = coefficient × surface

surface_test = 90
# prediction = ???
prediction = coef * surface_test

# TODO: Pour chaque maison du dataset, calcule l'erreur
# Erreur = |prix_réel - prix_prédit|
# Affiche l'erreur moyenne

# Indice : utilise une boucle et np.abs() pour la valeur absolue
pred = coef * surfaces  # Calcul vectoriel
erreurs = np.abs(prix_arr - pred)  # Calcul vectoriel

print("Erreurs:", erreurs)

# TODO: Pour chaque maison, affiche :
# "Maison X: réel=300k€, prédit=295k€, erreur=5k€"

for i in range(len(prix_arr)):
    print(f"Maison {i+1}: réel={prix_arr[i]}k€, prédit{pred[i]}k€, erreur={erreurs[i]}k€")

nouvelles_surfaces = np.array([70, 110, 140])
# TODO: Prédire le prix de chacune

pred_nouv_surf = coef * nouvelles_surfaces

print(pred_nouv_surf)