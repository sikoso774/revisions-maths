from algo import *

LIGNES_PRIM = [
    (0, "S ← {s} ; T ← vide"),
    (0, "tant que S ≠ V :"),
    (1, "e = {u,v} ← arête minimale sortant de S"),
    (1, "ajouter e à T"),
    (1, "ajouter v à S"),
]


class Prim(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "Le principe de Prim",
            ACCENT,
            [
                tex(r"$S_0 = \{s\} \qquad T_0 = \emptyset$", 44),
                tex(r"$e_k = \underset{e \in \delta(S_k)}{\arg\min}\ w(e) = \{u, v\} \qquad S_{k+1} = S_k \cup \{v\}$", 40),
            ],
            [
                tex(r"On fait grossir un seul arbre depuis $s$ : à chaque tour, on ajoute l'arête la moins chère qui en sort", 30, {"un seul arbre": ACCENT, "moins chère": VERT}),
                tex(r"C'est la propriété de coupe, appliquée à la coupe $(S_k, V \setminus S_k)$", 32, {"propriété de coupe": VIOLET}),
                tex(r"Même squelette que Dijkstra, mais on compare $w(u, v)$ et non $d[u] + w(u, v)$", 32, {"Dijkstra": SOMMET}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Complexité",
            VERT,
            [tex(r"$T(n, m) = O(m \log n)$", 50)],
            [
                tex(r"Un tas binaire garde les arêtes candidates triées par poids", 32, {"tas binaire": VIOLET}),
                tex(r"Avec une matrice d'adjacence et sans tas : $O(n^2)$, pratique pour les graphes denses", 32, {"denses": VERT}),
                tex(r"Kruskal en $O(m \log m)$, Prim en $O(m \log n)$ : équivalents, car $\log m \leq 2 \log n$", 32, {"équivalents": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Arbre couvrant minimal : Prim", 12)

        g = creer_graphe(SOMMETS_M, [(u, v) for u, v, _ in ARETES_M], POS_M)
        legende = self.legende("Faire grossir un arbre depuis un sommet", ["faire grossir un arbre"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        poids = VGroup(*[etiquette_poids(g, u, v, w) for u, v, w in ARETES_M])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in poids], lag_ratio=0.15))
        self.wait(1)

        legende = self.changer(
            legende, self.legende("L'algorithme : un pseudo-code et les arêtes qui sortent de S", ["pseudo-code", "sortent de S"])
        )
        code = PanneauCode("Prim(G, w, s)", LIGNES_PRIM, coin=(0.35, 2.25))
        self.play(*code.montrer(), run_time=1.5)
        self.det = self.detail(
            None, "Même graphe qu'avec Kruskal ; on part de la source s = A", ["s = A"]
        )
        self.wait(3.5)
        legende = self.changer(
            legende,
            self.legende(
                "Vert : dans S · Bleu : arêtes de la coupe · Jaune épais : dans T",
                {"Vert": VERT, "Bleu": SOMMET, "Jaune": ACCENT},
            ),
        )

        retenues = self.executer(g, code)
        self.conclure(g, code, retenues, poids)
        self.comparer(legende, titre)
        self.fin(3)

    # ---------- outils ----------
    def dire(self, contenu, cles=None):
        self.det = self.detail(self.det, contenu, cles)

    # ---------- exécution pas à pas ----------
    def executer(self, g, code):
        dans_s = {"A"}
        retenues = []
        total = 0

        def affiche_s():
            noms = ", ".join(sorted(dans_s))
            return tex(rf"$S = \{{{noms}\}}$", 36).move_to([3.7, -1.55, 0])

        def affiche_total():
            if retenues:
                somme = " + ".join(str(w) for _, _, w in retenues)
                return tex(rf"$w(T) = {somme} = {total}$", 34).move_to([3.7, -2.0, 0])
            return tex(r"$w(T) = 0$", 34).move_to([3.7, -2.0, 0])

        texte_s = affiche_s()
        texte_total = affiche_total()
        self.dire("On démarre avec S = {A} et T vide : A est le premier sommet de l'arbre", ["S = {A}"])
        self.play(code.aller_a(0), colorier(g, "A", VERT), FadeIn(texte_s), FadeIn(texte_total))
        self.wait(3)

        while len(dans_s) < len(SOMMETS_M):
            self.play(code.aller_a(1))
            candidates = sorted(
                [(w, u, v) for u, v, w in ARETES_M if (u in dans_s) != (v in dans_s)],
                key=lambda e: (e[0], e[1], e[2]),
            )
            liste = ", ".join(f"{u}{v} ({w})" for w, u, v in candidates)
            self.dire(
                f"Les arêtes qui sortent de S (la coupe) : {liste}",
                ["sortent de S"],
            )
            boites = VGroup(*[boite_arete(u, v, w) for w, u, v in candidates])
            for i, boite in enumerate(boites):
                boite.move_to([0.95 + i * 0.72, -0.8, 0])
            etiquette = Text("Arêtes de la coupe", font_size=20, color=SOMMET, weight=BOLD).move_to([3.7, -0.12, 0])
            self.play(
                *[arete(g, u, v).animate.set_color(SOMMET).set_stroke(width=7) for w, u, v in candidates],
                LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boites], lag_ratio=0.15),
                FadeIn(etiquette),
            )
            self.wait(3)

            w, u, v = candidates[0]
            nouveau = v if u in dans_s else u
            self.dire(
                f"La moins chère est {u}{v} (poids {w}) : elle relie S à {nouveau}",
                [f"{u}{v} (poids {w})", "moins chère"],
            )
            self.play(
                code.aller_a(2),
                boites[0][0].animate.set_stroke(color=ACCENT, width=6),
                Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0),
            )
            self.wait(2)

            retenues.append((u, v, w))
            total += w
            self.dire(f"On l'ajoute à T : {u}{v} rejoint l'arbre", ["à T"])
            self.play(
                code.aller_a(3),
                arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=9),
                *[
                    arete(g, a, b).animate.set_color(LIEN).set_stroke(width=5)
                    for ww, a, b in candidates[1:]
                ],
                boites[0][0].animate.set_stroke(color=VERT, width=6),
            )
            self.wait(1.5)

            dans_s.add(nouveau)
            self.dire(f"Et {nouveau} entre dans S : la coupe change, on recommence", [f"{nouveau} entre dans S"])
            nouveau_s, nouveau_total = affiche_s(), affiche_total()
            self.play(
                code.aller_a(4),
                colorier(g, nouveau, VERT),
                Transform(texte_s, nouveau_s),
                Transform(texte_total, nouveau_total),
                FadeOut(boites),
                FadeOut(etiquette),
            )
            self.wait(2)
        self.play(code.aller_a(1))
        return retenues

    # ---------- bilan ----------
    def conclure(self, g, code, retenues, poids):
        total = sum(w for _, _, w in retenues)
        self.dire("S = V : tous les sommets sont dans l'arbre, on s'arrête", ["S = V"])
        self.wait(3.5)
        retenues_cles = {frozenset((u, v)) for u, v, _ in retenues}
        autres = [arete(g, u, v) for u, v, _ in ARETES_M if frozenset((u, v)) not in retenues_cles]
        self.play(*[e.animate.set_stroke(opacity=0.25) for e in autres])
        self.dire(
            f"Arbre couvrant minimal de poids {total} : exactement le même que celui de Kruskal",
            [f"poids {total}", "le même que celui de Kruskal"],
        )
        self.wait(5)
        self.dire(
            "À chaque tour, la propriété de coupe garantit que l'arête choisie appartient à l'arbre minimal",
            ["propriété de coupe"],
        )
        self.wait(5)
        self.play(*code.cacher())

    # ---------- Kruskal contre Prim ----------
    def comparer(self, legende, titre):
        legende = self.changer(legende, self.legende("Kruskal ou Prim ?", ["Kruskal", "Prim"]))
        garder = {titre, self.trait_titre, legende}
        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in garder])), run_time=1.2)
        colonnes_x = [-0.4, 4.4]
        en_tetes = [
            Text("Kruskal", font_size=32, weight=BOLD, color=SOMMET).move_to([colonnes_x[0], 2.0, 0]),
            Text("Prim", font_size=32, weight=BOLD, color=VIOLET).move_to([colonnes_x[1], 2.0, 0]),
        ]
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.2) for e in en_tetes], lag_ratio=0.3))
        lignes_tab = [
            ("Idée", ["trier les arêtes, fusionner des composantes", "faire grossir un seul arbre depuis s"]),
            ("Outil", ["tri + structure Union-Find", "tas binaire des arêtes candidates"]),
            ("Complexité", ["O(m log m)", "O(m log n)"]),
            ("Plutôt pour", ["graphes peu denses", "graphes denses"]),
        ]
        for i, (nom, valeurs) in enumerate(lignes_tab):
            y = 1.0 - 0.95 * i
            etiquette = texte(nom, 24, [nom])
            etiquette.align_to([-6.9, 0, 0], LEFT).set_y(y)
            cellules = []
            for x, valeur in zip(colonnes_x, valeurs):
                t = Text(valeur, font_size=22, color=TEXTE)
                t.scale_to_fit_width(min(t.width, 4.6)).move_to([x, y, 0])
                cellules.append(t)
            separateur = Line([-6.9, y + 0.47, 0], [6.9, y + 0.47, 0], color=ARETE, stroke_width=1.5)
            self.play(Create(separateur), FadeIn(etiquette, shift=RIGHT * 0.2), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cellules], lag_ratio=0.25))
            self.wait(2)
        legende = self.changer(
            legende,
            self.legende("Même arbre minimal, deux chemins pour l'obtenir", {"Même arbre minimal": VERT}),
        )
        self.wait(4)
