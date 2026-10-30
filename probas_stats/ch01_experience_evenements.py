"""Chapitre 1 : expérience aléatoire, univers, événements et opérations sur les événements."""
from common import *
from proba import *


class Chapitre01(SceneProbas):
    def construct(self):
        self.intro("Expérience aléatoire et événements", 1)

        # ── Théorie : le vocabulaire, puis les opérations ─────────────────
        vocabulaire = self.carte(
            "Le vocabulaire de base",
            ACCENT,
            [
                tex(r"Univers : $\Omega=\{1,2,3,4,5,6\}$", 40, {r"\Omega": ACCENT}),
                tex(r"Événement : $A\subset\Omega$", 40, {r"A": VERT}),
            ],
            [
                texte("Expérience aléatoire : résultat imprévisible (lancer un dé)", 26, ["Expérience aléatoire"]),
                texte("Univers Ω : l'ensemble de tous les résultats possibles", 26, ["Univers Ω"]),
                texte("Événement : un scénario, c'est-à-dire une partie de Ω", 26, ["Événement"]),
            ],
        )
        self.play(FadeOut(vocabulaire))
        operations = self.carte(
            "Opérations sur les événements",
            ACCENT,
            [
                tex(r"$A\cap B$ \quad ($A$ \textbf{et} $B$)", 40, {r"\cap": VERT}),
                tex(r"$A\cup B$ \quad ($A$ \textbf{ou} $B$)", 40, {r"\cup": BLEU}),
                tex(r"$\bar{A}=\Omega\setminus A$ \quad (\textbf{contraire} de $A$)", 40, {r"\bar{A}": VIOLET}),
            ],
            [
                texte("Intersection : les deux scénarios arrivent en même temps", 24, ["Intersection"]),
                texte("Réunion : au moins un des deux scénarios arrive", 24, ["Réunion"]),
                texte("Contraire : A n'arrive pas, c'est tout Ω sauf A", 24, ["Contraire"]),
            ],
        )

        # ── Démonstration : un lancer de dé ────────────────────────────────
        de = face_de(3, 1.6).move_to([0, Y0, 0])
        legende = self.legende("On lance un dé à 6 faces : le résultat est imprévisible", ["imprévisible"])
        self.dezoom(operations, FadeIn(de), FadeIn(legende))
        self.wait(1.0)
        for valeur in [6, 1, 5, 2, 4]:
            self.remove(de)
            de = face_de(valeur, 1.6).move_to([0, Y0, 0])
            self.add(de)
            self.wait(0.22)
        self.play(Indicate(de, color=ACCENT, scale_factor=1.15))
        legende = self.changer(legende, self.legende("Une expérience aléatoire : on connaît les issues, pas laquelle va sortir", ["expérience aléatoire"]))
        self.wait(2.0)

        # L'univers : tous les résultats possibles
        cadre = univers(9.6, 4.0, [0, Y0, 0])
        faces = {n: face_de(n, 0.7).move_to([(n - 3.5) * 1.3, Y0, 0]) for n in range(1, 7)}
        self.play(FadeOut(de), Create(cadre[0]), FadeIn(cadre[1]))
        self.play(LaggedStart(*[FadeIn(f, scale=0.5) for f in faces.values()], lag_ratio=0.2))
        legende = self.changer(legende, self.legende("L'univers Ω contient les 6 résultats possibles", ["univers Ω"]))
        detail = self.detail(None, tex(r"$\Omega=\{1,2,3,4,5,6\}$", 46, {r"\Omega": ACCENT}))
        self.wait(2.5)

        # Un événement = une partie de Ω
        self.play(*[faces[n].animate.move_to(PLACES[n]) for n in faces], run_time=1.8)
        legende = self.changer(legende, self.legende("Un événement regroupe certains résultats de Ω", ["événement"]))
        self.wait(1.5)

        cercle_a, lettre_a = cercle_evenement(CERCLE_A, "A", VERT, 150)
        self.play(Create(cercle_a), FadeIn(lettre_a))
        self.play(*[a for n in (2, 4, 6) for a in style_de(faces[n], VERT, 0.3)])
        detail = self.detail(detail, tex(r"$A$ : \textit{le résultat est pair} $=\{2,4,6\}$", 46, {r"A": VERT}))
        self.wait(3.0)

        cercle_b, lettre_b = cercle_evenement(CERCLE_B, "B", BLEU, 40)
        self.play(Create(cercle_b), FadeIn(lettre_b))
        self.play(*[a for n in (5, 6) for a in style_de(faces[n], BLEU, 0.3)])
        detail = self.detail(detail, tex(r"$B$ : \textit{le résultat dépasse 4} $=\{5,6\}$", 46, {r"B": BLEU}))
        self.wait(3.0)

        # Intersection
        legende = self.changer(legende, self.legende("Le 6 est à la fois pair et plus grand que 4", ["6"]))
        self.play(*style_de(faces[6], ACCENT, 0.4))
        self.play(Indicate(faces[6], color=ACCENT, scale_factor=1.3))
        detail = self.detail(detail, tex(r"$A\cap B=\{6\}$ \quad ($A$ \textbf{et} $B$)", 46, {r"\cap": ACCENT}))
        self.wait(3.0)

        # Réunion
        legende = self.changer(legende, self.legende("Au moins un des deux : on garde 2, 4, 5 et 6", ["2, 4, 5 et 6"]))
        self.play(*[a for n in (2, 4, 5, 6) for a in style_de(faces[n], ACCENT, 0.35)])
        detail = self.detail(detail, tex(r"$A\cup B=\{2,4,5,6\}$ \quad ($A$ \textbf{ou} $B$)", 46, {r"\cup": ACCENT}))
        self.wait(3.0)

        # Contraire
        legende = self.changer(legende, self.legende("Le contraire de A : tous les résultats impairs", ["contraire de A", "impairs"]))
        self.play(
            *[a for n in (2, 4, 5, 6) for a in style_de(faces[n], BLANC)],
            FadeOut(cercle_b), FadeOut(lettre_b),
        )
        self.play(*[a for n in (1, 3, 5) for a in style_de(faces[n], VIOLET, 0.35)])
        detail = self.detail(detail, tex(r"$\bar{A}=\{1,3,5\}$ \quad (A n'arrive pas)", 46, {r"\bar{A}": VIOLET}))
        self.wait(3.0)

        # Cas particuliers
        self.play(
            FadeOut(cercle_a), FadeOut(lettre_a),
            *[a for n in (1, 3, 5) for a in style_de(faces[n], BLANC)],
        )
        legende = self.changer(legende, self.legende("Événement élémentaire : un seul résultat, par exemple « obtenir 4 »", ["Événement élémentaire"]))
        self.play(*style_de(faces[4], ACCENT, 0.4))
        self.play(Indicate(faces[4], color=ACCENT, scale_factor=1.3))
        detail = self.detail(detail, tex(r"$\{4\}$", 46, {r"4": ACCENT}))
        self.wait(2.5)
        self.play(*style_de(faces[4], BLANC))

        legende = self.changer(legende, self.legende("Événement certain : « obtenir un nombre de 1 à 6 », il se réalise toujours", ["Événement certain"]))
        self.play(*[a for n in faces for a in style_de(faces[n], VERT, 0.35)])
        detail = self.detail(detail, tex(r"$\Omega$", 46, {r"\Omega": VERT}))
        self.wait(2.5)
        self.play(*[a for n in faces for a in style_de(faces[n], BLANC)])

        legende = self.changer(legende, self.legende("Événement impossible : « obtenir 7 », aucun résultat ne convient", ["Événement impossible"]))
        self.play(*[faces[n].animate.set_opacity(0.25) for n in faces])
        detail = self.detail(detail, tex(r"$\emptyset$", 46, {r"\emptyset": ROUGE}))
        self.wait(3.0)
        self.play(*[faces[n].animate.set_opacity(1) for n in faces])

        self.fin()
