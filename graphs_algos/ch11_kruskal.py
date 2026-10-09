from algo import *

LIGNES_KRUSKAL = [
    (0, "trier les arêtes par poids croissant"),
    (0, "T ← vide ; un sommet = une composante"),
    (0, "pour chaque arête e = {u, v} dans l'ordre :"),
    (1, "si u et v sont dans deux composantes :"),
    (2, "ajouter e à T ; fusionner les composantes"),
    (1, "sinon : e fermerait un cycle, on l'ignore"),
    (0, "arrêt dès que |T| = n − 1"),
]
PALETTE = [VERT, VIOLET, SOMMET, "#FB923C"]


class Kruskal(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "Arbre couvrant minimal",
            VERT,
            [
                tex(r"$w(T) = \displaystyle\sum_{e \in E'} w(e)$", 46),
                tex(r"$T^{*} = \underset{T \text{ arbre couvrant de } G}{\arg\min}\ w(T)$", 42),
            ],
            [
                tex(r"Graphe connexe pondéré : relier tous les sommets avec le moins de coût total", 32, {"moins de coût": VERT}),
                tex(r"Un arbre couvrant a $n - 1$ arêtes ; si les poids sont distincts, l'ACM est unique", 32, {"unique": VERT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        carte = self.carte(
            "Pourquoi ça marche : la propriété de coupe",
            VIOLET,
            [
                tex(r"$\delta(S) = \{\, \{u, v\} \in E \mid u \in S,\ v \notin S \,\}$", 42),
                tex(r"$e^{*} = \underset{e \in \delta(S)}{\arg\min}\ w(e) \ \Longrightarrow\ e^{*} \in T^{*}$", 42),
            ],
            [
                tex(r"Une coupe sépare les sommets en deux groupes $S$ et $V \setminus S$", 32, {"coupe": VIOLET}),
                tex(r"L'arête la plus légère qui traverse la coupe appartient toujours à un ACM", 32, {"plus légère": VIOLET}),
                tex(r"Symétriquement, la plus lourde arête d'un cycle n'est jamais utile", 32, {"plus lourde": ROUGE}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Le principe de Kruskal",
            ACCENT,
            [
                tex(r"$w(e_1) \leq w(e_2) \leq \dots \leq w(e_m)$", 44),
                tex(r"$T \leftarrow T \cup \{e_i\} \ \text{ si } \ T \cup \{e_i\} \text{ est acyclique}$", 42),
            ],
            [
                tex(r"On parcourt les arêtes par poids croissant", 32, {"poids croissant": ACCENT}),
                tex(r"On garde $e_i$ seulement si elle relie deux composantes différentes (sinon : cycle)", 32, {"deux composantes différentes": VERT}),
                tex(r"Arrêt dès que $T$ a $n - 1$ arêtes ; complexité $O(m \log m)$, dominée par le tri", 32, {"O(m log m)": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Arbre couvrant minimal : Kruskal", 11)

        g = creer_graphe(SOMMETS_M, [(u, v) for u, v, _ in ARETES_M], POS_M)
        legende = self.legende("Relier tous les sommets au moindre coût", ["moindre coût"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        poids = VGroup(*[etiquette_poids(g, u, v, w) for u, v, w in ARETES_M])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in poids], lag_ratio=0.15))
        self.wait(1)

        legende = self.changer(
            legende, self.legende("L'algorithme : un pseudo-code, une liste triée, des composantes", ["pseudo-code", "liste triée", "composantes"])
        )
        code = PanneauCode("Kruskal(G, w)", LIGNES_KRUSKAL, coin=(0.35, 2.25))
        self.play(*code.montrer(), run_time=1.5)
        self.det = self.detail(
            None, "Graphe connexe pondéré à 6 sommets : l'arbre couvrant minimal aura n − 1 = 5 arêtes", ["n − 1 = 5"]
        )
        self.wait(4)
        legende = self.changer(
            legende,
            self.legende(
                "Jaune épais : dans T · Rouge : écartée · Même couleur : même composante",
                {"Jaune": ACCENT, "Rouge": ROUGE},
            ),
        )

        tri, boites, texte_comp = self.preparer(code)
        retenues = self.executer(g, code, tri, boites, texte_comp)
        self.conclure(g, code, retenues, poids)
        self.fin(3)

    # ---------- outils ----------
    def dire(self, contenu, cles=None):
        self.det = self.detail(self.det, contenu, cles)

    def preparer(self, code):
        """Tri des arêtes + affichage de la liste triée et des composantes initiales."""
        tri = sorted(ARETES_M, key=lambda e: (e[2], e[0], e[1]))
        boites = [boite_arete(u, v, w) for u, v, w in tri]
        for i, boite in enumerate(boites):
            boite.move_to([0.95 + i * 0.72, -1.75, 0])
        self.dire(
            "On commence par trier les 9 arêtes par poids croissant : C–F (2), D–E (3), A–B (4)…",
            ["trier", "poids croissant"],
        )
        self.play(code.aller_a(0), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boites], lag_ratio=0.15))
        self.wait(3)
        texte_comp = Text(
            "Composantes : {A}  {B}  {C}  {D}  {E}  {F}", font_size=24, color=TEXTE
        ).scale_to_fit_width(6.2).move_to([3.7, -0.9, 0])
        self.dire("Au départ, chaque sommet est seul dans sa composante : 6 composantes", ["6 composantes"])
        self.play(code.aller_a(1), FadeIn(texte_comp, shift=UP * 0.15))
        self.wait(3)
        return tri, boites, texte_comp

    def texte_composantes(self, uf, ancien):
        groupes = {}
        for x in SOMMETS_M:
            groupes.setdefault(uf(x), []).append(x)
        morceaux = [
            "{" + ", ".join(sorted(m)) + "}" for m in sorted(groupes.values(), key=lambda m: sorted(m)[0])
        ]
        nouveau = Text("Composantes : " + "  ".join(morceaux), font_size=24, color=TEXTE)
        if nouveau.width > 6.2:
            nouveau.scale_to_fit_width(6.2)
        return nouveau.move_to(ancien)

    # ---------- exécution pas à pas ----------
    def executer(self, g, code, tri, boites, texte_comp):
        pere = {x: x for x in SOMMETS_M}

        def trouver(x):
            while pere[x] != x:
                x = pere[x]
            return x

        couleurs = {}
        palette = list(PALETTE)
        retenues = []
        for i, (u, v, w) in enumerate(tri):
            boite = boites[i]
            self.dire(
                f"On examine {u}{v} (poids {w}) : {u} et {v} sont-ils déjà dans la même composante ?",
                [f"{u}{v} (poids {w})"],
            )
            self.play(
                code.aller_a(2),
                boite[0].animate.set_stroke(color=ACCENT, width=6),
                Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0),
            )
            self.wait(1.2)
            self.play(code.aller_a(3), run_time=0.7)
            ru, rv = trouver(u), trouver(v)
            if ru != rv:
                self.dire(
                    f"Composantes différentes : {u}{v} ne ferme aucun cycle, on la garde et on fusionne",
                    {"on la garde": VERT, "fusionne": VERT},
                )
                self.wait(1.2)
                couleur = couleurs.get(ru) or couleurs.get(rv) or palette.pop(0)
                pere[rv] = ru
                couleurs[ru] = couleur
                membres = [x for x in SOMMETS_M if trouver(x) == ru]
                retenues.append((u, v, w))
                self.play(
                    code.aller_a(4),
                    arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=9),
                    *[colorier(g, x, couleur) for x in membres],
                    boite[0].animate.set_stroke(color=VERT, width=6),
                )
                nouveau = self.texte_composantes(trouver, texte_comp)
                self.play(Transform(texte_comp, nouveau))
                self.wait(1.5)
                if len(retenues) == len(SOMMETS_M) - 1:
                    self.play(code.aller_a(6))
                    self.dire(
                        f"{len(retenues)} arêtes retenues = n − 1 : l'arbre est complet, on s'arrête",
                        [f"n − 1", "on s'arrête"],
                    )
                    self.wait(3.5)
                    return retenues
            else:
                self.dire(
                    f"Même composante : {u}{v} fermerait un cycle, on l'ignore",
                    {"fermerait un cycle": ROUGE, "on l'ignore": ROUGE},
                )
                self.wait(1.2)
                self.play(
                    code.aller_a(5),
                    arete(g, u, v).animate.set_stroke(color=ROUGE, width=4, opacity=0.6),
                    boite[0].animate.set_stroke(color=ROUGE, width=6),
                )
                self.play(Indicate(g.vertices[u], color=ROUGE), Indicate(g.vertices[v], color=ROUGE))
                self.wait(2.5)
        return retenues

    # ---------- bilan ----------
    def conclure(self, g, code, retenues, poids):
        total = sum(w for _, _, w in retenues)
        somme = " + ".join(str(w) for _, _, w in retenues)
        self.dire(
            f"Poids de l'arbre couvrant minimal : w(T) = {somme} = {total}",
            [f"w(T) = {somme} = {total}"],
        )
        retenues_cles = {frozenset((u, v)) for u, v, _ in retenues}
        autres = [
            arete(g, u, v) for u, v, _ in ARETES_M if frozenset((u, v)) not in retenues_cles
        ]
        self.play(*[e.animate.set_stroke(opacity=0.25) for e in autres], FadeOut(poids))
        self.wait(4)

        # propriété de coupe, sur la dernière arête retenue (C–D)
        self.dire(
            "Pourquoi C–D (7) est sûre : c'est la plus légère arête qui traverse cette coupe",
            ["plus légère", "coupe"],
        )
        gauche, droite = "ABCF", "DE"
        self.play(
            *[colorier(g, x, SOMMET) for x in gauche],
            *[colorier(g, x, VIOLET) for x in droite],
            *[e.animate.set_stroke(opacity=1) for e in autres],
        )
        traversent = [("E", "F"), ("B", "D")]  # C–D reste en jaune : c'est l'arête minimale
        self.play(
            *[arete(g, u, v).animate.set_color(SOMMET).set_stroke(width=7) for u, v in traversent],
        )
        self.wait(3.5)
        self.dire(
            "Les arêtes de la coupe : C–D (7), E–F (8) et B–D (10) ; la moins chère, C–D, est dans l'ACM",
            ["C–D (7)", "E–F (8)", "B–D (10)"],
        )
        self.play(Indicate(arete(g, "C", "D"), color=ACCENT, scale_factor=1.0))
        self.wait(5)
        self.dire(
            "Kruskal applique cette propriété à chaque étape : le coût total reste O(m log m), celui du tri",
            ["O(m log m)"],
        )
        self.wait(5)
        self.play(*code.cacher())
