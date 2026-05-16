from PyQt6.QtWidgets import QWidget, QLabel,QPushButton,QVBoxLayout
from PyQt6.QtCore import Qt,pyqtSignal,QSize
from PyQt6.QtGui import QPixmap,QTransform,QIcon
from Vue.Composants.Slot_minuteur.fleche import fleche


class SlotMinuteur(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layoutV = QVBoxLayout() ; self.setLayout(self.layoutV)
        
        """WIDGET DU SLOT"""
        self.flecheHaut : fleche = fleche("haut")
        self.flecheBas : fleche = fleche("bas")
        
        """LABEL """
        self.__nombre : int = 0
        self.label : QLabel = QLabel(str(self.__nombre))
        
        self.layoutV.addWidget(self.flecheHaut) ; self.layoutV.addWidget(self.label) ;self.layoutV.addWidget(self.flecheBas)
        
        """SIGNAUX ET CONNECTION"""
        self.flecheHaut.changement.connect(self.modification_label)
        self.flecheBas.changement.connect(self.modification_label)
        
        """STYLE """
        
        self.setStyleSheet("""QWidget {
                                            background-color: rgba(0, 0, 0, 0);
                                        }

                                        QLabel {
                                            color: #e0ca82;
                                            font-family: 'Georgia';
                                            font-size: 24px;
                                            font-weight: bold;
                                            qproperty-alignment: AlignCenter;
                                        }""")
        
        self.show()
    def modification_label(self,valeur):
        if  self.__nombre + valeur > -1 and self.__nombre + valeur < 10 :
            self.__nombre = self.__nombre + valeur
            self.label.setText(str(self.__nombre))
    
    def get_nombre(self):
        return self.__nombre
    

