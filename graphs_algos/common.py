"""Briques communes aux chapitres : palette, scène de base, helpers de graphes."""
from manim import *
import numpy as np

FOND = "#000000"
BLANC = "#FFFFFF"
TEXTE = BLANC
NOEUD = BLANC  # sommets des graphes (étiquette en noir)
LIEN = BLANC  # arêtes des graphes
SOMMET = "#38BDF8"  # bleu : mot « sommet » dans les textes
ARETE = "#94A3B8"  # gris : notes secondaires
ACCENT = "#FBBF24"  # jaune : mise en avant, arêtes
ROUGE = "#F87171"
VERT = "#4ADE80"
VIOLET = "#A78BFA"


def texte(contenu, taille=30, cles=None, couleur=TEXTE, **kwargs):
    """Texte avec mots clés colorés et en gras.

    `cles` : liste de mots (colorés en ACCENT) ou dict {mot: couleur}.
    """
    if cles is None:
        cles = {}
    if not isinstance(cles, dict):
        cles = {mot: ACCENT for mot in cles}
    return Text(
        contenu,
        font_size=taille,
        color=couleur,
        t2c=cles,
        t2w={mot: BOLD for mot in cles},
        **kwargs,
    )


def tex(contenu, taille=36, cles=None, couleur=TEXTE):
    """Texte LaTeX (mode texte, formules entre $...$) ; `cles` : {mot: couleur}."""
    return Tex(contenu, font_size=taille, color=couleur, tex_to_color_map=cles or {})


CENTRE_DETAIL = np.array([0, -2.55, 0])


class SceneGraphes(Scene):
    """Scène de base : fond, titre animé, légendes et sortie de chapitre cohérents."""

    def setup(self):
        self.camera.background_color = FOND

    def intro(self, contenu, numero=None):
        """Titre centré en grand, qui dézoome et monte en haut ; un trait jaune se déploie dessous."""
        titre = Text(contenu, font_size=44, weight=BOLD, color=TEXTE).to_edge(UP, buff=0.4)
        facteur = min(2.0, 11 / titre.width)  # grand, mais toujours dans le cadre
        grand = titre.copy().scale(facteur).move_to(ORIGIN)
        etiquette = None
        if numero is not None:
            etiquette = Text(f"CHAPITRE {numero}", font_size=26, color=ACCENT, weight=BOLD)
            etiquette.next_to(grand, UP, buff=0.5)
            self.play(FadeIn(etiquette, shift=DOWN * 0.3), run_time=0.6)
        self.play(Write(grand), run_time=1.5)
        self.wait(0.8)
        self.play(
            grand.animate.scale(1 / facteur).to_edge(UP, buff=0.4),
            *([FadeOut(etiquette, shift=UP * 0.3)] if etiquette else []),
            run_time=1.3,
            rate_func=smooth,
        )
        trait = Line(
            grand.get_corner(DL) + DOWN * 0.12,
            grand.get_corner(DR) + DOWN * 0.12,
            color=ACCENT,
            stroke_width=4,
        )
        self.play(GrowFromCenter(trait), run_time=0.6)
        self.trait_titre = trait
        return grand

    def legende(self, contenu, cles=None, taille=30):
        t = texte(contenu, taille, cles)
        if t.width > 13:  # rester dans le cadre (largeur visible : ~14,2)
            t.scale_to_fit_width(13)
        return t.to_edge(DOWN, buff=0.5)

    def changer(self, ancien, nouveau):
        """Une légende sort, puis la suivante entre (jamais superposées)."""
        self.play(
            LaggedStart(
                FadeOut(ancien, shift=DOWN * 0.3),
                FadeIn(nouveau, shift=DOWN * 0.3),
                lag_ratio=1.0,
            ),
            run_time=1.0,
        )
        return nouveau

    def detail(self, ancien, contenu, cles=None):
        """Phrase explicative au-dessus du tableau ; remplace la précédente."""
        nouveau = texte(contenu, 28, cles)
        if nouveau.width > 12.8:
            nouveau.scale_to_fit_width(12.8)
        nouveau.move_to(CENTRE_DETAIL)
        if ancien is None:
            self.play(FadeIn(nouveau, shift=DOWN * 0.15))
        else:
            self.play(
                LaggedStart(
                    FadeOut(ancien, shift=DOWN * 0.15),
                    FadeIn(nouveau, shift=DOWN * 0.15),
                    lag_ratio=1.0,
                ),
                run_time=0.8,
            )
        return nouveau

    def carte(self, titre, couleur, formules, explications):
        """Une « carte » théorique : titre, formules LaTeX, puis explications une à une.

        Renvoie le groupe complet, déjà affiché.
        """
        entete = Text(titre, font_size=36, weight=BOLD, color=couleur)
        if entete.width > 12.5:
            entete.scale_to_fit_width(12.5)
        entete.move_to(UP * 2.35)
        bloc = VGroup(*formules).arrange(DOWN, buff=0.35).next_to(entete, DOWN, buff=0.4)
        lignes = VGroup(*explications).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        lignes.next_to(bloc, DOWN, buff=0.45)
        if lignes.width > 12.5:
            lignes.scale_to_fit_width(12.5)
        lignes.set_x(0)

        self.play(FadeIn(entete, shift=DOWN * 0.2))
        for formule in formules:
            self.play(Write(formule), run_time=2)
            self.wait(1.5)
        for ligne in lignes:
            self.play(FadeIn(ligne, shift=UP * 0.2))
            self.wait(2.5)
        self.wait(1.5)
        return VGroup(entete, bloc, lignes)

    def dezoom(self, theorie, *animations, duree=3):
        """La théorie rétrécit et s'estompe pendant que l'exemple concret apparaît."""
        self.play(
            theorie.animate.scale(0.1).set_opacity(0),
            *animations,
            run_time=duree,
            rate_func=smooth,
        )
        self.remove(theorie)

    def fin(self, pause=1.5):
        """Fin de chapitre : courte pause, puis tout s'estompe."""
        if config.save_last_frame:  # mode -s : garder l'image finale lisible
            return
        self.wait(pause)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.3)


def parties(g):
    """Sommets et arêtes d'un graphe, comme objets indépendants (pour fondus et transformations)."""
    return VGroup(*g.vertices.values(), *g.edges.values())


def apparition(g):
    """Les sommets jaillissent un à un, puis les arêtes se tracent."""
    return Succession(
        LaggedStart(*[GrowFromCenter(v) for v in g.vertices.values()], lag_ratio=0.15),
        LaggedStart(*[Create(e) for e in g.edges.values()], lag_ratio=0.15),
    )


def positions_cercle(sommets, rayon=2.0, centre=ORIGIN, depart=90):
    """Place les sommets régulièrement sur un cercle (premier sommet en haut)."""
    n = len(sommets)
    return {
        v: centre + rayon * np.array([
            np.cos(np.radians(depart - 360 * i / n)),
            np.sin(np.radians(depart - 360 * i / n)),
            0,
        ])
        for i, v in enumerate(sommets)
    }


def creer_graphe(sommets, aretes, positions, orientee=False, rayon=0.3, couleur=NOEUD):
    """Graphe avec sommets étiquetés (Text, donc sans LaTeX)."""
    labels = {v: Text(str(v), font_size=30, color=FOND, weight=BOLD) for v in sommets}
    config_arete = {"stroke_color": LIEN, "stroke_width": 5}
    if orientee:
        config_arete["tip_config"] = {"tip_length": 0.25, "tip_width": 0.25}
    classe = DiGraph if orientee else Graph
    g = classe(
        sommets,
        aretes,
        layout=positions,
        labels=labels,
        vertex_type=LabeledDot,
        vertex_config={"fill_color": couleur, "radius": rayon},
        edge_config=config_arete,
    )
    for sommet in g.vertices.values():
        sommet.set_z_index(2)  # les sommets restent au-dessus des arêtes
    return g


def colorier(g, v, couleur):
    """Anime le remplissage du sommet v sans toucher à la couleur de son étiquette."""
    return g.vertices[v].animate.set_fill(couleur, family=False)


def arete(g, u, v):
    """Arête u-v quel que soit l'ordre dans lequel elle a été déclarée."""
    return g.edges[(u, v)] if (u, v) in g.edges else g.edges[(v, u)]


def etiquette_poids(g, u, v, valeur):
    """Poids affiché au milieu de l'arête, sur un fond qui masque le trait."""
    contenu = Text(str(valeur), font_size=26, color=ACCENT, weight=BOLD)
    fond = BackgroundRectangle(contenu, color=FOND, fill_opacity=1, buff=0.08)
    groupe = VGroup(fond, contenu).move_to(arete(g, u, v).get_center())
    groupe.set_z_index(3)
    return groupe
