from Modèle.Monstre import Monstre
import math

class MonstreSonore(Monstre): 
    def __init__(self,start : tuple,img : str):
        super().__init__(start,img)
    def bruit_entendu(self, coord_entendu :tuple,joueur_accroupi : bool) -> bool:
        dx = coord_entendu[0] - self.coord[0]
        dy = coord_entendu[1] - self.coord[1]
        
        distance = math.sqrt(dx**2 + dy**2)

        seuil = 3 if joueur_accroupi else 6

        print("entendue", distance, coord_entendu, self.get_coord())
        print(distance < seuil)

        return distance < seuil
            
        