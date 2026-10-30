"""Chapitre 3 : dénombrement, choisir la bonne formule (tiercé, exercices 2.3.2 et 2.3.3)."""
from itertools import permutations
from common import *
from proba import *

# Tableau « ordre / remise » : colonnes (en-tête, remise oui, remise non) et lignes (en-tête, ordre oui, ordre non)
X = [-5.7, -3.1, 1.3, 5.7]
Y = [1.3, 0.6, -1.4, -2.8]
PODIUM = [11, 4, 8]  # chevaux choisis dans la démonstration du tiercé


def case(i, j):
    """Rectangle de la case (ligne i, colonne j) du tableau."""
    return Rectangle(
        width=X[j + 1] - X[j], height=Y[i] - Y[i + 1], stroke_color=GRIS, stroke_width=2,
    ).move_to([(X[j] + X[j + 1]) / 2, (Y[i] + Y[i + 1]) / 2, 0])


def contenu_case(i, j, *elements):
    return VGroup(*elements).arrange(DOWN, buff=0.1).move_to(case(i, j).get_center())


def rangee_de_places(nombre, pas, largeur, y, noms):
    """Cases alignées (le podium) avec leur nom au-dessus : renvoie (cadres, titres)."""
    x0 = -pas * (nombre - 1) / 2
    cadres, titres = [], []
    for k in range(nombre):
        cadre = Rectangle(width=largeur, height=1.1, stroke_color=GRIS, stroke_width=3).move_to([x0 + pas * k, y, 0])
        titre = Text(noms[k], font_size=24, weight=BOLD, color=GRIS).move_to([x0 + pas * k, y + 0.85, 0])
        cadres.append(cadre)
        titres.append(titre)
    return cadres, titres


class Chapitre03(SceneProbas):
    def construct(self):
        titre = self.intro("Dénombrement : choisir la bonne formule", 3)

        self.tableau_des_formules()
        self.play(*[FadeOut(m) for m in self.mobjects if m is not titre and m is not self.trait_titre])

        relation = self.carte(
            "Arrangement = combinaison × ordre",
            ACCENT,
            [
                tex(r"$A_n^p=C_n^p\times p!$", 46, {r"p!": ACCENT}),
                tex(r"$C_n^p=\dfrac{A_n^p}{p!}=\dfrac{n!}{p!\,(n-p)!}$", 46, {r"p!": ACCENT}),
            ],
            [
                texte("Un groupe de p éléments peut être rangé de p! façons différentes", 26, ["p!"]),
                texte("Pour une combinaison, on « efface » l'ordre en divisant par p!", 26, ["combinaison"]),
            ],
        )
        self.tierce_dans_l_ordre(relation, titre)
        self.tierce_dans_le_desordre(titre)
        self.ordres_d_arrivee(titre)
        self.quinte(titre)
        self.fin()

    # ── Théorie : le tableau à double entrée ──────────────────────────────
    def tableau_des_formules(self):
        q1 = texte("Question 1 : l'ordre compte-t-il ?", 28, {"Question 1": ACCENT, "l'ordre": VIOLET}).move_to([0, 2.35, 0])
        q2 = texte("Question 2 : un élément peut-il être choisi plusieurs fois (remise) ?", 26,
                   {"Question 2": ACCENT, "remise": BLEU}).move_to([0, 1.8, 0])

        def entete(i, j, contenu, couleur):
            t = texte(contenu, 24, {contenu: couleur}).move_to(case(i, j).get_center())
            return VGroup(case(i, j), t)

        lignes = [entete(1, 0, "Ordre : oui", VIOLET), entete(2, 0, "Ordre : non", VIOLET)]
        colonnes = [entete(0, 1, "Remise : oui", BLEU), entete(0, 2, "Remise : non", BLEU)]

        p_liste = contenu_case(
            1, 1,
            texte("p-liste", 26, {"p-liste": BLEU}),
            tex(r"$n^p$", 40),
        )
        arrangement = contenu_case(
            1, 2,
            texte("Arrangement", 26, {"Arrangement": VIOLET}),
            tex(r"$A_n^p=\dfrac{n!}{(n-p)!}$", 32),
            texte("si p = n : permutation, n!", 20, {"permutation": ACCENT}),
        )
        combinaison = contenu_case(
            2, 2,
            texte("Combinaison", 26, {"Combinaison": VERT}),
            tex(r"$C_n^p=\dfrac{n!}{p!\,(n-p)!}$", 32),
        )
        hors_cours = texte("hors du cours", 22, couleur=GRIS).move_to(case(2, 1).get_center())

        legende = self.legende("Deux questions, quatre formules : on ne mémorise pas au hasard", ["Deux questions"])
        self.play(FadeIn(q1, shift=DOWN * 0.2), FadeIn(legende))
        self.wait(1.5)
        self.play(*[FadeIn(l) for l in lignes])
        self.wait(1.5)
        self.play(FadeIn(q2, shift=DOWN * 0.2))
        self.wait(1.5)
        self.play(*[FadeIn(c) for c in colonnes])
        self.wait(1.5)
        for cadre in (case(1, 1), case(1, 2), case(2, 1), case(2, 2)):
            self.add(cadre)
        for formule in (p_liste, arrangement, combinaison):
            self.play(Write(formule), run_time=2)
            self.wait(2.5)
        self.play(FadeIn(hors_cours))
        self.wait(2.5)
        self.wait(1.0)

    # ── Démonstration 1 : tiercé dans l'ordre, 15 chevaux ───────────────────
    def tierce_dans_l_ordre(self, relation, titre):
        pool = VGroup(*[disque(i + 1) for i in range(15)])
        for i, d in enumerate(pool):
            d.move_to([-5.6 + 0.8 * i, 1.95, 0])
        cadres, titres = rangee_de_places(3, 3.2, 1.9, 0.15, ["1er", "2e", "3e"])
        legende = self.legende("15 chevaux au départ : combien de tiercés dans l'ordre ?", ["tiercés dans l'ordre"])

        self.dezoom(relation, LaggedStart(*[GrowFromCenter(d) for d in pool], lag_ratio=0.05), FadeIn(legende))
        self.play(*[Create(c) for c in cadres], *[FadeIn(t) for t in titres])
        self.wait(1.5)

        phrases = [
            ("1re place : les 15 chevaux sont possibles", ["15 chevaux"]),
            ("2e place : le premier est déjà classé, il en reste 14", ["14"]),
            ("3e place : il en reste 13", ["13"]),
        ]
        detail = None
        for k, numero in enumerate(PODIUM):
            legende = self.changer(legende, self.legende(*phrases[k]))
            choix = texte(f"{15 - k} choix", 26, {f"{15 - k}": ACCENT}).move_to(cadres[k].get_center() + DOWN * 0.95)
            self.play(FadeIn(choix, shift=UP * 0.2))
            self.wait(1.0)
            copie = pool[numero - 1].copy()
            self.play(copie.animate.move_to(cadres[k].get_center()), pool[numero - 1].animate.set_opacity(0.25))
            self.wait(1.0)

        legende = self.changer(legende, self.legende("Chaque place retire un cheval de la liste : on multiplie", ["on multiplie"]))
        detail = self.detail(None, tex(r"$15\times 14\times 13=2730$", 48))
        self.wait(3.0)
        detail = self.detail(detail, tex(r"$A_{15}^3=\dfrac{15!}{12!}=15\times 14\times 13=2730$", 44, {r"A_{15}^3": VIOLET}))
        self.wait(4.0)
        self.vider(titre)

    # ── Démonstration 2 : tiercé dans le désordre ────────────────────────────
    def tierce_dans_le_desordre(self, titre):
        groupes = VGroup()
        for k, ordre in enumerate(permutations(PODIUM)):
            discs = VGroup(*[disque(n, couleur=BLANC, rayon=0.3) for n in ordre]).arrange(RIGHT, buff=0.25)
            cadre = RoundedRectangle(
                width=discs.width + 0.5, height=0.95, corner_radius=0.15, stroke_color=GRIS, stroke_width=2,
            ).move_to(discs.get_center())
            groupes.add(VGroup(cadre, discs))
        groupes.arrange_in_grid(rows=2, cols=3, buff=(0.8, 0.5)).move_to([0, 0.9, 0])

        legende = self.legende("« Dans le désordre » : seul compte le trio, pas son ordre", ["le trio"])
        self.play(FadeIn(legende))
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in groupes], lag_ratio=0.35), run_time=3.0)
        detail = self.detail(None, tex(r"$3!=6$ ordres pour les mêmes chevaux $\{4,\,8,\,11\}$", 42, {r"3!": ACCENT}))
        self.wait(3.0)

        legende = self.changer(legende, self.legende("Ces 6 tiercés dans l'ordre ne forment qu'un seul tiercé dans le désordre", ["un seul"]))
        self.play(*[g[0].animate.set_stroke(VERT, width=4) for g in groupes])
        self.wait(2.5)
        detail = self.detail(detail, tex(r"$C_{15}^3=\dfrac{A_{15}^3}{3!}=\dfrac{2730}{6}=455$", 46, {r"C_{15}^3": VERT}))
        legende = self.changer(legende, self.legende("On divise par 3! : l'ordre est effacé", ["3!"]))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Piège : « dans l'ordre » est un arrangement, « dans le désordre » une combinaison", ["arrangement", "combinaison"]))
        self.wait(4.0)
        self.vider(titre)

    # ── Exercice 2.3.2 : l'ordre d'arrivée complet ────────────────────────────
    def ordres_d_arrivee(self, titre):
        cases = VGroup(*[
            Square(side_length=0.62, stroke_color=GRIS, stroke_width=3).move_to([-5.6 + 0.8 * i, 0.9, 0]) for i in range(15)
        ])
        numeros = VGroup(*[
            Text(str(i + 1), font_size=16, color=GRIS).next_to(cases[i], UP, buff=0.1) for i in range(15)
        ])
        legende = self.legende("Combien d'ordres d'arrivée possibles pour 15 chevaux ?", ["ordres d'arrivée"])
        self.play(Create(cases), FadeIn(numeros), FadeIn(legende))
        self.wait(1.5)

        accolade = Brace(cases, DOWN, color=BLEU, buff=0.12)
        reste = Tex(r"$15!$", font_size=44, color=BLEU).next_to(accolade, DOWN, buff=0.12)
        self.play(GrowFromCenter(accolade), FadeIn(reste))
        legende = self.changer(legende, self.legende("On range les 15 chevaux dans les 15 places : une permutation", ["permutation"]))
        detail = self.detail(None, tex(r"$15!=1\,307\,674\,368\,000$", 46, {r"15!": BLEU}))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Si a, b et c sont imposés aux trois premières places…", ["a, b et c"]))
        lettres = [disque(c, couleur=ACCENT, rayon=0.27) for c in "abc"]
        for lettre, case_ in zip(lettres, cases[:3]):
            lettre.move_to(case_.get_center())
        self.play(*[FadeIn(l, scale=0.5) for l in lettres], *[c.animate.set_stroke(ACCENT) for c in cases[:3]])
        self.wait(1.0)
        accolade_restes = Brace(VGroup(*cases[3:]), DOWN, color=BLEU, buff=0.12)
        reste_restes = Tex(r"$12!$", font_size=44, color=BLEU).next_to(accolade_restes, DOWN, buff=0.12)
        self.play(ReplacementTransform(accolade, accolade_restes), ReplacementTransform(reste, reste_restes))
        legende = self.changer(legende, self.legende("…il reste à ranger les 12 autres chevaux dans les 12 autres places", ["12 autres"]))
        detail = self.detail(detail, tex(r"$12!=479\,001\,600$", 46, {r"12!": BLEU}))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Proportion de classements qui commencent par a, b, c", ["Proportion"]))
        detail = self.detail(detail, tex(r"$\dfrac{12!}{15!}=\dfrac{1}{15\times 14\times 13}=\dfrac{1}{2730}\approx 0{,}000366$", 42, {r"\dfrac{1}{2730}": ACCENT}))
        self.wait(5.0)

        legende = self.changer(legende, self.legende("Pour n chevaux et k places fixées : une chance sur A(n, k)", ["une chance sur"]))
        detail = self.detail(detail, tex(r"$\dfrac{(n-k)!}{n!}=\dfrac{1}{n(n-1)\cdots(n-k+1)}=\dfrac{1}{A_n^k}$", 42, {r"A_n^k": VIOLET}))
        self.wait(5.0)
        self.vider(titre)

    # ── Exercice 2.3.3 : le quinté ─────────────────────────────────────────────
    def quinte(self, titre):
        cadres, titres = rangee_de_places(5, 2.4, 1.7, 0.45, ["1er", "2e", "3e", "4e", "5e"])
        legende = self.legende("Quinté dans l'ordre : on prédit les 5 premiers", ["Quinté dans l'ordre"])
        self.play(*[Create(c) for c in cadres], *[FadeIn(t) for t in titres], FadeIn(legende))
        self.wait(1.5)

        produit = ["15", r"15\times 14=210", r"210\times 13=2730", r"2730\times 12=32\,760", r"32\,760\times 11=360\,360"]
        detail = None
        for k, ligne in enumerate(produit):
            choix = texte(f"{15 - k} choix", 24, {f"{15 - k}": ACCENT}).move_to(cadres[k].get_center() + DOWN * 0.9)
            self.play(FadeIn(choix, shift=UP * 0.2))
            detail = self.detail(detail, tex(f"${ligne}$", 46))
            self.wait(1.8)
        legende = self.changer(legende, self.legende("5 places, sans remise, l'ordre compte : un arrangement", ["arrangement"]))
        detail = self.detail(detail, tex(r"$A_{15}^5=15\times 14\times 13\times 12\times 11=360\,360$", 44, {r"A_{15}^5": VIOLET}))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Deux chevaux de plus à prédire : 132 fois plus de possibilités qu'au tiercé", ["132 fois plus"]))
        detail = self.detail(detail, tex(r"$\dfrac{360\,360}{2730}=132$", 46, {r"132": ACCENT}))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Avec n participants : chaque place supplémentaire multiplie par un facteur proche de n", ["multiplie"]))
        detail = self.detail(detail, tex(r"$A_n^3=n(n-1)(n-2)$", 46, {r"A_n^3": VIOLET}))
        self.wait(3.0)
        detail = self.detail(detail, tex(r"$A_n^5=n(n-1)(n-2)(n-3)(n-4)$", 46, {r"A_n^5": VIOLET}))
        self.wait(4.0)
