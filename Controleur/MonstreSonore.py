from Controleur.Monstre import Monstre
import math

class MonstreSonore(Monstre): 
    def __init__(self,start : tuple,img : str):
        super().__init__(start,img)
    def bruit_entendu(self, coord_entendu :tuple) -> bool:
        return math.sqrt((coord_entendu[0]-self.coord[0])**2+(coord_entendu[1]-self.coord[1])**2)<6
            
        