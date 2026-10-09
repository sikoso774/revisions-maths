from common import *
from algo import ARETES_P, POSITION_P, SOMMETS_P

SOMMETS = list("ABCDEFG")
ARETES = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G")]
# Même arbre, dessiné deux fois : « libre » puis « enraciné en A »
LIBRE = {
    "A": LEFT * 3.4 + UP * 0.4,
    "B": LEFT * 5.2 + UP * 1.6,
    "D": LEFT * 6.4 + UP * 0.4,
    "E": LEFT * 5.4 + DOWN * 1.1,
    "C": LEFT * 1.6 + UP * 1.3,
    "F": LEFT * 0.7 + DOWN * 0.2,
    "G": LEFT * 2.2 + DOWN * 1.0,
}
RACINE = {
    "A": LEFT * 3.5 + UP * 1.7,
    "B": LEFT * 5.2 + UP * 0.3,
    "C": LEFT * 1.8 + UP * 0.3,
    "D": LEFT * 6.0 + DOWN * 1.1,
    "E": LEFT * 4.4 + DOWN * 1.1,
    "F": LEFT * 2.6 + DOWN * 1.1,
    "G": LEFT * 1.0 + DOWN * 1.1,
}


class Arbres(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "Définition",
            ACCENT,
            [tex(r"$G \text{ est un arbre} \iff G \text{ est connexe et sans cycle}$", 46)],
            [
                tex(r"Exemples : une arborescence de dossiers, un arbre généalogique", 32, {"arborescence": ACCENT}),
                tex(r"Un arbre à $n$ sommets possède exactement $m = n - 1$ arêtes", 32, {"exactement": VERT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        carte = self.carte(
            "Caractérisations équivalentes",
            VERT,
            [
                tex(r"$G \text{ arbre} \iff G \text{ connexe et } m = n - 1 \iff G \text{ acyclique et } m = n - 1$", 36),
            ],
            [
                tex(r"$\iff$ entre deux sommets quelconques, il existe un unique chemin", 32, {"unique chemin": VERT}),
                tex(r"$\iff G$ connexe minimal : retirer une arête le déconnecte", 32, {"minimal": VERT}),
                tex(r"$\iff G$ acyclique maximal : ajouter une arête crée un cycle", 32, {"maximal": VERT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Arbre enraciné et arbre couvrant",
            VIOLET,
            [
                tex(r"$\text{prof}(v) = d(r, v) \qquad h = \max_{v \in V} \text{prof}(v)$", 44),
                tex(r"$T = (V, E') \text{ arbre couvrant de } G = (V, E) \iff E' \subseteq E$", 40),
            ],
            [
                tex(r"Racine $r$, parents, enfants ; une feuille est un sommet sans enfant", 32, {"feuille": VIOLET}),
                tex(r"$G$ connexe $\iff$ $G$ possède un arbre couvrant ($n - 1$ arêtes)", 32, {"arbre couvrant": VIOLET}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Les arbres", 7)

        g = creer_graphe(SOMMETS, ARETES, LIBRE)
        legende = self.legende("Un arbre : un graphe connexe et sans cycle", ["connexe", "sans cycle"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        g = self.verifier(g)
        g = self.cycle_et_deconnexion(g)
        g = self.enraciner(g)
        self.arbre_couvrant(g, legende)
        self.fin(3)

    # ---------- 1) vérifier que c'est un arbre ----------
    def verifier(self, g):
        detail = self.detail(
            None, "Connexe : on peut aller de n'importe quel sommet à n'importe quel autre", ["Connexe"]
        )
        self.play(*[colorier(g, v, VERT) for v in SOMMETS], *[g.edges[e].animate.set_color(VERT) for e in ARETES])
        self.wait(2.5)
        detail = self.detail(detail, "Sans cycle : impossible de revenir à son point de départ sans repasser par une arête", ["Sans cycle"])
        self.wait(3)
        self.play(*[colorier(g, v, NOEUD) for v in SOMMETS], *[g.edges[e].animate.set_color(LIEN) for e in ARETES])

        self.compteurs = VGroup(
            tex(r"$n = 7$ sommets", 36, {"sommets": SOMMET}),
            tex(r"$m = 6$ arêtes", 36, {"arêtes": ACCENT}),
            tex(r"$m = n - 1$", 54, couleur=VERT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 3.9 + UP * 0.6)
        detail = self.detail(detail, "Comptons : 7 sommets et 6 arêtes, donc m = n − 1", ["m = n − 1"])
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in self.compteurs], lag_ratio=0.5))
        self.wait(3)
        self.detail_courant = detail
        return g

    # ---------- 2) ajouter / retirer une arête ----------
    def cycle_et_deconnexion(self, g):
        detail = self.detail_courant
        aretes_visibles = [(u, v) for u, v in ARETES]

        # ajouter D–E : cycle
        detail = self.detail(
            detail, "Ajoutons l'arête D–E : un cycle B – D – E apparaît, ce n'est plus un arbre", ["D–E", "cycle"]
        )
        supplementaire = Line(
            g.vertices["D"].get_center(), g.vertices["E"].get_center(), stroke_color=ACCENT, stroke_width=5
        )
        self.play(Create(supplementaire))
        self.wait(1)
        cycle = [g.edges[("B", "D")], supplementaire, g.edges[("B", "E")]]
        self.play(
            *[e.animate.set_color(ROUGE).set_stroke(width=8) for e in cycle],
            *[colorier(g, v, ROUGE) for v in "BDE"],
        )
        nouveau_m = tex(r"$m = 7 = n$", 54, couleur=ROUGE).move_to(self.compteurs[2]).align_to(self.compteurs[2], LEFT)
        self.play(
            Transform(self.compteurs[1], tex(r"$m = 7$ arêtes", 36, {"arêtes": ACCENT}).move_to(self.compteurs[1]).align_to(self.compteurs[1], LEFT)),
            Transform(self.compteurs[2], nouveau_m),
        )
        self.wait(3.5)
        detail = self.detail(
            detail, "Acyclique maximal : ajouter n'importe quelle arête crée un cycle", ["maximal"]
        )
        self.wait(2.5)
        self.play(
            FadeOut(supplementaire),
            *[g.edges[e].animate.set_color(LIEN).set_stroke(width=5) for e in [("B", "D"), ("B", "E")]],
            *[colorier(g, v, NOEUD) for v in "BDE"],
            Transform(self.compteurs[1], tex(r"$m = 6$ arêtes", 36, {"arêtes": ACCENT}).move_to(self.compteurs[1]).align_to(self.compteurs[1], LEFT)),
            Transform(self.compteurs[2], tex(r"$m = n - 1$", 54, couleur=VERT).move_to(self.compteurs[2]).align_to(self.compteurs[2], LEFT)),
        )

        # retirer A–C : déconnexion
        detail = self.detail(
            detail, "Retirons l'arête A–C : le graphe se coupe en deux morceaux, il n'est plus connexe", ["A–C", "plus connexe"]
        )
        self.play(FadeOut(g.edges[("A", "C")]))
        self.play(
            *[colorier(g, v, VERT) for v in "ABDE"],
            *[colorier(g, v, VIOLET) for v in "CFG"],
            *[g.edges[e].animate.set_color(VERT) for e in [("A", "B"), ("B", "D"), ("B", "E")]],
            *[g.edges[e].animate.set_color(VIOLET) for e in [("C", "F"), ("C", "G")]],
        )
        self.wait(3)
        detail = self.detail(
            detail, "Connexe minimal : dans un arbre, retirer n'importe quelle arête déconnecte", ["minimal"]
        )
        self.wait(3)
        self.play(
            FadeIn(g.edges[("A", "C")]),
            *[colorier(g, v, NOEUD) for v in SOMMETS],
            *[g.edges[e].animate.set_color(LIEN) for e in ARETES],
        )

        # unique chemin D -> G
        detail = self.detail(
            detail, "Entre D et G, il n'existe qu'un seul chemin : D – B – A – C – G", ["un seul chemin"]
        )
        chemin = ["D", "B", "A", "C", "G"]
        self.play(colorier(g, chemin[0], ACCENT), run_time=0.4)
        for u, v in zip(chemin, chemin[1:]):
            e = g.edges[(u, v)] if (u, v) in g.edges else g.edges[(v, u)]
            self.play(e.animate.set_color(ACCENT).set_stroke(width=8), colorier(g, v, ACCENT), run_time=0.8)
        self.wait(3)
        self.play(
            *[colorier(g, v, NOEUD) for v in SOMMETS],
            *[g.edges[e].animate.set_color(LIEN).set_stroke(width=5) for e in ARETES],
        )
        self.detail_courant = detail
        return g

    # ---------- 3) arbre enraciné ----------
    def enraciner(self, g):
        detail = self.detail(
            self.detail_courant, "Choisissons A comme racine et dessinons l'arbre vers le bas", ["racine"]
        )
        racine = creer_graphe(SOMMETS, ARETES, RACINE)
        self.play(FadeOut(self.compteurs))
        self.play(ReplacementTransform(parties(g), parties(racine)), run_time=2.5)
        g = racine
        self.wait(2)

        detail = self.detail(detail, "A est la racine : le seul sommet sans parent", ["racine"])
        racine_txt = Text("racine", font_size=24, color=ACCENT, weight=BOLD).next_to(g.vertices["A"], RIGHT, buff=0.3)
        self.play(colorier(g, "A", ACCENT), FadeIn(racine_txt, shift=LEFT * 0.2))
        self.wait(2.5)

        detail = self.detail(
            detail, "B et C sont les enfants de A ; A est leur parent", ["enfants", "parent"]
        )
        self.play(*[colorier(g, v, SOMMET) for v in "BC"], *[g.edges[e].animate.set_color(SOMMET).set_stroke(width=8) for e in [("A", "B"), ("A", "C")]])
        self.wait(3)

        detail = self.detail(
            detail, "D, E, F et G n'ont pas d'enfant : ce sont les feuilles", ["feuilles"]
        )
        self.play(*[colorier(g, v, VERT) for v in "DEFG"], *[g.edges[e].animate.set_color(VERT).set_stroke(width=8) for e in [("B", "D"), ("B", "E"), ("C", "F"), ("C", "G")]])
        self.wait(3)

        detail = self.detail(
            detail,
            "La profondeur d'un sommet est sa distance à la racine ; la hauteur h = 2 est la plus grande",
            ["profondeur", "hauteur h = 2"],
        )
        niveaux = VGroup(
            Text("prof = 0", font_size=24, color=TEXTE).move_to([1.2, 1.7, 0]),
            Text("prof = 1", font_size=24, color=TEXTE).move_to([1.2, 0.3, 0]),
            Text("prof = 2", font_size=24, color=TEXTE).move_to([1.2, -1.1, 0]),
        )
        guides = VGroup(
            *[DashedLine([-6.9, y, 0], [0.4, y, 0], color=ARETE, stroke_width=1.5) for y in (1.7, 0.3, -1.1)]
        )
        guides.set_z_index(-1)
        self.play(LaggedStart(*[Create(x) for x in guides], lag_ratio=0.3), LaggedStart(*[FadeIn(n) for n in niveaux], lag_ratio=0.3))
        self.wait(4)
        self.play(FadeOut(niveaux), FadeOut(guides), FadeOut(racine_txt), FadeOut(parties(g)), FadeOut(detail))
        self.detail_courant = None
        return g

    # ---------- 4) arbre couvrant ----------
    def arbre_couvrant(self, g, legende):
        legende = self.changer(
            legende,
            self.legende("Un arbre couvrant : relier tous les sommets sans cycle", {"arbre couvrant": VIOLET}),
        )
        h = creer_graphe(SOMMETS_P, ARETES_P, POSITION_P)
        self.play(apparition(h), run_time=2.5)
        info_g = tex(
            r"$G$ : $n = 6$ sommets, $m = 6$ arêtes", 36, {"sommets": SOMMET, "arêtes": ACCENT}
        ).move_to(RIGHT * 3.6 + UP * 1.2)
        self.play(FadeIn(info_g, shift=LEFT * 0.3))
        detail = self.detail(None, "Ce graphe contient un cycle : A – B – E – F – C – A", ["cycle"])
        cycle = [("A", "B"), ("B", "E"), ("E", "F"), ("C", "F"), ("A", "C")]
        self.play(*[h.edges[e].animate.set_color(ROUGE).set_stroke(width=8) for e in cycle])
        self.wait(3)
        detail = self.detail(
            detail, "Un arbre couvrant garde les 6 sommets avec n − 1 = 5 arêtes : retirons E–F", ["n − 1 = 5", "E–F"]
        )
        self.play(
            *[h.edges[e].animate.set_color(ACCENT).set_stroke(width=8) for e in cycle if e != ("E", "F")],
            h.edges[("B", "D")].animate.set_color(ACCENT).set_stroke(width=8),
            h.edges[("E", "F")].animate.set_stroke(color=ROUGE, width=3, opacity=0.5),
        )
        info_t = tex(
            r"$T$ : $m' = 5 = n - 1$ arêtes", 36, {"arêtes": ACCENT}
        ).move_to(RIGHT * 3.6 + UP * 0.2)
        self.play(FadeIn(info_t, shift=LEFT * 0.3))
        self.wait(3.5)
        detail = self.detail(
            detail, "Plus de cycle, tout reste connecté : c'est un arbre couvrant de G", ["arbre couvrant"]
        )
        self.play(*[Indicate(h.vertices[v], color=VERT, scale_factor=1.25) for v in SOMMETS_P])
        self.wait(2.5)
        detail = self.detail(
            detail, "Il n'est pas unique : retirons plutôt C–F pour en obtenir un autre", ["pas unique", "C–F"]
        )
        self.play(
            h.edges[("E", "F")].animate.set_color(ACCENT).set_stroke(width=8, opacity=1),
            h.edges[("C", "F")].animate.set_stroke(color=ROUGE, width=3, opacity=0.5),
        )
        self.wait(3.5)
        detail = self.detail(
            detail,
            "Le parcours en largeur (BFS) et en profondeur (DFS) construisent chacun un arbre couvrant",
            ["BFS", "DFS"],
        )
        self.wait(4)
        self.play(FadeOut(detail))
