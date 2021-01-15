class Board:
    def __init__(self, board, fixed):
        self.__board = board
        self.__fixed = fixed

    def get_cell_value(self, row, col):
        return self.__board[row][col]

    def get_row_values(self, row, col):
        row_values = set()
        for i in range(9):
            if self.__board[row][i] != 0 and i != col:
                row_values.add(self.__board[row][i])
        return row_values

    def get_column_values(self, row, col):
        column_values = set()
        for i in range(9):
            if self.__board[i][col] != 0 and i != row:
                column_values.add(self.__board[i][col])
        return column_values

    def get_block_values(self, row, col):
        block_col = col // 3 * 3
        block_row = row // 3 * 3
        block_values = set()
        for i in range(3):
            for j in range(3):
                if self.__board[block_row + i][block_col + j] != 0 and (block_row + i != row and block_col + j != col):
                    block_values.add(self.__board[block_row + i][block_col + j])
        return block_values

    def __str__(self):
        string = ""
        for i in range(9):
            for j in range(9):
                string += str(self.__board[i][j]) + " "
                if j % 3 == 2 and j != 8:
                    string += "| "
            string += '\n'
            if i % 3 == 2 and i != 8:
                string += "---------------------\n"
        return string

    def set_value(self, row, col, value):
        self.__board[row][col] = value

    def fix_value(self, row, col):
        self.__fixed[row][col] = False

    def get_all_values(self, row, col):
        return self.get_block_values(row, col) | self.get_row_values(row, col) | self.get_column_values(row, col)

    def get_possible_values(self, row, col):
        possible = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        possible -= self.get_all_values(row, col)
        return possible

    def check_row(self, row, value):
        for i in range(9):
            if self.__board[row][i] == value:
                return False
        return True

    def check_column(self, col, value):
        for i in range(9):
            if self.__board[i][col] == value:
                return False
        return True

    def check_block(self, row, col, value):
        start_col = col // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.__board[start_row + i][start_col + j] == value:
                    return False
        return True

    def check_all(self, row, col, value):
        return self.check_block(row, col, value) and self.check_row(row, value) and self.check_column(col, value)

    def is_fixed(self, row, col):
        return self.__fixed[row][col]

    def find_optimal_cell(self):
        row = -1
        col = -1
        is_end = True
        optimal = 10
        opt_values = set()
        for i in range(9):
            for j in range(9):
                if self.__board[i][j] != 0:
                    continue
                values = self.get_possible_values(i, j)
                cur = len(values)
                if cur != 0:
                    is_end = False
                if cur == 0 and not is_end:
                    return 0, 0, set()
                if cur < optimal:
                    optimal = cur
                    row = i
                    col = j
                    opt_values = values
        if is_end:
            return 10, 10, set()
        return row, col, opt_values
