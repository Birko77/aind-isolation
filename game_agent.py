"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # Maximize own posibilities and minimize opponents possibilities looking two moves into the future.
    # Expensive?

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves_1 = game.get_legal_moves(player)
    own_moves_2 = []
    for move in own_moves_1:
        own_moves_2.extend(game.forecast_move(move).get_legal_moves(player))

    opponent = game.get_opponent(player)
    opponent_moves_1 = game.get_legal_moves(opponent)
    opponent_moves_2 = []
    for move in opponent_moves_1:
        opponent_moves_2.extend(game.forecast_move(move).get_legal_moves(opponent))


    return float(len(own_moves_1) + len(own_moves_2) - len(opponent_moves_1) - len(opponent_moves_2))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # Maximize own move possibilities and don't get to the border of the board
    # at the border = -2

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    position = game.get_player_location(player)
    border_penalty = None
    if position == None:
        border_penalty = 0
    elif position[0] == 0 or position[0] == game.height-1 or position[1] == 0 or position[1] == game.width-1:
        border_penalty = 3
    else:
        border_penalty = 0

    return float(len(own_moves) - border_penalty)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # Try to limit the possible moves of the opponent.

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)) - 3 * len(game.get_legal_moves(game.get_opponent(player))))

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=20.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        if len(game.get_legal_moves())<=0:
            # print("No legal moves left on call to MinimaxPlayer.get_move()")
            return (-1, -1)
        best_move = game.get_legal_moves()[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        if len(game.get_legal_moves())<=0:
            # print("No legal moves left on call to MinimaxPlayer.minimax() -- THIS SHOULD NOT HAPPEN!")
            return (-1, -1)
        best_move = game.get_legal_moves()[0]

        for m in game.get_legal_moves():

            v = self.min_value(game.forecast_move(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
        return best_move

    def min_value(self, gameState, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(gameState, depth):
            return self.score(gameState, self)

        v = float("inf")
        for m in gameState.get_legal_moves():
            v = min(v, self.max_value(gameState.forecast_move(m), depth - 1))
        return v

    def max_value(self, gameState, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(gameState, depth):
            return self.score(gameState, self)

        v = float("-inf")
        for m in gameState.get_legal_moves():
            v = max(v, self.min_value(gameState.forecast_move(m), depth - 1))
        return v

    def terminal_test(self, gameState, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return gameState.is_loser(self) or gameState.is_winner(self) or depth == 0



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        if len(game.get_legal_moves())<=0:
            # print("No legal moves left on call to AlphaBetaPlayer.get_move()")
            return (-1, -1)
        best_move = game.get_legal_moves()[0]

        self.search_depth = 1

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                best_move = self.alphabeta(game, self.search_depth)
                self.search_depth = self.search_depth + 1

        except SearchTimeout:
            # print("Timed out! Returned: " + str(best_move))
            pass
            # pass # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        best_move = game.get_legal_moves()[0]
        if len(game.get_legal_moves())<=0:
            # print("No legal moves left on call to AlphaBetaPlayer.alphabeta() -- THIS SHOULD NOT HAPPEN!")
            return (-1, -1)
        for m in game.get_legal_moves():

            v = self.min_value(game.forecast_move(m), depth - 1, alpha, beta)
            # print(v)
            # print(len(game.get_legal_moves()))
            if v > best_score:
                best_score = v
                best_move = m
            #    α ← MAX(α, v)
            alpha = max(alpha, v)
        return best_move

    def min_value(self, gameState, depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(gameState, depth):
            return self.score(gameState, self)

        v = float("inf")
        for m in gameState.get_legal_moves():
            v = min(v, self.max_value(gameState.forecast_move(m), depth - 1, alpha, beta))
            #    if v ≤ α then return v
            #    β ← MIN(β, v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, gameState, depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(gameState, depth):
            return self.score(gameState, self)

        v = float("-inf")
        for m in gameState.get_legal_moves():
            v = max(v, self.min_value(gameState.forecast_move(m), depth - 1, alpha, beta))
            #    if v ≥ β then return v
            #    α ← MAX(α, v)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def terminal_test(self, gameState, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return gameState.is_loser(self) or gameState.is_winner(self) or depth <= 0
