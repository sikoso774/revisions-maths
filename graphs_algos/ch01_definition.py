from common import *

SOMMETS = ["A", "B", "C", "D", "E"]
ARETES = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]


class Definition(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        return self.carte(
            "Définition",
            ACCENT,
            [
                tex(r"$G = (V, E)$", 54),
                tex(r"$E \subseteq \big\{\, \{u, v\} \mid u, v \in V,\ u \neq v \,\big\}$", 42),
            ],
            [
                tex(r"$V$ : l'ensemble fini des sommets (ou nœuds), $n = |V|$", 32, {"sommets": SOMMET}),
                tex(r"$E$ : l'ensemble des arêtes, chacune relie deux sommets, $m = |E|$", 32, {"arêtes": ACCENT}),
                tex(r"Graphe simple : ni boucle ($u \neq v$), ni arête multiple ($E$ est un ensemble)", 32, {"simple": VERT}),
                tex(r"Au plus $\displaystyle\binom{n}{2} = \frac{n(n-1)}{2}$ arêtes possibles", 32, {"Au plus": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        self.intro("Qu'est-ce qu'un graphe ?", 1)

        centre = LEFT * 3.3 + UP * 0.2
        g = creer_graphe(SOMMETS, ARETES, positions_cercle(SOMMETS, 2.0, centre))
        legende = self.legende("Un graphe, c'est des objets et des liens", ["objets", "liens"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        # 1. Les sommets
        legende = self.changer(
            legende,
            self.legende("Des objets : ce sont les sommets (ou nœuds)", {"sommets": SOMMET, "nœuds": SOMMET}),
        )
        self.play(LaggedStart(*[GrowFromCenter(g.vertices[v]) for v in SOMMETS], lag_ratio=0.25))
        self.play(*[Indicate(g.vertices[v], color=SOMMET, scale_factor=1.25) for v in SOMMETS])
        ensemble_v = tex(r"$V = \{A, B, C, D, E\}$", 38).move_to(RIGHT * 3.6 + UP * 0.9)
        detail = self.detail(None, "Cinq sommets : A, B, C, D et E, donc n = 5", ["n = 5"])
        self.play(Write(ensemble_v))
        self.wait(2.5)

        # 2. Les arêtes
        legende = self.changer(
            legende, self.legende("Des liens entre eux : ce sont les arêtes", ["arêtes"])
        )
        detail = self.detail(detail, "Chaque arête relie exactement deux sommets", ["deux sommets"])
        self.play(LaggedStart(*[Create(g.edges[e]) for e in ARETES], lag_ratio=0.3))
        self.play(*[Indicate(g.edges[e], color=ACCENT) for e in ARETES])
        ensemble_e = tex(r"$E = \{AB, AC, BD, CD, DE\}$", 38).move_to(RIGHT * 3.6 + DOWN * 0.1)
        detail = self.detail(detail, "Cinq arêtes : AB, AC, BD, CD et DE, donc m = 5", ["m = 5"])
        self.play(Write(ensemble_e))
        self.wait(2.5)

        # 3. Exemple concret
        legende = self.changer(
            legende,
            self.legende(
                "Exemple : sommets = personnes, arêtes = amitiés",
                {"sommets": SOMMET, "personnes": SOMMET, "arêtes": ACCENT, "amitiés": ACCENT},
            ),
        )
        detail = self.detail(detail, "A est ami avec B et C ; D est ami avec B, C et E", ["ami"])
        self.play(Indicate(g.vertices["A"], color=VERT, scale_factor=1.4))
        self.play(*[Indicate(arete(g, *e), color=VERT) for e in [("A", "B"), ("A", "C")]])
        self.wait(2.5)

        # 4. Combien d'arêtes possibles ?
        legende = self.changer(
            legende, self.legende("Toutes les arêtes possibles sont-elles présentes ?", ["possibles"])
        )
        detail = self.detail(
            detail, "Avec n = 5 sommets : au plus n(n − 1)/2 = 10 arêtes possibles", ["10 arêtes possibles"]
        )
        manquantes = [
            DashedLine(g.vertices[u].get_center(), g.vertices[v].get_center(), color=ROUGE, stroke_width=3)
            for u, v in [("A", "D"), ("A", "E"), ("B", "C"), ("B", "E"), ("C", "E")]
        ]
        self.play(LaggedStart(*[Create(m) for m in manquantes], lag_ratio=0.25))
        self.wait(2)
        detail = self.detail(
            detail, "Ici 5 sur 10 : il en manque 5 (en pointillés rouges)", ["5 sur 10"]
        )
        self.wait(3)
        self.play(*[FadeOut(m) for m in manquantes])

        # 5. Notation
        legende = self.changer(
            legende, self.legende("Un graphe est donc un couple G = (V, E)", ["graphe", "G = (V, E)"])
        )
        detail = self.detail(
            detail, "V recense les sommets, E recense les arêtes : le graphe est le couple (V, E)", ["V", "E"]
        )
        notation = Text("G = (V, E)", font_size=48, weight=BOLD, color=TEXTE).move_to(RIGHT * 3.6 + UP * 2.0)
        self.play(Write(notation))
        self.play(
            Indicate(ensemble_v, color=SOMMET),
            *[Indicate(g.vertices[v], color=SOMMET, scale_factor=1.3) for v in SOMMETS],
        )
        self.play(
            Indicate(ensemble_e, color=ACCENT),
            *[Indicate(g.edges[e], color=ACCENT) for e in ARETES],
        )
        self.wait(1)

        self.fin(2)
