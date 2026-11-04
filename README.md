# Project-Ethics-of-IA

Construction et audit d'un dataset de parties rapides chess.com, destiné à un modèle de prédiction de l'Elo.
L'objectif est de repérer ce qu'un tel modèle pourrait apprendre d'autre que le niveau de jeu (pays, origine de
l'échantillon, données manquantes).

Le dataset compte 4 200 parties de 856 joueurs, sur 12 mois, réparties par quotas en 7 tranches d'Elo et 5 pays
(FR, IN, US, BR, DE). Le découpage 80/10/10 se fait par joueur.

## Structure

```text
build_dataset.py          collecte via l'API publique de chess.com et découpage train/val/test
stockfish_features.py     gaffes, erreurs, imprécisions et ACPL calculés avec Stockfish
build_prompts.py          prompts du LLM et jeu de test de biais par pays, avec vérification de l'anonymat
01_eda.ipynb              analyse des biais du dataset
02_baseline.ipynb         modèles de référence à battre pour le LLM
03_prompting.ipynb        prompt engineering avec Qwen3-4B-Instruct-2507 et test de biais (Google Colab, GPU T4)
resultats_prompting_v1/   première exécution de 03_prompting.ipynb, relue par la seconde pour ne pas la recalculer
data/                     CSV générés par les scripts (non versionnés)
data/prompts/             prompts anonymes au format JSONL (versionnés)
figures/eda/              graphiques produits par le notebook
requirements.txt          dépendances
requirements.lock.txt     versions figées de l'environnement initial (sans chess ni statsmodels)
.env.example              modèle de configuration du contact chess.com
```

## Installation

Il faut Python 3.10 ou plus récent, ainsi que [Stockfish](https://stockfishchess.org/download/) pour la deuxième
étape de reproduction (sous Windows : `winget install Stockfish.Stockfish`).

```bash
git clone <url-du-repo>
cd Project-Ethics-of-IA
python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name ethics-of-ia --display-name "Python (Ethics of IA)"
```

## Reproduire

Les CSV de `data/` ne sont pas versionnés, car ils contiennent les pseudos des joueurs : le dépôt est public. Sans
copie de ces fichiers, il faut les régénérer avec les étapes 1 et 2. Lancer les commandes depuis la racine du projet.

```bash
# 1. Collecte. Le contact est obligatoire et n'est pas lu depuis un fichier .env.
export CHESSCOM_CONTACT="votre.email@example.com"   # PowerShell : $env:CHESSCOM_CONTACT = "votre.email@example.com"
python -u build_dataset.py

# 2. Variables Stockfish (environ 6 h avec 6 moteurs à la profondeur 14)
python -u stockfish_features.py

# 3. Analyse : exécuter 01_eda.ipynb
jupyter lab 01_eda.ipynb

# 4. Prompts du LLM : data/prompts/*.jsonl, et data/game_ids.csv pour relier un game_id à sa partie (non versionné)
python -u build_prompts.py

# 5. Modèles de référence. data/prompts/ suffit, sauf pour les intervalles de confiance (data/game_ids.csv)
jupyter lab 02_baseline.ipynb

# 6. Prompt engineering : ouvrir 03_prompting.ipynb dans Google Colab avec un GPU T4, puis tout exécuter.
#    Le notebook installe ses dépendances et télécharge data/prompts/ et resultats_prompting_v1/ depuis la branche main.
#    Il ne calcule que les variantes nouvelles et écrit dans resultats_prompting_v2/.
```

Les scripts de collecte et d'analyse Stockfish reprennent là où ils se sont arrêtés et acceptent `--max-hours`. Une nouvelle collecte ne redonne
pas les mêmes parties : la fenêtre de 12 mois part de la date du premier lancement, et les journaux de
`data/checkpoint/` ne sont pas versionnés.

## Limites connues du dataset

- **Échantillonnage boule de neige.** L'API limite la liste des joueurs d'un pays à 10 000 pseudos par ordre
  alphabétique. On part donc de quelques joueurs, puis on visite leurs adversaires : 93 % des parties viennent de
  joueurs atteints ainsi. Les joueurs ne sont pas tirés au hasard et les joueurs actifs sont favorisés, d'autant que
  chacun apporte jusqu'à 5 parties.
- **Leaderboards dans la tranche 1900+.** Les 101 parties issues des leaderboards sont toutes dans cette tranche et y
  pèsent 17 %, malgré un plafond de 25 % par case : 8 % en France, mais 26 % en Inde et aux États-Unis. Le haut de la
  tranche n'est donc pas comparable d'un pays à l'autre. Il faut recalculer les performances sans ces parties.
- **Quotas.** L'absence de lien entre pays et Elo est imposée par construction : elle ne décrit pas la population de
  chess.com.

Le détail et les conséquences pour le modèle (variables à exclure, dont `accuracy`, `source` et `opponent_elo`) sont
dans les conclusions de `01_eda.ipynb`.
