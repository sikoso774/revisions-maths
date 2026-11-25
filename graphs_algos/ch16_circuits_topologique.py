"""Chapitre 16 : circuits, détection par parcours en profondeur et ordre topologique (TD2, exercice 6, question 1)."""
from algo import *

CLES_CODE["circuit détecté"] = ROUGE
CLES_CODE["colorer"] = ACCENT

# Les 6 chalets de Rémi : un arc u -> v signifie « de u on descend vers v » (les altitudes sont toutes différentes)
CHALETS = ["N", "R", "L", "J", "G", "O"]
DESCENTES = [("R", "G"), ("R", "J"), ("N", "R"), ("N", "J"), ("J", "G"), ("G", "O"), ("L", "O"), ("N", "L")]
ARC_INCOHERENT = ("O", "N")  # « de O on descendrait vers N » : contredit les autres données
POS = {
    "N": np.array([-3.4, 2.0, 0]), "R": np.array([-5.6, 0.5, 0]), "L": np.array([-1.2, 0.5, 0]),
    "J": np.array([-5.0, -1.1, 0]), "G": np.array([-3.0, -1.6, 0]), "O": np.array([-1.0, -1.6, 0]),
}
POS = {v: np.array(p, dtype=float) for v, p in POS.items()}
POS_LIGNE = {v: np.array([-4.5 + 1.8 * i, 0.0, 0]) for i, v in enumerate(["N", "R", "L", "J", "G", "O"])}

LIGNES_DFS = [
    (0, "visiter(u) :"),
    (1, "colorer u en jaune"),
    (1, "pour chaque successeur v de u :"),
    (2, "si v est jaune : circuit détecté"),
    (2, "si v est blanc : visiter(v)"),
    (1, "colorer u en vert ; le mettre en tête de L"),
]


class CircuitsTopologique(SceneGraphes):
    # ---------- théorie ----------
    def theorie(self):
        carte = self.carte(
            "Circuit et ordre topologique",
            SOMMET,
            [
                tex(r"circuit : $v_1\to v_2\to\cdots\to v_k\to v_1$", 42, {r"v_1": ROUGE}),
                tex(r"$G$ sans circuit $\;\Longleftrightarrow\;$ il existe un ordre topologique", 40, {"ordre topologique": VERT}),
            ],
            [
                texte("Ordre topologique : on range les sommets pour que tous les arcs aillent vers la droite", 26, ["Ordre topologique"]),
                texte("Un circuit rend cet ordre impossible : on ne peut pas être avant soi-même", 26, ["circuit"]),
            ],
        )
        self.play(FadeOut(carte))
        return self.carte(
            "Détection par parcours en profondeur",
            VERT,
            [
                tex(r"blanc $\to$ jaune (en cours) $\to$ vert (terminé)", 40, {"jaune": ACCENT, "vert": VERT}),
                tex(r"arc $u\to v$ avec $v$ jaune $\;\Longrightarrow\;$ circuit", 40, {"circuit": ROUGE}),
            ],
            [
                texte("Un sommet jaune est sur la pile : retomber dessus, c'est avoir bouclé", 26, ["bouclé"]),
                texte("Sans circuit : l'ordre topologique est l'inverse de l'ordre où les sommets deviennent verts", 26, ["l'inverse"]),
            ],
        )

    # ---------- parcours animé ----------
    def parcours(self, g, panneau, liste, etat, detail, legende, rapide=False):
        """DFS depuis N. Renvoie (circuit trouvé ?, détail, liste) ; `etat` : couleur de chaque sommet."""
        pause = 0.6 if rapide else 1.3
        ordre_final = []
        trouve = [None]

        def maj_liste(nouvelle):
            return Tex(r"$L=[\," + ",\\,".join(nouvelle) + r"\,]$", font_size=42, color=VERT).move_to([3.7, -0.9, 0])

        def visiter(u):
            etat[u] = "jaune"
            detail_u = f"On visite {u} : il devient jaune (en cours)"
            self.detail_courant = self.detail(self.detail_courant, detail_u, ["jaune"])
            self.play(panneau.aller_a(1), colorier(g, u, ACCENT), run_time=0.9)
            self.wait(pause)
            for v in sorted(y for (x, y) in self.arcs_utilises if x == u):
                self.play(panneau.aller_a(2), Indicate(arete(g, u, v), color=ACCENT, scale_factor=1.0), run_time=0.8)
                if etat[v] == "jaune":
                    self.play(panneau.aller_a(3), run_time=0.6)
                    trouve[0] = (u, v)
                    return True
                if etat[v] == "vert":
                    self.detail_courant = self.detail(self.detail_courant, f"{v} est déjà vert : rien à faire", ["déjà vert"])
                    self.wait(pause * 0.6)
                    continue
                self.play(panneau.aller_a(4), run_time=0.6)
                if visiter(v):
                    return True
            etat[u] = "vert"
            ordre_final.insert(0, u)
            self.detail_courant = self.detail(self.detail_courant, f"{u} n'a plus de successeur à visiter : il devient vert et passe en tête de L", ["en tête de L"])
            nouvelle = maj_liste(ordre_final)
            self.play(panneau.aller_a(5), colorier(g, u, VERT), Transform(liste, nouvelle), run_time=1.0)
            self.wait(pause)
            return False

        self.detail_courant = detail
        circuit = visiter("N")
        return circuit, trouve[0], ordre_final

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Circuits et ordre topologique", 16)
        carte = self.theorie()

        arcs_coherents = list(DESCENTES)
        g = creer_graphe(CHALETS, [*DESCENTES, ARC_INCOHERENT], POS, orientee=True, rayon=0.3)
        reseau = Succession(
            LaggedStart(*[GrowFromCenter(v) for v in g.vertices.values()], lag_ratio=0.12),
            LaggedStart(*[Create(arete(g, *a)) for a in DESCENTES], lag_ratio=0.12),
        )
        legende = self.legende("Rémi a relevé 8 descentes entre ses 6 chalets, tous à des altitudes différentes", ["8 descentes"])
        self.dezoom(carte, reseau, FadeIn(legende))
        self.wait(2.0)

        # pourquoi la condition est nécessaire
        legende = self.changer(legende, self.legende("Un circuit qui ne fait que descendre est impossible : on reviendrait plus bas que son départ", ["impossible"]))
        detail = self.detail(None, tex(r"$h(v_1)>h(v_2)>\cdots>h(v_k)>h(v_1)$", 46, {r"h(v_1)>h(v_2)": ROUGE}))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Un circuit montant, lu à l'envers, est un circuit descendant : il suffit de tester les descentes", ["lu à l'envers"]))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Comment vérifier l'absence de circuit ? Par un parcours en profondeur", ["parcours en profondeur"]))
        detail = self.detail(detail, "Blanc : pas encore vu · Jaune : en cours · Vert : terminé", {"Jaune": ACCENT, "Vert": VERT})
        self.wait(3.0)

        panneau = PanneauCode("Parcours en profondeur", LIGNES_DFS, coin=(0.7, 2.35), largeur_max=6.2)
        liste = Tex(r"$L=[\,]$", font_size=42, color=VERT).move_to([3.7, -0.9, 0])
        self.play(*panneau.montrer(), FadeIn(liste), run_time=1.5)
        self.wait(2.0)

        # exécution sur les données de Rémi
        self.arcs_utilises = list(DESCENTES)
        etat = {v: "blanc" for v in CHALETS}
        legende = self.changer(legende, self.legende("On part de N, l'un des sommets sans arc entrant", ["N"]))
        circuit, _, ordre = self.parcours(g, panneau, liste, etat, detail, legende)
        detail = self.detail(self.detail_courant, "Aucun arc n'est revenu sur un sommet jaune : pas de circuit", ["pas de circuit"])
        legende = self.changer(legende, self.legende("Pas de circuit : les données de Rémi sont cohérentes", ["cohérentes"]))
        self.wait(4.0)
        detail = self.detail(detail, tex(r"$L=[N,R,L,J,G,O]$ : de l'altitude la plus haute à la plus basse", 40, {r"L=[N,R,L,J,G,O]": VERT}))
        self.wait(5.0)

        # un arc incohérent : de O on descendrait vers N
        legende = self.changer(legende, self.legende("Et si Rémi avait aussi noté : « de O, on descend vers N » ?", ["de O, on descend vers N"]))
        arc_extra = arete(g, *ARC_INCOHERENT)
        arc_extra.set_color(VIOLET).set_stroke(width=6)
        self.play(Create(arc_extra))
        self.wait(3.0)
        self.play(*[colorier(g, v, NOEUD) for v in CHALETS], Transform(liste, Tex(r"$L=[\,]$", font_size=42, color=VERT).move_to([3.7, -0.9, 0])), run_time=1.0)
        self.arcs_utilises = [*DESCENTES, ARC_INCOHERENT]
        etat = {v: "blanc" for v in CHALETS}
        legende = self.changer(legende, self.legende("On relance le parcours depuis N : tous les sommets sont de nouveau blancs", ["de nouveau blancs"]))
        circuit, trouve, _ = self.parcours(g, panneau, liste, etat, detail, legende, rapide=True)
        detail = self.detail(self.detail_courant, f"L'arc ({trouve[0]}, {trouve[1]}) arrive sur {trouve[1]}, qui est jaune : circuit détecté", ["circuit détecté"])
        legende = self.changer(legende, self.legende("On a bouclé : N, J, G, O, N est un circuit descendant, les données sont incohérentes", ["circuit descendant"]))
        cycle = [("N", "J"), ("J", "G"), ("G", "O"), ("O", "N")]
        self.play(*[arete(g, *a).animate.set_color(ROUGE).set_stroke(width=9) for a in cycle], run_time=1.5)
        self.wait(6.0)

        # ordre topologique : tous les arcs vers la droite
        self.vider(titre)
        noeuds = {v: LabeledDot(Text(v, font_size=28, color=FOND, weight=BOLD), radius=0.3, fill_color=NOEUD).move_to(POS_LIGNE[v]) for v in CHALETS}
        for n in noeuds.values():
            n.set_z_index(2)
        portees = {a: abs(CHALETS.index(a[1]) - CHALETS.index(a[0])) for a in DESCENTES}
        courbes = {a: arc_entre(POS_LIGNE[a[0]], POS_LIGNE[a[1]], angle=-(0.35 + 0.18 * portees[a]), rayon=0.3, epaisseur=3) for a in DESCENTES}
        legende = self.legende("Sans circuit, on peut ranger les sommets pour que tous les arcs aillent vers la droite", ["vers la droite"])
        self.play(LaggedStart(*[GrowFromCenter(n) for n in noeuds.values()], lag_ratio=0.15), FadeIn(legende))
        self.play(LaggedStart(*[Create(c) for c in courbes.values()], lag_ratio=0.1), run_time=3.0)
        detail = self.detail(None, tex(r"ordre topologique : $N,\;R,\;L,\;J,\;G,\;O$", 44, {"ordre topologique": VERT}))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Ici, c'est l'ordre des altitudes, de la plus haute à la plus basse : N domine tous les autres", ["altitudes"]))
        self.wait(5.0)
        self.fin()
