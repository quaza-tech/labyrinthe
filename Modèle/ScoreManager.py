import sqlite3,os,hashlib


class SQLite():
    def __init__(self,fichierDB : str):
        self.nom_bdd = fichierDB
        os.makedirs("data", exist_ok=True)
        self.con = sqlite3.connect("data/"+fichierDB)
        
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS joueur(id_j INTEGER PRIMARY KEY AUTOINCREMENT ,pseudo TEXT,email TEXT,mdp TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Score(id INTEGER PRIMARY KEY AUTOINCREMENT,id_joueur TEXT,temps INTEGER ,difficulté TEXT,score INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Touche(id INTEGER PRIMARY KEY AUTOINCREMENT,libelle TEXT,touche_assigne CHAR,id_joueur INTEGER)")
        
    def createAccount(self,donne : tuple):
        self.cur.execute("SELECT * FROM joueur WHERE email = ? or pseudo = ?",(donne[0],donne[1]))
        if not self.cur.fetchall():
            self.cur.execute("INSERT INTO joueur(pseudo,email,mdp) VALUES(?,?,?)",(donne[1],donne[0],hashlib.sha256(donne[2].encode()).hexdigest()))
            self.con.commit()
            return (True,"Compte crée avec succès !")
        else :
            return (False,"Compte deja existant avec cet email")
    def login (self,donne:tuple):
        self.cur.execute("SELECT pseudo FROM joueur WHERE email = ? and mdp = ? ",(donne[0],hashlib.sha256(donne[1].encode()).hexdigest()))
        data = self.cur.fetchall()
        if data:
            return (True,data)
        return (False,"ERR 404 : compte inexistant avec ce mot de passe ou email")
    def insert(self,donnee : tuple):
        print(donnee)
        self.cur.execute("INSERT INTO Score (pseudo,temps,difficulté,score) VALUES (?,?,?,?)",(donnee[0],donnee[1],donnee[2],donnee[3]))
        self.con.commit()
        
    def get_score(self,id_joueur : int):
        self.cur.execute("SELECT * FROM SCORE WHERE pseudo = (SELECT pseudo FROM joueur WHERE id_j = ?)",(id_joueur,))
        return self.cur.fetchall()
    def close(self):
        self.con.close()