import json

class Trace():
    def __init__(self, carte, scenario):
        self.donnees = {
            "format": "robot-reconfort/trace",
            "version": 1,
            "carte": carte,
            "scenario": scenario,
            "equipe": [
                "Thomas Breton",
                "Ibraïma Dramé"],
            "pas":[],
            "livraisons":[],
            "resume":{}

        }
        self.t = 0
        self.t_livraison = 0

    def ajouterPas(self,demande, position, casier, action, argument, perception, contenu_casier, commentaire):
        self.donnees["pas"].append({
            "t":self.t,
            "demande":demande,
            "position":position,
            "casier":casier, 
            "action":action,
            "argument": argument,
            "perception":perception,
            "contenu_casier":contenu_casier,
            "commentaire":commentaire
        })
        self.t += 1

    def ajouterLivraison(self, demande, resident, emotion, intensite, casier_choisi, repli, objet, succes, motif_echec):
        self.donnees["livraisons"].append({
            "demande": demande,
            "resident": resident,
            "emotion": emotion,
            "intensite": intensite,
            "casier_choisi": casier_choisi,
            "repli": repli,
            "objet": objet,
            "pas_utilises": self.t - self.t_livraison,
            "succes": succes,
            "motif_echec": motif_echec 
        })
        self.t_livraison = self.t


    def resume(self):
        nbr_livraison = len(self.donnees["livraisons"])
        nbr_pas = len(self.donnees["pas"])
        reussies = 0 
        for i in range(nbr_livraison):
            if self.donnees["livraisons"][i]["succes"]:
                reussies += 1

        self.donnees["resume"]  = {
            "demandes": nbr_livraison,
            "reussies": reussies,
            "echec":nbr_livraison - reussies,
            "pas_total": nbr_pas
        }

    def sauvegarder(self, chemin):
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump(self.donnees, fichier, indent=2, ensure_ascii=False)
        
