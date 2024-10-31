from morpion import*

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