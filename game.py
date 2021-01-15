import generator
import copy
import time
import pickle
from ctypes import *


class Game:
    def __init__(self, amount):
        self.board = generator.generate(amount)
        self.amount = 81 - amount
        self.start_board = copy.deepcopy(self.board)
        self.moves = []

    def play(self, player):
        if player == 1:
            result = self.play_human()
            if result:
                print(self.board)
                print("Congratulations! You've won!")
            else:
                print("Impossible to solve or you've done mistakes")
        else:
            self.play_computer()

    def play_human(self):
        while self.amount > 0:
            print(self.board)
            print("Enter \'S\' to save the game, \'L\' to load the game or enter row and col:")
            answer = input()
            if answer == "S":
                print("Enter filename: ")
                with open(input(), "wb") as file:
                    pickle.dump(self, file)
                    print("Game saved")
                    exit(0)
            elif answer == "L":
                print("Enter filename: ")
                with open(input(), "rb") as file:
                    buff = pickle.load(file)
                    self.board = buff.board
                    self.moves = buff.moves
                    self.amount = buff.amount
                    self.start_board = buff.start_board
                    print("Game loaded")
                    continue
            row, col = map(int, answer.split())
            row -= 1
            col -= 1
            values = self.board.get_possible_values(row, col)
            if len(values) == 0:
                print("There is no possible values.")
                print(
                    "Would you like to continue, try again, generate a new board or quit the game? C/A/N/Q")
                answer = input()
                if answer == "Q":
                    return False
                elif answer == "A":
                    self.board = copy.deepcopy(self.start_board)
                elif answer == "N":
                    print("Enter amount of filled cells:")
                    amount = int(input())
                    self.board = generator.generate(amount)
                    self.start_board = copy.deepcopy(self.board)
                continue
            if not self.board.is_fixed(row, col):
                print("You cannot change fixed cells")
                continue
            while True:
                print("Choose values from the list: ", values)
                value = int(input())
                if self.board.get_cell_value(row, col) != 0:
                    self.amount += 1
                if value in values:
                    self.board.set_value(row, col, value)
                    self.amount -= 1
                    break
                else:
                    print("Value is not in the list")
        return True

    def play_computer(self):
        print(self.board)
        result, temp_board = self.make_move(self.board)
        self.print_at(9, 9, "\n")
        if result:
            print("Sudoku is solved:")
            print(temp_board)
            print("Moves: ")
            for i in range(len(self.moves) - 1, -1, -1):
                print(self.moves[i])
        else:
            print("Solution doesn't exist")

    def make_move(self, temp_board):
        current_board = copy.deepcopy(temp_board)
        row, col, values = current_board.find_optimal_cell()
        if row == 10 and col == 10 and len(values) == 0:
            return True, current_board
        if len(values) == 0:
            return False, set()
        for value in values:
            current_board.set_value(row, col, value)
            time.sleep(.1)
            self.print_at(row, col, value)
            result, buff = self.make_move(current_board)
            if result:
                self.moves.append("Row: {}, col: {}, value: {}".format(row, col, value))
                return result, buff
        self.print_at(row, col, 0)
        return False, set()

    def print_at(self, row, col, to_write):
        print_at(row + row // 3 + 4, 2 * (col + col // 3), str(to_write))


# Source: https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python

STD_OUTPUT_HANDLE = -11


class COORD(Structure):
    pass


COORD._fields_ = [("X", c_short), ("Y", c_short)]


def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

    s = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(s), len(s), None, None)
