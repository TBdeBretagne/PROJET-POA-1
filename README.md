# Robot de réconfort — DRAME Ibraima \& BRETON Thomas

Projet de semestre, master informatique. Un robot à perception locale
consulte un dictionnaire, fouille une armoire et rapporte un objet à un
résident.

Langage : Python — Version : 3

## Lancer

```
python main.py <carte.json> <scenario.json> <dossier\_donnees> <trace\_sortie.json>
```

Exemple :

```
python main.py cartes/appartement\_01.json cartes/scenario\_01.json donnees sorties/sortie.json
```

Dépendances : *aucune*

## Tester

```
<votre commande de test>
```

*Une phrase sur ce que couvrent les tests.*

## Organisation du code

|Fichier|Rôle|
|-|-|
|`main.py`|point d'entrée, boucle de décision|
|`affichage.py`|gestion de l'affichage dans le terminal|
|`agent.py`|classe agent et toutes ces fonctionnalités|
|`armoire.py`|classe armoire et ces fonctionnalités|
|`chemin.py`|calcul du plus court chemin|
|`dictionnaire.py`|classe dictionnaire , recherche d'émotions|
|`File.py`|enfiler, défiler|
|`reconfort\_io.py`|vérification des fichiers d'entrées|
|`test.py`|vérification de la cohérence des données cartes/scénario|
|`trace.py`|classe Trace, écriture des données |

## État

**Ce qui marche.** *À compléter.*

**Ce qui ne marche pas.** *À compléter — soyez honnêtes, c'est noté en
votre faveur.*

## Vidéo

`VidéoAgent.mp4`

