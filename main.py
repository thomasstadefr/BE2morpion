from morpion import *
from ai import make_move_ai
from player import make_move_player
import threading


def main(player_color, size, enabled_repetitions):
    G = Game(size, enabled_repetitions)
    G.board.afficher_grille()

    if player_color == 2:
        make_move_ai(G)
        G.board.fenetre.after(1, G.board.afficher_grille)
        if G.result != 0:
            return G.result
    thread = threading.Thread(target=boucle, args=(G,), daemon=True)
    thread.start()

    G.board.fenetre.mainloop()


def boucle(G):
    while True:
        make_move_player(G)
        G.board.fenetre.after(1, G.board.afficher_grille)
        if G.result != 0:
            print("BRAVO ! 💪")
            return G.result

        make_move_ai(G)
        G.board.fenetre.after(1, G.board.afficher_grille)
        if G.result != 0:
            print("Perdu...😭")
            return G.result


print(main(1, 3, 5))
