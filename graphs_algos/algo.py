"""Outils pour animer des algorithmes : pseudo-code surligné, file/pile animées, graphe de parcours."""
from common import *

POLICE = "Consolas"
CLES_CODE = {
    "tant que": VIOLET,
    "répéter": VIOLET,
    "pour chaque": VIOLET,
    "sinon": VIOLET,
    "si ": VIOLET,
    "marquer": ACCENT,
    "enfiler": SOMMET,
    "défiler": SOMMET,
    "empiler": SOMMET,
    "dépiler": SOMMET,
    "cycle détecté": ROUGE,
    "cycle négatif": ROUGE,
}

# Graphe commun aux parcours BFS / DFS (une arête de plus qu'un arbre : E–F ferme un cycle)
SOMMETS_P = ["A", "B", "C", "D", "E", "F"]
ARETES_P = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("E", "F")]
VOISINS_P = {
    v: sorted(a if b == v else b for a, b in ARETES_P if v in (a, b)) for v in SOMMETS_P
}
POSITION_P = {
    "A": LEFT * 3.6 + UP * 1.7,
    "B": LEFT * 5.3 + UP * 0.4,
    "C": LEFT * 1.9 + UP * 0.4,
    "D": LEFT * 6.1 + DOWN * 1.1,
    "E": LEFT * 4.5 + DOWN * 1.1,
    "F": LEFT * 2.3 + DOWN * 1.1,
}


class PanneauCode:
    """Pseudo-code numéroté, avec un surligneur qui descend de ligne en ligne."""

    def __init__(self, titre, lignes, coin, largeur_max=6.4, taille=19, interligne=0.36):
        x0, y0 = coin
        titre_txt = Text(titre, font=POLICE, font_size=taille + 2, weight=BOLD, color=TEXTE)
        titre_txt.move_to([x0, y0, 0], aligned_edge=LEFT)
        self.numeros, self.textes = [], []
        for i, (niveau, contenu) in enumerate(lignes):
            y = y0 - (i + 1) * interligne - 0.08
            numero = Text(str(i + 1), font=POLICE, font_size=taille - 3, color=ARETE)
            numero.move_to([x0 + 0.12, y, 0])
            texte_code = Text(contenu, font=POLICE, font_size=taille, t2c=CLES_CODE)
            texte_code.move_to([x0 + 0.45 + niveau * 0.38, y, 0], aligned_edge=LEFT)
            self.numeros.append(numero)
            self.textes.append(texte_code)
        self.contenu = VGroup(titre_txt, *self.numeros, *self.textes)
        if self.contenu.width > largeur_max:
            self.contenu.scale_to_fit_width(largeur_max)
            self.contenu.align_to([x0, y0 + 0.15, 0], UL)
        self.cadre = SurroundingRectangle(
            self.contenu, color=ARETE, buff=0.18, corner_radius=0.1, stroke_width=2
        )
        self.ys = [n.get_center()[1] for n in self.numeros]
        self.surligneur = Rectangle(
            width=self.cadre.width - 0.12,
            height=interligne * 0.92,
            fill_color=ACCENT,
            fill_opacity=0.28,
            stroke_width=0,
        ).move_to([self.cadre.get_center()[0], self.ys[0], 0])
        self.surligneur.set_z_index(-1)
        self.courante = 0

    def montrer(self):
        return [FadeIn(self.contenu, shift=LEFT * 0.3), Create(self.cadre), FadeIn(self.surligneur)]

    def aller_a(self, i):
        """Animation : le surligneur se place sur la ligne i (numérotée à partir de 0)."""
        self.courante = i
        return self.surligneur.animate.set_y(self.ys[i])

    def cacher(self):
        return [FadeOut(self.contenu), FadeOut(self.cadre), FadeOut(self.surligneur)]


class Conteneur:
    """File (horizontale) ou pile (verticale) dont les cases entrent et sortent à l'écran."""

    def __init__(self, nom, origine, vertical=False, taille=(0.62, 0.5), capacite=6, couleur_nom=TEXTE):
        self.vertical = vertical
        self.largeur, self.hauteur = taille
        self.origine = np.array([origine[0], origine[1], 0], dtype=float)
        self.items = []  # liste de (nom, case)
        pas = (self.hauteur if vertical else self.largeur) + 0.08
        self.pas = pas
        self.etiquette = Text(nom, font_size=22, weight=BOLD, color=couleur_nom)
        if vertical:
            haut = self.origine + UP * (pas * (capacite - 1) + self.hauteur / 2 + 0.05)
            bas = self.origine + DOWN * (self.hauteur / 2 + 0.05)
            gauche, droite = LEFT * (self.largeur / 2 + 0.06), RIGHT * (self.largeur / 2 + 0.06)
            self.cadre = VGroup(
                Line(bas + gauche, haut + gauche, color=ARETE, stroke_width=3),
                Line(bas + droite, haut + droite, color=ARETE, stroke_width=3),
                Line(bas + gauche, bas + droite, color=ARETE, stroke_width=3),
            )
            self.etiquette.next_to(self.cadre, UP, buff=0.12)
        else:
            gauche = self.origine + LEFT * (self.largeur / 2 + 0.05)
            droite = self.origine + RIGHT * (pas * (capacite - 1) + self.largeur / 2 + 0.05)
            haut, bas = UP * (self.hauteur / 2 + 0.06), DOWN * (self.hauteur / 2 + 0.06)
            self.cadre = VGroup(
                Line(gauche + haut, droite + haut, color=ARETE, stroke_width=3),
                Line(gauche + bas, droite + bas, color=ARETE, stroke_width=3),
            )
            self.etiquette.next_to(self.cadre, LEFT, buff=0.25)

    def emplacement(self, k):
        direction = UP if self.vertical else RIGHT
        return self.origine + direction * self.pas * k

    def creer_case(self, nom, couleur):
        rectangle = Rectangle(
            width=self.largeur,
            height=self.hauteur,
            stroke_color=couleur,
            stroke_width=3,
            fill_color=FOND,
            fill_opacity=1,
        )
        contenu = Text(nom, font_size=22 if self.vertical else 24, weight=BOLD, color=couleur)
        if contenu.width > self.largeur - 0.1:
            contenu.scale_to_fit_width(self.largeur - 0.1)
        return VGroup(rectangle, contenu)

    def montrer(self):
        return [FadeIn(self.etiquette), Create(self.cadre)]

    def noms(self):
        return [n for n, _ in self.items]

    def ajouter(self, nom, couleur=ACCENT):
        """Empile / enfile ; renvoie la liste d'animations."""
        case = self.creer_case(nom, couleur).move_to(self.emplacement(len(self.items)))
        self.items.append((nom, case))
        return [FadeIn(case, shift=(DOWN if self.vertical else LEFT) * 0.5)]

    def retirer(self, fin=False):
        """Retire le premier (file) ou le dernier (pile) élément ; renvoie les animations."""
        indice = len(self.items) - 1 if fin else 0
        nom, case = self.items.pop(indice)
        animations = [FadeOut(case, shift=(UP if self.vertical else LEFT) * 0.6)]
        if not fin:
            for k, (_, autre) in enumerate(self.items):
                animations.append(autre.animate.move_to(self.emplacement(k)))
        return animations


# Graphe pondéré commun à Kruskal et Prim (poids tous distincts : l'arbre couvrant minimal est unique)
SOMMETS_M = list("ABCDEF")
ARETES_M = [
    ("A", "B", 4), ("A", "C", 5), ("A", "F", 9), ("B", "C", 6), ("B", "D", 10),
    ("C", "D", 7), ("C", "F", 2), ("D", "E", 3), ("E", "F", 8),
]
POS_M = {
    "A": LEFT * 6.0 + UP * 0.2,
    "B": LEFT * 4.8 + UP * 1.8,
    "C": LEFT * 3.9 + UP * 0.3,
    "D": LEFT * 2.6 + UP * 1.8,
    "E": LEFT * 1.4 + UP * 0.2,
    "F": LEFT * 3.0 + DOWN * 1.5,
}


def boite_arete(u, v, w, couleur=ARETE, cote=0.64):
    """Petite case « arête + poids » (liste triée de Kruskal, arêtes candidates de Prim)."""
    cadre = Rectangle(width=cote, height=cote, stroke_color=couleur, stroke_width=3, fill_color=FOND, fill_opacity=1)
    nom = Text(f"{u}{v}", font_size=19, weight=BOLD, color=TEXTE).move_to(cadre.get_center() + UP * 0.12)
    poids = Text(str(w), font_size=18, weight=BOLD, color=ACCENT).move_to(cadre.get_center() + DOWN * 0.16)
    return VGroup(cadre, nom, poids)
