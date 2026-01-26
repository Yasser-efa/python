"""
Génère les icônes PNG à partir du SVG
Nécessite: pip install cairosvg pillow
"""

import os

# Méthode simple sans dépendances externes
def create_simple_icons():
    """Crée des icônes PNG simples avec PIL"""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("PIL non disponible, création d'icônes basiques...")
        return

    sizes = [16, 48, 128]
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for size in sizes:
        # Créer une image avec fond gradient simulé
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Cercle de fond (cyan/bleu)
        padding = size // 16
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill=(79, 172, 254, 255)
        )

        # Cercle intérieur (horloge)
        inner_padding = size // 4
        draw.ellipse(
            [inner_padding, inner_padding, size - inner_padding, size - inner_padding],
            outline=(255, 255, 255, 255),
            width=max(1, size // 16)
        )

        # Centre de l'horloge
        center = size // 2
        dot_size = max(2, size // 16)
        draw.ellipse(
            [center - dot_size, center - dot_size, center + dot_size, center + dot_size],
            fill=(255, 255, 255, 255)
        )

        # Aiguilles
        line_width = max(1, size // 20)
        # Aiguille des heures (vers le haut)
        draw.line(
            [(center, center), (center, center - size // 4)],
            fill=(255, 255, 255, 255),
            width=line_width
        )
        # Aiguille des minutes (vers la droite et haut)
        draw.line(
            [(center, center), (center + size // 5, center - size // 8)],
            fill=(255, 255, 255, 255),
            width=line_width
        )

        # Sauvegarder
        output_path = os.path.join(script_dir, f'icon-{size}.png')
        img.save(output_path, 'PNG')
        print(f"Créé: {output_path}")


def create_icons_with_cairosvg():
    """Crée des icônes à partir du SVG avec cairosvg"""
    try:
        import cairosvg
    except ImportError:
        print("cairosvg non disponible, utilisation de la méthode simple...")
        create_simple_icons()
        return

    sizes = [16, 48, 128]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, 'icon.svg')

    for size in sizes:
        output_path = os.path.join(script_dir, f'icon-{size}.png')
        cairosvg.svg2png(
            url=svg_path,
            write_to=output_path,
            output_width=size,
            output_height=size
        )
        print(f"Créé: {output_path}")


if __name__ == '__main__':
    try:
        create_icons_with_cairosvg()
    except Exception as e:
        print(f"Erreur avec cairosvg: {e}")
        create_simple_icons()

    print("\nIcônes générées avec succès!")
