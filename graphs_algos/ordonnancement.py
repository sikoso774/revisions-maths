"""Données et helpers communs aux chapitres 18 et 19 : le problème d'ordonnancement du TD2 (exercice 7)."""
from algo import *

# Les 8 tâches du TD2 : durée et antécédents
DUREES = {"A": 7, "B": 4, "C": 5, "D": 8, "E": 6, "F": 3, "G": 7, "H": 4}
ANTECEDENTS = {"A": [], "B": [], "C": [], "D": ["A", "B"], "E": ["B"], "F": ["B", "C"], "G": ["D", "E"], "H": ["D", "E", "F"]}
SOMMETS = ["α", "A", "B", "C", "D", "E", "F", "G", "H", "ω"]

# Graphe potentiel-tâches : α (début) -> tâches sans antécédent ; i -> j si i précède j ; tâches sans successeur -> ω (fin)
ARCS = [("α", t) for t in "ABC"] + [(p, t) for t in "ABCDEFGH" for p in ANTECEDENTS[t]] + [("G", "ω"), ("H", "ω")]
LONGUEUR = {(a, b): (0 if a == "α" else DUREES[a]) for a, b in ARCS}
POS = {
    "α": np.array([-5.6, 0.3, 0]),
    "A": np.array([-3.4, 1.7, 0]), "B": np.array([-3.4, 0.3, 0]), "C": np.array([-3.4, -1.1, 0]),
    "D": np.array([-0.6, 1.7, 0]), "E": np.array([-0.6, 0.3, 0]), "F": np.array([-0.6, -1.1, 0]),
    "G": np.array([2.5, 1.4, 0]), "H": np.array([2.5, -0.7, 0]),
    "ω": np.array([5.6, 0.3, 0]),
}


def nom_tex(v):
    return {"α": r"\alpha", "ω": r"\omega"}.get(v, v)


# Étiquettes décalées le long de l'arc quand deux arcs se croisent (D→H et E→G se croisent en leur milieu)
PROPORTION = {("D", "H"): 0.22, ("E", "G"): 0.30}
BAS = ("C", "F", "H")  # sommets du bas : la date s'affiche dessous, pour ne pas toucher les arcs entrants


def etiquette_longueur(arc, valeur, taille=22, couleur=ACCENT, p=0.5):
    """Longueur d'un arc affichée sur l'arc (à la proportion p), sur un fond noir."""
    t = Text(str(valeur), font_size=taille, color=couleur, weight=BOLD)
    fond = BackgroundRectangle(t, color=FOND, fill_opacity=1, buff=0.05)
    groupe = VGroup(fond, t).move_to(arc.point_from_proportion(p))
    groupe.set_z_index(3)
    return groupe


def date_label(sommet, valeur, bas=False):
    """Date de début au plus tôt, affichée au-dessus (ou au-dessous) du sommet."""
    return Text(f"t = {valeur}", font_size=20, color=ACCENT, weight=BOLD).next_to(sommet, DOWN if bas else UP, buff=0.08)
