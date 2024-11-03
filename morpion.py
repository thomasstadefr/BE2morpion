import tkinter as tk


"""Instance pour gérer le plateau, elle contient notamment toutes les méthodes graphiques."""


class NonGraphic_Board:
    def __init__(self, size):
        self.size = size
        self.coup_choisi = False

        self.grille = [[0 for _ in range(self.size)] for _ in range(self.size)]


class Board:
    def __init__(self, size):
        self.size = size
        self.coup_choisi = False
        self.fenetre = tk.Tk()
        self.fenetre.title("Jeu de Morpion")

        # Création des boutons pour la grille
        self.boutons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.couleurs = {1: 'X', 2: 'O'}
        for i in range(self.size):
            for j in range(self.size):
                self.boutons[i][j] = tk.Button(self.fenetre, text='', font=('Helvetica', 20), height=2, width=5, command=lambda i=i, j=j: self.button_click(i, j))
                self.boutons[i][j].grid(row=i, column=j)
                self.boutons[i][j].config(text='')
                # self.boutons[i][j].config(state=tk.DISABLED)
        self.boutons_off()

        self.grille = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def afficher_grille(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grille[i][j] == 1:
                    text = 'O'
                elif self.grille[i][j] == 2:
                    text = 'X'
                else:
                    text = ''
                self.boutons[i][j].config(text=text)

    def placer_pion(self, col, final_pos, init_pos):
        if init_pos is not None:
            self.boutons[init_pos[0]][init_pos[1]].config(text='')
        self.boutons[final_pos[0]][final_pos[1]].config(text=self.couleurs[col])

    def button_click(self, i, j):
        self.coup_choisi = (i, j)

    def wait_for_player(self):
        while self.coup_choisi is False:
            pass
        return self.coup_choisi

    def boutons_on(self):
        for boutons in self.boutons:
            for bouton in boutons:
                bouton.config(state=tk.NORMAL)

    def boutons_off(self):
        for boutons in self.boutons:
            for bouton in boutons:
                bouton.config(state=tk.DISABLED)

    def get_bouton(self, i, j):
        return self.boutons[i][j]


'''
Un coup est une instance de la classe Move, avec comme attributs
la couleur du pion posé, la position finale du pion posé et la 
position initiale du pion posé (éventuellement None si ce pion est nouveau)

Les joueurs 1 et 2 auront respectivement des pions de couleur 1 et 2
'''


class Move:
    def __init__(self, col, final_pos, init_pos=None):
        self.color = col
        self.init_pos = init_pos
        self.final_pos = final_pos


'''
fast_pow_3 sert à calculer efficacement la puissance de 3
par l'entier n (en gardant en mémoire les résultats déjà calculés)

L'encodage d'une position utilise en effet ces calculs
'''

pow_3 = {0: 1, 1: 3}


def fast_pow_3(n):
    if n == 0 or n == 1 or n in pow_3.keys():
        return pow_3[n]
    y = fast_pow_3(n//2)
    res = y**2
    if n % 2 == 1:
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
    def __init__(self, size, enabled_repetitions, is_graphic=True):
        self.size = size
        self.enabled_repetitions = enabled_repetitions
        self.turn = 1
        self.result = 0
        if is_graphic is True:
            self.board = Board(self.size)
        else:
            self.board = NonGraphic_Board(self.size)
        self.current_pos = 1
        self.count_pos = {1: 1}
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
        b = self.board.grille
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
        b = self.board.grille
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
        b = self.board.grille
        for l in b:
            print(l)
