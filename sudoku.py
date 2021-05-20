from collections import OrderedDict
from itertools import chain

class Tile():
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val
        if val != 0:
            self.solved = True
        else:
            self.solved = False
        self.sub = []
        self.cellID = ()
    
    def __repr__(self):
        return f'{self.val}'

class Board():
    def __init__(self, name):
        self.board = []
        
        file = open(name, 'r')
        for i, line in enumerate(file):
            values = list(map(int, line.split()))
            row = []
            for j, val in enumerate(values):
                row.append(Tile((i, j), val))
            self.board.append(row)

    def __str__(self):
        res = '___________________\n'
        for row in self.board:
            res += '|'
            for col in row:
                res += str(col.val) +'|'
            res += '\n'
        res += '-------------------'
        return res

    def updateCells(self):
        self.cells = OrderedDict()
        for k in range(0, 9, 3):
            for l in range(0, 9, 3):
                cell = []
                cellID = (k//3, l//3)
                for i in range(3):
                    for j in range(3):
                        cell.append(self.board[i+k][j+l].val)
                        if not self.board[i+k][j+l].cellID:
                            self.board[i+k][j+l].cellID = cellID
                self.cells[cellID] = cell

    def updateRows(self):
        self.rows = []
        for i in range(9):
            new_row = []
            for j in range(9):
                new_row.append(self.board[i][j].val)
            self.rows.append(new_row)

    def updateCols(self):
        self.cols = []
        for i in range(9):
            new_col = []
            for j in range(9):
                new_col.append(self.board[j][i].val)
            self.cols.append(new_col)

    def cell_list(self):
        self.cell_container = []
        for k in range(0, 9, 3):
            for l in range(0, 9, 3):
                cell = []
                for i in range(3):
                    for j in range(3):
                        cell.append(self.board[i+k][j+l])
                self.cell_container.append(cell)
    
    def row_list(self):
        self.row_container = self.board

    def col_list(self):
        self.col_container = []
        for i in range(9):
            col = []
            for j in range(9):
                col.append(self.board[j][i])
            self.col_container.append(col)

    def printCells(self):
        print('Cells View')
        for _, cell in self.cells.items():
            for val in cell:
                print(val, end='')
            print('')
    
    def printCols(self):
        print('Columbs View')
        for col in self.cols:
            for tile in col:
                print(tile, end='')
            print('')

    def printRows(self):
        print('Rows View')
        for row in self.rows:
            for tile in row:
                print(tile, end='')
            print('')

    def fill_possible_answers(self):
        for row in self.board:
            for tile in row:
                if not tile.solved:
                    tile.sub = []
                    for i in range(1, 10):
                        if self.check_row(i, tile.pos) and self.check_col(i, tile.pos) and self.check_cell(i, tile.cellID):
                            tile.sub.append(i)

    def check_row(self, num, pos):
        return num not in self.rows[pos[0]]

    def check_col(self, num, pos):
        return num not in self.cols[pos[1]]

    def check_cell(self, num, cellID):
        return num not in self.cells[cellID]

    def check_board_solved(self):
        return all([x.solved for row in self.board for x in row])

    def update(self):
        self.updateRows()
        self.updateCols()
        self.updateCells()
        self.fill_possible_answers()

    def solve_len_sub(self):
        self.update()
        while not self.check_board_solved():
            stuck = True
            for row in self.board:
                for cell in row:
                    if len(cell.sub) == 1:
                        cell.val = cell.sub.pop()
                        cell.solved = True
                        # print(f'L. Put {cell.val} in {cell.pos}')
                        self.update()
                        if stuck: stuck = False

            if stuck:
                return False
        return True

    def check_solved(self, cell):
        return all([x.solved for x in cell])
    
    def solve_only_option(self, name):
        self.update()
        if not hasattr(self, name+'_container') : eval('self.' + name +'_list()')
        did_somthing = False
        flag = True

        while flag:
            flag = False
            for cell in getattr(self, name + '_container'):
                if not self.check_solved(cell):
                    sub_list = [x for y in cell if not y.solved for x in y.sub]
                    counter = {}
                    for x in range(1,9):
                        if x in sub_list:
                            counter[x] = sub_list.count(x)
                    answers = []
                    for key, value in counter.items():
                        if value == 1:
                            answers.append(key)

                    if len(answers) != 0:
                        for answer in answers:
                            for tile in cell:
                                if answer in tile.sub:
                                    tile.val = answer
                                    tile.solved = True
                                    tile.sub = []
                                    self.update()
                                    did_somthing = True
                                    flag = True
                                    # print(f'{name}. Put {answer} in {tile.pos}')
                                    break
        return did_somthing

    def solve(self):
        while not self.check_board_solved():
            if not self.solve_len_sub():
                if not self.solve_only_option('row') and not self.solve_only_option('col') and not self.solve_only_option('cell'):
                    print('Hard sudoku. Got as far as it could')
                    break

sudoku = Board('hard.txt')
sudoku.solve()
if sudoku.check_board_solved(): print('Solved!')
print(sudoku)
