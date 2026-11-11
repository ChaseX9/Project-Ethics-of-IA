# Texte oral de la soutenance

**Ethics_of_AI_ECE_DATA_IA** · Thibault Rabbé, Maël Vaudin, Hugo Rivière · environ 9 min 45

Mode d'emploi :
- **[clic]** = passer à la page suivante du PDF. Le numéro dans le pion, en bas à droite, indique la page.
- Les *italiques entre parenthèses* sont des indications de jeu, à ne pas lire.
- Les chiffres sont arrondis pour l'oral. Les valeurs exactes et leurs sources sont dans `plan_presentation.md`.

| Qui | Pages | Durée |
|---|---|---|
| Thibault | 1 à 16 | 3 min 30 |
| Maël | 17 à 24 | 3 min 20 |
| Hugo | 25 à 30 | 2 min 40 |

---

## Thibault

### Page 1 · Titre

*(Slide affichée pendant l'installation. On ne parle pas. Quand tout le monde est prêt :)* **[clic]**

### Page 2 · Les échecs en 20 secondes (15 s)

Bonjour à tous. Un petit rappel pour ceux qui ne jouent pas : les échecs, c'est les blancs contre les noirs, chacun son tour. Un seul but : mettre le roi adverse **échec et mat**, c'est-à-dire l'attaquer sans qu'il puisse s'échapper. Voyons ça en quatre coups. **[clic]**

### Pages 3 à 9 · Le coup du berger (30 s)

*(Cliquer à chaque phrase, sans attendre.)*

Les blancs avancent un pion au centre. **[clic]**

Les noirs font pareil. **[clic]**

Le fou vise la case f7, le point faible des noirs. **[clic]**

Les noirs sortent un cavalier. **[clic]**

La dame vise f7 à son tour. **[clic]**

Et là, les noirs attaquent la dame… mais oublient de défendre f7. Stockfish, le moteur d'échecs, le marque en rouge : c'est une **gaffe**. **[clic]**

La dame prend f7 : échec et mat, en quatre coups. **[clic]**

### Page 10 · Comment juger le niveau d'un joueur ? (15 s)

Comment juger le niveau d'un joueur ? On peut compter ses gaffes. Et on peut mesurer ce qu'il perd à chaque coup, en centièmes de pion : c'est l'**ACPL**. C'est exactement ce que fait Stockfish. À vous de jouer, maintenant. **[clic]**

### Page 11 · À votre avis, quel est l'Elo de ce joueur ? (30 s)

Voici une vraie partie rapide, jouée sur chess.com. Notre joueur a les noirs. Il perd par échec et mat en 67 coups, avec 8 gaffes.

À votre avis, quel est son Elo ? Levez la main : moins de 800 ? *(pause)* Entre 800 et 1 500 ? *(pause)* Plus de 1 500 ? *(pause)*

On vous donne la réponse à la fin. Deviner un niveau à partir d'une seule partie : c'est la question de notre projet. **[clic]**

### Page 12 · Le problème (25 s)

Pour y répondre, on a utilisé une IA, un modèle de langage. Mais ces modèles apprennent sur des milliards de textes du web, qui contiennent aussi des **clichés sur les pays**.

Il y a donc sûrement des biais de nationalité. Imaginez : la même partie, mais l'IA donne 1 500 si le joueur est français, et 1 400 s'il est américain. C'est un exemple fictif, mais ce serait le pays qui décide, pas le jeu. Et ce n'est pas normal : **même partie, même Elo**, quel que soit le pays. **[clic]**

### Page 13 · Notre cas d'usage (20 s)

Notre cas concret : un club organise un tournoi avec des poules de niveau. Un joueur arrive sans classement, joue une partie de placement, et l'IA estime son Elo pour le mettre dans la bonne poule. Mal placé, il affronte des adversaires bien trop forts, ou bien trop faibles. **[clic]**

### Page 14 · Nos données (30 s)

Aucun dataset ne répondait à notre question, alors on l'a construit nous-mêmes, avec l'API publique de chess.com. On est partis de quelques joueurs par pays, puis on a visité leurs adversaires, et ainsi de suite : c'est une collecte en boule de neige. On a exclu les comptes fermés, dont les tricheurs.

Résultat : **4 200 vraies parties**, 5 pays, 7 niveaux. Et chaque pays a la même répartition de niveaux : dans nos données, le pays ne dit rien de l'Elo. **[clic]**

### Page 15 · Stockfish (25 s)

Stockfish mesure l'ACPL. Pour comprendre : un pion vaut 100 centièmes. Perdre 100 centièmes en un coup, c'est comme offrir un pion à l'adversaire.

Les débutants perdent environ **109** centièmes par coup ; les joueurs au-dessus de 1 900, environ **40**. Mais Stockfish ne donne pas l'Elo : passer de ces chiffres à un Elo, c'est le travail de notre IA. **[clic]**

### Page 16 · Feuille de route (20 s)

Notre IA, c'est **Qwen**, un modèle léger. Imaginez un nouvel employé très cultivé, qui n'a jamais estimé un Elo. On a essayé trois façons de le rendre compétent : des consignes, des dossiers de cas similaires, ou une vraie formation. Puis on lui demandera de se justifier.

Maël, à toi. **[clic]**

---

## Maël

### Page 17 · Méthode 1 : le prompt (25 s)

Première méthode, la plus simple : on écrit au modèle une consigne, puis le résumé de la partie calculé par Stockfish. Ici, un joueur américain à 1 030 Elo.

Et le modèle répond… **1 800**. Retenez la ligne en rouge : **le pays**. C'est la seule ligne qu'on change pour mesurer le biais. **[clic]**

### Page 18 · Résultat du prompt (25 s)

Sur nos 437 parties de test, il répond 1 800 près d'une fois sur deux. Son erreur moyenne est de 644 points : pire qu'une réponse toujours identique.

Et à partie identique, s'il lit « allemand » ou « indien », il ajoute **100 points**. Notre employé est ignorant, et il a des préjugés. **[clic]**

### Page 19 · Le piège du few-shot (30 s)

Pour l'aider, on a ajouté sept exemples de parties avec leur vrai Elo. Dans notre première version, chaque exemple indiquait aussi le pays. Par malchance, l'exemple brésilien avait un Elo bas : le modèle en a tiré une règle, et un Brésilien perdait **243 points** !

Mêmes exemples, sans le pays : l'écart tombe à −62. Le biais venait aussi **de nos choix**. **[clic]**

### Page 20 · Méthode 2 : le RAG (25 s)

Deuxième méthode, le RAG. Pour la même partie, on cherche dans nos 3 332 parties d'entraînement les **dix plus proches**, sur la qualité du jeu, jamais sur le pays. On les donne au modèle avec leur vrai Elo, comme des dossiers à consulter.

Ici, il répond 1 450 : mieux, mais toujours loin de 1 030. **[clic]**

### Page 21 · Résultat du RAG (20 s)

Sur tout le test : il devient plus équitable, moins de 20 points d'écart entre pays. Mais il se trompe encore de **573 points**, plus qu'une réponse toujours identique. Équitable mais imprécis : juste n'est pas utile. **[clic]**

### Page 22 · Méthode 3 : le fine-tuning (25 s)

Troisième méthode : on l'entraîne vraiment. On lui montre nos 3 332 parties avec la bonne réponse, deux fois. On ajoute juste un petit module qui apprend, le reste du modèle ne bouge pas.

Deux versions : **FT-A** voit le vrai pays ; **FT-B** voit un pays tiré au hasard, pour casser le lien entre pays et Elo. Sur notre partie, il répond **1 017**, pour 1 030. **[clic]**

### Page 23 · Résultat du fine-tuning (20 s)

Sur tout le test, l'erreur tombe à **380 points**, contre 644 au départ. C'est le niveau d'un modèle classique, le gradient boosting, à 369. Notre employé est enfin compétent. **[clic]**

### Page 24 · Le biais fond (30 s)

Et le biais ? On présente une même partie cinq fois, en changeant seulement le pays, et on mesure l'écart entre la plus haute et la plus basse estimation.

Consignes : **150** points. Exemples : 120. Dossiers : 58. Formation : 37, et **16** pour FT-B, notre modèle retenu. Le biais fond.

Hugo, à toi. **[clic]**

---

## Hugo

### Page 25 · L'explicabilité (35 s)

Dernière étape : on demande au modèle de se justifier. Le principe : on lui cache une information, par exemple le pays, et on regarde de combien sa réponse change.

Le modèle de base regarde d'abord victoire ou défaite, puis… **le pays**, en deuxième position, avec 15 % de sa décision.

Notre modèle regarde l'ouverture, l'ACPL, les premiers coups : la vraie qualité du jeu. Le pays tombe à la **11e place sur 12**, avec 0,2 %. **[clic]**

### Page 26 · Et sur nous ? (20 s)

On est fans d'échecs, alors le vrai test, c'était nos propres parties : dix chacun pour Thibault et Maël, cinq pour moi. Et dix pour **Paul Carrère**, notre ami de classe l'an dernier, qui nous a initiés aux échecs. Vous voyez nos vrais Elo : Paul est de loin le plus fort, avec près de 1 500. **[clic]**

### Page 27 · La démo (40 s)

Le modèle de base donne à peu près le même Elo à tout le monde, entre 1 570 et 1 700. Et il classe Paul, le plus fort d'entre nous, **en dernier**. Notre modèle, lui, le classe **en premier**.

Il n'est pas parfait : Maël est surestimé de 500 points. Mais l'erreur par partie passe de 694 à 423.

Et la partie du début ? *(pause)* C'était celle de Maël, à **490**. Le modèle de base disait 1 400. Le nôtre dit **371**. **[clic]**

### Page 28 · Et si Paul se présentait comme américain ? (30 s)

Paul vit aux États-Unis depuis cette année. On s'est demandé : et s'il se présentait comme américain ?

On a donc présenté ses dix parties deux fois : une fois avec « France », une fois avec « États-Unis ». Son jeu est exactement le même ; seul le pays écrit change.

Résultat : le modèle de base lui retire **près de 100 points** en moyenne. Notre modèle, lui, ne bouge pas. Paul, tu peux jouer tranquille. **[clic]**

### Page 29 · Conclusion

*(Pas de texte : cliquer tout de suite.)* **[clic]**

### Page 30 · Ce qu'on retient (35 s)

Trois leçons. Un : ce qui a le plus réduit le biais, c'est notre dataset équilibré, puis la formation du modèle. Deux : le biais peut venir de nous, sept exemples ont suffi à en créer un. Trois : un modèle juste n'est pas forcément utile.

Nos limites : le modèle répond souvent les mêmes nombres, FT-B ne fait pas significativement mieux que FT-A, et nos échantillons restent petits.

Donc oui, on peut estimer le niveau d'un joueur à partir d'une seule partie, sans tenir compte de sa nationalité, mais seulement comme un premier avis. Merci, nous attendons vos questions.

---

## Si le temps presse

- **Pages 3 à 9 :** cliquer sans commenter les quatre premiers coups ; ne parler qu'à la gaffe (page 8) et au mat (page 9). Gain : environ 15 s.
- **Page 21 :** se contenter de « 573 points : équitable mais imprécis ».
- **Page 27 :** couper la phrase sur Maël surestimé.

## Pendant les questions

Les annexes commencent à la page 31. Pour y aller : taper le numéro de page dans le lecteur PDF.

| Question | Page | Réponse en une phrase |
|---|---|---|
| Pourquoi un LLM, si le gradient boosting fait aussi bien ? | 39, 41 | Pour un vrai tournoi, ce serait un bon choix, moins cher et explicable ; le sujet demandait d'adapter un LLM, et on a montré qu'on pouvait mesurer et réduire ses préjugés. |
| Comment savez-vous que l'écart vient du pays ? | 32, 33 | C'est la même partie, présentée cinq fois, et seule la ligne du pays change ; et nos quotas rendent le pays inutile pour prédire l'Elo. |
| Pourquoi FT-B, s'il n'est pas prouvé meilleur que FT-A ? | 41 | Même précision, et il va dans le bon sens sur tous les indicateurs de biais, sans rien coûter de plus. |
| 380 points d'erreur, c'est utilisable ? | 41 | Pas seul : c'est un premier avis, à corriger avec les résultats suivants du joueur. |
| Pourquoi SHAP plutôt que LIME ? | 34 | SHAP s'additionne exactement jusqu'à la prédiction et donne zéro au pays quand il n'a aucun effet ; LIME sert de contrôle. |
| La partie d'exemple des méthodes est-elle représentative ? | — | Non, elle est choisie pour être parlante : en moyenne, l'erreur est de 644, 573 et 380 points. |
| Et la vie privée des joueurs ? | — | Ni pseudo ni lien dans les données envoyées au modèle, et les fichiers avec les pseudos ne sont pas publiés ; pour la démo, on a utilisé nos propres parties. |
