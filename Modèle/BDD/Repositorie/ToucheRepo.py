import sqlite3,os,hashlib
from Modèle.BDD.Modèle.Touche import Touche
from Modèle.BDD.Database import DB

class ToucheRepo(Touche):
    def __init__(self):
        super().__init__()
        
        self.db = DB("Echo_du_silence.db")
        
    def getToucheBypseudo(self,pseudo) -> tuple:
        self.db.cur.execute("SELECT libelle,touche_assigne from touche WHERE pseudo = ?",(pseudo,))
        data = self.db.cur.fetchall()
        if data :
            return(True,data)
        return (False,"ERR 404 : not found")
    
    def getSpeToucheByIdJoueur(self,libelle,pseudo) -> tuple:
        self.db.cur.execute("SELECT libelle,touche_assigne from touche WHERE pseudo = ? and libelle = ?",(pseudo,libelle))
        data = self.db.cur.fetchall()
        if data :
            return(True,data)
        return (False,"ERR 404 : not found")
    
    def getToucheByAssignation(self,pseudo,assignation) -> tuple:
        self.db.cur.execute("SELECT libelle,touche_assigne from touche WHERE touche_assigne = ? and pseudo = ?",(assignation,pseudo))
        data = self.db.cur.fetchall()
        if data :
            return(True,data)
        return (False,"ERR 404 : not found")
    
    def CreateAssignation(self,libelle,assignation,pseudo) ->tuple:
        self.db.cur.execute("INSERT INTO touche(libelle,touche_assigne,pseudo) VALUES(?,?,?)",(libelle,assignation,pseudo))
        self.db.con.commit()
        return (True,None)
    
    def UpdateAssignation(self,libelle,assignation,pseudo)->tuple:
        self.db.cur.execute("SELECT * FROM touche WHERE libelle = ? and pseudo = ?",(libelle,pseudo))
        data = self.db.cur.fetchall()
        if data:
            print(data)
            self.db.cur.execute("UPDATE touche SET touche_assigne = ? WHERE libelle = ? and pseudo = ?",(assignation,libelle,pseudo))
            self.db.con.commit()
            return (True,None)
        else : 
            self.CreateAssignation(libelle,assignation,pseudo)
