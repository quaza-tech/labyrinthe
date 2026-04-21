from collections import deque

class Monstre:
    def __init__(self,start : tuple,img : str):
        self.coord : tuple = start
        self.start : tuple = start
        self.design : str = img
        self.etat : str = "Balade"
        self.deplacement  = deque([]) 
        self.vitesse : float = 0.25
        self.coord_visible : tuple = ()
    
    def get_coord(self) -> tuple:
        return self.coord

    def get_design(self) -> str:
        return self.design
    
    def get_etat(self) -> str:
        return self.etat
    
    def get_deplacement(self):
        return self.deplacement
    
    def get_vitesse(self) -> float:
        return self.vitesse
    
    def get_coord_visible(self)  -> tuple:
        return self.coord_visible
    
    def set_coord(self,coord : tuple):
        self.coord = (coord[0],coord[1])

    def set_design(self,design : str):
        self.design = design
    
    def set_etat(self,etat : str):
        self.etat = etat
    
    def set_deplacement(self,liste : list):
        self.deplacement = deque(liste)
    
    def set_vitesse(self,vitesse : float):
        self.vitesse = vitesse
    
    def set_coord_visible(self,coord : tuple):
        self.coord_visible = (coord[0],coord[1])
        
    def avance (self)->tuple:
        if self.get_deplacement():
            avance : tuple = self.deplacement.popleft()
            return avance
    
    def reset(self):
        self.coord = self.start
        self.deplacement = deque([])
        self.coord_visible = ()
        self.etat = "Balade"