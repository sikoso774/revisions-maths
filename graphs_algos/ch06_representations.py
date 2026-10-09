from common import *

SOMMETS = ["A", "B", "C", "D", "E"]
ARETES = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("D", "E")]
VOISINS = {v: sorted(a if b == v else b for a, b in ARETES if v in (a, b)) for v in SOMMETS}


def construire_tableau(lignes, colonnes, origine, pas, couleur_lignes, couleur_colonnes, taille=26):
    """Tableau de 0 avec ses en-têtes ; renvoie (en-têtes colonnes, en-têtes lignes, cases, cadre)."""
    entetes_col = {
        c: Text(c, font_size=taille - 2 if len(c) > 1 else taille, color=couleur_colonnes, weight=BOLD)
        .move_to(origine + RIGHT * pas * (j + 1))
        for j, c in enumerate(colonnes)
    }
    entetes_lig = {
        l: Text(l, font_size=taille, color=couleur_lignes, weight=BOLD)
        .move_to(origine + DOWN * 0.65 * (i + 1))
        for i, l in enumerate(lignes)
    }
    cases = {
        (l, c): Text("0", font_size=taille, color=ARETE).move_to(
            origine + RIGHT * pas * (j + 1) + DOWN * 0.65 * (i + 1)
        )
        for i, l in enumerate(lignes)
        for j, c in enumerate(colonnes)
    }
    cadre = SurroundingRectangle(VGroup(*cases.values()), color=TEXTE, buff=0.2, stroke_width=3)
    return entetes_col, entetes_lig, cases, cadre


def vers_un(case, couleur=ACCENT):
    """Animation qui transforme une case « 0 » en « 1 »."""
    un = Text("1", font_size=26, color=couleur, weight=BOLD).move_to(case)
    return Transform(case, un)


class Representations(SceneGraphes):
    # ---------- outils ----------
    def remplir(self, cases_a_remplir):
        """Passe des cases à 1, puis les fait ressortir (en deux temps : sinon Indicate écrase le 1)."""
        self.play(*[vers_un(c) for c in cases_a_remplir])
        self.play(*[Indicate(c, color=ACCENT, scale_factor=1.6) for c in cases_a_remplir])

    def rectangle(self, mobjects, couleur=SOMMET):
        return SurroundingRectangle(VGroup(*mobjects), color=couleur, buff=0.1, stroke_width=4)

    def surligner(self, g, u, v, couleur=ACCENT):
        return [colorier(g, u, couleur), colorier(g, v, couleur), arete(g, u, v).animate.set_color(couleur)]

    def reinitialiser(self, g):
        return [
            *[colorier(g, s, NOEUD) for s in SOMMETS],
            *[arete(g, *e).animate.set_color(LIEN) for e in ARETES],
        ]

    # ---------- 0) les formules ----------
    def formules(self):
        cles_sa = {"sommets": SOMMET, "arêtes": ACCENT}

        # Notations
        carte = self.carte(
            "Notations",
            TEXTE,
            [
                tex(r"$G = (V, E)$", 54),
                tex(r"$V = \{v_1, v_2, \dots, v_n\} \qquad E = \{e_1, e_2, \dots, e_m\}$", 44),
            ],
            [
                tex(r"$V$ : l'ensemble des $n = |V|$ sommets", 34, cles_sa),
                tex(r"$E$ : l'ensemble des $m = |E|$ arêtes", 34, cles_sa),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        # Matrice d'adjacence
        carte_a = self.carte(
            "1 · Matrice d'adjacence",
            SOMMET,
            [
                tex(r"$A = (a_{ij})_{1 \le i,\, j \le n}$", 44),
                tex(
                    r"$\displaystyle a_{ij} = \begin{cases} 1 & \text{si } \{v_i, v_j\} \in E \\ 0 & \text{sinon} \end{cases}$",
                    44,
                ),
            ],
            [
                tex(r"Matrice carrée $n \times n$ : une ligne et une colonne par sommet", 32, {"carrée": SOMMET}),
                tex(r"Graphe non orienté : $a_{ij} = a_{ji}$ (symétrique), diagonale nulle", 32, {"symétrique": SOMMET}),
                tex(r"Somme d'une ligne : $\displaystyle\sum_{j=1}^{n} a_{ij} = \deg(v_i)$", 32, {"degré": SOMMET}),
            ],
        )
        self.play(FadeOut(carte_a, shift=LEFT * 0.4))

        # Liste d'adjacence
        carte_l = self.carte(
            "2 · Liste d'adjacence",
            VIOLET,
            [tex(r"$\forall\, v \in V, \quad L(v) = \{\, w \in V \mid \{v, w\} \in E \,\}$", 44)],
            [
                tex(r"$L(v)$ : l'ensemble des voisins du sommet $v$", 32, {"voisins": ACCENT}),
                tex(r"On ne stocke que les arêtes qui existent : mémoire en $O(n + m)$", 32, {"existent": ACCENT}),
                tex(r"Chaque arête est comptée deux fois : $\displaystyle\sum_{v \in V} |L(v)| = 2m$", 32, {"deux fois": ACCENT}),
            ],
        )
        self.play(FadeOut(carte_l, shift=LEFT * 0.4))

        # Matrice d'incidence
        carte_i = self.carte(
            "3 · Matrice d'incidence",
            VERT,
            [
                tex(r"$B = (b_{ij})_{1 \le i \le n,\; 1 \le j \le m}$", 44),
                tex(
                    r"$\displaystyle b_{ij} = \begin{cases} 1 & \text{si } v_i \in e_j \\ 0 & \text{sinon} \end{cases}$",
                    44,
                ),
            ],
            [
                tex(r"$n$ lignes (les sommets) et $m$ colonnes (les arêtes)", 32, {"lignes": SOMMET, "colonnes": ACCENT}),
                tex(r"Chaque colonne contient exactement deux $1$ : les extrémités de l'arête", 32, {"extrémités": VERT}),
                tex(r"Somme d'une ligne : $\displaystyle\sum_{j=1}^{m} b_{ij} = \deg(v_i)$", 32, {"degré": VERT}),
            ],
        )
        self.play(FadeOut(carte_i, shift=LEFT * 0.4))

        # Récapitulatif, qui servira à « dézoomer »
        titre_recap = Text("En résumé", font_size=36, weight=BOLD, color=TEXTE).move_to(UP * 2.2)
        lignes_recap = [
            ("Adjacence", SOMMET, r"$A \in \{0, 1\}^{n \times n}$"),
            ("Liste", VIOLET, r"$L(v) = \{\, w \in V \mid \{v, w\} \in E \,\}$"),
            ("Incidence", VERT, r"$B \in \{0, 1\}^{n \times m}$"),
        ]
        recap = VGroup(titre_recap)
        for i, (nom, couleur, formule) in enumerate(lignes_recap):
            y = 0.8 - 1.3 * i
            etiquette = Text(nom, font_size=32, weight=BOLD, color=couleur).move_to([-4.2, y, 0])
            etiquette.align_to([-5.9, 0, 0], LEFT)
            formule = tex(formule, 42).move_to([1.6, y, 0])
            recap.add(etiquette, formule)
        self.play(FadeIn(recap, shift=UP * 0.3), run_time=1.5)
        self.wait(4)
        return recap

    # ---------- scène ----------
    def construct(self):
        self.intro("Représenter un graphe en machine", 6)

        position = {
            "A": LEFT * 5.5 + UP * 1.0,
            "B": LEFT * 5.5 + DOWN * 1.6,
            "C": LEFT * 3.7 + DOWN * 0.3,
            "D": LEFT * 2.0 + UP * 1.0,
            "E": LEFT * 2.0 + DOWN * 1.6,
        }
        g = creer_graphe(SOMMETS, ARETES, position)
        legende = self.legende("Comment stocker ce graphe dans un programme ?", ["stocker"])

        # D'abord la théorie : les formules ; puis on dézoome sur l'exemple concret.
        recap = self.formules()
        self.play(
            recap.animate.scale(0.1).set_opacity(0),
            apparition(g),
            FadeIn(legende, shift=UP * 0.2),
            run_time=3,
            rate_func=smooth,
        )
        self.remove(recap)
        self.wait(1)
        legende = self.changer(
            legende,
            self.legende(
                "Trois méthodes classiques : adjacence, liste, incidence",
                {"adjacence": SOMMET, "liste": VIOLET, "incidence": VERT},
            ),
        )
        self.wait(2)

        legende = self.partie_adjacence(g, legende)
        legende = self.partie_liste(g, legende)
        legende = self.partie_incidence(g, legende)
        self.partie_comparaison(g, legende)
        self.fin(3)

    # ---------- 1) matrice d'adjacence ----------
    def partie_adjacence(self, g, legende):
        legende = self.changer(
            legende,
            self.legende(
                "1) La matrice d'adjacence : sommets en lignes ET en colonnes",
                {"matrice d'adjacence": SOMMET},
            ),
        )
        origine = RIGHT * 2.2 + UP * 1.9
        pas = 0.65
        entetes_col, entetes_lig, cases, cadre = construire_tableau(
            SOMMETS, SOMMETS, origine, pas, SOMMET, SOMMET
        )
        detail = self.detail(None, "Un sommet = une ligne et une colonne : 5 sommets → matrice 5 × 5", ["5 × 5"])
        self.play(
            FadeIn(VGroup(*entetes_col.values(), *entetes_lig.values()), shift=LEFT * 0.3),
            LaggedStart(*[FadeIn(c) for c in cases.values()], lag_ratio=0.02),
            Create(cadre),
            run_time=2,
        )
        self.wait(2)

        detail = self.detail(
            detail, "Case (ligne, colonne) = 1 si les deux sommets sont reliés, sinon 0", ["1", "0"]
        )
        self.wait(2)

        # exemple détaillé : A - B
        detail = self.detail(detail, "Exemple : A et B sont reliés par une arête", ["A et B"])
        self.play(*self.surligner(g, "A", "B"))
        ligne_a = self.rectangle([entetes_lig["A"]] + [cases[("A", c)] for c in SOMMETS], SOMMET)
        colonne_b = self.rectangle([entetes_col["B"]] + [cases[(l, "B")] for l in SOMMETS], VIOLET)
        self.play(Create(ligne_a), Create(colonne_b))
        detail = self.detail(detail, "On lit la ligne A, colonne B : leur croisement vaut 1", ["ligne A", "colonne B", "1"])
        self.remplir([cases[("A", "B")]])
        self.wait(2)

        detail = self.detail(
            detail, "Pas de sens dans l'arête : B est aussi relié à A, donc (B, A) = 1", ["(B, A) = 1"]
        )
        self.play(FadeOut(ligne_a), FadeOut(colonne_b))
        ligne_b = self.rectangle([entetes_lig["B"]] + [cases[("B", c)] for c in SOMMETS], VIOLET)
        colonne_a = self.rectangle([entetes_col["A"]] + [cases[(l, "A")] for l in SOMMETS], SOMMET)
        self.play(Create(ligne_b), Create(colonne_a))
        self.remplir([cases[("B", "A")]])
        self.wait(2)
        self.play(FadeOut(ligne_b), FadeOut(colonne_a), *self.reinitialiser(g))

        # les autres arêtes
        for u, v in ARETES[1:]:
            detail = self.detail(
                detail, f"Arête {u}–{v} : on met 1 en ({u}, {v}) et en ({v}, {u})", [f"({u}, {v})", f"({v}, {u})"]
            )
            self.play(*self.surligner(g, u, v), run_time=0.8)
            self.remplir([cases[(u, v)], cases[(v, u)]])
            self.wait(1.2)
            self.play(*self.reinitialiser(g), run_time=0.6)

        # propriétés
        detail = self.detail(detail, "Propriété 1 : la diagonale est à 0 (aucun sommet n'est relié à lui-même)", ["diagonale"])
        diagonale = [SurroundingRectangle(cases[(s, s)], color=ROUGE, buff=0.08, stroke_width=3) for s in SOMMETS]
        self.play(LaggedStart(*[Create(d) for d in diagonale], lag_ratio=0.2))
        self.wait(2)
        self.play(*[FadeOut(d) for d in diagonale])

        detail = self.detail(detail, "Propriété 2 : la matrice est symétrique (graphe non orienté)", ["symétrique"])
        axe = DashedLine(
            cases[("A", "A")].get_center() + UL * 0.3,
            cases[("E", "E")].get_center() + DR * 0.3,
            color=VERT,
            stroke_width=3,
        )
        self.play(Create(axe))
        self.play(
            *[Indicate(cases[(u, v)], color=VERT, scale_factor=1.5) for u, v in ARETES],
            *[Indicate(cases[(v, u)], color=VERT, scale_factor=1.5) for u, v in ARETES],
        )
        self.wait(1.5)
        self.play(FadeOut(axe))

        detail = self.detail(
            detail, "Propriété 3 : la somme d'une ligne est le degré du sommet", ["somme d'une ligne", "degré"]
        )
        ligne_c = self.rectangle([entetes_lig["C"]] + [cases[("C", c)] for c in SOMMETS], ACCENT)
        self.play(Create(ligne_c), colorier(g, "C", ACCENT))
        self.wait(2.5)
        detail = self.detail(
            detail, "Ligne C : 1 + 1 + 0 + 1 + 0 = 3 = le degré de C", {"Ligne C": ACCENT, "= 3": VERT}
        )
        self.wait(3)
        self.play(FadeOut(ligne_c), colorier(g, "C", NOEUD))

        detail = self.detail(
            detail, "Graphe pondéré : on écrit le poids de l'arête à la place du 1", ["poids"]
        )
        self.wait(3)

        self.play(
            FadeOut(detail),
            FadeOut(VGroup(*entetes_col.values(), *entetes_lig.values(), *cases.values(), cadre), shift=RIGHT * 0.3),
        )
        return legende

    # ---------- 2) liste d'adjacence ----------
    def partie_liste(self, g, legende):
        legende = self.changer(
            legende,
            self.legende(
                "2) La liste d'adjacence : pour chaque sommet, la liste de ses voisins",
                {"liste d'adjacence": VIOLET, "voisins": ACCENT},
            ),
        )
        lignes = {
            v: texte(f"{v}  →  {', '.join(VOISINS[v])}", 34, {v: SOMMET}) for v in SOMMETS
        }
        groupe = VGroup(*lignes.values()).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        groupe.move_to(RIGHT * 3.4 + DOWN * 0.35)
        detail = self.detail(None, "Pour chaque sommet, on note uniquement ses voisins", ["voisins"])
        self.wait(2)

        for v in SOMMETS:
            detail = self.detail(
                detail,
                f"Voisins de {v} : {', '.join(VOISINS[v])}",
                {f"Voisins de {v}": ACCENT},
            )
            incidentes = [arete(g, v, w).animate.set_color(ACCENT) for w in VOISINS[v]]
            voisins = [colorier(g, w, VERT) for w in VOISINS[v]]
            self.play(colorier(g, v, ACCENT), *incidentes, *voisins, run_time=0.8)
            self.play(FadeIn(lignes[v], shift=LEFT * 0.3))
            self.wait(1.2)
            self.play(*self.reinitialiser(g), run_time=0.6)

        detail = self.detail(
            detail, "On ne stocke que ce qui existe : pas de 0 inutiles", ["que ce qui existe"]
        )
        self.wait(2.5)
        total = sum(len(VOISINS[v]) for v in SOMMETS)
        detail = self.detail(
            detail,
            f"Chaque arête apparaît deux fois (une par extrémité) : {total} = 2 × {len(ARETES)}",
            ["deux fois", f"{total} = 2 × {len(ARETES)}"],
        )
        self.play(
            Indicate(lignes["A"], color=VERT),
            Indicate(lignes["B"], color=VERT),
        )
        self.wait(3)

        self.play(FadeOut(detail), FadeOut(groupe, shift=RIGHT * 0.3))
        return legende

    # ---------- 3) matrice d'incidence ----------
    def partie_incidence(self, g, legende):
        legende = self.changer(
            legende,
            self.legende(
                "3) La matrice d'incidence : sommets en lignes, arêtes en colonnes",
                {"matrice d'incidence": VERT},
            ),
        )
        noms = [f"{u}{v}" for u, v in ARETES]
        origine = RIGHT * 2.2 + UP * 1.9
        pas = 0.75
        entetes_col, entetes_lig, cases, cadre = construire_tableau(
            SOMMETS, noms, origine, pas, SOMMET, ACCENT
        )
        detail = self.detail(
            None, "Cette fois : une ligne par sommet, une colonne par arête", ["ligne par sommet", "colonne par arête"]
        )
        self.play(
            FadeIn(VGroup(*entetes_col.values(), *entetes_lig.values()), shift=LEFT * 0.3),
            LaggedStart(*[FadeIn(c) for c in cases.values()], lag_ratio=0.02),
            Create(cadre),
            run_time=2,
        )
        self.wait(1.5)
        detail = self.detail(
            detail,
            f"{len(SOMMETS)} sommets et {len(ARETES)} arêtes → matrice {len(SOMMETS)} × {len(ARETES)}",
            [f"{len(SOMMETS)} × {len(ARETES)}"],
        )
        self.wait(2)
        detail = self.detail(
            detail, "Case (sommet, arête) = 1 si le sommet est une extrémité de l'arête", ["extrémité"]
        )
        self.wait(2.5)

        for k, (u, v) in enumerate(ARETES):
            nom = noms[k]
            detail = self.detail(
                detail,
                f"Arête {nom} : ses extrémités sont {u} et {v} → 1 sur les lignes {u} et {v}",
                {f"Arête {nom}": ACCENT},
            )
            colonne = self.rectangle([entetes_col[nom]] + [cases[(s, nom)] for s in SOMMETS], ACCENT)
            self.play(Create(colonne), *self.surligner(g, u, v), run_time=0.9 if k else 1.5)
            self.remplir([cases[(u, nom)], cases[(v, nom)]])
            self.wait(1.8 if k else 2.5)
            self.play(FadeOut(colonne), *self.reinitialiser(g), run_time=0.6)

        detail = self.detail(
            detail, "Propriété 1 : chaque colonne contient exactement deux 1", ["exactement deux 1"]
        )
        colonne_cd = self.rectangle([entetes_col["CD"]] + [cases[(s, "CD")] for s in SOMMETS], VERT)
        self.play(Create(colonne_cd))
        self.wait(1)
        detail = self.detail(
            detail, "Une arête a toujours deux extrémités : c'est ce qu'on lit ici", ["deux extrémités"]
        )
        self.wait(2.5)
        self.play(FadeOut(colonne_cd))

        detail = self.detail(
            detail, "Propriété 2 : la somme d'une ligne est encore le degré du sommet", ["somme d'une ligne", "degré"]
        )
        ligne_c = self.rectangle([entetes_lig["C"]] + [cases[("C", n)] for n in noms], ACCENT)
        self.play(Create(ligne_c), colorier(g, "C", ACCENT))
        self.wait(2.5)
        detail = self.detail(
            detail, "Ligne C : 0 + 1 + 1 + 1 + 0 = 3 = le degré de C", {"Ligne C": ACCENT, "= 3": VERT}
        )
        self.wait(3)
        self.play(FadeOut(ligne_c), colorier(g, "C", NOEUD))

        detail = self.detail(
            detail,
            "Pour un graphe orienté : +1 au départ, −1 à l'arrivée de l'arête",
            ["orienté", "+1", "−1"],
        )
        self.wait(3.5)

        self.play(
            FadeOut(detail),
            FadeOut(VGroup(*entetes_col.values(), *entetes_lig.values(), *cases.values(), cadre), shift=RIGHT * 0.3),
        )
        return legende

    # ---------- 4) comparaison ----------
    def partie_comparaison(self, g, legende):
        legende = self.changer(
            legende, self.legende("Quelle représentation choisir ?", ["choisir"])
        )
        self.play(FadeOut(g))

        colonnes_x = [-1.5, 2.0, 5.4]
        en_tetes = VGroup(
            Text("Adjacence", font_size=30, weight=BOLD, color=SOMMET).move_to([colonnes_x[0], 2.0, 0]),
            Text("Liste", font_size=30, weight=BOLD, color=VIOLET).move_to([colonnes_x[1], 2.0, 0]),
            Text("Incidence", font_size=30, weight=BOLD, color=VERT).move_to([colonnes_x[2], 2.0, 0]),
        )
        lignes = [
            ("Mémoire", ["n × n", "n + m", "n × m"]),
            ("Tester une arête u–v", ["immédiat", "parcours de la liste", "parcours des colonnes"]),
            ("Voisins d'un sommet", ["une ligne à lire", "directement", "via les colonnes"]),
            ("Idéale pour", ["graphes denses", "graphes peu denses", "raisonner sur les arêtes"]),
        ]
        for entete in en_tetes:
            entete.align_to([0, 2.3, 0], UP)  # même hauteur malgré les jambages
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.2) for e in en_tetes], lag_ratio=0.3))
        for i, (nom, valeurs) in enumerate(lignes):
            y = 1.0 - 0.95 * i
            etiquette = texte(nom, 24, [nom], couleur=TEXTE)
            etiquette.scale_to_fit_width(min(etiquette.width, 3.4)).move_to([-5.2, y, 0])
            etiquette.align_to([-6.9, 0, 0], LEFT)
            cellules = []
            for x, valeur in zip(colonnes_x, valeurs):
                t = Text(valeur, font_size=22, color=TEXTE)
                t.scale_to_fit_width(min(t.width, 3.2)).move_to([x, y, 0])
                cellules.append(t)
            separateur = Line([-6.9, y + 0.47, 0], [6.9, y + 0.47, 0], color=ARETE, stroke_width=1.5)
            self.play(Create(separateur), FadeIn(etiquette, shift=RIGHT * 0.2), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cellules], lag_ratio=0.25))
            self.wait(1.8)

        note = texte("n = nombre de sommets, m = nombre d'arêtes", 24, couleur=ARETE).next_to(
            legende, UP, buff=0.35
        )
        self.play(FadeIn(note))
        self.wait(3)
