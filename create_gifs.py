"""
Script pour générer un GIF de démonstration de l'interface IA
Crée des images PNG et les convertit en GIF animé
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Créer le dossier pour les gifs
os.makedirs('gifs', exist_ok=True)

frames = []

# ===== FRAME 1: Écran vide =====
img = Image.new('RGB', (400, 500), color='white')
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 350, 350], outline='black', width=2)
draw.text((100, 380), "Cliquez pour dessiner...", fill='black')
frames.append(img.copy())

# ===== FRAME 2-4: Animation de dessin d'un "3" =====
drawing_points = [
    (150, 30), (200, 40), (220, 50), (230, 70),
    (230, 90), (220, 110), (180, 120), (150, 120),
    (140, 140), (160, 140), (200, 140), (220, 150),
    (230, 170), (230, 190), (220, 210), (180, 220),
    (150, 220), (140, 210), (150, 200), (200, 190),
    (230, 200), (240, 220), (230, 240), (200, 250),
    (150, 250), (120, 240)
]

# Animer le dessin progressivement
for idx in range(0, len(drawing_points), 3):
    canvas_img = Image.new('RGB', (400, 500), color='white')
    canvas_draw = ImageDraw.Draw(canvas_img)
    
    # Dessiner la bordure
    canvas_draw.rectangle([50, 50, 350, 350], outline='black', width=2)
    
    # Dessiner les points du dessin
    for point in drawing_points[:idx+1]:
        r = 8
        canvas_draw.ellipse([point[0]-r+50, point[1]-r+50, point[0]+r+50, point[1]+r+50], fill='black')
    
    canvas_draw.text((80, 380), "Dessinez un chiffre (0-9)", fill='black')
    frames.append(canvas_img.copy())

# ===== FRAME 5: Bouton Deviner =====
canvas_img = Image.new('RGB', (400, 500), color='white')
canvas_draw = ImageDraw.Draw(canvas_img)
canvas_draw.rectangle([50, 50, 350, 350], outline='black', width=2)

# Redessiner le "3"
for point in drawing_points:
    r = 8
    canvas_draw.ellipse([point[0]-r+50, point[1]-r+50, point[0]+r+50, point[1]+r+50], fill='black')

# Bouton Deviner
canvas_draw.rectangle([100, 380, 200, 420], fill='lightblue', outline='black', width=2)
canvas_draw.text((120, 392), "Deviner", fill='black')
frames.append(canvas_img.copy())

# ===== FRAME 6: Résultat - Prédiction de l'IA =====
result_img = Image.new('RGB', (400, 500), color='white')
result_draw = ImageDraw.Draw(result_img)
result_draw.rectangle([50, 50, 350, 350], outline='black', width=2)

for point in drawing_points:
    r = 8
    result_draw.ellipse([point[0]-r+50, point[1]-r+50, point[0]+r+50, point[1]+r+50], fill='black')

result_draw.rectangle([100, 380, 200, 420], fill='lightgreen', outline='black', width=2)
result_draw.text((115, 392), "Prédiction", fill='black')
result_draw.text((120, 450), "L'IA pense: 3", fill='green')
frames.append(result_img.copy())

# ===== FRAME 7: Correction - Si erreur =====
correction_img = Image.new('RGB', (400, 500), color='white')
correction_draw = ImageDraw.Draw(correction_img)
correction_draw.text((60, 200), "Si l'IA se trompe,", fill='black')
correction_draw.text((70, 230), "clique sur le bon chiffre :", fill='black')

# Afficher les boutons 0-9
for i in range(10):
    x = 50 + (i % 5) * 70
    y = 300 + (i // 5) * 50
    correction_draw.rectangle([x, y, x+60, y+40], fill='lightyellow', outline='black', width=1)
    correction_draw.text((x+20, y+10), str(i), fill='black')

frames.append(correction_img.copy())

# ===== FRAME 8: IA apprend =====
learning_img = Image.new('RGB', (400, 500), color='white')
learning_draw = ImageDraw.Draw(learning_img)
learning_draw.text((60, 200), "Correction enregistree!", fill='green')
learning_draw.text((100, 250), "L'IA a appris", fill='black')
learning_draw.text((50, 280), "Nouvelle prediction: 3", fill='green')
frames.append(learning_img.copy())

# Sauvegarder en GIF
output_path = 'gifs/digit-recognition-demo.gif'
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=800,  # 800ms par frame
    loop=0  # Boucle infini
)

print(f"✓ GIF créé: {output_path}")
print(f"  Dimensions: {frames[0].size}")
print(f"  Nombre de frames: {len(frames)}")
