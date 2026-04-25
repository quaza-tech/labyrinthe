from PyQt6.QtWidgets import QApplication,QWidget
import sys
from Controleur.SceneManager import SceneManager
from Vue.Scène.UIgame import UIinGame

if __name__ == "__main__":

    print(' --- main --- ')
    
    # création d'une QApplication
    app = QApplication(sys.argv)
    # creation d'un widget
    manager = UIinGame({'dynamite' : 5,'water' : 5})
    # lancement de l'application
    sys.exit(app.exec()) 