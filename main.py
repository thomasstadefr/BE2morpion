from morpion import*
from ai import make_move_ai
from player import make_move_player

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