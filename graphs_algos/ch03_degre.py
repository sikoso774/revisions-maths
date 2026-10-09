from common import *

SOMMETS = ["A", "B", "C", "D", "E", "F"]
ARETES = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("D", "E"), ("C", "E"), ("E", "F")]
POSITION = {
    "A": LEFT * 5.2 + UP * 1.2,
    "B": LEFT * 5.2 + DOWN * 1.0,
    "C": LEFT * 3.2 + UP * 0.1,
    "D": LEFT * 1.4 + UP * 1.2,
    "E": LEFT * 1.4 + DOWN * 1.0,
    "F": LEFT * 3.2 + DOWN * 1.9,
}
DEGRES = {v: sum(v in e for e in ARETES) for v in SOMMETS}
COTES = {"A": UP, "D": UP, "C": UP, "E": RIGHT, "F": RIGHT}


class Degre(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        return self.carte(
            "Degré d'un sommet",
            ACCENT,
            [
                tex(r"$\deg(v) = \big|\{\, e \in E \mid v \in e \,\}\big|$", 46),
                tex(r"$\displaystyle\sum_{v \in V} \deg(v) = 2m$", 50),
            ],
            [
                tex(r"$\deg(v)$ : le nombre d'arêtes qui touchent le sommet $v$", 32, {"nombre d'arêtes": ACCENT}),
                tex(r"Chaque arête a deux extrémités : elle compte deux fois dans la somme", 32, {"deux fois": VERT}),
                tex(r"Conséquence : le nombre de sommets de degré impair est pair", 32, {"impair": VERT, "est pair": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        self.intro("Le degré d'un sommet", 3)

        g = creer_graphe(SOMMETS, ARETES, POSITION)
        legende = self.legende("Compter les arêtes attachées à chaque sommet", ["attachées"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        # degré de chaque sommet
        detail = None
        for v in SOMMETS:
            incidentes = [e for e in ARETES if v in e]
            noms = ", ".join("".join(e) for e in incidentes)
            detail = self.detail(
                detail, f"deg({v}) = {DEGRES[v]} : arêtes {noms}", [f"deg({v}) = {DEGRES[v]}"]
            )
            etiquette = texte(f"deg = {DEGRES[v]}", 24, {f"{DEGRES[v]}": ACCENT})
            etiquette.next_to(g.vertices[v], COTES.get(v, DOWN), buff=0.15)
            self.play(
                colorier(g, v, ACCENT),
                *[arete(g, *e).animate.set_color(ACCENT).set_stroke(width=8) for e in incidentes],
                FadeIn(etiquette, shift=UP * 0.1, scale=0.8),
                run_time=0.9,
            )
            self.wait(1.2)
            self.play(
                colorier(g, v, NOEUD),
                *[arete(g, *e).animate.set_color(LIEN).set_stroke(width=5) for e in incidentes],
                run_time=0.5,
            )

        # somme des degrés
        legende = self.changer(
            legende, self.legende("Que vaut la somme de tous les degrés ?", ["somme"])
        )
        somme = " + ".join(str(DEGRES[v]) for v in SOMMETS)
        total = sum(DEGRES.values())
        calcul = VGroup(
            tex(rf"$\displaystyle\sum_{{v \in V}} \deg(v) = {somme} = {total}$", 32),
            tex(rf"$m = |E| = {len(ARETES)}$ arêtes", 34, {"arêtes": ACCENT}),
            tex(rf"${total} = 2 \times {len(ARETES)}$", 54, couleur=VERT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 3.7 + UP * 0.2)
        detail = self.detail(detail, "On additionne les degrés de tous les sommets", ["additionne"])
        self.play(FadeIn(calcul[0], shift=LEFT * 0.3))
        self.wait(2)
        self.play(FadeIn(calcul[1], shift=LEFT * 0.3))
        self.wait(1.5)
        self.play(Write(calcul[2]))
        self.play(Circumscribe(calcul[2], color=VERT, run_time=1.2))
        self.wait(1.5)

        legende = self.changer(
            legende,
            self.legende(
                "Chaque arête a deux extrémités : elle compte deux fois",
                {"deux extrémités": ACCENT, "deux fois": VERT},
            ),
        )
        extremites = ("C", "D")
        detail = self.detail(
            detail, "Exemple : l'arête CD ajoute +1 au degré de C et +1 au degré de D", ["CD", "+1"]
        )
        plus_un = [
            Text("+1", font_size=26, color=VERT, weight=BOLD).next_to(
                g.vertices[v], RIGHT if v == "D" else LEFT, buff=0.1
            )
            for v in extremites
        ]
        self.play(
            arete(g, *extremites).animate.set_color(VERT).set_stroke(width=8),
            *[FadeIn(p, scale=1.5) for p in plus_un],
        )
        self.wait(3)
        self.play(
            arete(g, *extremites).animate.set_color(LIEN).set_stroke(width=5),
            *[FadeOut(p) for p in plus_un],
        )

        # parité
        legende = self.changer(
            legende, self.legende("Une conséquence : la parité des degrés", ["parité"])
        )
        impairs = [v for v in SOMMETS if DEGRES[v] % 2]
        detail = self.detail(
            detail,
            f"Sommets de degré impair : {' et '.join(impairs)}. Leur nombre ({len(impairs)}) est pair",
            ["impair", "est pair"],
        )
        self.play(*[colorier(g, v, ROUGE) for v in impairs])
        self.play(*[Indicate(g.vertices[v], color=ROUGE, scale_factor=1.4) for v in impairs])
        self.wait(3.5)

        self.fin(2)
