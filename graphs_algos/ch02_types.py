from common import *

SOMMETS = ["A", "B", "C", "D"]
ARETES = [("A", "B"), ("B", "C"), ("C", "D"), ("A", "C")]
CARRE = {"A": UL, "B": UR, "C": DR, "D": DL}
POIDS = {("A", "B"): 4, ("B", "C"): 2, ("C", "D"): 7, ("A", "C"): 5}


def disposition(centre_x):
    return {v: np.array([centre_x, 0.1, 0]) + 1.2 * CARRE[v] for v in SOMMETS}


class Types(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        return self.carte(
            "Trois variantes",
            ACCENT,
            [
                tex(r"$\text{Non orienté} : \ E \subseteq \big\{\, \{u, v\} \mid u, v \in V \,\big\}$", 38),
                tex(r"$\text{Orienté} : \ E \subseteq V \times V$", 38),
                tex(r"$\text{Pondéré} : \ w : E \longrightarrow \mathbb{R}$", 38),
            ],
            [
                tex(r"Non orienté : $\{u, v\} = \{v, u\}$ ; orienté : $(u, v) \neq (v, u)$", 30, {"Non orienté": ACCENT, "orienté": ACCENT}),
                tex(r"$w(e)$ : le poids de l'arête $e$ (distance, coût, durée…)", 30, {"poids": ACCENT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        self.intro("Les grands types de graphes", 2)

        colonnes = (-4.6, 0, 4.6)
        simple = creer_graphe(SOMMETS, ARETES, disposition(colonnes[0]), rayon=0.28)
        oriente = creer_graphe(SOMMETS, ARETES, disposition(colonnes[1]), orientee=True, rayon=0.28)
        pondere = creer_graphe(SOMMETS, ARETES, disposition(colonnes[2]), rayon=0.28)
        en_tetes = [
            Text(nom, font_size=34, weight=BOLD, color=ACCENT).move_to([x, 2.2, 0])
            for nom, x in zip(("Non orienté", "Orienté", "Pondéré"), colonnes)
        ]
        legende = self.legende("Trois façons de relier des sommets", ["relier"])

        # D'abord la théorie ; puis on dézoome sur les exemples concrets.
        carte = self.formules()
        self.dezoom(carte, FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        # 1. Non orienté
        self.play(FadeIn(en_tetes[0], shift=DOWN * 0.3), apparition(simple), run_time=1.8)
        detail = self.detail(
            None, "Non orienté : l'arête {A, B} est la même que {B, A}", ["{A, B}", "{B, A}"]
        )
        self.play(Indicate(simple.edges[("A", "B")], color=ACCENT))
        self.wait(3)

        # 2. Orienté
        self.play(FadeIn(en_tetes[1], shift=DOWN * 0.3), apparition(oriente), run_time=1.8)
        detail = self.detail(
            detail, "Orienté : l'arc (A, B) existe, mais l'arc (B, A) n'existe pas", ["(A, B)", "(B, A)"]
        )
        self.play(oriente.edges[("A", "B")].animate.set_color(VERT).set_stroke(width=8))
        self.wait(1)
        self.play(Indicate(oriente.vertices["A"], color=VERT), Indicate(oriente.vertices["B"], color=VERT))
        self.wait(2.5)
        self.play(oriente.edges[("A", "B")].animate.set_color(LIEN).set_stroke(width=5))

        # 3. Pondéré
        self.play(FadeIn(en_tetes[2], shift=DOWN * 0.3), apparition(pondere), run_time=1.8)
        detail = self.detail(
            detail, "Pondéré : chaque arête e porte un poids w(e)", ["poids w(e)"]
        )
        etiquettes = VGroup(*[etiquette_poids(pondere, u, v, p) for (u, v), p in POIDS.items()])
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in etiquettes], lag_ratio=0.25))
        self.wait(2.5)

        detail = self.detail(
            detail, "Poids d'un chemin = somme des poids : A – B – C pèse 4 + 2 = 6", ["4 + 2 = 6"]
        )
        chemin = [("A", "B"), ("B", "C")]
        self.play(
            *[pondere.edges[e].animate.set_color(ACCENT).set_stroke(width=8) for e in chemin],
            *[colorier(pondere, v, ACCENT) for v in "ABC"],
        )
        self.wait(3)
        detail = self.detail(
            detail, "Le chemin direct A – C ne pèse que 5 : le plus court n'est pas toujours évident", ["5", "plus court"]
        )
        self.play(
            *[pondere.edges[e].animate.set_color(LIEN).set_stroke(width=5) for e in chemin],
            pondere.edges[("A", "C")].animate.set_color(VERT).set_stroke(width=8),
            colorier(pondere, "B", NOEUD),
        )
        self.wait(3)

        legende = self.changer(
            legende,
            self.legende(
                "Amitié · Abonnement · Distance entre villes",
                {"Amitié": VERT, "Abonnement": VERT, "Distance": VERT},
            ),
        )
        self.wait(1.5)
        self.fin(2)
