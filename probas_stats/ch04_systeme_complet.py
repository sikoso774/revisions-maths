"""Chapitre 4 : système complet d'événements (exercice 2.3.4, les 30 sujets d'examen)."""
from common import *
from proba import *

# Les 30 sujets : 10 « connus » (vert) et 20 « inconnus » ; le tirage prend 3 sujets d'un coup
EFFECTIFS = [120, 900, 1900, 1140]  # exactement 3, 2, 1, 0 sujets connus
NOMS = ["3 connus", "2 connus", "1 connu", "0 connu"]
COULEURS = [VERT, BLEU, ACCENT, VIOLET]
TOTAL = 4060
X_BARRE = -5.0
LARGEUR_BARRE = 10.0
Y_BARRE = -0.35


class Chapitre04(SceneProbas):
    def construct(self):
        titre = self.intro("Système complet d'événements", 4)

        # ── Théorie ─────────────────────────────────────────────────────────
        carte = self.carte(
            "Système complet d'événements (partition de Ω)",
            ACCENT,
            [
                tex(r"$A_i\cap A_j=\emptyset\quad(i\neq j)$", 42),
                tex(r"$A_1\cup A_2\cup\dots\cup A_n=\Omega$", 42),
                tex(r"$P(A_1)+P(A_2)+\dots+P(A_n)=1$", 42),
            ],
            [
                texte("Disjoints : jamais deux de ces événements en même temps", 26, ["Disjoints"]),
                texte("Ils recouvrent Ω : l'un d'eux se produit toujours", 26, ["recouvrent Ω"]),
                texte("Leurs probabilités s'additionnent donc à 1", 26, ["s'additionnent"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "Deux réflexes : ET et OU",
            ACCENT,
            [
                tex(r"\textbf{ET} $\Rightarrow$ on multiplie \quad $C_{10}^2\times C_{20}^1$", 40, {r"\textbf{ET}": VERT}),
                tex(r"\textbf{OU} $\Rightarrow$ on additionne \quad $120+900+1900+1140$", 40, {r"\textbf{OU}": BLEU}),
            ],
            [
                texte("ET : deux choix simultanés et indépendants dans un même tirage", 26, ["ET"]),
                texte("OU : des cas alternatifs qui s'excluent, comme les branches de la partition", 26, ["OU"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "« Au moins » par le contraire",
            ACCENT,
            [tex(r"$P(\text{au moins }1)=1-P(\text{aucun})$", 44)],
            [
                texte("Au lieu d'additionner « exactement 1 », « exactement 2 », « exactement 3 »…", 26, ["additionner"]),
                texte("…un seul cas à calculer : « aucun »", 26, ["un seul cas"]),
            ],
        )

        # ── Démonstration : les 30 sujets ──────────────────────────────────────
        connus = VGroup(*[
            Square(side_length=0.6, stroke_color=VERT, stroke_width=3, fill_color=interpolate_color(ManimColor(FOND), ManimColor(VERT), 0.3), fill_opacity=1)
            for _ in range(10)
        ]).arrange_in_grid(rows=2, cols=5, buff=0.13)
        inconnus = VGroup(*[
            Square(side_length=0.6, stroke_color=GRIS, stroke_width=3, fill_color=FOND, fill_opacity=1) for _ in range(20)
        ]).arrange_in_grid(rows=2, cols=10, buff=0.13)
        grille = VGroup(connus, inconnus).arrange(RIGHT, buff=1.0).move_to([0, 1.55, 0])
        nom_connus = texte("10 sujets connus", 24, {"10 sujets connus": VERT}).next_to(connus, UP, buff=0.15)
        nom_inconnus = texte("20 sujets inconnus", 24, {"20 sujets inconnus": GRIS}).next_to(inconnus, UP, buff=0.15)
        legende = self.legende("Un examen : 30 sujets, dont 10 que tu as étudiés", ["10"])
        self.dezoom(
            carte,
            FadeIn(connus), FadeIn(inconnus), FadeIn(nom_connus), FadeIn(nom_inconnus), FadeIn(legende),
        )
        self.wait(2.0)

        legende = self.changer(legende, self.legende("On tire 3 sujets d'un coup : l'ordre ne compte pas, c'est une combinaison", ["combinaison"]))
        choisis = [connus[1], connus[7], inconnus[5]]
        self.play(*[c.animate.set_stroke(ACCENT, width=6) for c in choisis])
        self.play(*[Indicate(c, color=ACCENT, scale_factor=1.25) for c in choisis])
        detail = self.detail(None, tex(r"$|\Omega|=C_{30}^3=\dfrac{30\times 29\times 28}{3\times 2\times 1}=4060$", 44, {r"4060": ACCENT}))
        self.wait(4.0)
        self.play(connus[1].animate.set_stroke(VERT, width=3), connus[7].animate.set_stroke(VERT, width=3),
                  inconnus[5].animate.set_stroke(GRIS, width=3))

        # Les 4 morceaux de Ω
        segments, etiquettes = [], []
        x = X_BARRE
        for effectif, nom, couleur in zip(EFFECTIFS, NOMS, COULEURS):
            largeur = LARGEUR_BARRE * effectif / TOTAL
            seg = Rectangle(width=largeur, height=0.9, stroke_color=GRIS, stroke_width=3, fill_color=FOND, fill_opacity=1)
            seg.move_to([x + largeur / 2, Y_BARRE, 0])
            x += largeur
            segments.append(seg)
        omega = Tex(r"$\Omega$", font_size=44, color=GRIS).next_to(segments[0], LEFT, buff=0.2)
        legende = self.changer(legende, self.legende("On découpe Ω selon le nombre de sujets connus parmi les 3 tirés", ["nombre de sujets connus"]))
        self.play(*[Create(s) for s in segments], FadeIn(omega))
        self.wait(2.0)

        def etiquette(k):
            seg = segments[k]
            nom = Text(NOMS[k], font_size=18, weight=BOLD, color=COULEURS[k])
            valeur = Tex(f"${EFFECTIFS[k]}$", font_size=32, color=COULEURS[k])
            if k == 0:  # bande très étroite : étiquette au-dessus de la barre, pour ne pas toucher sa voisine
                groupe = VGroup(nom, valeur).arrange(RIGHT, buff=0.2)
                return groupe.move_to([seg.get_center()[0] + 0.7, Y_BARRE + 0.8, 0])
            groupe = VGroup(nom, valeur).arrange(DOWN, buff=0.06).move_to([seg.get_center()[0], Y_BARRE - 1.0, 0])
            return groupe

        calculs = [
            (r"$C_{10}^3\times C_{20}^0=120\times 1=120$",
             "3 connus et 0 inconnu : un seul choix dans chaque groupe", ["3 connus"]),
            (r"$C_{10}^2\times C_{20}^1=45\times 20=900$",
             "2 connus ET 1 inconnu : deux choix indépendants, on multiplie", ["ET", "on multiplie"]),
            (r"$C_{10}^1\times C_{20}^2=10\times 190=1900$",
             "1 connu ET 2 inconnus : on multiplie aussi", ["ET", "on multiplie"]),
            (r"$C_{10}^0\times C_{20}^3=1\times 1140=1140$",
             "Aucun connu : les 3 sujets viennent des 20 inconnus", ["Aucun connu"]),
        ]
        for k, (formule, phrase, cles) in enumerate(calculs):
            legende = self.changer(legende, self.legende(phrase, cles))
            self.play(segments[k].animate.set_fill(interpolate_color(ManimColor(FOND), ManimColor(COULEURS[k]), 0.5), opacity=1))
            detail = self.detail(detail, tex(formule, 44))
            etiquettes.append(etiquette(k))
            self.play(FadeIn(etiquettes[-1], shift=UP * 0.15))
            self.wait(3.5)

        legende = self.changer(legende, self.legende("Les 4 cas s'excluent (OU) et recouvrent tout Ω : on additionne", ["OU", "on additionne"]))
        detail = self.detail(detail, tex(r"$120+900+1900+1140=4060=|\Omega|$", 46, {r"|\Omega|": ACCENT}))
        self.play(*[Indicate(s, color=WHITE, scale_factor=1.0) for s in segments])
        self.wait(4.0)

        # Les cinq questions
        def mettre(indices):
            animations = []
            for k, seg in enumerate(segments):
                if k in indices:
                    animations.append(seg.animate.set_fill(interpolate_color(ManimColor(FOND), ManimColor(COULEURS[k]), 0.6), opacity=1))
                else:
                    animations.append(seg.animate.set_fill(FOND, opacity=1))
            return animations

        questions = [
            ([0], r"$P(3\text{ connus})=\dfrac{120}{4060}\approx 0{,}0296$",
             "Les trois sujets sont connus", ["connus"]),
            ([1], r"$P(\text{exactement }2)=\dfrac{900}{4060}\approx 0{,}2217$",
             "Exactement deux sujets connus", ["Exactement deux"]),
            ([3], r"$P(\text{aucun})=\dfrac{1140}{4060}\approx 0{,}2808$",
             "Aucun sujet connu", ["Aucun"]),
            ([0, 1, 2], r"$P(\text{au moins }1)=1-\dfrac{1140}{4060}=\dfrac{2920}{4060}\approx 0{,}7192$",
             "Au moins un connu : tout Ω sauf « aucun », un seul cas à calculer", ["tout Ω sauf « aucun »"]),
            ([0, 1], r"$P(\text{au moins }2)=\dfrac{900+120}{4060}=\dfrac{1020}{4060}\approx 0{,}2512$",
             "Au moins deux connus : « exactement 2 » OU « 3 », deux cas disjoints", ["OU"]),
        ]
        for indices, formule, phrase, cles in questions:
            legende = self.changer(legende, self.legende(phrase, cles))
            self.play(*mettre(indices), run_time=0.8)
            detail = self.detail(detail, tex(formule, 42))
            self.wait(4.5)

        legende = self.changer(legende, self.legende("Moins il y a de cas à calculer, moins on risque de se tromper", ["moins on risque de se tromper"]))
        self.play(*mettre([]), run_time=0.6)
        self.wait(3.0)

        self.fin()
