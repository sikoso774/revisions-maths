"""Objets propres aux probabilités : dés, boules, urnes, diagramme de l'univers."""
from common import *

PIPS = {
    1: [(0, 0)],
    2: [(-1, 1), (1, -1)],
    3: [(-1, 1), (0, 0), (1, -1)],
    4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
    5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
    6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)],
}


def face_de(n, cote=0.8, couleur=BLANC):
    """Face de dé : carré arrondi (index 0) et ses points."""
    carre = RoundedRectangle(
        width=cote, height=cote, corner_radius=cote * 0.18,
        stroke_color=couleur, stroke_width=3, fill_color=FOND, fill_opacity=1,
    )
    pas = cote * 0.25
    points = [Dot(np.array([x * pas, y * pas, 0]), radius=cote * 0.075, color=couleur) for x, y in PIPS[n]]
    face = VGroup(carre, *points)
    face.set_z_index(2)
    return face


def style_de(face, couleur=BLANC, teinte=0.0, opacite=1.0):
    """Animations qui recolorent une face de dé (contour, points, teinte du fond)."""
    fond = interpolate_color(ManimColor(FOND), ManimColor(couleur), teinte)
    return [
        face[0].animate.set_stroke(couleur, opacity=opacite).set_fill(fond, opacity=1),
        *[p.animate.set_fill(couleur, opacity=opacite) for p in face[1:]],
    ]


def univers(largeur, hauteur, centre=ORIGIN):
    """Rectangle de l'univers Ω, avec son étiquette en haut à gauche."""
    cadre = Rectangle(width=largeur, height=hauteur, stroke_color=GRIS, stroke_width=3).move_to(centre)
    lettre = Tex(r"$\Omega$", font_size=40, color=GRIS).move_to(cadre.get_corner(UL) + DR * 0.4)
    return VGroup(cadre, lettre)


# Diagramme du dé : A = pair (vert), B = plus de 4 (bleu), le 6 est dans l'intersection
Y0 = 0.5  # hauteur du centre de l'univers
CERCLE_A = (np.array([-1.0, Y0, 0]), 1.75)
CERCLE_B = (np.array([1.15, Y0, 0]), 1.35)
PLACES = {
    1: np.array([-3.9, Y0 + 1.1, 0]),
    2: np.array([-1.7, Y0 + 0.7, 0]),
    3: np.array([3.7, Y0 - 1.0, 0]),
    4: np.array([-1.7, Y0 - 0.7, 0]),
    5: np.array([1.75, Y0, 0]),
    6: np.array([0.28, Y0, 0]),
}


def cercle_evenement(cercle, lettre, couleur, angle, ecart=0.45):
    """Cercle d'un événement et sa lettre, posée à l'extérieur du trait (angle en degrés, `ecart` du trait)."""
    centre, rayon = cercle
    rond = Circle(radius=rayon, color=couleur, stroke_width=5).move_to(centre)
    direction = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0])
    nom = Text(lettre, font_size=34, weight=BOLD, color=couleur).move_to(centre + (rayon + ecart) * direction)
    return rond, nom


def disque(contenu, couleur=BLANC, rayon=0.3, taille=20):
    """Disque numéroté ou lettré (un cheval, une boule…) : cercle (index 0) et son texte."""
    cercle = Circle(radius=rayon, stroke_color=couleur, stroke_width=3, fill_color=FOND, fill_opacity=1)
    nombre = Text(str(contenu), font_size=taille, weight=BOLD, color=couleur)
    return VGroup(cercle, nombre)


def urne(composition, centre, colonnes=6, pas=0.62, rayon=0.26, graine=3):
    """Urne ouverte et ses boules (couleurs mélangées, ordre fixé par `graine`) : renvoie (cadre, boules)."""
    n = len(composition)
    lignes = -(-n // colonnes)
    largeur = colonnes * pas + 0.4
    hauteur = lignes * pas + 0.4
    cx, cy = centre
    cadre = VMobject(stroke_color=GRIS, stroke_width=5)
    cadre.set_points_as_corners([
        [cx - largeur / 2, cy + hauteur / 2, 0], [cx - largeur / 2, cy - hauteur / 2, 0],
        [cx + largeur / 2, cy - hauteur / 2, 0], [cx + largeur / 2, cy + hauteur / 2, 0],
    ])
    ordre = np.random.RandomState(graine).permutation(n)
    boules = []
    for place, indice in enumerate(ordre):
        ligne, colonne = divmod(place, colonnes)
        x = cx + (colonne - (colonnes - 1) / 2) * pas
        y = cy + ((lignes - 1) / 2 - ligne) * pas
        couleur = composition[indice]
        boule = Circle(radius=rayon, stroke_color=interpolate_color(ManimColor(couleur), ManimColor(BLANC), 0.4),
                       stroke_width=2, fill_color=couleur, fill_opacity=1).move_to([x, y, 0])
        boule.couleur_base = couleur
        boules.append(boule)
    return cadre, boules


POLICE = "Consolas"


def bloc_code(lignes, titre, cles=None, taille=22, interligne=0.2):
    """Cadre de code : `lignes` = liste de (niveau d'indentation, texte) ; `cles` = mots colorés."""
    entete = Text(titre, font=POLICE, font_size=taille - 2, color=GRIS)
    textes = VGroup(*[Text(contenu, font=POLICE, font_size=taille, t2c=cles or {}) for _, contenu in lignes])
    textes.arrange(DOWN, aligned_edge=LEFT, buff=interligne)
    for (niveau, _), ligne in zip(lignes, textes):
        ligne.shift(RIGHT * 0.4 * niveau)
    corps = VGroup(entete, textes).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    cadre = SurroundingRectangle(corps, color=GRIS, buff=0.25, corner_radius=0.1, stroke_width=2)
    return VGroup(cadre, corps)
