from PyQt6.QtWidgets import QApplication,QWidget
import sys
from Controleur.SceneManager import SceneManager
from Vue.Scène.UIgame import UIinGame

if __name__ == "__main__":

    print(' --- main --- ')
    
    # création d'une QApplication
    app = QApplication(sys.argv)
    # creation d'un widget
    manager = SceneManager((20,20))
    # lancement de l'application
    sys.exit(app.exec()) 