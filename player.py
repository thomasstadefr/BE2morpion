from morpion import *


def player_move(G, is_new):
    print("À ton tour ! Vers quelle case veux-tu mettre ton pion ?")
    G.board.boutons_on()
    G.board.coup_choisi = False
    (y_f, x_f) = G.board.wait_for_player()
    while y_f < 0 or y_f >= G.size or x_f < 0 or x_f >= G.size or G.board.grille[y_f][x_f] != 0:
        print("Case incorrecte ! Vers quelle case veux-tu mettre ton pion ?")
        G.board.coup_choisi = False
        (y_f, x_f) = G.board.wait_for_player()
    G.board.boutons_off()

    if is_new:
        return Move(G.turn, (y_f, x_f), None)

    print("Depuis quelle case veux-tu déplacer ton pion ?")
    G.board.boutons_on()
    G.board.coup_choisi = False
    (y_i, x_i) = G.board.wait_for_player()
    while y_i < 0 or y_i >= G.size or x_i < 0 or x_i >= G.size or G.board.grille[y_i][x_i] != G.turn:
        print("Case incorrecte ! Depuis quelle case veux-tu déplacer ton pion ?")
        G.board.coup_choisi = False
        (y_i, x_i) = G.board.wait_for_player()
    G.board.boutons_off()

    return Move(G.turn, (y_f, x_f), (y_i, x_i))


def make_move_player(G):
    G.play_move(player_move(G, G.played_moves < G.size))
    G.played_moves += 0.5
    G.change_turn()
    G.board.afficher_grille()
