from PyQt6.QtWidgets import QWidget,QHBoxLayout,QGridLayout
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import Qt
from Vue.Composants.carreInventaire import Slot
from Vue.Composants.Barre import barre
from Vue.Composants.Minuteur import Minuteur

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
        
        self.slots : list = []

        for i in range(0,4):
            if len(self.liste_keys) > i:
                slot = Slot((self.liste_keys[i],dico[self.liste_keys[i]]))
            else : 
                slot = Slot(("",0))
            self.slots.append(slot)
            self.layoutInventaire.addWidget(slot,Qt.AlignmentFlag.AlignBottom)
        self.slots[0].selection()     
        self.layoutInventaire.addStretch()
        self.layoutInventaire.setSpacing(2)

        self.minuteur : Minuteur = Minuteur()
        self.grid.addWidget(self.minuteur,3,3,1,2,Qt.AlignmentFlag.AlignBottom)
        
        """Layout Etat du joueur"""
        self.stamina,self.eau,self.nourriture = barre("#FFEE00","V"),barre('#54D6FF',"V"),barre("#9C3C00","V")
        self.layoutEtatJoueur.addWidget(self.stamina) ; self.layoutEtatJoueur.addWidget(self.eau) ;  self.layoutEtatJoueur.addWidget(self.nourriture)
        
        self.stamina_effect = QGraphicsOpacityEffect() ; self.progLaby_effect = QGraphicsOpacityEffect() ; self.minuteur_effect = QGraphicsOpacityEffect()
        """Widget barre de progression du laby"""
        self.progLaby = barre("#00CC11","H")
        
        self.grid.addWidget(self.progLaby,0,3,1,2)
        self.grid.addLayout(self.layoutInventaire,3,0,1,2,Qt.AlignmentFlag.AlignBottom) ; self.grid.addLayout(self.layoutEtatJoueur,3,7,1,2,Qt.AlignmentFlag.AlignBottom)
        self.grid.setColumnStretch(2,1) ; self.grid.setColumnStretch(5,1)
        
    def getValuesBarre(self,barre : str) -> int:
        match barre:
            case "eau":
                return self.eau.getValue()
            case "nourriture":
                return self.nourriture.getValue()
            case "stamina":
                return self.stamina.getValue()
            case "progression":
                return self.progLaby.getValue()
            
    def StaminaIsVisible(self) -> bool:
        return not self.stamina.isHidden()
    
    def PogressLabyIsVisible(self) -> bool:
        return not self.progLaby.isHidden()
    
    def SetStaminaVisibility(self,action : bool):
        match action:
            case False:
                self.stamina_effect.setOpacity(0)
            case True:
                self.stamina_effect.setOpacity(1)
        self.stamina.setGraphicsEffect(self.stamina_effect)
    
    def SetProgLabyVisibility(self,action : bool):
        match action:
            case False:
                self.prog_effect.setOpacity(0)
            case True:
                self.prog_effect.setOpacity(1)
        self.progLaby.setGraphicsEffect(self.stamina_effect)
    
    def MinuteurVisibility(self,action : bool):
        match action:
            case False:
                self.minuteur_effect.setOpacity(0)
            case True:
                self.minuteur_effect.setOpacity(1)
        self.minuteur.setGraphicsEffect(self.minuteur_effect)
        
    def SetNewValuesBarre(self,values :dict) :
        for key in values:
            match key:
                case "water":
                    self.eau.incValue(values[key])
                case "meat":
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
            elif self.slots[i].getItem()[0] == "" and valeurs > 0:
                self.slots[i].updateNbrItem(item,valeurs)
                return
            
    def selection(self,num_slots):
        for elt in self.slots:
            elt.deselection()
        self.slots[num_slots].selection()

    def WhichSelected(self) -> tuple:
        for elt in self.slots:
            if elt.isSelected():
                return elt.getItem()
            
    
        
        