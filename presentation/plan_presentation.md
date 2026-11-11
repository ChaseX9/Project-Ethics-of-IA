# Plan de la soutenance (9 minutes)

**Fil rouge :** peut-on deviner le niveau d'un joueur d'échecs à partir d'une seule partie, et le faire équitablement, quelle que soit sa nationalité ?

**Image qui revient tout au long :** Qwen est un nouvel employé très cultivé qui n'a jamais estimé un Elo.
Prompt = on lui donne des consignes (et quelques exemples). RAG = on lui donne des dossiers de cas similaires. Fine-tuning = on le forme vraiment. XAI = on lui demande de justifier ses décisions.

**Règles de forme :** une idée par slide, un titre qui est une phrase, un chiffre fort par slide, peu de texte. Les chiffres sont arrondis à l'oral ; la version exacte est dans la ligne « Sources ».

**Fichiers :** `presentation/soutenance.pptx` (notes du présentateur dans les notes PowerPoint), `presentation/soutenance.pdf` (plan B), figures dans `presentation/figures/`. Dans le PowerPoint, la slide de titre porte le numéro 1 : la slide *n* de ce plan est la slide *n* + 1 du fichier.

## Minutage

| Présentateur | Slides | Durée |
|---|---|---|
| — | 0 (titre) | 0 s, affichée pendant l'installation |
| Thibault | 1 à 5 | 3 min 00 |
| Maël | 6 à 10 | 2 min 55 |
| Hugo | 11 à 14 | 2 min 45 |
| **Total** | 15 slides | **8 min 40** de parole, environ **9 min** avec les passages de relais |

Détail : 1 (45 s), 2 (30 s), 3 (40 s), 4 (35 s), 5 (30 s) | 6 (40 s), 7 (35 s), 8 (30 s), 9 (35 s), 10 (35 s) | 11 (40 s), 12 (55 s), 13 (25 s), 14 (45 s).
Les raccourcis du plan B sont appliqués d'office : corrélation −0,92 non dite à la slide 4, phrase sur la médiane des voisins retirée de la slide 8, SHAP/LIME réduit à « SHAP mesure, LIME confirme » à la slide 11.
Repère : environ 2,3 mots par seconde à l'oral, soit 100 mots pour 45 s.

---

## Corrections apportées aux chiffres du brief

Tous les chiffres ont été recalculés à partir des CSV du dépôt. Ceux-ci étaient faux ou demandaient une précision :

| # | Dans le brief | Valeur vérifiée | Source |
|---|---|---|---|
| 1 | Few-shot : « **3** exemples mal choisis » | **7 exemples** (un par tranche d'Elo). Brésil : −243 avec le pays dans les exemples, **−62** sans. L'écart « tombe », mais ne disparaît pas : −62 reste significatif. | `resultats_prompting_v2/comparaison_premiere_execution.csv`, `resultats_finetuning_complets/biais_ecarts_france.csv` |
| 2 | Dataset « équilibré » | Équilibré **en proportions**, pas en effectifs : par tranche, 240 parties françaises et 90 pour chacun des 4 autres pays. La France pèse 40 % du dataset (1 680 sur 4 200). Ce qui est égal, c'est la répartition des tranches d'Elo dans chaque pays : le pays ne dit rien de l'Elo. | `data/prompts/*.jsonl` (recalculé), `07_rendu_final.ipynb` section 2 |
| 3 | ACPL « ~109 » chez les débutants, « ~40 » au-dessus de 1900 | Ce sont des **médianes** : 109,5 (100-400) et 39,5 (1900+). Les moyennes sont de 122 et 44. Ces chiffres ne sont affichés dans aucun notebook : recalculés depuis `acpl` dans `data/prompts/*.jsonl`. | `data/prompts/train.jsonl`, `val.jsonl`, `test.jsonl` |
| 4 | Zero-shot : « 1800 une fois sur deux » | **44,9 %** des réponses : dire « près d'une fois sur deux ». Le modèle n'utilise que 8 valeurs. | `resultats_finetuning_complets/valeurs_frequentes.csv` |
| 5 | « Prédictions concentrées sur ~20 valeurs comme "101" » | **23 valeurs** pour FT-A et pour FT-B. Les plus fréquentes sont **1677** (24,5 % pour FT-A) et **1777** (25,6 % pour FT-B). 101 : 4,1 % (FT-A), 9,6 % (FT-B). Dire « 23 valeurs, comme 1677, 1777 ou 101 ». | `resultats_finetuning_complets/valeurs_frequentes.csv` |
| 6 | RAG : « écarts entre pays < 20 points » | Juste pour l'**écart moyen à la France** (au plus +17,5). Nuances : partie par partie, le pays change encore 36 % des prédictions (étendue moyenne 58) ; écrire n'importe quel pays fait baisser la prédiction de 26 à 52 points par rapport au prompt sans pays. Dire « en moyenne, moins de 20 points d'écart entre pays ». | `resultats_finetuning_complets/biais_ecarts_france.csv`, `biais_etendue_par_partie.csv`, `biais_ecarts_sans_pays.csv` |
| 7 | « Effet du pays » 150 → 120 → 58 → 37 → 16 | Chiffres justes. C'est l'**étendue moyenne** : la même partie est présentée avec les 5 pays, on prend la plus haute prédiction moins la plus basse, puis la moyenne sur 140 parties. Le « 120 » est le few-shot **v2** (exemples sans pays). | `resultats_finetuning_complets/biais_etendue_par_partie.csv` |
| 8 | XAI : « le pays pèse **15 %** » | **15,5 %** (SHAP), 2e variable sur 12. Après : 1,0 % (FT-A) et 0,2 % (FT-B). | `resultats_xai/part_du_pays.csv` |
| 9 | Paul : « le nôtre, presque rien » | Sur ses 3 parties : le modèle de base retire **100 points à chacune** ; FT-B donne **+100, 0, 0** (FT-A : 0, −200, 0). Formulation retenue : « Le modèle de base lui retire 100 points à chaque partie ; le nôtre ne le pénalise pas. » | `resultats_demo/france_etats_unis.csv` (06c) |
| 10 | Comptes « bannis » exclus | Plus large : tous les **comptes fermés** sont exclus, dont ceux bannis pour triche. | `build_dataset.py`, `07_rendu_final.ipynb` section 2 |
| 11 | Démo : « 10 parties, 5 pour Hugo » | `resultats_demo/` a été produit à partir de l'**ancien** `demo.jsonl` : **3 parties par joueur** (Hugo compris), mêmes valeurs que `resultats_xai/predictions_demo.csv`. Les slides 12 et 13 disent donc « 3 dernières parties ». Pour passer à 10 parties, relancer 06c après avoir mis à jour le Dataset Kaggle avec le nouveau `demo.jsonl`. | `resultats_demo/elo_moyen_par_joueur.csv` (colonne `Parties` = 3) |

Les chiffres confirmés tels quels : 4 200 parties, 5 pays, 7 tranches ; corrélation −0,92 (Spearman, sur 1 198 parties avec accuracy) ; MAE zero-shot 644 contre 530 pour la constante ; +101 pour « Allemagne » et « Inde » par rapport au prompt sans pays ; RAG 573 contre 453 pour la médiane des voisins ; FT-A 380, FT-B 382, gradient boosting 369 ; Paul −100 avec le modèle de base.

---

## Charte graphique

- **Cadre (couleurs ECE) :** sarcelle `#036F78` extraite du logo (`presentation/ece.png`) pour les titres, les chiffres forts, la slide de titre et la slide de bilan ; sarcelle foncée `#024C52` ; teinte claire `#E6F1F2` pour les encadrés. Police Calibri, titres en 30 pt gras, texte à 18 pt minimum.
- **Motif répété :** un encadré teinté à droite, avec le chiffre fort en grand (48 à 72 pt).
- **Les 5 modèles, constants dans toutes les figures**, avec une couleur, un motif et un marqueur, pour rester distincts en noir et blanc :

| Modèle | Couleur | Motif des barres | Marqueur |
|---|---|---|---|
| Zero-shot | brique `#C8553D` | hachures `//` | rond |
| Few-shot | ambre `#E9A23B` | hachures `\\` | carré |
| RAG | prune `#7A5C99` | croisillons | triangle |
| FT-A | bleu `#3A86C8` | points | losange |
| FT-B (retenu) | sarcelle ECE `#036F78` | plein | étoile |

Les modèles de référence sont en gris (constante clair, médiane des voisins moyen, gradient boosting foncé).

---

## Slide 0 — Titre (aucun temps de parole)

**Titre :** « Deviner l'Elo d'un joueur d'échecs en une partie, sans préjugé de nationalité »

**Contenu affiché :** sous-titre « Peut-on estimer le niveau d'un joueur à partir d'une seule partie, et le faire équitablement, quel que soit son pays ? » ; photos rondes et noms : **Thibault Rabbé · Maël Vaudin · Hugo Riviere** ; logo ECE en blanc ; « Ethics of AI · ING5 · ECE 2026-2027 ». Fond sarcelle.

**Visuel :** `presentation/thibault.jpg`, `Mael.png`, `hugo.jpg` (non versionnées), logo `presentation/ece.png` passé en blanc.

**Notes :** slide affichée pendant l'installation ; Thibault enchaîne sur la slide 1.

---

## Slide 1 — Accroche (Thibault, 45 s)

**Titre :** « Une partie, 67 coups, 8 gaffes : à votre avis, quel est l'Elo de ce joueur ? »

**Contenu affiché :** échiquier animé à gauche ; à droite : le joueur a les **noirs** · ouverture **1. e4 e5 2. Dh5** · défaite par **échec et mat, en 67 coups** · **8 gaffes · 2 erreurs · 3 imprécisions** · ACPL **117,5** ; en grand : **« Elo = ? »**.

**Visuel :** F1, `presentation/figures/f1_echiquier.gif` : les 10 premiers coups de `demo_j2_p3` (partie de **Maël**, Elo réel 490), vue des noirs, 0,7 s par demi-coup, dernier coup surligné. La première image du GIF est la position finale : c'est elle qui apparaît dans le PDF.

**Notes du présentateur :**
> « Bonjour à tous. On commence par un petit jeu. Voici une vraie partie d'échecs en cadence rapide, jouée sur chess.com. Notre joueur a les noirs. Les dames s'échangent dès le huitième coup. La partie dure 67 coups, il fait 8 gaffes et finit mat. À votre avis, quel est son Elo ? Levez la main : moins de 800 ? Entre 800 et 1 500 ? Plus de 1 500 ? … On vous donne la réponse à la fin. Deviner un niveau à partir d'une seule partie : c'est exactement la question de notre projet. »

**Sources :** `data/prompts/demo.jsonl`, partie `demo_j2_p3` (non versionné). Réponse : `resultats_demo/predictions_demo.csv` (réel 490, modèle de base 1400, FT-B 371).

---

## Slide 2 — Le problème (Thibault, 30 s)

**Titre :** « Un joueur sans classement arrive au tournoi : l'IA doit le placer, sans le juger sur sa nationalité »

**Contenu affiché :** le schéma ; en dessous, dans un bandeau teinté : **« Même partie, même Elo prédit, quel que soit le pays »**.

**Visuel :** F2, `presentation/figures/f2_cas_usage.png`.

**Notes du présentateur :**
> « Le cas d'usage : un club organise un tournoi en rapide, avec des poules de niveau. Un joueur arrive sans classement. Il joue une partie de placement, et une IA estime son Elo pour le placer. C'est une décision sur une personne. Si l'IA place un joueur plus bas parce qu'il est brésilien ou américain, c'est injuste. On veut donc qu'à partie identique, la prédiction soit identique, quel que soit le pays. »

**Sources :** `07_rendu_final.ipynb`, section 1.

---

## Slide 3 — Nos données (Thibault, 40 s)

**Titre :** « Nous avons construit notre propre dataset : 4 200 vraies parties, 5 pays, 7 niveaux »

**Contenu affiché :** chiffre fort **4 200** vraies parties rapides de chess.com ; 856 joueurs · 12 mois ; 5 pays × 7 niveaux ; « Dans nos données, le pays ne dit rien de l'Elo ».

**Visuel :** F3, `presentation/figures/f3_collecte.png`.

**Notes du présentateur :**
> « Aucun dataset ne répondait à notre question : on l'a construit nous-mêmes, avec l'API publique de chess.com. L'API ne liste que 10 000 joueurs par pays. On est donc partis de quelques joueurs, puis on a visité leurs adversaires, puis les adversaires de ces adversaires : c'est une collecte en boule de neige. On a exclu les comptes fermés, dont les tricheurs bannis. Et on a imposé des quotas : chaque pays a la même répartition de niveaux. Résultat : dans nos données, le pays ne dit rien de l'Elo. Si un modèle s'en sert, c'est un biais du modèle. »

**Sources :** `07_rendu_final.ipynb` section 2 (4 200 parties, 856 joueurs, 93 %, quotas 240 / 90 par tranche), `build_dataset.py`.

---

## Slide 4 — Stockfish (Thibault, 35 s)

**Titre :** « Stockfish mesure la qualité du jeu, mais c'est au LLM d'en déduire l'Elo »

**Contenu affiché :** chiffre fort **109 → 40** (centipions perdus par coup, ACPL médian, des débutants aux plus de 1900) ; « Stockfish mesure les coups, pas l'Elo » ; en petit : « Validation : corrélation de −0,92 avec la précision de chess.com » (affiché, non dit).

**Visuel :** F4, `presentation/figures/f4_acpl_par_tranche.png`.

**Notes du présentateur :**
> « Pour décrire la partie, on utilise Stockfish, le moteur d'échecs. Attention : il ne donne pas l'Elo. Il mesure seulement la qualité de chaque coup : les gaffes, les erreurs, et l'ACPL, les centipions perdus en moyenne à chaque coup. Plus on est fort, moins on en perd : environ 109 chez les débutants, 40 au-dessus de 1 900. Passer de ces statistiques à un Elo, c'est le travail du LLM. »

**Sources :** ACPL médian par tranche recalculé depuis `data/prompts/{train,val,test}.jsonl` (109,45 / 90,3 / 76,05 / 63,4 / 59,8 / 56,2 / 39,5). Corrélation −0,92 (Spearman, 1 198 parties) : `07_rendu_final.ipynb` section 2.

---

## Slide 5 — Feuille de route (Thibault, 30 s)

**Titre :** « Trois façons d'apprendre l'Elo à un LLM, puis on lui demande de se justifier »

**Contenu affiché :** l'employé Qwen (« très cultivé, n'a jamais estimé un Elo ») et 4 cartes : 1 Prompt (des consignes et quelques exemples), 2 RAG (des dossiers de cas similaires), 3 Fine-tuning (une vraie formation), 4 XAI (on lui demande de se justifier). Chaque carte reprend la couleur de sa méthode.

**Visuel :** F5, `presentation/figures/f5_employe_methodes.png`.

**Notes du présentateur :**
> « Ce LLM, c'est Qwen, un modèle léger de 4 milliards de paramètres. Imaginez un nouvel employé très cultivé, qui n'a jamais estimé un Elo. On a essayé trois façons de le rendre compétent : lui donner des consignes, lui donner des dossiers de cas similaires, ou le former vraiment. Les trois partent du même modèle de base. Enfin, on lui demandera de justifier ses décisions. Maël, à toi. »

**Sources :** `07_rendu_final.ipynb`, section 5.

---

## Slide 6 — Méthode 1, le prompt (Maël, 40 s)

**Titre :** « Avec seulement des consignes, notre employé est à la fois ignorant et biaisé »

**Contenu affiché :** chiffre fort **644** points d'erreur moyenne, pire qu'une réponse constante (530) ; **« 1800 »** près d'une réponse sur deux ; « Allemand » ou « indien » : **+100 points**.

**Visuel :** F6, `presentation/figures/f6_zero_shot_pays.png`.

**Notes du présentateur :**
> « Première méthode : on donne juste des consignes au modèle, c'est le zero-shot. Résultat : il répond 1 800 près d'une fois sur deux, quel que soit le joueur. Son erreur moyenne est de 644 points : pire qu'un modèle qui répondrait toujours l'Elo médian. Et si on écrit que le joueur est allemand ou indien, à partie identique, il lui donne 100 points de plus que si on ne dit rien. Notre employé est ignorant, et il a des préjugés. »

**Sources :** `resultats_finetuning_complets/scores_global.csv` (643,9 ; 529,7), `valeurs_frequentes.csv` (1800 : 44,9 %), `biais_ecarts_sans_pays.csv` (DE et IN : +100,7 ; FR +51,4 ; BR +40,0 ; US −39,6). Notebook : `03_prompting.ipynb`.

---

## Slide 7 — Le piège du few-shot (Maël, 35 s)

**Titre :** « Sept exemples mal choisis suffisent à créer un biais : le Brésil perd 243 points »

**Contenu affiché :** chiffre fort **−243 → −62** (Brésil, par rapport à la France) ; « Mêmes 7 exemples, même ordre : on a seulement retiré leur pays » ; **« Le biais peut venir de nous »**.

**Visuel :** F7, `presentation/figures/f7_few_shot_exemples.png`.

**Notes du présentateur :**
> « Pour l'aider, on a ajouté sept exemples de parties avec leur vrai Elo : c'est le few-shot. Dans notre première version, chaque exemple mentionnait aussi le pays. Par malchance, l'exemple brésilien avait un Elo bas. Le modèle en a tiré une règle : à partie identique, un Brésilien perdait 243 points ! Mêmes exemples, sans le pays : l'écart tombe à −62. Le biais ne venait pas seulement du modèle, il venait aussi de nos choix. »

**Sources :** `resultats_prompting_v2/comparaison_premiere_execution.csv` (Few-shot : BR −242,9 → −61,9 ; IN −100,7 → +7,1 ; US −47,0 → +37,1 ; DE +71,6 → +46,1). Notebook : `03_prompting.ipynb`.

---

## Slide 8 — Méthode 2, le RAG (Maël, 30 s)

**Titre :** « Avec des dossiers de cas similaires, il devient plus juste, mais pas plus utile »

**Contenu affiché :** chiffre fort **573** points d'erreur moyenne, plus qu'une réponse constante (530) ; écart entre pays : moins de 20 points en moyenne ; **« Juste n'est pas utile »**.

**Visuel :** F8a, `presentation/figures/f8a_mae_rag.png` (RAG, constante et médiane des voisins en évidence).

**Notes du présentateur :**
> « Deuxième méthode, le RAG. Pour chaque partie, on va chercher les dix parties les plus proches, avec leur vrai Elo, et on les donne au modèle comme des dossiers. Bonne nouvelle : il devient plus équitable, l'écart moyen entre pays passe sous les 20 points. Mauvaise nouvelle : il se trompe encore de 573 points, plus que si on répondait toujours la même valeur. Équitable mais imprécis : ça ne sert à rien. »

(Pour les questions : la simple médiane de l'Elo des 10 voisins, sans LLM, fait 453.)

**Sources :** `resultats_finetuning_complets/scores_global.csv` (573,2 ; 529,7 ; médiane des voisins 452,6), `biais_ecarts_france.csv` (RAG : au plus +17,5). Notebook : `04_rag.ipynb`.

---

## Slide 9 — Méthode 3, le fine-tuning (Maël, 35 s)

**Titre :** « Une fois vraiment formé, il devient enfin compétent : aussi précis qu'un modèle classique »

**Contenu affiché :** chiffre fort **380** points d'erreur (FT-A), 382 pour FT-B, contre 644 au départ ; **≈ gradient boosting : 369** ; FT-A : vrai pays, FT-B : pays tiré au hasard.

**Visuel :** F8b, `presentation/figures/f8b_mae_finetuning.png` (FT-A, FT-B et gradient boosting en évidence, zero-shot en pâle).

**Notes du présentateur :**
> « Troisième méthode : on forme vraiment le modèle. C'est le fine-tuning : on entraîne un petit adaptateur sur nos 3 300 parties d'entraînement, chacune avec son vrai Elo. Deux versions : FT-A voit le vrai pays, FT-B voit un pays tiré au hasard, pour casser le lien entre pays et Elo. Les deux se trompent d'environ 380 points : 260 de moins qu'au départ, et le niveau d'un modèle classique, le gradient boosting, à 369. Notre employé est enfin compétent. »

**Sources :** `resultats_finetuning_complets/scores_global.csv` (379,6 ; 382,3 ; 369,4 ; 643,9), `comparaison_mae.csv` (FT-B − gradient boosting = +13, non significatif ; FT-B − zero-shot = −262). Notebooks : `05_finetuning.ipynb`, `05_finetuning_kaggle.ipynb`.

---

## Slide 10 — LA slide du biais (Maël, 35 s)

**Titre :** « À chaque méthode, l'effet du pays fond : de 150 points à 16 »

**Contenu affiché :** chiffre fort **150 → 16** points d'écart entre pays, pour une même partie ; le pays change la prédiction : 78 % des parties → 10 % ; **« FT-B : notre modèle retenu »**.

**Visuel :** F9, `presentation/figures/f9_etendue_biais.png`.

**Notes du présentateur :**
> « Voici la slide qui résume le projet. On présente une même partie cinq fois au modèle, en changeant seulement le pays, et on mesure l'écart entre sa plus haute et sa plus basse estimation. Avec les consignes : 150 points. Avec les exemples : 120. Avec les dossiers : 58. Après formation : 37, et 16 pour FT-B, notre modèle retenu. Au départ, le pays changeait la prédiction pour 78 % des parties ; avec FT-B, pour 10 %. Le biais fond. »

**Sources :** `resultats_finetuning_complets/biais_etendue_par_partie.csv` (150,0 ; 120,0 ; 57,7 ; 36,6 ; 15,75 ; 77,9 % et 10,0 %). Test sur 140 parties × 5 pays : `data/prompts/bias_test.jsonl`. (FT-B − FT-A = −21 [−51 ; +5], non significatif : dit à la slide 14.)

---

## Slide 11 — XAI (Hugo, 40 s)

**Titre :** « Quand on lui demande de se justifier, le modèle formé ne regarde plus le pays, mais la qualité du jeu »

**Contenu affiché :** chiffre fort **15,5 % → 0,2 %**, part du pays dans la décision, avant et après fine-tuning ; avant : victoire ou défaite, après : ouverture, ACPL, premiers coups ; *« SHAP mesure, LIME confirme »*.

**Visuel :** F10, `presentation/figures/f10_shap_avant_apres.png` (modèle de base : Résultat 35,6 %, Pays 15,5 %, Fin de partie 12,9 %, Ouverture 10,4 %, Gaffes 4,8 % ; FT-B : Ouverture 31,6 %, ACPL 28,7 %, Premiers coups 22,8 %, Fin de partie 9,2 %, Nombre de coups 2,8 %, Pays 0,2 %).

**Notes du présentateur :**
> « Dernière étape : on demande au modèle de justifier ses décisions, avec deux outils d'explicabilité. Le principe : on masque une ligne du prompt, par exemple le pays, et on regarde de combien la prédiction bouge. Avant la formation, le modèle juge surtout le résultat, victoire ou défaite, et en deuxième, le pays : 15 % de sa décision. Après, le pays tombe à 0,2 %, et le modèle regarde l'ouverture, l'ACPL et les premiers coups : la vraie qualité du jeu. SHAP mesure, LIME confirme. »

La justification détaillée (additivité, cas simulé, LIME qui réutilise les prédictions de SHAP) est dans l'annexe « Pourquoi SHAP ».

**Sources :** `resultats_xai/part_du_pays.csv` (15,48 ; 0,98 ; 0,24 ; rang 2 sur 12), parts par variable recalculées depuis `resultats_xai/importance_moyenne.csv`. Notebooks : `06_xai.ipynb`, `06_xai_kaggle.ipynb`.

---

## Slide 12 — Démo (Hugo, 55 s)

**Titre :** « Sur nos parties, le modèle de base place Paul, le plus fort, en dernier ; le nôtre le place en premier »

**Contenu affiché :** une carte par joueur, avec sa photo :

| Joueur | Parties | Réel (moyenne) | Base (zero-shot) | Nous (FT-B) |
|---|---|---|---|---|
| Thibault | 3 | 965 | 1 533 | 965 |
| Maël | 3 | 498 | 1 667 | 968 |
| Hugo | 3 | 892 | 1 583 | 803 |
| Paul | 3 | 1 479 | 1 433 | 1 710 |

En dessous : « Partie du début : Maël, 490 Elo · Base : 1 400 · Nous : 371 » ; chiffre fort **622 → 403** points d'erreur par partie.

**Visuel :** composé directement dans PowerPoint (photos `presentation/*.jpg|png`, non versionnées ; Paul compris, sa photo étant dans le dossier). La figure de 06c, `resultats_demo/fig_demo_elo_moyen.png`, avec FT-A, est en annexe.

**Notes du présentateur :**
> « Maintenant, testons-le sur nous. On a pris nos trois dernières parties rapides, et celles de Paul. Le modèle de base donne à peu près le même Elo à tout le monde, entre 1 430 et 1 670 en moyenne, et il place Paul, le plus fort d'entre nous, en dernier. Notre modèle place Paul en premier. Il n'est pas parfait : Maël est surestimé de 470 points. Mais son erreur moyenne par partie passe de 622 à 403 points. Et la partie du début ? C'était celle de Maël, qui est à 490. Le modèle de base disait 1 400. Le nôtre dit 371. »

**Sources :** `resultats_demo/elo_moyen_par_joueur.csv` et `predictions_demo.csv` (06c, 3 parties par joueur ; Joueur 1 = Thibault, 2 = Maël, 3 = Hugo, 4 = Paul). Erreurs par partie 622 et 403 : moyenne sur les 12 parties, vérifiée dans l'annexe de `07_rendu_final.ipynb`.

---

## Slide 13 — Dédicace à Paul (Hugo, 25 s)

**Titre :** « Pour Paul, parti aux États-Unis : le modèle de base lui retire 100 points, le nôtre ne le pénalise pas »

**Contenu affiché :** photo de Paul (1 479 Elo) ; « Ses 3 parties, présentées comme américain plutôt que français » ; modèle de base : **−100 · −100 · −100** (cases pleines) ; notre modèle (FT-B) : **+100 · 0 · 0** (cases contour).

**Visuel :** composé dans PowerPoint, photo `presentation/paul.jpg` (non versionnée). Les waterfalls SHAP de la partie 3 (−105 contre 0) sont en annexe.

**Notes du présentateur :**
> « Cette slide est pour Paul, notre ami parti vivre aux États-Unis cette année. On a présenté ses parties deux fois : comme français, puis comme américain. Le modèle de base lui retire 100 points à chaque partie, juste à cause du mot « États-Unis ». Notre modèle, lui, ne le pénalise pas. Paul, tu peux jouer tranquille. »

**Sources :** `resultats_demo/france_etats_unis.csv` (06c). SHAP du pays sur la partie 3 version « États-Unis » : −105 (base) et 0 (FT-B), `resultats_xai/shap_zero_shot.csv` et `shap_ft_b.csv`.

---

## Slide 14 — Ce qu'on retient (Hugo, 45 s)

**Titre :** « Un biais se mesure et se réduit, mais un modèle juste n'est pas forcément un bon modèle »

**Contenu affiché :** fond sarcelle.
- **3 leçons :** le dataset équilibré et le fine-tuning ont le plus réduit le biais ; le biais peut venir de nous : 7 exemples ont suffi à en créer un ; un modèle équitable n'est pas forcément utile (le RAG).
- **Nos limites :** prédictions concentrées sur 23 valeurs (1677, 1777, 101…) ; **FT-B ne fait pas significativement mieux que FT-A** ; petits échantillons : 140 parties pour le biais, 12 pour l'XAI.

**Notes du présentateur :**
> « Ce qu'on retient. Un : ce qui a le plus réduit le biais, c'est notre dataset équilibré, puis la formation du modèle sur de vraies parties. Deux : le biais peut venir de nous, sept exemples ont suffi à en créer un. Trois : un modèle juste n'est pas forcément utile. Nos limites : le modèle formé répond souvent les mêmes nombres ; FT-B ne fait pas significativement mieux que FT-A ; et nos échantillons restent petits. Donc oui, on peut estimer un niveau à partir d'une partie, sans tenir compte de la nationalité, mais comme un premier avis. Merci, on attend vos questions. »

**Sources :** `07_rendu_final.ipynb` sections 6, 9 et 10 ; `resultats_finetuning_complets/valeurs_frequentes.csv` ; `biais_ft_b_moins_ft_a.csv`.

---

## Annexes (après la slide 14, pour les questions)

| Annexe | Contenu | Fichier |
|---|---|---|
| A1 | Écarts à la France, 5 méthodes | `resultats_finetuning_complets/fig_biais_pays.png` |
| A2 | Écarts au prompt sans pays, 5 méthodes | `resultats_finetuning_complets/fig_biais_sans_pays.png` |
| A3 | Pourquoi SHAP est la mesure principale, et LIME le contrôle (4 arguments, parts LIME 8,8 / 7,0 / 5,8 %) | composée dans PowerPoint |
| A4, A5 | Waterfall SHAP de la partie g1852 (joueur des États-Unis à 707 Elo) : modèle de base (−190 pour le pays), puis FT-B (−10) | `resultats_xai/fig_waterfall_zero_shot_g1852.png`, `fig_waterfall_ft_b_g1852.png` |
| A6, A7 | Waterfall SHAP de la partie 3 de Paul, version « États-Unis » : modèle de base (−105), puis FT-B (0) | `resultats_xai/fig_waterfall_zero_shot_demo_j4_p3_us.png`, `fig_waterfall_ft_b_demo_j4_p3_us.png` |
| A8 | SHAP du gradient boosting : pays 0,9 %, ACPL 36,7 % | `resultats_xai_baseline/fig_importance_globale.png` |
| A9 | Démo complète avec FT-A | `resultats_demo/fig_demo_elo_moyen.png` |
| A10 | Benchmark complet : erreur, R², bonne tranche, écart entre pays, part SHAP du pays | tableau composé dans PowerPoint |

---

## Figures créées (`presentation/figures/`)

| # | Slide | Fichier | Données |
|---|---|---|---|
| F1 | 1 | `f1_echiquier.gif` (animé) et `f1_echiquier_final.png` (plan B) | `data/prompts/demo.jsonl`, champ `first_moves` de `demo_j2_p3` |
| F2 | 2 | `f2_cas_usage.png` | — |
| F3 | 3 | `f3_collecte.png` | `build_dataset.py`, `07_rendu_final.ipynb` section 2 |
| F4 | 4 | `f4_acpl_par_tranche.png` | `data/prompts/{train,val,test}.jsonl`, colonne `acpl` |
| F5 | 5 | `f5_employe_methodes.png` | — |
| F6 | 6 | `f6_zero_shot_pays.png` | `resultats_finetuning_complets/biais_ecarts_sans_pays.csv` (Zero-shot) |
| F7 | 7 | `f7_few_shot_exemples.png` | `resultats_prompting_v2/comparaison_premiere_execution.csv` (Few-shot) |
| F8 | 8 et 9 | `f8a_mae_rag.png`, `f8b_mae_finetuning.png` | `resultats_finetuning_complets/scores_global.csv` |
| F9 | 10 | `f9_etendue_biais.png` | `resultats_finetuning_complets/biais_etendue_par_partie.csv` |
| F10 | 11 | `f10_shap_avant_apres.png` | `resultats_xai/importance_moyenne.csv` (SHAP) |

Les icônes des schémas viennent de Font Awesome (via `react-icons`).

---

## 5 questions probables du jury

**1. Le gradient boosting fait aussi bien (369 contre 382). Pourquoi un LLM ?**
C'est vrai, et nous le disons : pour un vrai tournoi, le gradient boosting serait un choix défendable, moins cher et explicable, avec un pays qui ne pèse que 0,9 %. Le sujet demandait d'adapter un LLM. Notre intérêt a été de montrer qu'un LLM part avec des préjugés, et qu'on peut les mesurer et les réduire. Le LLM fine-tuné lit aussi les premiers coups et accepte du texte libre. *(Annexes A8 et A10.)*

**2. Comment savez-vous que l'écart vient du pays, et pas des parties elles-mêmes ?**
Par le test contrefactuel : c'est exactement la même partie, présentée 5 fois, seule la ligne du pays change. Et comme le dataset est construit avec des quotas, le pays n'apporte aucune information sur l'Elo. Tout écart vient donc du modèle. On ne sait pas dire, en revanche, si c'est un stéréotype sur le pays ou un effet du mot lui-même. *(Annexes A1 et A2.)*

**3. Si FT-B n'est pas meilleur que FT-A de façon prouvée, pourquoi le retenir ?**
À précision égale (382 contre 380, écart non significatif), FT-B va dans le bon sens sur tous les indicateurs de biais : étendue 16 contre 37, part SHAP du pays 0,2 % contre 1,0 %. Il ne coûte rien de plus. FT-A avait déjà peu de biais à corriger, car le train est équilibré. Sur des données déséquilibrées, c'est là que FT-B pourrait vraiment servir. *(Annexe A10.)*

**4. 380 points d'erreur et 29 % de bonnes tranches : c'est utilisable ?**
Pas seul. Une seule partie, c'est très peu d'information : même le meilleur modèle classique se trompe de 369 points. Nous le présentons comme un premier avis pour placer un joueur, à corriger avec ses résultats suivants dans le tournoi. *(28,6 % de bonnes tranches pour FT-B, contre environ 14 % au hasard ; annexe A10.)*

**5. Et la vie privée des joueurs ?**
Les prompts ne contiennent ni pseudo, ni lien, ni Elo de l'adversaire, et un script le vérifie. Les fichiers avec les pseudos ne sont pas publiés. Mais les parties de chess.com sont publiques : avec l'ouverture et les 10 premiers coups, on pourrait en principe retrouver une partie. L'anonymisation réduit le risque, elle ne l'élimine pas. Pour la démo, on a utilisé nos propres parties. *(`build_prompts.py`, `07_rendu_final.ipynb` section 9.)*

À garder en réserve : « Pourquoi SHAP plutôt que LIME ? » (annexe A3) ; « Pourquoi Stockfish ne donne pas directement l'Elo ? » (il évalue des coups, pas des joueurs ; c'est le modèle qui fait le lien) ; « Pourquoi ne pas utiliser l'accuracy de chess.com ? » (elle manque dans 71,5 % des parties, et pas au hasard : son absence dépend du pays).

---

## Plan B

| Problème | Solution |
|---|---|
| Le GIF ne s'anime pas (PDF, autre ordinateur) | Le PDF montre déjà la position finale (première image du GIF). Sinon, remplacer par `presentation/figures/f1_echiquier_final.png`. Thibault lit les coups « 1. e4 e5, 2. Dame h5… » en montrant la position. |
| L'ordinateur ou le PowerPoint ne marche pas | Ouvrir `presentation/soutenance.pdf` (sur une clé USB et un deuxième ordinateur), avec les notes imprimées. Toutes les « démos » sont des figures déjà calculées : rien ne tourne en direct. |
| Une vidéo ou une animation ajoutée plus tard ne se lance pas | Ne pas l'intégrer : mettre un lien et une capture fixe à la place. |
| Retard sur le minutage | Les raccourcis sont déjà appliqués. Si besoin : à la slide 10, ne pas citer 78 % → 10 % ; à la slide 12, couper la phrase sur Maël surestimé. Gain : environ 10 s. |
| Un présentateur absent | Chaque partie peut être reprise par les deux autres à partir des notes. Si Maël est absent, la révélation de la slide 12 devient « c'était la partie de Maël, qui n'a pas pu venir ». |
| Les résultats de 06c sur 10 parties arrivent avant la soutenance | Mettre à jour les cartes de la slide 12 et les cases de la slide 13 avec `resultats_demo/`, remplacer « 3 dernières parties » par « 10 » (5 pour Hugo), et revérifier la formulation du titre de la slide 12 (Paul toujours premier et dernier ?) et de la slide 13. |
