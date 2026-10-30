"""Chapitre 5 : tirages dans une urne, simultanés ou successifs avec remise (exercice 2.3.5)."""
from common import *
from proba import *

# 6 pièces bleues, 7 vertes, 5 jaunes (18 au total)
COMPOSITION = [BLEU] * 6 + [VERT] * 7 + [ACCENT] * 5

# Arbre des deux tirages avec remise : B = bleue, « B barre » = pas bleue
RACINE = np.array([-4.6, 0.4, 0])
NIVEAU_1 = {"B": np.array([-1.6, 1.45, 0]), "N": np.array([-1.6, -0.7, 0])}
FEUILLES = {
    "BB": np.array([1.2, 2.0, 0]),
    "BN": np.array([1.2, 0.9, 0]),
    "NB": np.array([1.2, -0.15, 0]),
    "NN": np.array([1.2, -1.2, 0]),
}
PRODUITS = {
    "BB": r"\dfrac{6\times 6}{18\times 18}",
    "BN": r"\dfrac{6\times 12}{18\times 18}",
    "NB": r"\dfrac{12\times 6}{18\times 18}",
    "NN": r"\dfrac{12\times 12}{18\times 18}",
}


def jeton(lettre, rayon=0.26):
    """Pastille « bleue » (B) ou « pas bleue » (B barre) d'un nœud de l'arbre."""
    if lettre == "B":
        fond, contenu = BLEU, Text("B", font_size=22, weight=BOLD, color=FOND)
    else:
        fond, contenu = GRIS, Tex(r"$\bar{B}$", font_size=30, color=FOND)
    disque_ = Circle(radius=rayon, stroke_width=0, fill_color=fond, fill_opacity=1)
    groupe = VGroup(disque_, contenu)
    groupe.set_z_index(3)
    return groupe


def etiquette_arete(depart, arrivee, fraction):
    """Fraction affichée au milieu d'une branche, sur un fond noir qui masque le trait."""
    t = Tex(f"${fraction}$", font_size=28, color=ACCENT)
    fond = BackgroundRectangle(t, color=FOND, fill_opacity=1, buff=0.05)
    groupe = VGroup(fond, t).move_to((depart + arrivee) / 2)
    groupe.set_z_index(2)
    return groupe


class Chapitre05(SceneProbas):
    def construct(self):
        titre = self.intro("Tirages dans une urne", 5)

        # ── Théorie ─────────────────────────────────────────────────────────
        carte = self.carte(
            "Tirage simultané de p objets parmi n",
            ACCENT,
            [tex(r"$\dfrac{n\,(n-1)\cdots(n-p+1)}{p\,(p-1)\cdots 2\times 1}$", 48)],
            [
                texte("C'est le nombre de tirages possibles, écrit sans la notation C(n, p)", 26, ["nombre de tirages possibles"]),
                texte("L'ordre ne compte pas : on divise par les façons de ranger les p objets", 26, ["L'ordre ne compte pas"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "Tirages successifs avec remise",
            ACCENT,
            [
                tex(r"$P(E_1\text{ puis }E_2)=P(E_1)\times P(E_2)$", 42),
                tex(r"$P(\text{cas 1 ou cas 2})=P(\text{cas 1})+P(\text{cas 2})$", 42),
            ],
            [
                texte("Avec remise, l'urne retrouve sa composition : les tirages sont indépendants", 26, ["indépendants"]),
                texte("Chaque façon d'obtenir le résultat est un cas : on multiplie le long d'une branche", 26, ["on multiplie"]),
                texte("Puis on additionne les cas qui s'excluent", 26, ["on additionne"]),
            ],
        )

        # ── Démonstration 1 : tirage simultané ─────────────────────────────────
        cadre, boules = urne(COMPOSITION, (-3.4, 0.55))
        compte = texte("6 bleues, 7 vertes, 5 jaunes", 24, {"6 bleues": BLEU, "7 vertes": VERT, "5 jaunes": ACCENT})
        compte.next_to(cadre, DOWN, buff=0.25)
        legende = self.legende("Une urne contient 18 pièces : 6 bleues, 7 vertes et 5 jaunes", ["18 pièces"])
        self.dezoom(
            carte,
            Create(cadre), LaggedStart(*[GrowFromCenter(b) for b in boules], lag_ratio=0.05), FadeIn(compte), FadeIn(legende),
        )
        self.wait(2.0)

        legende = self.changer(legende, self.legende("On tire 2 pièces d'un coup : quelle probabilité d'avoir au moins une jaune ?", ["au moins une jaune"]))
        zone = RoundedRectangle(width=3.6, height=1.5, corner_radius=0.2, stroke_color=GRIS, stroke_width=3).move_to([3.6, 0.55, 0])
        nom_zone = texte("tirage simultané", 22, {"tirage simultané": GRIS}).next_to(zone, UP, buff=0.12)
        jaunes = [b for b in boules if b.couleur_base == ACCENT]
        bleues = [b for b in boules if b.couleur_base == BLEU]
        tirees = [jaunes[0].copy(), bleues[0].copy()]
        self.play(Create(zone), FadeIn(nom_zone))
        self.play(tirees[0].animate.move_to([3.1, 0.55, 0]), tirees[1].animate.move_to([4.1, 0.55, 0]), run_time=1.6)
        self.wait(2.0)
        self.play(FadeOut(tirees[0]), FadeOut(tirees[1]))

        legende = self.changer(legende, self.legende("Plus simple par le contraire : « aucune jaune », donc 2 pièces parmi les 13 autres", ["aucune jaune", "13 autres"]))
        self.play(*[b.animate.set_opacity(0.15) for b in jaunes])
        detail = self.detail(None, tex(r"$13=6+7$ pièces non jaunes sur $18$", 42))
        self.wait(3.5)

        legende = self.changer(legende, self.legende("Tirages possibles : 18 × 17 divisé par 2 ; sans jaune : 13 × 12 divisé par 2", ["18 × 17", "13 × 12"]))
        detail = self.detail(detail, tex(r"$P(\text{aucune jaune})=\dfrac{13\times 12\,/\,2}{18\times 17\,/\,2}=\dfrac{13\times 12}{18\times 17}=\dfrac{156}{306}$", 40))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Les « divisé par 2 » se simplifient : l'ordre n'intervient pas dans le rapport", ["se simplifient"]))
        self.wait(3.0)

        self.play(*[b.animate.set_opacity(1.0) for b in jaunes])
        legende = self.changer(legende, self.legende("Au moins une jaune : tout sauf « aucune jaune »", ["Au moins une jaune"]))
        detail = self.detail(detail, tex(r"$P(\text{au moins une jaune})=1-\dfrac{156}{306}=\dfrac{150}{306}\approx 0{,}490$", 40, {r"0{,}490": ACCENT}))
        self.wait(5.0)
        self.vider(titre)

        # ── Démonstration 2 : tirages successifs avec remise ───────────────────────
        self.arbre(titre)
        self.fin()

    def arbre(self, titre):
        legende = self.legende("Deux tirages successifs avec remise : exactement une pièce bleue ?", ["exactement une pièce bleue"])
        self.play(FadeIn(legende))
        racine = Dot(RACINE, radius=0.1, color=GRIS)
        racine.set_z_index(3)
        self.play(FadeIn(racine))

        aretes, etiquettes = {}, {}
        noeuds = {cle: jeton(cle).move_to(pos) for cle, pos in NIVEAU_1.items()}
        fractions = {"B": r"\frac{6}{18}", "N": r"\frac{12}{18}"}

        legende = self.changer(legende, self.legende("1er tirage : bleue avec 6 chances sur 18, pas bleue avec 12 sur 18", ["6 chances sur 18", "12 sur 18"]))
        for cle in "BN":
            aretes[cle] = Line(RACINE, NIVEAU_1[cle], stroke_color=GRIS, stroke_width=3)
            etiquettes[cle] = etiquette_arete(RACINE, NIVEAU_1[cle], fractions[cle])
        self.play(*[Create(aretes[c]) for c in "BN"], *[FadeIn(etiquettes[c]) for c in "BN"],
                  *[FadeIn(noeuds[c], scale=0.5) for c in "BN"])
        self.wait(2.5)

        legende = self.changer(legende, self.legende("La pièce est remise : le 2e tirage a exactement les mêmes chances", ["remise"]))
        feuilles, branches, fractions_2 = {}, [], []
        for cle, pos in FEUILLES.items():
            parent = NIVEAU_1[cle[0]]
            branches.append(Line(parent, pos, stroke_color=GRIS, stroke_width=3))
            fractions_2.append(etiquette_arete(parent, pos, fractions[cle[1]]))
            feuilles[cle] = VGroup(jeton(cle[0]), jeton(cle[1])).arrange(RIGHT, buff=0.1).move_to(pos + RIGHT * 0.45)
        self.play(*[Create(b) for b in branches], *[FadeIn(f) for f in fractions_2], *[FadeIn(f, scale=0.5) for f in feuilles.values()])
        self.wait(2.5)

        legende = self.changer(legende, self.legende("Le long d'une branche, on multiplie : chaque tirage est indépendant", ["on multiplie"]))
        produits = {
            cle: Tex(f"${expr}$", font_size=34).move_to(pos + np.array([3.3, 0, 0]))
            for (cle, expr), pos in zip(PRODUITS.items(), FEUILLES.values())
        }
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in produits.values()], lag_ratio=0.4), run_time=3.0)
        self.wait(3.0)

        legende = self.changer(legende, self.legende("Exactement une bleue : bleue puis pas bleue, OU pas bleue puis bleue", ["OU"]))
        cadres = [SurroundingRectangle(VGroup(feuilles[c], produits[c]), color=ACCENT, buff=0.15, corner_radius=0.1, stroke_width=3)
                  for c in ("BN", "NB")]
        self.play(*[Create(c) for c in cadres])
        detail = self.detail(None, tex(r"$\dfrac{6\times 12}{18\times 18}+\dfrac{12\times 6}{18\times 18}$", 44))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Les deux cas sont égaux : le « 2 × » vient des deux places possibles de la bleue", ["« 2 × »"]))
        detail = self.detail(detail, tex(r"$P=2\times\dfrac{6\times 12}{18\times 18}=\dfrac{144}{324}\approx 0{,}444$", 44, {r"2\times": ACCENT}))
        self.wait(5.0)

        legende = self.changer(legende, self.legende("C'est l'embryon de la loi binomiale : ce 2 compte les places d'un succès parmi 2 tirages", ["loi binomiale"]))
        detail = self.detail(detail, tex(r"$P(X=k)=C_n^k\,p^k(1-p)^{n-k}\quad\text{ici}\quad C_2^1=2$", 42, {r"C_2^1=2": ACCENT}))
        self.wait(6.0)
