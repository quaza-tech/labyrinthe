from Services.Sound import son
from Modèle.BDD.Repositorie.AudioRepo import audioRepo

class SoundManager:
    def __init__(self):
        
        # dictionnaire de sons
        self.sounds = {}
        self.audio = audioRepo()
        self._load_sounds()

    def _load_sounds(self):
        
        
        self.sounds["effets"] = [("step",son("pas_beton",0.2)),("explosion",son("explosion",0.6)),("explosion_lointaine",son("explosion_lointaine",0.7))]
    
    def play(self, name,categorie):
        for i in range (0,len(self.sounds[categorie])):
            if self.sounds[categorie][i][0] == name:
                self.sounds[categorie][i][1].son.play()
                    
    def set_volume(self, volume):
        self.volume = volume
        
        for sound in self.sounds.values():
            for elt in sound:
                elt[1].setVolumeByPourcentage(volume/100)
    
    def set_volume_to(self,info : tuple):
        
        if info[0] in self.sounds:
            for elt in self.sounds[info[0]]:
                    self.sounds[info[0]][elt][1].son.setVolumeByPourcentage(info[1]/100)