"""Chapitre 9 : probabilités totales et formule de Bayes (exercices 2.4.2 le QCM, 2.4.3 l'assurance)."""
from common import *
from proba import *

# QCM : arbre « sait / ignore » puis « juste / faux »
RACINE = np.array([-5.4, 0.8, 0])
POS = {
    "K": np.array([-2.6, 1.9, 0]),    # elle connaît la réponse
    "N": np.array([-2.6, -0.3, 0]),   # elle l'ignore
    "Kj": np.array([0.6, 1.9, 0]),    # connaît et répond juste
    "Nj": np.array([0.6, 0.4, 0]),    # ignore mais répond juste (hasard)
    "Nf": np.array([0.6, -1.0, 0]),   # ignore et répond faux
}

# Assurance : trois classes de risque
CLASSES = [("R_1", 0.2, 0.05), ("R_2", 0.5, 0.15), ("R_3", 0.3, 0.30)]


def teinte(couleur, force=0.5):
    return interpolate_color(ManimColor(FOND), ManimColor(couleur), force)


def noeud(contenu, couleur, centre):
    """Étiquette encadrée d'un nœud de l'arbre."""
    t = Text(contenu, font_size=22, weight=BOLD, color=couleur)
    cadre = RoundedRectangle(width=max(1.3, t.width + 0.3), height=0.55, corner_radius=0.12,
                             stroke_color=couleur, stroke_width=3, fill_color=FOND, fill_opacity=1)
    groupe = VGroup(cadre, t).move_to(centre)
    groupe.set_z_index(3)
    return groupe


def etiquette_arete(depart, arrivee, contenu):
    """Probabilité au milieu d'une branche, sur un fond noir qui masque le trait."""
    t = Tex(f"${contenu}$", font_size=28, color=ACCENT)
    fond = BackgroundRectangle(t, color=FOND, fill_opacity=1, buff=0.05)
    groupe = VGroup(fond, t).move_to((depart + arrivee) / 2)
    groupe.set_z_index(2)
    return groupe


class Chapitre09(SceneProbas):
    def construct(self):
        titre = self.intro("Probabilités totales et Bayes", 9)

        # ── Théorie : trois cartes ───────────────────────────────────────────
        carte = self.carte(
            "Probabilités totales",
            ACCENT,
            [tex(r"$P(A)=\sum_i P(A\mid B_i)\,P(B_i)$", 46)],
            [
                texte("Les cas B1, B2… forment un système complet d'événements (chapitre 4)", 26, ["système complet"]),
                texte("On additionne la part de A trouvée dans chacun des cas", 26, ["additionne"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "Formules de Bayes",
            ACCENT,
            [
                tex(r"$P(B\mid A)=\dfrac{P(A\mid B)\,P(B)}{P(A)}$", 44),
                tex(r"$P(B_i\mid A)=\dfrac{P(A\mid B_i)\,P(B_i)}{\sum_k P(A\mid B_k)\,P(B_k)}$", 40),
            ],
            [
                texte("Bayes renverse la condition : de « A sachant B » vers « B sachant A »", 26, ["renverse la condition"]),
                texte("Le dénominateur vient des probabilités totales", 26, ["probabilités totales"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "Le réflexe en trois temps",
            ACCENT,
            [
                tex(r"\textbf{1.} Partitionner : $B_1,\dots,B_n$", 40, {r"\textbf{1.}": VERT}),
                tex(r"\textbf{2.} Totales : $P(A)=\sum_i P(A\mid B_i)\,P(B_i)$", 40, {r"\textbf{2.}": BLEU}),
                tex(r"\textbf{3.} Bayes : $P(B_i\mid A)=\dfrac{P(A\mid B_i)\,P(B_i)}{P(A)}$", 40, {r"\textbf{3.}": VIOLET}),
            ],
            [texte("Toujours dans cet ordre : c'est la meilleure façon de ne pas se tromper", 26, ["dans cet ordre"])],
        )

        # ── Démonstration 1 : le QCM (exercice 2.4.2) ─────────────────────────────
        racine = Dot(RACINE, radius=0.1, color=GRIS)
        racine.set_z_index(3)
        legende = self.legende("QCM à 4 réponses : l'étudiante connaît la réponse avec une probabilité de 0,3", ["0,3"])
        self.dezoom(carte, FadeIn(racine), FadeIn(legende))
        self.wait(1.5)

        n_k = noeud("Sait", VERT, POS["K"])
        n_n = noeud("Ignore", VIOLET, POS["N"])
        branche_k = Line(RACINE, POS["K"], stroke_color=GRIS, stroke_width=3)
        branche_n = Line(RACINE, POS["N"], stroke_color=GRIS, stroke_width=3)
        self.play(Create(branche_k), Create(branche_n),
                  FadeIn(etiquette_arete(RACINE, POS["K"], r"0{,}3")), FadeIn(etiquette_arete(RACINE, POS["N"], r"0{,}7")),
                  FadeIn(n_k, scale=0.6), FadeIn(n_n, scale=0.6))
        self.wait(2.5)

        legende = self.changer(legende, self.legende("Si elle sait : bonne réponse à coup sûr. Sinon elle répond au hasard : 1 chance sur 4", ["à coup sûr", "1 chance sur 4"]))
        feuilles = {"Kj": noeud("Juste", BLEU, POS["Kj"]), "Nj": noeud("Juste", BLEU, POS["Nj"]), "Nf": noeud("Faux", ROUGE, POS["Nf"])}
        liens = [("K", "Kj", r"1"), ("N", "Nj", r"\frac{1}{4}"), ("N", "Nf", r"\frac{3}{4}")]
        branches = [Line(POS[a], POS[b], stroke_color=GRIS, stroke_width=3) for a, b, _ in liens]
        etiquettes = [etiquette_arete(POS[a], POS[b], c) for a, b, c in liens]
        self.play(*[Create(b) for b in branches], *[FadeIn(e) for e in etiquettes], *[FadeIn(f, scale=0.6) for f in feuilles.values()])
        self.wait(2.5)

        legende = self.changer(legende, self.legende("Le long d'une branche, on multiplie", ["on multiplie"]))
        produits = {
            "Kj": Tex(r"$0{,}3\times 1=0{,}3$", font_size=34).move_to(POS["Kj"] + np.array([3.3, 0, 0])),
            "Nj": Tex(r"$0{,}7\times\dfrac{1}{4}=0{,}175$", font_size=34).move_to(POS["Nj"] + np.array([3.3, 0, 0])),
            "Nf": Tex(r"$0{,}7\times\dfrac{3}{4}=0{,}525$", font_size=34).move_to(POS["Nf"] + np.array([3.3, 0, 0])),
        }
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in produits.values()], lag_ratio=0.5), run_time=2.5)
        self.wait(3.0)

        legende = self.changer(legende, self.legende("Question : elle a donné la bonne réponse, a-t-elle vraiment su ? La condition est inversée : Bayes", ["Bayes"]))
        cadres = [SurroundingRectangle(VGroup(feuilles[c], produits[c]), color=ACCENT, buff=0.15, corner_radius=0.1, stroke_width=3)
                  for c in ("Kj", "Nj")]
        self.play(*[Create(c) for c in cadres])
        detail = self.detail(None, tex(r"$P(C)=1\times 0{,}3+\dfrac{1}{4}\times 0{,}7=0{,}3+0{,}175=0{,}475$", 40, {r"0{,}475": ACCENT}))
        legende = self.changer(legende, self.legende("Probabilités totales : les deux façons de répondre juste s'additionnent", ["Probabilités totales"]))
        self.wait(5.0)

        legende = self.changer(legende, self.legende("Bayes : la part « elle sait » parmi toutes les bonnes réponses", ["la part « elle sait »"]))
        detail = self.detail(detail, tex(r"$P(K\mid C)=\dfrac{P(C\mid K)\,P(K)}{P(C)}=\dfrac{0{,}3}{0{,}475}=\dfrac{12}{19}\approx 0{,}632$", 40, {r"0{,}632": ACCENT}))
        self.wait(5.5)
        self.vider(titre)

        # Le « pourquoi » : une barre des bonnes réponses
        largeur_sait = 10 * 0.3 / 0.475
        barre_sait = Rectangle(width=largeur_sait, height=1.2, stroke_color=VERT, stroke_width=3,
                               fill_color=teinte(VERT), fill_opacity=1).move_to([-5 + largeur_sait / 2, 0.6, 0])
        barre_hasard = Rectangle(width=10 - largeur_sait, height=1.2, stroke_color=GRIS, stroke_width=3,
                                 fill_color=teinte(GRIS, 0.4), fill_opacity=1).move_to([5 - (10 - largeur_sait) / 2, 0.6, 0])
        lab_sait = Tex(r"$0{,}3$", font_size=44).move_to(barre_sait.get_center())
        lab_hasard = Tex(r"$0{,}175$", font_size=44).move_to(barre_hasard.get_center())
        nom_sait = Text("elle savait", font_size=24, weight=BOLD, color=VERT).next_to(barre_sait, DOWN, buff=0.2)
        nom_hasard = Text("coup de chance", font_size=24, weight=BOLD, color=GRIS).next_to(barre_hasard, DOWN, buff=0.2)
        accolade = Brace(VGroup(barre_sait, barre_hasard), UP, color=ACCENT, buff=0.12)
        total = Tex(r"$P(C)=0{,}475$", font_size=40, color=ACCENT).next_to(accolade, UP, buff=0.12)
        legende = self.legende("Toutes les bonnes réponses : celles de l'étudiante qui savait, et celles dues au hasard", ["bonnes réponses"])
        self.play(Create(VGroup(barre_sait, barre_hasard)), FadeIn(lab_sait), FadeIn(lab_hasard), FadeIn(nom_sait), FadeIn(nom_hasard),
                  GrowFromCenter(accolade), FadeIn(total), FadeIn(legende))
        self.wait(3.0)
        legende = self.changer(legende, self.legende("Avant de voir la copie : 0,3. Après une bonne réponse : 0,63, mais jamais 1", ["0,63", "jamais 1"]))
        detail = self.detail(None, tex(r"$\dfrac{0{,}175}{0{,}475}\approx 37\,\%$ des bonnes réponses viennent du hasard", 42, {r"37\,\%": ACCENT}))
        self.play(Indicate(barre_hasard, color=ACCENT, scale_factor=1.0))
        self.wait(5.0)
        self.vider(titre)

        # ── Démonstration 2 : l'assurance (exercice 2.4.3) ──────────────────────────
        self.assurance(titre)
        self.fin()

    def assurance(self, titre):
        hauteur = 2.4
        bas = -0.8
        x = -5.0
        colonnes, rouges, noms, probas = [], [], [], []
        for nom, p, accident in CLASSES:
            largeur = 10 * p
            col = Rectangle(width=largeur, height=hauteur, stroke_color=GRIS, stroke_width=3, fill_color=FOND, fill_opacity=1)
            col.move_to([x + largeur / 2, bas + hauteur / 2, 0])
            rouge = Rectangle(width=largeur, height=hauteur * accident, stroke_width=0, fill_color=teinte(ROUGE, 0.6), fill_opacity=1)
            rouge.move_to([x + largeur / 2, bas + hauteur * accident / 2, 0])
            etiq = Tex(f"${nom}$ : ${str(p).replace('.', '{,}')}$", font_size=34).move_to([x + largeur / 2, bas + hauteur + 0.4, 0])
            colonnes.append(col)
            rouges.append(rouge)
            noms.append(etiq)
            x += largeur
        legende = self.legende("Une assurance classe ses clients en 3 niveaux de risque : 20 %, 50 % et 30 %", ["3 niveaux de risque"])
        self.play(*[Create(c) for c in colonnes], *[FadeIn(n) for n in noms], FadeIn(legende))
        detail = self.detail(None, tex(r"$P(R_1)+P(R_2)+P(R_3)=0{,}2+0{,}5+0{,}3=1$", 42))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Dans chaque classe, une part des clients a un accident dans l'année", ["a un accident"]))
        valeurs = [Tex(f"${str(a).replace('.', '{,}')}$", font_size=30, color=ROUGE).move_to([c.get_center()[0], bas - 0.35, 0])
                   for (_, _, a), c in zip(CLASSES, colonnes)]
        entete = Tex(r"$P(A\mid R_i)$", font_size=26, color=ROUGE).move_to([-5.9, bas - 0.35, 0])
        self.play(*[FadeIn(r) for r in rouges], *[FadeIn(v) for v in valeurs], FadeIn(entete))
        detail = self.detail(detail, tex(r"$P(A\mid R_1)=0{,}05\quad P(A\mid R_2)=0{,}15\quad P(A\mid R_3)=0{,}30$", 38))
        self.wait(4.5)

        legende = self.changer(legende, self.legende("Question 1 : probabilités totales, on additionne les trois zones rouges", ["probabilités totales"]))
        self.play(*[Indicate(r, color=ACCENT, scale_factor=1.0) for r in rouges])
        detail = self.detail(detail, tex(r"$P(A)=0{,}2\times 0{,}05+0{,}5\times 0{,}15+0{,}3\times 0{,}30=0{,}01+0{,}075+0{,}09=0{,}175$", 36, {r"0{,}175": ACCENT}))
        self.wait(6.0)

        legende = self.changer(legende, self.legende("Question 2 : M. Martin n'a pas eu d'accident. Dans quelle classe est-il ?", ["n'a pas eu d'accident"]))
        self.play(*[r.animate.set_opacity(0.15) for r in rouges])
        sans_accident = []
        for (nom, p, a), col in zip(CLASSES, colonnes):
            zone = Rectangle(width=col.width, height=hauteur * (1 - a), stroke_width=0, fill_color=teinte(GRIS, 0.35), fill_opacity=1)
            zone.move_to([col.get_center()[0], bas + hauteur * a + hauteur * (1 - a) / 2, 0])
            sans_accident.append(zone)
        self.play(*[FadeIn(z) for z in sans_accident])
        detail = self.detail(detail, tex(r"$P(\bar{A})=1-0{,}175=0{,}825$", 44))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Bayes : la zone « sans accident » de R1, rapportée à toutes les zones sans accident", ["Bayes"]))
        self.play(sans_accident[0].animate.set_fill(teinte(VERT, 0.6), opacity=1))
        detail = self.detail(detail, tex(r"$P(R_1\mid\bar{A})=\dfrac{0{,}95\times 0{,}2}{0{,}825}=\dfrac{0{,}19}{0{,}825}=\dfrac{38}{165}\approx 0{,}230$", 38, {r"0{,}230": ACCENT}))
        self.wait(6.0)

        legende = self.changer(legende, self.legende("Avant : 0,20. Après « pas d'accident » : 0,23. Cette information discrimine très peu", ["discrimine très peu"]))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("On calcule d'abord les intersections (les zones), puis Bayes se lit directement", ["les intersections"]))
        self.wait(4.0)
