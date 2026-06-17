import keras
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
import numpy as np


# On charge le modèle
modele = keras.models.load_model('mon_modele_ia.keras')

print("Le modèle a été chargé avec succès!")


class AppDessin:
    def __init__(self, fenetre_principale):
        self.fenetre = fenetre_principale
        self.fenetre.title("Mon IA Dessin")

        self.canvas = tk.Canvas(self.fenetre, width=280, height=280, bg="white")
        self.canvas.pack(pady=10)

        # Vérifie bien cette ligne : il y a un 's' à self.dessiner, mais sans parenthèses () à la fin
        self.canvas.bind("<B1-Motion>", self.dessiner)

        #  Bouton pour deviner
        self.btn_deviner = tk.Button(self.fenetre, text="Deviner", command=self.predire)
        self.btn_deviner.pack(side=tk.LEFT, padx=20)

        #Bouton pour effacer
        self.btn_effacer = tk.Button(self.fenetre, text="Effacer", command=self.effacer)
        self.btn_effacer.pack(side=tk.RIGHT, padx=20)

        # On crée une image blanche en mémoire de 280x280 pixels
        # "L" signifie qu'elle est en niveaux de gris (noir et blanc)
        self.image_pil = Image.new("L", (280, 280), color=255)
        # On crée un texte pour guider l'utilisateur
        self.label_correction = tk.Label(self.fenetre, text="Si l'IA s'est trompée, clique sur le bon chiffre :")
        self.label_correction.pack(pady=5)

        # On crée un cadre pour aligner les 10 boutons horizontalement
        cadre_boutons = tk.Frame(self.fenetre)
        cadre_boutons.pack(pady=5)

        # On crée les boutons de 0 à 9 avec une boucle
        for i in range(10):
            # Le "lambda" permet de passer le numéro du bouton à la fonction de correction
            btn = tk.Button(cadre_boutons, text=str(i), width=2, command=lambda c=i: self.corriger_ia(c))
            btn.pack(side=tk.LEFT, padx=2)

    def dessiner(self, event):
        #  8 espaces ici (4 pour être dans la fonction, 4 pour être dans la classe)
        x, y = event.x, event.y
        r = 15
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black", outline="black")

        # On dessine exactement la même chose sur l'image invisible
        # fill=0 signifie "noir" dans le langage de Pillow pour les images en niveaux de gris
        draw = ImageDraw.Draw(self.image_pil)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=0)

    def effacer(self):
        # On demande au canvas de supprimer tout ce qui est dessiné dessus
        self.canvas.delete("all")
        self.image_pil = Image.new("L", (280, 280), color=255)

    def predire(self):
        # 1. On rétrécit l'image de 280x280 à 28x28 pixels
        img_petite = self.image_pil.resize((28, 28))

        # 2. On inverse les couleurs (le dessin devient blanc sur fond noir)
        img_inversee = ImageOps.invert(img_petite)

        # 3. On transforme l'image en un tableau de nombres grâce à numpy
        tab_pixels = np.array(img_inversee)

        # 4. On aplatit le tableau en une seule ligne de 784 pixels pour le modèle simple
        donnees_ia = tab_pixels.reshape(1, 784)

        # 5. On remet les pixels entre 0 et 1 (normalisation)
        donnees_ia = donnees_ia / 255.0

        # 6. ON SAUVEGARDE le dessin propre pour la fonction de correction
        self.dernier_dessin = donnees_ia

        # 7. On demande la prédiction à l'IA
        prediction = modele.predict(donnees_ia)

        # 8. On cherche le numéro du chiffre deviné
        chiffre_devine = prediction.argmax()

        print("--- RÉSULTAT ---")
        print("L'IA pense que tu as dessiné un :", chiffre_devine)


    def corriger_ia(self, vrai_chiffre):
        # 1. On vérifie qu'il y a bien un dessin en mémoire
        if hasattr(self, 'dernier_dessin') and self.dernier_dessin is not None:

            # 2. On prépare la vraie réponse au format attendu par Keras (un tableau)
            vraie_etiquette = np.array([vrai_chiffre])

            # 3. LA COMMANDE MAGIQUE : On entraîne l'IA sur ce cas précis !
            # Elle va ajuster ses poids immédiatement pour ce dessin
            modele.train_on_batch(self.dernier_dessin, vraie_etiquette)

            # On grave immédiatement les nouveaux poids dans le fichier !
            modele.save('mon_modele_ia.keras')

            print(f"Correction enregistrée ! L'IA a appris que ce dessin est un {vrai_chiffre}.")

            # 4. On ré-exécute la prédiction pour voir si elle a compris
            prediction = modele.predict(self.dernier_dessin)
            print("Nouvelle prédiction de l'IA après correction :", prediction.argmax())
        else:
            print("Dessine d'abord et clique sur Deviner avant de corriger !")




# --- Code pour lancer la fenêtre ---
if __name__ == "__main__":
    racine = tk.Tk()
    app = AppDessin(racine)
    racine.mainloop()



