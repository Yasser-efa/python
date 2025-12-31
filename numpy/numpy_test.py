import numpy as np

def creer_drapeau_france():
    """Crée le drapeau français en ASCII avec numpy"""
    # Crée une grille 9x15 (hauteur x largeur)
    drapeau = np.full((9, 15), ' ')  # Grille vide
    
    # Colonne bleue (3 colonnes)
    drapeau[:, 0:3] = '█'
    
    # Colonne blanche (3 colonnes)
    drapeau[:, 6:9] = '█'
    
    # Colonne rouge (3 colonnes)
    drapeau[:, 12:] = '█'
    
    return drapeau

def creer_croix():
    """Crée une croix suisse"""
    croix = np.full((9, 9), ' ')
    
    # Barre verticale
    croix[:, 4] = '█'
    
    # Barre horizontale
    croix[4, :] = '█'
    
    return croix

def creer_damier(taille=8):
    """Crée un damier d'échecs"""
    damier = np.full((taille, taille), ' ')
    
    # Utilise tile et repeat pour créer le motif
    ligne1 = np.tile([' ', '█'], taille//2)
    ligne2 = np.tile(['█', ' '], taille//2)
    
    # Répète les lignes alternativement
    for i in range(taille):
        if i % 2 == 0:
            damier[i] = ligne1
        else:
            damier[i] = ligne2
    
    return damier

def creer_logo_numpy():

    """Crée un logo Numpy simplifié"""
    logo = np.full((7, 15), ' ')
    
    # Lettre N
    logo[:, 0] = '█'  # Première colonne
    logo[:, 14] = '█'  # Dernière colonne
    perm = 1
    # Diagonale de la N
    for i in range(7):
        logo[i, i*2] = '█'
    # ligne milieu
        logo[3, i*2] = '█'
        logo[4, i*2] = '█'

        logo[i, 7] = '█'
    # diagonale inversée
    for i in range(6,0,-1):
        logo[i, perm*2] = '█'
        perm += 1
        
    
    return logo

def creer_coeur():
    """Crée un cœur simple"""
    coeur = np.full((7, 7), ' ')
    
    # À toi de jouer avec les indices !
    coeur[0, 1:6] = '❤'
    coeur[0, 2:5] = ' '
    coeur[1, 0] = '❤'
    coeur[1, 6] = '❤'
    coeur[1, 3] = '❤'

    
    for i in range(4):
        coeur[2:i+2, i] = '❤'
    
    for i in range(6, 0, 1):
        coeur[2:, i] = '❤'
    # Continue...
    
    return coeur



# Afficher tous les motifs


print("Drapeau français:")
for ligne in creer_drapeau_france():
    print(''.join(ligne))

print("Croix suisse:")
for ligne in creer_croix():
    print(''.join(ligne))

print("Damier 8x8:")
for ligne in creer_damier():
    print(''.join(ligne))

print("Logo Numpy stylisé:")
for ligne in creer_logo_numpy():
    print(''.join(ligne))

print("Coeur:")
for ligne in creer_coeur():
    print(''.join(ligne))