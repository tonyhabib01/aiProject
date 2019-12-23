# -*- coding: utf-8 -*-
"""
Created on: 16 - 12 - 2019

@author: Tony Habib
"""
import random
from collections import namedtuple

GameState = namedtuple('GameState', 'to_move, utility, board, moves')
infinity = float('inf')
game_result = { 1:"Player 1 Wins", -1:"Player 2 Wins", 0:"It is a Tie" }

class Game:
    """To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                
                move = player(self, state)
                state = self.result(state, move)
                
                if self.terminal_test(state):
                    self.display(state)
                    print("Game Over.", game_result.get(self.utility(state, self.to_move(self.initial)), "Thank you for playing"))
                    restart=input("Type 1 to play again: ") # Asking the user to play again once the game is over
                    while (restart != "1"): #forcing the user for a valid input
                        restart=input("Enter a valid input: ")
                    if (restart == "1"):
                        startgame() #starts the game once the user put 1 as input.
                    return self.utility(state, self.to_move(self.initial))
                

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            print("\nThis is not a legal move, please play again\n")
            return state  # Illegal move has no effect
        
        board = state.board.copy() 
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()
        
    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k



def minimax_search(state, game):
    #Search game to determine best action; use minimax search

    player = game.to_move(state) # get the player to move

    def max_value(state): # max_value function to return v the value of a max node
        
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state): # min_value function to return v the value of a min node
        

        if game.terminal_test(state):
            return game.utility(state, player)
        v = +infinity
        for b in game.actions(state):
            v = min(v, max_value(game.result(state, b)))
        return v
                
    # Body of minimax:
    best_score = -infinity
    best_action = None
    
    #Body of the function minimax_search

    for a in game.actions(state): # Searching for the best action.
        temp = min_value(game.result(state, a))
        if (best_score < temp):
            best_score = temp
            best_action = a
     
    return best_action # returning the best action of the whole minimax algorithm


def alphabeta_search(state, game):
    #Search game to determine best action using the minimax alphabeta pruning search

    player = game.to_move(state) # get the player to move

    def max_value(state, alpha, betta): # max_value function to return v the value of a max node

        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, betta))
            if v >= betta:
                return v
            alpha = max(alpha,v)
        return v
            
    def min_value(state, alpha, betta): # min_value function to return v the value of a min node

        if game.terminal_test(state):
            return game.utility(state, player)
        v = +infinity
        for b in game.actions(state):
            v = min(v, max_value(game.result(state,b), alpha, betta))
            if v <= alpha:
                return v
            betta = min(betta, v)
        return v
    # Body of AlphaBetta
    alpha = -infinity
    betta = +infinity
    v = max_value(state, alpha, betta) # Giving the v the max value.
    best_action = None
    for a in game.actions(state): # Searching for the best node that is equalt to b and and assining the best action to it
        temp = min_value(game.result(state, a), alpha, betta)
        if max(alpha,temp) == v:
            best_action = a
    return best_action #returning the best action of alphabetta search function
        

"""Define the players"""

def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None

def minmax_player(game, state):
    """A player that chooses a legal move using minmax."""
    return minimax_search(state, game)

def alphabeta_player(game, state):
    """A player that chooses a legal move using minmax with alpha-beta pruning."""
    return alphabeta_search(state, game)
    
def human_player(game, state):
    """Human player: make a move by querying standard input."""
    
    print("Game board:")
    game.display(state)
    print("Available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state): 
        move_string = input('Your move? ') 
        while (True):
            try:
                move = eval(move_string)
                if move in game.actions(state): # Forcing the user to chose a legal move that is available in the actions state.
                    break
                else:
                    move_string = input("Invalid move, please enter a valid move: ") 

            except NameError:
                if move in game.actions(state): # If the user enters a character it forces him to chose a valid input
                    break
                else:
                    move_string = input("Invalid move, please enter a valid move: ")                  
    else:
        print("no legal moves: passing turn to next player")  
    return move

# play a game of tic tac toe
def startgame():
    ttt_game = TicTacToe()

    print("Welcome to TicTacToe Game:\n")
    print("Please choose one of the following AI to play against:\n")
    print("1. Random AI \n2. Minimax AI \n3. Alpha Beta Pruning AI \n")
    ai_choice = input("Your choice: ")
    while (ai_choice != "1" and ai_choice != "2" and ai_choice != "3"):
        print("\nInvalid input please enter a valid choice: \n")
        ai_choice = input("Your choice: ")

    if (ai_choice == "1"):
        print("")
        ttt_game.play_game(human_player,random_player)

    elif (ai_choice == "2"):
        print("")
        ttt_game.play_game(human_player,minmax_player)

    elif (ai_choice == "3") :
        print("")
        ttt_game.play_game(human_player,alphabeta_player)

startgame()