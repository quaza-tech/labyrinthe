from Modèle.Monstre import Monstre
import math

class MonstreSonore(Monstre): 
    def __init__(self,start : tuple,img : str):
        super().__init__(start,img)
    def bruit_entendu(self, pertinence : float) -> bool:
        return pertinence > 0.05
            
        