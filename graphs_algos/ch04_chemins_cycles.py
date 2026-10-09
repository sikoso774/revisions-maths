from common import *

SOMMETS = ["A", "B", "C", "D", "E", "F"]
ARETES = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "B"), ("D", "E"), ("E", "F")]
POSITION = {
    "A": LEFT * 3.3 + UP * 0.1,
    "B": LEFT * 1.3 + UP * 0.1,
    "C": RIGHT * 0.0 + UP * 1.7,
    "D": RIGHT * 0.0 + DOWN * 1.5,
    "E": RIGHT * 1.8 + UP * 0.1,
    "F": RIGHT * 3.8 + UP * 0.1,
}


class CheminsCycles(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        return self.carte(
            "Chemins, cycles et arbres",
            ACCENT,
            [
                tex(r"$\mu = (x_0, x_1, \dots, x_k)$ avec $\{x_{i-1}, x_i\} \in E$", 42),
                tex(r"Cycle : $x_0 = x_k$, $k \geq 3$, sommets $x_0, \dots, x_{k-1}$ distincts", 38),
            ],
            [
                tex(r"Un chemin $\mu$ a pour longueur $k$ : le nombre d'arêtes parcourues", 32, {"longueur": VERT}),
                tex(r"Chemin simple : aucun sommet n'est répété", 32, {"simple": ACCENT}),
                tex(r"Arbre : graphe connexe et acyclique, il vérifie $m = n - 1$", 32, {"Arbre": VERT, "acyclique": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        self.intro("Chemins et cycles", 4)

        g = creer_graphe(SOMMETS, ARETES, POSITION)
        legende = self.legende("Un graphe, vu comme un réseau de routes", ["réseau de routes"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        # Chemin A -> B -> C -> D -> E
        chemin = ["A", "B", "C", "D", "E"]
        legende = self.changer(
            legende,
            self.legende(
                "Un chemin : une suite de sommets reliés deux à deux",
                {"chemin": ACCENT, "suite de sommets": ACCENT},
            ),
        )
        detail = self.detail(None, "Partons de A et suivons les arêtes jusqu'à E", ["A", "E"])
        compteur = Text("longueur : 0", font_size=32, color=ACCENT).to_corner(UR).shift(DOWN * 1.2)
        self.play(colorier(g, chemin[0], ACCENT), FadeIn(compteur, shift=LEFT * 0.3))
        for i, (u, v) in enumerate(zip(chemin, chemin[1:]), start=1):
            self.play(
                arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=8),
                colorier(g, v, ACCENT),
                Transform(compteur, Text(f"longueur : {i}", font_size=32, color=ACCENT).move_to(compteur)),
                run_time=1,
            )
            self.wait(0.6)
        detail = self.detail(
            detail,
            "Chemin A → B → C → D → E : 4 arêtes parcourues, donc longueur 4",
            {"A → B → C → D → E": ACCENT, "longueur 4": VERT},
        )
        self.wait(2.5)
        detail = self.detail(
            detail, "Aucun sommet n'est répété : c'est un chemin simple", ["chemin simple"]
        )
        self.wait(2.5)
        self.play(
            *[colorier(g, v, NOEUD) for v in SOMMETS],
            *[arete(g, *e).animate.set_color(LIEN).set_stroke(width=5) for e in ARETES],
            FadeOut(compteur, shift=RIGHT * 0.3),
        )

        # Cycle B -> C -> D -> B
        cycle = ["B", "C", "D", "B"]
        legende = self.changer(
            legende,
            self.legende(
                "Un cycle : un chemin qui revient à son point de départ",
                {"cycle": ROUGE, "revient à son point de départ": ROUGE},
            ),
        )
        detail = self.detail(detail, "Partons de B et essayons de revenir en B", ["B"])
        self.play(colorier(g, "B", ROUGE))
        for u, v in zip(cycle, cycle[1:]):
            self.play(
                arete(g, u, v).animate.set_color(ROUGE).set_stroke(width=8),
                colorier(g, v, ROUGE),
                run_time=1,
            )
            self.wait(0.5)
        self.play(Indicate(g.vertices["B"], color=ROUGE, scale_factor=1.4))
        detail = self.detail(
            detail,
            "Cycle B → C → D → B : on revient au départ (x₀ = x₃), longueur 3",
            {"Cycle B → C → D → B": ROUGE, "longueur 3": VERT},
        )
        self.wait(3.5)

        # Arbre : on casse le cycle
        legende = self.changer(
            legende,
            self.legende(
                "Sans cycle : un graphe acyclique, comme un arbre",
                {"acyclique": VERT, "arbre": VERT},
            ),
        )
        detail = self.detail(detail, "Retirons l'arête D – B : le cycle disparaît", ["D – B"])
        self.play(
            *[colorier(g, v, NOEUD) for v in "BCD"],
            *[arete(g, u, v).animate.set_color(LIEN).set_stroke(width=5) for u, v in [("B", "C"), ("C", "D")]],
            FadeOut(arete(g, "D", "B")),
        )
        self.wait(2)
        detail = self.detail(
            detail,
            "Connexe et acyclique : c'est un arbre, avec m = n − 1 (ici 5 arêtes pour 6 sommets)",
            {"arbre": VERT, "m = n − 1": VERT},
        )
        self.play(*[Indicate(g.vertices[v], color=VERT, scale_factor=1.25) for v in SOMMETS])
        self.wait(4)

        self.fin(2)
