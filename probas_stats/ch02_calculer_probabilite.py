"""Chapitre 2 : calculer une probabilité (cas favorables, contraire, union, De Morgan, exercice 2.3.1)."""
from common import *
from proba import *

# Barre de l'exercice 2.3.1 : Ω de longueur 10, découpée en « A seul » | « A et B » | « B seul »
LARGEURS = [6.0, 2.0, 2.0]
X_GAUCHE = -5.0
Y_BARRE = 0.3
HAUTEUR_BARRE = 1.4


class Chapitre02(SceneProbas):
    def construct(self):
        titre = self.intro("Calculer une probabilité", 2)

        # ── Théorie : trois cartes ─────────────────────────────────────────
        carte = self.carte(
            "Probabilité et événement contraire",
            ACCENT,
            [
                tex(r"$P(E)=\dfrac{\text{cas favorables}}{\text{cas possibles}}$", 44),
                tex(r"$P(\bar{E})=1-P(E)$", 44),
            ],
            [
                texte("Équiprobabilité : toutes les issues ont la même chance (dé équilibré)", 26, ["Équiprobabilité"]),
                texte("Contraire : « E n'arrive pas », souvent plus simple à calculer", 26, ["Contraire"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "Addition d'événements",
            ACCENT,
            [
                tex(r"$A\cap B=\emptyset\;\Rightarrow\;P(A\cup B)=P(A)+P(B)$", 40),
                tex(r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$", 42),
            ],
            [
                texte("Exclusifs : jamais en même temps, on additionne simplement", 26, ["Exclusifs"]),
                texte("Cas général : l'intersection est comptée deux fois, on la retire une fois", 26, ["Cas général"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "Lois de De Morgan",
            ACCENT,
            [
                tex(r"$\overline{A\cup B}=\bar{A}\cap\bar{B}$", 44),
                tex(r"$\overline{A\cap B}=\bar{A}\cup\bar{B}$", 44),
            ],
            [
                texte("Le contraire d'un « ou » est un « et » des contraires", 26, {"« ou »": BLEU, "« et »": VERT}),
                texte("Le contraire d'un « et » est un « ou » des contraires", 26, {"« ou »": BLEU, "« et »": VERT}),
            ],
        )

        # ── Démonstration 1 : le dé équilibré ───────────────────────────────
        cadre = univers(9.6, 4.0, [0, Y0, 0])
        faces = {n: face_de(n, 0.7).move_to(PLACES[n]) for n in range(1, 7)}
        cercle_a, lettre_a = cercle_evenement(CERCLE_A, "A", VERT, 150)
        cercle_b, lettre_b = cercle_evenement(CERCLE_B, "B", BLEU, 40)
        legende = self.legende("Dé équilibré : chacune des 6 faces a la même chance", ["Dé équilibré"])

        def remettre(*numeros):
            return [a for n in numeros for a in style_de(faces[n], BLANC)]

        self.dezoom(
            carte,
            FadeIn(cadre),
            *[FadeIn(f) for f in faces.values()],
            Create(cercle_a), Create(cercle_b), FadeIn(lettre_a), FadeIn(lettre_b),
            FadeIn(legende),
        )
        self.wait(1.5)

        # P(A) : cas favorables / cas possibles
        legende = self.changer(legende, self.legende("A = « pair » : 3 cas favorables sur 6 cas possibles", ["3 cas favorables", "6 cas possibles"]))
        self.play(*[a for n in (2, 4, 6) for a in style_de(faces[n], VERT, 0.3)])
        self.play(LaggedStart(*[Indicate(faces[n], color=VERT, scale_factor=1.3) for n in (2, 4, 6)], lag_ratio=0.4))
        detail = self.detail(None, tex(r"$P(A)=\dfrac{3}{6}=\dfrac{1}{2}$", 46, {"A": VERT}))
        self.wait(3.0)

        # P(B)
        legende = self.changer(legende, self.legende("B = « plus de 4 » : 2 cas favorables sur 6", ["2 cas favorables"]))
        self.play(*remettre(2, 4, 6))
        self.play(*[a for n in (5, 6) for a in style_de(faces[n], BLEU, 0.3)])
        self.play(LaggedStart(*[Indicate(faces[n], color=BLEU, scale_factor=1.3) for n in (5, 6)], lag_ratio=0.4))
        detail = self.detail(detail, tex(r"$P(B)=\dfrac{2}{6}=\dfrac{1}{3}$", 46, {"B": BLEU}))
        self.wait(3.0)

        # Contraire
        legende = self.changer(legende, self.legende("Le contraire de A : les 3 faces impaires", ["contraire de A"]))
        self.play(*remettre(5, 6))
        self.play(*[a for n in (1, 3, 5) for a in style_de(faces[n], VIOLET, 0.3)])
        detail = self.detail(detail, tex(r"$P(\bar{A})=1-P(A)=1-\dfrac{1}{2}=\dfrac{1}{2}$", 44, {r"\bar{A}": VIOLET}))
        self.wait(3.0)

        # Addition d'événements exclusifs : A = pair et C = 1 ou 3
        legende = self.changer(legende, self.legende("A (pair) et C (1 ou 3) n'ont aucune face en commun : on additionne", ["n'ont aucune face en commun", "on additionne"]))
        self.play(*remettre(1, 3, 5), FadeOut(cercle_b), FadeOut(lettre_b))
        self.play(*[a for n in (2, 4, 6) for a in style_de(faces[n], VERT, 0.3)],
                  *[a for n in (1, 3) for a in style_de(faces[n], ROUGE, 0.3)])
        detail = self.detail(detail, tex(r"$P(A\cup C)=\dfrac{3}{6}+\dfrac{2}{6}=\dfrac{5}{6}$", 46, {r"C": ROUGE}))
        self.wait(3.5)

        # Cas général : A et B se chevauchent sur le 6
        legende = self.changer(legende, self.legende("A et B se chevauchent : le 6 est à la fois pair et plus grand que 4", ["le 6"]))
        self.play(*remettre(1, 2, 3, 4), FadeIn(cercle_b), FadeIn(lettre_b))
        self.play(*[a for n in (2, 4, 5, 6) for a in style_de(faces[n], ACCENT, 0.3)])
        mot_double = Text("compté 2 fois", font_size=22, weight=BOLD, color=ROUGE)
        fond_double = BackgroundRectangle(mot_double, color=FOND, fill_opacity=1, buff=0.06)
        double = VGroup(fond_double, mot_double).move_to([0.28, Y0 + 0.8, 0])
        double.set_z_index(3)
        detail = self.detail(detail, tex(r"$\dfrac{3}{6}+\dfrac{2}{6}=\dfrac{5}{6}$ \quad mais il n'y a que 4 faces !", 42))
        self.play(FadeIn(double, shift=DOWN * 0.2), Indicate(faces[6], color=ROUGE, scale_factor=1.3))
        self.wait(2.5)
        legende = self.changer(legende, self.legende("On retire une fois l'intersection {6}, comptée en double", ["l'intersection"]))
        detail = self.detail(detail, tex(r"$P(A\cup B)=\dfrac{3}{6}+\dfrac{2}{6}-\dfrac{1}{6}=\dfrac{4}{6}=\dfrac{2}{3}$", 42, {r"-\dfrac{1}{6}": ROUGE}))
        self.wait(4.0)

        # ── Démonstration 2 : l'exercice 2.3.1 ─────────────────────────────
        autres = [m for m in self.mobjects if m is not titre and m is not self.trait_titre]
        self.play(*[FadeOut(m) for m in autres])

        bandes = []
        x = X_GAUCHE
        for largeur in LARGEURS:
            bande = Rectangle(width=largeur, height=HAUTEUR_BARRE, stroke_color=GRIS, stroke_width=3,
                              fill_color=FOND, fill_opacity=1)
            bande.move_to([x + largeur / 2, Y_BARRE, 0])
            x += largeur
            bandes.append(bande)
        barre = VGroup(*bandes)
        omega = Tex(r"$\Omega$", font_size=44, color=GRIS).next_to(barre, LEFT, buff=0.2)
        omega.shift(LEFT * 0.0)

        def etiquette(i, contenu, couleur=TEXTE):
            t = Tex(contenu, font_size=44, color=couleur).move_to(bandes[i].get_center())
            t.set_z_index(3)
            return t

        def remplir(indices, couleur):
            return [bandes[i].animate.set_fill(interpolate_color(ManimColor(FOND), ManimColor(couleur), 0.5), opacity=1)
                    for i in indices]

        def vider():
            return [b.animate.set_fill(FOND, opacity=1) for b in bandes]

        legende = self.legende("Ω est une barre de longueur 1 : les longueurs sont des probabilités", ["longueur 1"])
        detail = self.detail(None, tex(r"$P(A)=0{,}8\qquad P(B)=0{,}4\qquad P(A\cap B)=0{,}2$", 42))
        self.play(Create(barre), FadeIn(omega), FadeIn(legende))
        self.wait(3.0)

        accolade_a = Brace(VGroup(bandes[0], bandes[1]), UP, color=VERT, buff=0.1)
        texte_a = Tex(r"$P(A)=0{,}8$", font_size=40, color=VERT).next_to(accolade_a, UP, buff=0.12)
        accolade_b = Brace(VGroup(bandes[1], bandes[2]), DOWN, color=BLEU, buff=0.1)
        texte_b = Tex(r"$P(B)=0{,}4$", font_size=40, color=BLEU).next_to(accolade_b, DOWN, buff=0.12)
        legende = self.changer(legende, self.legende("A occupe 0,8 de la barre, B occupe 0,4 : ils se recouvrent sur 0,2", ["se recouvrent"]))
        self.play(GrowFromCenter(accolade_a), FadeIn(texte_a))
        self.play(GrowFromCenter(accolade_b), FadeIn(texte_b))
        self.wait(2.0)

        # Les trois morceaux de Ω
        legende = self.changer(legende, self.legende("L'intersection est la bande commune : P(A et B) = 0,2", ["P(A et B) = 0,2"]))
        lab1, lab2, lab3 = etiquette(0, r"$0{,}6$"), etiquette(1, r"$0{,}2$", ACCENT), etiquette(2, r"$0{,}2$")
        self.play(*remplir([1], ACCENT))
        self.play(FadeIn(lab2))
        self.wait(2.0)
        legende = self.changer(legende, self.legende("B se coupe en deux morceaux disjoints : « avec A » et « sans A »", ["deux morceaux disjoints"]))
        self.play(*remplir([2], BLEU))
        detail = self.detail(detail, tex(r"$P(\bar{A}\cap B)=P(B)-P(A\cap B)=0{,}4-0{,}2=0{,}2$", 40))
        self.play(FadeIn(lab3))
        self.wait(3.5)
        legende = self.changer(legende, self.legende("De même pour A : la partie de A sans B", ["sans B"]))
        self.play(*remplir([0], VERT))
        detail = self.detail(detail, tex(r"$P(A\cap\bar{B})=P(A)-P(A\cap B)=0{,}8-0{,}2=0{,}6$", 40))
        self.play(FadeIn(lab1))
        self.wait(3.5)
        legende = self.changer(legende, self.legende("Les trois morceaux recouvrent tout Ω : rien n'échappe à A et B", ["tout Ω"]))
        detail = self.detail(detail, tex(r"$0{,}6+0{,}2+0{,}2=1$", 44))
        self.wait(3.0)
        self.play(*vider(), *[FadeOut(m) for m in (accolade_a, accolade_b, texte_a, texte_b)])

        # Les huit probabilités demandées
        requetes = [
            ([0, 1, 2], ACCENT, r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)=0{,}8+0{,}4-0{,}2=1$",
             "Union : on retire l'intersection comptée deux fois", ["Union"]),
            ([2], VIOLET, r"$P(\bar{A})=1-P(A)=1-0{,}8=0{,}2$",
             "Contraire de A : 1 moins la probabilité de A", ["Contraire de A"]),
            ([0], VIOLET, r"$P(\bar{B})=1-P(B)=1-0{,}4=0{,}6$",
             "Contraire de B : 1 moins la probabilité de B", ["Contraire de B"]),
            ([2], BLEU, r"$P(\bar{A}\cap B)=P(B)-P(A\cap B)=0{,}4-0{,}2=0{,}2$",
             "B sans A : la bande de droite", ["B sans A"]),
            ([0, 1], VERT, r"$P(A\cup\bar{B})=P(A)+P(\bar{B})-P(A\cap\bar{B})=0{,}8+0{,}6-0{,}6=0{,}8$",
             "A ou « pas B » : on retire A sans B, compté deux fois", ["A ou « pas B »"]),
            ([0, 2], ACCENT, r"$P(\bar{A}\cup\bar{B})=P(\overline{A\cap B})=1-P(A\cap B)=1-0{,}2=0{,}8$",
             "De Morgan : le contraire d'un « et » est un « ou » des contraires", ["De Morgan"]),
            ([], ROUGE, r"$P(\bar{A}\cap\bar{B})=P(\overline{A\cup B})=1-P(A\cup B)=1-1=0$",
             "De Morgan : aucun résultat n'échappe à la fois à A et à B", ["De Morgan"]),
            ([0, 1, 2], VERT, r"$P(\bar{A}\cup\Omega)=P(\Omega)=1$",
             "Ω contient tout : la réunion avec Ω vaut Ω", ["Ω contient tout"]),
        ]
        for indices, couleur, formule, phrase, cles in requetes:
            legende = self.changer(legende, self.legende(phrase, cles))
            detail = self.detail(detail, tex(formule, 40))
            if indices:
                self.play(*remplir(indices, couleur))
            else:
                vide = Text("aucune bande : P = 0", font_size=28, weight=BOLD, color=ROUGE).next_to(barre, DOWN, buff=0.5)
                self.play(FadeIn(vide, shift=UP * 0.2))
            self.wait(3.5)
            if not indices:
                self.play(FadeOut(vide), run_time=0.5)
            self.play(*vider(), run_time=0.5)

        legende = self.changer(legende, self.legende("Vérification : les deux résultats se confirment l'un l'autre", ["se confirment"]))
        detail = self.detail(detail, tex(r"$P(A\cup B)=1\;\Longleftrightarrow\;P(\bar{A}\cap\bar{B})=0$", 44))
        self.wait(4.0)

        self.fin()
