from PyQt6.QtCore import QTimer,pyqtSignal,QObject,Qt
from Modèle.Joueur import Joueur
from Modèle import MonstreSonore
from Vue.Vue import Vue
from Modèle import MonstreVision
from Modèle.BDD.Repositorie.ScoreRepo import ScoreRepo
import time,random
from PyQt6.QtGui import QKeySequence
from Modèle.Dynamite import Dynamite



class Jeu(QObject):
    
    victoire = pyqtSignal()
    defaite = pyqtSignal()
    
    def __init__(self,vue : Vue,joueur : Joueur,MonstreVisuel : MonstreVision,MonstreSon : MonstreSonore,on_defaite,score: ScoreRepo,mode : str, Sound):
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
        self.last_moove : str = None
        self.timer = QTimer()
        
        """Lien avec le joueur"""
        self.liste_touche : dict = {self.joueur.get_commande("avancer") : (-1,0,"Nord"),self.joueur.get_commande("reculer") : (1,0,"Sud"),self.joueur.get_commande("droite") : (0,1,"Est") ,self.joueur.get_commande("gauche") :(0,-1,"Ouest")}
        """SONS DES DIFFERENTS MOBS (PAS, CRI)"""
        
        self.son = Sound
        self.liste_bruit : list = []
        
        """SIGNAUX"""
        
        self.timer_deplacement_vision.timeout.connect(self.deplacement_monstre_vision)
        self.timer_deplacement.timeout.connect(self.deplacement_monstre_sonore) 
        self.vue.UIingame.minuteur.temps.connect(self.explosion)
        
    def update_touche(self):
        self.liste_touche : dict = {self.joueur.get_commande("avancer") : (-1,0,"Nord"),self.joueur.get_commande("reculer") : (1,0,"Sud"),self.joueur.get_commande("droite") : (0,1,"Est") ,self.joueur.get_commande("gauche") :(0,-1,"Ouest")}
    def condition_victoire(self,timer)-> bool:
        
        if self.joueur.get_coord() == self.vue.labyrinthe.get("end"):
            self.timer_deplacement.stop()
            self.timer_deplacement_vision.stop()
            if self.mode != "lore":
                self.score.CreateScore(self.joueur.get_nom(),self.vue.temps-self.vue.temps_restant,self.vue.labyrinthe.get("dimension")[0],self.vue.temps_restant*10-(self.vue.temps-self.vue.temps_restant*10%10)) 
            self.victoire.emit()
            self.joueur.set_freeze(True)
            return True
        return False
    def condition_defaite(self):
        if (self.joueur.get_coord()[0] == self.monstre_sonore.get_coord()[0] and self.joueur.get_coord()[1] == self.monstre_sonore.get_coord()[1]) or (self.joueur.get_coord()[0] == self.monstre_vision.get_coord()[0] and self.joueur.get_coord()[1] == self.monstre_vision.get_coord()[1]):
            self.timer_deplacement.stop()
            self.timer_deplacement_vision.stop()
            self.defaite.emit()
            self.on_defaite()
        elif self.vue.UIingame.getValuesBarre("nourriture") == 0 or self.vue.UIingame.getValuesBarre("water") == 0:
            self.timer_deplacement.stop()
            self.timer_deplacement_vision.stop()
            self.defaite.emit()
            self.on_defaite()
        return False
    
    def prendre_item(self,item : tuple,case : tuple):
        self.vue.UIingame.updateItem(item[0],item[1])
        self.vue.labyrinthe.labyrinthe[case].set_item(("",""))
    
    def utiliser_item(self,touche):
        touche = "Left" if touche == Qt.MouseButton.LeftButton else "Right"
        if touche  == self.joueur.get_commande("utiliser"):
            item = self.vue.UIingame.WhichSelected()
            match item[0]:
                case "meat":
                    self.vue.UIingame.SetNewValuesBarre({"meat" : 300})
                    self.vue.UIingame.updateItem("meat",-1)
                case "water":
                    self.vue.UIingame.SetNewValuesBarre({"water" : 200})
                    self.vue.UIingame.updateItem("water",-1)
                case "barre_energisante":
                    self.vue.UIingame.SetNewValuesBarre({"stamina" : 300, "meat" : 150})
                    self.vue.UIingame.updateItem("barre_energisante",-1)
                case "dynamite":
                    if self.last_moove in self.vue.labyrinthe.murs_cassable(self.coord_j_actuel):
                        self.joueur.set_freeze(True)
                        self.vue.UIingame.MinuteurVisibility(True)
                        
    def explosion(self,valeur):
        
        self.vue.UIingame.MinuteurVisibility(False)
        self.vue.UIingame.updateItem("dynamite",-1)
        self.dynamite = Dynamite(self.joueur.get_coord(),self.last_moove,"en cours",valeur)
        print(self.dynamite.get("coord"))
        self.joueur.set_freeze(False)
        self.timer.timeout.connect(self.update_minuteur) 
        self.timer.start(1000)
        
        
    def update_minuteur(self):
        if self.dynamite.get("temps")-1 > 0:
            self.dynamite.set("temps",1)
        else:
            self.timer.stop()
            chemin  : list = self.vue.labyrinthe.bfs_monstre(self.dynamite.get("coord"),self.joueur.get_coord())
            print(len(chemin))
            if len(chemin) >= 8:
                self.son.play("explosion_lointaine","effets")
            else:
                self.son.play("explosion","effets")
            if self.dynamite.get("coord") not in self.vue.cases_visibles:
                self.liste_bruit.append((self.dynamite.get("coord"),3.3,time.time()))
                self.vue.start_timer_shake()
                self.vue.labyrinthe.destruction(self.dynamite.get("direction"),self.dynamite.get("coord"))
            else :
                self.vue.UIingame.SetNewValuesBarre({"meat" : -1000})
                self.condition_defaite()
            self.vue.update()
            
    def deplacer_joueur(self,touche):
        
        if self.joueur.get_commande("freeze"):
            return True
        
        dico_slot = self.joueur.get_slots_dico()
        touche = QKeySequence(touche).toString()
        
        if self.joueur.is_accroupi() and self.vue.UIingame.getValuesBarre("stamina") > 0 :
            timelaps = 1
        elif self.joueur.is_sprint() and self.vue.UIingame.getValuesBarre("stamina") > 0 : 
             timelaps = 0.10
        else :
            self.joueur.set_accroupi(False)
            self.joueur.set_sprint(False)
            timelaps = 0.50
             
        if self.joueur.get_commande("accroupi") == touche:
            if self.joueur.is_accroupi():
                self.joueur.set_accroupi(False)
            else:
                if self.vue.UIingame.getValuesBarre("stamina") > 0:
                    self.joueur.set_accroupi(True)
                    self.joueur.set_sprint(False)
                    
        elif self.joueur.get_commande("sprint") == touche:
            if self.joueur.is_sprint():
                self.joueur.set_sprint(False)
            else:
                if self.vue.UIingame.getValuesBarre("stamina") > 0:
                    self.joueur.set_sprint(True)
                    self.joueur.set_accroupi(False)
                    
        elif touche in dico_slot.values():
            keys = [k for k, v in dico_slot.items() if v == touche]        #on cherche la clé associé a la touche pour savoir quelle est le slot selectionné
            self.vue.UIingame.selection(keys[0])
        
        elif touche == self.joueur.get_commande("prendre"):
            item = self.vue.labyrinthe.labyrinthe[self.joueur.get_coord()].get_item()
            if item != None:
                self.prendre_item(item,self.joueur.get_coord())
            
        elif touche in self.liste_touche:
            coord_direction = (self.joueur.get_x()+self.liste_touche[touche][0],self.joueur.get_y()+self.liste_touche[touche][1])
            self.last_moove = self.liste_touche[touche][2]
            if self.vue.labyrinthe.can_moove(self.joueur.get_coord(),coord_direction):
                if (time.time()-self.dernier_deplacement) > timelaps:
                    self.dernier_deplacement = time.time()
                    self.vue.cases_visibles = self.vue.labyrinthe.get_cases_visibles(coord_direction,3)
                    self.joueur.set_coord(coord_direction)
                    self.son.play("step","effets")
                    self.liste_bruit.append((coord_direction,0.5 if self.joueur.is_accroupi() else (1.5 if self.joueur.is_sprint() else 1),time.time()))
                    self.vue.UIingame.SetNewValuesBarre({"water" : -5,"meat" : -2})
                    if self.joueur.is_accroupi():
                        self.vue.UIingame.SetNewValuesBarre({"stamina" : -50})
                    elif self.joueur.is_sprint():
                        self.vue.UIingame.SetNewValuesBarre({"stamina" : -75})
                    
                        
        if self.condition_victoire(self.vue.temps_restant):
            return
        
        self.vue.update()
        
    def timer_moove(self):
        self.timer_deplacement.start(1000)
        self.timer_deplacement_vision.start(1000)
        
    def bruit_pertinence(self):
        for elt in self.liste_bruit:
            if (time.time()-elt[2]) > 3:
                self.liste_bruit.remove(elt)
        pertinence = 0
        element_pertinent : int = None
        for elt in self.liste_bruit:
            
            x = len(self.vue.labyrinthe.bfs_monstre(self.monstre_sonore.get_coord(),elt[0]))
            y = elt[1]
            f = y / (1+2*x)
            if f > pertinence:
                pertinence = f
                element_pertinent = (x,elt[0],pertinence)
        
        return element_pertinent
                
    def deplacement_monstre_sonore(self):
        """Deplacement monstre sonore"""
        if not self.joueur.is_accroupi() and self.vue.UIingame.getValuesBarre("stamina") == 1000 or not self.joueur.is_sprint() and self.vue.UIingame.getValuesBarre("stamina") == 1000 :
            self.vue.UIingame.SetStaminaVisibility(False)
        else:
            self.vue.UIingame.SetStaminaVisibility(True)
            if self.vue.UIingame.getValuesBarre("stamina") != 1000 and not self.joueur.is_accroupi() and not self.joueur.is_sprint():
                self.vue.UIingame.SetNewValuesBarre({"stamina" : 50})
                
        if self.liste_bruit != []:
            bruit = self.bruit_pertinence()
            if bruit:
                if self.monstre_sonore.bruit_entendu(bruit[2]):
                    self.monstre_sonore.set_etat("Alerte")
                    self.timer_deplacement.stop()
                    self.timer_deplacement.start(250)
                    self.monstre_sonore.set_coord_visible(bruit[1])
            
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