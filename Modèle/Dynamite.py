class Dynamite():
    def __init__(self,coord : tuple,direction : str,etat : str,temps : int):
        self.coord : tuple = coord
        self.direction : str = direction
        self.etat : str = etat
        self.temps : int = temps
        
    def get (self,what) :
        match what:
            case "coord":
                return self.coord
            case "direction":
                return self.direction
            case "etat":
                return self.etat
            case "temps":
                return self.temps
    def set (self,what,truc) :
        match what:
            case "coord":
                self.coord = truc
            case "direction":
                self.direction = truc
            case "etat":
                self.etat = truc
            case "temps":
                self.temps -= truc
    