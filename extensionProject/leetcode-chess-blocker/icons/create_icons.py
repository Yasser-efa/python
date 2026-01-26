"""
Script pour créer les icônes PNG de l'extension.
Utilise PIL (Pillow) pour dessiner les icônes.

Usage: python create_icons.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    """Crée une icône PNG de la taille spécifiée."""
    # Créer une image avec fond transparent
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Couleurs
    orange_start = (249, 115, 22)  # #f97316
    orange_end = (234, 88, 12)     # #ea580c

    # Dessiner un cercle orange (approximation du gradient)
    center = size // 2
    radius = size // 2 - 2

    # Cercle principal
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=orange_start
    )

    # Symbole du cavalier d'échecs (texte)
    try:
        font_size = int(size * 0.5)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Dessiner le symbole ♞
    chess_symbol = "♞"
    # Calculer la position pour centrer
    bbox = draw.textbbox((0, 0), chess_symbol, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - int(size * 0.05)

    draw.text((x, y), chess_symbol, fill=(255, 255, 255), font=font)

    return img


def main():
    """Génère les icônes 16x16, 48x48 et 128x128."""
    sizes = [16, 48, 128]
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for size in sizes:
        icon = create_icon(size)
        filename = os.path.join(script_dir, f"icon-{size}.png")
        icon.save(filename, "PNG")
        print(f"Créé: {filename}")

    print("\nIcônes créées avec succès!")


if __name__ == "__main__":
    main()
