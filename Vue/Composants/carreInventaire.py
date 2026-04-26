from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class Slot(QWidget):
    def __init__(self, item: tuple):
        super().__init__()

        
        self.item = item
        self.setFixedSize(72,72)
        
        self.label = QLabel(self)
        self.label.setObjectName("deselection")
        self.label.setGeometry(0, 0, 64, 64)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if item[0] != "":
            pixmap = QPixmap(f"assets/img/labyrinthe/inventaire/items/{item[0]}.png")
            self.label.setPixmap(pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))

        self.label_nbr = QLabel(str(item[1]), self)
        self.label_nbr.setObjectName("nbr")
        self.label_nbr.setFixedSize(20, 20)
            # position en bas à droite
        self.label_nbr.move(64 - 20, 64 - 20)
            # style
        
        self.label_nbr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if item[1] == 0:
            self.label_nbr.hide()
            
        self.load_styleSheet()
        # 🎨 Style du slot
        
    def load_styleSheet(self):
        
        with open("assets/style/slots.qss") as f:
            self.setStyleSheet(f.read())
            
    def getItem(self) -> tuple:
        return self.item
    def updateVue(self):
        pixmap = QPixmap(f"assets/img/labyrinthe/inventaire/items/{self.item[0]}.png")
        self.label.setPixmap(pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
        print(self.item)
        if self.item[1] > 0:
            self.label_nbr.setText(str(self.item[1]))
            self.label_nbr.show()
        else:
            self.label_nbr.hide()
    def updateNbrItem(self,item,valeurs):
        if self.item[1]+valeurs == 0 and self.item != ("",0) :
            self.item = ("",0)
            
        elif self.item == ("",0):
            self.item = (item,valeurs)
        else :
            ancien = (self.item[0],self.item[1])
            self.item = (ancien[0],ancien[1]+valeurs)
        self.updateVue()
    
    def selection(self):
        self.label.setObjectName("selection")
        self.load_styleSheet()
    
    def deselection(self):
        self.label.setObjectName("deselection")
        self.load_styleSheet()
        
        