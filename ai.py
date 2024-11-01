from morpion import*
from random import choice


'''
lst_allowed_moves prend en argument la Game G 
et le booléen indiquant si le coup à jouer consiste 
à poser un nouveau pion (et donc pas à en déplacer un existant)

et renvoie la liste des coups autorisés
'''
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



def ai_move_random(G, is_new):
    return choice(lst_allowed_moves(G, is_new))

def h1(G):
    if G.result == 1:
        return 99999
    if G.result == 2:
        return -99999
    if G.result == 3:
        return 0
    return 0


'''
ai_move_min_max prend en argument la Game G, 
l'heuristique h et la profondeur d'exploration depth

et renvoie le coup de l'IA, déterminé en utilisant l'algorithme
de recherche arborescente min_max avec l'élagage alpha-bêta
'''
def ai_move_min_max(G, h, depth):
    # alpha et bêta sont définis à des valeurs arbitraires pour alpha = -inf, bêta = +inf
    # on utilise des pointeurs pour les modifier par effets de bord
    alpha = [-99999]
    beta = [99999]

    # check_final traite le cas où on atteint une position terminale
    def check_final(G, m):
        if G.result == 1:
                G.result = 0
                G.cancel_move(m)
                return (99999, m) # cas terminal -> 1 a gagné
            
        if G.result == 2:
            G.result = 0
            G.cancel_move(m)
            return (-99999, m) # cas terminal -> 2 a gagné
        
        if G.result == 3:
            G.result = 0
            G.cancel_move(m)
            return (0, m) # cas terminal -> match nul

    '''
    get_max renvoie le couple (score, coup) ayant le score maximal pour l'heuristique h
    
    l'élagage beta amène à stopper l'exploration si un coup obtient un score
    suppérieur à bêta car le score max aura forcément un score suppérieur à bêta
    donc le coup d'avant n'aurait pas été minimal par l'heuristique (car un autre coup 
    menait à un score de bêta)
    '''
    def get_max(d):
        if d == 0:
            return (h(G), None) # cas terminal -> on a atteint la profondeur maximale donc on calcule le score par l'heuristique
        
        l_moves = lst_allowed_moves(G, G.played_moves<G.size)
        best_move = l_moves[0]

        G.play_move(best_move)
        if G.result != 0: # si on a atteint une position terminale
            return check_final(G, best_move)
        
        G.played_moves += 0.5
        G.change_turn()
        a = get_min(d-1)[0]
        G.change_turn()
        G.played_moves -= 0.5
        G.cancel_move(best_move)

        for m in l_moves:  # pour chaque coup, on le joue puis on effectue l'appel croisé et get_min et enfin on l'annule
            G.play_move(m)
            if G.result != 0:
                return check_final(G, m)
            
            G.played_moves += 0.5
            G.change_turn()
            score = get_min(d-1)[0]
            G.change_turn()
            G.played_moves -= 0.5
            G.cancel_move(m)

            if score>beta[0]: # dans ce cas on réalise une coupure bêta
                return (score, None)
            if score>a: # cas où l'on a trouvé un coup meilleur que les précédants
                a = score
                best_move = m

        beta[0] = a   # on met à jour la valeur de bêta car on a trouvé le coup pour l'instant meilleur
        return (a, best_move)
    
    def get_min(d):  # fonctionne similairement à get_max (avec une coupure alpha)
        if d == 0:
            return (h(G), None)
    
        l_moves = lst_allowed_moves(G, G.played_moves<G.size)
        best_move = l_moves[0]
        
        G.play_move(best_move)
        if G.result != 0:
            return check_final(G, best_move)
        
        G.played_moves += 0.5
        G.change_turn()
        b = get_max(d-1)[0]
        G.change_turn()
        G.played_moves -= 0.5
        G.cancel_move(best_move)

        for m in l_moves:
            G.play_move(m)
            if G.result != 0:
                return check_final(G, m)
            
            G.played_moves += 0.5
            G.change_turn()
            score = get_max(d-1)[0]
            G.change_turn()
            G.played_moves -= 0.5
            G.cancel_move(m)

            if score<alpha[0]:
                return (score, None)
            if score<b:
                b = score
                best_move = m
            
        alpha[0] = b
        return (b, best_move)

    if G.turn == 1:
        return get_max(depth)[1]   # on renvoie le max ou le min selon la couleur de l'IA
    else:
        return get_min(depth)[1]



def ai_move(G, is_new):
    return ai_move_min_max(G, h1, 3)

def make_move_ai(G):
    G.play_move(ai_move(G, G.played_moves < G.size))
    G.played_moves += 0.5
    G.change_turn()
    G.test()