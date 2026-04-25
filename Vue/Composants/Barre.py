from PyQt6.QtWidgets import QWidget,QLabel,QVBoxLayout,QPushButton,QTableWidget,QTableWidgetItem,QHeaderView,QHBoxLayout,QProgressBar,QGridLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt

class barre(QWidget):
    def __init__(self,couleur : str,orientation : str):
        super().__init__()
        
        self.__value = 0

        
        layout = QVBoxLayout(self)
        self.__progressBar = QProgressBar()
        
        match orientation:
            case "V": 
                self.__progressBar.setOrientation(Qt.Orientation.Vertical)
                self.setFixedSize(50, 200)
            case "H":
                self.__progressBar.setOrientation(Qt.Orientation.Horizontal)
                self.setFixedSize(200,50)
        self.__progressBar.setValue(100)
        self.__progressBar.setTextVisible(False)

        layout.addWidget(self.__progressBar)
        """self.__button.clicked.connect(self.incValue)"""
        self.setStyleSheet(""" QProgressBar {
                                border: 2px solid grey;
                                border-radius: 5px;
                                background-color: black;
                                width: 30px;
                            }

                            QProgressBar::chunk {
                                background-color: """+ couleur +""";
                            }
                            
                            """)
        self.incValue(20)
    def incValue(self,value):
        self.__value = self.__value + value
        self.__progressBar.setValue(self.__value)
        
        