from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt,QTimer,pyqtSignal,QObject,QUrl
from Modèle.Joueur import Joueur
from Modèle import MonstreSonore
from Vue.Vue import Vue
from Modèle import MonstreVision
from Modèle.BDD.Repositorie.ScoreRepo import ScoreRepo
import time,random



class Jeu(QObject):
    
    victoire = pyqtSignal()
    defaite = pyqtSignal()
    
    def __init__(self,vue : Vue,joueur : Joueur,MonstreVisuel : MonstreVision,MonstreSon : MonstreSonore,on_defaite,score: ScoreRepo,mode : str):
        super().__init__()
        self.vue : Vue = vue
        self.joueur : Joueur = joueur
        self.monstre_vision : MonstreVision = MonstreVisuel
        self.monstre_sonore : MonstreSonore = MonstreSon
        self.timer_deplacement = QTimer()
        self.timer_deplacement_vision = QTimer()
        
        self.dernier_deplacement = time.time()
        self.coord_j_actuel : tuple = self.joueur.get_coord()
        self.on_defaite = on_defaite
        self.score = score
        self.mode = mode
        
        """SONS DES DIFFERENTS MOBS (PAS, CRI)"""
        
        self.sound_pas = QSoundEffect()
        self.sound_pas.setSource(QUrl.fromLocalFile("assets/son/pas_beton.wav"))
        self.sound_pas.setVolume(0.2)
        
        """SIGNAUX"""
        
        self.timer_deplacement_vision.timeout.connect(self.deplacement_monstre_vision)
        self.timer_deplacement.timeout.connect(self.deplacement_monstre_sonore) 
        
    def condition_victoire(self,timer)-> bool:
        
        if self.joueur.get_coord() == self.vue.labyrinthe.get("end"):
            self.timer_deplacement.stop()
            self.timer_deplacement_vision.stop()
            if self.mode != "lore":
                self.score.CreateScore(self.joueur.get_nom(),self.vue.temps-self.vue.temps_restant,self.vue.labyrinthe.get("dimension")[0],self.vue.temps_restant*10-(self.vue.temps-self.vue.temps_restant*10%10)) 
            self.victoire.emit()
            return True
        return False
    def condition_defaite(self):
        if self.joueur.get_coord()[0] == self.monstre_sonore.get_coord()[0] and self.joueur.get_coord()[1] == self.monstre_sonore.get_coord()[1]:
            self.timer_deplacement.stop()
            self.timer_deplacement_vision.stop()
            self.defaite.emit()
            self.on_defaite()
        elif self.joueur.get_coord()[0] == self.monstre_vision.get_coord()[0] and self.joueur.get_coord()[1] == self.monstre_vision.get_coord()[1]:
            self.timer_deplacement.stop()
            self.timer_deplacement_vision.stop()
            self.defaite.emit()
            self.on_defaite()
        return False
    def deplacer_joueur(self,touche):
            
        fleche = [Qt.Key.Key_Up,Qt.Key.Key_Down,Qt.Key.Key_Right,Qt.Key.Key_Left]
        if touche not in fleche:
            touche = chr(touche)
        if touche == self.joueur.get_commande("avancer") or touche == Qt.Key.Key_Up:
            coord_joueur = self.joueur.get_coord()
            coord_direction = (coord_joueur[0]-1,coord_joueur[1])
            if self.vue.labyrinthe.can_moove(coord_joueur,coord_direction):
                if (time.time()-self.dernier_deplacement) >0.28:
                        self.dernier_deplacement = time.time()
                        self.vue.cases_visibles = self.vue.labyrinthe.get_cases_visibles(coord_direction,3)
                        self.joueur.set_coord(coord_direction)
                        self.sound_pas.play()
                
        elif touche == self.joueur.get_commande("reculer") or touche == Qt.Key.Key_Down:
            coord_joueur = self.joueur.get_coord()
            coord_direction = (coord_joueur[0]+1,coord_joueur[1])
            if self.vue.labyrinthe.can_moove(coord_joueur,coord_direction):
                if (time.time()-self.dernier_deplacement) >0.28:
                        self.dernier_deplacement = time.time()
                        self.vue.cases_visibles = self.vue.labyrinthe.get_cases_visibles(coord_direction,3)
                        self.joueur.set_coord(coord_direction)
                        self.sound_pas.play()
                
        elif touche == self.joueur.get_commande("droite") or touche == Qt.Key.Key_Right :
            coord_joueur = self.joueur.get_coord()
            coord_direction = (coord_joueur[0],coord_joueur[1]+1)
            if self.vue.labyrinthe.can_moove(coord_joueur,coord_direction):
                if (time.time()-self.dernier_deplacement) >0.28:
                        self.dernier_deplacement = time.time()
                        self.vue.cases_visibles = self.vue.labyrinthe.get_cases_visibles(coord_direction,3)
                        self.joueur.set_coord(coord_direction)
                        self.sound_pas.play()
                
        elif touche == self.joueur.get_commande("gauche") or touche == Qt.Key.Key_Left:
            coord_joueur = self.joueur.get_coord()
            coord_direction = (coord_joueur[0],coord_joueur[1]-1)
            if self.vue.labyrinthe.can_moove(coord_joueur,coord_direction):
                if (time.time()-self.dernier_deplacement) >0.28:
                        self.dernier_deplacement = time.time()
                        self.vue.cases_visibles = self.vue.labyrinthe.get_cases_visibles(coord_direction,3)
                        self.joueur.set_coord(coord_direction)
                        self.sound_pas.play()
        
        if self.condition_victoire(self.vue.temps_restant):
            return
        self.vue.update()
        
    def timer_moove(self):
        self.timer_deplacement.start(1000)
        self.timer_deplacement_vision.start(1000)
        
    def deplacement_monstre_sonore(self):
        """Deplacement monstre sonore"""
        if self.monstre_sonore.bruit_entendu(self.joueur.get_coord()):
            self.monstre_sonore.set_etat("Alerte")
            self.timer_deplacement.stop()
            self.timer_deplacement.start(250)
            self.monstre_sonore.set_coord_visible(self.joueur.get_coord())
            
        else :
            if not self.monstre_sonore.get_deplacement():
                self.timer_deplacement.stop()
                self.timer_deplacement.start(500)
                etat_possible : list = ["Balade","Arret"]
                self.monstre_sonore.set_etat(random.choice(etat_possible))
                
        if self.monstre_sonore.get_etat() == "Balade":
            
            if not self.monstre_sonore.get_deplacement():
                deplacement : list  = self.vue.labyrinthe.deplacement_aléatoire_monstre(self.monstre_sonore.get_coord())
                self.monstre_sonore.set_deplacement(deplacement)
                self.coord_j_actuel = self.joueur.get_coord()
                
            else:
                self.monstre_sonore.set_coord(self.monstre_sonore.avance())
                self.condition_defaite()
                
                
        elif self.monstre_sonore.get_etat() == "Alerte":
            if self.joueur.get_coord() != self.coord_j_actuel:
                self.monstre_sonore.set_deplacement(self.vue.labyrinthe.bfs_monstre(self.monstre_sonore.get_coord(),self.monstre_sonore.get_coord_visible()))
                self.coord_j_actuel = self.joueur.get_coord()
                
            if self.monstre_sonore.get_deplacement():
                self.monstre_sonore.set_coord(self.monstre_sonore.avance())
                self.condition_defaite()
                
            else:
                if self.monstre_sonore.get_coord() != self.monstre_sonore.get_coord_visible():
                    self.monstre_sonore.set_deplacement(self.vue.labyrinthe.bfs_monstre(self.monstre_sonore.get_coord(),self.monstre_sonore.get_coord_visible()))
        
                else :
                    self.monstre_sonore.set_etat("Arret")
        else : 
            self.monstre_sonore.set_coord(self.monstre_sonore.get_coord())
            
        """Deplacement monstr vision"""
    def deplacement_monstre_vision(self):
        if self.monstre_vision.joueur_est_visible(self.vue.labyrinthe.get_cases_visibles(self.monstre_vision.get_coord(),6),self.joueur.get_coord()):
            self.monstre_vision.set_etat("Alerte")
            self.timer_deplacement_vision.stop()
            self.timer_deplacement_vision.start(250)
            self.monstre_vision.set_coord_visible(self.joueur.get_coord())
            self.monstre_vision.set_deplacement(self.vue.labyrinthe.bfs_monstre(self.monstre_vision.get_coord(),self.monstre_vision.get_coord_visible()))
            
        else :
            if not self.monstre_vision.get_deplacement():
                self.timer_deplacement_vision.stop()
                self.timer_deplacement_vision.start(500)
                etat_possible : list = ["Balade","Arret"]
                self.monstre_vision.set_etat(random.choice(etat_possible))
                
        if self.monstre_vision.get_etat() == "Balade":
            
            if not self.monstre_vision.get_deplacement():
                deplacement : list  = self.vue.labyrinthe.deplacement_aléatoire_monstre(self.monstre_vision.get_coord())
                self.monstre_vision.set_deplacement(deplacement)
                
            else:
                self.monstre_vision.set_coord(self.monstre_vision.avance())
                self.condition_defaite()
                
        elif self.monstre_vision.get_etat() == "Alerte":
            
            if self.monstre_vision.get_deplacement():
                self.monstre_vision.set_coord(self.monstre_vision.avance())
                self.condition_defaite()
                
            else:
                if self.monstre_vision.get_coord() != self.monstre_vision.get_coord_visible():
                    self.monstre_vision.set_deplacement(self.vue.labyrinthe.bfs_monstre(self.monstre_vision.get_coord(),self.monstre_vision.get_coord_visible()))
                else :
                    self.monstre_vision.set_etat("Arret")
        else : 
            self.monstre_vision.set_coord(self.monstre_vision.get_coord())
            self.condition_defaite()