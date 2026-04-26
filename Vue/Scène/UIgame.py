from PyQt6.QtWidgets import QWidget,QLabel,QVBoxLayout,QPushButton,QTableWidget,QTableWidgetItem,QHeaderView,QHBoxLayout,QProgressBar,QGridLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from Vue.Composants.carreInventaire import Slot
from Vue.Composants.Barre import barre

class UIinGame(QWidget):
    def __init__(self,dico : dict,parent = None):
        super().__init__(parent)
        
        self.resize(800,500)
        self.grid = QGridLayout() ; self.layoutInventaire = QHBoxLayout() ; self.layoutEtatJoueur = QHBoxLayout()
        self.setLayout(self.grid)
        
        """Layout Inventaire"""
        self.liste_keys : list = []
        for elt in dico:
            self.liste_keys.append(elt)
        print(self.liste_keys)
        
        self.slots : list = []

        for i in range(0,4):
            if len(self.liste_keys) > i:
                slot = Slot((self.liste_keys[i],dico[self.liste_keys[i]]))
            else : 
                slot = Slot(("",0))
            self.slots.append(slot)
            self.layoutInventaire.addWidget(slot,Qt.AlignmentFlag.AlignBottom)
                
        self.layoutInventaire.addStretch()
        self.layoutInventaire.setSpacing(2)
        
        """Layout Etat du joueur"""
        self.stamina,self.eau,self.nourriture = barre("#FFEE00","V"),barre('#54D6FF',"V"),barre("#9C3C00","V")
        self.layoutEtatJoueur.addWidget(self.stamina) ; self.layoutEtatJoueur.addWidget(self.eau) ;  self.layoutEtatJoueur.addWidget(self.nourriture)
        
        """Widget barre de progression du laby"""
        self.progLaby = barre("#00CC11","H")
        
        self.grid.addWidget(self.progLaby,0,2,1,2)
        self.grid.addLayout(self.layoutInventaire,3,0,1,2,Qt.AlignmentFlag.AlignBottom) ; self.grid.addLayout(self.layoutEtatJoueur,3,4,1,1,Qt.AlignmentFlag.AlignBottom)
        
        self.show()
        
    def StaminaIsVisible(self) -> bool:
        return not self.stamina.isHidden()
    
    def PogressLabyIsVisible(self) -> bool:
        return not self.progLaby.isHidden()
    
    def SetStaminaVisibility(self,action : bool):
        match action:
            case False:
                self.stamina.hide()
            case True:
                self.stamina.show()
    
    def SetProgLabyVisibility(self,action : bool):
        match action:
            case False:
                self.progLaby.hide()
            case True:
                self.progLaby.show()
    
    def SetNewValuesBarre(self,values :dict) :
        for key in values:
            match key:
                case "eau":
                    self.eau.incValue(values[key])
                case "nourriture":
                    self.nourriture.incValue(values[key])
                case "stamina":
                    self.stamina.incValue(values[key])
                case "progression":
                    self.progLaby.incValue(values[key])
                    
    def updateItem(self,item,valeurs):
        for i in range(len(self.slots)):
            if self.slots[i].getItem()[0] == item:
                self.slots[i].updateNbrItem(item,valeurs)
                return
            elif self.slots[i].getItem()[0] == "":
                self.slots[i].updateNbrItem(item,valeurs)
                return
    def selection(self,num_slots):
        for elt in self.slots:
            elt.deselection()
        self.slots[num_slots].selection()
        
    
    
  
