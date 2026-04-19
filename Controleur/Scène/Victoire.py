from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QPushButton
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt

class Victoire(QWidget):
    
    continuer = pyqtSignal()
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        """INITIALISATION DU LAYOUT PRINCIPALE"""
        self.panneau_victoire = QVBoxLayout() ; self.setLayout(self.panneau_victoire)
        
        """AJOUT DES QLABEL ET PUSHBUTTON"""
        
        self.labVictoire = QLabel("VOUS AVEZ SURVÉCU ! ")
        self.butVoirStat = QPushButton("Voir le tableau des scores")
        
        self.panneau_victoire.addWidget(self.labVictoire) ; self.panneau_victoire.addWidget(self.butVoirStat)
        
        """Signal"""
        self.butVoirStat.clicked.connect(self.clic)
        
        """Style"""
        
        self.setObjectName("Victoire")
        with open("assets/style/Victoire.qss") as f:
            self.setStyleSheet(f.read())
            
    def clic(self):
        self.continuer.emit()
        
        
        