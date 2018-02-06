import collections
import sys
from random import randint

# Flags
HIDDEN = -1
MINE = -2
VISITED = -3

# Error Codes
CELL_ALREADY_SELECTED = 1
HIT_A_MINE = 2

Cell = collections.namedtuple('cell', ('r', 'c'))


class Minesweeper:

    def __init__(self, rows, cols, mines):
        self.cells_left = -1
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = self.create_board()
        self.add_mines()

    def create_board(self):
        self.cells_left = self.rows * self.cols
        return [[HIDDEN for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self, hidden):
        print()
        print(' ', end=' ')
        for i in range(len(self.board[0])):
            print(i+1, end=' ')
        print()
        for i in range(len(self.board)):
            print(i+1, end=' ')
            for j in range(len(self.board[0])):
                if self.board[i][j] == HIDDEN:
                    print('H', end=' ')
                elif self.board[i][j] == MINE:
                    if hidden:
                        print('H', end=' ')
                    else:
                        print('*', end=' ')
                elif self.board[i][j] == VISITED:
                    print('.', end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print()

    def add_mines(self):
        mine_positions = set()
        i = 0
        while i < self.mines:  # potentially endless loop
            position = self.get_random_cell()
            if position not in mine_positions:
                mine_positions.add(position)
                self.board[position.r][position.c] = MINE
                i += 1

    def get_random_cell(self):
        x = randint(0, len(self.board) - 1)
        y = randint(0, len(self.board[0]) - 1)
        return Cell(x, y)

    def visit_cell(self, cell):
        # if self.board[row][col] != HIDDEN:
        #     return

        def get_adjacent(r, c):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i or j) and 0 <= r + i < self.rows and 0 <= c + j < self.cols:
                        yield (r + i, c + j)

        initial_cell = True
        stack = [cell]
        visited = {cell}
        while stack:
            r, c = stack.pop()
            mines_adj = sum(self.board[nr][nc] == MINE for nr, nc in get_adjacent(r, c))
            if mines_adj:
                self.board[r][c] = mines_adj
                if initial_cell:
                    initial_cell = False
                    for nei in get_adjacent(r, c):
                        if self.board[nei[0]][nei[1]] in (HIDDEN, VISITED) and nei not in visited:
                            stack.append(nei)
                            visited.add(nei)
            else:
                self.board[r][c] = VISITED
                for nei in get_adjacent(r, c):
                    if self.board[nei[0]][nei[1]] in (HIDDEN, VISITED) and nei not in visited:
                        stack.append(nei)
                        visited.add(nei)

    def check_hit(self, cell):
        if self.board[cell.r][cell.c] == MINE:
            return HIT_A_MINE
        elif self.board[cell.r][cell.c] == HIDDEN:
            self.visit_cell(cell)
        else:
            return CELL_ALREADY_SELECTED

    def move_mine(self, cell):
        ran = self.get_random_cell()
        while self.board[ran.r][ran.c] == MINE:
            ran = self.get_random_cell()
        self.board[ran.r][ran.c] = MINE
        self.board[cell.r][cell.c] = HIDDEN

    def get_input(self):
        r_in = input('Enter a row: ')
        while not r_in.isdigit() or not (0 < int(r_in) <= self.rows):
            print("Invalid row. Try again.")
            r_in = input('Enter a row: ')
        c_in = input('Enter a column: ')
        while not c_in.isdigit() or not (0 < int(c_in) <= self.cols):
            print("Invalid column. Try again.")
            c_in = input('Enter a column: ')
        r = int(r_in) - 1  # sub 1 because grid is 0 indexed
        c = int(c_in) - 1
        cell = Cell(r, c)
        if self.board[r][c] == MINE:
            self.move_mine(cell)
        return cell

    def play(self):
        initial_move = True
        while self.cells_left:
            self.print_board(True)
            cell = self.get_input()
            if initial_move:
                initial_move = False
                self.move_mine(cell)
            res = self.check_hit(cell)
            if res == CELL_ALREADY_SELECTED:
                print('You\'ve already selected this cell. Try again.')
            elif res == HIT_A_MINE:
                self.print_board(False)
                print('You lose')
                return
        print('You win')


if __name__ == '__main__':
    cols = int(sys.argv[1])
    rows = int(sys.argv[2])
    mines = int(sys.argv[3])
    game = Minesweeper(rows, cols, mines)
    game.play()
