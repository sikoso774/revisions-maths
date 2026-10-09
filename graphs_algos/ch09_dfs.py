from algo import *

LIGNES_DFS = [
    (0, "marquer u"),
    (0, "temps ← temps + 1 ; d[u] ← temps"),
    (0, "pour chaque voisin v de u :"),
    (1, "si v n'est pas marqué :"),
    (2, "parent[v] ← u"),
    (2, "DFS(G, v)"),
    (1, "sinon si v ≠ parent[u] :"),
    (2, "cycle détecté !"),
    (0, "temps ← temps + 1 ; f[u] ← temps"),
]

LIGNES_PILE = [
    (0, "P ← pile contenant s"),
    (0, "tant que P n'est pas vide :"),
    (1, "u ← dépiler(P)"),
    (1, "si u n'est pas marqué :"),
    (2, "marquer u"),
    (2, "pour chaque voisin v de u :"),
    (3, "empiler(P, v)"),
]

COTES = {"A": UP, "B": LEFT, "C": RIGHT}


class ParcoursProfondeur(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "Principe : aller le plus loin possible",
            VIOLET,
            [
                tex(
                    r"$\text{DFS}(u) :\ \text{marquer } u,\ \ \forall v \in L(u),\ v \text{ non marqué} \Rightarrow \text{DFS}(v)$",
                    38,
                )
            ],
            [
                tex(r"On s'enfonce dans une branche jusqu'au bout, puis on revient en arrière", 32, {"revient en arrière": VIOLET}),
                tex(r"Structure : une pile (LIFO), ou simplement la récursivité (pile d'appels)", 32, {"pile": ACCENT, "LIFO": ACCENT}),
                tex(r"$L(u)$ : la liste des voisins de $u$ (liste d'adjacence)", 32, {"voisins": SOMMET}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Dates de visite et détection de cycle",
            ACCENT,
            [
                tex(r"$d[u] < d[v] < f[v] < f[u]$ si $v$ est découvert depuis $u$", 40),
                tex(r"$\{u, v\} \in E,\ v \text{ marqué},\ v \neq \text{parent}[u] \Longrightarrow \text{cycle}$", 38),
            ],
            [
                tex(r"$d[u]$ : date de découverte, $f[u]$ : date de fin ; les intervalles $[d, f]$ sont emboîtés ou disjoints", 30, {"emboîtés": ACCENT, "disjoints": ACCENT}),
                tex(r"Une arête vers un sommet déjà marqué (hors parent) est une arête de retour", 32, {"arête de retour": ROUGE}),
                tex(r"Complexité : $O(n + m)$, comme le BFS", 32, {"O(n + m)": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Parcours en profondeur (DFS)", 9)

        g = creer_graphe(SOMMETS_P, ARETES_P, POSITION_P)
        legende = self.legende("Plonger au bout d'une branche avant de revenir", ["plonger", "revenir"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        legende = self.changer(
            legende, self.legende("L'algorithme : un pseudo-code et une pile d'appels", ["pseudo-code", "pile d'appels"])
        )
        code = PanneauCode("DFS(G, u)", LIGNES_DFS, coin=(0.25, 2.25), largeur_max=5.4)
        pile = Conteneur("Pile", origine=(6.2, -1.45), vertical=True, taille=(1.15, 0.46), capacite=6)
        self.play(*code.montrer(), *pile.montrer(), run_time=1.5)
        self.det = self.detail(
            None, "On lance DFS(G, A) : les voisins sont pris dans l'ordre alphabétique", ["DFS(G, A)"]
        )
        self.wait(4)
        legende = self.changer(
            legende,
            self.legende(
                "Blanc : pas vu · Jaune : en attente · Bleu : en cours · Vert : terminé",
                {"Jaune": ACCENT, "Bleu": SOMMET, "Vert": VERT},
            ),
        )

        # état de l'exécution
        self.marque, self.parent, self.ordre = set(), {}, []
        self.temps, self.d, self.f, self.labels, self.retours = 0, {}, {}, {}, set()
        self.dfs(g, code, pile, "A", None)

        self.play(code.aller_a(2))
        self.bilan(g, code, pile, legende, titre)
        self.fin(3)

    # ---------- outils ----------
    def dire(self, contenu, cles=None):
        self.det = self.detail(self.det, contenu, cles)

    def etiquette(self, g, v, contenu):
        return Text(contenu, font_size=22, color=ACCENT, weight=BOLD).next_to(
            g.vertices[v], COTES.get(v, DOWN), buff=0.12
        )

    # ---------- exécution pas à pas (récursive, comme l'algorithme) ----------
    def dfs(self, g, code, pile, u, p):
        self.marque.add(u)
        self.ordre.append(u)
        self.dire(f"Appel de DFS({u}) : on marque {u} et l'appel s'empile", [f"DFS({u})"])
        self.play(code.aller_a(0), colorier(g, u, SOMMET), *pile.ajouter(f"DFS({u})", ACCENT))
        self.wait(1.2)

        self.temps += 1
        self.d[u] = self.temps
        self.labels[u] = self.etiquette(g, u, f"{self.temps} /")
        self.dire(f"Date de découverte : d[{u}] = {self.temps}", [f"d[{u}] = {self.temps}"])
        self.play(code.aller_a(1), FadeIn(self.labels[u], scale=0.8))
        self.wait(1.2)

        for v in VOISINS_P[u]:
            self.play(code.aller_a(2), Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0), run_time=1)
            self.play(code.aller_a(3), run_time=0.6)
            if v not in self.marque:
                self.parent[v] = u
                self.dire(f"{v} n'est pas marqué : on s'y enfonce depuis {u}", ["on s'y enfonce"])
                self.play(code.aller_a(4), arete(g, u, v).animate.set_color(ACCENT).set_stroke(width=8))
                self.play(code.aller_a(5), colorier(g, u, ACCENT))
                self.wait(0.6)
                self.dfs(g, code, pile, v, u)
                self.dire(f"Retour dans DFS({u}) : on essaie le voisin suivant", [f"Retour dans DFS({u})"])
                self.play(colorier(g, u, SOMMET))
                self.wait(0.8)
            else:
                self.play(code.aller_a(6), run_time=0.6)
                cle = frozenset((u, v))
                if v == p:
                    self.dire(f"{v} est le parent de {u} : on ne revient pas en arrière", ["le parent"])
                    self.wait(1.4)
                elif cle in self.retours:
                    self.dire(
                        f"{v} est marqué : l'arête {u}–{v} a déjà été signalée comme arête de retour",
                        ["déjà été signalée"],
                    )
                    self.wait(2)
                else:
                    self.retours.add(cle)
                    self.dire(
                        f"{v} est déjà marqué et n'est pas le parent de {u} : arête de retour, donc cycle !",
                        {"arête de retour": ROUGE, "cycle !": ROUGE},
                    )
                    self.play(code.aller_a(7), arete(g, u, v).animate.set_color(ROUGE).set_stroke(width=8))
                    self.play(Indicate(g.vertices[u], color=ROUGE), Indicate(g.vertices[v], color=ROUGE))
                    self.wait(2.5)

        self.temps += 1
        self.f[u] = self.temps
        self.dire(
            f"Plus aucun voisin à explorer : f[{u}] = {self.temps}, DFS({u}) se termine",
            [f"f[{u}] = {self.temps}"],
        )
        nouveau = self.etiquette(g, u, f"{self.d[u]} / {self.temps}")
        self.play(
            code.aller_a(8),
            Transform(self.labels[u], nouveau),
            colorier(g, u, VERT),
            *pile.retirer(fin=True),
        )
        self.wait(1.2)

    # ---------- bilan ----------
    def bilan(self, g, code, pile, legende, titre):
        self.dire(
            f"Terminé : ordre de visite {', '.join(self.ordre)}, avec une arête de retour (A–C)",
            [", ".join(self.ordre), "arête de retour"],
        )
        self.wait(4)

        # --- intervalles [d, f] ---
        legende = self.changer(legende, self.legende("Les dates de visite : des intervalles emboîtés", ["emboîtés"]))
        self.play(*code.cacher(), FadeOut(pile.etiquette), FadeOut(pile.cadre))
        lignes = sorted(self.ordre, key=lambda v: self.d[v])
        pas_x = 4.5 / (2 * len(SOMMETS_P) - 1)
        barres = {}
        decor = VGroup()
        for i, v in enumerate(lignes):
            y = 1.9 - 0.6 * i
            x1 = 1.2 + (self.d[v] - 1) * pas_x
            x2 = 1.2 + (self.f[v] - 1) * pas_x
            nom = Text(v, font_size=26, color=SOMMET, weight=BOLD).move_to([0.55, y, 0])
            barre = Rectangle(
                width=x2 - x1, height=0.32, fill_color=VERT, fill_opacity=0.85, stroke_width=0
            ).move_to([(x1 + x2) / 2, y, 0])
            valeurs = Text(f"[{self.d[v]}, {self.f[v]}]", font_size=18, color=TEXTE).next_to(barre, RIGHT, buff=0.12)
            barres[v] = barre
            decor.add(nom, valeurs)
            self.play(FadeIn(nom), GrowFromEdge(barre, LEFT), FadeIn(valeurs), run_time=0.7)
        self.dire(
            "Chaque intervalle [d, f] est contenu dans celui de son parent, ou disjoint des autres",
            ["emboîté", "disjoint"],
        )
        self.wait(2)
        self.play(Indicate(barres["B"], color=ACCENT, scale_factor=1.05), Indicate(barres["A"], color=ACCENT, scale_factor=1.02))
        self.wait(1)
        self.play(Indicate(barres["D"], color=ACCENT, scale_factor=1.2), Indicate(barres["C"], color=ACCENT, scale_factor=1.2))
        self.dire(
            "D et C sont sans lien d'ancêtre : leurs intervalles sont disjoints. C'est la pile d'appels qui l'impose",
            ["disjoints", "pile d'appels"],
        )
        self.wait(5)
        self.play(FadeOut(decor), *[FadeOut(b) for b in barres.values()])

        # --- version itérative avec une pile explicite ---
        legende = self.changer(
            legende, self.legende("Sans récursivité : une pile explicite", ["pile explicite"])
        )
        self.play(
            *[colorier(g, v, NOEUD) for v in SOMMETS_P],
            *[arete(g, *e).animate.set_color(LIEN).set_stroke(width=5) for e in ARETES_P],
            *[FadeOut(etiq) for etiq in self.labels.values()],
        )
        code2 = PanneauCode("DFS_pile(G, s)", LIGNES_PILE, coin=(0.25, 2.25), largeur_max=5.4)
        pile2 = Conteneur("Pile P", origine=(6.2, -1.45), vertical=True, taille=(1.15, 0.46), capacite=6)
        self.play(*code2.montrer(), *pile2.montrer(), run_time=1.5)
        self.dire("La pile P remplace la pile d'appels : on empile les sommets à visiter", ["pile P"])
        self.wait(3.5)
        self.dire("On empile la source A", ["A"])
        self.play(code2.aller_a(0), *pile2.ajouter("A", ACCENT))
        self.wait(2)
        self.dire("Tant que la pile n'est pas vide : on dépile le sommet du dessus", ["dépile"])
        self.play(code2.aller_a(1))
        self.wait(1)
        self.play(code2.aller_a(2), *pile2.retirer(fin=True), colorier(g, "A", SOMMET))
        self.wait(2)
        self.dire("A n'est pas marqué : on le marque, puis on empile ses voisins", ["on le marque"])
        self.play(code2.aller_a(3))
        self.play(code2.aller_a(4))
        self.wait(1.5)
        self.play(code2.aller_a(5))
        self.dire("On empile C puis B : B sera dépilé en premier (ordre alphabétique conservé)", ["C puis B", "dépilé en premier"])
        self.play(code2.aller_a(6), *pile2.ajouter("C", ACCENT))
        self.play(*pile2.ajouter("B", ACCENT))
        self.wait(3)
        self.play(code2.aller_a(2), *pile2.retirer(fin=True), colorier(g, "B", SOMMET), colorier(g, "A", VERT))
        self.dire(
            "On dépile B : on explore B avant C, exactement comme avec la récursivité",
            ["B avant C", "récursivité"],
        )
        self.wait(4)
        self.dire("Et ainsi de suite : même ordre de visite, sans récursivité", ["même ordre de visite"])
        self.wait(4)
        self.play(
            *code2.cacher(),
            FadeOut(pile2.etiquette),
            FadeOut(pile2.cadre),
            *[FadeOut(case) for _, case in pile2.items],
        )

        # --- comparaison BFS / DFS ---
        legende = self.changer(legende, self.legende("BFS ou DFS ?", ["BFS", "DFS"]))
        garder = {titre, self.trait_titre}
        a_effacer = [m for m in self.mobjects if m not in garder]
        self.play(FadeOut(Group(*[m for m in a_effacer if m is not legende])), run_time=1.2)
        colonnes_x = [-0.4, 4.4]
        en_tetes = [
            Text("BFS · largeur", font_size=30, weight=BOLD, color=SOMMET).move_to([colonnes_x[0], 2.0, 0]),
            Text("DFS · profondeur", font_size=30, weight=BOLD, color=VIOLET).move_to([colonnes_x[1], 2.0, 0]),
        ]
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.2) for e in en_tetes], lag_ratio=0.3))
        lignes_tab = [
            ("Structure", ["file (FIFO)", "pile (LIFO) ou récursivité"]),
            ("Exploration", ["par couches", "au bout d'une branche"]),
            ("Idéal pour", ["plus court chemin (non pondéré)", "cycles, composantes, arborescences"]),
            ("Complexité", ["O(n + m)", "O(n + m)"]),
        ]
        for i, (nom, valeurs) in enumerate(lignes_tab):
            y = 1.0 - 0.95 * i
            etiquette = texte(nom, 24, [nom])
            etiquette.align_to([-6.9, 0, 0], LEFT).set_y(y)
            cellules = []
            for x, valeur in zip(colonnes_x, valeurs):
                t = Text(valeur, font_size=22, color=TEXTE)
                t.scale_to_fit_width(min(t.width, 4.6)).move_to([x, y, 0])
                cellules.append(t)
            separateur = Line([-6.9, y + 0.47, 0], [6.9, y + 0.47, 0], color=ARETE, stroke_width=1.5)
            self.play(Create(separateur), FadeIn(etiquette, shift=RIGHT * 0.2), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cellules], lag_ratio=0.25))
            self.wait(2)
        legende = self.changer(
            legende,
            self.legende("Même coût O(n + m) : le choix dépend de ce qu'on cherche", {"O(n + m)": VERT}),
        )
        self.wait(4)
