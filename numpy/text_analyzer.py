import numpy as np
import re

def analyser_texte(texte):
    # 1. Nettoyage
    texte = texte.lower()
    texte = re.sub(r'[^\w\s]', ' ', texte)
    texte = [str(car) for car in texte.split()]
    
    print("Mots nettoyés:", texte)
    
    # 2. Stats
    mots_unique, comptes = np.unique(texte, return_counts=True)
    
    # Option liste complète
    input_liste = input("Voulez-vous une liste avec tous les mots et leur fréquence ? (O/N) ")
    if input_liste.lower() == "o" or input_liste.lower() == "oui":
        for i in range(len(mots_unique)):
            print(f"{mots_unique[i]}: {comptes[i]}")
    
    # Top 3
    indices_tries = np.argsort(comptes)
    top3_indices = indices_tries[-3:]  # Indices des 3 plus fréquents
    
    print("\n🏆 TOP 3 des mots les plus fréquents:")
    for rang, idx in enumerate(top3_indices[::-1], 1):  # [::-1] pour du plus au moins fréquent
        print(f"{rang}. {mots_unique[idx]} (fréquence: {comptes[idx]})")
    
    # 4. Affichage professionnel (autres stats à ajouter)
    print(f"\n📊 Autres stats:")
    print(f"Nombre total de mots: {len(texte)}")
    print(f"Nombre de mots uniques: {len(mots_unique)}")

analyser_texte(input("Veuillez écrire une phrase: "))