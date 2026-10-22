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

**Ce qui marche.** 
Le robot ce déplace librement dans l'espace, tout en découvrant celui-ci.
Il ne connais donc pas l'espace à l'avance, uniquement l'emplacement de l'armoire, du dictionnaire et des résidents.
Il parvient a livrer un objet au résident quand cela est possible, en décidant lui même qu'elle objet choisir, et dans le cas contraire il passe à la demande suivante.
Il s'arrete une fois qu'il a traité toutes les demandes.
Une fois qu'il a découvert la zone, ses déplacements sont plus précis.

**Ce qui ne marche pas.** 
Une fois toute l'armoire découverte, le robot la parcoure en entier si elle est vide, malgres le fait qu'il sache qu'elle est vide, et ce à chaque fois qu'il y va. Il ne prends pas l'initiative de ne pas la parcourir.


 

## Vidéo

`VidéoAgent.mp4`

