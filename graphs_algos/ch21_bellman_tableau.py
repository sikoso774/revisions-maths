"""Chapitre 21 : Bellman-Ford en tableau, corrigé du TD2 exercice 3 (graphe imprimé) puis variante de l'enseignant (circuit négatif)."""
from algo import *

INF = float("inf")
SOMMETS = ["s", 1, 2, 3, 4, 5, 6]
# Graphe imprimé sur la Feuille 2 (exercice 3) : (de, vers, longueur)
ARCS = [
    ("s", 1, 1), ("s", 2, 4), (1, 2, 1), (1, 3, 1), (1, 4, 3), (1, 5, -2),
    (3, 5, 1), (3, 6, 2), (5, 6, 8), (4, 5, 4), (4, 6, 4), (2, 4, -1),
]
# Variante vue en cours : l'arc 1 -> 5 de poids -2 est remplacé par un arc 5 -> 1 de poids -4
ARCS_VARIANTE = [a for a in ARCS if (a[0], a[1]) != (1, 5)] + [(5, 1, -4)]
POS = {
    "s": np.array([-6.5, 0.2, 0]), 1: np.array([-4.8, 1.5, 0]), 2: np.array([-4.8, -1.1, 0]),
    3: np.array([-2.8, 1.5, 0]), 4: np.array([-2.8, -1.1, 0]), 5: np.array([-2.8, 0.2, 0]), 6: np.array([-1.0, 0.2, 0]),
}
X_TABLEAU = 0.7
LARGEUR_TOTALE = 5.65


def valeur_tex(x):
    return r"\infty" if x == INF else str(x)


def iteration(arcs, pi, pred):
    """Une itération synchrone : toutes les valeurs sont recalculées à partir de la colonne précédente."""
    nouveau, nouveau_pred, changements = dict(pi), dict(pred), {}
    for v in SOMMETS:
        candidats = [(pi[u] + w, u) for (u, x, w) in arcs if x == v and pi[u] != INF]
        meilleur = min(candidats, default=(INF, None))
        if meilleur[0] < pi[v]:
            nouveau[v], nouveau_pred[v] = meilleur
            changements[v] = (meilleur[1], [c for c, _ in candidats])
    return nouveau, nouveau_pred, changements


class Tableau:
    """Tableau « π^k(·), pred(·) » : une ligne par sommet, une colonne par itération."""

    def __init__(self, nb_colonnes):
        self.n = nb_colonnes
        self.largeur = min(1.4, LARGEUR_TOTALE / nb_colonnes)
        self.x0 = X_TABLEAU + 0.55  # début des colonnes de données
        self.y_haut = 2.2
        self.pas_y = 0.5
        self.cellules = {}
        self.cadre = VGroup()
        self.entetes = VGroup()
        for k in range(1, nb_colonnes + 1):
            tete = Tex(rf"$\pi^{k}$", font_size=30, color=ACCENT).move_to(self.position(k, None))
            self.entetes.add(tete)
        for i, v in enumerate(SOMMETS):
            lab = Text(str(v), font_size=24, weight=BOLD, color=SOMMET if v != "s" else ACCENT)
            lab.move_to([X_TABLEAU + 0.2, self.y_haut - self.pas_y * (i + 1), 0])
            self.entetes.add(lab)
        largeur_tab = 0.55 + self.largeur * nb_colonnes
        haut, bas = self.y_haut + 0.28, self.y_haut - self.pas_y * (len(SOMMETS) + 0.5)
        self.cadre.add(Rectangle(width=largeur_tab, height=haut - bas, stroke_color=ARETE, stroke_width=2).move_to(
            [X_TABLEAU - 0.05 + largeur_tab / 2, (haut + bas) / 2, 0]))
        for k in range(1, nb_colonnes):
            x = self.x0 + self.largeur * k
            self.cadre.add(Line([x, haut, 0], [x, bas, 0], stroke_color=ARETE, stroke_width=1))
        self.cadre.add(Line([self.x0, haut, 0], [self.x0, bas, 0], stroke_color=ARETE, stroke_width=1))
        self.cadre.add(Line([X_TABLEAU - 0.05, self.y_haut - 0.25, 0], [X_TABLEAU - 0.05 + largeur_tab, self.y_haut - 0.25, 0],
                            stroke_color=ARETE, stroke_width=1))

    def position(self, k, v):
        x = self.x0 + self.largeur * (k - 0.5)
        y = self.y_haut if v is None else self.y_haut - self.pas_y * (SOMMETS.index(v) + 1)
        return np.array([x, y, 0])

    def cellule(self, k, v, valeur, pred, couleur):
        p = r"\emptyset" if pred is None else str(pred)
        t = Tex(rf"${valeur_tex(valeur)},\,{p}$", font_size=26 if self.n <= 5 else 22, color=couleur)
        if t.width > self.largeur - 0.08:
            t.scale_to_fit_width(self.largeur - 0.08)
        t.move_to(self.position(k, v))
        self.cellules[(k, v)] = t
        return t


class BellmanTableau(SceneGraphes):
    # ---------- théorie ----------
    def theorie(self):
        carte = self.carte(
            "Bellman-Ford en tableau",
            SOMMET,
            [
                tex(r"$\pi^0(s)=0\qquad\pi^0(v)=+\infty$", 44),
                tex(r"$\pi^k(v)=\min\bigl(\pi^{k-1}(v),\ \min_{(u,v)}\,\pi^{k-1}(u)+l(u,v)\bigr)$", 38, {r"\pi^{k-1}(u)+l(u,v)": ACCENT}),
            ],
            [
                texte("Une colonne par itération : tout est recalculé à partir de la colonne précédente", 26, ["Une colonne par itération"]),
                texte("Dans chaque case : la valeur π et le prédécesseur qui la donne", 26, ["prédécesseur"]),
                texte("Au plus n colonnes (n = nombre de sommets) : on s'arrête quand deux colonnes sont identiques", 26, ["Au plus n colonnes"]),
            ],
        )
        self.play(FadeOut(carte))
        return self.carte(
            "Lire le résultat",
            VERT,
            [
                tex(r"colonne $k$ = colonne $k-1$ $\;\Longrightarrow\;$ valeurs optimales", 40, {"valeurs optimales": VERT}),
                tex(r"colonne $n$ $\neq$ colonne $n-1$ $\;\Longrightarrow\;$ circuit négatif", 40, {"circuit négatif": ROUGE}),
            ],
            [
                texte("Les prédécesseurs forment alors l'arborescence des plus courts chemins", 26, ["arborescence"]),
                texte("Sinon, ils ne forment plus une arborescence : on retrouve le circuit négatif avec eux", 26, ["circuit négatif"]),
            ],
        )

    # ---------- graphe ----------
    def dessiner(self, arcs):
        g = creer_graphe(SOMMETS, [(u, v) for u, v, _ in arcs], POS, orientee=True, rayon=0.3)
        etiq = {(u, v): etiquette_sur(arete(g, u, v), str(w).replace("-", "−"), taille=20, couleur=ACCENT if w >= 0 else ROUGE) for u, v, w in arcs}
        return g, etiq

    # ---------- partie 1 : le graphe de la Feuille 2 ----------
    def partie_imprimee(self, carte, titre):
        g, etiq = self.dessiner(ARCS)
        legende = self.legende("TD2, exercice 3 : plus courts chemins depuis s, avec des poids négatifs (−1 et −2)", ["poids négatifs"])
        self.dezoom(
            carte,
            Succession(
                LaggedStart(*[GrowFromCenter(v) for v in g.vertices.values()], lag_ratio=0.1),
                LaggedStart(*[Create(a) for a in g.edges.values()], *[FadeIn(e) for e in etiq.values()], lag_ratio=0.05),
            ),
            FadeIn(legende),
        )
        self.wait(2.5)

        tab = Tableau(4)
        self.play(FadeIn(tab.cadre), FadeIn(tab.entetes))
        legende = self.changer(legende, self.legende("Départ : π(s) = 0 et π = +∞ ailleurs, tous les prédécesseurs sont vides", ["π(s) = 0"]))
        detail = self.detail(None, tex(r"$\pi^0=(0,\ \infty,\ \infty,\ \infty,\ \infty,\ \infty,\ \infty)$", 40))
        self.wait(4.0)

        pi = {v: INF for v in SOMMETS}
        pi["s"] = 0
        pred = {v: None for v in SOMMETS}
        for k in range(1, 5):
            legende = self.changer(legende, self.legende(f"Itération {k} : on recalcule chaque sommet avec la colonne {k - 1 if k > 1 else 0}", [f"Itération {k}"]))
            nouveau, nouveau_pred, changements = iteration(ARCS, pi, pred)
            # cases inchangées : recopiées en gris
            self.play(*[FadeIn(tab.cellule(k, v, nouveau[v], nouveau_pred[v], ARETE)) for v in SOMMETS if v not in changements], run_time=0.8)
            for v in SOMMETS:
                if v not in changements:
                    continue
                u, candidats = changements[v]
                termes = ",\\;".join(valeur_tex(c) for c in candidats)
                ancien = valeur_tex(pi[v])
                formule = rf"$\pi^{k}({v})=\min({ancien},\;{termes})={nouveau[v]}$"
                detail = self.detail(detail, tex(formule, 40))
                cellule = tab.cellule(k, v, nouveau[v], nouveau_pred[v], ACCENT)
                self.play(Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0), FadeIn(cellule), run_time=1.1)
                self.wait(1.4)
            if not changements:
                break
            pi, pred = nouveau, nouveau_pred
        legende = self.changer(legende, self.legende("La colonne 4 est identique à la colonne 3 : l'algorithme s'arrête, les valeurs sont optimales", ["identique"]))
        detail = self.detail(detail, "Aucun changement à l'itération 4 : pas de circuit négatif", ["pas de circuit négatif"])
        self.wait(4.0)

        # lecture des plus courts chemins
        legende = self.changer(legende, self.legende("Les prédécesseurs donnent les plus courts chemins : s, 1, 2, 4 et 5 via 1, 6 via 3", ["prédécesseurs"]))
        chemin = [("s", 1), (1, 2), (1, 3), (2, 4), (1, 5), (3, 6)]
        self.play(*[arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=8) for u, v in chemin], run_time=1.5)
        detail = self.detail(detail, tex(r"$d(1)=1\quad d(2)=2\quad d(3)=2\quad d(4)=1\quad d(5)=-1\quad d(6)=4$", 40, {r"d(5)=-1": ROUGE}))
        self.wait(7.0)
        legende = self.changer(legende, self.legende("Le poids négatif −2 de l'arc (1, 5) fait passer 5 de 3 à −1 : Dijkstra aurait pu se tromper", ["Dijkstra"]))
        self.wait(5.0)
        return g, etiq, tab, legende, detail

    # ---------- partie 2 : la variante avec circuit négatif ----------
    def partie_variante(self, g, etiq, tab, legende, detail):
        legende = self.changer(legende, self.legende("Variante vue en cours : l'arc (1, 5) de poids −2 devient un arc (5, 1) de poids −4", ["(5, 1)", "−4"]))
        self.play(*[FadeOut(x) for x in (*g.edges.values(), *etiq.values())], FadeOut(tab.cadre), FadeOut(tab.entetes),
                  *[FadeOut(c) for c in tab.cellules.values()], FadeOut(detail))
        autres = [(u, v, w) for u, v, w in ARCS_VARIANTE if (u, v) != (5, 1)]
        arcs = {(u, v): arete(g, u, v) for u, v, _ in ARCS if (u, v) != (1, 5)}
        labels = {(u, v): etiquette_sur(arcs[(u, v)], str(w).replace("-", "−"), taille=20, couleur=ACCENT if w >= 0 else ROUGE) for u, v, w in autres}
        for a in arcs.values():  # les arcs ont été colorés pendant la lecture du résultat : on les remet à neuf
            a.set_color(LIEN).set_stroke(width=4)
        arc51 = arc_entre(POS[5], POS[1], couleur=VIOLET, rayon=0.3, epaisseur=5)
        label51 = etiquette_sur(arc51, "−4", taille=20, couleur=VIOLET)
        arcs[(5, 1)] = arc51
        self.play(*[Create(a) for a in arcs.values()], *[FadeIn(e) for e in labels.values()], FadeIn(label51), run_time=2.0)
        self.wait(2.0)

        circuit = [(1, 3), (3, 5), (5, 1)]
        legende = self.changer(legende, self.legende("Le circuit 1, 3, 5, 1 a pour longueur 1 + 1 − 4 = −2 : chaque tour fait baisser les valeurs", ["−2"]))
        self.play(*[arcs[a].animate.set_color(ROUGE).set_stroke(width=7) for a in circuit], run_time=1.2)
        detail = self.detail(None, tex(r"$l(1\to 3\to 5\to 1)=1+1-4=-2<0$", 44, {r"-2<0": ROUGE}))
        self.wait(5.0)
        self.play(*[arcs[a].animate.set_color(LIEN).set_stroke(width=4) for a in circuit if a != (5, 1)], arcs[(5, 1)].animate.set_color(VIOLET).set_stroke(width=5))

        # tableau à 7 colonnes : n = 7 sommets
        tab = Tableau(7)
        self.play(FadeIn(tab.cadre), FadeIn(tab.entetes))
        legende = self.changer(legende, self.legende("n = 7 sommets : on calcule jusqu'à 7 colonnes au plus", ["n = 7"]))
        detail = self.detail(detail, "Au plus 7 itérations : si la septième change encore une valeur, il y a un circuit négatif", ["septième"])
        self.wait(4.0)
        pi = {v: INF for v in SOMMETS}
        pi["s"] = 0
        pred = {v: None for v in SOMMETS}
        for k in range(1, 8):
            nouveau, nouveau_pred, changements = iteration(ARCS_VARIANTE, pi, pred)
            self.play(*[FadeIn(tab.cellule(k, v, nouveau[v], nouveau_pred[v], ARETE)) for v in SOMMETS if v not in changements], run_time=0.7)
            if changements:
                detail = self.detail(detail, f"Itération {k} : mise à jour de {', '.join(str(v) for v in changements)}", [f"Itération {k}"])
            animations = []
            for v in changements:
                u, _ = changements[v]
                animations += [Indicate(arcs[(u, v)], color=ACCENT, scale_factor=1.0), FadeIn(tab.cellule(k, v, nouveau[v], nouveau_pred[v], ACCENT))]
            if animations:
                self.play(*animations, run_time=1.2)
            if k == 4:
                legende = self.changer(legende, self.legende("Itération 4 : le sommet 1 descend à −1 en passant par 5 : 3 − 4", ["−1"]))
            if k == 6:
                legende = self.changer(legende, self.legende("Les colonnes 5 et 6 continuent de changer, alors que le graphe n'a que 7 sommets", ["continuent de changer"]))
            self.wait(1.6)
            pi, pred = nouveau, nouveau_pred

        legende = self.changer(legende, self.legende("La colonne 7 diffère encore de la colonne 6 : le sommet 1 passe de −1 à −3", ["colonne 7"]))
        self.play(Indicate(tab.cellules[(7, 1)], color=ROUGE, scale_factor=1.4), Indicate(tab.cellules[(6, 1)], color=ROUGE, scale_factor=1.4))
        detail = self.detail(detail, tex(r"$\pi^7\neq\pi^6\;\Longrightarrow\;$ pas de stabilisation : circuit négatif", 42, {"circuit négatif": ROUGE}))
        self.wait(6.0)

        # retrouver le circuit avec les prédécesseurs
        legende = self.changer(legende, self.legende("Les prédécesseurs ne forment pas une arborescence : en remontant depuis 1, on boucle", ["boucle"]))
        detail = self.detail(detail, tex(r"$\mathrm{pred}(1)=5,\quad\mathrm{pred}(5)=3,\quad\mathrm{pred}(3)=1$", 44))
        self.play(*[arcs[a].animate.set_color(ROUGE).set_stroke(width=9) for a in circuit], run_time=1.5)
        self.wait(6.0)
        legende = self.changer(legende, self.legende("Bellman-Ford détecte donc le circuit négatif 1, 3, 5 : il n'existe pas de plus court chemin", ["détecte"]))
        detail = self.detail(detail, tex(r"$l=1+1-4=-2<0$", 46, {r"-2<0": ROUGE}))
        self.wait(7.0)

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Bellman-Ford en tableau", 21)
        carte = self.theorie()
        g, etiq, tab, legende, detail = self.partie_imprimee(carte, titre)
        self.partie_variante(g, etiq, tab, legende, detail)
        self.fin()
