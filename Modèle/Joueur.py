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
    
    def get_nom(self) ->str:
        return self.pseudo
    
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
        
    def reset(self):
        self.est_accroupi = False
        self.coord = self.start