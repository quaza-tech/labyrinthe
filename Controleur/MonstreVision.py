from Controleur.Monstre import Monstre

class MonstreVision(Monstre): 
    def __init__(self,start : tuple,img : str):
        super().__init__(start,img)
    def joueur_est_visible(self, coord_visible :dict,coord_joueur : tuple) -> bool:
        return coord_joueur in coord_visible.keys()
            
        