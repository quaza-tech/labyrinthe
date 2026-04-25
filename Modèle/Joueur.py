class Joueur:
    def __init__(self,coordonnee : tuple ,couleur : str, pseudo : str):
        self.coord = coordonnee
        self.start = coordonnee
        self.couleur = couleur
        self.avancer = "Z"
        self.reculer =  "S"
        self.gauche = "Q"
        self.droite = "D"
        self.accroupi = 16
        self.est_accroupi = False
        self.pseudo : str = pseudo
        self.inventaire : dict = {}
        self.stamina : float = 1.0
        self.eau : float = 1.0
        self.faim : float = 1.0
        
    def get_coord(self)-> tuple:
        return self.coord
    
    def get_x(self) -> int:
        return self.coord[0]
    
    def get_y(self) ->int :
        return self.coord[1]
    
    def get_couleur(self)->str:
        return self.couleur
    def get_commande(self,commande):
        match commande:
            case "avancer":
                return self.avancer
            case "reculer":
                return self.reculer
            case "gauche" :
                return self.gauche
            case "droite":
                return self.droite
            case "accroupi":
                return self.accroupi
    
    def get_item(self,item) -> int:
        if item in self.inventaire:
            return self.inventaire[item]
        return 0
    
    def get_nom(self) ->str:
        return self.pseudo
    def get_barre(self,barre) -> float :
        match barre:
            case "eau":
                return self.eau
            case "faim":
                return self.faim
            case "stamina":
                return self.stamina
            
    def is_accroupi(self) -> bool:
        return self.est_accroupi
    
    def set_nom(self,nom : str):
        self.pseudo = nom
        
    def set_commande(self,commande,new):
       match commande:
            case "avancer":
                self.avancer = new
            case "reculer":
                self.reculer = new
            case "gauche" :
                self.gauche = new
            case "droite":
                self.droite = new
            case "accroupi":
                self.accroupi = new
    
    def set_coord(self,coord : tuple ):
        self.coord = coord
    
    def set_accroupi(self,etat : bool):
        self.est_accroupi = etat
    
    def set_barre(self,barre,pourcentage : float):
        match barre:
            case "eau":
                self.eau = pourcentage
            case "faim":
                self.faim = pourcentage
            case "stamina":
                self.stamina = pourcentage
    def set_item(self,item,nbr):
        if item in self.inventaire:
            self.inventaire[item] += nbr
        else :
            self.inventaire[item] = nbr      
    def reset(self):
        self.est_accroupi = False
        self.coord = self.start
        self.eau,self.faim,self.stamina = 1.0