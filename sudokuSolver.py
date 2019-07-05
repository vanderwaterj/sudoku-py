import numpy as np
import sys
import copy

def main():
    original = Puzzle(open_board(sys.argv[1]))
    original.print_board()
    original.solve()

def open_board(file):
    f = open(file, "r")
    tempboard = []
    for x in (raw.strip() for raw in f):
        tempboard.append(np.asarray(list(x), dtype=np.uint8))
    return np.asarray(tempboard, dtype=np.uint8)

class Puzzle:
    def __init__(self, board):
        self.temp_board = board
        self.board = board
        self.board_size = len(self.board)
        self.possible_cell_vals = []

        self.update_possible_cell_vals()

    def get_row_vals(self, row):
        return np.asarray(list(filter(lambda a: a != 0, self.board[row,:])))

    def get_col_vals(self, col):
        return np.asarray(list(filter(lambda a: a != 0, self.board[:,col])))

    def get_sec_vals(self, sec): # sec is a tuple representing the cartesian coords of the sector from the top left
        secList = []
        for i in range(3):
            for j in range(3):
                secList.append(self.board[sec[1]*3+i][sec[0]*3+j])
        return np.asarray(list(filter(lambda a: a != 0, secList)))

    def get_possible_cell_vals(self, cell): # cell is a tuple representing the cartesian coords of the cell from the top left
        row_vals = self.get_row_vals(cell[0])
        col_vals = self.get_col_vals(cell[1])
        sec_vals = self.get_sec_vals((cell[1] // 3, cell[0] // 3))
        all_vals = np.concatenate([row_vals, col_vals, sec_vals])

        possible_cell_vals = []
        for i in range(1, 10):
            if i not in all_vals:
                possible_cell_vals.append(i)
        return np.asarray(possible_cell_vals)

    def update_possible_cell_vals(self):
        self.possible_cell_vals = []
        for i in range(self.board_size):
            tempRow = []
            for j in range(self.board_size):
                if self.board[i][j] == 0: # This may be problematic so check this later
                    tempRow.append(self.get_possible_cell_vals((i, j)))
                else:
                    tempRow.append([])
            self.possible_cell_vals.append(np.asarray(tempRow))

    def fill_lonely(self, my_board):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if len(self.possible_cell_vals[i][j]) == 1:
                    my_board[i][j] = self.possible_cell_vals[i][j][0]

    def solve(self):
        self.temp_board = self.board;
        board_copy = np.copy(self.board);
        while not self.check_solved():
            if not self.check_lonely():
                self.fill_lonely(self.board)
            if np.array_equal(self.board, board_copy):
                for i in range(len(self.get_possible_cell_vals(self.next_open_cell()))):
                    if self.solvable_given_assumption(self.next_open_cell(), self.get_possible_cell_vals(self.next_open_cell())[i]):
                        self.board = self.temp_board;
            else:
                board_copy = np.copy(self.board);
            self.update_possible_cell_vals()
    
    def next_open_cell(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.temp_board[i][j] == 0:
                    print(i,j)
                    return (i,j)

    def solvable_given_assumption(self, cell, val):
        self.temp_board[cell[0]][cell[1]] = val
        return False

    def check_lonely(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if len(self.possible_cell_vals[i][j]) == 1:
                    return False
        return True

    def check_solved(self):
        for i in range(self.board_size):
            for j in range(1, 1 + self.board_size):
                if j not in self.get_row_vals(i):
                    return False
        self.print_board()
        print('Puzzle solved.')
        return True

    def print_board(self):
        for row in self.board:
            for char in row:
                if (char != 0):
                    print(char, end="")
                else:
                    print('.', end="")
            print() 
        print()

if __name__ == "__main__":
    main()
