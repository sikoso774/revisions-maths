from algo import *

INF = float("inf")

# Graphe pondéré d'étude (planaire, une relaxation « améliore » deux sommets : D et F)
SOMMETS_D = list("ABCDEF")
ARETES_D = [
    ("A", "B", 7), ("A", "C", 9), ("A", "F", 14), ("B", "C", 10), ("B", "D", 15),
    ("C", "D", 11), ("C", "F", 2), ("D", "E", 6), ("E", "F", 9),
]
POS_D = {
    "A": LEFT * 6.0 + UP * 0.2,
    "B": LEFT * 4.8 + UP * 1.8,
    "C": LEFT * 3.9 + UP * 0.3,
    "D": LEFT * 2.6 + UP * 1.8,
    "E": LEFT * 1.4 + UP * 0.2,
    "F": LEFT * 3.0 + DOWN * 1.5,
}
COTES_D = {"A": DOWN, "B": UP, "C": RIGHT, "D": UP, "E": RIGHT, "F": DOWN}

# L'exemple filé de ta note : quatre villes
VILLES = ["Paris", "Lyon", "Marseille", "Nice"]
ROUTES = [("Paris", "Lyon", 460), ("Lyon", "Marseille", 315), ("Lyon", "Nice", 470), ("Marseille", "Nice", 200)]
POS_V = {
    "Paris": LEFT * 5.2 + UP * 0.4,
    "Lyon": LEFT * 1.6 + UP * 0.4,
    "Marseille": RIGHT * 2.6 + UP * 1.7,
    "Nice": RIGHT * 2.6 + DOWN * 0.9,
}

LIGNES_DIJKSTRA = [
    (0, "d[v] ← ∞ pour tout v ; d[s] ← 0"),
    (0, "N ← tous les sommets"),
    (0, "tant que N n'est pas vide :"),
    (1, "u ← sommet de N avec d[u] minimal"),
    (1, "retirer u de N (d[u] définitif)"),
    (1, "pour chaque voisin v de u dans N :"),
    (2, "si d[u] + w(u,v) < d[v] :"),
    (3, "d[v] ← d[u] + w(u,v)"),
    (3, "parent[v] ← u"),
]


def valeur(x, unite=""):
    return "∞" if x == INF else f"{x}{unite}"


class Dijkstra(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "Le problème",
            SOMMET,
            [
                tex(r"$w(\mu) = \displaystyle\sum_{i=1}^{k} w(x_{i-1}, x_i)$", 44),
                tex(r"$\delta(s, v) = \min \{\, w(\mu) \mid \mu \text{ chemin de } s \text{ à } v \,\}$", 42),
            ],
            [
                tex(r"Graphe pondéré : chaque arête $e$ a un poids $w(e) \geq 0$ (distance, coût, temps)", 32, {"poids": ACCENT}),
                tex(r"$\delta(s, v)$ : la plus courte distance de $s$ à $v$ ; le BFS est le cas où tous les poids valent $1$", 30, {"plus courte distance": VERT}),
                tex(r"Condition de Dijkstra : poids positifs ou nuls (sinon, on utilise Bellman-Ford)", 32, {"positifs": ROUGE}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Le principe",
            VERT,
            [
                tex(r"$d[s] = 0 \qquad d[v] = +\infty \ \ (v \neq s)$", 44),
                tex(r"$d[v] \leftarrow \min\big(d[v],\ d[u] + w(u, v)\big)$", 44),
            ],
            [
                tex(r"$d[v]$ : la meilleure distance connue pour l'instant, toujours $\geq \delta(s, v)$", 32, {"meilleure distance": ACCENT}),
                tex(r"On fixe le sommet non visité $u$ de $d[u]$ minimal : alors $d[u] = \delta(s, u)$", 32, {"minimal": VERT}),
                tex(r"Complexité : $O((n + m) \log n)$ avec un tas binaire pour trouver le minimum", 32, {"tas binaire": VIOLET}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("L'algorithme de Dijkstra", 10)

        g = creer_graphe(SOMMETS_D, [(u, v) for u, v, _ in ARETES_D], POS_D)
        legende = self.legende("Trouver le chemin le moins coûteux", ["moins coûteux"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        poids = VGroup(*[etiquette_poids(g, u, v, w) for u, v, w in ARETES_D])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in poids], lag_ratio=0.15))
        self.wait(1)

        legende = self.changer(
            legende, self.legende("L'algorithme : un pseudo-code et des distances provisoires", ["pseudo-code", "distances provisoires"])
        )
        code = PanneauCode("Dijkstra(G, w, s)", LIGNES_DIJKSTRA, coin=(0.35, 2.25))
        self.play(*code.montrer(), run_time=1.5)
        self.det = self.detail(
            None, "Graphe pondéré, source s = A : on cherche les plus courtes distances depuis A", ["s = A"]
        )
        self.wait(4)
        legende = self.changer(
            legende,
            self.legende(
                "Blanc : pas fixé · Bleu : choisi · Vert : distance définitive",
                {"Bleu": SOMMET, "Vert": VERT},
            ),
        )

        def etiqueter(v, val, couleur):
            return Text(f"d = {valeur(val)}", font_size=22, color=couleur, weight=BOLD).next_to(
                g.vertices[v], COTES_D[v], buff=0.12
            )

        d, parent = self.executer(g, SOMMETS_D, ARETES_D, "A", etiqueter, code)
        self.conclure(g, d, parent, code)
        legende = self.exemple_villes(legende, titre)
        self.fin(3)

    # ---------- outils ----------
    def dire(self, contenu, cles=None):
        self.det = self.detail(self.det, contenu, cles)

    # ---------- exécution pas à pas (générique : sert aussi pour les villes) ----------
    def executer(self, g, sommets, aretes, source, etiqueter, code=None):
        adj = {v: [] for v in sommets}
        for u, v, w in aretes:
            adj[u].append((v, w))
            adj[v].append((u, w))
        for v in adj:
            adj[v].sort()
        d = {v: INF for v in sommets}
        d[source] = 0
        visites, parent = set(), {}

        def ligne(i):
            return [code.aller_a(i)] if code else []

        def jouer(*animations, **options):
            if animations:  # sans pseudo-code (exemple des villes), certaines étapes sont vides
                self.play(*animations, **options)

        labels = {v: etiqueter(v, d[v], ACCENT) for v in sommets}
        self.dire(f"Initialisation : toutes les distances valent ∞, sauf d[{source}] = 0", ["∞", f"d[{source}] = 0"])
        self.play(*ligne(0), LaggedStart(*[FadeIn(l, scale=0.8) for l in labels.values()], lag_ratio=0.1))
        self.wait(3)
        self.dire("N est l'ensemble des sommets pas encore fixés : au début, tous", ["N"])
        jouer(*ligne(1))
        self.wait(2.5)

        while len(visites) < len(sommets):
            jouer(*ligne(2))
            u = min((v for v in sommets if v not in visites), key=lambda v: (d[v], v))
            self.dire(
                f"Parmi les sommets non visités, {u} est le plus proche : d[{u}] = {valeur(d[u])}",
                {"le plus proche": ACCENT},
            )
            self.play(*ligne(3), colorier(g, u, SOMMET), Indicate(labels[u], color=ACCENT))
            self.wait(2)
            visites.add(u)
            self.dire(f"On le retire de N : sa distance {valeur(d[u])} est définitive", ["définitive"])
            self.play(*ligne(4), colorier(g, u, VERT), Transform(labels[u], etiqueter(u, d[u], VERT)))
            self.wait(1.8)

            voisins = [(v, w) for v, w in adj[u] if v not in visites]
            if not voisins:
                self.dire("Aucun voisin non fixé : il n'y a rien à mettre à jour", ["rien à mettre à jour"])
                jouer(*ligne(5))
                self.wait(2)
                continue
            if len(visites) == 2:
                self.dire("On ne regarde que les voisins pas encore fixés : les autres sont déjà optimaux", ["pas encore fixés"])
                self.wait(2.5)
            for v, w in voisins:
                self.play(*ligne(5), Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0), run_time=1)
                candidat = d[u] + w
                avant = d[v]
                jouer(*ligne(6), run_time=0.6)
                calcul = f"d[{u}] + w({u},{v}) = {d[u]} + {w} = {candidat}"
                if candidat < avant:
                    if avant == INF:
                        self.dire(f"{calcul} < ∞ : première estimation, d[{v}] = {candidat}", {"première estimation": VERT})
                    else:
                        self.dire(
                            f"{calcul} < {avant} : meilleur chemin, d[{v}] passe de {avant} à {candidat}",
                            {"meilleur chemin": VERT},
                        )
                    self.wait(1.8)
                    d[v] = candidat
                    ancien = (
                        [arete(g, parent[v], v).animate.set_color(LIEN).set_stroke(width=5)]
                        if v in parent
                        else []
                    )
                    parent[v] = u
                    self.play(*ligne(7), Transform(labels[v], etiqueter(v, candidat, ACCENT)))
                    self.play(*ligne(8), arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=8), *ancien)
                    self.wait(1.2)
                else:
                    self.dire(f"{calcul} ≥ {avant} : pas mieux, d[{v}] reste {avant}", {"pas mieux": ROUGE})
                    self.wait(2.2)
        jouer(*ligne(2))
        return d, parent

    # ---------- bilan sur le graphe d'étude ----------
    def conclure(self, g, d, parent, code):
        self.dire("N est vide : toutes les distances sont définitives", ["définitives"])
        self.wait(3.5)
        legende = None  # la légende reste celle des couleurs ; on ne la change pas ici

        chemin = ["E"]
        while chemin[-1] in parent:
            chemin.append(parent[chemin[-1]])
        chemin.reverse()
        self.dire(
            f"Plus court chemin de A à E : on remonte les parents, soit {' → '.join(chemin)} de longueur 9 + 2 + 9 = {d['E']}",
            [" → ".join(chemin), f"{d['E']}"],
        )
        self.play(
            *[arete(g, u, v).animate.set_color(VERT).set_stroke(width=10) for u, v in zip(chemin, chemin[1:])],
        )
        self.wait(5)
        self.dire(
            "A – F – E n'a que 2 arêtes mais pèse 14 + 9 = 23 : un BFS se tromperait, il ignore les poids",
            ["23", "BFS"],
        )
        self.play(arete(g, "A", "F").animate.set_color(ROUGE).set_stroke(width=8))
        self.wait(5)
        self.play(arete(g, "A", "F").animate.set_color(LIEN).set_stroke(width=5))
        self.dire(
            "Le minimum est cherché à chaque tour : avec un tas binaire, le coût total est O((n + m) log n)",
            ["tas binaire", "O((n + m) log n)"],
        )
        self.wait(5)
        self.dire(
            "Attention : les poids doivent être positifs ou nuls ; sinon, il faut Bellman-Ford",
            ["positifs", "Bellman-Ford"],
        )
        self.wait(5)
        self.play(*code.cacher())

    # ---------- l'exemple filé de la note : Paris → Nice ----------
    def exemple_villes(self, legende, titre):
        legende = self.changer(
            legende,
            self.legende("Ton exemple filé : de Paris à Nice au plus court", {"Paris": ACCENT, "Nice": ACCENT}),
        )
        garder = {titre, self.trait_titre, legende}
        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in garder])), run_time=1.2)

        g = Graph(
            VILLES,
            [(a, b) for a, b, _ in ROUTES],
            layout=POS_V,
            vertex_config={"radius": 0.18, "fill_color": NOEUD},
            edge_config={"stroke_color": LIEN, "stroke_width": 5},
        )
        for sommet in g.vertices.values():
            sommet.set_z_index(2)
        cotes = {"Paris": UP, "Lyon": UP, "Marseille": RIGHT, "Nice": RIGHT}
        noms = {
            v: Text(v, font_size=28, weight=BOLD, color=TEXTE).next_to(g.vertices[v], cotes[v], buff=0.2)
            for v in VILLES
        }
        ancres = {
            v: (g.vertices[v].get_center() + DOWN * 0.55) if cotes[v] is UP else (noms[v].get_center() + DOWN * 0.45)
            for v in VILLES
        }
        poids = VGroup(*[etiquette_poids(g, a, b, f"{w} km") for a, b, w in ROUTES])
        self.play(apparition(g), LaggedStart(*[FadeIn(n) for n in noms.values()], lag_ratio=0.2), run_time=2.5)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in poids], lag_ratio=0.2))
        self.det = self.detail(
            None, "Quatre villes et leurs routes : Dijkstra donne la distance la plus courte depuis Paris", ["Dijkstra"]
        )
        self.wait(3.5)

        def etiqueter(v, val, couleur):
            return Text(f"d = {valeur(val, ' km')}", font_size=24, color=couleur, weight=BOLD).move_to(ancres[v])

        d, parent = self.executer(g, VILLES, ROUTES, "Paris", etiqueter, None)
        self.dire(
            "Paris → Lyon → Nice : 460 + 470 = 930 km, contre 975 km en passant par Marseille",
            ["930 km", "975 km"],
        )
        chemin = [("Paris", "Lyon"), ("Lyon", "Nice")]
        self.play(*[arete(g, u, v).animate.set_color(VERT).set_stroke(width=10) for u, v in chemin])
        self.wait(6)
        self.play(FadeOut(self.det))
        return legende
