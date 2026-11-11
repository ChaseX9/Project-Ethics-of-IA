# Texte oral de la soutenance

**Ethics_of_AI_ECE_DATA_IA** · Thibault Rabbé, Maël Vaudin, Hugo Riviere · environ 9 min 30

Mode d'emploi :
- **[clic]** = passer à la page suivante du PDF. Le numéro dans le pion, en bas à droite, indique la page.
- Les *italiques entre parenthèses* sont des indications de jeu, à ne pas lire.
- Les chiffres sont arrondis pour l'oral. Les valeurs exactes et leurs sources sont dans `plan_presentation.md`.

| Qui | Pages | Durée |
|---|---|---|
| Thibault | 1 à 15 | 3 min 45 |
| Maël | 16 à 20 | 2 min 55 |
| Hugo | 21 à 24 | 2 min 35 |

---

## Thibault

### Page 1 · Titre

*(Slide affichée pendant l'installation. On ne parle pas. Quand tout le monde est prêt :)* **[clic]**

### Page 2 · Les échecs en 20 secondes (20 s)

Bonjour à tous. Avant de commencer, un petit rappel pour ceux qui ne jouent pas.

Les échecs, c'est les blancs contre les noirs, chacun son tour. Il y a six sortes de pièces, et un seul but : mettre le roi adverse **échec et mat**, c'est-à-dire l'attaquer sans qu'il puisse s'échapper.

Voyons ce que ça donne en quatre coups. **[clic]**

### Pages 3 à 9 · Le coup du berger (35 s)

*(Cliquer à chaque phrase, sans attendre.)*

Les blancs avancent un pion au centre. **[clic]**

Les noirs font pareil. **[clic]**

Le fou vise la case f7, le point faible des noirs. **[clic]**

Les noirs sortent un cavalier. **[clic]**

La dame vise f7 à son tour. **[clic]**

Et là, les noirs attaquent la dame… mais oublient de défendre f7. Stockfish, le moteur d'échecs, le marque en rouge : c'est une **gaffe**. **[clic]**

La dame prend f7 : échec et mat, en quatre coups. **[clic]**

### Page 10 · Comment juger le niveau d'un joueur ? (20 s)

Alors, comment juger le niveau d'un joueur ?

On peut compter ses gaffes, comme celle qu'on vient de voir. Et on peut mesurer ce qu'il perd à chaque coup, en centièmes de pion : on appelle ça l'**ACPL**.

C'est exactement ce que fait Stockfish. Maintenant, c'est à vous de jouer. **[clic]**

### Page 11 · À votre avis, quel est l'Elo de ce joueur ? (35 s)

Voici une vraie partie rapide, jouée sur chess.com. Notre joueur a les noirs. Il perd par échec et mat en 67 coups, avec 8 gaffes, et il perd en moyenne 117 centièmes de pion par coup.

À votre avis, quel est son Elo ? Levez la main : moins de 800 ? *(pause)* Entre 800 et 1 500 ? *(pause)* Plus de 1 500 ? *(pause)*

On vous donne la réponse à la fin. Deviner un niveau à partir d'une seule partie : c'est exactement la question de notre projet. **[clic]**

### Page 12 · Le problème (30 s)

Notre cas d'usage : un club organise un tournoi en rapide, avec des poules de niveau. Un joueur arrive sans classement. Il joue une partie de placement, et une IA estime son Elo pour le mettre dans la bonne poule.

C'est une décision sur une personne. Si l'IA le place plus bas parce qu'il est brésilien ou américain, c'est injuste. Notre règle est donc simple : **même partie, même Elo prédit, quel que soit le pays**. **[clic]**

### Page 13 · Nos données (35 s)

Aucun dataset ne répondait à notre question, alors on l'a construit nous-mêmes, avec l'API publique de chess.com.

On est partis de quelques joueurs par pays, puis on a visité leurs adversaires, puis les adversaires de ces adversaires : c'est une collecte en boule de neige. On a exclu les comptes fermés, dont les tricheurs bannis.

Résultat : **4 200 vraies parties**, 5 pays, 7 niveaux. Et on a imposé des quotas : chaque pays a la même répartition de niveaux. Dans nos données, le pays ne dit donc rien de l'Elo. Si un modèle s'en sert, c'est un biais du modèle, pas des données. **[clic]**

### Page 14 · Stockfish (25 s)

Les gaffes, on les a déjà vues. Stockfish mesure aussi l'ACPL : les débutants perdent environ **109** centièmes de pion par coup, les joueurs au-dessus de 1 900, environ **40**.

Attention : Stockfish ne donne pas l'Elo. Il mesure les coups. Passer de ces statistiques à un Elo, c'est le travail de notre IA. **[clic]**

### Page 15 · Feuille de route (25 s)

Notre IA, c'est **Qwen**, un modèle de langage léger, de 4 milliards de paramètres. Imaginez un nouvel employé très cultivé, qui n'a jamais estimé un Elo de sa vie.

On a essayé trois façons de le rendre compétent : lui donner des consignes, lui donner des dossiers de cas similaires, ou le former vraiment. Les trois partent du même modèle de base. Et à la fin, on lui demandera de justifier ses décisions.

Maël, à toi. **[clic]**

---

## Maël

### Page 16 · Méthode 1, le prompt (40 s)

Première méthode : on donne juste des consignes au modèle. C'est ce qu'on appelle le *zero-shot*.

Résultat : il répond **1 800** près d'une fois sur deux, quel que soit le joueur. Son erreur moyenne est de 644 points : c'est pire qu'un modèle qui répondrait toujours la même valeur.

Et ce n'est pas tout. À partie identique, si on écrit que le joueur est allemand ou indien, il lui donne **100 points de plus** que si on ne dit rien. Notre employé est ignorant, et en plus, il a des préjugés. **[clic]**

### Page 17 · Le piège du few-shot (35 s)

Pour l'aider, on a ajouté sept exemples de parties avec leur vrai Elo. C'est le *few-shot*.

Dans notre première version, chaque exemple mentionnait aussi le pays du joueur. Par malchance, l'exemple brésilien avait un Elo bas. Le modèle en a tiré une règle : à partie identique, un Brésilien perdait **243 points** !

On a gardé les mêmes exemples, dans le même ordre, en retirant juste le pays. L'écart tombe à −62. Le biais ne venait pas seulement du modèle : **il venait aussi de nos choix**. **[clic]**

### Page 18 · Méthode 2, le RAG (30 s)

Deuxième méthode, le RAG. Pour chaque partie, on va chercher les dix parties les plus proches dans nos données, avec leur vrai Elo, et on les donne au modèle comme des dossiers à consulter.

Bonne nouvelle : il devient plus équitable, l'écart moyen entre pays passe sous les 20 points. Mauvaise nouvelle : il se trompe encore de **573 points**, plus que si on répondait toujours la même valeur.

Équitable mais imprécis : juste n'est pas utile. **[clic]**

### Page 19 · Méthode 3, le fine-tuning (35 s)

Troisième méthode : on forme vraiment le modèle. C'est le *fine-tuning*. On entraîne un petit module supplémentaire sur nos 3 300 parties d'entraînement, chacune avec son vrai Elo.

On a fait deux versions. FT-A voit le vrai pays du joueur. FT-B voit un pays tiré au hasard : on casse volontairement le lien entre le pays et l'Elo.

Les deux se trompent d'environ **380 points**. C'est 260 de moins qu'au départ, et c'est le niveau d'un modèle classique, le gradient boosting, à 369. Notre employé est enfin compétent. **[clic]**

### Page 20 · Le biais fond (35 s)

Voici la slide qui résume notre projet. On présente une même partie cinq fois au modèle, en changeant seulement le pays, et on mesure l'écart entre sa plus haute et sa plus basse estimation.

Avec les consignes : **150** points. Avec les exemples : 120. Avec les dossiers : 58. Après la formation : 37, et **16** pour FT-B, notre modèle retenu.

Au départ, le pays changeait la prédiction pour 78 % des parties. Avec FT-B, pour 10 %. Le biais fond.

Hugo, à toi. **[clic]**

---

## Hugo

### Page 21 · L'explicabilité (40 s)

Dernière étape : on demande au modèle de justifier ses décisions, avec deux outils d'explicabilité. Le principe : on masque une ligne du résumé de la partie, par exemple le pays, et on regarde de combien la prédiction bouge.

Avant la formation, le modèle juge surtout le résultat, victoire ou défaite. Et en deuxième position, le pays : **15 %** de sa décision.

Après la formation, le pays tombe à **0,2 %**. Le modèle regarde maintenant l'ouverture, l'ACPL et les premiers coups : la vraie qualité du jeu. SHAP mesure, LIME confirme. **[clic]**

### Page 22 · La démo (50 s)

Maintenant, testons-le sur nous. On a pris nos dix dernières parties rapides, cinq pour moi, et celles de notre ami Paul.

Le modèle de base donne à peu près le même Elo à tout le monde, entre 1 570 et 1 700. Et il classe Paul, le plus fort d'entre nous, **en dernier**. Notre modèle, lui, le classe **en premier**.

Il n'est pas parfait : Maël est surestimé de 500 points. Mais l'erreur par partie passe de 694 à 423.

Et la partie du début ? *(pause)* C'était celle de Maël, qui est à **490**. Le modèle de base disait 1 400. Le nôtre dit **371**. **[clic]**

### Page 23 · Pour Paul (25 s)

Cette slide est pour Paul, notre ami parti vivre aux États-Unis cette année.

On a présenté ses dix parties deux fois : comme français, puis comme américain. Le modèle de base lui retire **près de 100 points** en moyenne, juste à cause du mot « États-Unis », et jusqu'à 200 sur certaines parties. Notre modèle, lui, ne le pénalise pas.

Paul, tu peux jouer tranquille. **[clic]**

### Page 24 · Ce qu'on retient (40 s)

Ce qu'on retient, en trois points.

Un : ce qui a le plus réduit le biais, c'est notre dataset équilibré, puis la formation du modèle sur de vraies parties.

Deux : le biais peut venir de nous. Sept exemples mal choisis ont suffi à en créer un.

Trois : un modèle juste n'est pas forcément utile.

Nos limites, maintenant : le modèle répond souvent les mêmes nombres, FT-B ne fait pas significativement mieux que FT-A, et nos échantillons restent petits.

Donc oui, on peut estimer le niveau d'un joueur à partir d'une seule partie, sans tenir compte de sa nationalité. Mais seulement comme un premier avis.

Merci. Nous attendons vos questions.

---

## Si le temps presse

- **Pages 3 à 9 :** cliquer sans commenter les quatre premiers coups ; ne parler qu'à la gaffe (page 8) et au mat (page 9). Gain : environ 15 s.
- **Page 20 :** ne pas citer « 78 % → 10 % ».
- **Page 22 :** couper la phrase sur Maël surestimé.

## Pendant les questions

Les annexes commencent à la page 25. Pour y aller : taper le numéro de page dans le lecteur PDF.

| Question | Page | Réponse en une phrase |
|---|---|---|
| Pourquoi un LLM, si le gradient boosting fait aussi bien ? | 33, 35 | Pour un vrai tournoi, ce serait un bon choix, moins cher et explicable ; le sujet demandait d'adapter un LLM, et on a montré qu'on pouvait mesurer et réduire ses préjugés. |
| Comment savez-vous que l'écart vient du pays ? | 26, 27 | C'est la même partie, présentée cinq fois, et seule la ligne du pays change ; et nos quotas rendent le pays inutile pour prédire l'Elo. |
| Pourquoi FT-B, s'il n'est pas prouvé meilleur que FT-A ? | 35 | Même précision, et il va dans le bon sens sur tous les indicateurs de biais, sans rien coûter de plus. |
| 380 points d'erreur, c'est utilisable ? | 35 | Pas seul : c'est un premier avis, à corriger avec les résultats suivants du joueur. |
| Pourquoi SHAP plutôt que LIME ? | 28 | SHAP s'additionne exactement jusqu'à la prédiction et donne zéro au pays quand il n'a aucun effet ; LIME sert de contrôle. |
| Et la vie privée des joueurs ? | — | Ni pseudo ni lien dans les données envoyées au modèle, et les fichiers avec les pseudos ne sont pas publiés ; pour la démo, on a utilisé nos propres parties. |
