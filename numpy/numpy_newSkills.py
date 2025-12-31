import numpy as np

# ndarray basique
arr = np.array([1,2,3])
print("array:")
print(arr)
print("//////////")

# arange -> crée liste sur portée donnée
arange = np.arange(0, 10, 2)
print("arange:")
print(arange)
print("//////////")

# crée une liste que de 0 (sur une portée donnée)
zeros = np.zeros(5)
print("zeros:")
print(zeros)
print("//////////")

# crée une liste que de 1 (sur une portée donnée)
ones = np.ones(5)
print("ones:")
print(ones)
print("//////////")

# crée une liste que d'une seule donnée (qu'on donne)
full = np.full(5,8)
print("full:")

print(full)
print("//////////")

# répète chaque élément d'une liste un certain nombre de fois
rpt = np.repeat(arr,5)
print("repeat:")
print(rpt)
print("//////////")

# répète la liste complète un certain nombre de fois
tile = np.tile(arr,3)
print("tile:")
print(tile)
print("//////////")

# fais une diagonale du top left à en bottom right ex de np.eye(4): 
# [[1. 0. 0. 0.]
#  [0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]]
# PS: np.idendtity() est le même que np.eye() sauf qu'ave eye on peut
# mettre une valeur k qui permet de décaler la diagonale vers la droite ou la gauche
eye = np.eye(4)
print("eye:")
print(eye)
print("//////////")

# exactement la meme que eye sauf qu'on choisit les valeurs de la diagonale (au lieu de 1 et 0 autour)
# EX:
# np.eye(4) :
# [[1. 0. 0. 0.]
#  [0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]]

# np.diag([10,20,30,40]) :
# [[10  0  0  0]
#  [ 0 20  0  0]
#  [ 0  0 30  0]
#  [ 0  0  0 40]]





# idées:
#     -Faire un programme qui calcule les moyennes des matières
#     -
#     -  
#     -     
#     -