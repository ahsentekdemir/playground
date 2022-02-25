# Battleship Attempt 2

# Imports
import copy as c
from multiprocessing.sharedctypes import Value
import os
import random as rand
from typing import Callable, Tuple


def read_guess(guessed: Callable[[int, int], bool]) -> Tuple[int, int]:
    """read guess from user

    Args:
        guessed (Callable[[int, int], bool]): gets min-max value and returns tuple

    Returns:
        Tuple[int, int]: returns guesses
    """
    while True:
        # read the row and column
        guess_row = read_int("guess row:", max_value=5) -1
        guess_col = read_int("guess col", max_value=5) -1

        if not guessed(guess_row, guess_col):
            return guess_row, guess_col

        
        print("You've already guessed on that row! Try again.")

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

def battleship_run() -> int:
    """this method start game

    Returns:
        int: num of players
    """
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
 
class Game(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
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

    def create_matrix(self, max_x, max_y):
        """_summary_

        Args:
            max_x (_type_): _description_
            max_y (_type_): _description_

        Returns:
            _type_: _description_
        """
        matrix = list(range(max_x))
        for x in matrix:
            matrix[x] = list(range(max_y))
            for y in range(max_y):
                matrix[x][y] = "O"
        return c.deepcopy(matrix)

    def print_board(self, board_in):
        """_summary_

        Args:
            board_in (_type_): _description_

        Returns:
            _type_: _description_
        """
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
    
    def already_guessed(self, row: int, col: int) -> bool:
        """_summary_

        Args:
            row (int): _description_
            col (int): _description_

        Returns:
            bool: _description_
        """
        return self.board[row][col] == "X"

    def game_logic(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        guess_row, guess_col = read_guess(self.already_guessed)
        if (
            self.board[guess_row][guess_col]
            == self.board[self.ship_row][self.ship_col]
        ):
        
            return True
        else:
            if self.player_list[self.current_player - 1] > 0:
                print("Sorry, you missed!")
                self.board[guess_row][guess_col] = "X"
                self.board_visible[guess_row][guess_col] = "X"
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





def main() -> None:
    os.system("cls")
    player_count = read_int("pls how many players r gonna play", max_value=2)
    battle_ship = Game(player_count)
    battle_ship.main()

if __name__ == "__main__":
    main()