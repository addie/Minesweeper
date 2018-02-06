import collections
from random import randint
from colorama import init, Fore, Style


# Colors
Colors = {
    1: Fore.RED,
    2: Fore.BLUE,
    3: Fore.BLACK,
    4: Fore.GREEN,
    5: Fore.YELLOW,
    6: Fore.MAGENTA,
    7: Fore.CYAN,
    8: Fore.BLACK
}

# Flags
HIDDEN = -1
MINE = -2
VISITED = -3

# Error Codes
CELL_ALREADY_SELECTED = 1
HIT_A_MINE = 2

Cell = collections.namedtuple('cell', ('r', 'c'))


class Minesweeper:

    def __init__(self):
        self.rows = None
        self.cols = None
        self.mines = None
        self.board = None
        init()

    def create_board(self):
        self.board = [[HIDDEN for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self, hidden):
        print()
        print(' ', end='  ')
        for i in range(len(self.board[0])):
            if i < 9:
                print(i+1, end='  ')
            else:
                print(i+1, end=' ')
        print()
        for i in range(len(self.board)):
            if i < 9:
                print(i+1, end='  ')
            else:
                print(i+1, end=' ')
            for j in range(len(self.board[0])):
                if self.board[i][j] == HIDDEN:
                    print('H', end='  ')
                elif self.board[i][j] == MINE:
                    if hidden:
                        print('H', end='  ')
                    else:
                        print('*', end='  ')
                elif self.board[i][j] == VISITED:
                    print('.', end='  ')
                else:
                    c = self.board[i][j]
                    print(Colors[c] + str(c) + Style.RESET_ALL, end='  ')
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
                    if self.board[nei[0]][nei[1]] == HIDDEN and nei not in visited:
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
        return cell

    def set_up(self):
        print('Welcome to Minesweeper')
        level = input('(B)eginner, (I)ntermediate, (E)xpert, or (C)ustom? ')
        while level.lower() not in ('b', 'i', 'e', 'c'):
            level = input('(B)eginner, (I)ntermediate, (E)xpert, or (C)ustom? ')
        level = level.lower()[0]
        if level == 'b':
            self.mines = 10
            self.rows = self.cols = 9
        elif level == 'i':
            self.mines = 40
            self.rows = self.cols = 15
        elif level == 'e':
            self.mines = 99
            self.rows = self.cols = 20
        elif level == 'c':
            rows = input('Number of rows? ')
            while not rows.isdigit() or not (3 <= int(rows) <= 20):
                print('Invalid row number')
                rows = input('Number of rows? ')
            cols = input('Number of columns? ')
            while not cols.isdigit() or not (3 <= int(cols) <= 20):
                print('Invalid column number')
                cols = input('Number of columns? ')
            mines = input('Number of mines? ')
            while not mines.isdigit() or not (1 <= int(mines) <= 99):
                print('Invalid number of mines')
                mines = input('Number of mines? ')

            self.rows = int(rows)
            self.cols = int(cols)
            self.mines = int(mines)

    def play(self):
        self.set_up()
        self.create_board()
        self.add_mines()
        initial_move = True
        while True:
            self.print_board(True)
            cell = self.get_input()
            if initial_move and self.board[cell.r][cell.c] == MINE:
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
    # cols = int(sys.argv[1])
    # rows = int(sys.argv[2])
    # mines = int(sys.argv[3])
    game = Minesweeper()
    game.play()
