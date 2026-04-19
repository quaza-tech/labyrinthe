from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QStackedWidget,QVBoxLayout,QPushButton,QSlider,QCheckBox,QTabWidget,QLineEdit
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtGui import QGuiApplication,QPainter, QPen, QColor, QBrush
from Controleur.Joueur import Joueur
from Controleur.Jeu import Jeu
from Modèle.Labyrinthe import labyrinthe
from Controleur.CurrentKey import KeyBinder
from Vue.Vue import Vue
from PyQt6.QtCore import pyqtSignal
import sys

class Parametre(QTabWidget):
    
    touche_assign = pyqtSignal(tuple)
    
    def __init__(self,joueur):
        
        settings = QWidget()
        super().__init__()
        self.joueur = joueur
        # 1. Création des onglets
        
        self.tab_audio = QWidget()
        self.tab_visuel = QWidget()
        self.tab_commandes = QWidget()
        self.tab_gameplay = QWidget()
        
        self.addTab(self.tab_audio, "AUDIO")
        self.addTab(self.tab_visuel, "VISUEL")
        self.addTab(self.tab_commandes, "COMMANDES")
        self.addTab(self.tab_gameplay, "GAMEPLAY")
        
        
        self.setup_audio_tab()
        
        self.apply_medieval_style()
        
    def setup_audio_tab(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Volume des bruitages (Pas, Cris) :"))
        self.sfx_slider = QSlider(Qt.Orientation.Horizontal)
        self.sfx_slider.setRange(0, 100)
        self.sfx_slider.setValue(80)
        layout.addWidget(self.sfx_slider)
        
        layout.addWidget(QCheckBox("Aide visuelle pour l'aveugle"))
        layout.addStretch() # Pousse tout vers le haut
        self.tab_audio.setLayout(layout)
    def setup_commande_tab(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Avancé : "))
        self.key_up = KeyBinder(self.joueur.get_commande("avancer"),lambda t: self.joueur.set_commande("avancer", t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.key_up)
        
        layout.addWidget(QLabel("Reculer : "))
        self.key_down = KeyBinder(self.joueur.get_commande("reculer"),lambda t: self.joueur.set_commande("reculer", t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.key_down)
        
        layout.addWidget(QLabel("Droite : "))
        self.key_right = KeyBinder(self.joueur.get_commande("droite"),lambda t: self.joueur.set_commande("droite", t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.key_right)
        
        layout.addWidget(QLabel("Gauche : "))
        self.key_left = KeyBinder(self.joueur.get_commande("gauche"),lambda t: self.joueur.set_commande("gauche", t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.key_left)
        
        self.tab_commandes.setLayout(layout)
        
        """SIGNAUX"""
        
        self.key_up.new_touche.connect(lambda t: self.touche_assign.emit(("avancer", t))) 
        self.key_down.new_touche.connect(lambda t: self.touche_assign.emit(("reculer", t)))
        self.key_left.new_touche.connect(lambda t: self.touche_assign.emit(("gauche", t)))
        self.key_right.new_touche.connect(lambda t: self.touche_assign.emit(("droite", t)))
        
    def apply_medieval_style(self):
        self.setStyleSheet("""
            /* Le conteneur global */
            QTabWidget::pane {
                border: 2px solid #3d2b1f;
                background: rgba(40, 30, 20, 220); /* Fond sombre transparent */
                border-radius: 5px;
            }

            /* Style des onglets (le menu du haut) */
            QTabBar::tab {
                background: #1a120b;
                color: #d4c4a8;
                padding: 15px 30px;
                border: 1px solid #3d2b1f;
                border-bottom: none;
                font-family: 'Georgia';
                font-weight: bold;
                font-size: 16px;
            }

            QTabBar::tab:selected {
                background: #4e342e; /* Plus clair quand sélectionné */
                color: #e0ca82;
                border-top: 3px solid #e0ca82;
            }

            QTabBar::tab:hover {
                background: #32211c;
            }

            /* Style des textes à l'intérieur */
            QLabel {
                color: #d4c4a8;
                font-size: 14px;
            }
        """)