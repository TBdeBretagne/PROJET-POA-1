from src import reconfort_io as rio

class Dictionnaire():
    emotions = {
    "joie": 0,
    "confiance": 1,
    "peur": 2,
    "surprise": 3,
    "tristesse": 4,
    "degout": 5,
    "colere": 6,
    "anticipation": 7
    }

    intensites = {
        "faible": 0,
        "moyenne": 1,
        "forte": 2
    }

    def findEmotion(self,message, entrees):
        words = rio.normaliser(message)
        for word in words:
            for j in range(len(entrees)):
                if word in entrees[j].get("formes"):
                    return [
                        self.intensites[entrees[j].get("intensite")],
                        self.emotions[entrees[j].get("emotion")]
                    ],entrees[j].get("emotion"),entrees[j].get("intensite")
        return None,None,None

