import sqlite3,os


class Audio():
    def __init__(self):
        self.id : int
        self.id_joueur : int
        self.libelle : str
        self.volume : str
    
    def get_id(self) -> int:
        return self.id
    
    def get_id_joueur(self) -> int:
        return self.id_joueur
    
    def get_libelle(self) -> int:
        return self.libelle
    
    def get_touche_assigne(self) -> str:
        return self.touche_assigne
    
    def set_id(self,id):
        self.id = id
        
    def set_id_joueur(self,id):
        self.id_joueur = id
        
    def set_libelle(self,libelle):
        self.libelle = libelle
        
    def set_touche_assigne(self,volume):
        self.touche_assigne = volume
