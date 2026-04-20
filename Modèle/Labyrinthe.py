from Modèle.Case import Case 
import random,time
from collections import deque
class labyrinthe:
    def __init__(self,dimension : tuple,debut : tuple, fin : tuple):
        self.labyrinthe = {}
        self.dimension = dimension
        self.start = debut
        self.end = fin
        self.dernier_deplacement = time.time()
    def get(self,want):
        
        match want:
            case "dimension":
                return self.dimension
            case "start":
                return self.start
            case "end":
                return self.end
            
    def set_labyrinthe(self,nb_texture : str):
        for x in range(0,self.dimension[0]):
            for y in range(0,self.dimension[1]): 
                texture = random.randint(0,nb_texture-1)
                coord = (x,y)
                if coord not in self.labyrinthe.keys():
                    self.labyrinthe[coord] = Case(coord,texture)
                else:
                    print ("une case existe déja avec ces coordonnées ",coord," donc ERR")
    def murs_cassable(self,case_actuel) ->list:
        liste_cassable = self.labyrinthe[case_actuel].murs_cassable()
        if case_actuel[0]==0:
            if "Nord" in liste_cassable:
                liste_cassable.remove("Nord")
        if case_actuel[0] == self.dimension[0]-1:
            if "Sud" in liste_cassable:
                liste_cassable.remove("Sud")
        if case_actuel[1] == 0:
            if "Ouest" in liste_cassable:
                liste_cassable.remove("Ouest")
        if case_actuel[1] == self.dimension[1]-1:
            if "Est" in liste_cassable:
                liste_cassable.remove("Est")
        return liste_cassable
    
    def add_ouverture(self):
        for elt in self.labyrinthe.keys():
            case_non_voisine : list = self.murs_cassable(elt)
            if len(case_non_voisine)>=2:
                casse = random.randint(0,100)
                if casse < 10:
                    choix_murs = random.randint(0,len(case_non_voisine)-1)
                    match case_non_voisine[choix_murs]:
                        case "Nord":
                            case_adjacent = (elt[0]-1,elt[1])
                            self.labyrinthe[case_adjacent].set_direction("Sud")
                            self.labyrinthe[elt].set_direction("Nord")
                        case "Sud":
                            case_adjacent = (elt[0]+1,elt[1])
                            self.labyrinthe[case_adjacent].set_direction("Nord")
                            self.labyrinthe[elt].set_direction("Sud")
                        case "Est":
                            case_adjacent = (elt[0],elt[1]+1)
                            self.labyrinthe[case_adjacent].set_direction("Ouest")
                            self.labyrinthe[elt].set_direction("Est")
                        case "Ouest":
                            case_adjacent = (elt[0],elt[1]-1)
                            self.labyrinthe[case_adjacent].set_direction("Est")
                            self.labyrinthe[elt].set_direction("Ouest")
                    
    def create_way(self):
            Pile = [(0,0)]
            while Pile != []:
                case_actuel : tuple = Pile[-1]
                liste_cassable : list = self.murs_cassable(case_actuel)
                case_trouve : bool = False
                while case_trouve == False and liste_cassable != []:
                    choix_murs = random.randint(0,len(liste_cassable)-1)
                    self.labyrinthe[case_actuel].set_visite()
                    match liste_cassable[choix_murs]:
                        case "Nord":
                            case_adjacent = (case_actuel[0]-1,case_actuel[1])
                            if self.labyrinthe[case_adjacent].get_visite() != True:
                                self.labyrinthe[case_adjacent].set_direction("Sud")
                                self.labyrinthe[case_actuel].set_direction("Nord")
                                case_trouve = True
                                Pile.append(case_adjacent)
                            else:
                                liste_cassable.remove("Nord")
                        case "Sud":
                            case_adjacent = (case_actuel[0]+1,case_actuel[1])
                            if self.labyrinthe[case_adjacent].get_visite() != True:
                                self.labyrinthe[case_adjacent].set_direction("Nord")
                                self.labyrinthe[case_actuel].set_direction("Sud")
                                case_trouve = True
                                Pile.append(case_adjacent)
                            else:
                                liste_cassable.remove("Sud")
                        case "Est":
                            case_adjacent = (case_actuel[0],case_actuel[1]+1)
                            if self.labyrinthe[case_adjacent].get_visite() != True:
                                self.labyrinthe[case_adjacent].set_direction("Ouest")
                                self.labyrinthe[case_actuel].set_direction("Est")
                                case_trouve = True
                                Pile.append(case_adjacent)
                            else:
                                liste_cassable.remove("Est")
                        case "Ouest":
                            case_adjacent = (case_actuel[0],case_actuel[1]-1)
                            if self.labyrinthe[case_adjacent].get_visite() != True:
                                self.labyrinthe[case_adjacent].set_direction("Est") 
                                self.labyrinthe[case_actuel].set_direction("Ouest") 
                                case_trouve = True
                                Pile.append(case_adjacent)
                            else:
                                liste_cassable.remove("Ouest")
                if not case_trouve :
                    Pile.pop()
            self.add_ouverture()
    def can_moove(self,coord : tuple ,coor_direction : tuple) -> bool:
        x, y = coor_direction[0]-coord[0], coor_direction[1]-coord[1]
        match x:
            case -1:
                if self.labyrinthe[coord].get_direction("Nord"):
                        return True
            case 1:
                if self.labyrinthe[coord].get_direction("Sud"):
                        return True
        match y :
            case -1:
                if self.labyrinthe[coord].get_direction("Ouest"):
                        return True
            case 1:
                if self.labyrinthe[coord].get_direction("Est"):
                        return True
        return False
    def can_see(self, observateur: tuple, cible: tuple) -> float:
        dx : int = cible[0] - observateur[0]
        dy : int = cible[1] - observateur[1]
        vision : float = 0.0
        liste_direction: list  = []

        # Case adjacente (distance 1, pas diagonale)
        if abs(dx) + abs(dy) == 1:
            if self.can_moove(observateur,cible):
                
                vision += 1
        # Case à distance 2 en ligne droite
        if (abs(dx) == 2 and dy == 0) or (dx == 0 and abs(dy) == 2):
            # deux can_moove à enchaîner
            case_intermédiaire : tuple = (observateur[0]+dx//2,observateur[1]+dy//2)
            if self.can_moove(observateur,case_intermédiaire) and self.can_moove(case_intermédiaire,cible):
                vision += 1
        
        # Diagonale simple
        if abs(dx) == 1 and abs(dy) == 1:
            if self.can_moove(observateur,(observateur[0],observateur[1]+dy)) and self.can_moove((observateur[0],observateur[1]+dy),cible):
                vision += 0.5
                match dy:
                    case -1:
                        liste_direction.append("Ouest")
                    case 1 :
                        liste_direction.append("Est")
                match dx : 
                    case -1:
                        liste_direction.append("Nord")
                    case 1:
                        liste_direction.append("Sud")
            if self.can_moove(observateur,(observateur[0]+dx,observateur[1])) and self.can_moove((observateur[0]+dx,observateur[1]),cible):
                vision += 0.5
                match dx : 
                    case -1:
                        liste_direction.append("Nord")
                    case 1:
                        liste_direction.append("Sud")
                match dy:
                    case -1:
                        liste_direction.append("Ouest")
                    case 1 :
                        liste_direction.append("Est")
        if (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2):
            # deux can_moove à enchaîner
            if abs(dx) ==2:
                case_intermédiaire_v1 :tuple = (observateur[0]+dx//2,observateur[1])
                case_intermédiaire_v2 : tuple = (observateur[0]+dx,observateur[1])
            elif abs(dy) == 2:
                case_intermédiaire_v1 :tuple = (observateur[0],observateur[1]+dy//2)
                case_intermédiaire_v2 : tuple = (observateur[0],observateur[1]+dy)
                
            if case_intermédiaire_v2 in self.labyrinthe.keys() and case_intermédiaire_v1 in self.labyrinthe.keys():
                if self.can_moove(observateur,case_intermédiaire_v1) and self.can_moove(case_intermédiaire_v1,case_intermédiaire_v2) and self.can_moove(case_intermédiaire_v2,cible):
                    vision += 0.33
                    if abs(dx) == 2:
                        match dx : 
                            case -2:
                                liste_direction.append("Nord")
                            case 2:
                                liste_direction.append("Sud")
                        match dy:
                            case 1:
                                liste_direction.append("Est")
                            case -1:
                                liste_direction.append("Ouest")
                    elif abs(dy) == 2:
                        match dy:
                            case 2:
                                liste_direction.append("Est")
                            case -2:
                                liste_direction.append("Ouest")
                        match dx : 
                            case -1:
                                liste_direction.append("Nord")
                            case 1:
                                liste_direction.append("Sud")
                
                        
            
        return (vision,liste_direction)
    def get_cases_visibles(self, observateur: tuple,dist : int) -> dict:
        dico_see : dict = {observateur : (1,[])}
        for x in range(observateur[0]-dist,observateur[0]+dist):
            for y in range (observateur[1]-dist,observateur[1]+dist):
                case_test : tuple = (x,y)
                if 0 <= x < self.dimension[0] and 0 <= y < self.dimension[1]:
                    test_vision : float = self.can_see(observateur,case_test)
                    if test_vision[0] != 0:
                        dico_see[case_test] = test_vision
        return dico_see
        
    ''' METHODE DE BFS POUR LES MONSTRES '''
    
    def bfs_monstre(self,coord_monstre : tuple,coord_joueur : tuple):
        
        File = deque([coord_monstre]) 
        dico : dict = {}
        trouve : bool = False
        directions : dict = {"Nord": (-1,0), "Sud": (1,0), "Est": (0,1), "Ouest": (0,-1)}
        while len(File) != 0 and not trouve:
            case_actuelle : tuple = File.popleft()
            liste_case : list = self.labyrinthe[case_actuelle].direction_dispo()
            for elt in liste_case:
                enfant : tuple = (case_actuelle[0]+directions[elt][0],case_actuelle[1]+directions[elt][1])
                if enfant not in dico.keys():
                    dico[enfant] = case_actuelle
                    if enfant[0] == coord_joueur[0] and enfant[1] == coord_joueur[1]:
                        trouve = True
                        break
                    else :
                        File.append(enfant)
        liste_chemin : list = [coord_joueur]
        while liste_chemin[-1][0] != coord_monstre[0] or liste_chemin[-1][1] != coord_monstre[1]:
            coord : tuple = dico[liste_chemin[-1]]
            liste_chemin.append(coord)
        return liste_chemin[::-1]
    def deplacement_aléatoire_monstre(self,coord : tuple)->list:
        chemin : list = []
        coord_actuel : tuple = coord
        directions : dict = {"Nord": (-1,0), "Sud": (1,0), "Est": (0,1), "Ouest": (0,-1)}
        while len(chemin) < 6:
            liste_direction : list = self.labyrinthe[coord_actuel].direction_dispo()
            choix : str = random.choice(liste_direction)
            chemin.append((coord_actuel[0]+directions[choix][0],coord_actuel[1]+directions[choix][1]))
            coord_actuel : tuple = (coord_actuel[0]+directions[choix][0],coord_actuel[1]+directions[choix][1])
        return chemin
        