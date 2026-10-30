# revisions-maths — branche `probas_stats`

Révisions de maths en vidéos [Manim](https://www.manim.community/) (Community Edition), en français : fond noir, mots clés en couleur, formules en LaTeX.

Cette branche est consacrée aux **probabilités et statistiques**. Elle est en cours : les **5 premiers chapitres du bloc A** (modèle probabiliste) sont rendus en 480p. Elle repart du socle commun du projet (palette, scène de base, outils d'animation), sans les chapitres de graphes.

> Les 14 vidéos sur la **théorie des graphes** (BFS, DFS, Dijkstra, Bellman-Ford, Kruskal, Prim, PageRank…) sont sur la branche [`graph_algo`](https://github.com/sikoso774/revisions-maths/tree/graph_algo), figées dans les tags `v1.0` et `v1.1`.

## Chapitres

Chaque chapitre : cartes de formules LaTeX, puis démonstration animée (dés, urnes, barres de probabilité, arbres), en français.

| N° | Chapitre | Contenu | Vidéo |
|---|---|---|---|
| 1 | Expérience aléatoire et événements | univers Ω, événements, ∩, ∪, contraire, événements particuliers | `ch01_experience_evenements` |
| 2 | Calculer une probabilité | cas favorables / possibles, contraire, addition, De Morgan, exercice 2.3.1 | `ch02_calculer_probabilite` |
| 3 | Dénombrement : choisir la bonne formule | p-liste, arrangement, permutation, combinaison, tiercé et quinté, exercices 2.3.2 et 2.3.3 | `ch03_denombrement` |
| 4 | Système complet d'événements | partition de Ω, ET / OU, « au moins » par le contraire, exercice 2.3.4 | `ch04_systeme_complet` |
| 5 | Tirages dans une urne | tirage simultané, tirages avec remise, arbre, embryon de la loi binomiale, exercice 2.3.5 | `ch05_tirages_urne` |

**À venir** : chapitre 6 (paradoxe des anniversaires, exercice 2.3.6) pour finir le bloc A, puis conditionnement et indépendance, variables aléatoires et lois usuelles, statistique inférentielle.

## Dépendances

### Outils à installer sur la machine

| Outil | Rôle | Remarque |
|---|---|---|
| [Python](https://www.python.org/) ≥ 3.12 | exécution | `uv` peut l'installer pour toi (`.python-version` = 3.12) |
| [uv](https://docs.astral.sh/uv/) | gestion de l'environnement et des dépendances | lit `pyproject.toml` et `uv.lock` |
| Une distribution LaTeX ([MiKTeX](https://miktex.org/) ou TeX Live) | composition des formules (`Tex`) | doit fournir `latex` et `dvisvgm` |

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

Rendu d'une scène (depuis la racine du dépôt), par exemple `uv run manim -ql probas_stats/ch01_experience_evenements.py Chapitre01` :

```powershell
uv run manim -pql probas_stats/<fichier>.py <Scène>     # aperçu rapide, 480p15
uv run manim -ql -s probas_stats/<fichier>.py <Scène>   # image finale seulement
```

Les vidéos sont écrites dans `media/videos/<chapitre>/<qualité>/`. Seuls les rendus 480p sont suivis par Git ; les fichiers intermédiaires (morceaux partiels, SVG, `.tex`) sont ignorés.

## Organisation du dépôt

```text
revisions-maths/
├── probas_stats/
│   ├── common.py        # palette, scène de base, textes et formules
│   ├── proba.py         # dés, univers, urnes, diagramme de Venn du dé
│   └── chNN_*.py        # un fichier par chapitre (une scène chacun)
├── media/videos/        # vidéos 480p suivies par Git (une par chapitre)
├── ARCHITECTURE.md      # vide pour l'instant (à rédiger quand le bloc A sera terminé)
├── LICENSE              # MIT
├── pyproject.toml       # dépendances (uv)
└── uv.lock
```

Le dossier `media/` est créé au premier rendu ; seuls les `.mp4` en 480p y sont versionnés.

## Licence

Projet sous licence [MIT](LICENSE) — © 2026 Zoléni KOKOLO ZASSI.
