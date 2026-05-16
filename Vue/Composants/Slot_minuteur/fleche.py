from PyQt6.QtWidgets import QWidget, QLabel,QPushButton
from PyQt6.QtCore import Qt,pyqtSignal,QSize
from PyQt6.QtGui import QPixmap,QTransform,QIcon


class fleche(QPushButton):
    
    changement : pyqtSignal = pyqtSignal(int)
    
    def __init__(self,orientation : str):
        super().__init__()
        
        self.img = QPixmap("assets/img/Labyrinthe/inventaire/UI/top-arrow-icon.png") if orientation == "haut" else QPixmap("assets/img/Labyrinthe/inventaire/UI/top-arrow-icon.png").transformed(QTransform().rotate(180))
        self.Icon = QIcon(self.img)
        self.setIcon(self.Icon)
        self.setIconSize(QSize(32,32))
        self.setFixedSize(32,32)
        self.orientation : str = orientation
        self.clicked.connect(self.emettre)
        
        self.setStyleSheet(""" QPushButton {
                                background-color: rbga(0,0,0,0);
                                width: 30px;
                            }
                            """)
        self.show()
    def emettre(self):
        if self.orientation == "haut":
            self.changement.emit(1)
        else :
            self.changement.emit(-1)

