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

test_zero_1 = np.array([[0, 1, 1, 0],
                        [1, 0, 0, 1],
                        [1, 1, 0, 1],
                        [0, 1, 1, 0]])

test_zero_2 = np.array([[1, 1, 1, 0],
                        [1, 0, 0, 1],
                        [1, 0, 0, 1],
                        [0, 1, 1, 1]])

test_un_1 = np.array([[0, 0, 1, 0],
                      [0, 1, 1, 0],
                      [0, 0, 1, 1],
                      [0, 0, 1, 0]])

test_un_2 = np.array([[0, 1, 0, 0],
                      [0, 1, 1, 0],
                      [0, 0, 1, 0],
                      [0, 0, 1, 0]])

images_test = np.array([test_zero_1, test_zero_2, test_un_1, test_un_2])
labels_test = np.array([0, 0, 1, 1])

class ClassifieurImageKNN():
  def __init__(self):
    self.zero = None
    self.un = None

  def entrainer(self, images, labels):  
    self.images = images
    self.labels = labels

  def calc_distance(self, image1, image2):
    image1_flatten = image1.flatten()
    image2_flatten = image2.flatten()
    
    distance = np.sqrt(np.sum((image1_flatten - image2_flatten)**2))
    return distance

  def predire_type(self, image_inconnue):
    distances = []
    for i in range(len(self.images)):
      d = self.calc_distance(image_inconnue, self.images[i])
      distances.append((d, self.labels[i]))
    
    distances.sort(key=lambda x: x[0])

    return distances[0][1]
  
  def evaluer(self, images_Test, labels_test):
    correct = 0

    for i in range(len(images_Test)):
      pred = self.predire_type(images_Test[i])
      if pred == labels_test[i]:
        correct+=1

    precision = correct/(len(images_test))
    return precision
    
      

detect = ClassifieurImageKNN()
detect.entrainer(images_entrainement, labels_entrainement)
print(detect.predire_type(test_un_2))

precis = detect.evaluer(images_test, labels_test)

print(f"Precision de {precis:.1%}")