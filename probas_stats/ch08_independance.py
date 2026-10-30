"""Chapitre 8 : indépendance de deux événements (deux dés, indépendants ≠ incompatibles, P(A|B) ≠ P(B|A))."""
from common import *
from proba import *

# Grille des 36 résultats : lignes = dé rouge (1 à 6), colonnes = dé noir (1 à 6)
CENTRE_GRILLE = np.array([-3.2, 0.2, 0])
PAS = 0.62
COTE = 0.56

# Barre du chapitre 7 (0,6 | 0,2 | 0,2) pour le rappel P(A|B) et P(B|A)
LARGEURS = [6.0, 2.0, 2.0]
X_GAUCHE = -5.0
Y_BARRE = 0.3
HAUTEUR_BARRE = 1.4


def teinte(couleur, force=0.55):
    return interpolate_color(ManimColor(FOND), ManimColor(couleur), force)


def centre_case(ligne, colonne):
    return CENTRE_GRILLE + np.array([(colonne - 2.5) * PAS, (2.5 - ligne) * PAS, 0])


class Chapitre08(SceneProbas):
    def construct(self):
        titre = self.intro("Indépendance", 8)

        # ── Théorie ─────────────────────────────────────────────────────────
        carte = self.carte(
            "Deux événements indépendants",
            ACCENT,
            [
                tex(r"$P(A\mid B)=P(A)$", 46),
                tex(r"$\Longleftrightarrow\;P(A\cap B)=P(A)\,P(B)$", 46, {r"P(A)\,P(B)": ACCENT}),
                tex(r"$A\mathrel{\perp\!\!\!\perp}B$", 46),
            ],
            [
                texte("Savoir que B est réalisé ne change rien à la probabilité de A", 26, ["ne change rien"]),
                texte("Test pratique : la probabilité de « A et B » vaut le produit des deux", 26, ["le produit"]),
            ],
        )

        # ── Démonstration 1 : les deux dés ─────────────────────────────────────
        cases = {}
        for r in range(6):
            for c in range(6):
                cases[(r, c)] = Square(side_length=COTE, stroke_color=GRIS, stroke_width=2,
                                       fill_color=FOND, fill_opacity=1).move_to(centre_case(r, c))
        grille = VGroup(*cases.values())
        nombres_noir = VGroup(*[Text(str(c + 1), font_size=18, color=GRIS).move_to(centre_case(0, c) + UP * 0.5) for c in range(6)])
        nombres_rouge = VGroup(*[Text(str(r + 1), font_size=18, color=GRIS).move_to(centre_case(r, 0) + LEFT * 0.5) for r in range(6)])
        nom_noir = Text("dé noir", font_size=20, color=GRIS).move_to(centre_case(0, 5) + RIGHT * 0.95 + UP * 0.5)
        nom_rouge = Text("dé rouge", font_size=20, color=ROUGE).rotate(PI / 2).move_to(CENTRE_GRILLE + LEFT * 2.5)
        annotations = VGroup(nombres_noir, nombres_rouge, nom_noir, nom_rouge)

        def colorer(cles, couleur):
            return [cases[k].animate.set_fill(teinte(couleur), opacity=1).set_stroke(couleur, opacity=1) for k in cles]

        def remettre(cles):
            return [cases[k].animate.set_fill(FOND, opacity=1).set_stroke(GRIS, width=2, opacity=1) for k in cles]

        diagonale = [(i, i) for i in range(6)]
        ligne_b = [(0, c) for c in range(6)]

        legende = self.legende("Deux dés, un rouge et un noir : 36 résultats équiprobables", ["36 résultats"])
        self.dezoom(carte, FadeIn(grille), FadeIn(annotations), FadeIn(legende))
        detail = self.detail(None, tex(r"$|\Omega|=6\times 6=36$", 46))
        self.wait(3.0)

        compte = VGroup(
            texte("A : 6 cases", 28, {"A": VERT}),
            texte("B : 6 cases", 28, {"B": BLEU}),
            texte("A et B : 1 case", 28, {"A et B": ACCENT}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.8, 0.6, 0])

        legende = self.changer(legende, self.legende("A : « les deux dés donnent le même résultat », la diagonale", ["la diagonale"]))
        self.play(*colorer(diagonale, VERT))
        self.play(FadeIn(compte[0], shift=LEFT * 0.2))
        detail = self.detail(detail, tex(r"$P(A)=\dfrac{6}{36}=\dfrac{1}{6}$", 46, {"A": VERT}))
        self.wait(3.5)

        legende = self.changer(legende, self.legende("B : « le dé rouge donne 1 », la première ligne", ["la première ligne"]))
        self.play(*colorer(ligne_b, BLEU))
        self.play(*colorer([(0, 0)], ACCENT))
        self.play(FadeIn(compte[1], shift=LEFT * 0.2), FadeIn(compte[2], shift=LEFT * 0.2))
        detail = self.detail(detail, tex(r"$P(B)=\dfrac{6}{36}=\dfrac{1}{6}$", 46, {"B": BLEU}))
        self.wait(3.5)

        legende = self.changer(legende, self.legende("Sachant que le rouge donne 1, il reste 6 cases dont 1 seule dans A", ["1 seule dans A"]))
        autres = [k for k in cases if k[0] != 0]
        self.play(*[cases[k].animate.set_opacity(0.15) for k in autres], run_time=1.2)
        self.play(Indicate(cases[(0, 0)], color=ACCENT, scale_factor=1.3))
        detail = self.detail(detail, tex(r"$P(A\mid B)=\dfrac{1}{6}=P(A)$", 46, {r"P(A)": VERT}))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Le produit des probabilités redonne la probabilité de l'intersection", ["le produit"]))
        detail = self.detail(detail, tex(r"$P(A)\,P(B)=\dfrac{1}{6}\times\dfrac{1}{6}=\dfrac{1}{36}=P(A\cap B)$", 44, {r"\dfrac{1}{36}": ACCENT}))
        self.wait(4.0)
        legende = self.changer(legende, self.legende("A et B sont donc indépendants", ["indépendants"]))
        self.wait(3.0)

        # ── Démonstration 2 : indépendants ≠ incompatibles ──────────────────────
        self.play(*[cases[k].animate.set_opacity(1.0) for k in autres], run_time=0.6)
        self.play(*remettre(list(cases)), *[FadeOut(compte)], run_time=0.8)
        somme_sept = [(r, 5 - r) for r in range(6)]
        legende = self.changer(legende, self.legende("Autre événement C : « la somme des deux dés vaut 7 »", ["la somme des deux dés vaut 7"]))
        self.play(*colorer(diagonale, VERT))
        self.play(*colorer(somme_sept, VIOLET))
        detail = self.detail(detail, tex(r"$P(A)=\dfrac{1}{6}\qquad P(C)=\dfrac{6}{36}=\dfrac{1}{6}$", 44, {r"C": VIOLET}))
        self.wait(3.5)

        legende = self.changer(legende, self.legende("A et C n'ont aucune case en commun : ils sont incompatibles", ["incompatibles"]))
        detail = self.detail(detail, tex(r"$P(A\cap C)=0\;\neq\;P(A)\,P(C)=\dfrac{1}{36}$", 46, {r"\neq": ROUGE}))
        self.wait(4.5)

        legende = self.changer(legende, self.legende("Sachant C, A devient impossible : indépendants ne veut pas dire incompatibles", ["indépendants ne veut pas dire incompatibles"]))
        detail = self.detail(detail, tex(r"$P(A\mid C)=0\;\neq\;P(A)=\dfrac{1}{6}$", 46, {r"\neq": ROUGE}))
        self.play(*[cases[k].animate.set_opacity(0.15) for k in cases if k not in somme_sept], run_time=1.0)
        self.wait(5.0)

        # ── Démonstration 3 : P(A|B) n'est pas P(B|A) ─────────────────────────────
        self.vider(titre)
        bandes, x = [], X_GAUCHE
        for largeur in LARGEURS:
            bande = Rectangle(width=largeur, height=HAUTEUR_BARRE, stroke_color=GRIS, stroke_width=3,
                              fill_color=FOND, fill_opacity=1).move_to([x + largeur / 2, Y_BARRE, 0])
            x += largeur
            bandes.append(bande)
        etiquettes = [
            Tex(r"$0{,}6$", font_size=44).move_to(bandes[0].get_center()),
            Tex(r"$0{,}2$", font_size=44, color=ACCENT).move_to(bandes[1].get_center()),
            Tex(r"$0{,}2$", font_size=44).move_to(bandes[2].get_center()),
        ]
        for e in etiquettes:
            e.set_z_index(3)
        accolade_a = Brace(VGroup(bandes[0], bandes[1]), UP, color=VERT, buff=0.1)
        texte_a = Tex(r"$P(A)=0{,}8$", font_size=40, color=VERT).next_to(accolade_a, UP, buff=0.12)
        accolade_b = Brace(VGroup(bandes[1], bandes[2]), DOWN, color=BLEU, buff=0.1)
        texte_b = Tex(r"$P(B)=0{,}4$", font_size=40, color=BLEU).next_to(accolade_b, DOWN, buff=0.12)
        legende = self.legende("Autre piège : ne pas confondre « A sachant B » et « B sachant A »", ["« A sachant B »", "« B sachant A »"])
        self.play(Create(VGroup(*bandes)), *[FadeIn(e) for e in etiquettes], GrowFromCenter(accolade_a), FadeIn(texte_a),
                  GrowFromCenter(accolade_b), FadeIn(texte_b), FadeIn(legende))
        self.play(bandes[1].animate.set_fill(teinte(ACCENT), opacity=1))
        detail = self.detail(None, tex(r"$P(A\cap B)=0{,}2$", 46))
        self.wait(3.0)

        legende = self.changer(legende, self.legende("Sachant B (longueur 0,4), l'intersection en occupe la moitié", ["Sachant B"]))
        self.play(Indicate(accolade_b, color=ACCENT, scale_factor=1.0), Indicate(texte_b, color=ACCENT, scale_factor=1.1))
        detail = self.detail(detail, tex(r"$P(A\mid B)=\dfrac{0{,}2}{0{,}4}=0{,}5$", 46))
        self.wait(4.0)
        legende = self.changer(legende, self.legende("Sachant A (longueur 0,8), elle n'en occupe que le quart", ["Sachant A"]))
        self.play(Indicate(accolade_a, color=ACCENT, scale_factor=1.0), Indicate(texte_a, color=ACCENT, scale_factor=1.1))
        detail = self.detail(detail, tex(r"$P(B\mid A)=\dfrac{0{,}2}{0{,}8}=0{,}25$", 46))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Même intersection, mais pas la même condition : les deux valeurs diffèrent", ["pas la même condition"]))
        detail = self.detail(detail, tex(r"$P(A\mid B)=0{,}5\;\neq\;P(B\mid A)=0{,}25$", 46, {r"\neq": ROUGE}))
        self.wait(4.0)
        legende = self.changer(legende, self.legende("Passer de l'un à l'autre, c'est le rôle de la formule de Bayes", ["formule de Bayes"]))
        self.wait(4.0)

        self.fin()
