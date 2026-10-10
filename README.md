# revisions-maths — branche `probas_stats`

Révisions de maths en vidéos [Manim](https://www.manim.community/) (Community Edition), en français : fond noir, mots clés en couleur, formules en LaTeX.

Cette branche est consacrée aux **probabilités et statistiques**. Elle est en cours de démarrage : **aucune vidéo n'est encore produite**. Elle repart du socle commun du projet (palette, scène de base, outils d'animation), sans les chapitres de graphes.

> Les 14 vidéos sur la **théorie des graphes** (BFS, DFS, Dijkstra, Bellman-Ford, Kruskal, Prim, PageRank…) sont sur la branche [`graph_algo`](https://github.com/sikoso774/revisions-maths/tree/graph_algo), figées dans les tags `v1.0` et `v1.1`.

## Contenu prévu

Le plan des chapitres n'est pas encore arrêté. Les notes de cours servant de point de départ portent sur :

- le dénombrement et le choix de la bonne formule ;
- le modèle probabiliste et ses exercices ;
- les systèmes complets d'événements ;
- les règles de calcul des probabilités et les méthodes statistiques.

## Dépendances

### Outils à installer sur la machine

| Outil | Rôle | Remarque |
|---|---|---|
| [Python](https://www.python.org/) ≥ 3.12 | exécution | `uv` peut l'installer pour toi (`.python-version` = 3.12) |
| [uv](https://docs.astral.sh/uv/) | gestion de l'environnement et des dépendances | lit `pyproject.toml` et `uv.lock` |
| Une distribution LaTeX ([MiKTeX](https://miktex.org/) ou TeX Live) | composition des formules (`Tex`) | doit fournir `latex` et `dvisvgm` |
| Police **Consolas** | pseudo-code (`PanneauCode` dans `algo.py`) | présente sous Windows ; sur un autre système, Pango choisit une police de remplacement |

FFmpeg n'est **pas** nécessaire : Manim 0.22 utilise PyAV pour encoder les vidéos.

### Bibliothèques Python

Le seul paquet déclaré est `manim>=0.22.0` ; le reste en découle (versions figées dans `uv.lock`) :

| Paquet | Rôle dans le projet |
|---|---|
| `manim` 0.22 | moteur d'animation, classes `Tex`, `Text`, `Graph`… |
| `numpy`, `scipy`, `networkx` | calcul numérique ; `networkx` porte la structure interne de `manim.Graph` |
| `manimpango`, `pycairo`, `pillow`, `svgelements`, `skia-pathops` | rendu du texte et des formes vectorielles |
| `av` (PyAV) | encodage vidéo |
| `moderngl`, `moderngl-window` | rendu OpenGL (non utilisé ici, requis par Manim) |
| `click`, `cloup`, `rich`, `tqdm`, `pygments`, `watchdog`, `screeninfo` | ligne de commande, affichage, divers |

## Installation et rendu

```powershell
git clone <url-du-dépôt> revisions-maths
cd revisions-maths
git switch probas_stats
uv sync
```

Rendu d'une scène (depuis la racine du dépôt), une fois un chapitre écrit :

```powershell
uv run manim -pql graphs_algos/<fichier>.py <Scène>     # aperçu rapide, 480p15
uv run manim -ql -s graphs_algos/<fichier>.py <Scène>   # image finale seulement
```

Les vidéos sont écrites dans `media/videos/<chapitre>/<qualité>/`. Seuls les rendus 480p sont suivis par Git ; les fichiers intermédiaires (morceaux partiels, SVG, `.tex`) sont ignorés.

## Organisation du dépôt

```text
revisions-maths/
├── graphs_algos/        # socle commun (le nom du dossier sera à revoir pour cette branche)
│   ├── common.py        # palette, scène de base, textes et formules, helpers
│   └── algo.py          # pseudo-code surligné, file / pile animées
├── ARCHITECTURE.md      # vide pour l'instant (à rédiger avec les premiers chapitres)
├── LICENSE              # MIT
├── pyproject.toml       # dépendances (uv)
└── uv.lock
```

`media/` n'existe pas encore : il sera créé au premier rendu.

## Licence

Projet sous licence [MIT](LICENSE) — © 2026 Zoléni KOKOLO ZASSI.
