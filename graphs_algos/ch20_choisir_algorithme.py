"""Chapitre 20 : quel algorithme choisir ? Tableaux comparatifs, ordres de grandeur et applications aux exercices des TD."""
import math
from algo import *

# Tableau A : parcours et plus courts chemins ; tableau B : arbres couvrants, classement, délais maximaux
COLONNES = [("Algorithme", 2.7), ("Problème résolu", 4.4), ("Conditions", 3.4), ("Coût", 2.5)]
LIGNES_A = [
    ("BFS", "parcourir, atteindre,\nplus court chemin (en arêtes)", "aucune", r"$O(n+m)$", VERT),
    ("DFS", "parcourir, détecter un circuit,\nordre topologique", "aucune", r"$O(n+m)$", VERT),
    ("Dijkstra", "plus courts chemins\ndepuis une source", "poids positifs ou nuls", r"$O((n+m)\log n)$", ACCENT),
    ("Bellman-Ford", "plus courts chemins\ndepuis une source", "poids négatifs permis,\nsans circuit négatif", r"$O(n\cdot m)$", ROUGE),
    ("Relaxation en ordre\ntopologique", "plus court ou plus long chemin", "graphe sans circuit", r"$O(n+m)$", VERT),
]
LIGNES_B = [
    ("Kruskal", "arbre couvrant minimal\n(tri des arêtes)", "graphe non orienté\nconnexe", r"$O(m\log m)$", ACCENT),
    ("Prim", "arbre couvrant minimal\n(arêtes de la coupe)", "graphe non orienté\nconnexe", r"$O(m\log n)$", ACCENT),
    ("PageRank", "classer les sommets\nd'un graphe orienté", "itérer jusqu'à\nconvergence", r"$O(m)$ par itération", VERT),
    ("Bellman-Ford\navec un maximum", "plus long chemin,\ndélais maximaux", "aucun circuit de\nlongueur positive", r"$O(n\cdot m)$", ROUGE),
]
PHRASES_A = [
    ("BFS : le plus court chemin en nombre d'arêtes, quand les arêtes n'ont pas de poids", ["BFS"]),
    ("DFS : il explore en profondeur, d'où la détection de circuit et l'ordre topologique", ["DFS"]),
    ("Dijkstra : le bon choix tant qu'aucun poids n'est négatif", ["Dijkstra"]),
    ("Bellman-Ford : plus général, mais plus lent : jusqu'à n passages sur toutes les arêtes", ["Bellman-Ford"]),
    ("Sans circuit, un seul passage dans l'ordre topologique suffit, même avec des poids négatifs", ["Sans circuit"]),
]
PHRASES_B = [
    ("Kruskal trie les arêtes : le coût est celui du tri", ["Kruskal"]),
    ("Prim fait grandir un arbre avec un tas : à peu près le même coût que Kruskal", ["Prim"]),
    ("PageRank : chaque itération parcourt tous les liens une fois", ["PageRank"]),
    ("Bellman-Ford avec un maximum : le seul cas pour les délais maximaux, avec arcs négatifs et circuits", ["Bellman-Ford avec un maximum"]),
]

# Ordres de grandeur pour n = 1 000 sommets et m = 5 000 arêtes (log de base 2, constantes ignorées)
N, M = 1000, 5000
BARRES = [
    ("BFS, DFS", N + M, r"$\approx 6\,000$", VERT),
    ("Prim", M * math.log2(N), r"$\approx 50\,000$", ACCENT),
    ("Dijkstra", (N + M) * math.log2(N), r"$\approx 60\,000$", ACCENT),
    ("Kruskal", M * math.log2(M), r"$\approx 61\,000$", ACCENT),
    ("Bellman-Ford", N * M, r"$\approx 5\,000\,000$", ROUGE),
]

# Quel algorithme pour chaque exercice des feuilles de TD ?
EXERCICES = [
    ("TD1 · 3 : sommets atteignables", "BFS ou DFS", VERT),
    ("TD1 · 4 : arbre de coût minimum", "Kruskal ou Prim", ACCENT),
    ("TD1 · 5, TD2 · 1 et 4 : poids positifs", "Dijkstra", SOMMET),
    ("TD2 · 2 et 3 : poids négatifs", "Bellman-Ford", VIOLET),
    ("TD2 · 5 : Guérande (sans circuit)", "Dijkstra (poids positifs)", SOMMET),
    ("TD2 · 6 : Rémi, cohérence puis trajets", "DFS, puis Dijkstra", VERT),
    ("TD2 · 7.1 et 7.2 : durée d'un projet", "Relaxation topologique", ROUGE),
    ("TD2 · 7.3 et 7.4 : avec délais maximaux", "Bellman-Ford avec un maximum", VIOLET),
]


def cellule(contenu, largeur, hauteur, couleur=TEXTE, taille=20, gras=False):
    """Contenu d'une case de tableau (Tex si la chaîne commence par $), réduit pour tenir dans la case."""
    if contenu.startswith("$") or "$" in contenu:
        objet = Tex(contenu, font_size=taille + 8, color=couleur)
    else:
        objet = Text(contenu, font_size=taille, color=couleur, weight=BOLD if gras else NORMAL, line_spacing=0.8)
    if objet.width > largeur - 0.2:
        objet.scale_to_fit_width(largeur - 0.2)
    if objet.height > hauteur - 0.12:
        objet.scale_to_fit_height(hauteur - 0.12)
    return objet


def ligne_tableau(valeurs, couleurs, y, hauteur, x0=-6.5):
    """Une ligne du tableau : cadres, textes ; renvoie un VGroup."""
    elements = VGroup()
    x = x0
    for (titre, largeur), valeur, couleur in zip(COLONNES, valeurs, couleurs):
        cadre = Rectangle(width=largeur, height=hauteur, stroke_color=ARETE, stroke_width=2)
        cadre.move_to([x + largeur / 2, y, 0])
        contenu = cellule(valeur, largeur, hauteur, couleur, gras=(couleur != TEXTE and not valeur.startswith("$")))
        contenu.move_to(cadre.get_center())
        elements.add(cadre, contenu)
        x += largeur
    return elements


class ChoisirAlgorithme(SceneGraphes):
    # ---------- théorie ----------
    def theorie(self):
        carte = self.carte(
            "Mesurer le coût d'un algorithme",
            SOMMET,
            [
                tex(r"$n$ sommets \qquad $m$ arêtes", 46, {"sommets": SOMMET, "arêtes": ACCENT}),
                tex(r"$n-1\leq m\leq\dfrac{n(n-1)}{2}$", 46),
            ],
            [
                texte("Le coût est un ordre de grandeur en fonction de n et de m, constantes ignorées", 26, ["ordre de grandeur"]),
                texte("Graphe creux : m proche de n. Graphe dense : m proche de n²", 26, ["creux", "dense"]),
            ],
        )
        self.play(FadeOut(carte))
        return self.carte(
            "Quatre questions pour choisir",
            VERT,
            [
                tex(r"\textbf{1.} Que cherche-t-on ? chemins, arbre, classement, circuit", 34, {r"\textbf{1.}": VERT}),
                tex(r"\textbf{2.} Les arcs ont-ils un poids ? de quel signe ?", 34, {r"\textbf{2.}": VERT}),
                tex(r"\textbf{3.} Le graphe a-t-il des circuits ?", 34, {r"\textbf{3.}": VERT}),
                tex(r"\textbf{4.} Est-il creux ou dense ?", 34, {r"\textbf{4.}": VERT}),
            ],
            [texte("Ces quatre réponses suffisent presque toujours à désigner l'algorithme", 26, ["quatre réponses"])],
        )

    # ---------- les deux tableaux ----------
    def tableau(self, lignes, phrases, legende, premiere_fois):
        hauteur_entete, hauteur_ligne, y_haut = 0.55, 0.8, 2.45
        entete = VGroup()
        x = -6.5
        for titre, largeur in COLONNES:
            cadre = Rectangle(width=largeur, height=hauteur_entete, stroke_color=ACCENT, stroke_width=2)
            cadre.move_to([x + largeur / 2, y_haut - hauteur_entete / 2, 0])
            t = Text(titre, font_size=22, weight=BOLD, color=ACCENT).move_to(cadre.get_center())
            entete.add(cadre, t)
            x += largeur
        if premiere_fois:
            self.dezoom(self.carte_courante, FadeIn(entete), FadeIn(legende))
        else:
            self.play(FadeIn(entete), FadeIn(legende))
        groupes = []
        for k, (nom, probleme, condition, cout, couleur) in enumerate(lignes):
            y = y_haut - hauteur_entete - hauteur_ligne * (k + 0.5)
            groupe = ligne_tableau([nom, probleme, condition, cout], [couleur, TEXTE, TEXTE, couleur], y, hauteur_ligne)
            groupes.append(groupe)
            phrase, cles = phrases[k]
            legende = self.changer(legende, self.legende(phrase, cles))
            self.play(FadeIn(groupe, shift=UP * 0.15))
            self.wait(4.0)
        return VGroup(entete, *groupes), legende

    # ---------- ordres de grandeur ----------
    def ordres_de_grandeur(self, legende):
        legende = self.changer(legende, self.legende("Ordres de grandeur sur un graphe de 1 000 sommets et 5 000 arêtes", ["1 000 sommets", "5 000 arêtes"]))
        x_barres = -3.0
        elements = VGroup()
        barres = []
        for k, (nom, valeur, etiquette, couleur) in enumerate(BARRES):
            y = 2.0 - 0.7 * k
            longueur = (math.log10(valeur) - 3) * 1.6 + 0.6
            barre = Rectangle(width=longueur, height=0.5, stroke_width=0, fill_color=couleur, fill_opacity=0.85)
            barre.move_to([x_barres + longueur / 2, y, 0])
            nom_t = Text(nom, font_size=24, weight=BOLD, color=couleur).move_to([x_barres - 0.2, y, 0], aligned_edge=RIGHT)
            valeur_t = Tex(etiquette, font_size=34, color=couleur).next_to(barre, RIGHT, buff=0.2)
            elements.add(nom_t)
            barres.append((barre, valeur_t))
        echelle = Text("échelle logarithmique : la longueur d'une barre est proportionnelle au logarithme du coût", font_size=20, color=ARETE).move_to([0.5, -1.55, 0])
        self.play(FadeIn(elements), FadeIn(echelle))
        for barre, valeur_t in barres:
            self.play(GrowFromEdge(barre, LEFT), FadeIn(valeur_t), run_time=1.0)
            self.wait(0.8)
        self.wait(2.0)
        detail = self.detail(None, tex(r"$n\cdot m=5\,000\,000\quad\text{contre}\quad(n+m)\log n\approx 60\,000$", 40, {r"5\,000\,000": ROUGE}))
        legende = self.changer(legende, self.legende("Bellman-Ford coûte ici environ 80 fois plus que Dijkstra : on ne l'utilise que si on en a besoin", ["80 fois plus"]))
        self.wait(6.0)
        return VGroup(elements, echelle, *[b for pair in barres for b in pair]), legende, detail

    # ---------- application aux exercices ----------
    def exercices(self, titre, legende):
        legende = self.changer(legende, self.legende("Quel algorithme pour chaque exercice des feuilles de TD ?", ["chaque exercice"]))
        reponses = []
        for k, (exercice, algorithme, couleur) in enumerate(EXERCICES):
            y = 2.25 - 0.6 * k
            question = Text(exercice, font_size=23, color=TEXTE)
            question.move_to([-6.6, y, 0], aligned_edge=LEFT)
            if question.width > 6.9:
                question.scale_to_fit_width(6.9)
                question.move_to([-6.6, y, 0], aligned_edge=LEFT)
            fleche = Arrow([0.5, y, 0], [1.0, y, 0], buff=0, stroke_width=3, color=ARETE, max_tip_length_to_length_ratio=0.5)
            reponse = Text(algorithme, font_size=24, weight=BOLD, color=couleur)
            if reponse.width > 5.6:
                reponse.scale_to_fit_width(5.6)
            reponse.move_to([1.3, y, 0], aligned_edge=LEFT)
            self.play(FadeIn(question, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(1.6)
            self.play(GrowArrow(fleche), FadeIn(reponse, shift=RIGHT * 0.2), run_time=0.9)
            reponses.append(reponse)
            self.wait(1.3)
        legende = self.changer(legende, self.legende("Les poids, leur signe et la présence de circuits décident presque tout ; la taille départage ensuite", ["décident presque tout"]))
        self.wait(6.0)
        return legende

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Quel algorithme choisir ?", 20)
        self.carte_courante = self.theorie()

        legende = self.legende("Parcours et plus courts chemins : cinq algorithmes à distinguer", ["cinq algorithmes"])
        _, legende = self.tableau(LIGNES_A, PHRASES_A, legende, premiere_fois=True)
        self.wait(3.0)
        self.vider(titre)

        legende = self.legende("Arbres couvrants, classement et délais maximaux", ["délais maximaux"])
        _, legende = self.tableau(LIGNES_B, PHRASES_B, legende, premiere_fois=False)
        self.wait(3.0)
        self.vider(titre)

        legende = self.legende("Et en pratique ? Un ordre de grandeur vaut mieux qu'une formule", ["ordre de grandeur"])
        self.play(FadeIn(legende))
        _, legende, _ = self.ordres_de_grandeur(legende)
        self.vider(titre)

        legende = self.legende("Mettons cela en pratique", ["pratique"])
        self.play(FadeIn(legende))
        self.exercices(titre, legende)
        self.fin()
