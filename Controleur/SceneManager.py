from PyQt6.QtWidgets import QWidget,QStackedWidget,QVBoxLayout,QPushButton
from PyQt6.QtGui import QGuiApplication
from Modèle.Joueur import Joueur
from Controleur.Jeu import Jeu
from Modèle.Labyrinthe import labyrinthe
from Vue.Vue import Vue
from Controleur.Parametre import Parametre
from Modèle.MonstreSonore import MonstreSonore
from Modèle.MonstreVision import MonstreVision
from Vue.Scène.Menu import Menu
from Vue.Scène.Login import login
from Vue.Scène.Pause import Pause
from Modèle.BDD.Repositorie.JoueurRepo import JoueurRepo
from Modèle.BDD.Repositorie.ScoreRepo import ScoreRepo
from Modèle.BDD.Repositorie.ToucheRepo import ToucheRepo
from Modèle.BDD.Repositorie.AudioRepo import audioRepo
from Services.SoundManager import SoundManager


class SceneManager:
    def __init__(self,dimension : tuple):
        
        """INSTANCIATION DU LABYRINTHE"""
        start = (0,0)
        end = (dimension[0]-1,dimension[1]-1)
        self.labyrinthe = labyrinthe(dimension,start,end)
        self.labyrinthe.set_labyrinthe(4)
        

        """INSTANCIATION DES DIFFERENTS MOB"""
        self.joueur = Joueur((0,0),"#FFFFFF","")
        self.monstre_sonore : MonstreSonore = MonstreSonore((18,19),"test")
        self.monstre_vision  : MonstreVision = MonstreVision((10,10),"test")
        
        """INSTANCIATION DES LOGIQUES DE VUE BDD ET JEU"""
        self.login = login()
        self.joueurRepo,self.ScoreRepo = JoueurRepo(),ScoreRepo() ; self.ToucheRepo,self.AudioRepo = ToucheRepo(),audioRepo()
        self.soundManager = SoundManager()
        self.Pause = Pause()
        self.vue = Vue(self.labyrinthe,self.joueur)
        self.jeu = Jeu(self.vue,self.joueur,self.monstre_vision,self.monstre_sonore,self.retour_menu,self.ScoreRepo,None,self.soundManager)
        self.vue.jeu = self.jeu
        self.vue.setup_signaux()
        
        
        self.stack = QStackedWidget()
        self.menu = Menu()
        self.parametres = Parametre(self.joueur)
            
        
        
        """Gestion des cliques"""
        self.menu.button_continue.clicked.connect(lambda: self.start_game("speedrun"))
        self.menu.button_start.clicked.connect(lambda: self.start_game("lore"))
        self.menu.button_Parameter.clicked.connect(lambda :self.parametre("menu"))
        self.menu.button_leave.clicked.connect(self.leave)
        self.login.envoie_donnee.connect(self.verifier_login)
        
        """Signaux en lien avec le son """
        self.parametres.son_generale.connect(self.sauvegarder_audio)
        self.parametres.son_musique.connect(self.sauvegarder_audio)
        self.parametres.son_effet.connect(self.sauvegarder_audio)
        self.parametres.son_ui.connect(self.sauvegarder_audio)
        self.parametres.aide_vis.connect(self.sauvegarder_audio)
        
        
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.vue)
        
        Widgetparent = QWidget()
        layoutparent = QVBoxLayout()
        self.button_retour = QPushButton("RETOUR")
        layoutparent.addWidget(self.button_retour)
        
        layoutparent.addWidget(self.parametres)
        Widgetparent.setLayout(layoutparent)
        self.stack.addWidget(Widgetparent)
        self.stack.addWidget(self.Pause)
        new_width = QGuiApplication.primaryScreen().size().width()-100
        new_height =  QGuiApplication.primaryScreen().size().height()-100
        self.stack.resize(new_width, new_height)
        self.stack.show()
        
        self.button_retour.clicked.connect(lambda : self.retour(self.contexte))
        self.vue.tableau.retourMenu.connect(self.retour_menu)
        self.parametres.touche_assign.connect(self.sauvegarder_touche)
        self.Pause.retourMenu.connect(self.retour_menu)
        self.Pause.parametres.connect(self.parametre)
        self.vue.fondMenuPause.connect(self.Menu_pause)
        self.Pause.retour_jeu.connect(self.retour_jeu)

    def start_game(self,mode : str):
        self.joueur.set_freeze(False)
        self.labyrinthe.create_way()
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
    def parametre(self,contexte):
        self.contexte = contexte
        self.stack.setCurrentIndex(3)
        
    def retour(self,scene):
        match scene:
            case "menu":
                self.stack.setCurrentIndex(1)
            case "jeu":
                self.stack.setCurrentIndex(4)
                
                
    def Menu_pause(self,fond ):
        self.joueur.set_freeze(True)
        self.jeu.timer_pause()
        self.Pause.changement_fond(fond)
        self.stack.setCurrentIndex(4)
        if self.jeu.mode != "lore":
            self.vue.timer.stop()
    
    def retour_jeu(self):
        self.jeu.update_touche()
        self.joueur.set_freeze(False)
        self.jeu.timer_moove()
        self.stack.setCurrentIndex(2)
        if self.jeu.mode != "lore":
            self.vue.start_timer()
        
    def leave(self):
        self.stack.close()
        
    def retour_menu(self):
        self.stack.setCurrentIndex(1)
        self.jeu.reset()
        self.vue.reset()
        self.labyrinthe.reset_laby()
        self.labyrinthe.set_labyrinthe(4)
        
    
    def setup_touche(self,pseudo):
        reponse = self.ToucheRepo.getToucheBypseudo(pseudo)
        if reponse[0] != False:
            for elt in reponse[1]:
                self.joueur.set_commande(elt[0],elt[1])
    
    def setup_audio(self,pseudo):
        reponse = self.AudioRepo.getSonBypseudo(pseudo)
        if reponse[0] != False:
            self.parametres.setup_audio_bdd(reponse[1])
        
    def verifier_login(self, email, mdp,pseudo):
        
        if pseudo =="":
            reponse = self.joueurRepo.getByEmailAndPassword(email,mdp)
        else :
            self.joueurRepo.create(email,mdp,pseudo)
            reponse = self.joueurRepo.getByEmailAndPassword(email,mdp)
        if reponse[0] != True:
            self.login.messageERR(reponse[1])
        else:
            self.menu.setPseudo(reponse[1][0][1])
            self.joueur.set_nom(reponse[1][0][1])
            self.setup_touche(reponse[1][0][1])
            self.setup_audio(reponse[1][0][1])
            self.jeu.update_touche()
            self.parametres.setup_commande_tab()
            
            self.stack.setCurrentIndex(1)
    def ajout_donnee_score(self,id_joueur : int):
        ajout = self.db.get_score(id_joueur)
    
    def sauvegarder_touche(self,assignation):
        self.ToucheRepo.UpdateAssignation(assignation[0],assignation[1],self.joueur.get_nom())
        self.jeu.update_touche()
    
    def sauvegarder_audio(self,assignation):
        self.AudioRepo.UpdateVolume(assignation[0],assignation[1],self.joueur.get_nom())
        if assignation[0] != "aide_visuelle":
            self.soundManager.set_volume_to(assignation)
        else:
            match assignation[1]:
                case 0:
                    self.vue.UIingame.SetProgLabyVisibility(False)
                case 1:
                    self.vue.UIingame.SetProgLabyVisibility(True)
        
    
        