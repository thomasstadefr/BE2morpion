from morpion import*

def lst_allowed_moves(G, is_new):
    n = G.size
    c = G.turn
    res = []

    if not(is_new):
        lst_pawns = []
        for i in range(n):
            for j in range(n):
                if G.board[i][j] == c:
                    lst_pawns.append((i, j))
        
        for i in range(n):
            for j in range(n):
                if G.board[i][j] == 0:
                    for k in range(n):
                        res.append(Move(c, (i, j), lst_pawns[k]))

    else:
        for i in range(n):
            for j in range(n):
                if G.board[i][j] == 0:
                    res.append(Move(c, (i, j), None))

    return res

def ai_move(G, is_new):
    return lst_allowed_moves(G, is_new)[0]

def make_move_ai(G):
    G.play_move(ai_move(G, G.played_moves < G.size))
    G.played_moves += 0.5
    G.change_turn()
    G.test()