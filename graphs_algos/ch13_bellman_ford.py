from algo import *

INF = float("inf")

# Graphe orienté d'étude : l'ordre des arcs est volontairement défavorable (il faut 4 passes)
SOMMETS_B = list("ABCDE")
ARCS_B = [
    ("D", "E", -2), ("C", "E", 8), ("C", "D", 3), ("B", "D", 7),
    ("B", "C", -3), ("A", "C", 5), ("A", "B", 4),
]
POS_B = {
    "A": LEFT * 6.0 + UP * 0.3,
    "B": LEFT * 4.6 + UP * 1.7,
    "C": LEFT * 4.0 + DOWN * 0.8,
    "D": LEFT * 2.2 + UP * 0.9,
    "E": LEFT * 1.2 + DOWN * 1.0,
}
COTES_B = {"A": DOWN, "B": UP, "C": DOWN, "D": UP, "E": RIGHT}

# Petit graphe avec un cycle négatif : B → C → D → B pèse −2 + 1 + 0 = −1
SOMMETS_N = list("ABCD")
ARCS_N = [("A", "B", 2), ("B", "C", -2), ("C", "D", 1), ("D", "B", 0)]
POS_N = {
    "A": LEFT * 6.2 + UP * 0.3,
    "B": LEFT * 4.0 + UP * 1.4,
    "C": LEFT * 1.8 + UP * 0.2,
    "D": LEFT * 4.0 + DOWN * 1.0,
}
COTES_N = {"A": DOWN, "B": UP, "C": RIGHT, "D": DOWN}

LIGNES_BF = [
    (0, "d[v] ← ∞ pour tout v ; d[s] ← 0"),
    (0, "répéter n − 1 fois :"),
    (1, "pour chaque arc (u, v) de poids w :"),
    (2, "si d[u] + w < d[v] :"),
    (3, "d[v] ← d[u] + w ; parent[v] ← u"),
    (0, "pour chaque arc (u, v) de poids w :"),
    (1, "si d[u] + w < d[v] : cycle négatif !"),
]


def nb(x):
    """Nombre lisible : ∞, ou entier avec un vrai signe moins."""
    return "∞" if x == INF else str(x).replace("-", "−")


class BellmanFord(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "Pourquoi un autre algorithme ?",
            ROUGE,
            [tex(r"$w(e) < 0 \ \text{ possible} \qquad \text{Dijkstra : } w(e) \geq 0$", 44)],
            [
                tex(r"Un poids négatif modélise un gain, une remise, un remboursement", 32, {"poids négatif": ROUGE}),
                tex(r"Dijkstra fixe un sommet trop tôt : un arc négatif peut raccourcir un chemin déjà « définitif »", 30, {"trop tôt": ROUGE}),
                tex(r"Bellman-Ford accepte les poids négatifs et détecte les cycles négatifs", 32, {"détecte les cycles négatifs": VERT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        carte = self.carte(
            "Le principe",
            VERT,
            [
                tex(r"$d[v] \leftarrow \min\big(d[v],\ d[u] + w(u, v)\big) \quad \text{pour tout arc } (u, v)$", 40),
                tex(r"$\text{on répète } n - 1 \text{ fois}$", 42),
            ],
            [
                tex(r"Un plus court chemin simple a au plus $n - 1$ arcs : $n - 1$ passes suffisent", 32, {"n - 1": VERT}),
                tex(r"Après la passe $k$, $d[v]$ est exact pour tous les sommets à au plus $k$ arcs de $s$", 32, {"au plus": VERT}),
                tex(r"Si une $n$-ième passe améliore encore une distance : cycle négatif accessible depuis $s$", 32, {"cycle négatif": ROUGE}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Complexité",
            ACCENT,
            [tex(r"$T(n, m) = O(n \cdot m)$", 52)],
            [
                tex(r"$n - 1$ passes, chacune parcourt les $m$ arcs", 32, {"m arcs": ACCENT}),
                tex(r"Plus lent que Dijkstra en $O((n + m) \log n)$, mais plus général", 32, {"plus général": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("L'algorithme de Bellman-Ford", 13)

        g = creer_graphe(SOMMETS_B, [(u, v) for u, v, _ in ARCS_B], POS_B, orientee=True)
        legende = self.legende("Plus courts chemins, même avec des poids négatifs", ["poids négatifs"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        poids = self.poids(g, ARCS_B)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in poids], lag_ratio=0.15))
        self.wait(1)

        legende = self.changer(
            legende, self.legende("L'algorithme : un pseudo-code et des passes sur tous les arcs", ["pseudo-code", "passes"])
        )
        code = PanneauCode("BellmanFord(G, w, s)", LIGNES_BF, coin=(0.35, 2.25))
        self.play(*code.montrer(), run_time=1.5)
        self.det = self.detail(
            None, "Graphe orienté pondéré, source s = A, avec deux arcs de poids négatif (en rouge)", ["s = A", "négatif"]
        )
        self.wait(4)
        legende = self.changer(
            legende,
            self.legende("Blanc : distance ∞ ou provisoire · Jaune épais : arc parent", {"Jaune": ACCENT}),
        )

        historique, _, _ = self.executer(g, SOMMETS_B, ARCS_B, "A", self.etiqueteur(g, COTES_B), code)
        self.tableau(g, code, historique, poids)
        legende = self.pourquoi_pas_dijkstra(legende, titre, g, poids)
        legende = self.cycle_negatif(legende, titre, code)
        self.comparer(legende, titre)
        self.fin(3)

    # ---------- outils ----------
    def dire(self, contenu, cles=None):
        self.det = self.detail(self.det, contenu, cles)

    def poids(self, g, arcs):
        """Poids sur les arcs ; les poids négatifs sont en rouge."""
        groupe = VGroup()
        for u, v, w in arcs:
            etiquette = etiquette_poids(g, u, v, nb(w))
            if w < 0:
                etiquette[1].set_color(ROUGE)
            groupe.add(etiquette)
        return groupe

    def etiqueteur(self, g, cotes):
        def etiqueter(v, val, couleur):
            return Text(f"d = {nb(val)}", font_size=22, color=couleur, weight=BOLD).next_to(
                g.vertices[v], cotes[v], buff=0.12
            )
        return etiqueter

    # ---------- exécution pas à pas ----------
    def executer(self, g, sommets, arcs, source, etiqueter, code, detaille=True):
        n = len(sommets)
        d = {v: INF for v in sommets}
        d[source] = 0
        parent = {}
        labels = {v: etiqueter(v, d[v], ACCENT) for v in sommets}
        historique = [dict(d)]

        def passe(k, texte_passe):
            return Text(texte_passe, font_size=30, weight=BOLD, color=ACCENT).move_to([3.7, -1.2, 0])

        self.dire(f"Initialisation : d[{source}] = 0 et toutes les autres distances valent ∞", ["∞"])
        indicateur = passe(0, f"Passe 0 / {n - 1}")
        self.play(code.aller_a(0), LaggedStart(*[FadeIn(l, scale=0.8) for l in labels.values()], lag_ratio=0.1), FadeIn(indicateur))
        self.wait(2.5 if detaille else 1.5)

        for k in range(1, n):
            nouveau = passe(k, f"Passe {k} / {n - 1}")
            self.dire(
                f"Passe {k} sur {n - 1} : on relâche chacun des {len(arcs)} arcs, dans l'ordre de la liste"
                if k == 1
                else f"Passe {k} : on relâche de nouveau tous les arcs",
                [f"Passe {k}"],
            )
            self.play(code.aller_a(1), Transform(indicateur, nouveau))
            self.wait(1.5 if k == 1 else 0.8)
            modifies = []
            for u, v, w in arcs:
                rapide = k > 1 or not detaille
                self.play(code.aller_a(2), Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0), run_time=0.8 if rapide else 1)
                self.play(code.aller_a(3), run_time=0.5)
                if d[u] == INF:
                    self.dire(f"{u} → {v} : d[{u}] vaut encore ∞, rien à relâcher", ["∞"])
                    self.wait(0.8 if rapide else 1.6)
                    continue
                candidat = d[u] + w
                avant = d[v]
                calcul = f"d[{u}] + w({u},{v}) = {nb(d[u])} + {('(' + nb(w) + ')') if w < 0 else nb(w)} = {nb(candidat)}"
                if candidat < avant:
                    if avant == INF:
                        self.dire(f"{calcul} < ∞ : première estimation, d[{v}] = {nb(candidat)}", {"première estimation": VERT})
                    else:
                        self.dire(
                            f"{calcul} < {nb(avant)} : d[{v}] passe de {nb(avant)} à {nb(candidat)}",
                            {f"passe de {nb(avant)} à {nb(candidat)}": VERT},
                        )
                    self.wait(0.9 if rapide else 1.8)
                    ancien = (
                        [arete(g, parent[v], v).animate.set_color(LIEN).set_stroke(width=5)] if v in parent else []
                    )
                    parent[v] = u
                    d[v] = candidat
                    modifies.append(v)
                    self.play(
                        code.aller_a(4),
                        Transform(labels[v], etiqueter(v, candidat, ACCENT)),
                        arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=8),
                        *ancien,
                    )
                    self.wait(0.8 if rapide else 1.4)
                else:
                    self.dire(f"{calcul} ≥ {nb(avant)} : pas mieux, d[{v}] reste {nb(avant)}", {"pas mieux": ROUGE})
                    self.wait(0.9 if rapide else 1.8)
            historique.append(dict(d))
            if modifies:
                self.dire(
                    f"Fin de la passe {k} : distances modifiées pour {', '.join(sorted(set(modifies)))}",
                    [f"Fin de la passe {k}"],
                )
            else:
                self.dire(f"Fin de la passe {k} : aucune distance modifiée", [f"Fin de la passe {k}"])
            self.wait(2.2 if detaille else 1.2)

        # passe de contrôle (n-ième passe)
        controle = passe(n, "Passe de contrôle")
        self.dire(
            f"Passe de contrôle : si un arc améliore encore une distance, il y a un cycle négatif",
            ["cycle négatif"],
        )
        self.play(code.aller_a(5), Transform(indicateur, controle))
        self.wait(1.5)
        for u, v, w in arcs:
            self.play(code.aller_a(6), Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0), run_time=0.6)
            if d[u] != INF and d[u] + w < d[v]:
                self.dire(
                    f"{u} → {v} améliore encore d[{v}] ({nb(d[u] + w)} < {nb(d[v])}) : cycle négatif détecté !",
                    {"cycle négatif détecté !": ROUGE},
                )
                self.wait(2)
                self.play(FadeOut(indicateur))
                return historique, True, (u, v)
        self.dire("Aucun arc n'améliore une distance : pas de cycle négatif, les distances sont exactes", {"pas de cycle négatif": VERT})
        self.play(*[colorier(g, v, VERT) for v in sommets], FadeOut(indicateur))
        self.wait(3.5)
        return historique, False, None

    # ---------- tableau récapitulatif : une ligne par passe ----------
    def tableau(self, g, code, historique, poids):
        self.dire("Récapitulons les distances après chaque passe", ["après chaque passe"])
        self.play(*code.cacher())
        n_col = len(SOMMETS_B)
        x0, y0, pas_x, pas_y = 1.4, 1.9, 0.95, 0.55
        entetes = VGroup(
            Text("passe", font_size=22, color=ARETE).move_to([x0, y0, 0]),
            *[
                Text(v, font_size=26, color=SOMMET, weight=BOLD).move_to([x0 + pas_x * (j + 1), y0, 0])
                for j, v in enumerate(SOMMETS_B)
            ],
        )
        self.play(FadeIn(entetes, shift=DOWN * 0.2))
        # sommet devenu définitif à chaque passe (au plus k arcs de la source)
        definitifs = {1: "B", 2: "C", 3: "D", 4: "E"}
        lignes = []
        for k, d in enumerate(historique):
            y = y0 - pas_y * (k + 1)
            nom = Text("0" if k == 0 else str(k), font_size=24, color=ARETE).move_to([x0, y, 0])
            cellules = []
            for j, v in enumerate(SOMMETS_B):
                change = k > 0 and d[v] != historique[k - 1][v]
                couleur = VERT if definitifs.get(k) == v else (ACCENT if change else TEXTE)
                cellules.append(
                    Text(nb(d[v]), font_size=26, color=couleur, weight=BOLD if change else NORMAL).move_to(
                        [x0 + pas_x * (j + 1), y, 0]
                    )
                )
            lignes.append(VGroup(nom, *cellules))
            self.play(FadeIn(lignes[-1], shift=UP * 0.15), run_time=0.8)
            if k == 0:
                self.wait(1.5)
            else:
                self.wait(2.2)
        self.dire(
            "En vert : le sommet devenu exact à cette passe. Passe k : tous les sommets à ≤ k arcs de A sont corrects",
            ["En vert", "≤ k arcs"],
        )
        self.wait(5)
        chemin = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")]
        self.dire(
            "Chemin de A à E : A → B → C → D → E, de poids 4 − 3 + 3 − 2 = 2 (4 arcs, donc 4 passes)",
            ["4 − 3 + 3 − 2 = 2"],
        )
        self.play(*[arete(g, u, v).animate.set_color(VERT).set_stroke(width=10) for u, v in chemin])
        self.wait(5)
        self.play(
            FadeOut(entetes),
            *[FadeOut(l) for l in lignes],
            *[arete(g, u, v).animate.set_color(LIEN).set_stroke(width=5) for u, v, _ in ARCS_B],
        )

    # ---------- pourquoi Dijkstra échoue ----------
    def pourquoi_pas_dijkstra(self, legende, titre, g, poids):
        legende = self.changer(legende, self.legende("Pourquoi Dijkstra se trompe avec un poids négatif", ["Dijkstra", "se trompe"]))
        garder = {titre, self.trait_titre, legende}
        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in garder])), run_time=1.0)

        arcs = [("A", "B", 2), ("A", "C", 3), ("C", "B", -2)]
        pos = {"A": LEFT * 4.5 + UP * 0.2, "B": LEFT * 1.0 + UP * 1.2, "C": LEFT * 1.0 + DOWN * 1.1}
        petit = creer_graphe(list("ABC"), [(u, v) for u, v, _ in arcs], pos, orientee=True)
        cotes = {"A": LEFT, "B": RIGHT, "C": RIGHT}
        etiqueter = self.etiqueteur(petit, cotes)
        self.play(apparition(petit))
        p = self.poids(petit, arcs)
        self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in p], lag_ratio=0.2))
        self.det = self.detail(None, "Trois sommets : A → B (2), A → C (3) et C → B (−2). Dijkstra part de A", ["Dijkstra"])
        labels = {v: etiqueter(v, 0 if v == "A" else INF, ACCENT) for v in "ABC"}
        self.play(LaggedStart(*[FadeIn(l, scale=0.8) for l in labels.values()], lag_ratio=0.15), colorier(petit, "A", VERT))
        self.wait(3)
        self.dire("Il relâche A : d[B] = 2 et d[C] = 3. Le plus proche non fixé est B", ["le plus proche"])
        self.play(Transform(labels["B"], etiqueter("B", 2, ACCENT)), Transform(labels["C"], etiqueter("C", 3, ACCENT)))
        self.wait(2.5)
        self.dire("Dijkstra fixe B avec d[B] = 2 : il le croit définitif", ["fixe B", "définitif"])
        self.play(colorier(petit, "B", VERT), Transform(labels["B"], etiqueter("B", 2, VERT)))
        self.wait(3)
        self.dire("Puis C (3) : l'arc C → B est ignoré, car B est déjà fixé", ["déjà fixé"])
        self.play(colorier(petit, "C", VERT), Transform(labels["C"], etiqueter("C", 3, VERT)))
        self.play(petit.edges[("C", "B")].animate.set_color(ROUGE).set_stroke(width=8))
        self.wait(3.5)
        self.dire("Résultat faux : d[B] = 2, alors que A → C → B ne pèse que 3 − 2 = 1", {"faux": ROUGE, "3 − 2 = 1": VERT})
        self.play(*[Indicate(petit.vertices["B"], color=ROUGE, scale_factor=1.4)])
        self.wait(4)
        self.dire("Bellman-Ford relâche tous les arcs à chaque passe : à la passe 2, C → B corrige d[B] = 1", ["Bellman-Ford", "d[B] = 1"])
        self.play(
            Transform(labels["B"], etiqueter("B", 1, VERT)),
            petit.edges[("C", "B")].animate.set_color(VERT).set_stroke(width=8),
        )
        self.wait(5)
        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in garder])), run_time=1.0)
        self.det = None
        return legende

    # ---------- cycle négatif ----------
    def cycle_negatif(self, legende, titre, code):
        legende = self.changer(
            legende, self.legende("Un cycle négatif : plus de plus court chemin", {"cycle négatif": ROUGE})
        )
        g2 = creer_graphe(SOMMETS_N, [(u, v) for u, v, _ in ARCS_N], POS_N, orientee=True)
        self.play(apparition(g2), *code.montrer(), run_time=2)
        p = self.poids(g2, ARCS_N)
        self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in p], lag_ratio=0.2))
        self.det = self.detail(
            None, "Le cycle B → C → D → B pèse −2 + 1 + 0 = −1 : chaque tour fait baisser les distances", ["−1", "chaque tour"]
        )
        self.play(*[g2.edges[e].animate.set_color(ROUGE).set_stroke(width=7) for e in [("B", "C"), ("C", "D"), ("D", "B")]])
        self.wait(4)
        self.play(*[g2.edges[e].animate.set_color(LIEN).set_stroke(width=5) for e in [("B", "C"), ("C", "D"), ("D", "B")]])

        _, cycle, arc = self.executer(g2, SOMMETS_N, ARCS_N, "A", self.etiqueteur(g2, COTES_N), code, detaille=False)
        if cycle:
            self.play(*[g2.edges[e].animate.set_color(ROUGE).set_stroke(width=9) for e in [("B", "C"), ("C", "D"), ("D", "B")]])
            self.dire(
                "Les distances baissent à chaque passe, même la n-ième : aucun plus court chemin n'existe, l'algorithme le signale",
                ["aucun plus court chemin", "le signale"],
            )
            self.wait(6)
        self.play(*code.cacher())
        return legende

    # ---------- Dijkstra contre Bellman-Ford ----------
    def comparer(self, legende, titre):
        legende = self.changer(legende, self.legende("Dijkstra ou Bellman-Ford ?", ["Dijkstra", "Bellman-Ford"]))
        garder = {titre, self.trait_titre, legende}
        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in garder])), run_time=1.2)
        colonnes_x = [-0.4, 4.4]
        en_tetes = [
            Text("Dijkstra", font_size=32, weight=BOLD, color=SOMMET).move_to([colonnes_x[0], 2.0, 0]),
            Text("Bellman-Ford", font_size=32, weight=BOLD, color=VIOLET).move_to([colonnes_x[1], 2.0, 0]),
        ]
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.2) for e in en_tetes], lag_ratio=0.3))
        lignes_tab = [
            ("Idée", ["fixer le sommet le plus proche", "relâcher tous les arcs, n − 1 fois"]),
            ("Poids négatifs", ["interdits", "acceptés"]),
            ("Cycle négatif", ["non détecté", "détecté (n-ième passe)"]),
            ("Complexité", ["O((n + m) log n)", "O(n · m)"]),
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
            self.legende("Sans poids négatifs : Dijkstra. Sinon : Bellman-Ford", {"Dijkstra": SOMMET, "Bellman-Ford": VIOLET}),
        )
        self.wait(4)
