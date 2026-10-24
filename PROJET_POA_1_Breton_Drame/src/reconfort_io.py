"""
Base de code fournie -- projet "Robot de reconfort".

Ce module fait DEUX choses, et rien d'autre :

  1. lire les quatre fichiers d'entree (carte, dictionnaire, armoire,
     scenario) ;
  2. construire et exporter le fichier de trace attendu a la sortie.

Tout le reste du projet -- perception, carte mentale, planification de
chemin, consultation du dictionnaire, fouille de l'armoire, boucle de
decision -- est a votre charge. Ne cherchez pas ces fonctions ici : elles
n'y sont pas, et c'est volontaire.

Vous avez le droit de modifier ce fichier. Vous avez surtout le devoir de
le comprendre : les verifications faites ici sont minimales (voir la
section "Ce qui n'est PAS verifie" plus bas), et les validations
manquantes font partie du travail demande.

Python 3.9+. Aucune dependance externe.
"""

from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

__all__ = [
    "ErreurFichier",
    "charger_carte",
    "charger_dictionnaire",
    "charger_armoire",
    "charger_scenario",
    "normaliser",
    "Trace",
]

VERSION_ATTENDUE = 1


class ErreurFichier(Exception):
    """Fichier d'entree absent, illisible, ou d'un type inattendu."""


# ---------------------------------------------------------------------------
# Lecture
# ---------------------------------------------------------------------------

def _lire_json(chemin: str | Path, format_attendu: str) -> Dict[str, Any]:
    """Lit un fichier JSON UTF-8 et verifie son en-tete.

    Ce qui EST verifie ici :
      - le fichier existe et se lit en UTF-8 ;
      - son contenu est du JSON valide ;
      - la racine est un objet ;
      - les champs "format" et "version" sont presents et corrects.

    Ce qui n'est PAS verifie (a vous de le faire, enonce section 5.6) :
      - la presence et le type de chacun des autres champs ;
      - la coherence des donnees (grille rectangulaire, positions dans les
        bornes, resident pose sur un mur, casier hors de l'armoire,
        emotion inconnue, resident cite par un scenario mais absent de la
        carte...).
    """
    chemin = Path(chemin)
    try:
        texte = chemin.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ErreurFichier(f"fichier introuvable : {chemin}") from None
    except UnicodeDecodeError as err:
        raise ErreurFichier(
            f"{chemin} n'est pas encode en UTF-8 (octet {err.start})"
        ) from None
    except OSError as err:
        raise ErreurFichier(f"{chemin} illisible : {err}") from None

    try:
        donnees = json.loads(texte)
    except json.JSONDecodeError as err:
        raise ErreurFichier(
            f"{chemin} n'est pas un JSON valide : {err.msg} "
            f"(ligne {err.lineno}, colonne {err.colno})"
        ) from None

    if not isinstance(donnees, dict):
        raise ErreurFichier(
            f"{chemin} : la racine doit etre un objet JSON, "
            f"pas {type(donnees).__name__}"
        )

    format_trouve = donnees.get("format")
    if format_trouve != format_attendu:
        raise ErreurFichier(
            f"{chemin} : format attendu '{format_attendu}', "
            f"trouve {format_trouve!r}"
        )

    version = donnees.get("version")
    if version != VERSION_ATTENDUE:
        raise ErreurFichier(
            f"{chemin} : version {VERSION_ATTENDUE} attendue, trouve {version!r}"
        )
    return donnees

# Verification des champs intérieur
def verifier_dict(donnees, squelette, nom):
    if not isinstance(donnees, dict):
        raise ErreurFichier(f"{nom} doit être un dictionnaire")

    for cle, type_attendu in squelette.items():
        if cle not in donnees:
            raise ErreurFichier(f"{nom} : clé manquante : {cle}")

        if not isinstance(donnees[cle], type_attendu):
            raise ErreurFichier(f"{nom} : type incorrect pour {cle}")

def verifier_liste(liste, type_element, nom):
    if not isinstance(liste, list):
        raise ErreurFichier(f"{nom} doit être une liste")

    for element in liste:
        if not isinstance(element, type_element):
            raise ErreurFichier(
                f"{nom} contient un élément de type incorrect"
            )

def charger_carte(chemin: str | Path) -> Dict[str, Any]:
    """Charge un fichier carte. Voir l'enonce, section 5.1."""
    donnees = _lire_json(chemin, "robot-reconfort/carte")

    squelette = {
            "nom": str,
            "dimensions": dict,
            "legende": dict,
            "grille": list,
            "depart_robot":list,
            "armoire":dict,
            "dictionnaire":dict,
            "residents":list,

        }
    
    for cle, type_attendu in squelette.items():
        if cle not in donnees:
            raise ErreurFichier(f"Clé manquante dans la carte : {cle}")
        if not isinstance(donnees[cle], type_attendu):
            raise ErreurFichier(f"Type incorrect dans la carte : {cle}")

    # Verification des dicts interne
    squelette = {
        "hauteur":int,
        "largeur":int,
    }
    verifier_dict(donnees["dimensions"],squelette,"carte/dimensions")

    squelette = {
        "#": str,
        ".": str,
        "R": str,
        "A": str,
        "D": str,
        "P": str
    }
    verifier_dict(donnees["legende"],squelette,"carte/legende")

    squelette = {
        "position":list,
    }
    verifier_dict(donnees["armoire"],squelette,"carte/armoire")
    verifier_dict(donnees["dictionnaire"],squelette,"carte/dictionnaire")


    # Verification des listes interne

    # Verification armoire et dictionnaire
    if len(donnees["armoire"]["position"]) ==2:
        verifier_liste(donnees["armoire"]["position"],int,"position armoire")
    else: raise ErreurFichier("Position de l'armoire incorrecte dans la carte")

    if len(donnees["dictionnaire"]["position"]) ==2:
        verifier_liste(donnees["dictionnaire"]["position"],int,"position dictionnaire")
    else : raise ErreurFichier("Position du dictionnaire incorrecte dans la carte")

    # Verification de la grille
    verifier_liste(donnees["grille"],str,"grille")
    hauteur = donnees["dimensions"]["hauteur"]
    largeur = donnees["dimensions"]["largeur"]
    
    if len(donnees["grille"]) != hauteur:
        raise ErreurFichier("Hauteur incohérente avec la grille")

    for ligne in donnees["grille"]:
        if len(ligne) != largeur:
            raise ErreurFichier("Dimensions de la grille incohérentes")

    # Verification position de départ
    if len(donnees["depart_robot"]) == 2:
        verifier_liste(donnees["depart_robot"],int,"depart_robot")
    else:
        raise ErreurFichier("Position de départ incorrecte dans la carte")

    # Verification des résidents
    verifier_liste(donnees["residents"],dict,"residents")
    for resident in donnees["residents"]:
        squelette = {
            "id":str,
            "nom":str,
            "position":list
        }
        verifier_dict(resident,squelette,"carte/resident")
        if len(resident["position"]) == 2:
            verifier_liste(resident["position"],int,"resident['position']")
        else: raise ErreurFichier("Position d'un résident incorrecte dans la carte")
  


    return donnees


def charger_dictionnaire(chemin: str | Path) -> Dict[str, Any]:
    """Charge un fichier dictionnaire. Voir l'enonce, section 5.2."""
    donnees = _lire_json(chemin, "robot-reconfort/dictionnaire")

    squelette = {
        "nom": str,
        "emotions": list,
        "intensites": list,
        "entrees": list
    }

    for cle, type_attendu in squelette.items():
        if cle not in donnees:
            raise ErreurFichier(f"Clé manquante dans le dictionnaire : {cle}")
        if not isinstance(donnees[cle], type_attendu):
            raise ErreurFichier(f"Type incorrect dans le dictionnaire : {cle}")

    # Verification des listes
    if len(donnees["emotions"]) == 8:
        verifier_liste(donnees["emotions"],str,"liste émotions")
    else: raise ErreurFichier(f"Liste d'émotions incorrecte dans dictionnaire")

    if len(donnees["intensites"]) == 3:
        verifier_liste(donnees["intensites"],str,"liste intensités")
    else: raise ErreurFichier(f"Liste d'intensités incorrecte dans dictionnaire")

    verifier_liste(donnees["entrees"], dict, "entrees")
    for entree in donnees["entrees"]:
        squelette = {
            "formes": list,
            "emotion": str,
            "intensite": str
            }
        verifier_dict(entree,squelette,"dictionnaire/entree")
        verifier_liste(entree["formes"],str,"formes")

    return donnees


def charger_armoire(chemin: str | Path) -> Dict[str, Any]:
    """Charge un fichier armoire. Voir l'enonce, section 5.3."""
    donnees =  _lire_json(chemin, "robot-reconfort/armoire")
    squelette = {
            "nom": str,
            "emotions": list,
            "intensites": list,
            "casier_depart": list,
            "casiers":list,
        }
    
    for cle, type_attendu in squelette.items():
        if cle not in donnees:
            raise ErreurFichier(f"Clé manquante dans l'armoire : {cle}")
        if not isinstance(donnees[cle], type_attendu):
            raise ErreurFichier(f"Type incorrect dans l'armoire : {cle}")

    # Verification des listes
    if len(donnees["emotions"]) == 8:
        verifier_liste(donnees["emotions"],str,"liste émotions")
    else: raise ErreurFichier(f"Liste d'émotions incorrecte dans armoire")

    if len(donnees["intensites"]) == 3:
        verifier_liste(donnees["intensites"],str,"liste intensités")
    else: raise ErreurFichier(f"Liste d'intensités incorrecte dans armoire")

    if len(donnees["casier_depart"]) == 2:
        verifier_liste(donnees["casier_depart"],int,"casier_depart")
    else: raise ErreurFichier(f"casier_depart incorrecte dans armoire")

    verifier_liste(donnees["casiers"],dict,"casiers")
    for casier in donnees["casiers"]:
        squelette = {
            "ligne": int,
            "colonne": int,
            "emotion": str,
            "intensite": str,
            "objet": str | type(None)
        }
        verifier_dict(casier,squelette,"armoire/casiers")

    return donnees


def charger_scenario(chemin: str | Path) -> Dict[str, Any]:
    """Charge un fichier scenario. Voir l'enonce, section 5.4."""
    donnees = _lire_json(chemin, "robot-reconfort/scenario")

    squelette = {
        "nom": str,
        "carte": str,
        "armoire": str,
        "demandes": list
    }

    for cle, type_attendu in squelette.items():
        if cle not in donnees:
            raise ErreurFichier(f"Clé manquante dans le scenario : {cle}")
        if not isinstance(donnees[cle], type_attendu):
            raise ErreurFichier(f"Type incorrect dans le scenario : {cle}")

    # Verification demandes
    verifier_liste(donnees["demandes"],dict,"demandes")
    for demande in donnees["demandes"]:
        squelette = {
            "numero": int,
            "resident": str,
            "message": str
        }
        verifier_dict(demande,squelette,"scenario/demande")

    return donnees


# ---------------------------------------------------------------------------
# Normalisation des messages
# ---------------------------------------------------------------------------

def normaliser(texte: str) -> List[str]:
    """Decoupe un message en mots comparables au dictionnaire.

    Minuscules, accents retires, decoupage sur tout ce qui n'est pas une
    lettre. C'est exactement la regle de l'enonce, section 6.1 ;
    reimplementez-la vous-meme si vous travaillez dans un autre langage.

        >>> normaliser("Je suis TERRIFIEE, vraiment !")
        ['je', 'suis', 'terrifiee', 'vraiment']
    """
    decompose = unicodedata.normalize("NFD", texte.lower())
    sans_accents = "".join(
        c for c in decompose if unicodedata.category(c) != "Mn"
    )
    mots: List[str] = []
    courant: List[str] = []
    for caractere in sans_accents:
        if caractere.isalpha():
            courant.append(caractere)
        elif courant:
            mots.append("".join(courant))
            courant = []
    if courant:
        mots.append("".join(courant))
    return mots


# ---------------------------------------------------------------------------
# Ecriture de la trace
# ---------------------------------------------------------------------------

ACTIONS = ("AVANCER", "CONSULTER", "CHERCHER", "PRENDRE", "DONNER", "ATTENDRE")
DIRECTIONS = ("N", "S", "E", "O")
REPLIS = ("aucun", "intensite", "voisine_1", "voisine_2")


class Trace:
    """Accumule les pas et les livraisons, puis ecrit le fichier de sortie.

    Utilisation typique :

        trace = Trace(nom_carte="appartement_01",
                      nom_scenario="scenario_01",
                      equipe=["Dupont", "Martin"])
        ...
        trace.ajouter_pas(demande=1, position=(6, 1), casier=(1, 0),
                          action="AVANCER", argument="E",
                          perception={"N": "libre", "S": "mur",
                                      "E": "libre", "O": "mur"})
        ...
        trace.ajouter_livraison(demande=1, resident="R1",
                                emotion="tristesse", intensite="moyenne",
                                casier_choisi=(1, 4), repli="aucun",
                                objet="couverture", succes=True)
        trace.ecrire("sorties/trace_01.json")
    """

    def __init__(
        self,
        nom_carte: str,
        nom_scenario: str,
        equipe: Optional[Sequence[str]] = None,
    ) -> None:
        self.nom_carte = nom_carte
        self.nom_scenario = nom_scenario
        self.equipe: List[str] = list(equipe or [])
        self.pas: List[Dict[str, Any]] = []
        self.livraisons: List[Dict[str, Any]] = []

    # -- pas ---------------------------------------------------------------

    def ajouter_pas(
        self,
        demande: Optional[int],
        position: Sequence[int],
        casier: Sequence[int],
        action: str,
        argument: Optional[str] = None,
        perception: Optional[Dict[str, str]] = None,
        contenu_casier: Optional[str] = None,
        commentaire: Optional[str] = None,
    ) -> None:
        """Enregistre un pas de simulation.

        `position`  : couple (ligne, colonne) du robot AVANT l'action.
        `casier`    : couple (ligne, colonne) du selecteur dans l'armoire,
                      AVANT l'action.
        `perception`: ce que le robot voit depuis sa position, sous la forme
                      d'un dictionnaire des quatre directions vers "mur",
                      "libre", "armoire", "dictionnaire" ou "resident".
        `contenu_casier` : l'objet du casier courant, quand le robot est
                      devant l'armoire et peut donc le voir ; None sinon.
        """
        if action not in ACTIONS:
            raise ValueError(
                f"action inconnue {action!r} (attendu : {', '.join(ACTIONS)})"
            )
        if action in ("AVANCER", "CHERCHER") and argument not in DIRECTIONS:
            raise ValueError(
                f"{action} attend une direction parmi {DIRECTIONS}, "
                f"pas {argument!r}"
            )
        self.pas.append({
            "t": len(self.pas),
            "demande": demande,
            "position": [int(position[0]), int(position[1])],
            "casier": [int(casier[0]), int(casier[1])],
            "action": action,
            "argument": argument,
            "perception": dict(perception) if perception else None,
            "contenu_casier": contenu_casier,
            "commentaire": commentaire,
        })

    # -- livraisons --------------------------------------------------------

    def ajouter_livraison(
        self,
        demande: int,
        resident: str,
        emotion: Optional[str],
        intensite: Optional[str],
        casier_choisi: Optional[Sequence[int]],
        repli: str,
        objet: Optional[str],
        succes: bool,
        motif_echec: Optional[str] = None,
    ) -> None:
        """Enregistre l'issue d'une demande, reussie ou non.

        En cas d'echec, `succes` vaut False et `motif_echec` explique
        pourquoi en une chaine courte (par exemple "resident inaccessible",
        "armoire vide", "emotion indeterminee").
        """
        if repli not in REPLIS:
            raise ValueError(
                f"repli inconnu {repli!r} (attendu : {', '.join(REPLIS)})"
            )
        if not succes and not motif_echec:
            raise ValueError("un echec doit etre accompagne d'un motif_echec")
        self.livraisons.append({
            "demande": int(demande),
            "resident": resident,
            "emotion": emotion,
            "intensite": intensite,
            "casier_choisi": ([int(casier_choisi[0]), int(casier_choisi[1])]
                              if casier_choisi is not None else None),
            "repli": repli,
            "objet": objet,
            "pas_utilises": sum(1 for p in self.pas if p["demande"] == demande),
            "succes": bool(succes),
            "motif_echec": motif_echec,
        })

    # -- export ------------------------------------------------------------

    def en_dictionnaire(self) -> Dict[str, Any]:
        reussies = sum(1 for l in self.livraisons if l["succes"])
        return {
            "format": "robot-reconfort/trace",
            "version": VERSION_ATTENDUE,
            "carte": self.nom_carte,
            "scenario": self.nom_scenario,
            "equipe": self.equipe,
            "pas": self.pas,
            "livraisons": self.livraisons,
            "resume": {
                "demandes": len(self.livraisons),
                "reussies": reussies,
                "echecs": len(self.livraisons) - reussies,
                "pas_total": len(self.pas),
            },
        }

    def ecrire(self, chemin: str | Path) -> Path:
        """Ecrit la trace en JSON UTF-8 indente. Cree le dossier au besoin."""
        chemin = Path(chemin)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(
            json.dumps(self.en_dictionnaire(), ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
        return chemin
