from PyQt6.QtWidgets import QWidget,QLabel,QPushButton,QGridLayout
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtGui import QPixmap,QKeySequence,QGuiApplication

class Pause(QWidget):
    
    retourMenu : pyqtSignal = pyqtSignal()
    parametres : pyqtSignal = pyqtSignal(str)
    retour_jeu : pyqtSignal = pyqtSignal()
    
    def __init__(self,parent = None):
        super().__init__(parent)
        
        
        self.new_width = QGuiApplication.primaryScreen().size().width()-100
        self.new_height =  QGuiApplication.primaryScreen().size().height()-100
        
        self.grid : QGridLayout = QGridLayout() ; self.setLayout(self.grid)
        
        self.label = QLabel()
        self.label.setGeometry(0,0,self.new_width,self.new_height)
        self.label.lower()
        
        self.button_reprendre = QPushButton("Reprendre")
        self.button_parametres = QPushButton("Parametres")
        self.button_menu = QPushButton("Menu")
        
        self.grid.addWidget(self.button_reprendre,1,1) ; self.grid.addWidget(self.button_parametres,3,1) ; self.grid.addWidget(self.button_menu,5,1)
        self.apply_style()
        
        self.button_reprendre.clicked.connect(self.retour_jeu_emit)
        self.button_parametres.clicked.connect(lambda t :self.parametres.emit("jeu"))
        self.button_menu.clicked.connect(self.retourMenu.emit)
        
        self.setVisible(False)
    
    
    def apply_style(self):
        self.setStyleSheet("""
                           QGridLayout {
                               background-color : rgba(26, 18, 11, 180);
                           }
                           QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                                            stop:0 #4e342e, stop:1 #261b18); /* Dégradé bois sombre */
                                color: #d7ccc8;
                                font-family: 'Georgia', serif;
                                font-size: 24px;
                                font-weight: bold;
                                
                                border: 3px solid #1a1a1a; /* Bordure fer forgé */
                                border-radius: 8px;
                                
                                /* C'est ici qu'on agrandit la taille */
                                min-width: 250px;
                                min-height: 60px;
                                margin-bottom: 10px;
                            }

                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                                            stop:0 #5d4037, stop:1 #3e2723);
                                border: 3px solid #e0ca82; /* Lueur dorée au survol */
                                color: #ffffff;
                            }

                            QPushButton:pressed {
                                background: #1b110f;
                                padding-top: 5px; /* Effet enfoncé */
                                padding-left: 5px;
                            }
                           """)
        
    def changement_fond(self,fond : QPixmap):
        self.label.setPixmap(fond)
        
    def keyPressEvent(self, a0):
        touche = QKeySequence(a0.key()).toString()
        if touche == "Esc":
            self.retour_jeu_emit()
            
    def retour_jeu_emit(self):
        self.retour_jeu.emit()