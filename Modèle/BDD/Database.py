import sqlite3,os

class DB():
    def __init__(self,fichierDB : str):
        self.nom_bdd = fichierDB
        os.makedirs("data", exist_ok=True)
        self.con = sqlite3.connect("data/"+fichierDB)
        
        self.cur = self.con.cursor()
        
        """VERIFIE L'EXISTENCE DES TABLES NEEDED """
        self.cur.execute("CREATE TABLE IF NOT EXISTS joueur(id_j INTEGER PRIMARY KEY AUTOINCREMENT ,pseudo TEXT,email TEXT,mdp TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Score(id INTEGER PRIMARY KEY AUTOINCREMENT,pseudo TEXT,temps INTEGER ,difficulté TEXT,score INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Touche(id INTEGER PRIMARY KEY AUTOINCREMENT,libelle TEXT,touche_assigne CHAR,pseudo TEXT)")
    def endSession(self):
        self.con.close()