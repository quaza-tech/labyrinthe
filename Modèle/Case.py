class Case:
    def __init__(self,coordonnee : tuple,texture : str):
        self.Nord : bool = False
        self.Sud : bool = False
        self.Est : bool = False
        self.Ouest : bool = False
        self.coordonnee : tuple = coordonnee
        self.visite : bool = False
        self.texture_sol = texture
    def get_direction(self,direction) ->bool:
        match direction :
            case "Nord":
                return self.Nord
            case "Sud":
                return self.Sud
            case "Est":
                return self.Est
            case "Ouest":
                return self.Ouest
            
    def get_visite(self)-> bool:
        return self.visite
    
    def get_texture(self)->str:
        return self.texture_sol
    
    def set_direction(self,direction): 
        match direction :
            case "Nord":
                self.Nord = True
            case "Sud":
                self.Sud = True
            case "Est":
                self.Est = True
            case "Ouest":
                self.Ouest = True
                
    def set_visite(self):
        self.visite = True
        
    def set_texture(self,texture):
        self.texture_sol = texture
        
    def direction_dispo(self) ->list:
        liste = ["Nord","Sud","Est","Ouest"]
        dispo = []
        for i in range (len(liste)):
            if self.get_direction(liste[i]) != False:
                dispo.append(liste[i])
        return dispo
    
    def murs_cassable(self) ->list:
        liste = ["Nord","Sud","Est","Ouest"]
        cassable = []
        for i in range (len(liste)):
            if self.get_direction(liste[i]) == False:
                cassable.append(liste[i])
        return cassable