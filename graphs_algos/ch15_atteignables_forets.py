"""Chapitre 15 : sommets atteignables et forêts (TD1, exercice 3 question 1 et exercice 4 questions 1 et 2)."""
from algo import *

# ── Le graphe orienté de l'exercice 3 du TD1 : 14 sommets, 23 arcs ──────────────────────
ARCS_14 = [
    (1, 2), (5, 1), (5, 2), (5, 6), (6, 2), (2, 3), (2, 7), (3, 4), (4, 3), (3, 9), (8, 3), (7, 6),
    (7, 8), (9, 8), (6, 11), (10, 6), (10, 11), (10, 13), (12, 9), (12, 14), (14, 12), (13, 14), (14, 13),
]
DOUBLES = {(3, 4), (4, 3), (12, 14), (14, 12), (13, 14), (14, 13)}  # arcs dessinés en courbe : les deux sens existent
COLONNES = {1: 0, 5: 0, 10: 0, 2: 1, 6: 1, 11: 1, 13: 1, 3: 2, 7: 2, 12: 2, 14: 2, 4: 3, 8: 3, 9: 4}
LIGNES = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 2, 11: 2, 12: 2, 13: 3, 14: 3}
POS_14 = {v: np.array([-6.2 + 1.45 * COLONNES[v], 2.0 - 1.1 * LIGNES[v], 0]) for v in COLONNES}
SOURCE = 10

# ── Une forêt de 10 sommets et 3 arbres ────────────────────────────────────────────────
SOMMETS_F = list(range(1, 11))
ARETES_F = [(1, 2), (1, 3), (3, 4), (5, 6), (5, 7), (8, 9), (9, 10)]
ARETES_AJOUTEES = [(3, 5), (7, 8), (2, 4)]  # deux arêtes qui relient des arbres, puis une qui crée un cycle
POS_F = {
    1: [-4.6, 1.2, 0], 2: [-5.6, -0.2, 0], 3: [-3.6, -0.2, 0], 4: [-3.6, -1.4, 0],
    5: [-0.2, 1.2, 0], 6: [-1.0, -0.2, 0], 7: [0.6, -0.2, 0],
    8: [3.4, 0.6, 0], 9: [4.6, 0.6, 0], 10: [5.8, 0.6, 0],
}
POS_F = {v: np.array(p, dtype=float) for v, p in POS_F.items()}
COMPOSANTES = [([1, 2, 3, 4], VERT), ([5, 6, 7], SOMMET), ([8, 9, 10], VIOLET)]

LIGNES_MARQUAGE = [
    (0, "marquer s"),
    (0, "tant qu'il existe un arc (u, v)"),
    (1, "avec u marqué et v non marqué :"),
    (2, "marquer v"),
    (0, "résultat : les sommets marqués"),
]


class AtteignablesForets(SceneGraphes):
    # ---------- théorie ----------
    def theorie(self):
        carte = self.carte(
            "Les sommets atteignables depuis s",
            SOMMET,
            [
                tex(r"$\mathrm{Acc}(s)=\{\,v\in V \mid \text{il existe un chemin de } s \text{ à } v\,\}$", 38, {r"\mathrm{Acc}(s)": SOMMET}),
            ],
            [
                texte("On marque s, puis tout successeur d'un sommet déjà marqué, jusqu'à ne plus pouvoir", 26, ["On marque s"]),
                texte("C'est exactement ce que fait un parcours (BFS ou DFS) à partir de s", 26, ["parcours"]),
                texte("Chaque sommet et chaque arc sont vus une fois : O(n + m)", 26, ["O(n + m)"]),
            ],
        )
        self.play(FadeOut(carte))
        return self.carte(
            "Forêt : des arbres disjoints",
            VERT,
            [
                tex(r"$m=n-k$", 54, {r"n-k": VERT}),
                tex(r"$m\geq n-k$, avec égalité si et seulement si $G$ est une forêt", 38, {"forêt": VERT}),
            ],
            [
                texte("n sommets, m arêtes et k composantes connexes", 26, ["k composantes connexes"]),
                texte("Un arbre de n sommets a n − 1 arêtes : en additionnant tous les arbres, on obtient n − k", 26, ["n − k"]),
                texte("Un arbre est le cas particulier k = 1 : m = n − 1", 26, ["m = n − 1"]),
            ],
        )

    # ---------- démonstration 1 : l'atteignabilité ----------
    def atteignables(self, carte, titre):
        noeuds = {v: LabeledDot(Text(str(v), font_size=28, color=FOND, weight=BOLD), radius=0.3, fill_color=NOEUD) for v in POS_14}
        for v, n in noeuds.items():
            n.move_to(POS_14[v])
            n.set_z_index(2)
        arcs = {}
        for (u, v) in ARCS_14:
            arcs[(u, v)] = arc_entre(POS_14[u], POS_14[v], angle=0.35 if (u, v) in DOUBLES else 0.0, rayon=0.3, epaisseur=3)
        legende = self.legende("Un graphe orienté à 14 sommets : quels sommets peut-on atteindre depuis 10 ?", ["atteindre depuis 10"])
        self.dezoom(
            carte,
            LaggedStart(*[GrowFromCenter(n) for n in noeuds.values()], lag_ratio=0.08),
            FadeIn(legende),
        )
        self.play(LaggedStart(*[Create(a) for a in arcs.values()], lag_ratio=0.05), run_time=3.0)
        self.wait(2.0)

        panneau = PanneauCode("Atteignables(G, s)", LIGNES_MARQUAGE, coin=(0.7, 2.35), largeur_max=6.0)
        legende = self.changer(legende, self.legende("On applique l'algorithme de marquage, avec s = 10", ["marquage", "s = 10"]))
        self.play(*panneau.montrer(), run_time=1.5)
        self.wait(2.5)

        marques = [SOURCE]
        ensemble = Tex(r"$M=\{10\}$", font_size=40, color=VERT).move_to([3.7, -0.35, 0])
        detail = self.detail(None, "On marque la source s = 10", ["s = 10"])
        self.play(panneau.aller_a(0), noeuds[SOURCE].animate.set_fill(ACCENT, family=False), FadeIn(ensemble))
        self.wait(2.5)

        file = [SOURCE]
        while file:
            u = file.pop(0)
            for v in sorted(w for (x, w) in ARCS_14 if x == u):
                self.play(panneau.aller_a(1), run_time=0.5)
                if v in marques:
                    continue
                self.play(panneau.aller_a(2), Indicate(arcs[(u, v)], color=ACCENT, scale_factor=1.0), run_time=0.9)
                marques.append(v)
                nouvel_ensemble = Tex("$M=\\{" + ",".join(str(x) for x in sorted(marques)) + "\\}$", font_size=40, color=VERT).move_to([3.7, -0.35, 0])
                if nouvel_ensemble.width > 6.0:
                    nouvel_ensemble.scale_to_fit_width(6.0)
                detail = self.detail(detail, f"L'arc ({u}, {v}) part d'un sommet marqué vers {v} : on marque {v}", [f"on marque {v}"])
                self.play(panneau.aller_a(3), noeuds[v].animate.set_fill(VERT, family=False), Transform(ensemble, nouvel_ensemble), run_time=1.1)
                self.wait(1.2)
                file.append(v)
        self.play(panneau.aller_a(4))
        legende = self.changer(legende, self.legende("Plus aucun arc ne sort de l'ensemble marqué : ce sont exactement les sommets atteignables", ["atteignables"]))
        detail = self.detail(detail, "12 sommets sont atteignables depuis 10 : tous sauf 1 et 5", ["tous sauf 1 et 5"])
        self.play(*[Indicate(noeuds[v], color=ROUGE, scale_factor=1.3) for v in (1, 5)])
        self.wait(4.0)
        legende = self.changer(legende, self.legende("5 mène à 1, mais aucun arc ne conduit à 5 ou à 1 depuis l'ensemble marqué", ["aucun arc"]))
        self.wait(5.0)
        self.vider(titre)

    # ---------- démonstration 2 : les forêts ----------
    def forets(self, titre):
        g = creer_graphe(SOMMETS_F, [*ARETES_F, *ARETES_AJOUTEES], POS_F, orientee=False, rayon=0.3)
        aretes = {a: arete(g, *a) for a in [*ARETES_F, *ARETES_AJOUTEES]}
        legende = self.legende("Une forêt : 10 sommets répartis en 3 arbres, sans aucun cycle", ["forêt", "3 arbres"])
        self.play(LaggedStart(*[GrowFromCenter(v) for v in g.vertices.values()], lag_ratio=0.08),
                  LaggedStart(*[Create(aretes[a]) for a in ARETES_F], lag_ratio=0.1), FadeIn(legende), run_time=3.0)
        self.wait(1.5)
        legende = self.changer(legende, self.legende("Chaque composante connexe est un arbre : on la colorie", ["composante connexe"]))
        self.play(*[colorier(g, v, couleur) for membres, couleur in COMPOSANTES for v in membres])
        self.wait(2.0)

        # un arbre de n_i sommets a n_i − 1 arêtes
        legende = self.changer(legende, self.legende("Un arbre de n sommets a n − 1 arêtes : on compte arbre par arbre", ["n − 1 arêtes"]))
        bilans = []
        for membres, couleur in COMPOSANTES:
            centre_x = sum(POS_F[v][0] for v in membres) / len(membres)
            bilan = Tex(rf"${len(membres)}-1={len(membres) - 1}$", font_size=36, color=couleur).move_to([centre_x, -2.0, 0])
            bilans.append(bilan)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bilans], lag_ratio=0.5), run_time=2.5)
        detail = self.detail(None, tex(r"$m=(4-1)+(3-1)+(3-1)=10-3=7$", 42, {r"10-3": ACCENT}))
        self.wait(4.5)

        compteurs = self.compteurs(10, 3, 7)
        self.play(FadeOut(VGroup(*bilans)), FadeIn(compteurs))
        legende = self.changer(legende, self.legende("En tout : n − k arêtes, avec n = 10 sommets et k = 3 composantes", ["n − k"]))
        detail = self.detail(detail, tex(r"$m=n-k=10-3=7$", 46, {r"n-k": VERT}))
        self.wait(4.0)

        # relier deux arbres : k diminue de 1, m augmente de 1
        legende = self.changer(legende, self.legende("Relier deux arbres par une arête : k baisse de 1, m monte de 1", ["k baisse de 1"]))
        self.play(Create(aretes[(3, 5)]), *[colorier(g, v, VERT) for v in (5, 6, 7)])
        compteurs = self.maj_compteurs(compteurs, 10, 2, 8)
        detail = self.detail(detail, tex(r"$m=n-k=10-2=8$", 46, {r"n-k": VERT}))
        self.wait(4.0)
        self.play(Create(aretes[(7, 8)]), *[colorier(g, v, VERT) for v in (8, 9, 10)])
        compteurs = self.maj_compteurs(compteurs, 10, 1, 9)
        legende = self.changer(legende, self.legende("Avec k = 1, on retrouve l'arbre : m = n − 1", ["m = n − 1"]))
        detail = self.detail(detail, tex(r"$m=n-k=10-1=9$", 46, {r"n-k": VERT}))
        self.wait(4.0)

        # une arête de trop crée un cycle
        legende = self.changer(legende, self.legende("Une arête de plus à l'intérieur d'un arbre crée un cycle : m dépasse n − k", ["cycle"]))
        self.play(Create(aretes[(2, 4)]))
        cycle = [(1, 2), (2, 4), (3, 4), (1, 3)]
        self.play(*[aretes[a].animate.set_color(ROUGE).set_stroke(width=8) for a in cycle])
        compteurs = self.maj_compteurs(compteurs, 10, 1, 10)
        detail = self.detail(detail, tex(r"$m=10>n-k=9$", 46, {r"10": ROUGE}))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("m − n + k compte les cycles indépendants : il vaut 0 exactement pour une forêt", ["0 exactement pour une forêt"]))
        detail = self.detail(detail, tex(r"$m-n+k\geq 0\qquad m-n+k=0\iff G\text{ est une forêt}$", 42, {r"=0": VERT}))
        self.wait(6.0)

    def compteurs(self, n, k, m):
        t = VGroup(
            Tex(f"$n={n}$", font_size=38, color=TEXTE),
            Tex(f"$k={k}$", font_size=38, color=VERT),
            Tex(f"$m={m}$", font_size=38, color=ACCENT),
        ).arrange(RIGHT, buff=1.0).move_to([0, 2.25, 0])
        return t

    def maj_compteurs(self, anciens, n, k, m):
        nouveaux = self.compteurs(n, k, m)
        self.play(Transform(anciens, nouveaux), run_time=0.9)
        return anciens

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Sommets atteignables et forêts", 15)
        carte = self.theorie()
        self.atteignables(carte, titre)
        self.forets(titre)
        self.fin()
