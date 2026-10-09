from common import *

# --- Graphe non orienté : deux morceaux séparés ---
S1 = ["A", "B", "C", "D", "E", "F", "G"]
E1 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G")]
P1 = {
    "A": LEFT * 4.8 + UP * 1.5,
    "B": LEFT * 2.8 + UP * 1.5,
    "C": LEFT * 2.8 + DOWN * 0.7,
    "D": LEFT * 4.8 + DOWN * 0.7,
    "E": RIGHT * 1.6 + UP * 1.3,
    "F": RIGHT * 3.4 + UP * 0.1,
    "G": RIGHT * 5.2 + UP * 1.3,
}

# --- Graphe orienté : trois composantes fortement connexes ---
S2 = ["A", "B", "C", "D", "E", "F", "G"]
E2 = [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "D"), ("F", "G")]
P2 = {
    "A": LEFT * 5.6 + UP * 0.6,
    "B": LEFT * 4.3 + UP * 1.7,
    "C": LEFT * 4.3 + DOWN * 0.5,
    "D": LEFT * 1.3 + UP * 0.6,
    "E": RIGHT * 0.2 + UP * 1.7,
    "F": RIGHT * 0.2 + DOWN * 0.5,
    "G": RIGHT * 3.6 + UP * 0.6,
}
COMPOSANTES = [(["A", "B", "C"], VERT), (["D", "E", "F"], VIOLET), (["G"], SOMMET)]


def parties(g):
    """Sommets et arêtes d'un graphe, comme objets indépendants (pour les fondus)."""
    return VGroup(*g.vertices.values(), *g.edges.values())


def ajuste(mobject, largeur=12.5):
    """Réduit une formule trop large pour qu'elle reste dans le cadre."""
    if mobject.width > largeur:
        mobject.scale_to_fit_width(largeur)
    return mobject


class Connexite(SceneGraphes):
    # ---------- outils ----------
    def parcourir(self, g, chemin, couleur=ACCENT, duree=0.7):
        """Colore un chemin sommet après sommet."""
        self.play(colorier(g, chemin[0], couleur), run_time=0.4)
        for u, v in zip(chemin, chemin[1:]):
            self.play(
                arete(g, u, v).animate.set_color(couleur).set_stroke(width=8),
                colorier(g, v, couleur),
                run_time=duree,
            )

    def remettre(self, g, sommets, aretes):
        return [
            *[colorier(g, s, NOEUD) for s in sommets],
            *[arete(g, *e).animate.set_color(LIEN).set_stroke(width=5) for e in aretes],
        ]

    # ---------- 0) les formules ----------
    def formules(self):
        fleche = r"\xrightarrow{*}"

        carte = self.carte(
            "Rappel · Chemin",
            TEXTE,
            [ajuste(tex(r"$u \leadsto v \iff \exists\, x_0, \dots, x_k : \ x_0 = u,\ x_k = v,\ \{x_{i-1}, x_i\} \in E$", 38))],
            [
                tex(r"Un chemin de $u$ à $v$ : une suite de sommets reliés deux à deux", 32, {"chemin": ACCENT}),
                tex(r"Sa longueur est $k$ : le nombre d'arêtes parcourues", 32, {"longueur": VERT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        carte = self.carte(
            "1 · Composantes connexes (graphe non orienté)",
            VERT,
            [tex(r"$u \sim v \iff \text{il existe un chemin de } u \text{ à } v$", 46)],
            [
                tex(r"$\sim$ est une relation d'équivalence : réflexive, symétrique, transitive", 32, {"équivalence": VERT}),
                tex(r"Ses classes d'équivalence sont les composantes connexes", 32, {"composantes connexes": VERT}),
                tex(r"$G$ connexe $\iff$ une seule composante $\iff \forall\, u, v \in V,\ u \sim v$", 32, {"connexe": VERT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        carte = self.carte(
            "2 · Composantes fortement connexes (graphe orienté)",
            VIOLET,
            [tex(rf"$u \equiv v \iff u {fleche} v \ \text{{ et }} \ v {fleche} u$", 46)],
            [
                tex(rf"$u {fleche} v$ : il existe un chemin orienté de $u$ à $v$ (on suit le sens des arcs)", 32, {"orienté": VIOLET}),
                tex(r"Les classes de $\equiv$ sont les composantes fortement connexes", 32, {"fortement connexes": VIOLET}),
                tex(rf"$G$ fortement connexe $\iff$ une seule composante $\iff \forall\, u, v,\ u {fleche} v$", 32, {"fortement connexe": VIOLET}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        carte = self.carte(
            "3 · Faiblement connexe, et le cas pondéré",
            ACCENT,
            [tex(r"$G \text{ fortement connexe} \;\Longrightarrow\; G \text{ faiblement connexe}$", 44)],
            [
                tex(r"Faiblement connexe : connexe quand on oublie le sens des arcs (graphe $\overline{G}$)", 32, {"Faiblement": ACCENT}),
                tex(r"La réciproque est fausse : un sens unique suffit à casser la forte connexité", 32, {"fausse": ROUGE}),
                tex(r"Graphe pondéré : les poids n'interviennent pas, seule l'existence des arêtes compte", 32, {"poids": ACCENT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        # Récapitulatif, qui servira à « dézoomer »
        titre_recap = Text("En résumé", font_size=36, weight=BOLD, color=TEXTE).move_to(UP * 2.2)
        lignes_recap = [
            ("Connexité", VERT, r"$u \sim v \iff u \leadsto v$"),
            ("Forte connexité", VIOLET, rf"$u \equiv v \iff u {fleche} v \ \wedge\ v {fleche} u$"),
            ("Faible connexité", ACCENT, r"$\overline{G}$ connexe"),
        ]
        recap = VGroup(titre_recap)
        for i, (nom, couleur, formule) in enumerate(lignes_recap):
            y = 0.8 - 1.3 * i
            etiquette = Text(nom, font_size=32, weight=BOLD, color=couleur).move_to([-4.2, y, 0])
            etiquette.align_to([-6.2, 0, 0], LEFT)
            recap.add(etiquette, tex(formule, 38).move_to([2.4, y, 0]))
        self.play(FadeIn(recap, shift=UP * 0.3), run_time=1.5)
        self.wait(4)
        return recap

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("La connexité", 5)

        g = creer_graphe(S1, E1, P1)
        legende = self.legende(
            "1) Graphe non orienté : les composantes connexes", {"composantes connexes": VERT}
        )

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

        self.partie_non_oriente(g, titre)
        legende = self.changer(
            legende,
            self.legende(
                "2) Graphe orienté : les composantes fortement connexes",
                {"fortement connexes": VIOLET},
            ),
        )
        self.partie_oriente(titre)
        self.fin(3)

    # ---------- 1) graphe non orienté ----------
    def partie_non_oriente(self, g, titre):
        detail = self.detail(None, "Question : peut-on aller de A à C en suivant des arêtes ?", ["A à C"])
        self.play(colorier(g, "A", ACCENT), colorier(g, "C", ACCENT))
        self.wait(2.5)

        detail = self.detail(detail, "A ∼ B : une arête les relie directement", ["A ∼ B"])
        self.play(arete(g, "A", "B").animate.set_color(ACCENT).set_stroke(width=8), colorier(g, "B", ACCENT))
        self.wait(2)
        detail = self.detail(detail, "B ∼ C : une arête les relie directement", ["B ∼ C"])
        self.play(arete(g, "B", "C").animate.set_color(ACCENT).set_stroke(width=8))
        self.wait(2)
        detail = self.detail(
            detail, "Donc A ∼ C (transitivité) : le chemin A – B – C existe", ["A ∼ C", "transitivité"]
        )
        self.play(Indicate(g.vertices["A"], color=VERT), Indicate(g.vertices["C"], color=VERT))
        self.wait(3)
        self.play(*self.remettre(g, S1, E1))

        # exploration depuis A
        detail = self.detail(detail, "Et de A à F ? Explorons tout ce que A peut atteindre…", ["A à F"])
        self.play(colorier(g, "A", VERT))
        self.wait(1)
        self.play(
            arete(g, "A", "B").animate.set_color(VERT),
            arete(g, "D", "A").animate.set_color(VERT),
            colorier(g, "B", VERT),
            colorier(g, "D", VERT),
        )
        self.wait(1)
        self.play(
            arete(g, "B", "C").animate.set_color(VERT),
            colorier(g, "C", VERT),
        )
        self.wait(1.5)
        detail = self.detail(
            detail, "A n'atteint que A, B, C et D : E, F et G restent hors de portée", ["A, B, C et D", "hors de portée"]
        )
        self.play(*[Indicate(g.vertices[v], color=ROUGE, scale_factor=1.3) for v in "EFG"])
        self.wait(2)
        detail = self.detail(
            detail, "Il n'existe aucun chemin de A à F : A et F ne sont pas équivalents", ["aucun chemin"]
        )
        self.play(colorier(g, "F", ROUGE))
        self.wait(3)
        self.play(*self.remettre(g, S1, E1))

        # composantes
        detail = self.detail(
            detail,
            "Les classes de ∼ : { A, B, C, D } et { E, F, G } sont les composantes connexes",
            ["composantes connexes"],
        )
        groupes = [(["A", "B", "C", "D"], VERT), (["E", "F", "G"], VIOLET)]
        animations = []
        for membres, couleur in groupes:
            animations += [colorier(g, v, couleur) for v in membres]
            animations += [
                arete(g, *e).animate.set_color(couleur) for e in E1 if e[0] in membres
            ]
        self.play(*animations)
        compteur = Text("2 composantes connexes", font_size=34, weight=BOLD, color=ACCENT)
        compteur.next_to(titre, DOWN, buff=0.45)
        self.play(FadeIn(compteur, shift=DOWN * 0.3))
        self.wait(2)
        detail = self.detail(
            detail, "Chaque sommet appartient à une seule composante : elles forment une partition de V", ["partition"]
        )
        self.wait(3)

        # fusion
        detail = self.detail(detail, "Ajoutons l'arête C–E : les deux morceaux se rejoignent", ["C–E"])
        pont = Line(
            g.vertices["C"].get_center(),
            g.vertices["E"].get_center(),
            stroke_color=ACCENT,
            stroke_width=5,
        )
        self.play(Create(pont), run_time=1.2)
        self.wait(1)
        self.play(
            *[colorier(g, v, NOEUD) for v in S1],
            *[arete(g, *e).animate.set_color(LIEN) for e in E1],
            pont.animate.set_color(LIEN),
            Transform(
                compteur,
                Text("1 composante connexe", font_size=34, weight=BOLD, color=VERT).move_to(compteur),
            ),
        )
        detail = self.detail(
            detail, "Tout sommet atteint tout autre : G est connexe (une seule composante)", ["connexe"]
        )
        self.wait(3.5)
        self.play(FadeOut(parties(g)), FadeOut(pont), FadeOut(compteur), FadeOut(detail))

    # ---------- 2) graphe orienté ----------
    def partie_oriente(self, titre):
        dg = creer_graphe(S2, E2, P2, orientee=True)
        self.play(apparition(dg), run_time=2.5)
        detail = self.detail(
            None, "Les arêtes deviennent des arcs : on ne peut les suivre que dans leur sens", ["arcs"]
        )
        self.wait(3)

        # aller et retour entre A et C
        detail = self.detail(detail, "A atteint C en suivant les arcs : A → B → C", ["A → B → C"])
        self.parcourir(dg, ["A", "B", "C"])
        self.wait(2)
        detail = self.detail(detail, "Et C atteint A grâce à l'arc C → A : l'aller-retour existe", ["C → A"])
        self.play(arete(dg, "C", "A").animate.set_color(VERT).set_stroke(width=8))
        self.wait(1)
        detail = self.detail(
            detail, "A et C s'atteignent mutuellement : A ≡ C (même composante fortement connexe)", ["A ≡ C"]
        )
        self.play(Indicate(dg.vertices["A"], color=VERT), Indicate(dg.vertices["C"], color=VERT))
        self.wait(3)
        self.play(*self.remettre(dg, S2, E2))

        # aller sans retour entre D et G
        detail = self.detail(detail, "D atteint G : D → E → F → G", ["D → E → F → G"])
        self.parcourir(dg, ["D", "E", "F", "G"])
        self.wait(2)
        detail = self.detail(
            detail, "Mais aucun arc ne sort de G : impossible de revenir vers D", ["aucun arc ne sort de G"]
        )
        self.play(colorier(dg, "G", ROUGE))
        self.play(Indicate(dg.vertices["G"], color=ROUGE, scale_factor=1.4))
        self.wait(2.5)
        detail = self.detail(
            detail, "Il faut pouvoir aller ET revenir : D et G ne sont pas équivalents", ["aller ET revenir"]
        )
        self.wait(3)
        self.play(*self.remettre(dg, S2, E2))

        # faiblement connexe
        detail = self.detail(
            detail, "Si on oublie le sens des arcs, tout est d'un seul morceau : faiblement connexe", ["faiblement connexe"]
        )
        non_oriente = creer_graphe(S2, E2, P2)
        self.play(FadeOut(parties(dg)), FadeIn(parties(non_oriente)), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(parties(non_oriente)), FadeIn(parties(dg)), run_time=1.5)

        # composantes fortement connexes
        detail = self.detail(
            detail,
            "Classes de ≡ : { A, B, C }, { D, E, F } et { G } = composantes fortement connexes",
            ["composantes fortement connexes"],
        )
        animations = []
        for membres, couleur in COMPOSANTES:
            animations += [colorier(dg, v, couleur) for v in membres]
            animations += [
                arete(dg, u, v).animate.set_color(couleur)
                for u, v in E2
                if u in membres and v in membres
            ]
        self.play(*animations)
        compteur = Text("3 composantes fortement connexes", font_size=34, weight=BOLD, color=ACCENT)
        compteur.next_to(titre, DOWN, buff=0.45)
        self.play(FadeIn(compteur, shift=DOWN * 0.3))
        self.wait(2.5)
        detail = self.detail(
            detail, "Dans chacune, on va de n'importe quel sommet à n'importe quel autre, et on revient", ["et on revient"]
        )
        for membres, couleur in COMPOSANTES[:2]:
            self.play(*[Indicate(dg.vertices[v], color=TEXTE, scale_factor=1.3) for v in membres])
        self.wait(2)
        detail = self.detail(
            detail, "Un sommet seul, comme G, forme à lui seul une composante", ["G"]
        )
        self.play(Indicate(dg.vertices["G"], color=TEXTE, scale_factor=1.5))
        self.wait(3)

        # graphe pondéré
        detail = self.detail(
            detail, "Et si le graphe est pondéré ? Les poids ne changent rien aux composantes", ["pondéré", "poids"]
        )
        poids = {e: 2 + (3 * i) % 7 for i, e in enumerate(E2)}
        etiquettes = VGroup(*[etiquette_poids(dg, u, v, p) for (u, v), p in poids.items()])
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in etiquettes], lag_ratio=0.2))
        self.wait(2)
        self.play(*[Indicate(dg.vertices[v], color=TEXTE, scale_factor=1.2) for v in S2])
        detail = self.detail(
            detail, "Seule compte l'existence d'un arc : mêmes composantes avec ou sans poids", ["existence"]
        )
        self.wait(3.5)
        self.play(FadeOut(etiquettes))

        # graphe des composantes
        detail = self.detail(
            detail, "Contractons chaque composante en un seul sommet…", ["Contractons"]
        )
        noeuds = []
        animations = []
        for k, (membres, couleur) in enumerate(COMPOSANTES, start=1):
            centre = np.mean([P2[v] for v in membres], axis=0)
            noeud = LabeledDot(
                Text(f"C{k}", font_size=28, color=FOND, weight=BOLD),
                radius=0.45,
                fill_color=couleur,
            ).move_to(centre)
            noeuds.append(noeud)
            elements = VGroup(
                *[dg.vertices[v] for v in membres],
                *[
                    dg.edges[(u, v)]
                    for u, v in E2
                    if u in membres and v in membres
                ],
            )
            animations.append(ReplacementTransform(elements, noeud))
        liaisons = [dg.edges[("C", "D")], dg.edges[("F", "G")]]
        self.play(*animations, *[FadeOut(e) for e in liaisons], run_time=2)
        fleches = [
            Arrow(noeuds[0].get_right(), noeuds[1].get_left(), buff=0.1, color=LIEN, stroke_width=5),
            Arrow(noeuds[1].get_right(), noeuds[2].get_left(), buff=0.1, color=LIEN, stroke_width=5),
        ]
        self.play(*[Create(f) for f in fleches])
        self.wait(2)
        detail = self.detail(
            detail,
            "Le graphe des composantes n'a aucun cycle : c'est un graphe orienté acyclique (DAG)",
            ["aucun cycle", "DAG"],
        )
        self.wait(4)
        self.play(FadeOut(Group(*noeuds, *fleches)), FadeOut(compteur), FadeOut(detail))
