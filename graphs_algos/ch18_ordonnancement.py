"""Chapitre 18 : ordonnancement, graphe potentiel-tâches et chemin critique (TD2, exercice 7, questions 1 et 2)."""
from ordonnancement import *

TABLEAU = r"""
\begin{tabular}{|l|c|c|c|c|c|c|c|c|}\hline
Tâches & A & B & C & D & E & F & G & H \\ \hline
Antécédents &  &  &  & A,B & B & B,C & D,E & D,E,F \\ \hline
Durée & 7 & 4 & 5 & 8 & 6 & 3 & 7 & 4 \\ \hline
\end{tabular}
"""


class Ordonnancement(SceneGraphes):
    # ---------- théorie ----------
    def theorie(self):
        carte = self.carte(
            "Le graphe potentiel-tâches",
            SOMMET,
            [
                tex(r"arc $i\to j$ si $i$ précède $j$ \quad longueur $d_i$", 38, {r"d_i": ACCENT}),
                tex(r"$\alpha\to j$ si $j$ n'a pas d'antécédent \quad longueur $0$", 38),
                tex(r"$j\to\omega$ si $j$ n'a pas de successeur \quad longueur $d_j$", 38),
            ],
            [
                texte("Les sommets sont les tâches, plus deux sommets fictifs : début α et fin ω", 26, ["début α", "fin ω"]),
                texte("La longueur d'un arc est la durée de la tâche d'où il part", 26, ["durée de la tâche"]),
            ],
        )
        self.play(FadeOut(carte))
        return self.carte(
            "Durée minimale du projet",
            VERT,
            [
                tex(r"$t_j=\max_{i\to j}\,(t_i+d_i)\qquad t_\alpha=0$", 44),
                tex(r"durée minimale $=t_\omega=$ plus long chemin de $\alpha$ à $\omega$", 38, {"plus long chemin": VERT}),
            ],
            [
                texte("Le t de la formule est la date de début au plus tôt de la tâche", 26, ["date de début au plus tôt"]),
                texte("Le plus long chemin s'appelle le chemin critique : tout retard dessus retarde le projet", 26, ["chemin critique"]),
            ],
        )

    # ---------- construction du graphe ----------
    def construire(self, g, legende, detail):
        arcs = {k: arete(g, *k) for k in ARCS}
        etiquettes = {}
        groupes = [("α", "Début : les tâches sans antécédent partent de α, avec une longueur nulle")] + [
            (t, f"La tâche {t} dure {DUREES[t]} : ses arcs ont pour longueur {DUREES[t]}") for t in "ABCDEFGH"
        ]
        for source, phrase in groupes:
            sortants = [k for k in ARCS if k[0] == source]
            detail = self.detail(detail, phrase, [f"{source}"] if source != "α" else ["α"])
            animations = []
            for k in sortants:
                etiquettes[k] = etiquette_longueur(arcs[k], LONGUEUR[k], p=PROPORTION.get(k, 0.5))
                animations += [Create(arcs[k]), FadeIn(etiquettes[k])]
            self.play(*animations, run_time=1.2)
            self.wait(1.4)
        return arcs, etiquettes, detail

    # ---------- dates au plus tôt ----------
    def dates(self, g, arcs, legende, detail):
        t = {"α": 0}
        labels = {"α": date_label(g.vertices["α"], 0)}
        self.play(FadeIn(labels["α"], scale=0.8), colorier(g, "α", ACCENT))
        detail = self.detail(detail, "On part de α : la date de début est 0", ["α"])
        self.wait(2.5)

        # les tâches sans antécédent démarrent tout de suite
        for x in "ABC":
            t[x] = 0
            labels[x] = date_label(g.vertices[x], 0, bas=x in BAS)
        detail = self.detail(detail, "A, B et C n'ont pas d'antécédent : elles démarrent à 0", ["A, B et C"])
        self.play(*[FadeIn(labels[x], scale=0.8) for x in "ABC"], *[colorier(g, x, ACCENT) for x in "ABC"])
        self.wait(2.5)

        legende = self.changer(legende, self.legende("Une tâche démarre quand tous ses antécédents sont finis : on prend le maximum", ["le maximum"]))
        for x in ["D", "E", "F", "G", "H", "ω"]:
            preds = [p for (p, y) in ARCS if y == x]
            termes = [t[p] + LONGUEUR[(p, x)] for p in preds]
            t[x] = max(termes)
            expr = ",\\;".join(rf"t_{nom_tex(p)}+{LONGUEUR[(p, x)]}" for p in preds)
            valeurs = ",\\;".join(str(v) for v in termes)
            if len(preds) == 1:
                formule = rf"$t_{nom_tex(x)}={expr}={t[x]}$"
            else:
                formule = rf"$t_{nom_tex(x)}=\max({expr})=\max({valeurs})={t[x]}$"
            detail = self.detail(detail, tex(formule, 40))
            self.play(*[Indicate(arcs[(p, x)], color=ACCENT, scale_factor=1.0) for p in preds], run_time=1.2)
            labels[x] = date_label(g.vertices[x], t[x], bas=x in BAS)
            self.play(FadeIn(labels[x], scale=0.8), colorier(g, x, ACCENT), run_time=0.9)
            self.wait(3.0)
        return t, labels, detail

    # ---------- chemin critique ----------
    def critique(self, g, arcs, t, legende, detail):
        legende = self.changer(legende, self.legende("Pour trouver le chemin critique, on remonte depuis ω : quel antécédent donne le maximum ?", ["chemin critique"]))
        chemin = ["ω"]
        while chemin[-1] != "α":
            x = chemin[-1]
            preds = [p for (p, y) in ARCS if y == x]
            chemin.append(max(preds, key=lambda p: t[p] + LONGUEUR[(p, x)]))
        chemin.reverse()
        detail = self.detail(detail, "ω : le maximum vient de G (15 + 7). G : il vient de D (7 + 8). D : de A (0 + 7)", ["G", "D", "A"])
        self.wait(4.0)
        self.play(*[arcs[(a, b)].animate.set_color(ROUGE).set_stroke(width=9) for a, b in zip(chemin, chemin[1:])], run_time=1.5)
        self.wait(1.0)
        legende = self.changer(legende, self.legende("Chemin critique : α, A, D, G, ω. Les tâches A, D et G n'ont aucune marge", ["A, D et G"]))
        detail = self.detail(detail, tex(r"$7+8+7=22$", 52, {r"22": ROUGE}))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Durée minimale du projet : 22 unités de temps, en commençant tout au plus tôt", ["22 unités de temps"]))
        self.wait(5.0)
        return detail

    # ---------- scène ----------
    def construct(self):
        titre = self.intro("Ordonnancement et chemin critique", 18)
        carte = self.theorie()

        tableau = Tex(TABLEAU, font_size=52)
        tableau.scale_to_fit_width(min(tableau.width, 12.5))
        tableau.move_to([0, 0.4, 0])
        legende = self.legende("Un projet de 8 tâches : leurs durées et leurs antécédents", ["8 tâches"])
        self.dezoom(carte, FadeIn(tableau), FadeIn(legende))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("Combien de temps faut-il au minimum, si l'on commence chaque tâche au plus tôt ?", ["au minimum"]))
        self.wait(4.0)
        self.play(FadeOut(tableau))

        g = creer_graphe(SOMMETS, ARCS, POS, orientee=True, rayon=0.3)
        legende = self.changer(legende, self.legende("On construit le graphe potentiel-tâches", ["graphe potentiel-tâches"]))
        self.play(LaggedStart(*[GrowFromCenter(v) for v in g.vertices.values()], lag_ratio=0.12), run_time=2.0)
        arcs, etiquettes, detail = self.construire(g, legende, None)
        t, labels, detail = self.dates(g, arcs, legende, detail)
        self.critique(g, arcs, t, legende, detail)
        self.fin()
