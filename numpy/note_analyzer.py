import numpy as np

# points de 5 étudiants sur 4 matières
points = np.array([
    [15, 12, 18, 14],  # Étudiant 0
    [10, 8, 12, 9],    # Étudiant 1
    [18, 16, 19, 17],  # Étudiant 2
    [12, 14, 11, 13],  # Étudiant 3
    [8, 9, 7, 10]      # Étudiant 4
])

# Noms des matières (pour référence)
matieres = ["Maths", "Physique", "Info", "Anglais"]

# TODO: Affiche la shape du array 'points'
# Combien d'étudiants ? Combien de matières ?

def array_info(array):
  Shape = np.shape(array)
  nb_students = Shape[0]
  nb_classes = Shape[1]
  return nb_students, nb_classes
print(f"Number of students: {array_info(points)[0]}, number of classes: {array_info(points)[1]}")
# TODO: Quelle est la note en Info (colonne 2) de l'étudiant 2 ?
# Affiche : "L'étudiant 2 a eu X en Info"

def student_points(student):
  array_info(points)
  return points[student][2]
print(student_points(2))
# TODO: Calcule la moyenne de l'étudiant 0
# Indice : tu peux utiliser np.mean() ou faire la somme / 4

print(f"Mean of student 0: {np.mean(points[0])}")

# TODO: Pour chaque matière, calcule la moyenne de la classe
# Quelle matière a la moyenne la plus élevée ?
# Affiche : "La meilleure matière est X avec une moyenne de Y"

points_T = points.T.copy()
for i in range(len(points_T)):
  print(f"{points_T[i]} {matieres[i]}")

means_class = []
for i in range(len(points_T)):
  means_class.append(points_T[i].mean())
idx_max = np.argmax(means_class)
maxClass_X = matieres[idx_max]
maxClass_Y = means_class[idx_max]
print(f"La meilleure matière est {maxClass_X} avec une moyenne de {maxClass_Y}")


# TODO: Quel étudiant a la meilleure moyenne générale ?
# Affiche : "L'étudiant X est le meilleur avec une moyenne de Y"

means_stu = []
for i in range(len(points)):
  means_stu.append(points[i].mean())
idx_maxx = np.argmax(means_stu)
maxStu_X = idx_maxx
maxStu_Y = means_stu[idx_maxx]
print(f"L'étudiant {maxStu_X} a eu la meilleure moyenne qui est de {maxStu_Y}")