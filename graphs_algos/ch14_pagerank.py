from algo import *

PAGES = list("ABCDEF")
LIENS = [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "C"), ("F", "A")]
D_AMORT = 0.85
POS_PR = {
    "A": LEFT * 5.3 + UP * 1.3,
    "B": LEFT * 5.3 + DOWN * 1.0,
    "C": LEFT * 3.4 + UP * 0.2,
    "D": LEFT * 1.5 + UP * 1.3,
    "E": LEFT * 1.5 + DOWN * 1.0,
    "F": LEFT * 3.8 + UP * 2.4,
}
COTES_PR = {"A": LEFT, "B": LEFT, "C": DOWN, "D": RIGHT, "E": RIGHT, "F": LEFT}
SORTANTS = {p: [v for u, v in LIENS if u == p] for p in PAGES}
ENTRANTS = {p: [u for u, v in LIENS if v == p] for p in PAGES}


def suivant(r):
    """Une itération : PR_{k+1}(p) = (1 − d)/N + d · Σ_{q → p} PR_k(q) / L(q)."""
    n = len(PAGES)
    return {
        p: (1 - D_AMORT) / n + D_AMORT * sum(r[q] / len(SORTANTS[q]) for q in ENTRANTS[p])
        for p in PAGES
    }


def fr(x, decimales=3):
    """Nombre à la française : virgule décimale."""
    return f"{x:.{decimales}f}".replace(".", ",")


def rayon_halo(x):
    return 0.28 + 1.0 * x


class PageRank(SceneGraphes):
    # ---------- 0) la théorie ----------
    def formules(self):
        carte = self.carte(
            "L'idée : le surfeur aléatoire",
            VIOLET,
            [tex(r"$PR(p) = \text{probabilité d'être sur la page } p$", 44)],
            [
                tex(r"Un internaute clique au hasard sur un des liens de la page où il se trouve", 32, {"au hasard": VIOLET}),
                tex(r"Une page est importante si beaucoup de pages importantes pointent vers elle", 32, {"importantes": VIOLET}),
                tex(r"Avec la probabilité $1 - d$, il se téléporte sur une page au hasard ($d \approx 0{,}85$)", 32, {"se téléporte": ACCENT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        carte = self.carte(
            "La formule",
            ACCENT,
            [tex(r"$PR(p) = \dfrac{1 - d}{N} + d \displaystyle\sum_{q \to p} \dfrac{PR(q)}{L(q)}$", 46)],
            [
                tex(r"$N$ : nombre de pages ; $L(q)$ : nombre de liens sortants de la page $q$", 32, {"liens sortants": ACCENT}),
                tex(r"Chaque page $q$ répartit son score à parts égales entre ses liens sortants", 32, {"parts égales": ACCENT}),
                tex(r"La somme des $PR(p)$ vaut $1$ : ce sont des probabilités", 32, {"vaut $1$": VERT}),
            ],
        )
        self.play(FadeOut(carte, shift=LEFT * 0.4))

        return self.carte(
            "Calcul par itérations",
            VERT,
            [
                tex(r"$r_{k+1} = d\, M\, r_k + \dfrac{1 - d}{N}\, \mathbf{1} \qquad r_0 = \left(\dfrac{1}{N}, \dots, \dfrac{1}{N}\right)$", 40),
            ],
            [
                tex(r"$M_{pq} = \dfrac{1}{L(q)}$ si $q \to p$, sinon $0$ : la matrice de transition", 32, {"matrice de transition": VERT}),
                tex(r"On itère jusqu'à $\lVert r_{k+1} - r_k \rVert < \varepsilon$ ; la convergence est garantie pour $d < 1$", 32, {"convergence": VERT}),
                tex(r"Chaque itération coûte $O(m)$ : un passage sur tous les liens", 32, {"O(m)": VERT}),
            ],
        )

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("PageRank : classer les pages web", 14)

        g = creer_graphe(PAGES, LIENS, POS_PR, orientee=True)
        legende = self.legende("Une page est importante si des pages importantes la citent", ["page est importante", "pages importantes"])

        # D'abord la théorie ; puis on dézoome sur l'exemple concret.
        carte = self.formules()
        self.dezoom(carte, apparition(g), FadeIn(legende, shift=UP * 0.2))
        self.wait(1)

        self.det = self.detail(
            None, "Six pages web : une flèche A → B signifie « la page A contient un lien vers B »", ["A → B"]
        )
        self.wait(4)

        self.liens_sortants(g)
        self.matrice(legende)
        legende = self.changer(
            legende, self.legende("Le calcul : on répète la formule, jusqu'à convergence", ["répète la formule", "convergence"])
        )
        self.iterations(g, legende)
        self.fin(3)

    # ---------- outils ----------
    def dire(self, contenu, cles=None):
        self.det = self.detail(self.det, contenu, cles)

    # ---------- 1) répartition des liens sortants ----------
    def liens_sortants(self, g):
        self.dire(
            "Liens sortants : L(A) = L(B) = L(D) = L(E) = L(F) = 1, mais L(C) = 2",
            ["L(C) = 2"],
        )
        self.play(Indicate(g.vertices["C"], color=ACCENT, scale_factor=1.3))
        self.wait(3)
        self.dire(
            "C répartit son score en deux parts égales : PR(C)/2 pour A et PR(C)/2 pour D",
            ["deux parts égales", "PR(C)/2"],
        )
        moitie = VGroup(*[etiquette_poids(g, "C", cible, "1/2") for cible in "AD"])
        self.play(
            *[g.edges[("C", cible)].animate.set_color(ACCENT).set_stroke(width=8) for cible in "AD"],
            LaggedStart(*[FadeIn(m, scale=0.5) for m in moitie], lag_ratio=0.3),
        )
        self.wait(4)
        self.dire(
            "Les pages à lien unique donnent tout leur score : B donne PR(B) à C, E donne PR(E) à C",
            ["tout leur score"],
        )
        self.play(
            *[g.edges[e].animate.set_color(VERT).set_stroke(width=8) for e in [("B", "C"), ("E", "C")]],
            *[g.edges[("C", cible)].animate.set_color(LIEN).set_stroke(width=5) for cible in "AD"],
            FadeOut(moitie),
        )
        self.wait(4)
        self.play(*[g.edges[e].animate.set_color(LIEN).set_stroke(width=5) for e in [("B", "C"), ("E", "C")]])

    # ---------- 2) forme matricielle ----------
    def matrice(self, legende):
        self.dire(
            "Forme matricielle : la colonne q de M répartit les liens sortants de q",
            ["colonne q"],
        )
        matrice = tex(
            r"$M = \begin{pmatrix} 0 & 0 & \tfrac12 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 1 & 0 \\ 0 & 0 & \tfrac12 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{pmatrix}$",
            40,
        ).move_to([3.9, 0.2, 0])
        colonnes = VGroup(
            *[
                Text(p, font_size=22, color=SOMMET, weight=BOLD).move_to([matrice.get_left()[0] + 1.0 + 0.78 * j, matrice.get_top()[1] + 0.3, 0])
                for j, p in enumerate(PAGES)
            ]
        )
        self.play(Write(matrice), run_time=2.5)
        self.play(FadeIn(colonnes))
        self.wait(4)
        self.dire(
            "Exemple : la colonne C vaut 1/2 en A et 1/2 en D ; la ligne F est nulle : personne ne cite F",
            ["colonne C", "ligne F"],
        )
        self.wait(5)
        self.play(FadeOut(matrice), FadeOut(colonnes))

    # ---------- 3) itérations ----------
    def iterations(self, g, legende):
        r = {p: 1 / len(PAGES) for p in PAGES}
        halos = {
            p: Circle(radius=rayon_halo(r[p]), fill_color=VERT, fill_opacity=0.35, stroke_width=0)
            .move_to(g.vertices[p].get_center())
            .set_z_index(-1)
            for p in PAGES
        }
        rayons = {p: rayon_halo(r[p]) for p in PAGES}

        def etiquette(p, x, couleur=ACCENT):
            return Text(fr(x), font_size=22, color=couleur, weight=BOLD).next_to(
                g.vertices[p], COTES_PR[p], buff=0.32
            )

        valeurs = {p: etiquette(p, r[p]) for p in PAGES}

        # tableau des valeurs par itération (à droite)
        x0, y0, pas_x, pas_y = 1.0, 1.55, 0.9, 0.42
        entetes = VGroup(
            Text("k", font_size=20, color=ARETE).move_to([x0, y0, 0]),
            *[
                Text(p, font_size=22, color=SOMMET, weight=BOLD).move_to([x0 + pas_x * (j + 1), y0, 0])
                for j, p in enumerate(PAGES)
            ],
        )
        formule = tex(
            r"$PR_{k+1}(p) = \dfrac{1 - d}{N} + d \displaystyle\sum_{q \to p} \dfrac{PR_k(q)}{L(q)}$", 28
        ).move_to([3.7, 2.3, 0])
        lignes = []

        def ligne(k, x, nom=None):
            y = y0 - pas_y * (len(lignes) + 1)
            maximum = max(x, key=x.get)
            cellules = [Text(nom or str(k), font_size=20, color=ARETE).move_to([x0, y, 0])]
            for j, p in enumerate(PAGES):
                cellules.append(
                    Text(fr(x[p]), font_size=20, color=VERT if (p == maximum and k > 0) else TEXTE).move_to(
                        [x0 + pas_x * (j + 1), y, 0]
                    )
                )
            groupe = VGroup(*cellules)
            lignes.append(groupe)
            return groupe

        self.dire(
            "Départ : le surfeur peut être n'importe où, PR₀ = 1/6 = 0,167 pour chaque page (la taille du halo = le score)",
            ["PR₀ = 1/6 = 0,167", "halo"],
        )
        self.play(
            LaggedStart(*[FadeIn(halos[p], scale=0.5) for p in PAGES], lag_ratio=0.1),
            LaggedStart(*[FadeIn(valeurs[p]) for p in PAGES], lag_ratio=0.1),
            FadeIn(entetes),
            FadeIn(formule),
        )
        self.play(FadeIn(ligne(0, r), shift=UP * 0.15))
        self.wait(4)

        # itération 1, détaillée sur la page C
        r1 = suivant(r)
        self.dire(
            f"Itération 1, page C : PR₁(C) = 0,15/6 + 0,85 × (PR₀(B)/1 + PR₀(E)/1) = 0,025 + 0,85 × 0,333 = {fr(r1['C'])}",
            [fr(r1["C"])],
        )
        self.play(
            *[g.edges[e].animate.set_color(VERT).set_stroke(width=8) for e in [("B", "C"), ("E", "C")]],
            colorier(g, "C", ACCENT),
        )
        self.wait(5)
        r = self.avancer(g, r, 1, halos, rayons, valeurs, etiquette, ligne, reinit=[("B", "C"), ("E", "C")])
        self.wait(2)

        # itération 2, détaillée sur la page A
        r2 = suivant(r)
        self.dire(
            f"Itération 2, page A : PR₂(A) = 0,025 + 0,85 × (PR₁(C)/2 + PR₁(F)/1) = 0,025 + 0,85 × ({fr(r['C'] / 2)} + {fr(r['F'])}) = {fr(r2['A'])}",
            [fr(r2["A"])],
        )
        self.play(
            *[g.edges[e].animate.set_color(VERT).set_stroke(width=8) for e in [("C", "A"), ("F", "A")]],
            colorier(g, "A", ACCENT),
        )
        self.wait(5)
        r = self.avancer(g, r, 2, halos, rayons, valeurs, etiquette, ligne, reinit=[("C", "A"), ("F", "A")])
        self.wait(2)

        # itérations 3 et 4 : un tour de table chacune
        for k in (3, 4):
            self.dire(f"Itération {k} : la même formule, appliquée à toutes les pages en même temps", [f"Itération {k}"])
            r = self.avancer(g, r, k, halos, rayons, valeurs, etiquette, ligne)
            self.wait(2.5)

        # convergence
        k = 4
        ecart = 1.0
        ecarts = []
        while ecart >= 0.001 and k < 60:
            suiv = suivant(r)
            ecart = max(abs(suiv[p] - r[p]) for p in PAGES)
            ecarts.append(ecart)
            r, k = suiv, k + 1
        self.dire(
            f"On répète : après {k} itérations, l'écart maximal entre deux itérations passe sous 0,001",
            [f"{k} itérations", "0,001"],
        )
        final = ligne(k, r, nom="∞")
        self.play(
            *[
                halos[p].animate.scale(rayon_halo(r[p]) / rayons[p])
                for p in PAGES
            ],
            *[Transform(valeurs[p], etiquette(p, r[p], VERT)) for p in PAGES],
            FadeIn(final, shift=UP * 0.15),
            run_time=2.5,
        )
        self.wait(5)

        # lecture du résultat
        classement = sorted(PAGES, key=lambda p: -r[p])
        self.dire(
            "Classement : " + " > ".join(f"{p} ({fr(r[p])})" for p in classement),
            ["Classement"],
        )
        self.play(Indicate(halos[classement[0]], color=ACCENT, scale_factor=1.15))
        self.wait(5)
        self.dire(
            "C est en tête : elle est citée par B et E, et distribue la moitié de son score à A et à D",
            ["C est en tête"],
        )
        self.play(*[Indicate(g.vertices[p], color=VERT, scale_factor=1.3) for p in "BCE"])
        self.wait(5)
        self.dire(
            f"F n'est citée par personne : il ne lui reste que la téléportation, (1 − d)/N = {fr(0.15 / 6)}",
            ["F n'est citée par personne", fr(0.15 / 6)],
        )
        self.play(Indicate(g.vertices["F"], color=ROUGE, scale_factor=1.4))
        self.wait(5)
        self.dire(f"Vérification : la somme des scores vaut {fr(sum(r.values()), 1)}, ce sont bien des probabilités", ["somme"])
        self.wait(4)
        self.dire(
            "Une page sans lien sortant redistribue son score à toutes les pages ; chaque itération coûte O(m)",
            ["sans lien sortant", "O(m)"],
        )
        self.wait(6)

    def avancer(self, g, r, k, halos, rayons, valeurs, etiquette, ligne, reinit=()):
        """Applique une itération et anime halos, valeurs et tableau."""
        suiv = suivant(r)
        nouvelle_ligne = ligne(k, suiv)
        animations = [FadeIn(nouvelle_ligne, shift=UP * 0.15)]
        for p in PAGES:
            facteur = rayon_halo(suiv[p]) / rayons[p]
            animations.append(halos[p].animate.scale(facteur))
            rayons[p] = rayon_halo(suiv[p])
            animations.append(Transform(valeurs[p], etiquette(p, suiv[p])))
        animations += [g.edges[e].animate.set_color(LIEN).set_stroke(width=5) for e in reinit]
        animations += [colorier(g, p, NOEUD) for p in PAGES]
        self.play(*animations, run_time=2)
        return suiv
