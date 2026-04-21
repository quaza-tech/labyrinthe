from PyQt6.QtWidgets import QLabel,QWidget,QVBoxLayout,QPushButton
from PyQt6.QtCore import Qt

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.menu_organisation = QVBoxLayout(); self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True) 
        self.label = QLabel("L'ECHO DU SILENCE") ; self.pseudoJoueur = QLabel("")
        self.button_start = QPushButton("Mode : Traversée solitaire") ; self.button_start.setObjectName("start")
        self.button_continue = QPushButton("Mode : Souffle Court")
        self.button_Parameter = QPushButton("Paramètre")
        self.button_leave = QPushButton("Quitter")
        
        """Construction du menu """
        self.menu_organisation.addWidget(self.label,1,Qt.AlignmentFlag.AlignCenter) ; self.menu_organisation.addWidget(self.pseudoJoueur,1,Qt.AlignmentFlag.AlignCenter)
        self.menu_organisation.addWidget(self.button_start,1,Qt.AlignmentFlag.AlignCenter)
        self.menu_organisation.addWidget(self.button_continue,1,Qt.AlignmentFlag.AlignCenter)
        self.menu_organisation.addWidget(self.button_Parameter,1,Qt.AlignmentFlag.AlignCenter)
        self.menu_organisation.addWidget(self.button_leave,1,Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.menu_organisation)
        
        """Style du menu """
        self.setObjectName("Menu")
        with open("assets/style/Menu.qss") as f:
            self.setStyleSheet(f.read())
    
    def setPseudo(self,pseudo):
        self.pseudoJoueur.setText(pseudo)