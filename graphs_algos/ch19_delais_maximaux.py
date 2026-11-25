"""Chapitre 19 : délais maximaux, arcs négatifs et plus long chemin avec Bellman-Ford (TD2, exercice 7, questions 3 et 4)."""
from ordonnancement import *

# Deux contraintes de délai maximal : la fin de G (resp. H) ne dépasse pas le début de E de plus de 15 (resp. 11)
SUPPLEMENTS = [("G", "E", 7 - 15), ("H", "E", 4 - 11)]
TOUS_LES_ARCS = [(a, b, LONGUEUR[(a, b)]) for a, b in ARCS] + SUPPLEMENTS
MOINS_INF = None  # valeur « −∞ » : pas encore de date connue


def texte_date(v):
    return "−∞" if v is MOINS_INF else str(v)


class DelaisMaximaux(SceneGraphes):
    # ---------- théorie ----------
    def theorie(self):
        carte = self.carte(
            "Une contrainte de temps devient un arc",
            SOMMET,
            [
                tex(r"$t_j-t_i\geq\alpha_{ij}\;\Longleftrightarrow\;$ arc $i\to j$ de longueur $\alpha_{ij}$", 38, {r"\alpha_{ij}": ACCENT}),
                tex(r"$t_i+d_i\leq t_j+\delta\;\Longleftrightarrow\;t_j-t_i\geq d_i-\delta$", 40, {r"d_i-\delta": VIOLET}),
            ],
            [
                texte("Précédence : l'arc part de i vers j avec la durée de i", 26, ["Précédence"]),
                texte("Délai maximal δ : la fin de i ne dépasse pas le début de j de plus de δ", 26, ["Délai maximal δ"]),
                texte("La longueur de l'arc est alors la durée de i moins δ : souvent négative", 26, ["négative"]),
            ],
        )
        self.play(FadeOut(carte))
        return self.carte(
            "Plus long chemin : Bellman-Ford avec un maximum",
            VERT,
            [
                tex(r"$t_j\leftarrow\max\,(t_j,\;t_i+\alpha_{ij})$", 46),
                tex(r"au plus $n-1$ passages sur tous les arcs", 40, {r"n-1": ACCENT}),
            ],
            [
                texte("Comme Bellman-Ford, mais avec un maximum : on part de −∞, sauf t(α) = 0", 26, ["maximum"]),
                texte("Une amélioration encore possible au n-ième passage : circuit de longueur positive", 26, ["circuit de longueur positive"]),
                texte("Dans ce cas, les contraintes sont incompatibles : le projet est infaisable", 26, ["infaisable"]),
            ],
        )

    # ---------- exécution ----------
    def executer(self, g, arcs, legende, detail):
        t = {v: MOINS_INF for v in SOMMETS}
        t["α"] = 0
        labels = {v: date_label(g.vertices[v], texte_date(t[v]), bas=v in BAS) for v in SOMMETS}
        for v in SOMMETS:
            labels[v].set_color(ARETE)
        labels["α"].set_color(ACCENT)
        legende = self.changer(legende, self.legende("On part de −∞ partout, sauf à α où la date vaut 0", ["−∞", "0"]))
        self.play(*[FadeIn(l, scale=0.8) for l in labels.values()], colorier(g, "α", ACCENT))
        self.wait(3.0)

        n = len(SOMMETS)
        passage = 0
        while True:
            passage += 1
            legende = self.changer(legende, self.legende(f"Passage {passage} : on examine tous les arcs, un par un", [f"Passage {passage}"]))
            modifie = False
            for (u, v, w) in TOUS_LES_ARCS:
                if t[u] is MOINS_INF:
                    continue
                candidat = t[u] + w
                if t[v] is MOINS_INF or candidat > t[v]:
                    ancien = t[v]
                    t[v] = candidat
                    modifie = True
                    anc = r"-\infty" if ancien is MOINS_INF else str(ancien)
                    signe = f"{w}" if w >= 0 else f"({w})"
                    formule = rf"$t_{nom_tex(v)}=\max({anc},\;t_{nom_tex(u)}+{signe})=\max({anc},\;{candidat})={candidat}$"
                    detail = self.detail(detail, tex(formule, 40))
                    nouveau = date_label(g.vertices[v], candidat, bas=v in BAS)
                    animations = [Indicate(arcs[(u, v)], color=ACCENT, scale_factor=1.0), Transform(labels[v], nouveau)]
                    if ancien is MOINS_INF:
                        animations.append(colorier(g, v, ACCENT))
                    self.play(*animations, run_time=1.1)
                    labels[v].set_color(ACCENT)
                    self.wait(1.3)
            if not modifie:
                break
            if passage >= n:
                break
        detail = self.detail(detail, f"Passage {passage} : plus aucune amélioration, les dates sont définitives", [f"Passage {passage}"])
        self.play(LaggedStart(*[Indicate(a, color=ACCENT, scale_factor=1.0) for a in arcs.values()], lag_ratio=0.05), run_time=2.5)
        self.wait(3.0)
        return t, detail, legende

    # ---------- cas infaisable ----------
    def infaisable(self, titre):
        e = LabeledDot(Text("E", font_size=30, color=FOND, weight=BOLD), radius=0.32, fill_color=NOEUD).move_to([-2.5, 0.4, 0])
        gg = LabeledDot(Text("G", font_size=30, color=FOND, weight=BOLD), radius=0.32, fill_color=NOEUD).move_to([2.5, 0.4, 0])
        aller = arc_entre(e.get_center(), gg.get_center(), angle=0.35, couleur=LIEN, rayon=0.32)
        retour = arc_entre(gg.get_center(), e.get_center(), angle=0.35, couleur=VIOLET, rayon=0.32)
        lab_aller = etiquette_longueur(aller, 6)
        lab_retour = etiquette_longueur(retour, 2, couleur=VIOLET)
        legende = self.legende("Et si la fin de G devait dépasser le début de E de 5 au plus, au lieu de 15 ?", ["5 au plus"])
        self.play(GrowFromCenter(e), GrowFromCenter(gg), FadeIn(legende))
        self.play(Create(aller), FadeIn(lab_aller))
        detail = self.detail(None, tex(r"$t_G+7\leq t_E+5\;\Longleftrightarrow\;t_E-t_G\geq 7-5=2$", 44, {r"2": VIOLET}))
        self.play(Create(retour), FadeIn(lab_retour))
        self.wait(4.5)

        legende = self.changer(legende, self.legende("Le circuit E, G, E a une longueur positive : 6 + 2 = 8", ["longueur positive"]))
        detail = self.detail(detail, tex(r"$6+2=8>0$", 52, {r"8": ROUGE}))
        self.wait(3.5)
        legende = self.changer(legende, self.legende("Chaque tour repousse E de 8 de plus : les dates augmentent sans fin", ["sans fin"]))
        valeur = Text("t(E) = 0", font_size=28, color=ACCENT, weight=BOLD).next_to(e, UP, buff=0.2)
        self.play(FadeIn(valeur))
        for k in (8, 16, 24, 32):
            nouveau = Text(f"t(E) = {k}", font_size=28, color=ACCENT, weight=BOLD).move_to(valeur)
            self.play(FadeOut(valeur), FadeIn(nouveau),
                      Indicate(aller, color=ACCENT, scale_factor=1.0), Indicate(retour, color=VIOLET, scale_factor=1.0), run_time=1.3)
            valeur = nouveau
            self.wait(0.6)
        detail = self.detail(detail, "Au n-ième passage, une date s'améliore encore : Bellman-Ford le détecte", ["Bellman-Ford le détecte"])
        self.wait(4.0)
        legende = self.changer(legende, self.legende("Faisable si et seulement si aucun circuit n'a une longueur strictement positive", ["aucun circuit"]))
        self.wait(5.0)

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Délais maximaux et plus long chemin", 19)
        carte = self.theorie()

        g = creer_graphe(SOMMETS, ARCS, POS, orientee=True, rayon=0.3)
        arcs = {k: arete(g, *k) for k in ARCS}
        etiquettes = {k: etiquette_longueur(arcs[k], LONGUEUR[k], p=PROPORTION.get(k, 0.5)) for k in ARCS}
        legende = self.legende("Le graphe du chapitre précédent : sans contrainte de délai, la durée minimale est 22", ["22"])
        self.dezoom(
            carte,
            Succession(
                LaggedStart(*[GrowFromCenter(v) for v in g.vertices.values()], lag_ratio=0.1),
                LaggedStart(*[Create(a) for a in arcs.values()], *[FadeIn(e) for e in etiquettes.values()], lag_ratio=0.05),
            ),
            FadeIn(legende),
        )
        self.wait(2.5)

        # les deux contraintes de délai maximal
        legende = self.changer(legende, self.legende("Contrainte 1 : la fin de G ne doit pas dépasser le début de E de plus de 15", ["Contrainte 1"]))
        detail = self.detail(None, tex(r"$t_G+7\leq t_E+15\;\Longleftrightarrow\;t_E-t_G\geq 7-15=-8$", 42, {r"-8": VIOLET}))
        sup = {}
        for u, v, w in SUPPLEMENTS:
            courbe = arc_entre(g.vertices[u].get_center(), g.vertices[v].get_center(), angle=0.5, couleur=VIOLET, rayon=0.3)
            sup[(u, v)] = (courbe, etiquette_longueur(courbe, w, couleur=VIOLET))
        self.play(Create(sup[("G", "E")][0]), FadeIn(sup[("G", "E")][1]))
        self.wait(4.5)
        legende = self.changer(legende, self.legende("Contrainte 2 : la fin de H ne doit pas dépasser le début de E de plus de 11", ["Contrainte 2"]))
        detail = self.detail(detail, tex(r"$t_H+4\leq t_E+11\;\Longleftrightarrow\;t_E-t_H\geq 4-11=-7$", 42, {r"-7": VIOLET}))
        self.play(Create(sup[("H", "E")][0]), FadeIn(sup[("H", "E")][1]))
        self.wait(4.5)

        legende = self.changer(legende, self.legende("Il y a maintenant des arcs négatifs et des circuits : on utilise Bellman-Ford avec un maximum", ["Bellman-Ford"]))
        detail = self.detail(detail, tex(r"$E\to G\to E:\ 6+(-8)=-2\qquad E\to H\to E:\ 6+(-7)=-1$", 42))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Ces circuits sont de longueur négative : aucun problème", ["longueur négative"]))
        self.wait(3.0)

        arcs_tous = dict(arcs)
        for k, (courbe, _) in sup.items():
            arcs_tous[k] = courbe
        t, detail, legende = self.executer(g, arcs_tous, legende, detail)

        legende = self.changer(legende, self.legende("Résultat : E ne peut plus démarrer à 4, il doit attendre la date 8", ["E", "8"]))
        detail = self.detail(detail, tex(r"$t_E=8\ (\text{au lieu de }4)\qquad t_\omega=22$", 46, {r"t_E=8": VIOLET}))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Les contraintes sont respectées et la durée minimale reste 22 unités de temps", ["22 unités de temps"]))
        detail = self.detail(detail, tex(r"$t_G+7=22\leq t_E+15=23\qquad t_H+4=19\leq t_E+11=19$", 40))
        self.wait(6.0)
        self.vider(titre)
        self.infaisable(titre)
        self.fin()
