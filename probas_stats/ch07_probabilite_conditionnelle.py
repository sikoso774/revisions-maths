"""Chapitre 7 : probabilité conditionnelle (exercice 2.4.1, reprise de l'exercice 2.3.1)."""
from common import *
from proba import *

# Même barre que le chapitre 2 : « A seul » 0,6 | « A et B » 0,2 | « B seul » 0,2
LARGEURS = [6.0, 2.0, 2.0]
X_GAUCHE = -5.0
LARGEUR_BARRE = 10.0
Y_BARRE = 0.3
HAUTEUR_BARRE = 1.4


def teinte(couleur, force=0.5):
    return interpolate_color(ManimColor(FOND), ManimColor(couleur), force)


class Chapitre07(SceneProbas):
    def construct(self):
        titre = self.intro("Probabilité conditionnelle", 7)

        # ── Théorie ─────────────────────────────────────────────────────────
        carte = self.carte(
            "Probabilité de A sachant B",
            ACCENT,
            [
                tex(r"$P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}\qquad(P(B)>0)$", 44, {r"A\mid B": VERT}),
                tex(r"$P(A\cap B)=P(A\mid B)\,P(B)$", 44),
            ],
            [
                texte("Quand on sait que B est réalisé, l'univers se restreint à B", 26, ["l'univers se restreint"]),
                texte("On ne regarde plus que la part de A qui tombe dans B", 26, ["la part de A"]),
            ],
        )

        # ── Démonstration : l'exercice 2.4.1 sur la barre de l'exercice 2.3.1 ─────
        bandes, x = [], X_GAUCHE
        for largeur in LARGEURS:
            bande = Rectangle(width=largeur, height=HAUTEUR_BARRE, stroke_color=GRIS, stroke_width=3,
                              fill_color=FOND, fill_opacity=1).move_to([x + largeur / 2, Y_BARRE, 0])
            x += largeur
            bandes.append(bande)
        barre = VGroup(*bandes)
        etiquettes = [
            Tex(r"$0{,}6$", font_size=44).move_to(bandes[0].get_center()),
            Tex(r"$0{,}2$", font_size=44, color=ACCENT).move_to(bandes[1].get_center()),
            Tex(r"$0{,}2$", font_size=44).move_to(bandes[2].get_center()),
        ]
        for e in etiquettes:
            e.set_z_index(3)
        omega = Tex(r"$\Omega$", font_size=44, color=GRIS).next_to(bandes[0], LEFT, buff=0.2)
        accolade_a = Brace(VGroup(bandes[0], bandes[1]), UP, color=VERT, buff=0.1)
        texte_a = Tex(r"$P(A)=0{,}8$", font_size=40, color=VERT).next_to(accolade_a, UP, buff=0.12)
        accolade_b = Brace(VGroup(bandes[1], bandes[2]), DOWN, color=BLEU, buff=0.1)
        texte_b = Tex(r"$P(B)=0{,}4$", font_size=40, color=BLEU).next_to(accolade_b, DOWN, buff=0.12)
        accessoires = [accolade_a, texte_a, accolade_b, texte_b]

        legende = self.legende("On reprend l'exercice 2.3.1 : les trois morceaux de Ω", ["exercice 2.3.1"])
        self.dezoom(
            carte,
            Create(barre), *[FadeIn(e) for e in etiquettes], FadeIn(omega),
            GrowFromCenter(accolade_a), FadeIn(texte_a), GrowFromCenter(accolade_b), FadeIn(texte_b),
            FadeIn(legende),
        )
        detail = self.detail(None, tex(r"$P(A)=0{,}8\qquad P(B)=0{,}4\qquad P(A\cap B)=0{,}2$", 42))
        self.wait(4.0)

        elements = [*bandes, *etiquettes, *accessoires]
        for m in elements:
            m.save_state()

        def restreindre(indices):
            """Animations : seules les bandes `indices` restent, étirées pour remplir toute la barre."""
            facteur = LARGEUR_BARRE / sum(LARGEURS[i] for i in indices)
            x = X_GAUCHE
            animations = []
            for i in range(3):
                if i in indices:
                    w = LARGEURS[i] * facteur
                    animations.append(bandes[i].animate.stretch_to_fit_width(w).move_to([x + w / 2, Y_BARRE, 0]))
                    animations.append(etiquettes[i].animate.move_to([x + w / 2, Y_BARRE, 0]))
                    x += w
                else:
                    animations.append(bandes[i].animate.set_opacity(0))
                    animations.append(etiquettes[i].animate.set_opacity(0))
            return animations

        def remplir(indices, couleur):
            return [bandes[i].animate.set_fill(teinte(couleur), opacity=1) for i in indices]

        # (bandes connues, couleur, bandes visées, couleur, formule, phrase, mots clés, nouvelles valeurs des bandes)
        questions = [
            ([1, 2], BLEU, [1], VERT,
             r"$P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}=\dfrac{0{,}2}{0{,}4}=0{,}5$",
             "On sait que B est réalisé : l'univers se restreint à B, de longueur 0,4", ["l'univers se restreint"],
             {1: r"$0{,}5$", 2: r"$0{,}5$"}),
            ([0, 1], VERT, [1], BLEU,
             r"$P(B\mid A)=\dfrac{P(A\cap B)}{P(A)}=\dfrac{0{,}2}{0{,}8}=0{,}25$",
             "On sait que A est réalisé : l'univers devient A, de longueur 0,8", ["l'univers devient A"],
             {0: r"$0{,}75$", 1: r"$0{,}25$"}),
            ([2], VIOLET, [2], BLEU,
             r"$P(B\mid\bar{A})=\dfrac{P(\bar{A}\cap B)}{P(\bar{A})}=\dfrac{0{,}2}{0{,}2}=1$",
             "Si A n'arrive pas, il ne reste que la bande de droite : tout y est dans B", ["A n'arrive pas"],
             {2: r"$1$"}),
            ([0, 1], VERT, [0], ACCENT,
             r"$P(\bar{B}\mid A)=\dfrac{P(A\cap\bar{B})}{P(A)}=\dfrac{0{,}6}{0{,}8}=0{,}75=1-P(B\mid A)$",
             "Le complément se prend sur la partie de gauche : 1 − 0,25 = 0,75", ["partie de gauche"],
             {0: r"$0{,}75$", 1: r"$0{,}25$"}),
            ([0, 1, 2], GRIS, [0, 1], VERT,
             r"$P(A\mid\Omega)=\dfrac{P(A\cap\Omega)}{P(\Omega)}=\dfrac{P(A)}{1}=0{,}8$",
             "Savoir que « quelque chose s'est produit » n'apprend rien", ["n'apprend rien"],
             {}),
        ]
        for connues, c_connue, visees, c_visee, formule, phrase, cles, nouvelles in questions:
            legende = self.changer(legende, self.legende(phrase, cles))
            self.play(*remplir(connues, c_connue), *[FadeOut(m) for m in accessoires], run_time=1.0)
            self.wait(1.0)
            self.play(*restreindre(connues), run_time=1.8)
            nouvelles_etiquettes = []
            for i, contenu in nouvelles.items():
                nouvelle = Tex(contenu, font_size=44).move_to(etiquettes[i].get_center())
                nouvelle.set_z_index(3)
                nouvelles_etiquettes.append(Transform(etiquettes[i], nouvelle))
            self.play(*remplir(visees, c_visee), *nouvelles_etiquettes, run_time=1.0)
            detail = self.detail(detail, tex(formule, 40))
            self.wait(4.5)
            self.play(*[Restore(m) for m in elements], run_time=1.2)

        # Le piège du complément
        legende = self.changer(legende, self.legende("Mais le complément ne s'applique jamais à la condition", ["jamais à la condition"]))
        detail = self.detail(detail, tex(r"$P(B\mid\bar{A})=1\;\neq\;1-P(B\mid A)=0{,}75$", 44, {r"\neq": ROUGE}))
        self.wait(5.0)

        # Pas indépendants : annonce du chapitre suivant
        legende = self.changer(legende, self.legende("Savoir B change la probabilité de A : ces deux événements ne sont pas indépendants", ["ne sont pas indépendants"]))
        detail = self.detail(detail, tex(r"$P(A\mid B)=0{,}5\;\neq\;P(A)=0{,}8$", 46, {r"\neq": ROUGE}))
        self.wait(5.0)

        self.fin()
