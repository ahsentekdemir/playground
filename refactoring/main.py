# Battleship Attempt 2

# Imports
import copy as c
from multiprocessing.sharedctypes import Value
import os
import random as rand

"""
Defining the Game class to make it easier to 
understand the code further in the project
"""


def read_int(prompt: str, min_value: int = 1, max_value: int = 5) -> int:
    """read and integer between a min and max value.

        Args:
            prompt (str): prompt from user
            min_value (int): minimum value
            max_value (int): max value

        Returns:
            int: 
    """ 
    while True:
        line = input(prompt)
        try:
            value = int(line)
            if value < min_value:
                print(f"the min value is {min_value}! try again.")
            elif value > max_value:
                print(f"the mx value is {max_value}! try again.")
            else:
                return value
        except ValueError:
                print("Thats not number! try again!")
 
class Game(object):
    def __init__(self, players):
        self.guesses = 5
        self.player_list = []
        for player in range(players):
            self.player_list.append(self.guesses)
        self.current_player = 1
        self.board = self.create_matrix(5, 5)
        self.board_visible = c.deepcopy(self.board)
        self.ship_row = rand.randint(0, 4)
        self.ship_col = rand.randint(0, 4)
        self.guess_row = 0
        self.guess_col = 0

    """
    Defining the many methods that makes the game work,
    starting with the create_matrix where we take in the 
    boards max x and max y to define its size.
    """

    def create_matrix(self, max_x, max_y):
        matrix = list(range(max_x))
        for x in matrix:
            matrix[x] = list(range(max_y))
            for y in range(max_y):
                matrix[x][y] = "O"
        return c.deepcopy(matrix)

    """
    Defining the print_board function, here I respresent
    x as rows
    y as colums
    """

    def print_board(self, board_in):
        
        
        x = 0
        y = 0
        for column in board_in:
            y = 0
            for row in column:
                if y == 0:
                    print(" ", row, end=" ")
                elif y == len(board_in[x]):
                    print("", row, end="")
                else:
                    print(row, end=" ")
                y += 1
            print()
            x += 1
        return None

    """
    To avoid repeating the same code twice, I maderead_int method more generalized
    and made a seperate method to take care of if its row or column thats being inputed.
    That way I can make a robust input check without having to repeat code.
    I also use recursive methods here to avoid using while loops.
    """

    def player_guesses(self):
        if self.player_list[self.current_player - 1] == 0:
            return False
        else:
            print(
                "Player {} has {} guesses left.".format(
                    self.current_player, self.player_list[self.current_player - 1]
                )
            )

            print("Player {}: Guess row: ".format(self.current_player), end="")
            self.guess_row = read_int("guess row:", max_value=5) -1

            print("Player {}: Guess column: ".format(self.current_player), end="")
            self.guess_col = read_int("guess col", max_value=5) -1

            if self.board[self.guess_row][self.guess_col] == "X":
                print("You've already guessed on that row! Try again.")
                return self.player_guesses("\n")
            else:
                return None

    """
    Seperating out the game_logic to try to make the main function as readable as possible.
    This is also an exercise to practice writing recursive code instead of using while loops.
    """

    def game_logic(self):
        self.player_guesses()

        # I first did -1 here and spread out in the code. Very bad and confusing.
        if (
            self.board[self.guess_row][self.guess_col]
            == self.board[self.ship_row][self.ship_col]
        ):
            # if self.guess_row == self.ship_row and self.guess_col == self.ship_col:
            return True
        else:
            if self.player_list[self.current_player - 1] > 0:
                print("Sorry, you missed!")
                self.board[self.guess_row][self.guess_col] = "X"
                self.board_visible[self.guess_row][self.guess_col] = "X"
                self.player_list[self.current_player - 1] -= 1
                self.print_board(self.board_visible)

                if len(self.player_list) > 1:
                    self.current_player += 1
                if self.current_player > len(self.player_list):
                    self.current_player = 1
                return self.game_logic()
            else:
                print("Player {} ran out of guesses!".format(self.current_player))
                return False

    """
    Keeping the main function simple and easy to read by handling game logic
    above and using return to see the condition of the game.
    """

    def main(self):
        os.system("clear")
        self.print_board(self.board)
        self.board[self.ship_row][self.ship_col] = "S"
        if self.game_logic() == True:
            self.board[self.ship_row][self.ship_col] = "S"
            self.print_board(self.board)
            print(
                "Congratulations! Player {} sank the ship!".format(self.current_player)
            )
        else:
            print("Game over! Player {} has lost!".format(self.current_player))
            self.print_board(self.board)


"""
Defining the run function here to easier handle player input.
Doing it this way avoids using confusing while loops entirely.
"""


def battleship_run():
    os.system("clear")
    print("Please enter how many players are going to play:")
    players = input("\n")
    if len(players) > 0:
        if int(players) < 0:
            print("You can't have a negative amount of players. Try again.")
            return battleship_run()
        else:
            return int(players)
    else:
        print("You didn't type any player amount! Try again.")
        return battleship_run()


def main() -> None:
    os.system("cls")
    player_count = read_int("pls how many players r gonna play", max_value=2)
    battle_ship = Game(player_count)
    battle_ship.main()

if __name__ == "__main__":
    main()