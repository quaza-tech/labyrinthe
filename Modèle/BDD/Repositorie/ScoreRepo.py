import sqlite3,os,hashlib
from Modèle.BDD.Modèle.Score import Score
from Modèle.BDD.Database import DB

class ScoreRepo(Score):
    def __init__(self):
        super().__init__()
        
        self.db = DB("Echo_du_silence.db")
        
    def getAllScore(self) ->tuple:
        self.db.cur.execute("SELECT * FROM Score")
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    
    def getScoreByIdJoueur(self,id_joueur) ->tuple:
        self.db.cur.execute("SELECT * FROM score WHERE pseudo = (SELECT pseudo FROM joueur WHERE id_joueur = ?)",(id_joueur))
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    def getScoreByPseudo(self,pseudo) ->tuple:
        self.db.cur.execute("SELECT * FROM socre WHERE pseudo = ?",(pseudo))
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    def getAllScoreDESC(self):
        self.db.cur.execute("SELECT pseudo,temps,difficulté,score FROM score ORDER BY score DESC")
        data = self.db.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : not found")
    def CreateScore(self,pseudo : str,temps : int,diff : int,score : int)->tuple:
        if diff < 10:
            diff : str = "Easy"
        elif diff < 30:
            diff : str = "Meduim"
        else :
            diff : str = "Hardcore"
        self.db.cur.execute("INSERT INTO SCORE(pseudo,temps,difficulté,score) VALUES(?,?,?,?)",(pseudo,temps,diff,score))
        self.db.con.commit()
    def deleteAllScore(self):
        self.db.cur.execute("DELETE FROM score")
        self.db.con.commit()