from PyQt6.QtWidgets import QApplication,QWidget
import sys
from Modèle.Labyrinthe import labyrinthe
from Controleur.Joueur import Joueur
from Controleur.Jeu import Jeu
from Vue.Vue import Vue
from Controleur.SceneManager import SceneManager

if __name__ == "__main__":

    print(' --- main --- ')
    
    # création d'une QApplication
    app = QApplication(sys.argv)
    # creation d'un widget
    manager = SceneManager((20,20))
    # lancement de l'application
    sys.exit(app.exec()) 