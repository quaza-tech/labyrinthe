from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QPushButton,QTableWidget,QTableWidgetItem,QHeaderView,QHBoxLayout,QAbstractItemView
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from Modèle.BDD.Repositorie.ScoreRepo import ScoreRepo

class TabScore(QWidget):
    retourMenu = pyqtSignal()
    
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.layoutPrincipale = QVBoxLayout() ; self.setLayout(self.layoutPrincipale)
        
        """INSTANCIATION DES ELEMENTS DU TABLEAU DES SCORES"""
        """ -------------------------------------
            retour    TABLEAU DES SCORES
            -------------------------------------
            Nom    |    TEMPS   |   Difficulté  |   SCore
            jf          3s             eleve        0
            n           1min50s        faible       200
            
            
            ------------------------------------"""
        
        """Conteneur haut"""
        self.layoutContainer = QHBoxLayout()
        self.backButton = QPushButton('retour')
        self.labTabScore = QLabel("TABLEAU DES SCORES")
        
        """Tableau : QTABLEWIDGET"""
        self.tab = QTableWidget(self)
        self.tab.setRowCount(5)
        self.tab.setColumnCount(4)
        self.tab.setHorizontalHeaderLabels(['Pseudo','Temps','Difficulté','Score'])
        self.ScoreRepo = ScoreRepo()
        
        """ENCAPSULATION DES DIFFERENTS ELEMENTS DU TABLEAU """
        self.layoutContainer.addWidget(self.backButton,1,Qt.AlignmentFlag.AlignLeft) ; self.layoutContainer.addWidget(self.labTabScore,3,Qt.AlignmentFlag.AlignHCenter)
        self.layoutPrincipale.addLayout(self.layoutContainer) ; self.layoutPrincipale.addWidget(self.tab,2)
        self.tab.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        """MISE EN PLACE DU STYLE DU TABLEAU DES SCORES"""


        self.tab.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        
        with open("assets/style/TabScore.qss") as f:
            self.setStyleSheet(f.read())
            self.tab.setAlternatingRowColors(True)
        
        """SIGNAUX"""
        
        self.backButton.clicked.connect(self.retour)
            
    def affichageScore(self):
        data = self.ScoreRepo.getAllScoreDESC()
        if data[0] == True:
            row_index = 0
            for row in data[1]:
                self.tab.setItem(row_index, 0 , QTableWidgetItem(str(row[0])))
                self.tab.setItem(row_index, 1 , QTableWidgetItem(str(row[1])+" s"))
                self.tab.setItem(row_index, 2 , QTableWidgetItem(str(row[2])))
                self.tab.setItem(row_index, 3 , QTableWidgetItem(str(row[3])))
                row_index = row_index + 1
    def retour(self):
        self.retourMenu.emit()
                