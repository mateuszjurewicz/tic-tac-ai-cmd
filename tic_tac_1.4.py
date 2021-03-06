# tic_tac_1.4.py
# by Mateusz Jurewicz (Mjure)
# 2016 08 16

# plays a perfect game of tic tac toe against a human opponent
# inspired by http://neverstopbuilding.com/minimax (salutations to them!)

# the AI uses a strategy called "minimax algorithm" and bears in mind
# the number of turns left, preferring to win quick and lose late.

# version 1.4 includes visualising the AI's perspective of the board
# by writing it into a separate file (what_AI_saw.txt)
# with minimax scores shown on the board

# file for storing the AI's perception of the board (with each tile having a certain score)
f = open("what_AI_saw.txt", "w")

# define the global, recursive minimax algorithm
def minimax(player, game):
    """ This is the minimax calculation which will be
    called by the AI player object's move() method """

    # if the game is over, return the score from AI's perspective,
    # taking number of turns already taken (aka depth) into consideration
    # (this is the end condition of the recursion)
    if game.is_over():
        # we need to pass an empty string here because minimax is expected
        # to return the easily readable board state
        # and then the AI_player writes it into a file
        empty_string = ""
        return game.minimax_score(player), empty_string

    # create lists holding possible moves and their scores
    scores = []
    moves = []

    # consider each possible game state within each next legal move and run minimax on it
    for move in game.legal_moves():

        # create a new, potential board as a copy of the current game's board
        # the [:] is important - otherwise we won't use a copy
        # of the original game's board but the actual board
        potential_board = game.board[:]

        # add the token (X or O) of the current player onto that tile
        potential_board[move] = game.active_player.token

        # create a new game, passing it that potential board
        # and incrementing the depth by 10 to show that a turn has passed
        potential_game = Game(game.player_one, game.player_two, potential_board, game.depth + 10)

        # switch potential game's active player attribute to be
        # the opposite of the current game's active player
        # (since we already took his turn for him/her)
        if game.active_player == game.player_one:
            potential_game.active_player = potential_game.player_two
        elif game.active_player == game.player_two:
            potential_game.active_player = potential_game.player_one
        else:
            print("\nError while switching potential game's active player\n")

        # Recursion:
        # add the minimax value of that potential game to the scores
        # and grab the easy to read string representation
        # of the board that will be returned by minimax
        score_to_append, readable_board = minimax(player, potential_game)
        scores.append(score_to_append)
        # add the currently considered move to the moves list,
        # at the same index as the corresponding score
        moves.append(move)

    # depending on whether it's the human or the AI making the current
    # choice of move, return the lowest or highest score from the scores list
    # store the chosen move in AI player's AI_chosen_move attribute

    # if the active player is human, choose the worst scoring move and return its score
    if game.active_player != player:

        # for the human the best option is the one with the lowest score
        # (worst choice from the perspective of the AI)
        worst_choice = min(scores)

        # find the index of that item
        worst_choice_index = scores.index(worst_choice)

        # find the corresponding move by the index and assign it
        # to the choice that AI will assume a human would make
        player.AI_chosen_move = moves[worst_choice_index]

        # create a nicely formatted version of the currently considered
        # board showing the scores for each untaken tile
        considered_board = game.board[:]
        for idx, move in enumerate(moves):
            considered_board[move] = scores[idx]

        # make the board easy to read
        easy_read_board = make_readable(considered_board, game.depth)

        # return the lowest score and the AI's perception of the board, in easy to read format
        return scores[worst_choice_index], easy_read_board

    # if the active player is the computer, choose the highest scoring move and return its score
    elif game.active_player == player:

        # for the AI the best option is the one with the highest score
        best_choice = max(scores)

        # find the index of the highest score
        best_choice_index = scores.index(best_choice)

        # find the highest-scoring move and assign it to the AI player's AI_chosen_move attribute
        player.AI_chosen_move = moves[best_choice_index]

        # create a nicely formatted version of the currently considered board
        # showing the scores for each untaken tile
        considered_board = game.board[:]
        for idx, move in enumerate(moves):
            considered_board[move] = scores[idx]

        # make the board easy to read
        easy_read_board = make_readable(considered_board, game.depth)

        # return the highest score and the AI's perception of the board, in easy to read format
        return scores[best_choice_index], easy_read_board

# a global function for making the AI's perception of the board easy to read
def make_readable(board, depth):
    """ Take the AI's model of the board and the number
    of turns taken (depth) and make them easy to read"""
    easy_read_board = ""
    easy_read_board += str(board[0]) + "\t" + str(board[1]) + "\t" + str(board[2])
    easy_read_board += "\n"
    easy_read_board += "\n" + str(board[3]) + "\t" + str(board[4]) + "\t" + str(board[5])
    easy_read_board += "\n"
    easy_read_board += "\n" + str(board[6]) + "\t" + str(board[7]) + "\t" + str(board[8]) + "\n\n" + "---" + str(depth) + "---" + "\n\n"

    return easy_read_board

# initialize global, constant variables:
# for tile values
X = "X"
O = "O"
EMPTY = " "

# for starting depth (number of taken turns)
START_DEPTH = 0

# for board size
NUM_SQUARES = 9

# for ways to win
WAYS_TO_WIN = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6))

# initialize an empty board
EMPTY_BOARD = []
for x in range(NUM_SQUARES):
    EMPTY_BOARD.append(EMPTY)

# define functions for getting the right user input
def ask_yes_no(question):
    """Ask a question for which the only answers are y and n."""
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response

def ask_number(question, low, high):
    """Ask for a number within a given range."""
    # remember that the upper bound of the range will not be a viable choice
    response = None
    while response not in range(low, high):
        response = input(question)
        # check if response can be converted to an integer
        try:
            response = int(response)
        except ValueError:
            print("You must enter a number between", low, "and", high, "... Try again.")
            # set response to be beyond the range, so that the loop condition evaluates to False
            response = high + 1
    return response

# define player object classes
class Human_Player(object):
    """ a human player in a game of tic-tac-toe """
    def __init__(self, token):
        self.token = token

    # this method mirrors the AI player's move method
    # in that it grabs the game itself, but here it doesn't actually use it
    def move(self, game):
        """ make the human choose a move (tile number) and return it"""
        chosen_move = None
        # grab a list of currently possible moves
        legal_moves = game.legal_moves()
        while chosen_move not in legal_moves:
            print("\nYou, the human, are now placing the", self.token, "tile.")
            # later versions with bigger boards can avoid use of "magic numbers" (0 and 9) here.
            chosen_move = ask_number(
                "\nWhich tile would you like to place your token on? (0-8)\n",
                0, 9)
        return chosen_move

class AI_Player(object):
    """ an AI player in a game of tic-tac-toe """
    def __init__(self, token):
        self.token = token
        # in this property we'll be storing the move (0-8) aka tile number,
        # which the AI will chose via the minimax function
        self.AI_chosen_move = None

    # define the minimax calculation defining the AI's next move
    def move(self, game):
        """ returns the chosen move of the AI given game-state """
        # run the minimax calculation passing the player object and the current game
        the_move, easy_read_board = minimax(self, game)
        # write the AI's perception of the board, in easy to read format and store it in a txt file
        f.write(easy_read_board)
        # return the global variable AI_chosen_move,
        # whose value will be changed by the minimax() function
        return self.AI_chosen_move

# define game object class
class Game(object):
    """ a game of tic tac toe, with 2 players and a board """
    def __init__(self, player_one, player_two, board, depth):
        self.player_one = player_one
        self.player_two = player_two
        self.board = board
        # we need to be able to define the number of turns
        # already taken (depth) here because in the minimax
        # algorithm we create potential games with some moves already taken
        self.depth = depth

        # depending on the choice of the user, set the
        # active player to be the player with the X token
        if player_one.token == X:
            self.active_player = player_one
        elif player_two.token == X:
            self.active_player = player_two
        else:
            print("\nError while setting active player, when initializing the game\n")

    # define a method for showing the current state of the board
    def display_board(self):
        """Display the game-board on the command line/terminal screen in readable format."""
        print("\n\t", self.board[0], "|", self.board[1], "|", self.board[2])
        print("\t", "---------")
        print("\n\t", self.board[3], "|", self.board[4], "|", self.board[5])
        print("\t", "---------")
        print("\n\t", self.board[6], "|", self.board[7], "|", self.board[8])

    # define a method to check if a given player has won the game
    def has_won(self, player):
        """ Find out if the player passed as argument is the winner, return Boolean value"""
        checked_token = player.token
        for sequence in WAYS_TO_WIN:
            if checked_token == self.board[sequence[0]] == self.board[sequence[1]] == \
                                self.board[sequence[2]]:
                return True
        return False

    # define a method for checking if the game is over (either player wins or it's a tie)
    def is_over(self):
        """ Find out if the game is over, return True or False"""
        if self.has_won(self.player_one):
            return True
        elif self.has_won(self.player_two):
            return True
        elif EMPTY not in self.board:
            return True
        else:
            return False

    # define a method that returns a list of all available moves left
    def legal_moves(self):
        """Create a list of legal moves."""
        moves = []
        for tile in range(NUM_SQUARES):
            if self.board[tile] == EMPTY:
                moves.append(tile)
        return moves

    # define a method for playing one turn of the game
    # (includes switching the active player of the game)
    def play_turn(self):
        """ play the next turn by grabbing a move from the active player """
        # grab a chosen tile from active (turn-taking) player
        # for minimax purposes we have to pass the game itself as argument here
        # (only needed for AI player)
        move = self.active_player.move(self)
        # and place the active player's token on that tile
        self.board[move] = self.active_player.token
        # switch active players
        self.switch_active_player()
        # increment depth (number of turns taken),
        # in multiples of ten for aesthetic reasons
        # (looks clearer when combined with the minimax score)
        self.depth += 10

    # define a method for switching the active (currently turn-taking) player
    def switch_active_player(self):
        """ Switch active players, with error checking """
        if self.active_player == self.player_one:
            self.active_player = self.player_two
        elif self.active_player == self.player_two:
            self.active_player = self.player_one
        else:
            print("\nError while switching active players\n")

    # define a method that will return the game's minimax score
    def minimax_score(self, current_player):
        """ Return the minimax strategy score of the current game-state for a given player """
        # define the current turn-taking player and his/her opponent
        if current_player == self.player_one:
            opponent_player = self.player_two
        else:
            opponent_player = self.player_one

        # player 2 is always the AI, so if he/she wins, we return
        # the most desirable score of 100, adjusting for the depth
        if self.has_won(current_player):
            return 100 - self.depth
        # else if the human player won, return the worst score of depth - 100
        elif self.has_won(opponent_player):
            return self.depth - 100
        # in case of a tie at the end, return neutral value of 0
        else:
            return 0

# play a new game of tic-tac-toe
# ask the player if they want to start (y/n)
human_starts = ask_yes_no("\nWould you like to take the first move?\n")

# create players and assign to them the appropriate tokens
if human_starts == "y":
    player_1 = Human_Player(X)
    player_2 = AI_Player(O)
elif human_starts == "n":
    player_1 = Human_Player(O)
    player_2 = AI_Player(X)
else:
    print("\nError has occurred during token assignment\n")

# create a new game, passing both player objects
# and an empty board as well as the starting depth of 0
current_game = Game(player_1, player_2, EMPTY_BOARD, START_DEPTH)

# start the main game loop
# while game isn't over, play the game's next turn
while not current_game.is_over():
    current_game.play_turn()
    # display the board so that the user can see what happened
    current_game.display_board()

# display final game result
if current_game.has_won(current_game.player_one):
    print("\nHuman has won!\n")
elif current_game.has_won(current_game.player_two):
    print("\nAI has won!\n")
elif EMPTY not in current_game.board:
    print("\nIt's a tie!\n")

# close the file with AI's perception of the boards
f.close()

# wait for user to finish the program' run
input("\n\nTo exit, press enter!")
