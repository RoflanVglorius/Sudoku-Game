import random
import board


def generate(start_amount):
    while True:
        amount = start_amount
        array = []
        boolean = []
        for i in range(9):
            buff = []
            buff2 = []
            for j in range(9):
                buff.append(0)
                buff2.append(True)
            array.append(buff)
            boolean.append(buff2)

        table = board.Board(array, boolean)
        while amount > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if table.get_cell_value(row, col) == 0:
                values = table.get_possible_values(row, col)
                if len(values) == 0:
                    break
                while True:
                    value = random.randint(1, 9)
                    if value in values:
                        table.set_value(row, col, value)
                        table.fix_value(row, col)
                        break
                amount -= 1
        row, col, values = table.find_optimal_cell()
        if len(values) == 0:
            continue
        else:
            break
    return table
