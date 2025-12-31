import numpy as np
import math

# Températures relevées pendant une semaine (en °C)
temperatures = np.array([22, 24, 23, 25, 45, 21, 23])
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


standard_deviation = np.std(temperatures)

print("Températures de la semaine :")
for i, jour in enumerate(jours):
    print(f"{jour}: {temperatures[i]}°C")

# TODO: Calcule la température moyenne de la semaine
# Affiche : "Température moyenne : X°C"

mean_t = np.mean(temperatures)
print(f"Mean of the temperature : {mean_t:.2f}°C")

# TODO: Trouve les jours où température > moyenne + 10°C
# Affiche chaque jour anormal avec sa température
# Exemple : "⚠️ Vendredi : 45°C (anomalie !)"

days_anomaly = {}
for i in range(len(temperatures)):
    if temperatures[i] > mean_t + 2 * standard_deviation or temperatures[i] < mean_t - 2 * standard_deviation:
        days_anomaly.update({jours[i] : temperatures[i]})

print(f"The days with an anomaly detected are : {days_anomaly}")

# TODO: Remplace les températures anormales par la moyenne
# Crée un nouveau array 'temperatures_corrigees'
# N'oublie pas de créer une COPIE de l'array original !

temp_corr = temperatures.copy()
for i in range(len(temperatures)):
    if temperatures[i] > mean_t + 2 * standard_deviation or temperatures[i] < mean_t - 2 * standard_deviation:
        temp_corr[i] = mean_t


# TODO: Affiche les deux versions côte à côte
# Exemple :
# Lundi    : 22°C → 22°C
# ...
# Vendredi : 45°C → 24°C (corrigé)  

for i in range(len(temp_corr)):
    if temperatures[i] == temp_corr[i]:
        print(f"{jours[i]}: {temperatures[i]}°C => {temp_corr[i]}°C")
    else:
        print(f"{jours[i]}: {temperatures[i]}°C => {temp_corr[i]}°C (corrected)")


# TODO: Affiche min, max, écart-type des températures
# Avant et après correction

print("Before correction:")
print(f"min: {min(temperatures)}, max: {max(temperatures)}, mean: {np.mean(temperatures):.2f}")
print("After correction:")
print(f"min: {min(temp_corr)}, max: {max(temp_corr)}, mean: {np.mean(temp_corr):.2f}")