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
        self.sprint = None
        self.prendre = None
        self.use = None
        self.touche_slots = {0: "&" ,1 : "é", 2 : '"', 3 : "'"}
        self.est_accroupi = self.est_sprint = self.est_freeze = False
        
        self.pseudo : str = pseudo
        self.inventaire : dict = {}
        
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
            case "sprint":
                return self.sprint
            case "freeze":
                return self.est_freeze
            case 0:
                return self.touche_slots[0]
            case 1:
                return self.touche_slots[1]
            case 2:
                return self.touche_slots[2]
            case 3:
                return self.touche_slots[3]
            case "prendre":
                return self.prendre
            case "utiliser":
                return self.use
            
    def get_slots_dico(self) -> dict:
        return self.touche_slots
            
    
    def get_item(self,item) -> int:
        if item in self.inventaire:
            return self.inventaire[item]
        return 0
    
    def get_nom(self) ->str:
        return self.pseudo
    
            
    def is_accroupi(self) -> bool:
        return self.est_accroupi
    
    def is_sprint(self) -> bool:
        return self.est_sprint
    
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
            case "sprint":
                self.sprint = new
            case "prendre":
                self.prendre = new
            case "utiliser":
                self.use = new
            case '0':
                self.touche_slots[0] = new
            case '1':
                self.touche_slots[1] = new
            case '2':
                self.touche_slots[2] = new
            case '3':
                self.touche_slots[3] = new
    
    def set_coord(self,coord : tuple ):
        self.coord = coord
    
    def set_accroupi(self,etat : bool):
        self.est_accroupi = etat
    
    def set_sprint(self,etat : bool):
        self.est_sprint = etat
    
    def set_freeze(self,etat : bool):
        self.est_freeze = etat
                
    def set_item(self,item,nbr) :
        if item in self.inventaire:
            self.inventaire[item] += nbr
        else :
            if len(self.inventaire) >=4:
                item_tombe = self.inventaire.popitem()
                self.inventaire[item] = nbr
                return item_tombe
            else:
                self.inventaire[item] = nbr   
                 
    def reset(self):
        self.est_accroupi = self.est_freeze = self.est_sprint = False
        self.coord = self.start
        self.inventaire = {}
        self.eau = self.faim = self.stamina = 1.0