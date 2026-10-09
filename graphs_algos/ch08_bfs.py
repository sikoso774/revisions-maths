from algo import *

LIGNES_BFS = [
    (0, "marquer s ; dist[s] ← 0"),
    (0, "F ← file contenant s"),
    (0, "tant que F n'est pas vide :"),
    (1, "u ← défiler(F)"),
    (1, "pour chaque voisin v de u :"),
    (2, "si v n'est pas marqué :"),
    (3, "marquer v ; dist[v] ← dist[u] + 1"),
    (3, "parent[v] ← u"),
    (3, "enfiler(F, v)"),
]


class ParcoursLargeur(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "Principe : visiter par couches",
            SOMMET,
            [tex(r"$N_k = \{\, v \in V \mid d(s, v) = k \,\}$", 48)],
            [
                tex(r"On part de la source $s$ : $N_0 = \{s\}$, puis ses voisins $N_1$, puis $N_2$…", 32, {"source": SOMMET, "couches": SOMMET}),
                tex(r"$d(s, v)$ : le nombre minimal d'arêtes d'un chemin de $s$ à $v$", 32, {"minimal": VERT}),
                tex(r"Structure de données : une file (FIFO), premier entré, premier sorti", 32, {"file": ACCENT, "FIFO": ACCENT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Propriétés du BFS",
            VERT,
            [
                tex(r"$\text{dist}[v] = d(s, v)$", 50),
                tex(r"$T(n, m) = O(n + m)$", 50),
            ],
            [
                tex(r"Plus court chemin en nombre d'arêtes, dans un graphe non pondéré", 32, {"Plus court chemin": VERT}),
                tex(r"Chaque sommet est enfilé une seule fois, chaque arête vue au plus deux fois", 32, {"une seule fois": ACCENT}),
                tex(r"Les liens $\text{parent}[v] \to v$ forment un arbre couvrant (arbre du parcours)", 32, {"arbre couvrant": VIOLET}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        self.intro("Parcours en largeur (BFS)", 8)

        g = creer_graphe(SOMMETS_P, ARETES_P, POSITION_P)
        legende = self.legende("Explorer un graphe couche par couche", ["couche par couche"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        # l'algorithme apparaît à droite, avec sa file
        legende = self.changer(
            legende, self.legende("L'algorithme : un pseudo-code et une file", ["pseudo-code", "file"])
        )
        code = PanneauCode("BFS(G, s)", LIGNES_BFS, coin=(0.35, 2.25))
        file = Conteneur("File F", origine=(2.35, -1.85))
        self.play(*code.montrer(), *file.montrer(), run_time=1.5)
        detail = self.detail(
            None, "Entrée : le graphe G et la source s. Ici, s = A et les voisins sont pris dans l'ordre alphabétique", ["s = A"]
        )
        self.wait(4)
        legende = self.changer(
            legende,
            self.legende(
                "Blanc : pas vu · Jaune : dans la file · Bleu : en cours · Vert : traité",
                {"Jaune": ACCENT, "Bleu": SOMMET, "Vert": VERT},
            ),
        )
        detail = self.executer(g, code, file, detail)
        self.conclure(g, code, file, detail, legende)
        self.fin(3)

    # ---------- exécution pas à pas ----------
    def etiquette_dist(self, g, v, k):
        cote = {"B": LEFT, "C": UP}.get(v, DOWN)
        return Text(f"d = {k}", font_size=22, color=ACCENT, weight=BOLD).next_to(g.vertices[v], cote, buff=0.12)

    def executer(self, g, code, file, detail):
        s = "A"
        marque = {s}
        dist = {s: 0}
        self.parent = {}
        self.etiquettes = {s: self.etiquette_dist(g, s, 0)}
        self.ordre = [s]
        attente = [s]

        detail = self.detail(detail, "Initialisation : on marque A, sa distance à la source vaut 0", ["marque A", "distance"])
        self.play(code.aller_a(0), colorier(g, s, ACCENT), FadeIn(self.etiquettes[s], scale=0.8))
        self.wait(2.5)
        detail = self.detail(detail, "On place A dans la file : c'est la seule chose à traiter pour l'instant", ["file"])
        self.play(code.aller_a(1), *file.ajouter(s))
        self.wait(2.5)

        while attente:
            self.play(code.aller_a(2))
            u = attente.pop(0)
            detail = self.detail(
                detail,
                f"La file n'est pas vide : on défile {u}, le plus ancien, et on le traite",
                [f"on défile {u}"],
            )
            self.play(code.aller_a(3), *file.retirer(), colorier(g, u, SOMMET))
            self.wait(1.5)
            for v in VOISINS_P[u]:
                self.play(code.aller_a(4), Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0), run_time=1)
                self.play(code.aller_a(5), run_time=0.6)
                if v in marque:
                    detail = self.detail(
                        detail, f"{v} est déjà marqué : on ne fait rien", [f"{v} est déjà marqué"]
                    )
                    self.wait(1.5)
                    continue
                marque.add(v)
                dist[v] = dist[u] + 1
                self.parent[v] = u
                detail = self.detail(
                    detail,
                    f"{v} n'est pas marqué : dist[{v}] = dist[{u}] + 1 = {dist[v]}",
                    [f"dist[{v}] = dist[{u}] + 1 = {dist[v]}"],
                )
                self.etiquettes[v] = self.etiquette_dist(g, v, dist[v])
                self.play(code.aller_a(6), colorier(g, v, ACCENT), FadeIn(self.etiquettes[v], scale=0.8))
                self.wait(1)
                self.play(
                    code.aller_a(7),
                    arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=8),
                )
                self.play(code.aller_a(8), *file.ajouter(v))
                attente.append(v)
                self.ordre.append(v)
                self.wait(1.2)
            self.play(colorier(g, u, VERT), run_time=0.8)
            self.wait(0.6)
        self.play(code.aller_a(2))
        return detail

    # ---------- bilan ----------
    def conclure(self, g, code, file, detail, legende):
        detail = self.detail(
            detail,
            f"La file est vide : tout est visité, dans l'ordre {', '.join(self.ordre)}",
            [", ".join(self.ordre)],
        )
        self.wait(3.5)

        # couches
        legende = self.changer(legende, self.legende("Le résultat : des couches", ["couches"]))
        couches = [(0, ["A"], 1.7), (1, ["B", "C"], 0.4), (2, ["D", "E", "F"], -1.1)]
        guides = VGroup(
            *[DashedLine([-6.9, y, 0], [-1.3, y, 0], color=ARETE, stroke_width=1.5) for _, _, y in couches]
        )
        guides.set_z_index(-1)
        etiquettes = VGroup(
            *[
                tex(rf"$N_{k}$", 34).move_to([-0.7, y, 0])
                for k, _, y in couches
            ]
        )
        detail = self.detail(
            detail, "Les sommets se rangent par couches : N₀ = {A}, N₁ = {B, C}, N₂ = {D, E, F}", ["couches"]
        )
        self.play(
            LaggedStart(*[Create(x) for x in guides], lag_ratio=0.3),
            LaggedStart(*[FadeIn(e) for e in etiquettes], lag_ratio=0.3),
        )
        self.wait(4)

        # plus court chemin
        legende = self.changer(legende, self.legende("Le plus court chemin de A à F", ["plus court chemin"]))
        detail = self.detail(
            detail, "On remonte les parents : F ← C ← A, soit le chemin A → C → F de 2 arêtes", ["F ← C ← A", "2 arêtes"]
        )
        chemin = [("C", "F"), ("A", "C")]
        self.play(
            *[arete(g, u, v).animate.set_color(VERT).set_stroke(width=10) for u, v in chemin],
            *[colorier(g, v, ACCENT) for v in "ACF"],
        )
        self.wait(3)
        detail = self.detail(
            detail, "A – B – E – F existe aussi, mais fait 3 arêtes : BFS trouve toujours le plus court", ["3 arêtes", "plus court"]
        )
        self.wait(3.5)
        detail = self.detail(
            detail,
            "Attention : en nombre d'arêtes seulement. Avec des poids, il faut Dijkstra",
            ["nombre d'arêtes", "Dijkstra"],
        )
        self.wait(4)

        # complexité
        legende = self.changer(legende, self.legende("Le coût de l'algorithme", ["coût"]))
        detail = self.detail(
            detail,
            "Chaque sommet entre une fois dans la file, chaque arête est vue deux fois : O(n + m)",
            ["O(n + m)"],
        )
        self.wait(5)
        self.play(FadeOut(detail), FadeOut(guides), FadeOut(etiquettes), *code.cacher())
