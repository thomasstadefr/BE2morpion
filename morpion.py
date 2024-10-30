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
        self.played_moves = 0

    # change_turn permet de changer le trait
    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1

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
        win_row = True
        win_column = True
        win_diag1 = True
        win_diag2 = True
        for i in range(n):
            if b[y][i] != col:
                win_row = False
            if b[i][x] != col:
                win_column = False
            if y != x or b[i][i] != col:
                win_diag1 = False
            if y != n-1-x or b[i][n-1-i] != col:
                win_diag2 = False
        if win_row or win_column or win_diag1 or win_diag2:
            self.result = col

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
        print("\n")
        b = self.board
        for l in b:
            print(l)
        print("\ncurrent pos : ", self.current_pos)
        print("count : ", self.count_pos)
        print("played moves : ", self.played_moves)
        


def ai_move(G, is_new):
    if is_new:
        return Move(G.turn, (int(input("y final : ")), int(input("x final : "))), None)
    return Move(G.turn, (int(input("y final : ")), int(input("x final : "))), (int(input("y init : ")), int(input("x init : "))))

def make_move_ai(G):
    G.play_move(ai_move(G, G.played_moves < G.size))
    G.played_moves += 0.5
    G.change_turn()
    G.test()


def player_move(G, is_new):
    (y_f, x_f) = (int(input("y final : ")), int(input("x final : ")))
    while y_f<0 or y_f>=G.size or x_f<0 or x_f>=G.size or G.board[y_f][x_f] != 0:
        (y_f, x_f) = (int(input("y final : ")), int(input("x final : ")))

    if is_new:
        return Move(G.turn, (y_f, x_f), None)
    
    (y_i, x_i) = (int(input("y init : ")), int(input("x init : ")))
    while y_i<0 or y_i>=G.size or x_i<0 or x_i>=G.size or G.board[y_i][x_i] != G.turn:
        (y_i, x_i) = (int(input("y init : ")), int(input("x init : ")))

    return Move(G.turn, (y_f, x_f), (y_i, x_i))

def make_move_player(G):
    G.play_move(player_move(G, G.played_moves < G.size))
    G.played_moves += 0.5
    G.change_turn()
    G.test()



def main(player_color, size, enabled_repetitions):
    G = Game(size, enabled_repetitions)
    G.test()

    if player_color == 2:
        make_move_ai(G)
        if G.result != 0:
            return G.result

    while True:
        make_move_player(G)
        if G.result != 0:
            return G.result
        
        make_move_ai(G)
        if G.result != 0:
            return G.result
        

print(main(1, 3, 5))

        

