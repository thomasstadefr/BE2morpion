'''
Un coup est une instance de la classe Move, avec comme attributs
la couleur du pion posé, la position finale du pion posé et la 
position initiale du pion posé (éventuellement None si ce pion est nouveau)

Les joueurs 1 et 2 auront respectivement des pions de couleur 1 et 2
'''

class Move:
    def __init__(self, col, final_pos, init_pos = None):
        self.color = col
        self.init_pos = init_pos
        self.final_pos = final_pos


'''
fast_pow_3 sert à calculer efficacement la puissance de 3
par l'entier n (en gardant en mémoire les résultats déjà calculés)

L'encodage d'une position utilise en effet ces calculs
'''

pow_3 = {0:1, 1:3}
def fast_pow_3(n):
    if n == 0 or n == 1 or n in pow_3.keys():
        return pow_3[n]
    y = fast_pow_3(n//2)
    res = y**2
    if n%2 == 1:
        res *= 3
    pow_3[n] = res
    return res


'''
Une partie est une instance de la classe Game, avec comme attributs
le plateau, sa taille, le trait actuel, le résultat, la position actuelle, 
le comptage des occurences des positions rencontrées et le nombre
maximal de répétitions d'une position avant de déclarer la partie nulle

Le plateau sera représenté par une matrice dont chaque case vaut :
0 si elle est vide, 1 (respectivement 2) si elle contient un pion 
du joueur 1 (respectivement 2)

On utilisera comme convention pour le résultat :
partie en cours : result = 0 
victoire de 1 : result = 1
victoire de 2 : result = 2
partie nulle : result = 3

Pour compter les occurences de chaque position, on encode chaque position par un entier 
(le méthode est détaillée dans le rapport)
'''

class Game:
    def __init__(self, size, enabled_repetitions):
        self.size = size
        self.enabled_repetitions = enabled_repetitions
        self.turn = 1
        self.result = 0
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_pos = 1
        self.count_pos = {1 : 1}

    '''
    play_move prend en argument un coup de classe Move
    et modifie l'instance de Game afin de prendre en compte 
    que ce coup a été joué
    '''
    def play_move(self, m):
        # On remplie la case correspondant au coup joué
        b = self.board
        col = m.color
        n = self.size
        init_pos = m.init_pos
        final_pos = m.final_pos
        (y, x) = final_pos
        b[y][x] = col

        # On calcule l'encodage de la position résultante
        self.current_pos += col * fast_pow_3(n*y+x+1)
        if init_pos != None:
            (i, j) = init_pos
            b[i][j] = 0
            self.current_pos -= col * fast_pow_3(n*i+j+1)
        if col == 1:
            self.current_pos += 1
        else:
            self.current_pos -= 1

        # On enregistre l'occurence de cette position et on vérifie si elle ne s'est pas trop répétée
        if self.current_pos in self.count_pos.keys():
            self.count_pos[self.current_pos] += 1
            if self.count_pos[self.current_pos] == self.enabled_repetitions:
                self.result = 3
        else:
            self.count_pos[self.current_pos] = 1

        # On vérifie si le coup joué est gagnant
        pass

    '''
    cancel_move prend en argument un coup de classe Move
    et modifie l'instance de Game afin de prendre en compte 
    que ce coup a été annulé
    '''
    def cancel_move(self, m):
        # On vide la case correspondant au coup annulé
        b = self.board
        col = m.color
        n = self.size
        init_pos = m.init_pos
        final_pos = m.final_pos
        (y, x) = final_pos
        b[y][x] = 0

        # On enlève l'occurence de cette position
        self.count_pos[self.current_pos] -= 1

        # On calcule l'encodage de la position résulante
        self.current_pos -= col * fast_pow_3(n*y+x+1)
        if init_pos != None:
            (i, j) = init_pos
            b[i][j] = col
            self.current_pos += col * fast_pow_3(n*i+j+1)
        if col == 1:
            self.current_pos -= 1
        else:
            self.current_pos += 1

    def test(self):
        b = self.board
        for l in b:
            print(l)
        print("current pos : ", self.current_pos)
        print("count : ", self.count_pos)
        

G = Game(5, 10)
G.test()
G.play_move(Move(1, (3, 3), None))
G.test()
G.cancel_move(Move(1, (3, 3), None))
G.test()
G.play_move(Move(1, (0, 1), None))
G.play_move(Move(2, (0, 0), None))
G.test()