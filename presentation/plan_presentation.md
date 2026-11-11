# Plan de la soutenance (environ 9 min 45)

**Fil rouge :** peut-on deviner le niveau d'un joueur d'échecs à partir d'une seule partie, et le faire équitablement, quelle que soit sa nationalité ?

**Image qui revient tout au long :** Qwen est un nouvel employé très cultivé qui n'a jamais estimé un Elo.
Prompt = on lui donne des consignes (et quelques exemples). RAG = on lui donne des dossiers de cas similaires. Fine-tuning = on le forme vraiment. XAI = on lui demande de justifier ses décisions.

**Fichiers :**
- `presentation/soutenance.pdf` : la présentation, projetée telle quelle (16:9, 41 pages : 30 de présentation, 11 d'annexes).
- `presentation/texte_oral.md` : **le texte à dire**, page par page, avec les [clic], les durées et les réponses aux questions.
- `presentation/figures/` : les visuels en SVG (échiquiers et graphiques, sans photo).
- `presentation/logos/` : logos officiels téléchargés (non versionnés, sources ci-dessous).
- `presentation/apercu/` : une image PNG par page du PDF, pour relire (non versionnée : elle contient nos photos).

## Minutage

| Présentateur | Pages | Durée |
|---|---|---|
| — | 1 (titre) | 0 s, affichée pendant l'installation |
| Thibault | 2 à 16 | 3 min 30 |
| Maël | 17 à 24 | 3 min 20 |
| Hugo | 25 à 30 | 2 min 40 |
| **Total** | 30 pages | **9 min 30** de parole, environ **9 min 45** avec les passages de relais |

Détail : 2 (15 s), 3 à 9 (30 s en tout), 10 (15 s), 11 (30 s), 12 (25 s), 13 (20 s), 14 (30 s), 15 (25 s), 16 (20 s) | 17 (25 s), 18 (25 s), 19 (30 s), 20 (25 s), 21 (20 s), 22 (25 s), 23 (20 s), 24 (30 s) | 25 (35 s), 26 (20 s), 27 (40 s), 28 (30 s), 29 (clic), 30 (35 s).

Les six pages ajoutées (problème, explication de chaque méthode, contexte de la démo, « Conclusion ») ont été compensées en raccourcissant les pages de résultats, qui n'ont plus à expliquer la méthode. Raccourcis possibles en cas de retard : voir `texte_oral.md`.

---

## Corrections apportées aux chiffres du brief

Tous les chiffres ont été recalculés à partir des CSV du dépôt. Ceux-ci étaient faux ou demandaient une précision :

| # | Dans le brief | Valeur vérifiée | Source |
|---|---|---|---|
| 1 | Few-shot : « **3** exemples mal choisis » | **7 exemples** (un par tranche d'Elo). Brésil : −243 avec le pays dans les exemples, **−62** sans. −62 reste significatif. | `resultats_prompting_v2/comparaison_premiere_execution.csv`, `resultats_finetuning_complets/biais_ecarts_france.csv` |
| 2 | Dataset « équilibré » | Équilibré **en proportions** : par tranche, 240 parties françaises et 90 pour chacun des 4 autres pays (la France fait 40 % du dataset). Chaque pays a la même répartition de niveaux : le pays ne dit rien de l'Elo. | `data/prompts/*.jsonl`, `07_rendu_final.ipynb` section 2 |
| 3 | ACPL « ~109 » et « ~40 » | Ce sont des **médianes** : 109,5 (100-400) et 39,5 (1900+). Moyennes : 122 et 44. | `data/prompts/{train,val,test}.jsonl` |
| 4 | « 1800 une fois sur deux » | **44,9 %** des réponses : « près d'une fois sur deux ». | `resultats_finetuning_complets/valeurs_frequentes.csv` |
| 5 | « ~20 valeurs comme 101 » | **23 valeurs** (FT-A et FT-B), surtout 1677 et 1777 ; 101 : 4,1 % (FT-A), 9,6 % (FT-B). | `resultats_finetuning_complets/valeurs_frequentes.csv` |
| 6 | RAG : « écarts < 20 points » | Juste pour l'**écart moyen à la France** (au plus +17,5). Partie par partie, le pays change encore 36 % des prédictions (étendue moyenne 58). | `biais_ecarts_france.csv`, `biais_etendue_par_partie.csv` |
| 7 | « Effet du pays » 150 → 16 | Juste. C'est l'**étendue moyenne** : même partie avec les 5 pays, plus haute prédiction moins plus basse, moyenne sur 140 parties. 120 = few-shot v2. | `resultats_finetuning_complets/biais_etendue_par_partie.csv` |
| 8 | « Le pays pèse 15 % » | **15,5 %** (SHAP), 2e variable sur 12 ; 1,0 % (FT-A), 0,2 % (FT-B, 11e sur 12). | `resultats_xai/part_du_pays.csv` |
| 9 | Paul : « retire 100 Elo ; le nôtre, presque rien » | Sur ses 10 parties : le modèle de base retire **95 points en moyenne** (7 parties sur 10, jusqu'à −200). FT-B : **+10 en moyenne** (une seule partie bouge, de +100). | `resultats_demo/france_etats_unis.csv` |
| 10 | Comptes « bannis » exclus | Tous les **comptes fermés** sont exclus, dont les bannis pour triche. | `build_dataset.py` |
| 11 | Démo : « 10 parties, 5 pour Hugo » | Confirmé : 10 parties pour Thibault, Maël et Paul, 5 pour Hugo ; 88 prédictions par modèle, toutes lues. Les 3 premières parties de chacun redonnent exactement les valeurs de 06_xai. | `resultats_demo/elo_moyen_par_joueur.csv` |

---

## Direction artistique

- **Style keynote :** fond blanc, titres en phrases de 40 px, grands chiffres, cartes aux coins arrondis (28 px), beaucoup d'espace. Police Segoe UI Variable. Texte à 24 px minimum sur une page de 1 280 × 720 px (au moins 18 pt projeté), sauf le libellé de bas de page.
- **Charte ECE :** sarcelle `#036F78` (extraite de `presentation/ece.png`) ; sarcelle foncée `#024C52` ; teinte claire `#E6F1F2` pour les cartes.
- **Bas de page :** libellé de la matière « Ethics of AI · ECE · DATA IA » en gris clair, en bas à gauche (sauf sur la slide de titre) ; numéro de page dans un pion dessiné, en bas à droite.
- **Slides de transition** (titre, feuille de route, « Et sur nous ? », « Conclusion », bilan, annexes) : fond sarcelle avec un motif discret d'échiquier en fondu.
- **Une seule famille d'icônes :** Font Awesome 6 Free (pleines), via `react-icons`.
- **Couleurs des méthodes, constantes partout :** Zero-shot brique `#C8553D`, Few-shot ambre `#E9A23B`, RAG prune `#7A5C99`, FT-A bleu `#3A86C8`, FT-B sarcelle ECE `#036F78`. Chaque élément porte aussi son icône et son nom, pour rester lisible en noir et blanc.
- **Pastille de méthode** (logo Qwen3 + « Méthode N · … ») en bas à droite des pages 17 à 23.
- **Badges de coups (dessin maison) :** « ! » bleu `#2F7FD8` (bon coup), « !! » sarcelle `#1BA39C` (seul coup gagnant), « ?? » rouge `#D7263D` (gaffe, case entourée de rouge).

## Logos et ressources externes

| Élément | Fichier | Source officielle |
|---|---|---|
| Stockfish | `presentation/logos/stockfish.png` (512 × 512, non modifié) | https://stockfishchess.org/images/logo/icon_512x512.png, site officiel ; le README du dépôt officiel https://github.com/official-stockfish/Stockfish pointe vers ce dossier |
| Qwen3 | `presentation/logos/qwen3.png` (non modifié) | https://qianwen-res.oss-accelerate-overseas.aliyuncs.com/logo_qwen3.png, affiché par le README du dépôt officiel https://github.com/QwenLM/Qwen3 |
| chess.com | `presentation/logos/chesscom2309.logowik.com.webp` (fourni par l'équipe ; marges blanches retirées à l'affichage, dessin non modifié) | Téléchargé sur logowik.com, un site de logos **tiers**, et non sur le site de chess.com (le site officiel bloque les téléchargements automatisés, et ses pages presse et marque renvoient 404). |
| ECE | `presentation/ece.png` (fourni), passé en blanc ou en sarcelle sur fond transparent | — |
| Drapeaux | intégrés | `flag-icons`, https://github.com/lipis/flag-icons (licence MIT) |
| Icônes, dont le logo GitHub | intégrées | Font Awesome 6 Free (licence CC BY 4.0), via `react-icons` |
| Pièces d'échecs | intégrées | rendu `chess.svg` de python-chess (pièces « cburnett ») |

## Classement des coups du coup du berger par Stockfish

Profondeur 18, règle de notre projet (`stockfish_features.py`) : chances de gain de −1 à +1 (définition de Lichess), perte = chances avec le meilleur coup − chances après le coup joué. Gaffe à partir de 0,3. « !! » si le coup est le meilleur et que la 2e meilleure option perd au moins 0,3 : seul coup qui gagne.

| Coup | Perte | Badge |
|---|---|---|
| 1. e4 | 0,007 | ! |
| 1… e5 | 0 | ! |
| 2. Fc4 | 0,052 | ! |
| 2… Cc6 | 0,007 | ! |
| 3. Dh5 | 0,075 | ! |
| 3… Cf6 | **1,05** (de +0,05 à −1, mat en 1) | **??** |
| 4. Dxf7# | 0 ; 2e meilleure option à −0,44 | **!!** |

## Partie d'exemple des trois méthodes (pages 17, 20 et 22)

Partie **g2599** du test : joueur des États-Unis, Elo 1 030, blancs, victoire par mat en 55 coups, 2 gaffes, ACPL 58,3. Choisie parce qu'elle illustre bien chaque méthode (exemple parlant, pas représentatif) :

| Méthode | Réponse | Source |
|---|---|---|
| Prompt (zero-shot) | 1 800 | `resultats_prompting_v1/predictions_zero_shot_test.csv` |
| RAG | 1 450 (10 voisins : 1 879, 1 334, 1 126, 641, 479, 2 072, 1 651, 1 000, 1 284, 1 372) | `resultats_rag/predictions_rag_test.csv`, `voisins.csv` |
| FT-A / FT-B | 1 077 / 1 017 | `resultats_finetuning_complets/predictions_ft_*_test.csv` |

Les trois parties d'entraînement montrées en page 22 sont les trois premières de `train.jsonl` (Elo 152, 561 et 2 337).

---

## Page par page

Le texte à dire est dans `texte_oral.md`.

| Page | Qui | Titre affiché | Contenu et visuel | Sources |
|---|---|---|---|---|
| 1 | — | Deviner l'Elo d'un joueur d'échecs en une partie, sans préjugé de nationalité | « Ethics_of_AI_ECE_DATA_IA », ING5 · ECE 2026-2027, sous-titre (la question), nos trois noms, lien cliquable vers le dépôt (logo GitHub + github.com/ChaseX9/Project-Ethics-of-IA), logo ECE blanc, sans photo | — |
| 2 | Thibault | Les échecs en 20 secondes | Échiquier initial (`f01_echiquier_depart.svg`) ; blancs contre noirs, 6 pièces, le but : échec et mat | — |
| 3 à 9 | Thibault | Une partie en 4 coups : le coup du berger | Un coup par page, flèche et badge de Stockfish (`f02_coup_du_berger_1` à `_7.svg`) | tableau ci-dessus |
| 10 | Thibault | Comment juger le niveau d'un joueur ? | Compter les gaffes ; mesurer les pertes par coup (1 pion = 100 centièmes) : l'ACPL ; logo Stockfish | — |
| 11 | Thibault | À votre avis, quel est l'Elo de ce joueur ? | Partie de Maël (`f03_partie_de_mael.svg`) ; noirs, 1. e4 e5 2. Dh5, mat en 67 coups, 8 gaffes, ACPL 117,5 ; « Elo = ? » | `data/prompts/demo.jsonl` (`demo_j2_p3`) |
| 12 | Thibault | Le problème : une IA risque de juger un joueur sur sa nationalité, et ce n'est pas normal | Les LLM apprennent sur des textes du web, avec des clichés sur les pays ; **exemple fictif** : même partie, France 1 500 ≠ États-Unis 1 400 ; « Même partie, même Elo prédit, quel que soit le pays » | — |
| 13 | Thibault | Notre cas d'usage : placer un joueur sans classement dans un tournoi, sur son seul jeu | 4 étapes (joueur → partie → IA, pays barré → poule) ; « Mal placé, un joueur affronte des adversaires bien trop forts, ou bien trop faibles » | `07_rendu_final.ipynb` section 1 |
| 14 | Thibault | Nous avons construit notre propre dataset : 4 200 vraies parties, 5 pays, 7 niveaux | Logo chess.com, 4 étapes de collecte, **4 200**, 856 joueurs · 12 mois, 5 drapeaux × 7 niveaux | `07_rendu_final.ipynb` section 2 |
| 15 | Thibault | Stockfish mesure la qualité du jeu ; c'est au LLM d'en déduire l'Elo | ACPL médian par tranche (`f04_acpl_par_tranche.svg`) ; **109 → 40** ; « 1 pion = 100 centièmes. Perdre 100 en un coup, c'est comme offrir un pion à l'adversaire. » | `data/prompts/*.jsonl` |
| 16 | Thibault | Trois façons d'apprendre l'Elo à notre LLM, puis on lui demande de se justifier | Logo Qwen3, « un nouvel employé… » ; 4 cartes : Prompt, RAG, Fine-tuning, XAI | — |
| 17 | Maël | Méthode 1 : on lui écrit des consignes et le résumé de la partie, il répond un Elo | Prompt de g2599 mis en forme (consigne, lignes de la partie, ligne du **pays** surlignée en rouge) ; Qwen répond **1 800**, vrai Elo 1 030 ; few-shot = 7 exemples ajoutés avant | `data/prompts/test.jsonl`, `03_prompting.ipynb` (consigne système) |
| 18 | Maël | Avec seulement des consignes, notre employé est à la fois ignorant et biaisé | **« 1800 »** près d'une réponse sur deux, erreur 644 ; 5 drapeaux : +101, +101, +51, +40, −40 (`f06_prompt_drapeaux.svg`) | `scores_global.csv`, `valeurs_frequentes.csv`, `biais_ecarts_sans_pays.csv` |
| 19 | Maël | Sept exemples mal choisis suffisent à créer un biais : le Brésil perd 243 points | Drapeau du Brésil, **−243 → −62**, « Le biais peut venir de nous » | `comparaison_premiere_execution.csv` |
| 20 | Maël | Méthode 2 : on lui donne aussi les dossiers des 10 parties les plus proches | Partie g2599 → loupe → 10 dossiers avec leur vrai Elo → Qwen répond **1 450** ; voisins choisis sur la qualité du jeu, jamais sur le pays | `resultats_rag/voisins.csv`, `04_rag.ipynb` |
| 21 | Maël | Avec des dossiers de cas similaires, il devient plus juste, mais pas plus utile | « Course » (`f08_course_rag.svg`) ; **573** ; moins de 20 points d'écart entre pays ; « Juste n'est pas utile » | `scores_global.csv`, `biais_ecarts_france.csv` |
| 22 | Maël | Méthode 3 : on l'entraîne vraiment, en lui montrant les parties et la bonne réponse | 3 332 parties avec leur Elo, lues 2 fois → petit module LoRA, le reste figé → **1 017** pour 1 030 ; FT-A : vrai pays ; FT-B : pays tiré au hasard | `config_ft_a.json` (2 époques, LoRA rang 8) |
| 23 | Maël | Une fois vraiment formé, il devient enfin compétent : aussi précis qu'un modèle classique | « Course » (`f09_course_finetuning.svg`) ; **380**, cible 369 | `scores_global.csv`, `comparaison_mae.csv` |
| 24 | Maël | L'effet du pays fond : de 150 à 16 points | 5 barres du rouge au vert (`f10_biais_fond.svg`) ; 78 % → 10 % des parties ; FT-B retenu | `biais_etendue_par_partie.csv` |
| 25 | Hugo | Notre modèle ne regarde plus le pays, mais le jeu | « On cache une information à la fois… (SHAP) » ; deux classements : modèle de base 1. Victoire ou défaite 36 %, **2. Pays 15,5 %**, 3. Fin de partie 13 %, 4. Ouverture 10 % ; FT-B 1. Ouverture 32 %, 2. ACPL 29 %, 3. Premiers coups 23 %, … **11. Pays 0,2 %** ; « SHAP mesure, LIME confirme » | `resultats_xai/importance_moyenne.csv`, `part_du_pays.csv` |
| 26 | Hugo | Et sur nous ? Nos modèles face à nos propres parties | Fans d'échecs : le vrai test, nos parties ; Thibault (959 Elo, 10 parties), Maël (492, 10), Hugo (877, 5), Paul Carrère (1 494, 10), Elo moyen réel lu dans `resultats_demo/`, « notre ami de classe l'an dernier, qui nous a initiés aux échecs » ; pas de photo | `data/prompts/demo.jsonl` |
| 27 | Hugo | Le modèle de base classe Paul dernier ; le nôtre, premier | Une carte par joueur avec sa photo et sa règle d'Elo (`f12_demo_*.svg`) : Thibault 959 / base 1 630 / nous 1 179 ; Maël 492 / 1 700 / 1 007 ; Hugo 877 / 1 680 / 837 ; Paul 1 494 / 1 570 / 1 737 ; partie du début 490 / 1 400 / 371 ; erreur par partie 694 → 423 | `resultats_demo/` (recalculé à chaque génération) |
| 28 | Hugo | Et si Paul se présentait comme américain ? 95 points de moins pour le modèle de base, rien pour le nôtre | « Paul vit aux États-Unis depuis cette année. Test : ses 10 parties, présentées deux fois. Seul le pays écrit change ; son jeu est identique. » ; règles France / États-Unis (`f13_paul_france_etats_unis.svg`) : base 1 570 → 1 475 (−95), nous 1 737 → 1 747 | `resultats_demo/france_etats_unis.csv` |
| 29 | Hugo | Conclusion | Séparateur | — |
| 30 | Hugo | Un biais se mesure et se réduit, mais un modèle juste n'est pas forcément un bon modèle | 3 leçons ; limites : 23 valeurs, FT-B pas significativement meilleur que FT-A, petits échantillons | `07_rendu_final.ipynb` sections 6, 9, 10 |

### Annexes (pages 31 à 41)

| Page | Contenu |
|---|---|
| 31 | Séparateur « Annexes » |
| 32 | Écarts à la France, 5 méthodes (`resultats_finetuning_complets/fig_biais_pays.png`) |
| 33 | Écarts au prompt sans pays (`fig_biais_sans_pays.png`) |
| 34 | Pourquoi SHAP est la mesure principale, et LIME le contrôle |
| 35, 36 | Partie g1852 : waterfall du modèle de base (−190 pour le pays), puis de FT-B (−10) |
| 37, 38 | Partie 3 de Paul, version « États-Unis » : modèle de base (−105), puis FT-B (0) |
| 39 | SHAP du gradient boosting : pays 0,9 %, ACPL 37 % |
| 40 | Démo complète avec FT-A, sur nos 10 dernières parties (`resultats_demo/fig_demo_elo_moyen.png`) |
| 41 | Benchmark complet : erreur, R², bonne tranche, écart entre pays, part SHAP du pays |

---

## Figures (`presentation/figures/`, SVG)

| Fichier | Page | Données |
|---|---|---|
| `f01_echiquier_depart.svg` | 2 | — |
| `f02_coup_du_berger_1.svg` à `_7.svg` | 3 à 9 | coups du berger, badges de Stockfish |
| `f03_partie_de_mael.svg` | 11 | `data/prompts/demo.jsonl`, `first_moves` de `demo_j2_p3` |
| `f04_acpl_par_tranche.svg` | 15 | `data/prompts/{train,val,test}.jsonl`, colonne `acpl` |
| `f06_prompt_drapeaux.svg` | 18 | `biais_ecarts_sans_pays.csv` (zero-shot) |
| `f08_course_rag.svg`, `f09_course_finetuning.svg` | 21, 23 | `scores_global.csv` |
| `f10_biais_fond.svg` | 24 | `biais_etendue_par_partie.csv` |
| `f12_demo_*.svg` (4 fichiers) | 27 | `resultats_demo/elo_moyen_par_joueur.csv` |
| `f13_paul_france_etats_unis.svg` | 28 | `resultats_demo/france_etats_unis.csv` |

Les autres visuels (problème, explication des méthodes, XAI, contexte de la démo) sont composés directement dans la page. L'ancienne figure empilée de l'XAI (`f11_xai_ce_qui_compte.svg`) est supprimée : elle était illisible pour un public extérieur.

---

## Plan B

| Problème | Solution |
|---|---|
| L'ordinateur de la salle ne lit pas le PDF | Avoir `soutenance.pdf` sur une clé USB et sur un deuxième ordinateur ; en dernier recours, projeter les images de `presentation/apercu/`. |
| Les notes manquent (le PDF n'en contient pas) | Imprimer `texte_oral.md`, ou l'ouvrir sur un téléphone. |
| Retard sur le minutage | Voir « Si le temps presse » dans `texte_oral.md` (gain d'environ 30 s). |
| Un présentateur absent | Les deux autres reprennent ses pages à partir de `texte_oral.md`. Si Maël est absent, la révélation de la page 27 devient « c'était la partie de Maël, qui n'a pas pu venir ». |
| La démo est relancée (nouvelles parties) | Remplacer `resultats_demo/`, puis régénérer le PDF : règles, erreur par partie, partie de l'accroche, nombre de parties et écart de Paul se recalculent. Revérifier à la main le titre de la page 27 et les chiffres du texte oral (pages 27 et 28). |
