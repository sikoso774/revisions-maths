"""Chapitre 17 : modéliser un problème en plus court chemin (TD2, exercice 5 : Guérande, exercice 6 : Rémi)."""
from algo import *

# ── Exercice 5 : les foires de Guérande ─────────────────────────────────────────
ARCS_G = [
    (0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 7), (4, 8), (5, 8),
    (5, 9), (5, 10), (6, 10), (7, 11), (8, 11), (8, 12), (8, 13), (9, 13), (10, 13), (10, 14),
]
PEAGE = {1: 10, 2: 12, 3: 15, 4: 5, 5: 15, 6: 10, 7: 3, 8: 10, 9: 5, 10: 20, 11: 4, 12: 5, 13: 20, 14: 7}
GAIN = {11: 550, 12: 580, 13: 590, 14: 600}
VILLES = {11: "Rennes", 12: "Loudéac", 13: "Pontivy", 14: "Lorient"}
CONSTANTE = 600  # poids des arcs finaux : 600 − gain
POS_G = {
    0: [-6.4, 0.2, 0], 1: [-5.0, 1.8, 0], 2: [-5.0, 0.4, 0], 3: [-5.0, -1.0, 0],
    4: [-3.6, 1.4, 0], 5: [-3.6, -0.2, 0], 6: [-3.6, -1.5, 0],
    7: [-2.2, 2.0, 0], 8: [-2.2, 0.7, 0], 9: [-2.2, -0.6, 0], 10: [-2.2, -1.6, 0],
    11: [-0.6, 2.0, 0], 12: [-0.6, 0.7, 0], 13: [-0.6, -0.6, 0], 14: [-0.6, -1.6, 0],
    "ω": [1.4, 0.2, 0],
}
POS_G = {v: np.array(p, dtype=float) for v, p in POS_G.items()}
POIDS_G = {(a, b): PEAGE[b] for a, b in ARCS_G}  # un arc coûte le péage de la ville d'arrivée
POIDS_G.update({(f, "ω"): CONSTANTE - g for f, g in GAIN.items()})

# ── Exercice 6 : les chalets de Rémi ─────────────────────────────────────────────
# (de, vers, km) : la route descend de « de » vers « vers »
DESCENTES = [("R", "G", 2), ("R", "J", 1), ("N", "R", 3), ("N", "J", 2), ("J", "G", 2), ("G", "O", 1), ("L", "O", 2), ("N", "L", 2)]
POS_R = {
    "N": np.array([-0.8, 1.9, 0]), "R": np.array([-4.8, 0.6, 0]), "J": np.array([-1.8, 0.3, 0]),
    "G": np.array([-3.4, -1.4, 0]), "O": np.array([0.9, -1.4, 0]), "L": np.array([3.4, 0.5, 0]),
}
POIDS_R = {}
for haut, bas, km in DESCENTES:
    POIDS_R[(haut, bas)] = km          # descente : 1 unité par km
    POIDS_R[(bas, haut)] = 2 * km      # montée : deux fois plus lente


def etiquette_dist(sommet, valeur):
    """Distance courante affichée au-dessus d'un sommet."""
    return Text(str(valeur), font_size=22, color=ACCENT, weight=BOLD).next_to(sommet, UP, buff=0.08)


class Modelisation(SceneGraphes):
    # ---------- théorie ----------
    def theorie(self):
        carte = self.carte(
            "Ramener un problème à un plus court chemin",
            ACCENT,
            [
                tex(r"$\text{coût}(P)=\sum_{a\in P} w(a)$", 46),
                tex(r"minimiser un coût $\;\Longleftrightarrow\;$ plus court chemin", 40, {"plus court chemin": VERT}),
            ],
            [
                texte("1. Les sommets sont les situations : villes, chalets, étapes", 26, ["1."]),
                texte("2. Les arcs sont les déplacements possibles, leur poids est ce qu'on veut minimiser", 26, ["2."]),
                texte("3. Un sommet fictif d'arrivée relie toutes les sorties possibles", 26, ["3."]),
            ],
        )
        self.play(FadeOut(carte))
        return self.carte(
            "Quel algorithme choisir ?",
            VERT,
            [
                tex(r"$w\geq 0\;\Longrightarrow\;$ Dijkstra", 44, {"Dijkstra": SOMMET}),
                tex(r"$w<0$ possible $\;\Longrightarrow\;$ Bellman-Ford", 44, {"Bellman-Ford": VIOLET}),
            ],
            [
                texte("Poids tous positifs : Dijkstra, le plus simple et le plus rapide", 26, ["Dijkstra"]),
                texte("Astuce : si tous les chemins utilisent un arc d'un même groupe, on peut ajouter une constante", 26, ["Astuce"]),
            ],
        )

    # ---------- exercice 5 ----------
    def guerande(self, carte, titre):
        g = creer_graphe(list(POS_G), [*ARCS_G, *[(f, "ω") for f in GAIN]], POS_G, orientee=True, rayon=0.3)
        peages = {v: Text(str(p), font_size=18, color=ARETE).next_to(g.vertices[v], DOWN, buff=0.06) for v, p in PEAGE.items()}
        villes = VGroup(*[
            Text(f"{nom} ({n}) : {GAIN[n]} écus", font_size=22, color=TEXTE) for n, nom in VILLES.items()
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 0.6, 0])
        legende = self.legende("Gwendal part de Guérande (0) vendre son sel dans l'une des 4 foires", ["4 foires"])
        # d'abord le réseau de villes (sans le sommet d'arrivée ω, ajouté plus tard dans la modélisation)
        reseau = Succession(
            LaggedStart(*[GrowFromCenter(v) for k, v in g.vertices.items() if k != "ω"], lag_ratio=0.1),
            LaggedStart(*[Create(e) for k, e in g.edges.items() if k[1] != "ω"], lag_ratio=0.1),
        )
        self.dezoom(carte, reseau, FadeIn(villes), FadeIn(legende))
        self.wait(2.0)

        legende = self.changer(legende, self.legende("Il paie un péage à l'entrée de chaque ville, ville d'arrivée comprise", ["péage"]))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in peages.values()], lag_ratio=0.1), run_time=2.5)
        self.wait(2.0)

        legende = self.changer(legende, self.legende("Son bénéfice : le gain de la foire moins les péages payés", ["bénéfice"]))
        detail = self.detail(None, tex(r"$\text{bénéfice}=\text{gain}-\sum\text{péages}$", 42))
        self.wait(4.0)
        legende = self.changer(legende, self.legende("Maximiser le bénéfice, c'est minimiser « péages − gain »", ["minimiser"]))
        detail = self.detail(detail, tex(r"$\max(\text{gain}-\text{péages})\;\Longleftrightarrow\;\min(\text{péages}-\text{gain})$", 42))
        self.wait(4.0)

        # poids des arcs : le péage de la ville d'arrivée
        legende = self.changer(legende, self.legende("Chaque arc a pour poids le péage de la ville où il arrive", ["le péage de la ville où il arrive"]))
        exemple = arete(g, 1, 4)
        poids_exemple = etiquette_sur(exemple, PEAGE[4])
        self.play(Indicate(exemple, color=ACCENT, scale_factor=1.0), FadeIn(poids_exemple))
        detail = self.detail(detail, tex(r"$w(i\to j)=\text{péage}(j)\qquad w(1\to 4)=5$", 44))
        self.wait(4.5)
        # le poids de chaque arc remplace les péages affichés sous les villes
        poids_arcs = {k: etiquette_sur(arete(g, *k), w, taille=18) for k, w in POIDS_G.items() if k[1] != "ω"}
        self.play(FadeOut(poids_exemple), *[FadeOut(p) for p in peages.values()],
                  *[FadeIn(e) for e in poids_arcs.values()], run_time=1.5)
        self.wait(3.0)

        # sommet fictif d'arrivée
        legende = self.changer(legende, self.legende("On ajoute un sommet d'arrivée ω, relié aux 4 foires, qui porte le gain", ["sommet d'arrivée ω"]))
        arcs_finaux = [arete(g, f, "ω") for f in GAIN]
        poids_finaux = [etiquette_sur(arete(g, f, "ω"), CONSTANTE - GAIN[f], couleur=VIOLET) for f in GAIN]
        self.play(GrowFromCenter(g.vertices["ω"]), *[Create(a) for a in arcs_finaux])
        self.play(*[a.animate.set_color(VIOLET) for a in arcs_finaux], *[FadeIn(p) for p in poids_finaux])
        detail = self.detail(detail, tex(r"$w(f\to\omega)=600-\text{gain}(f)$", 44, {r"600": VIOLET}))
        self.wait(4.0)
        legende = self.changer(legende, self.legende("Tous les trajets prennent exactement un arc final : la constante 600 ne change pas le meilleur", ["exactement un arc final"]))
        detail = self.detail(detail, tex(r"$\text{coût du trajet}=\sum\text{péages}+600-\text{gain}$", 42))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Tous les poids sont positifs ou nuls : on applique l'algorithme de Dijkstra", ["Dijkstra"]))
        self.wait(3.0)

        detail = self.executer_dijkstra(g, peages, detail, legende)
        return g, detail

    def executer_dijkstra(self, g, peages, detail, legende):
        dist = {0: 0}
        parent = {}
        fait = set()
        etiquettes = {0: etiquette_dist(g.vertices[0], 0)}
        sortants = {}
        for (a, b), w in POIDS_G.items():
            sortants.setdefault(a, []).append((b, w))
        self.play(colorier(g, 0, ACCENT), FadeIn(etiquettes[0]))
        detail = self.detail(detail, "Départ : la distance de Guérande (0) est 0", ["Départ"])
        self.wait(2.0)

        while len(fait) < len(dist):
            u = min((v for v in dist if v not in fait), key=lambda v: (dist[v], str(v)))
            fait.add(u)
            nom = "ω" if u == "ω" else str(u)
            animations = [colorier(g, u, VERT)]
            for v, w in sortants.get(u, []):
                if v not in dist or dist[u] + w < dist[v]:
                    ancien = dist.get(v)
                    dist[v] = dist[u] + w
                    parent[v] = u
                    nouveau = etiquette_dist(g.vertices[v], dist[v])
                    if ancien is None:
                        etiquettes[v] = nouveau
                        animations += [FadeIn(nouveau, scale=0.8), colorier(g, v, ACCENT)]
                    else:
                        animations.append(Transform(etiquettes[v], nouveau))
                    animations.append(Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0))
            detail = self.detail(detail, f"On retient {nom} : sa distance est définitive, {dist[u]}", ["définitive"])
            self.play(*animations, run_time=1.2)
            self.wait(0.9)

        legende = self.changer(legende, self.legende("Le meilleur trajet est celui qui arrive en ω avec la plus petite distance", ["ω"]))
        chemin = ["ω"]
        while chemin[-1] != 0:
            chemin.append(parent[chemin[-1]])
        chemin.reverse()
        detail = self.detail(detail, f"Distance de ω : {dist['ω']}", ["Distance de ω"])
        self.play(*[arete(g, a, b).animate.set_color(ACCENT).set_stroke(width=9) for a, b in zip(chemin, chemin[1:])])
        self.wait(2.5)
        legende = self.changer(legende, self.legende("Gwendal va à Loudéac (12) par 0, 1, 4, 8 : péages 10 + 5 + 10 + 5 = 30", ["Loudéac (12)", "30"]))
        detail = self.detail(detail, tex(r"$d(\omega)=50\;\Longrightarrow\;\text{bénéfice}=600-50=550$ écus", 44, {r"550": ACCENT}))
        self.wait(6.0)
        legende = self.changer(legende, self.legende("Vérification : 580 écus de gain moins 30 de péages = 550", ["550"]))
        self.wait(4.0)
        return detail

    # ---------- exercice 6 ----------
    def chalets(self, titre):
        noeuds = {v: LabeledDot(Text(v, font_size=28, color=FOND, weight=BOLD), radius=0.3, fill_color=NOEUD) for v in POS_R}
        for v, n in noeuds.items():
            n.move_to(POS_R[v])
            n.set_z_index(2)
        legende = self.legende("Rémi habite en montagne : 6 chalets, tous à des altitudes différentes", ["6 chalets"])
        descentes = {(h, b): arc_entre(POS_R[h], POS_R[b], couleur=SOMMET) for h, b, _ in DESCENTES}
        etiq_km = {(h, b): etiquette_sur(descentes[(h, b)], f"{km} km", taille=20, couleur=SOMMET) for h, b, km in DESCENTES}
        self.play(*[GrowFromCenter(n) for n in noeuds.values()], FadeIn(legende))
        self.play(*[Create(a) for a in descentes.values()], *[FadeIn(e) for e in etiq_km.values()], run_time=2.5)
        legende = self.changer(legende, self.legende("Chaque route est dessinée dans le sens de la descente, avec sa longueur en km", ["sens de la descente"]))
        self.wait(5.0)

        # le modèle : deux arcs par route
        legende = self.changer(legende, self.legende("À pied, Rémi va deux fois plus vite en descente qu'en montée", ["deux fois plus vite"]))
        detail = self.detail(None, tex(r"$\text{temps de descente}=d\qquad\text{temps de montée}=2d$", 42, {r"2d": ROUGE}))
        self.wait(4.0)
        legende = self.changer(legende, self.legende("Chaque route donne deux arcs : un en descente, un en montée", ["deux arcs"]))
        arcs, etiquettes = {}, {}
        for (a, b), w in POIDS_R.items():
            descente = (a, b) in descentes
            arcs[(a, b)] = arc_entre(POS_R[a], POS_R[b], angle=0.45, couleur=SOMMET if descente else ROUGE, epaisseur=3)
            etiquettes[(a, b)] = etiquette_sur(arcs[(a, b)], w, taille=20, couleur=SOMMET if descente else ROUGE)
        self.play(*[FadeOut(a) for a in descentes.values()], *[FadeOut(e) for e in etiq_km.values()])
        self.play(*[Create(a) for a in arcs.values()], *[FadeIn(e) for e in etiquettes.values()], run_time=3.0)
        detail = self.detail(detail, tex(r"$w(\text{descente})=d\qquad w(\text{montée})=2d$", 44, {r"2d": ROUGE}))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Poids positifs : on applique Dijkstra depuis R, l'unité étant le temps pour descendre 1 km", ["Dijkstra"]))
        self.wait(3.0)

        # Dijkstra depuis R
        dist = {"R": 0}
        parent = {}
        fait = set()
        etiq_dist = {"R": etiquette_dist(noeuds["R"], 0)}
        sortants = {}
        for (a, b), w in POIDS_R.items():
            sortants.setdefault(a, []).append((b, w))
        self.play(noeuds["R"].animate.set_fill(ACCENT, family=False), FadeIn(etiq_dist["R"]))
        detail = self.detail(detail, "Départ : la distance de R est 0", ["Départ"])
        self.wait(2.0)
        while len(fait) < len(dist):
            u = min((v for v in dist if v not in fait), key=lambda v: (dist[v], v))
            fait.add(u)
            animations = [noeuds[u].animate.set_fill(VERT, family=False)]
            maj = []
            for v, w in sortants[u]:
                if v in fait:
                    continue
                if v not in dist or dist[u] + w < dist[v]:
                    ancien = dist.get(v)
                    dist[v] = dist[u] + w
                    parent[v] = u
                    nouveau = etiquette_dist(noeuds[v], dist[v])
                    if ancien is None:
                        etiq_dist[v] = nouveau
                        animations += [FadeIn(nouveau, scale=0.8), noeuds[v].animate.set_fill(ACCENT, family=False)]
                    else:
                        animations.append(Transform(etiq_dist[v], nouveau))
                    animations.append(Indicate(arcs[(u, v)], color=ACCENT, scale_factor=1.0))
                    maj.append(v)
            texte_etape = f"On retient {u} (temps {dist[u]})" + (" : on met à jour " + ", ".join(maj) if maj else "")
            detail = self.detail(detail, texte_etape, [f"temps {dist[u]}"])
            self.play(*animations, run_time=1.3)
            self.wait(1.2)

        legende = self.changer(legende, self.legende("Résultat : le meilleur trajet depuis R vers chaque copain", ["le meilleur trajet"]))
        chemins = []
        for v in ("J", "G", "O", "N", "L"):
            c = [v]
            while c[-1] != "R":
                c.append(parent[c[-1]])
            chemins.append(c[::-1])
        arcs_choisis = {(a, b) for c in chemins for a, b in zip(c, c[1:])}
        self.play(*[arcs[k].animate.set_stroke(width=8) for k in arcs_choisis],
                  *[arcs[k].animate.set_stroke(opacity=0.15) for k in arcs if k not in arcs_choisis],
                  *[etiquettes[k].animate.set_opacity(0.15) for k in arcs if k not in arcs_choisis])
        detail = self.detail(detail, tex(r"$J:1\quad G:2\quad O:3\quad N:5\quad L:7$", 46, {r"7": ACCENT}))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Vers N, le détour par J (1 + 4 = 5) bat la route directe (6)", ["N", "5"]))
        self.wait(4.0)
        legende = self.changer(legende, self.legende("Vers L, deux trajets sont à égalité : par G et O, ou par J et N (7 dans les deux cas)", ["à égalité"]))
        self.play(arcs[("N", "L")].animate.set_stroke(width=8, opacity=1), etiquettes[("N", "L")].animate.set_opacity(1))
        self.wait(5.0)

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Modéliser en plus court chemin", 17)
        carte = self.theorie()
        g, detail = self.guerande(carte, titre)
        self.vider(titre)
        self.chalets(titre)
        self.fin()
