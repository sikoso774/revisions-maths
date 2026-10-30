"""Chapitre 6 : le paradoxe des anniversaires (exercice 2.3.6)."""
from itertools import combinations
from common import *
from proba import *


def p_anniv(n):
    """Probabilité que, parmi n personnes, au moins deux fêtent leur anniversaire le même jour."""
    if n < 2:
        return 0.0
    if n > 365:
        return 1.0
    toutes_differentes = 1.0
    for k in range(n):
        toutes_differentes *= (365 - k) / 365
    return 1 - toutes_differentes


def p_martin(n):
    """Probabilité qu'au moins un des n-1 autres élèves fête son anniversaire le même jour que Martin."""
    return 1 - (364 / 365) ** (n - 1) if n >= 1 else 0.0


class Chapitre06(SceneProbas):
    def construct(self):
        titre = self.intro("Le paradoxe des anniversaires", 6)

        # ── Théorie ─────────────────────────────────────────────────────────
        carte = self.carte(
            "Au moins deux dates identiques : le contraire",
            ACCENT,
            [tex(r"$P(\text{au moins 2 identiques})=1-P(\text{toutes différentes})$", 38)],
            [
                texte("365 jours dans l'année, toutes les dates de naissance sont équiprobables", 26, ["équiprobables"]),
                texte("Le contraire n'a qu'un seul cas : les N élèves ont des dates toutes différentes", 26, ["un seul cas"]),
            ],
        )
        self.play(FadeOut(carte))
        carte = self.carte(
            "Formule générale pour N élèves",
            ACCENT,
            [tex(r"$P(N)=1-\dfrac{365\times 364\times\cdots\times(365-N+1)}{365^N}=1-\dfrac{A_{365}^N}{365^N}$", 40)],
            [
                texte("Au numérateur : un arrangement, l'ordre compte et les dates sont toutes différentes", 26, ["arrangement"]),
                texte("Au dénominateur : 365 dates possibles pour chacun des N élèves", 26, ["365 dates possibles"]),
            ],
        )

        # ── Démonstration 1 : 2 puis 3 élèves ──────────────────────────────────
        positions = [-4.4, 0.0, 4.4]
        cadres = [Rectangle(width=3.4, height=1.3, stroke_color=GRIS, stroke_width=3).move_to([x, 0.7, 0]) for x in positions]
        noms = [Text(f"élève {k + 1}", font_size=24, weight=BOLD, color=GRIS).move_to([x, 1.7, 0]) for k, x in enumerate(positions)]
        legende = self.legende("On attribue une date de naissance à chaque élève, l'un après l'autre", ["l'un après l'autre"])
        self.dezoom(carte, *[Create(c) for c in cadres[:2]], *[FadeIn(n) for n in noms[:2]], FadeIn(legende))
        self.wait(1.5)

        choix = []
        for k in range(2):
            valeur = 365 - k
            sous = "n'importe quelle date" if k == 0 else "pas celle de l'élève 1"
            t = VGroup(Tex(f"${valeur}$", font_size=44, color=ACCENT), Text(sous, font_size=18, color=GRIS)).arrange(DOWN, buff=0.08)
            t.move_to(cadres[k].get_center())
            choix.append(t)
        self.play(FadeIn(choix[0], shift=UP * 0.2))
        self.wait(1.5)
        legende = self.changer(legende, self.legende("Avec 2 élèves : le 2e doit tomber sur la date du 1er, 1 chance sur 365", ["1 chance sur 365"]))
        self.play(FadeIn(choix[1], shift=UP * 0.2))
        detail = self.detail(None, tex(r"$P(\text{même jour})=\dfrac{1}{365}\approx 0{,}27\,\%$", 44, {r"0{,}27\,\%": ACCENT}))
        self.wait(4.0)

        legende = self.changer(legende, self.legende("Avec 3 élèves : le 3e doit éviter les deux dates déjà prises", ["3 élèves"]))
        self.play(Create(cadres[2]), FadeIn(noms[2]))
        troisieme = VGroup(Tex("$363$", font_size=44, color=ACCENT), Text("ni l'une ni l'autre", font_size=18, color=GRIS)).arrange(DOWN, buff=0.08)
        troisieme.move_to(cadres[2].get_center())
        self.play(FadeIn(troisieme, shift=UP * 0.2))
        detail = self.detail(detail, tex(r"$P(\text{toutes différentes})=\dfrac{365\times 364\times 363}{365\times 365\times 365}$", 42))
        self.wait(4.5)
        detail = self.detail(detail, tex(r"$P(\text{au moins 2})=1-\dfrac{365\times 364\times 363}{365^3}\approx 0{,}0082=0{,}82\,\%$", 40, {r"0{,}82\,\%": ACCENT}))
        self.wait(5.0)
        self.vider(titre)

        # ── Démonstration 2 : la fonction R et la courbe ───────────────────────────
        code1 = bloc_code(
            [(0, "anniv <- function(N) {"), (1, "1 - prod(365:(365 - N + 1)) / 365^N"), (0, "}")],
            "R : traduction directe de la formule", {"function": VIOLET, "prod": BLEU}, taille=24,
        ).move_to([0, 0.7, 0])
        note = Text("Les valeurs de la courbe sont calculées ici avec la même formule", font_size=20, color=GRIS)
        note.next_to(code1, DOWN, buff=0.35)
        legende = self.legende("La formule se traduit presque mot pour mot en une fonction R", ["fonction R"])
        self.play(FadeIn(code1, shift=UP * 0.2), FadeIn(legende))
        self.play(FadeIn(note))
        self.wait(5.0)

        axes = Axes(
            x_range=[0, 400, 100], y_range=[0, 1, 0.5], x_length=6.4, y_length=2.8,
            axis_config={"include_tip": False, "stroke_width": 2, "color": GRIS},
        ).move_to([3.0, 0.75, 0])
        graduations = VGroup(
            *[Tex(f"${v}$", font_size=22, color=GRIS).move_to(axes.c2p(v, 0) + DOWN * 0.28) for v in (0, 100, 200, 300, 400)],
            *[Tex(t, font_size=22, color=GRIS).move_to(axes.c2p(0, v) + LEFT * 0.3) for v, t in ((0.5, "$0{,}5$"), (1, "$1$"))],
        )
        nom_x = Text("N (nombre de personnes)", font_size=18, color=GRIS).next_to(axes, DOWN, buff=0.5)
        nom_y = Tex(r"$P(N)$", font_size=26, color=GRIS).next_to(axes.c2p(0, 1), UP + RIGHT * 0.2, buff=0.1)
        legende = self.changer(legende, self.legende("On calcule P(N) pour N de 2 à 400 et on trace la courbe", ["P(N)"]))
        self.play(
            code1.animate.scale(0.62).move_to([-3.9, 1.5, 0]),
            note.animate.scale(0.62).move_to([-3.9, 0.55, 0]),
            Create(axes), FadeIn(graduations), FadeIn(nom_x), FadeIn(nom_y),
            run_time=2.0,
        )
        courbe = VMobject(stroke_color=VERT, stroke_width=5)
        courbe.set_points_as_corners([axes.c2p(n, p_anniv(n)) for n in range(2, 401)])
        self.play(Create(courbe), run_time=4.0, rate_func=linear)
        self.wait(1.0)

        # N = 23
        legende = self.changer(legende, self.legende("Avec seulement 23 personnes, la probabilité dépasse déjà 1 chance sur 2", ["23 personnes"]))
        point = Dot(axes.c2p(23, p_anniv(23)), color=ACCENT, radius=0.09)
        lignes = VGroup(
            DashedLine(axes.c2p(0, 0.5), axes.c2p(23, p_anniv(23)), color=ACCENT, stroke_width=2),
            DashedLine(axes.c2p(23, 0), axes.c2p(23, p_anniv(23)), color=ACCENT, stroke_width=2),
        )
        etiquette = Tex(r"$N=23$", font_size=30, color=ACCENT).next_to(point, RIGHT, buff=0.35).shift(DOWN * 0.45)
        self.play(Create(lignes), FadeIn(point), FadeIn(etiquette))
        detail = self.detail(None, tex(r"$P(22)\approx 0{,}476\qquad P(23)\approx 0{,}507$", 44, {r"0{,}507": ACCENT}))
        self.wait(5.0)

        legende = self.changer(legende, self.legende("Et dès 57 personnes, on dépasse 99 %", ["57 personnes", "99 %"]))
        point2 = Dot(axes.c2p(57, p_anniv(57)), color=VIOLET, radius=0.09)
        etiquette2 = Tex(r"$N=57$", font_size=30, color=VIOLET).move_to(point2.get_center() + np.array([0.85, -0.4, 0]))
        self.play(FadeIn(point2), FadeIn(etiquette2))
        detail = self.detail(detail, tex(r"$P(57)\approx 0{,}990$", 44, {r"0{,}990": VIOLET}))
        self.wait(4.0)

        # Le cas de Martin
        legende = self.changer(legende, self.legende("Autre question : quelqu'un partage-t-il la date de Martin, un élève précis ?", ["Martin"]))
        detail = self.detail(detail, tex(r"$P(\text{personne ne partage sa date})=\left(\dfrac{364}{365}\right)^{N-1}$", 36))
        self.wait(5.0)
        code2 = bloc_code(
            [(0, "anniv2 <- function(N) {"), (1, "1 - (364/365)^(N - 1)"), (0, "}")],
            "R : le cas de Martin", {"function": VIOLET}, taille=24,
        ).scale(0.62).move_to([-3.9, -0.55, 0])
        detail = self.detail(detail, tex(r"$P(\text{au moins un partage sa date})=1-\left(\dfrac{364}{365}\right)^{N-1}$", 36))
        self.play(FadeIn(code2, shift=UP * 0.2), FadeOut(note))
        courbe2 = VMobject(stroke_color=ROUGE, stroke_width=5)
        courbe2.set_points_as_corners([axes.c2p(n, p_martin(n)) for n in range(1, 401)])
        self.play(Create(courbe2), run_time=4.0, rate_func=linear)
        self.wait(1.0)

        legende = self.changer(legende, self.legende("Pour Martin, il faut attendre N = 254 pour dépasser 1 chance sur 2", ["N = 254"]))
        point3 = Dot(axes.c2p(254, p_martin(254)), color=ROUGE, radius=0.09)
        lignes3 = DashedLine(axes.c2p(254, 0), axes.c2p(254, p_martin(254)), color=ROUGE, stroke_width=2)
        etiquette3 = Tex(r"$N=254$", font_size=30, color=ROUGE).next_to(point3, DOWN, buff=0.3).shift(LEFT * 0.4)
        self.play(Create(lignes3), FadeIn(point3), FadeIn(etiquette3))
        detail = self.detail(detail, tex(r"$N=23\ \text{ou}\ N=254$ \quad la question change tout", 44, {r"N=254": ROUGE}))
        self.wait(5.0)
        self.vider(titre)

        # ── Démonstration 3 : pourquoi l'écart ? Les paires ───────────────────────
        centre = np.array([0, 0.4, 0])
        n = 23
        pts = [centre + 1.9 * np.array([np.cos(np.radians(180 - 360 * i / n)), np.sin(np.radians(180 - 360 * i / n)), 0]) for i in range(n)]
        personnes = VGroup(*[Dot(p, radius=0.13, color=BLANC) for p in pts])
        personnes[0].set_color(ACCENT).scale(1.4)
        nom_martin = Text("Martin", font_size=24, weight=BOLD, color=ACCENT).next_to(personnes[0], LEFT, buff=0.2)
        for p in personnes:
            p.set_z_index(3)
        legende = self.legende("23 élèves : combien de paires d'élèves peuvent partager une date ?", ["paires"])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in personnes], lag_ratio=0.05), FadeIn(nom_martin), FadeIn(legende))
        self.wait(1.5)

        liens_martin = VGroup(*[Line(pts[0], pts[j], stroke_color=ROUGE, stroke_width=3) for j in range(1, n)])
        legende = self.changer(legende, self.legende("Les paires qui impliquent Martin : 22", ["22"]))
        self.play(LaggedStart(*[Create(l) for l in liens_martin], lag_ratio=0.1), run_time=3.0)
        detail = self.detail(None, tex(r"$N-1=22$ paires avec Martin", 44, {r"22": ROUGE}))
        self.wait(3.5)

        autres = VGroup(*[Line(pts[i], pts[j], stroke_color=VERT, stroke_width=1.5, stroke_opacity=0.7) for i, j in combinations(range(1, n), 2)])
        legende = self.changer(legende, self.legende("Mais n'importe quelle paire du groupe peut créer une coïncidence", ["n'importe quelle paire"]))
        self.play(LaggedStart(*[Create(l) for l in autres], lag_ratio=0.01), run_time=4.0)
        detail = self.detail(detail, tex(r"$\dbinom{23}{2}=\dfrac{23\times 22}{2}=253$ paires au total", 44, {r"253": VERT}))
        self.wait(5.0)

        legende = self.changer(legende, self.legende("253 occasions de coïncidence contre 22 : c'est tout le paradoxe", ["253", "22"]))
        self.wait(5.0)
        legende = self.changer(legende, self.legende("On pense spontanément « coïncidence avec moi », alors que la question porte sur « n'importe quelle coïncidence »", ["n'importe quelle coïncidence"]))
        self.wait(5.0)

        self.fin()
