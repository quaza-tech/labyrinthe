from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QStackedWidget,QVBoxLayout,QPushButton
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtGui import QGuiApplication,QPainter, QPen, QColor, QBrush
from Controleur.Joueur import Joueur
from Controleur.Jeu import Jeu
from Modèle.Labyrinthe import labyrinthe
from Vue.Vue import Vue
from Controleur.Parametre import Parametre
from Controleur.MonstreSonore import MonstreSonore
from Controleur.MonstreVision import MonstreVision
from Controleur.Scène.Menu import Menu
from Modèle.ScoreManager import SQLite
from Controleur.Scène.Login import login
from Modèle.BDD.Repositorie.JoueurRepo import JoueurRepo
from Modèle.BDD.Repositorie.ScoreRepo import ScoreRepo
from Modèle.BDD.Repositorie.ToucheRepo import ToucheRepo
import sys
import time

class SceneManager:
    def __init__(self,dimension : tuple):
        
        """INSTANCIATION DU LABYRINTHE"""
        start = (0,0)
        end = (dimension[0]-1,dimension[1]-1)
        self.labyrinthe = labyrinthe(dimension,start,end)
        self.labyrinthe.set_labyrinthe(4)
        self.labyrinthe.create_way()

        """INSTANCIATION DES DIFFERENTS MOB"""
        self.joueur = Joueur((0,0),"#FFFFFF","")
        self.monstre_sonore : MonstreSonore = MonstreSonore((18,19),"test")
        self.monstre_vision  : MonstreVision = MonstreVision((10,10),"test")
        
        """INSTANCIATION DES LOGIQUES DE VUE BDD ET JEU"""
        self.login = login()
        self.joueurRepo,self.ScoreRepo = JoueurRepo(),ScoreRepo() ; self.ToucheRepo = ToucheRepo()
        self.vue = Vue(self.labyrinthe,self.joueur)
        self.jeu = Jeu(self.vue,self.joueur,self.monstre_vision,self.monstre_sonore,self.retour_menu,self.ScoreRepo,None)
        self.vue.jeu = self.jeu
        self.vue.setup_signaux()
        
        
        self.stack = QStackedWidget()
        self.menu = Menu()
            
        
        
        """Gestion des cliques"""
        self.menu.button_continue.clicked.connect(lambda: self.start_game("speedrun"))
        self.menu.button_start.clicked.connect(lambda: self.start_game("lore"))
        self.menu.button_Parameter.clicked.connect(self.parametre)
        self.menu.button_leave.clicked.connect(self.leave)
        self.login.envoie_donnee.connect(self.verifier_login)
        
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.vue)
        Widgetparent = QWidget()
        layoutparent = QVBoxLayout()
        self.button_retour = QPushButton("RETOUR")
        layoutparent.addWidget(self.button_retour)
        self.parametres = Parametre(self.joueur)
        layoutparent.addWidget(self.parametres)
        Widgetparent.setLayout(layoutparent)
        self.stack.addWidget(Widgetparent)
        new_width = QGuiApplication.primaryScreen().size().width()-100
        new_height =  QGuiApplication.primaryScreen().size().height()-100
        self.stack.resize(new_width, new_height)
        self.stack.show()
        
        self.button_retour.clicked.connect(self.retour)
        self.vue.tableau.retourMenu.connect(self.retour_menu)
        self.parametres.touche_assign.connect(self.sauvegarder_touche)

    def start_game(self,mode : str):
        match mode:
            case "lore":
                self.stack.setCurrentIndex(2)
                self.vue.timer_fps.start(16)
                self.jeu.mode = mode
                self.jeu.timer_moove()
            case "speedrun":
                self.stack.setCurrentIndex(2)
                self.vue.start_timer()
                self.vue.timer_fps.start(16)
                self.jeu.timer_moove()
    def parametre(self):
        self.stack.setCurrentIndex(3)
    def retour(self):
        self.stack.setCurrentIndex(1)
    def leave(self):
        self.stack.close()
    def retour_menu(self):
        self.stack.setCurrentIndex(1)
        self.vue.timer.stop()
        self.vue.timer_fps.stop()
        self.jeu.timer_deplacement.stop()
        self.jeu.timer_deplacement_vision.stop()
        self.jeu.monstre_vision.reset()
        self.jeu.monstre_sonore.reset()
        self.jeu.joueur.reset()
        self.vue.reset()
    
    def setup_touche(self,pseudo):
        reponse = self.ToucheRepo.getToucheBypseudo(pseudo)
        if reponse[0] != False:
            for elt in reponse[1]:
                self.joueur.set_commande(elt[0],elt[1])
        
    def verifier_login(self, email, mdp,pseudo):
        if pseudo =="":
            reponse = self.joueurRepo.getByEmailAndPassword(email,mdp)
        else :
            reponse = self.joueurRepo.create(email,mdp,pseudo)
        if reponse[0] != True:
            self.login.messageERR(reponse[1])
        else:
            self.menu.setPseudo(reponse[1][0][1])
            self.joueur.set_nom(reponse[1][0][1])
            self.setup_touche(reponse[1][0][1])
            self.parametres.setup_commande_tab()
            
            self.stack.setCurrentIndex(1)
    def ajout_donnee_score(self,id_joueur : int):
        ajout = self.db.get_score(id_joueur)
    
    def sauvegarder_touche(self,assignation):
        self.ToucheRepo.UpdateAssignation(assignation[0],assignation[1],self.joueur.get_nom())
        
    
        