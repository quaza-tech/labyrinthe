import sqlite3,os,hashlib
from Modèle.BDD.Modèle.Audio import Audio
from Modèle.BDD.Database import DB

class audioRepo(Audio):
    def __init__(self):
        super().__init__()
        
        self.db = DB("Echo_du_silence.db")
        
    def getVolumeBypseudo(self,pseudo) -> tuple:
        self.db.cur.execute("SELECT libelle,volume from audio WHERE pseudo = ?",(pseudo,))
        data = self.db.cur.fetchall()
        if data :
            return(True,data)
        return (False,"ERR 404 : not found")
    
    def getVolumeSpeByIdJoueur(self,libelle,pseudo) -> tuple:
        self.db.cur.execute("SELECT libelle,volume from audio WHERE pseudo = ? and libelle = ?",(pseudo,libelle))
        data = self.db.cur.fetchall()
        if data :
            return(True,data)
        return (False,"ERR 404 : not found")
    
    def getSonBylibelle(self,pseudo,libelle) -> tuple:
        self.db.cur.execute("SELECT libelle,volume from audio WHERE libelle = ? and pseudo = ?",(libelle,pseudo))
        data = self.db.cur.fetchall()
        if data :
            return(True,data)
        return (False,"ERR 404 : not found")
    
    def CreateSon(self,libelle,volume,pseudo) ->tuple:
        self.db.cur.execute("INSERT INTO audio(libelle,volume,pseudo) VALUES(?,?,?)",(libelle,volume,pseudo))
        self.db.con.commit()
        return (True,None)
    
    def UpdateVolume(self,libelle,volume,pseudo)->tuple:
        self.db.cur.execute("SELECT * FROM audio WHERE libelle = ? and pseudo = ?",(libelle,pseudo))
        data = self.db.cur.fetchall()
        if data:
            print(data)
            self.db.cur.execute("UPDATE audio SET volume = ? WHERE libelle = ? and pseudo = ?",(volume,libelle,pseudo))
            self.db.con.commit()
            return (True,None)
        else : 
            self.CreateAssignation(libelle,volume,pseudo)
