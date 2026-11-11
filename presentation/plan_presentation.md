# Plan de la soutenance (environ 9 min 30)

**Fil rouge :** peut-on deviner le niveau d'un joueur d'échecs à partir d'une seule partie, et le faire équitablement, quelle que soit sa nationalité ?

**Image qui revient tout au long :** Qwen est un nouvel employé très cultivé qui n'a jamais estimé un Elo.
Prompt = on lui donne des consignes (et quelques exemples). RAG = on lui donne des dossiers de cas similaires. Fine-tuning = on le forme vraiment. XAI = on lui demande de justifier ses décisions.

**Fichiers :**
- `presentation/soutenance.pdf` : la présentation, projetée telle quelle (16:9, 35 pages). Il n'y a plus de PowerPoint : les notes du présentateur sont **dans ce fichier**, slide par slide.
- `presentation/figures/` : les visuels en SVG (échiquiers et graphiques, sans photo).
- `presentation/logos/` : logos officiels téléchargés (non versionnés, sources ci-dessous).
- `presentation/apercu/` : une image PNG par page du PDF, pour relire (non versionnée : elle contient nos photos).

## Minutage

| Présentateur | Slides | Pages du PDF | Durée |
|---|---|---|---|
| — | 0 (titre) | 1 | 0 s, affichée pendant l'installation |
| Thibault | 1.1 à 1.3, puis 1 à 5 | 2 à 15 | 3 min 45 |
| Maël | 6 à 10 | 16 à 20 | 2 min 55 |
| Hugo | 11 à 14 | 21 à 24 | 2 min 35 |
| **Total** | 24 pages | | **9 min 15** de parole, environ **9 min 30** avec les passages de relais |

Détail : 1.1 (20 s), 1.2 (35 s en tout, 7 pages, environ 5 s par coup), 1.3 (20 s), 1 (35 s), 2 (30 s), 3 (35 s), 4 (25 s), 5 (25 s) | 6 (40 s), 7 (35 s), 8 (30 s), 9 (35 s), 10 (35 s) | 11 (40 s), 12 (50 s), 13 (25 s), 14 (40 s).

Thibault parle plus longtemps que les autres (3 min 45 contre 2 min 35 à 2 min 55), à cause de la nouvelle intro. Pour rééquilibrer, Maël peut prendre la slide 5 (feuille de route) : 3 min 20 pour Thibault et 3 min 20 pour Maël.

Raccourcis déjà appliqués : corrélation −0,92 non dite (slide 4, elle n'est plus affichée), phrase sur la médiane des voisins retirée (slide 8), SHAP/LIME réduit à « SHAP mesure, LIME confirme » (slide 11).
Repère : environ 2,3 mots par seconde à l'oral, soit 100 mots pour 45 s.

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
| 8 | « Le pays pèse 15 % » | **15,5 %** (SHAP), 2e variable sur 12 ; 1,0 % (FT-A), 0,2 % (FT-B). | `resultats_xai/part_du_pays.csv` |
| 9 | Paul : « retire 100 Elo ; le nôtre, presque rien » | Sur ses 10 parties : le modèle de base retire **95 points en moyenne** (7 parties sur 10, jusqu'à −200). FT-B : **+10 en moyenne** (une seule partie bouge, de +100) : il ne le pénalise pas. | `resultats_demo/france_etats_unis.csv` |
| 10 | Comptes « bannis » exclus | Tous les **comptes fermés** sont exclus, dont les bannis pour triche. | `build_dataset.py` |
| 11 | Démo : « 10 parties, 5 pour Hugo » | Confirmé après la nouvelle exécution de 06c (Dataset Kaggle `ethics-of-ai-xai-10-parties`) : 10 parties pour Thibault, Maël et Paul, 5 pour Hugo ; 88 prédictions par modèle, toutes lues. Les 3 premières parties de chacun redonnent exactement les valeurs de 06_xai. | `resultats_demo/elo_moyen_par_joueur.csv` (`Parties` = 10, 10, 5, 10) |

---

## Direction artistique

- **Style keynote :** fond blanc, titres en phrases de 40 px, grands chiffres (60 à 190 px), cartes aux coins arrondis (28 px), beaucoup d'espace. Police Segoe UI Variable. Texte à 24 px minimum sur une page de 1 280 × 720 px, soit au moins 18 pt projeté.
- **Charte ECE :** sarcelle `#036F78` (extraite de `presentation/ece.png`) pour les titres, les chiffres et les slides de transition ; sarcelle foncée `#024C52` ; teinte claire `#E6F1F2` pour les cartes.
- **Slides de transition** (titre, feuille de route, bilan, annexes) : fond sarcelle avec un motif discret d'échiquier en fondu.
- **Une seule famille d'icônes :** Font Awesome 6 Free (pleines), via `react-icons`.
- **Couleurs des méthodes, constantes partout :** Zero-shot brique `#C8553D`, Few-shot ambre `#E9A23B`, RAG prune `#7A5C99`, FT-A bleu `#3A86C8`, FT-B sarcelle ECE `#036F78`. Chaque ligne porte aussi l'icône et le nom de sa méthode, pour rester lisible en noir et blanc.
- **Numéros de page :** dans un pion dessiné (sarcelle sur fond blanc, blanc sur fond sarcelle), le numéro dans la tête du pion.
- **Texte oral :** `presentation/texte_oral.md`, à lire et répéter, page par page, avec les [clic].
- **Badges de coups (dessin maison) :** « ! » bleu `#2F7FD8` (bon coup), « !! » sarcelle `#1BA39C` (seul coup gagnant), « ?? » rouge `#D7263D` (gaffe, case entourée de rouge). Pastille ronde dans le coin de la case d'arrivée, flèche du dernier coup.

## Logos et ressources externes

| Élément | Fichier | Source officielle |
|---|---|---|
| Stockfish | `presentation/logos/stockfish.png` (512 × 512, non modifié) | https://stockfishchess.org/images/logo/icon_512x512.png, site officiel ; le README du dépôt officiel https://github.com/official-stockfish/Stockfish pointe vers ce dossier (`icon_128x128.png`) |
| Qwen3 | `presentation/logos/qwen3.png` (non modifié) | https://qianwen-res.oss-accelerate-overseas.aliyuncs.com/logo_qwen3.png, affiché par le README du dépôt officiel https://github.com/QwenLM/Qwen3 |
| chess.com | **non récupéré** : emplacement « [logo chess.com] » sur la slide 3 | chess.com bloque les téléchargements automatisés, et ses pages presse et marque (`/press`, `/brand`) renvoient 404. Pour l'ajouter : déposer le fichier officiel sous `presentation/logos/chesscom.svg` (ou `.png`), puis régénérer le PDF. |
| ECE | `presentation/ece.png` (fourni), passé en blanc ou en sarcelle sur fond transparent | — |
| Drapeaux | intégrés dans les SVG | `flag-icons`, https://github.com/lipis/flag-icons (licence MIT) |
| Icônes | intégrées | Font Awesome 6 Free, https://fontawesome.com (licence CC BY 4.0), via `react-icons` |
| Pièces d'échecs | intégrées | rendu `chess.svg` de python-chess (pièces « cburnett ») |

## Classement des coups du coup du berger par Stockfish

Analyse à la profondeur 18 (Stockfish installé sur le PC), avec la règle de notre projet (`stockfish_features.py`) : chances de gain de −1 à +1 (définition de Lichess), perte = chances avant le coup avec le meilleur coup − chances après le coup joué. Gaffe à partir de 0,3. « !! » si le coup est le meilleur et que la 2e meilleure option perd au moins 0,3 : c'est le seul coup qui gagne.

| Coup | Perte | Badge |
|---|---|---|
| 1. e4 | 0,007 | ! |
| 1… e5 | 0 (meilleur que la ligne principale à cette profondeur) | ! |
| 2. Fc4 | 0,052 | ! |
| 2… Cc6 | 0,007 | ! |
| 3. Dh5 | 0,075 | ! |
| 3… Cf6 | **1,05** (de +0,05 à −1, mat en 1) | **??** |
| 4. Dxf7# | 0 ; 2e meilleure option à −0,44 | **!!** |

---

## Slide 0 — Titre (page 1, aucun temps de parole)

**Affiché :** « **Ethics_of_AI_ECE_DATA_IA** » puis « ING5 · ECE 2026-2027 » ; titre **« Deviner l'Elo d'un joueur d'échecs en une partie, sans préjugé de nationalité »** ; sous-titre « Peut-on estimer le niveau d'un joueur à partir d'une seule partie, et le faire équitablement, quel que soit son pays ? » ; **Thibault Rabbé · Maël Vaudin · Hugo Riviere** ; logo ECE blanc. Fond sarcelle à motif d'échiquier, sans photo.

---

## Slide 1.1 — Les échecs en 20 secondes (page 2, Thibault, 20 s)

**Titre :** « Les échecs en 20 secondes »

**Affiché :** échiquier en position initiale ; « Blancs contre noirs, chacun son tour, les blancs commencent » ; « 6 sortes de pièces : pion, cavalier, fou, tour, dame, roi » ; en carte : « **Le but : mettre le roi adverse échec et mat** ».

**Visuel :** `figures/f01_echiquier_depart.svg`.

**Notes :**
> « Bonjour à tous. Pour ceux qui ne jouent pas : les échecs, c'est les blancs contre les noirs, chacun son tour. Six sortes de pièces, et un seul but : mettre le roi adverse échec et mat, c'est-à-dire l'attaquer sans qu'il puisse s'échapper. »

---

## Slide 1.2 — Le coup du berger (pages 3 à 9, Thibault, 35 s en tout)

**Titre (le même sur les 7 pages) :** « Une partie en 4 coups : le coup du berger »

**Affiché sur chaque page :** l'échiquier après le coup, avec la flèche du coup et son badge ; à droite, la liste des coups (le coup courant en surbrillance, les suivants grisés), le badge en grand, le verdict de Stockfish et une phrase d'explication.

| Page | Coup | Badge | Phrase affichée | Figure |
|---|---|---|---|---|
| 3 | 1. e4 | ! bon coup | Les blancs avancent un pion au centre. | `f02_coup_du_berger_1.svg` |
| 4 | 1… e5 | ! bon coup | Les noirs répondent de la même façon. | `_2` |
| 5 | 2. Fc4 | ! bon coup | Le fou vise la case f7, le point faible des noirs. | `_3` |
| 6 | 2… Cc6 | ! bon coup | Les noirs sortent un cavalier. | `_4` |
| 7 | 3. Dh5 | ! bon coup | La dame vise f7 elle aussi : la menace est double. | `_5` |
| 8 | 3… Cf6 | ?? gaffe, case entourée de rouge | Les noirs attaquent la dame… et oublient de défendre f7. | `_6` |
| 9 | 4. Dxf7# | !! seul coup gagnant | La dame prend f7 : échec et mat en 4 coups. | `_7` |

**Notes (une phrase par page, en cliquant vite) :**
> « Voici la partie la plus courte qu'on voit chez les débutants. Les blancs avancent un pion… les noirs aussi. Le fou vise f7, le point faible… les noirs sortent un cavalier. La dame vise f7 à son tour. Et là, les noirs attaquent la dame, mais oublient f7 : c'est une gaffe, Stockfish la marque en rouge. La dame prend f7 : échec et mat, en quatre coups. »

---

## Slide 1.3 — Comment juger le niveau d'un joueur ? (page 10, Thibault, 20 s)

**Titre :** « Comment juger le niveau d'un joueur ? »

**Affiché :** deux cartes : « ?? **Compter ses gaffes** : les coups qui changent l'issue de la partie » et « **Mesurer ses pertes** : ce qu'il perd à chaque coup, en centièmes de pion : l'ACPL » ; en dessous, logo Stockfish et « C'est exactement ce que fait **Stockfish**, le moteur d'échecs ».

**Notes :**
> « Alors, comment juger le niveau d'un joueur ? On peut compter ses gaffes, comme celle qu'on vient de voir. Et mesurer ce qu'il perd à chaque coup, en centièmes de pion : c'est l'ACPL. C'est exactement ce que fait Stockfish. Maintenant, à vous de jouer. »

---

## Slide 1 — Accroche (page 11, Thibault, 35 s)

**Titre :** « À votre avis, quel est l'Elo de ce joueur ? »

**Affiché :** l'échiquier après les 10 premiers coups de `demo_j2_p3` (partie de **Maël**, vue des noirs, dernier coup fléché) ; à droite : noirs · ouverture 1. e4 e5 2. Dh5 · défaite par échec et mat, 67 coups · 8 gaffes, 2 erreurs · ACPL 117,5 ; en grand : **« Elo = ? »**.

**Visuel :** `figures/f03_partie_de_mael.svg`. Le PDF ne s'anime pas : la position est fixe.

**Notes :**
> « Voici une vraie partie rapide, jouée sur chess.com. Notre joueur a les noirs. Il perd par échec et mat en 67 coups, avec 8 gaffes, et il perd en moyenne 117 centièmes de pion par coup. À votre avis, quel est son Elo ? Levez la main : moins de 800 ? Entre 800 et 1 500 ? Plus de 1 500 ? … On vous donne la réponse à la fin. Deviner un niveau à partir d'une seule partie : c'est la question de notre projet. »

**Sources :** `data/prompts/demo.jsonl` (`demo_j2_p3`, non versionné). Réponse : `resultats_demo/predictions_demo.csv` (réel 490, base 1400, FT-B 371).

---

## Slide 2 — Le problème (page 12, Thibault, 30 s)

**Titre :** « Un joueur arrive sans classement : l'IA doit le placer, sans le juger sur sa nationalité »

**Affiché :** 4 étapes en icônes (joueur sans classement → 1 partie de placement → IA : Elo estimé, avec un drapeau barré → sa poule de niveau) ; carte « **Même partie, même Elo prédit, quel que soit le pays** ».

**Notes :**
> « Le cas d'usage : un club organise un tournoi en rapide, avec des poules de niveau. Un joueur arrive sans classement. Il joue une partie de placement, et une IA estime son Elo pour le placer. C'est une décision sur une personne : si l'IA le place plus bas parce qu'il est brésilien ou américain, c'est injuste. À partie identique, la prédiction doit être identique, quel que soit le pays. »

**Sources :** `07_rendu_final.ipynb`, section 1.

---

## Slide 3 — Nos données (page 13, Thibault, 35 s)

**Titre :** « Nous avons construit notre propre dataset : 4 200 vraies parties, 5 pays, 7 niveaux »

**Affiché :** logo chess.com (emplacement, voir « Logos ») et « API publique » ; 4 étapes en icônes : départ (10 joueurs par pays), boule de neige (on visite leurs adversaires), filtres (comptes fermés et tricheurs exclus), quotas (mêmes niveaux dans chaque pays) ; carte **4 200** vraies parties rapides, 856 joueurs · 12 mois ; les 5 drapeaux (France, Inde, États-Unis, Brésil, Allemagne) × 7 niveaux, de 100 à 1 900+.

**Notes :**
> « Aucun dataset ne répondait à notre question : on l'a construit nous-mêmes, avec l'API publique de chess.com. On est partis de quelques joueurs par pays, puis on a visité leurs adversaires, et ainsi de suite : c'est une collecte en boule de neige. On a exclu les comptes fermés, dont les tricheurs. Et on a imposé des quotas : chaque pays a la même répartition de niveaux. Dans nos données, le pays ne dit donc rien de l'Elo. Si un modèle s'en sert, c'est un biais du modèle. »

**Sources :** `07_rendu_final.ipynb` section 2, `build_dataset.py`.

---

## Slide 4 — Stockfish (page 14, Thibault, 25 s)

**Titre :** « Stockfish mesure la qualité du jeu ; c'est au LLM d'en déduire l'Elo »

**Affiché :** barres de l'ACPL médian par tranche (109, 90, 76, 63, 60, 56, 40 ; la première et la dernière en sarcelle) ; carte avec le logo Stockfish, **109 → 40**, « centièmes de pion perdus par coup, des débutants aux plus de 1 900 », « Il mesure les coups, pas l'Elo ».

**Visuel :** `figures/f04_acpl_par_tranche.svg`.

**Notes :**
> « Les gaffes, on les a déjà vues. Stockfish mesure aussi l'ACPL : les débutants perdent environ 109 centièmes de pion par coup, les joueurs au-dessus de 1 900, environ 40. Attention : Stockfish ne donne pas l'Elo. Passer de ces statistiques à un Elo, c'est le travail du LLM. »

**Sources :** ACPL médian recalculé depuis `data/prompts/{train,val,test}.jsonl`. Pour les questions : corrélation de −0,92 avec l'accuracy de chess.com (`07_rendu_final.ipynb` section 2).

---

## Slide 5 — Feuille de route (page 15, Thibault, 25 s)

**Titre :** « Trois façons d'apprendre l'Elo à notre LLM, puis on lui demande de se justifier »

**Affiché :** fond sarcelle à motif ; bandeau blanc avec le logo Qwen3 : « un nouvel employé très cultivé, qui n'a jamais estimé un Elo » ; 4 cartes blanches : 1. Prompt (des consignes et quelques exemples), 2. RAG (des dossiers de cas similaires), 3. Fine-tuning (une vraie formation), 4. XAI (on lui demande de se justifier).

**Notes :**
> « Notre LLM, c'est Qwen, un modèle léger de 4 milliards de paramètres. Imaginez un nouvel employé très cultivé, qui n'a jamais estimé un Elo. Trois façons de le rendre compétent : des consignes, des dossiers de cas similaires, ou une vraie formation. Toutes partent du même modèle de base. Enfin, on lui demandera de se justifier. Maël, à toi. »

---

## Slide 6 — Méthode 1, le prompt (page 16, Maël, 40 s)

**Titre :** « Avec seulement des consignes, notre employé est à la fois ignorant et biaisé »

**Affiché :** un énorme **« 1800 »**, « près d'une réponse sur deux », « erreur moyenne : 644 points, pire qu'une réponse constante (530) » ; à droite, les 5 drapeaux avec l'écart dû au seul pays écrit, par rapport au prompt sans pays : Allemagne **+101**, Inde **+101**, France **+51**, Brésil **+40**, États-Unis **−40** ; pastille « Qwen3 · Méthode 1 · Prompt ».

**Visuel :** `figures/f06_prompt_drapeaux.svg`.

**Notes :**
> « Première méthode : on donne juste des consignes au modèle, c'est le zero-shot. Résultat : il répond 1 800 près d'une fois sur deux, quel que soit le joueur. Son erreur moyenne est de 644 points : pire qu'un modèle qui répondrait toujours la même valeur. Et si on écrit que le joueur est allemand ou indien, à partie identique, il lui donne 100 points de plus que si on ne dit rien. Notre employé est ignorant, et il a des préjugés. »

**Sources :** `resultats_finetuning_complets/scores_global.csv` (643,9 ; 529,7), `valeurs_frequentes.csv` (44,9 %), `biais_ecarts_sans_pays.csv` (zero-shot : DE +100,7 ; IN +100,7 ; FR +51,4 ; BR +40,0 ; US −39,6).

---

## Slide 7 — Le piège du few-shot (page 17, Maël, 35 s)

**Titre :** « Sept exemples mal choisis suffisent à créer un biais : le Brésil perd 243 points »

**Affiché :** grand drapeau du Brésil ; **−243 → −62** en très gros ; « Brésil, par rapport à la France. Mêmes 7 exemples, même ordre : on a seulement retiré leur pays. » ; carte « **Le biais peut venir de nous** ».

**Notes :**
> « Pour l'aider, on a ajouté sept exemples de parties avec leur vrai Elo : c'est le few-shot. Dans notre première version, chaque exemple mentionnait aussi le pays. Par malchance, l'exemple brésilien avait un Elo bas. Le modèle en a tiré une règle : à partie identique, un Brésilien perdait 243 points ! Mêmes exemples, sans le pays : l'écart tombe à −62. Le biais ne venait pas seulement du modèle : il venait aussi de nos choix. »

**Sources :** `resultats_prompting_v2/comparaison_premiere_execution.csv` (Few-shot, Brésil : −242,9 → −61,9).

---

## Slide 8 — Méthode 2, le RAG (page 18, Maël, 30 s)

**Titre :** « Avec des dossiers de cas similaires, il devient plus juste, mais pas plus utile »

**Affiché :** « course » horizontale, une ligne par méthode avec son icône et sa valeur au bout de la barre : Zero-shot 644, Few-shot 507 (estompées), **RAG 573** (en évidence), FT-A et FT-B « à suivre… » ; ligne pointillée de la cible « gradient boosting, 369 » et ligne de la « réponse constante : 530 » ; carte **573**, « Écart entre pays : moins de 20 points », « **Juste n'est pas utile** ».

**Visuel :** `figures/f08_course_rag.svg`.

**Notes :**
> « Deuxième méthode, le RAG. Pour chaque partie, on va chercher les dix parties les plus proches, avec leur vrai Elo, et on les donne au modèle comme des dossiers. Bonne nouvelle : il devient plus équitable, l'écart moyen entre pays passe sous les 20 points. Mauvaise nouvelle : il se trompe encore de 573 points, plus que si on répondait toujours la même valeur. Équitable mais imprécis : ça ne sert à rien. »

**Sources :** `scores_global.csv` (573,2), `biais_ecarts_france.csv` (RAG : au plus +17,5). Pour les questions : la simple médiane des 10 voisins fait 453.

---

## Slide 9 — Méthode 3, le fine-tuning (page 19, Maël, 35 s)

**Titre :** « Une fois vraiment formé, il devient enfin compétent : aussi précis qu'un modèle classique »

**Affiché :** la même course, cette fois avec **FT-A 380** et **FT-B 382** en évidence, juste à côté de la cible de 369 ; carte **380**, « contre 644 au départ », « ≈ la cible : 369 », « FT-A : vrai pays · FT-B : pays tiré au hasard ».

**Visuel :** `figures/f09_course_finetuning.svg`.

**Notes :**
> « Troisième méthode : on forme vraiment le modèle. On entraîne un petit adaptateur sur nos 3 300 parties d'entraînement, chacune avec son vrai Elo. Deux versions : FT-A voit le vrai pays, FT-B voit un pays tiré au hasard, pour casser le lien entre pays et Elo. Les deux se trompent d'environ 380 points : 260 de moins qu'au départ, et le niveau d'un modèle classique, le gradient boosting, à 369. Notre employé est enfin compétent. »

**Sources :** `scores_global.csv` (379,6 ; 382,3 ; 369,4), `comparaison_mae.csv` (FT-B − gradient boosting = +13, non significatif).

---

## Slide 10 — LA slide du biais (page 20, Maël, 35 s)

**Titre :** « L'effet du pays fond : de 150 à 16 points »

**Affiché :** 5 barres qui rétrécissent, du rouge au vert, valeurs en très gros : Zero-shot **150**, Few-shot **120**, RAG **58**, FT-A **37**, FT-B **16**, chacune avec l'icône de sa méthode ; carte **150 → 16**, « le pays change la prédiction : 78 % → 10 % des parties », « FT-B : notre modèle retenu ».

**Visuel :** `figures/f10_biais_fond.svg`.

**Notes :**
> « Voici la slide qui résume le projet. On présente une même partie cinq fois au modèle, en changeant seulement le pays, et on mesure l'écart entre sa plus haute et sa plus basse estimation. Avec les consignes : 150 points. Avec les exemples : 120. Avec les dossiers : 58. Après formation : 37, et 16 pour FT-B, notre modèle retenu. Au départ, le pays changeait la prédiction pour 78 % des parties ; avec FT-B, pour 10 %. Le biais fond. »

**Sources :** `resultats_finetuning_complets/biais_etendue_par_partie.csv`.

---

## Slide 11 — XAI (page 21, Hugo, 40 s)

**Titre :** « Le modèle formé ne regarde plus le pays, mais la qualité du jeu »

**Affiché :** deux barres empilées à 100 % : « Ce qui compte dans la décision ».
- **Modèle de base :** Pays **15,5 %** (en rouge, encadré), Résultat 36 %, Fin de partie 13 %, Ouverture 10 %, autres 26 %.
- **FT-B :** Pays **0,2 %** (repère rouge), Ouverture 32 %, ACPL 29 %, Premiers coups 23 %, Fin de partie 9 %, autres 7 %.

Légende en icônes (une par variable), puis **15,5 % → 0,2 %** (part du pays dans la décision) et la pastille « SHAP mesure, LIME confirme ».

**Visuel :** `figures/f11_xai_ce_qui_compte.svg`.

**Notes :**
> « Dernière étape : on demande au modèle de justifier ses décisions. On masque une ligne du prompt, par exemple le pays, et on regarde de combien la prédiction bouge. Avant la formation, le modèle juge surtout le résultat, victoire ou défaite, et en deuxième, le pays : 15 % de sa décision. Après, le pays tombe à 0,2 %, et le modèle regarde l'ouverture, l'ACPL et les premiers coups : la vraie qualité du jeu. SHAP mesure, LIME confirme. »

**Sources :** `resultats_xai/part_du_pays.csv`, `resultats_xai/importance_moyenne.csv` (parts SHAP recalculées). Justification détaillée : annexe « Pourquoi SHAP ».

---

## Slide 12 — Démo (page 22, Hugo, 50 s)

**Titre :** « Le modèle de base classe Paul dernier ; le nôtre, premier »

**Affiché :** sous-titre « Elo moyen sur nos 10 dernières parties rapides (5 pour Hugo) · règle de 100 à 2 000 » ; une carte par joueur, avec sa photo et une règle d'Elo à trois marqueurs (trait noir : vrai Elo ; rond brique : modèle de base ; losange sarcelle : nous, FT-B) :

| Joueur | Parties | Réel | Base | Nous |
|---|---|---|---|---|
| Thibault | 10 | 959 | 1 630 | 1 179 |
| Maël | 10 | 492 | 1 700 | 1 007 |
| Hugo | 5 | 877 | 1 680 | 837 |
| Paul | 10 | 1 494 | 1 570 | 1 737 |

En bas : « La partie du début : Maël, 490 · Base 1 400 · Nous 371 » et « Erreur par partie : 694 → 423 » (35 parties). Ces textes sont recalculés à partir de `resultats_demo/` à chaque génération du PDF.

**Visuel :** `figures/f12_demo_{thibault,mael,hugo,paul}.svg` (sans photo) ; photos `presentation/*.jpg|png`, sur cette slide uniquement (non versionnées).

**Notes :**
> « Testons-le sur nous. On a pris nos dix dernières parties rapides, cinq pour moi, et celles de Paul. Le modèle de base donne à peu près le même Elo à tout le monde, entre 1 570 et 1 700, et il classe Paul, le plus fort, en dernier. Notre modèle le classe premier. Il n'est pas parfait : Maël est surestimé de 500 points. Mais l'erreur par partie passe de 694 à 423. Et la partie du début ? C'était celle de Maël, à 490. Le modèle de base disait 1 400 ; le nôtre, 371. »

**Sources :** `resultats_demo/elo_moyen_par_joueur.csv`, `predictions_demo.csv` (06c ; Joueur 1 = Thibault, 2 = Maël, 3 = Hugo, 4 = Paul). Erreur par partie : moyenne de |prédit − réel| sur les 35 parties en version d'origine (693,6 et 422,8). Maël : FT-B 1 006,8 contre 492,3, soit +514,5.

---

## Slide 13 — Dédicace à Paul (page 23, Hugo, 25 s)

**Titre :** « Pour Paul, parti aux États-Unis : le modèle de base lui retire 95 points en moyenne, le nôtre ne le pénalise pas »

**Affiché :** deux règles parallèles, avec les drapeaux France et États-Unis : modèle de base 1 570 puis 1 475, avec une flèche courbe et **−95** en grand ; notre modèle 1 737 puis 1 747 ; trait gris pour son vrai Elo (1 494). Moyennes sur ses 10 parties. Pas de photo sur cette slide.

**Visuel :** `figures/f13_paul_france_etats_unis.svg`.

**Notes :**
> « Cette slide est pour Paul, notre ami parti vivre aux États-Unis cette année. On a présenté ses dix parties deux fois : comme français, puis comme américain. Le modèle de base lui retire près de 100 points en moyenne, juste à cause du mot « États-Unis », et jusqu'à 200 sur certaines parties. Notre modèle, lui, ne le pénalise pas. Paul, tu peux jouer tranquille. »

**Sources :** `resultats_demo/france_etats_unis.csv` (base : −95 en moyenne, 7 parties sur 10 pénalisées, de −100 à −200 ; FT-B : +10 en moyenne, une seule partie change, de +100 ; FT-A : −20 en moyenne, une seule partie, de −200).

---

## Slide 14 — Ce qu'on retient (page 24, Hugo, 40 s)

**Titre :** « Un biais se mesure et se réduit, mais un modèle juste n'est pas forcément un bon modèle »

**Affiché :** fond sarcelle à motif ; 3 leçons en icônes : le dataset équilibré et le fine-tuning ont le plus réduit le biais ; le biais peut venir de nous : 7 exemples ont suffi ; un modèle équitable n'est pas forcément utile. Carte « Nos limites » : réponses concentrées sur 23 valeurs (1677, 1777, 101…) ; FT-B ne fait pas significativement mieux que FT-A ; petits échantillons (140 parties pour le biais, 12 pour l'XAI).

**Notes :**
> « Ce qu'on retient. Un : ce qui a le plus réduit le biais, c'est notre dataset équilibré, puis la formation du modèle. Deux : le biais peut venir de nous. Trois : un modèle juste n'est pas forcément utile. Nos limites : le modèle répond souvent les mêmes nombres, FT-B ne fait pas significativement mieux que FT-A, et nos échantillons restent petits. Donc oui, on peut estimer un niveau à partir d'une partie, sans tenir compte de la nationalité, mais comme un premier avis. Merci, on attend vos questions. »

---

## Annexes (pages 25 à 35)

| Page | Contenu |
|---|---|
| 25 | Séparateur « Annexes » |
| 26 | Écarts à la France, 5 méthodes (`resultats_finetuning_complets/fig_biais_pays.png`) |
| 27 | Écarts au prompt sans pays (`fig_biais_sans_pays.png`) |
| 28 | Pourquoi SHAP est la mesure principale, et LIME le contrôle (4 cartes ; LIME : 8,8 / 7,0 / 5,8 %) |
| 29, 30 | Partie g1852 (États-Unis, 707 Elo) : waterfall du modèle de base (−190 pour le pays), puis de FT-B (−10) |
| 31, 32 | Partie 3 de Paul, version « États-Unis » : modèle de base (−105), puis FT-B (0) |
| 33 | SHAP du gradient boosting : pays 0,9 %, ACPL 37 % (`resultats_xai_baseline/fig_importance_globale.png`) |
| 34 | Démo complète avec FT-A, sur nos 10 dernières parties (`resultats_demo/fig_demo_elo_moyen.png`) |
| 35 | Benchmark complet : erreur, R², bonne tranche, écart entre pays, part SHAP du pays |

Les graphiques des notebooks ne figurent qu'ici ; tous les visuels des slides 1.1 à 14 sont faits pour la projection.

---

## Figures (`presentation/figures/`, SVG)

| Fichier | Slide | Données |
|---|---|---|
| `f01_echiquier_depart.svg` | 1.1 | — |
| `f02_coup_du_berger_1.svg` à `_7.svg` | 1.2 | coups du berger, badges de Stockfish (tableau ci-dessus) |
| `f03_partie_de_mael.svg` | 1 | `data/prompts/demo.jsonl`, `first_moves` de `demo_j2_p3` |
| `f04_acpl_par_tranche.svg` | 4 | `data/prompts/{train,val,test}.jsonl`, colonne `acpl` |
| `f06_prompt_drapeaux.svg` | 6 | `biais_ecarts_sans_pays.csv` (zero-shot) |
| `f08_course_rag.svg`, `f09_course_finetuning.svg` | 8, 9 | `scores_global.csv` |
| `f10_biais_fond.svg` | 10 | `biais_etendue_par_partie.csv` |
| `f11_xai_ce_qui_compte.svg` | 11 | `resultats_xai/importance_moyenne.csv` (SHAP) |
| `f12_demo_*.svg` (4 fichiers) | 12 | `resultats_demo/elo_moyen_par_joueur.csv` |
| `f13_paul_france_etats_unis.svg` | 13 | `resultats_demo/france_etats_unis.csv` |

---

## 5 questions probables du jury

**1. Le gradient boosting fait aussi bien (369 contre 382). Pourquoi un LLM ?**
C'est vrai, et nous le disons : pour un vrai tournoi, le gradient boosting serait un choix défendable, moins cher et explicable, avec un pays qui ne pèse que 0,9 %. Le sujet demandait d'adapter un LLM ; notre intérêt a été de montrer qu'un LLM part avec des préjugés, et qu'on peut les mesurer et les réduire. *(Pages 33 et 35.)*

**2. Comment savez-vous que l'écart vient du pays, et pas des parties elles-mêmes ?**
Par le test contrefactuel : la même partie, présentée 5 fois, seule la ligne du pays change. Et les quotas rendent le pays inutile pour prédire l'Elo. Tout écart vient donc du modèle. On ne sait pas dire, en revanche, si c'est un stéréotype sur le pays ou un effet du mot lui-même. *(Pages 26 et 27.)*

**3. Si FT-B n'est pas meilleur que FT-A de façon prouvée, pourquoi le retenir ?**
À précision égale (382 contre 380), FT-B va dans le bon sens sur tous les indicateurs de biais : étendue 16 contre 37, part SHAP du pays 0,2 % contre 1,0 %. Il ne coûte rien de plus. Sur des données déséquilibrées, c'est là qu'il pourrait vraiment servir. *(Page 35.)*

**4. 380 points d'erreur et 29 % de bonnes tranches : c'est utilisable ?**
Pas seul. Une seule partie, c'est très peu d'information : même le meilleur modèle classique se trompe de 369 points. C'est un premier avis pour placer un joueur, à corriger avec ses résultats suivants. *(Hasard : environ 14 % de bonnes tranches.)*

**5. Et la vie privée des joueurs ?**
Les prompts ne contiennent ni pseudo, ni lien, ni Elo de l'adversaire, et un script le vérifie. Les fichiers avec les pseudos ne sont pas publiés. Mais les parties de chess.com sont publiques : avec l'ouverture et les 10 premiers coups, on pourrait en principe retrouver une partie. Pour la démo, on a utilisé nos propres parties.

À garder en réserve : « Pourquoi SHAP plutôt que LIME ? » (page 28) ; « Comment Stockfish classe-t-il les coups ? » (tableau du coup du berger ci-dessus) ; « L'ACPL est-il fiable ? » (corrélation de −0,92 avec l'accuracy de chess.com).

---

## Plan B

| Problème | Solution |
|---|---|
| L'ordinateur de la salle ne lit pas le PDF | Avoir `soutenance.pdf` sur une clé USB et sur un deuxième ordinateur ; en dernier recours, projeter les images de `presentation/apercu/`. |
| Les notes manquent (le PDF n'en contient pas) | Imprimer ce plan, ou l'ouvrir sur un téléphone. |
| Retard sur le minutage | Pages 3 à 9 : cliquer sans commenter les coups 1 à 4, ne parler qu'à la gaffe (page 8) et au mat (page 9) : gain d'environ 15 s. Slide 10 : ne pas citer 78 % → 10 %. Slide 12 : couper la phrase sur Maël surestimé. |
| Un présentateur absent | Les deux autres reprennent ses slides à partir des notes. Si Maël est absent, la révélation de la slide 12 devient « c'était la partie de Maël, qui n'a pas pu venir ». |
| La démo est relancée (nouvelles parties) | Remplacer `resultats_demo/`, puis régénérer le PDF : les règles, l'erreur par partie, la partie de l'accroche, le nombre de parties et l'écart de Paul se recalculent. Revérifier à la main le titre de la slide 12 (Paul toujours dernier, puis premier ?) et les chiffres du texte oral (pages 22 et 23). |
| Le logo chess.com est fourni | Le déposer sous `presentation/logos/chesscom.svg` ou `.png`, puis régénérer le PDF. |
