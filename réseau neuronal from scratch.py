import numpy as np
import os
import urllib.request
import gzip
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense
import keras

#1. On donne au modèle les images et leurs étiquettes et on les transforme en matrices

#Lien vers un site contenant les pixels
URL_IMAGES = "https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz"
chemin_images = "data/train-images-idx3-ubyte.gz"

#Lien vers un site contenant les étiquettes
URL_ETIQUETTES = "https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz"
chemin_etiquettes = "data/train-labels-idx1-ubyte.gz"

#si "data" n'existe pas encore sur l'ordi, le créer
if not os.path.exists("data"):
    os.makedirs("data")

# on vérifie si le fichier n'est pas déjà téléchargé
if not os.path.exists(chemin_images):
    print("Téléchargement du vrai fichier d'images...")

# On envoie la requête en tant que navigateur pour éviter les blocages
    requete = urllib.request.Request(URL_IMAGES, headers={'User-Agent': 'Mozilla/5.0'})

# Le programme fait la requête, la transforme en binaire et l'écrit dans le fichier
    with urllib.request.urlopen(requete) as reponse, open(chemin_images, 'wb') as fichier_sortie:
        fichier_sortie.write(reponse.read())
    print("Téléchargement réussi !")

#Même structure que pour le fichier d'images
if not os.path.exists(chemin_etiquettes):
    print("Téléchargement du vrai fichier d'étiquettes...")
    requete = urllib.request.Request(URL_ETIQUETTES, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(requete) as reponse, open(chemin_etiquettes, 'wb') as fichier_sortie:
        fichier_sortie.write(reponse.read())
    print("Téléchargement réussi !")


with gzip.open(chemin_etiquettes, "rb") as f:
    f.read(8)  # On saute l'en-tête de 8 octets
    toutes_les_etiquettes = np.frombuffer(f.read(), dtype=np.uint8)
    print("Nombre total d'étiquettes chargées :", len(toutes_les_etiquettes))


# Lecture et décompression
with gzip.open(chemin_images, "rb") as f:
    f.read(16) # On saute l'en-tête
    tous_les_pixels = np.frombuffer(f.read(), dtype=np.uint8)

images = tous_les_pixels.reshape(60000, 784)
etiquettes = toutes_les_etiquettes.reshape(60000, 1)

# 1. On télécharge et on récupère le dataset MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# 2. On aplatit les images pour notre modèle (60000 images de 784 pixels)
images = X_train.reshape(60000, 784)

# 3. Lignes de vérification (on les commente avec # pour ne plus bloquer le script)
# premiere_image = images[0].reshape(28, 28)
# plt.imshow(premiere_image, cmap='gray')
# plt.show()

#2. On crée la structure de L'IA (on ne donne pas d'instructions à une IA, on lui donne une structure)

modele=Sequential()#on utilise la fonction sequential pour créer une structure en couches
modele.add(keras.Input(shape=(784,)))#on crée la première couche composé de 64 neurones
modele.add(Dense(64, activation='relu'))#on crée la deuxième couche composé de 10 neurones assocuié chacun à un chiffre
modele.add(Dense(10, activation='softmax'))
#softmax et relu son des fonctions d'activation

modele.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
modele.fit(images, y_train, epochs=5)

# On prépare les 10 000 images de test (mêmes dimensions)
images_test = X_test.reshape(10000, 784)

# On demande au modèle de calculer son score sur ces images inconnues
score = modele.evaluate(images_test, y_test)
print("Précision sur les images de test :", score[1])

# 1. On prend la première image (index 0) du dataset de test
une_image = images_test[0]

# 2. Keras a besoin qu'on lui donne une liste d'images.
# On transforme notre image seule en une liste contenant 1 image grâce à reshape.
image_a_predire = une_image.reshape(1, 784)

# 3. L'IA fait sa prédiction (elle renvoie les 10 probabilités)
predictions = modele.predict(image_a_predire)

# 4. On cherche quel neurone a le plus gros score (entre 0 et 9)
chiffre_devine = predictions.argmax()

print("L'IA a analysé l'image et elle pense que c'est le chiffre :", chiffre_devine)
print("Le vrai chiffre était :", y_test[0])

modele.save('mon_modele_ia.keras')



