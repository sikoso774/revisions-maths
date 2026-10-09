# revisions-maths

Révisions de maths en vidéos : la théorie des graphes et les algorithmes classiques, en animations.

Douze vidéos en français qui expliquent la théorie des graphes et les algorithmes classiques, du vocabulaire de base jusqu'à Dijkstra, Kruskal et Prim. Elles sont animées avec [Manim](https://www.manim.community/) (Community Edition) : fond noir, graphes en blanc, mots clés en couleur, formules en LaTeX.

Chaque chapitre suit le même schéma : un titre centré qui dézoome, les **formules avec leurs explications**, un dézoom sur un **exemple concret**, puis des **démonstrations pas à pas**. Pour les algorithmes, le pseudo-code s'exécute ligne par ligne à l'écran, avec la file, la pile ou les distances qui évoluent en direct.

> Les rendus 480p sont versionnés dans `media/videos/` (≈ 58 Mo). Les fichiers intermédiaires de Manim (morceaux de vidéo, SVG, `.tex`) sont ignorés par Git.

## Chapitres

| N° | Chapitre | Contenu | Vidéo (480p) |
|---|---|---|---|
| 1 | Qu'est-ce qu'un graphe ? | sommets, arêtes, G = (V, E), nombre d'arêtes possibles | [Definition.mp4](media/videos/ch01_definition/480p15/Definition.mp4) |
| 2 | Les grands types de graphes | non orienté, orienté, pondéré, poids d'un chemin | [Types.mp4](media/videos/ch02_types/480p15/Types.mp4) |
| 3 | Le degré d'un sommet | degré, somme des degrés = 2m, parité | [Degre.mp4](media/videos/ch03_degre/480p15/Degre.mp4) |
| 4 | Chemins et cycles | chemins, longueur, cycles, arbres | [CheminsCycles.mp4](media/videos/ch04_chemins_cycles/480p15/CheminsCycles.mp4) |
| 5 | La connexité | composantes connexes et fortement connexes, graphe des composantes | [Connexite.mp4](media/videos/ch05_connexite/480p15/Connexite.mp4) |
| 6 | Représenter un graphe en machine | matrice d'adjacence, liste d'adjacence, matrice d'incidence | [Representations.mp4](media/videos/ch06_representations/480p15/Representations.mp4) |
| 7 | Les arbres | caractérisations, arbre enraciné, arbre couvrant | [Arbres.mp4](media/videos/ch07_arbres/480p15/Arbres.mp4) |
| 8 | Parcours en largeur (BFS) | pseudo-code, file, couches, plus court chemin | [ParcoursLargeur.mp4](media/videos/ch08_bfs/480p15/ParcoursLargeur.mp4) |
| 9 | Parcours en profondeur (DFS) | pile d'appels, dates d/f, cycles, version itérative, BFS vs DFS | [ParcoursProfondeur.mp4](media/videos/ch09_dfs/480p15/ParcoursProfondeur.mp4) |
| 10 | L'algorithme de Dijkstra | relaxation pas à pas, exemple Paris → Nice | [Dijkstra.mp4](media/videos/ch10_dijkstra/480p15/Dijkstra.mp4) |
| 11 | Arbre couvrant minimal : Kruskal | propriété de coupe, liste triée, composantes | [Kruskal.mp4](media/videos/ch11_kruskal/480p15/Kruskal.mp4) |
| 12 | Arbre couvrant minimal : Prim | arêtes de la coupe, comparaison Kruskal / Prim | [Prim.mp4](media/videos/ch12_prim/480p15/Prim.mp4) |

À venir : Bellman-Ford, PageRank.

## Dépendances

### Outils à installer sur la machine

| Outil | Rôle | Remarque |
|---|---|---|
| [Python](https://www.python.org/) ≥ 3.12 | exécution | `uv` peut l'installer pour toi (`.python-version` = 3.12) |
| [uv](https://docs.astral.sh/uv/) | gestion de l'environnement et des dépendances | lit `pyproject.toml` et `uv.lock` |
| Une distribution LaTeX ([MiKTeX](https://miktex.org/) ou TeX Live) | composition des formules (`Tex`) | doit fournir `latex` et `dvisvgm` |
| Police **Consolas** | pseudo-code | présente sous Windows ; sur un autre système, Pango choisit une police de remplacement |

FFmpeg n'est **pas** nécessaire : Manim 0.22 utilise PyAV pour encoder les vidéos.

### Bibliothèques Python

Le seul paquet déclaré est `manim>=0.22.0` ; le reste en découle (versions figées dans `uv.lock`) :

| Paquet | Rôle dans le projet |
|---|---|
| `manim` 0.22 | moteur d'animation, classes `Graph`, `DiGraph`, `Tex`, `Text`… |
| `numpy`, `scipy`, `networkx` | calcul numérique ; `networkx` porte la structure interne de `manim.Graph` |
| `manimpango`, `pycairo`, `pillow`, `svgelements`, `skia-pathops` | rendu du texte et des formes vectorielles |
| `av` (PyAV) | encodage vidéo |
| `moderngl`, `moderngl-window` | rendu OpenGL (non utilisé ici, requis par Manim) |
| `click`, `cloup`, `rich`, `tqdm`, `pygments`, `watchdog`, `screeninfo` | ligne de commande, affichage, divers |

## Installation et rendu

```powershell
git clone <url-du-dépôt> revisions-maths
cd revisions-maths
git switch graph_algo
uv sync
```

Rendu d'un chapitre (depuis la racine du dépôt) :

```powershell
uv run manim -pql graphs_algos/ch08_bfs.py ParcoursLargeur     # aperçu rapide, 480p15
uv run manim -pqh graphs_algos/ch08_bfs.py ParcoursLargeur     # qualité finale, 1080p60
uv run manim -ql -s graphs_algos/ch08_bfs.py ParcoursLargeur   # image finale seulement
```

La scène à passer en argument est indiquée dans la colonne « Vidéo » (nom du fichier `.mp4`) ; l'architecture détaille la correspondance fichier ↔ scène. Les vidéos sont écrites dans `media/videos/<chapitre>/<qualité>/`. Les chapitres 5 à 12 prennent plusieurs minutes à rendre.

## Organisation du dépôt

```text
revisions-maths/
├── graphs_algos/        # code source : une scène Manim par chapitre
│   ├── common.py        # palette, scène de base, helpers de graphes
│   ├── algo.py          # pseudo-code surligné, file / pile animées
│   └── ch01_…ch12_*.py  # les 12 chapitres
├── media/videos/        # vidéos 480p versionnées (le reste de media/ est ignoré)
├── ARCHITECTURE.md      # conception détaillée du code
├── LICENSE              # MIT
├── pyproject.toml       # dépendances (uv)
└── uv.lock
```

La branche `graph_algo` regroupe l'ensemble du projet. Pour comprendre comment le code est construit et comment ajouter un chapitre, voir [ARCHITECTURE.md](ARCHITECTURE.md).

## Licence

Projet sous licence [MIT](LICENSE) — © 2026 Zoléni KOKOLO ZASSI.
