import sqlite3,hashlib

class Joueur():
    def __init__(self):
        
        self.nom : str
        self.email : str
        self.mdp : str
        self.avatars : str
        
    def get_nom(self) -> str:
        return self.nom
    
    def set_nom(self,pseudo):
        self.nom = pseudo
    
    def get_email(self) -> str:
        return self.email
    
    def set_email(self,email):
        self.email = email
        
    def get_mdp(self) ->str:
        return self.mdp
    
    def set_mdp(self,mdp) -> str:
        self.mdp = hashlib.sha256(mdp.encode()).hexdigest()
    
    def get_avatars(self) ->str:
        return self.avatars
    
    def set_avatars(self,avatar):
        self.avatars = avatar
        