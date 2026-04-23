from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt,QTimer,pyqtSignal,QObject,QUrl

class son:
    def __init__(self,fichier : str,volume_initial : float):
        
        self.volume = volume_initial
        self.son = QSoundEffect()
        self.son.setSource(QUrl.fromLocalFile("assets/son/"+fichier+".wav"))
        self.son.setVolume(volume_initial)
    
    def setNewVolume(self,newVolume : float):
        self.son.setVolume(newVolume)
        
    def setVolumeByPourcentage(self,pourcentage : float):
        self.volumePourcentage = self.volume * pourcentage
        self.son.setVolume(self.volumePourcentage)
    