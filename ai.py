from morpion import *
from random import choice
from copy import deepcopy
import random
import math
import numpy as np
from collections import defaultdict


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

    if not (is_new):
        lst_pawns = []
        for i in range(n):
            for j in range(n):
                if G.board.grille[i][j] == c:
                    lst_pawns.append((i, j))
        print(lst_pawns, G.board.grille)
        for i in range(n):
            for j in range(n):
                if G.board.grille[i][j] == 0:
                    for k in range(n):
                        res.append(Move(c, (i, j), lst_pawns[k]))

    else:
        for i in range(n):
            for j in range(n):
                if G.board.grille[i][j] == 0:
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
            return (99999, m)  # cas terminal -> 1 a gagné

        if G.result == 2:
            G.result = 0
            G.cancel_move(m)
            return (-99999, m)  # cas terminal -> 2 a gagné

        if G.result == 3:
            G.result = 0
            G.cancel_move(m)
            return (0, m)  # cas terminal -> match nul

    '''
    get_max renvoie le couple (score, coup) ayant le score maximal pour l'heuristique h
    
    l'élagage beta amène à stopper l'exploration si un coup obtient un score
    suppérieur à bêta car le score max aura forcément un score suppérieur à bêta
    donc le coup d'avant n'aurait pas été minimal par l'heuristique (car un autre coup 
    menait à un score de bêta)
    '''
    def get_max(d):
        if d == 0:
            return (h(G), None)  # cas terminal -> on a atteint la profondeur maximale donc on calcule le score par l'heuristique

        l_moves = lst_allowed_moves(G, G.played_moves < G.size)
        best_move = l_moves[0]

        G.play_move(best_move)
        if G.result != 0:  # si on a atteint une position terminale
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

            if score > beta[0]:  # dans ce cas on réalise une coupure bêta
                return (score, None)
            if score > a:  # cas où l'on a trouvé un coup meilleur que les précédants
                a = score
                best_move = m

        beta[0] = a   # on met à jour la valeur de bêta car on a trouvé le coup pour l'instant meilleur
        return (a, best_move)

    def get_min(d):  # fonctionne similairement à get_max (avec une coupure alpha)
        if d == 0:
            return (h(G), None)

        l_moves = lst_allowed_moves(G, G.played_moves < G.size)
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

            if score < alpha[0]:
                return (score, None)
            if score < b:
                b = score
                best_move = m

        alpha[0] = b
        return (b, best_move)

    if G.turn == 1:
        return get_max(depth)[1]   # on renvoie le max ou le min selon la couleur de l'IA
    else:
        return get_min(depth)[1]


class Noeud():
    def __init__(self, G, parent=None, move_from=None):
        self.G = deepcopy(G)
        self.etat = deepcopy(G.board.grille)
        self.parent = parent
        self.enfants = []
        self.visites = 0
        self.victoires = 0
        self.move_from = move_from

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)

    def est_fully_expanded(self):
        return len(self.enfants) == len(lst_allowed_moves(self.G, self.G.played_moves < self.G.size))

    def actions_possibles(self):
        print("Allowed moves : ", len(lst_allowed_moves(self.G, self.G.played_moves < self.G.size)))
        return lst_allowed_moves(self.G, self.G.played_moves < self.G.size)

    def maj(self, G):
        self.G = deepcopy(G)
        self.etat = deepcopy(G.board.grille)


class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():

            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        return possible_moves[np.random.randint(len(possible_moves))]


class NoeudMCTS():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = Game(state.size, state.enabled_repetitions, False)  # On créé une nouvelle instance Game pour copier l'état et éviter les effets de bords. Puis on copie la valeur de tous les attributs

        self.state.board.size = state.board.size
        self.state.board.coup_choisi = state.board.coup_choisi
        self.state.board.grille = deepcopy(state.board.grille)

        self.state.count_pos = deepcopy(state.count_pos)
        self.state.current_pos = state.current_pos
        self.state.enabled_repetitions = state.enabled_repetitions
        self.state.played_moves = state.played_moves
        self.state.result = state.result
        self.state.size = state.size
        self.state.turn = state.turn

        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[2] = 0
        self._results[3] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()

        print("untried actions : ", [(action.init_pos, action.final_pos, action.color) for action in self._untried_actions])

        print(self.state.played_moves, self.state.played_moves < self.state.size, self.state.turn)
        return

    def untried_actions(self):
        print("STATE : ", self.state.board.grille)
        self._untried_actions = lst_allowed_moves(self.state, self.state.played_moves < self.state.size)
        return self._untried_actions

    def best_action(self, itermax):
        for i in range(itermax):
            v = self._tree_policy()  # Retourne le noeud pour faire l'expansion
            reward = v.rollout()  # Simulation
            v.backpropagate(reward)  # Rétropropagation
        return self.best_child(0)

    def _tree_policy(self):  # PARTIE SELECTION
        current_node = self
        while not current_node.is_terminal_node():  # On selectionne les noeuds enfants jusqu'à ce qu'une feuille soit atteinte
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()  # On choisi la meilleure feuille selon l'heuristique ubs1
        return current_node

    def is_terminal_node(self):
        if self.state.result == 0 or self.state.result == 3:
            return True
        return False

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def expand(self):  # PARTIE DÉPLOIEMENT
        # print("Untried Actions : ", [(action.init_pos, action.final_pos, action.color) for action in self._untried_actions])
        # print("Action : ", self._untried_actions[-1].init_pos)
        action = self._untried_actions.pop()
        # print("action : ", action.init_pos)
        parent = deepcopy(self)
        # self.state.play_move(action)  # On fait évoluer le jeu contenu dans le noeud
        # self.state.played_moves += 0.5
        # self.state.change_turn()
        child_node = NoeudMCTS(self.state, parent=parent, parent_action=action)
        self.children.append(child_node)
        return child_node

    def best_child(self, param=1):
        return max(self.children, key=lambda c: (c.q() / c.n()) + param * math.sqrt(2 * math.log(self.n()) / c.n()))

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def rollout(self):  # Simulation de l'ensemble du jeu jusqu'à ce qu'un résultat soit obtenu : PARTIE EXPANSION
        current_rollout_state = self.state
        while current_rollout_state.result == 0:  # Tant que le jeu n'est pas terminé
            print("Current rollout node grille : ", current_rollout_state.board.grille, current_rollout_state.played_moves)
            possible_moves = lst_allowed_moves(current_rollout_state, current_rollout_state.played_moves < current_rollout_state.size)
            action = self.rollout_policy(possible_moves)  # Heuristique de choix pour l'action
            current_rollout_state.play_move(action)
            current_rollout_state.played_moves += 0.5
            current_rollout_state.change_turn()
        return current_rollout_state.result

    def rollout_policy(self, possible_moves):
        return random.choice(possible_moves)

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)


def ai_move_MCTS(G, itermax, joueur_actuel):
    root = NoeudMCTS(state=G)
    selected_node = root.best_action(itermax)
    return selected_node.parent_action


"""
def ai_move_MCTS(G, itermax, joueur_actuel):
    G_copy = Game(G.size, G.enabled_repetitions, False)
    G_copy.board.grille = deepcopy(G.board.grille)
    G_copy.change_turn()
    root = Noeud(deepcopy(G_copy))

    for _ in range(itermax):
        node = deepcopy(root)
        # G_copy = Game(node.G.size, node.G.enabled_repetitions, False)
        # G_copy.board.grille = deepcopy(node.G.board.grille)
        print("FST BCL ", node.G.turn)
        node.G.test()

        # Sélection
        while node.est_fully_expanded() and node.enfants:
            node = meilleur_noeud_ucb1(node)

        # Expansion
        if not node.est_fully_expanded():
            action = random.choice(node.actions_possibles())
            G_copy.play_move(action)
            G_copy.played_moves += 0.5
            node.maj(G_copy)
            print("iteration ", _, 'tour ', node.G.turn)
            node.G.test()
            enfant = Noeud(G_copy, node, action)
            node.ajouter_enfant(enfant)
            node = deepcopy(enfant)

        # Simulation
        joueur_simulation = joueur_actuel
        while True:
            actions_possibles = node.actions_possibles()
            if not actions_possibles:
                break
            action = random.choice(actions_possibles)
            G_copy.play_move(action)
            G_copy.played_moves += 0.5
            G_copy.change_turn()
            node.maj(G_copy)
            print("Iteration ", _)
            node.G.test()
            if G_copy.result == 1:
                if joueur_simulation == joueur_actuel:
                    node.victoires += 1
                node.visites += 1
                break
            joueur_simulation = 2 if joueur_simulation == 1 else 1

        # Propagation
        while node is not None:
            node.visites += 1
            node = node.parent

    return max(root.enfants, key=lambda n: n.visites).move_from
"""


def meilleur_noeud_ucb1(node):
    return max(node.enfants, key=lambda n: n.victoires / n.visites + math.sqrt(2 * math.log(node.visites) / n.visites))


def ai_move(G, is_new):
    return ai_move_MCTS(G, 15, G.turn)


def make_move_ai(G):
    G.play_move(ai_move(G, G.played_moves < G.size))
    G.played_moves += 0.5
    G.change_turn()
    G.board.afficher_grille()
