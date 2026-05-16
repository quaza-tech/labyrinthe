from PyQt6.QtWidgets import QWidget,QLabel
from PyQt6.QtCore import Qt,QTimer,QPoint
from PyQt6.QtGui import QGuiApplication,QPainter, QColor,QPixmap,QTransform,QPolygon
from Vue.Scène.Victoire import Victoire
from Vue.Scène.TabScore import TabScore
from Vue.Scène.UIgame import UIinGame




class Vue(QWidget):
    def __init__(self,labyrinthe,Joueur):
        super().__init__()
        
        """CE QUI TOUCHE A LA FENETRE"""
        self.new_width = QGuiApplication.primaryScreen().size().width()-100
        self.new_height =  QGuiApplication.primaryScreen().size().height()-100
        self.resize(self.new_width, self.new_height)
        self.setWindowTitle("Labyrinthe")
        self.victoire = Victoire(self)
        self.tableau = TabScore(self)
        
        self.victoire.hide() ; self.tableau.hide()
        
        
        """INITIALISATION DES VARIABLE A AFFICHE"""
        self.labyrinthe = labyrinthe
        self.joueur = Joueur
        self.jeu = None
        self.UIingame = UIinGame(self.joueur.inventaire,self)
        self.UIingame.MinuteurVisibility(False)
        self.UIingame.setGeometry(0,0,self.new_width, self.new_height)
        self.item : dict = {"dynamite" : QPixmap("assets/img/labyrinthe/inventaire/items/dynamite.png"),"water" : QPixmap("assets/img/labyrinthe/inventaire/items/water.png"),"meat" : QPixmap("assets/img/labyrinthe/inventaire/items/meat.png"),"barre_energisante" : QPixmap("assets/img/labyrinthe/inventaire/items/barre_energisante.png")}
        
        """ATTRIBUT POUR LE LABY"""
        self.size_case = (self.new_height-50)//(self.labyrinthe.get("dimension")[0]+1)
        self.marge_cote = (self.new_width-((self.labyrinthe.get("dimension")[0]+1)*self.size_case))//2
        self.size_murs = self.size_case//2
        self.marge = 50
        dim = self.labyrinthe.get("dimension")[0]
        laby_largeur = dim * self.size_case
        laby_hauteur = dim * self.size_case
        self.offset_x = int((self.new_width - laby_largeur-self.marge*1) // 2)
        self.offset_y = int((self.new_height - laby_hauteur-self.marge*0.05) // 2)
        self.heigth_murs = int(self.size_case*1.6)
        self.texture_murs = QPixmap("assets/img/labyrinthe/rempart.png").scaled(self.size_murs,self.size_case,Qt.AspectRatioMode.IgnoreAspectRatio)
        self.texture_sol = QPixmap("assets/img/labyrinthe/sol_sombre.jpg").scaled(self.size_case,self.size_case,Qt.AspectRatioMode.IgnoreAspectRatio)
    
        self.texture_mur_h = QPixmap("assets/img/labyrinthe/rempartsombre.png").scaled(self.heigth_murs, self.size_murs)  # fin et large → pour Ouest/Est
        murs = QPainter(self.texture_mur_h)
        murs.fillRect(self.texture_mur_h.rect(),QColor(0, 0, 0, 30))
        murs.end()
        transform = QTransform().rotate(90)
        self.texture_mur_v = self.texture_mur_h.transformed(transform)
        
        
        """CAMERA"""
        
        self.cam_x = -(self.marge_cote + self.joueur.get_y()*self.size_case + self.size_case//4)
        self.cam_y  = -(self.marge + self.joueur.get_x()*self.size_case + self.size_case//4)
        self.cases_visibles = self.labyrinthe.get_cases_visibles((0,0),3)
        
        """FOV EN TRIANGLE"""
        self.dico_direction = {('Sud','Est') : ((0,0),(0,self.size_case),(self.size_case,self.size_case)),('Est','Sud') : ((0,0),(self.size_case,0),(self.size_case,self.size_case)),('Est','Nord') : ((self.size_case,0),(0,0),(0,self.size_case)),('Nord','Est') : ((self.size_case,0),(self.size_case,self.size_case),(0,self.size_case)),('Nord','Ouest') : ((self.size_case,self.size_case),(self.size_case,0),(0,0)),('Ouest','Nord') : ((self.size_case,self.size_case),(0,self.size_case),(0,0)),('Ouest','Sud') : ((0,self.size_case),(self.size_case,self.size_case),(self.size_case,0)),('Sud','Ouest') : ((self.size_case,0),(0,0),(0,self.size_case))}
        
        self.dico_direction_range = {('Sud','Est') : ((0,0),(0,self.size_case),(self.size_case,self.size_case),(self.size_case,self.size_case//2)),('Est','Sud') : ((0,0),(self.size_case,0),(self.size_case,self.size_case),(self.size_case//2,self.size_case)),('Est','Nord') : ((self.size_case,0),(0,0),(0,self.size_case),(self.size_case//2,self.size_case)),('Nord','Est') : ((self.size_case,0),(self.size_case,self.size_case),(0,self.size_case),(0,self.size_case//2)),('Nord','Ouest') : ((self.size_case,self.size_case),(self.size_case,0),(0,0),(0,self.size_case//2)),('Ouest','Nord') : ((self.size_case,self.size_case),(0,self.size_case),(0,0),(self.size_case//2,0)),('Ouest','Sud') : ((0,self.size_case),(self.size_case,self.size_case),(self.size_case,0),(self.size_case//2,0)),('Sud','Ouest') : ((0,self.size_case),(0,0),(self.size_case,0),(self.size_case,self.size_case//2))}
        
        """((self.marge_cote + x * self.size_case, self.marge + y * self.size_case),(self.marge_cote + x * self.size_case, self.marge + y * self.size_case+self.size_case),(self.marge_cote + x * self.size_case + self.size_case, self.marge + y * self.size_case + self.size_case))"""
    
        
        """ TIMER """
        self.temps = 211
        self.temps_restant = 211
        self.timer_label = QLabel(f"Temps restant : {self.temps_restant}s")
        self.timer_label.move(self.new_width//2, self.new_height//10)
        self.timer = QTimer(self)
        
        self.timer_fps = QTimer(self)
        self.timer_fps.timeout.connect(self.update_fps)
        
    """SIGNAUX"""
    def setup_signaux(self):
        self.jeu.victoire.connect(self.show_victoire)
        self.victoire.continuer.connect(self.show_tab)
        
    def show_victoire(self):
        if not self.jeu.mode == "lore":
            self.victoire.setGeometry(self.new_width//5,self.new_height//4,int(self.new_width//1.5), self.new_height//2)
            self.victoire.show()
        
    def show_tab(self):
        if not self.jeu.mode == "lore":
            self.victoire.hide()
            self.tableau.setGeometry(self.new_width//5,self.new_height//4,int(self.new_width//1.5), self.new_height//2)
            self.tableau.show()
            self.tableau.affichageScore()
            
    def update_fps(self):
        self.update()

    def start_timer(self):
        
        self.timer.timeout.connect(self.update_chronometre) 
        self.timer.start(1000)
        
    def update_chronometre(self):
        self.temps_restant -= 1
        print(f"Temps avant la cavalerie : {self.temps_restant}s")
        
        # Mise à jour de l'affichage (ton Label par exemple)
        self.timer_label.setText(f"Survivez : {self.temps_restant}s")
        
        if self.temps_restant <= 0:
            self.timer.stop()
            self.jeu.condition_victoire(self.temps_restant)
            
    def paintEvent(self,event):
        painter = QPainter(self)
        """Zoom sur le joueur"""
        
        self.cam_x = self.cam_x + (-(self.marge_cote + self.joueur.get_y()*self.size_case + self.size_case//4)-self.cam_x)*0.4
        self.cam_y = self.cam_y +  (-(self.marge + self.joueur.get_x()*self.size_case + self.size_case//4)-self.cam_y)*0.4
        painter.translate(self.new_width//2, self.new_height//2)
        painter.scale(2,2) 
        painter.translate(self.cam_x, self.cam_y)
        """A FINIR LE CAM_Y pour le zoom"""
        '''Dessin des parois du labyrinthe'''
                
        for elt in self.labyrinthe.labyrinthe.keys():
            liste_mur = self.labyrinthe.labyrinthe[elt].murs_cassable()
            y = elt[1]
            x = elt[0]
            for mur in liste_mur:
                match mur:
                    case "Nord":
                        painter.drawPixmap(QPoint(self.offset_x + y * self.size_case,self.offset_y + x * self.size_case),self.texture_mur_h)
                    case "Sud":
                        painter.drawPixmap(QPoint(self.offset_x + y * self.size_case,self.offset_y+x * self.size_case+self.size_case),self.texture_mur_h)
                    case "Ouest":
                        painter.drawPixmap(QPoint(self.offset_x + y * self.size_case,self.offset_y + x * self.size_case),self.texture_mur_v)
                    case "Est":
                        painter.drawPixmap(QPoint(self.offset_x + y * self.size_case+self.size_case,self.offset_y + x * self.size_case),self.texture_mur_v)
                        
        
        for elt in self.labyrinthe.labyrinthe.keys():
            
            if elt not in self.cases_visibles:
                painter.fillRect(self.marge_cote + elt[1] * self.size_case,self.marge + elt[0] * self.size_case,self.size_case,self.size_case,QColor(0, 0, 0, 255))
            
            elif float(self.cases_visibles[elt][0]) == 1.0:
                painter.drawPixmap(QPoint(self.marge_cote + elt[1] * self.size_case, self.marge + elt[0] * self.size_case), self.texture_sol)
                item = self.labyrinthe.labyrinthe[elt].get_item()
                if item != None:
                    painter.drawPixmap(QPoint(self.marge_cote + elt[1] * self.size_case, self.marge + elt[0] * self.size_case),self.item[item[0]].scaled(int(self.size_case//1.5),int(self.size_case//1.5),Qt.AspectRatioMode.IgnoreAspectRatio))

            elif float(self.cases_visibles[elt][0]) == 0.5:
                painter.drawPixmap(QPoint(self.marge_cote + elt[1] * self.size_case, self.marge + elt[0] * self.size_case), self.texture_sol)
                points = self.dico_direction[tuple(self.cases_visibles[elt][1])]
                base_x = self.marge_cote + elt[1] * self.size_case
                base_y = self.marge + elt[0] * self.size_case

                polygone = QPolygon([
                    QPoint(base_x + points[0][1], base_y + points[0][0]),
                    QPoint(base_x + points[1][1], base_y + points[1][0]),
                    QPoint(base_x + points[2][1], base_y + points[2][0])
                ])

                painter.setBrush(QColor(0, 0, 0, 255))
                painter.setPen(Qt.PenStyle.NoPen)  # pas de contour
                painter.drawPolygon(polygone)
                
            elif float(self.cases_visibles[elt][0]) == 0.33:
                painter.drawPixmap(QPoint(self.marge_cote + elt[1] * self.size_case, self.marge + elt[0] * self.size_case), self.texture_sol)
                points = self.dico_direction_range[tuple(self.cases_visibles[elt][1])]
                base_x = self.marge_cote + elt[1] * self.size_case
                base_y = self.marge + elt[0] * self.size_case
                
                polygone = QPolygon([
                    QPoint(base_x + points[0][1], base_y + points[0][0]),
                    QPoint(base_x + points[1][1], base_y + points[1][0]),
                    QPoint(base_x + points[2][1], base_y + points[2][0]),
                    QPoint(base_x + points[3][1], base_y + points[3][0])
                ])

                painter.setBrush(QColor(0, 0, 0, 255))
                painter.setPen(Qt.PenStyle.NoPen)  # pas de contour
                painter.drawPolygon(polygone)
        
        if self.UIingame.WhichSelected()[0] == "dynamite":
            murs_present = self.labyrinthe.murs_cassable(self.joueur.get_coord())
            for murs in murs_present:
                match murs:
                    case "Nord":
                         painter.fillRect(self.marge_cote + self.joueur.get_y()*self.size_case,self.marge + self.joueur.get_x()*self.size_case,self.size_case,2
                                          ,QColor(255, 0, 0) if self.jeu.last_moove == "Nord" else QColor(255, 140, 0))
                    case "Sud":
                        painter.fillRect(self.marge_cote + self.joueur.get_y()*self.size_case,self.marge + self.joueur.get_x()*self.size_case+self.size_case,self.size_case,2
                                          ,QColor(255, 0, 0) if self.jeu.last_moove == "Sud" else QColor(255, 140, 0))
                    case "Ouest":
                        painter.fillRect(self.marge_cote + self.joueur.get_y()*self.size_case,self.marge + self.joueur.get_x()*self.size_case,2,self.size_case
                                          ,QColor(255, 0, 0) if self.jeu.last_moove == "Ouest" else QColor(255, 140, 0))
                    case "Est":
                        painter.fillRect(self.marge_cote + self.joueur.get_y()*self.size_case+self.size_case,self.marge + self.joueur.get_x()*self.size_case,2,self.size_case
                                         ,QColor(255, 0, 0) if self.jeu.last_moove == "Est" else QColor(255, 140, 0))
                        
                
                
        if (x,y) == self.labyrinthe.get("end"):
            painter.fillRect(self.marge_cote + self.labyrinthe.get("end")[0]*self.size_case + self.size_case//4,self.marge + self.labyrinthe.get("end")[1]*self.size_case +self.size_case//4, self.size_case//2, self.size_case//2, QColor(255, 128,0))
        
        '''Dessin du joueur''' 
        painter.fillRect(self.marge_cote + self.joueur.get_y()*self.size_case + self.size_case//4,self.marge + self.joueur.get_x()*self.size_case +self.size_case//4, self.size_case//2, self.size_case//2, QColor(self.joueur.get_couleur()))
        
        """Dessin des monstres"""
        painter.fillRect(self.marge_cote + self.jeu.monstre_sonore.get_coord()[1]*self.size_case + self.size_case//4,self.marge + self.jeu.monstre_sonore.get_coord()[0]*self.size_case +self.size_case//4, self.size_case//2, self.size_case//2, QColor(self.joueur.get_couleur()))
        painter.fillRect(self.marge_cote + self.jeu.monstre_vision.get_coord()[1]*self.size_case + self.size_case//4,self.marge + self.jeu.monstre_vision.get_coord()[0]*self.size_case +self.size_case//4, self.size_case//2, self.size_case//2, QColor(self.joueur.get_couleur()))
        
        
        painter.end()
        
    def keyPressEvent(self, a0):
        self.jeu.deplacer_joueur(a0.key())
        
    def mousePressEvent(self, a0):
        self.jeu.utiliser_item(a0.buttons())
    
    def reset(self):
        self.temps_restant = 211
        self.timer_label.setText(f"Survivez : {self.temps_restant}s")
        self.setFocus()
        self.tableau.hide()
        self.victoire.hide()

                