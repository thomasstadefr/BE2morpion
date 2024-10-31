def ai_move(G, is_new):
    if is_new:
        return Move(G.turn, (int(input("y final : ")), int(input("x final : "))), None)
    return Move(G.turn, (int(input("y final : ")), int(input("x final : "))), (int(input("y init : ")), int(input("x init : "))))

def make_move_ai(G):
    G.play_move(ai_move(G, G.played_moves < G.size))
    G.played_moves += 0.5
    G.change_turn()
    G.test()