import sqlite3,os


class Score():
    def __init__(self):
        self.id : int
        self.id_joueur : int
        self.temps : int
        self.diff : str
        self.score : int
    
    def get_id(self) -> int:
        return self.id
    
    def get_id_joueur(self) -> int:
        return self.id_joueur
    
    def get_temps(self) -> int:
        return self.temps
    
    def get_difficulté(self) -> str:
        return self.diff
    
    def get_score(self) -> int:
        return self.score
    
    def set_id(self,id):
        self.id = id
        
    def set_id_joueur(self,id):
        self.id_joueur = id
        
    def set_temps(self,temps):
        self.temps = temps
        
    def set_difficulté(self,diff):
        self.diff = diff
        
    def set_score(self,score):
        self.score = score