# Project-Ethics-of-IA

## Structure du projet

- `DataSets/` : jeux de données
- `Notebooks/` : notebooks Jupyter
- `requirements.txt` : dépendances du projet
- `requirements.lock.txt` : versions exactes installées (optionnel)

## Installation (nouveaux collaborateurs)

### 1. À installer sur votre machine

- [Git](https://git-scm.com/downloads)
- [Python 3.10 ou plus récent](https://www.python.org/downloads/) (le projet a été créé avec Python 3.12)
- [VS Code](https://code.visualstudio.com/) avec les extensions **Python** et **Jupyter** (ou utilisez JupyterLab, installé avec les dépendances)

### 2. Récupérer le projet et créer l'environnement

```bash
git clone <url-du-repo>
cd Project-Ethics-of-IA
python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name ethics-of-ia --display-name "Python (Ethics of IA)"
```

Pour avoir exactement les mêmes versions que l'auteur de l'environnement, remplacez `requirements.txt` par `requirements.lock.txt` dans la commande `pip install`.

