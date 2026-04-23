import sqlite3,os,hashlib
from Modèle.BDD.Modèle.Joueur import Joueur
from Modèle.BDD.Database import DB

class JoueurRepo(Joueur):
    def __init__(self):
        super().__init__()
        
        self.db = DB("Echo_du_silence.db")
        
    def getById(self,id_joueur)-> tuple:
        self.db.cur.execute("SELECT email,pseudo FROM joueur WHERE id =  ?",(id_joueur))
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    def getByEmail(self,email) -> tuple:
        self.db.cur.execute("SELECT email,pseudo FROM joueur WHERE email =  ?",(email))
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    def getByEmailAndPassword(self,email,mdp) -> tuple:
        self.db.cur.execute("SELECT email,pseudo FROM joueur WHERE email =  ? and mdp = ?",(email,hashlib.sha256(mdp.encode()).hexdigest()))
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    def existByEmailOrName (self,email,pseudo) ->tuple:
        self.db.cur.execute("SELECT email,pseudo FROM joueur WHERE email =  ? or pseudo = ?",(email,pseudo))
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    def create(self,email,mdp,pseudo) -> tuple:
        if self.existByEmailOrName(email,pseudo)[0]:
            return (False,"ERR : UserAccountAlreadyExist")
        else : 
            self.db.cur.execute("INSERT INTO joueur(pseudo,email,mdp) VALUES(?,?,?)",(pseudo,email,hashlib.sha256(mdp.encode()).hexdigest()))
            self.db.con.commit()
            return (True,"201 : Compte crée avec succès !")
    def delete(self,email,pseudo,mdp) ->tuple:
        if self.existByEmailOrName(email,pseudo)[0]:
            self.db.cur.execute("DELETE FROM joueur WHERE email = ? and pseudo = ? and mdp = ?",(email,pseudo,hashlib.sha256(mdp.encode()).hexdigest()))
            self.db.con.commit()
            return (True,"204 : Delete with success ! ")
        