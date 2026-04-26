from PyQt6.QtWidgets import QLabel,QWidget,QVBoxLayout,QSlider,QCheckBox,QTabWidget
from PyQt6.QtCore import Qt
from Controleur.CurrentKey import KeyBinder
from PyQt6.QtCore import pyqtSignal

class Parametre(QTabWidget):
    
    touche_assign = pyqtSignal(tuple)
    son_generale = pyqtSignal(int)
    son_effet = pyqtSignal(tuple)
    son_musique = pyqtSignal(tuple)
    son_ui = pyqtSignal(tuple)
    aide_vis = pyqtSignal()
    
    
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
        
        layout.addWidget(QLabel("Volume générale (Pas, Cris) :"))
        self.gene_vol = QSlider(Qt.Orientation.Horizontal)
        self.gene_vol.setRange(0, 100)
        self.gene_vol.setValue(100)
        layout.addWidget(self.gene_vol)
        
        layout.addWidget(QLabel("Volume de la Musique :"))
        self.mus_vol = QSlider(Qt.Orientation.Horizontal)
        self.mus_vol.setRange(0, 100)
        self.mus_vol.setValue(100)
        layout.addWidget(self.mus_vol)
        
        layout.addWidget(QLabel("Volume des effets sonore:"))
        self.eff_vol = QSlider(Qt.Orientation.Horizontal)
        self.eff_vol.setRange(0, 100)
        self.eff_vol.setValue(100)
        layout.addWidget(self.eff_vol)
        
        layout.addWidget(QLabel("Volume de l'interface (bouton) :"))
        self.ui_vol = QSlider(Qt.Orientation.Horizontal)
        self.ui_vol.setRange(0, 100)
        self.ui_vol.setValue(100)
        layout.addWidget(self.ui_vol)
        
        self.aide_visu = QCheckBox("Aide visuelle")
        layout.addWidget(self.aide_visu)
        layout.addStretch() # Pousse tout vers le haut
        self.tab_audio.setLayout(layout)
        
        """SIGNAUX"""
        self.gene_vol.valueChanged.connect(self.son_generale.emit)
        self.mus_vol.valueChanged.connect(lambda t: self.son_musique.emit(("musique", t)))
        self.eff_vol.valueChanged.connect(lambda t: self.son_effet.emit(("effet",t)))
        self.ui_vol.valueChanged.connect(lambda t: self.son_ui.emit(("ui",t)))
        self.aide_visu.checkStateChanged.connect(self.aide_vis.emit)
        
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
        
        layout.addWidget(QLabel("S'accroupir : "))
        self.shift = KeyBinder(self.joueur.get_commande("accroupi"),lambda t: self.joueur.set_commande("accroupi", t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.shift)
        
        layout.addWidget(QLabel("Slot 1  : "))
        self.slots1 = KeyBinder(self.joueur.get_commande(0),lambda t: self.joueur.set_commande('0', t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.slots1)
        
        layout.addWidget(QLabel("Slot 2 : "))
        self.slots2 = KeyBinder(self.joueur.get_commande(1),lambda t: self.joueur.set_commande('1', t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.slots2)
        
        layout.addWidget(QLabel("Slot 3 : "))
        self.slots3 = KeyBinder(self.joueur.get_commande(2),lambda t: self.joueur.set_commande('2', t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.slots3)
        
        layout.addWidget(QLabel("Slot 4 : "))
        self.slots4 = KeyBinder(self.joueur.get_commande(3),lambda t: self.joueur.set_commande('3', t)) # On crée le binder avec la touche par défaut
        layout.addWidget(self.slots4)
        
        self.tab_commandes.setLayout(layout)
        
        """SIGNAUX"""
        
        self.key_up.new_touche.connect(lambda t: self.touche_assign.emit(("avancer", t))) 
        self.key_down.new_touche.connect(lambda t: self.touche_assign.emit(("reculer", t)))
        self.key_left.new_touche.connect(lambda t: self.touche_assign.emit(("gauche", t)))
        self.key_right.new_touche.connect(lambda t: self.touche_assign.emit(("droite", t)))
        self.shift.new_touche.connect(lambda t: self.touche_assign.emit(("accroupi", t)))
        self.slots1.new_touche.connect(lambda t: self.touche_assign.emit((0, t)))
        self.slots2.new_touche.connect(lambda t: self.touche_assign.emit((1, t)))
        self.slots3.new_touche.connect(lambda t: self.touche_assign.emit((2, t)))
        self.slots4.new_touche.connect(lambda t: self.touche_assign.emit((3, t)))
        
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