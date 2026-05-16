from PyQt6.QtWidgets import QWidget, QPushButton,QGridLayout
from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtGui import QPixmap
from Vue.Composants.Slot_minuteur.Slot_minuteur import SlotMinuteur


class Minuteur(QWidget):
    
    temps : pyqtSignal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.layoutG = QGridLayout() ; self.setLayout(self.layoutG)
        
        self.firstSlot : SlotMinuteur = SlotMinuteur()
        self.secondSlot : SlotMinuteur = SlotMinuteur()
        
        self.validation : QPushButton = QPushButton("Valider")
        self.validation.setObjectName("valider")
        
        self.layoutG.addWidget(self.firstSlot,0,0,Qt.AlignmentFlag.AlignCenter) ; self.layoutG.addWidget(self.secondSlot,0,1,Qt.AlignmentFlag.AlignCenter) ; self.layoutG.addWidget(self.validation,1,0,1,2,Qt.AlignmentFlag.AlignCenter)
        """CONNECTION"""
        
        self.validation.clicked.connect(self.emission_temps)
        
        """STYLE"""
        
        self.setStyleSheet("""
                           QWidget {
                                background-color : rgba(0,0,0,125)
                                max-width: 200px;
                                max-height: 200px;
                               }
                            #valider {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                                            stop:0 #4e342e, stop:1 #261b18); /* Dégradé bois sombre */
                                color: #d7ccc8;
                                font-family: 'Georgia', serif;
                                font-size: 20px;
                                font-weight: bold;
                                
                                border: 3px solid #1a1a1a; /* Bordure fer forgé */
                                border-radius: 8px;
                                
                                /* C'est ici qu'on agrandit la taille */
                                min-width: 100px;
                                min-height: 20px;
                                margin-bottom: 10px;
                               }
                            #valider:hover {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                                            stop:0 #5d4037, stop:1 #3e2723);
                                border: 3px solid #e0ca82; /* Lueur dorée au survol */
                                color: #ffffff;
                            }
                            #valider:pressed {
                                background: #1b110f;
                                padding-top: 5px; /* Effet enfoncé */
                                padding-left: 5px;
                            }""")
    def emission_temps(self):
        self.temps.emit(self.firstSlot.get_nombre()*10 + self.secondSlot.get_nombre())
        
        
        
        
        
        