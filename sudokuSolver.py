import numpy as np
import sys
import time

def main():
    if len(sys.argv) == 2:
        try:
            original = Puzzle(open_board(sys.argv[1]))
            print("\nOriginal puzzle: ")
            original.print_board()
            original.solve()
        except FileNotFoundError:
            print(f"File \"{sys.argv[1]}\" not found.")
    else:
        print("Usage: python sudokuSolver.py PUZZLE.txt")

def stop():
    print("Found solution in %.4f seconds" % (time.time() - start_time))
    quit()

def open_board(file):
    f = open(file, "r")
    tempboard = []
    for x in (raw.strip() for raw in f):
        tempboard.append(np.asarray(list(x), dtype=np.uint8))
    return np.asarray(tempboard, dtype=np.uint8)

class Puzzle:
    def __init__(self, board):
        self.original = board
        self.board = board
        self.board_size = len(self.board)
        self.possible_cell_vals = []
        self.update_possible_cell_vals()

    def get_row_vals(self, row):
        return np.asarray(list(filter(lambda a: a != 0, self.board[row,:])))
    def get_col_vals(self, col):
        return np.asarray(list(filter(lambda a: a != 0, self.board[:,col])))
    def get_sec_vals(self, sec):
        secList = []
        for i in range(3):
            for j in range(3):
                secList.append(self.board[sec[1]*3+i][sec[0]*3+j])
        return np.asarray(list(filter(lambda a: a != 0, secList)))

    def get_possible_cell_vals(self, cell):
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

    def set_cell(self, cell, val):
        self.board[cell[0]][cell[1]] = val
        self.update_possible_cell_vals()

    def check_lonely(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if len(self.possible_cell_vals[i][j]) == 1:
                    return True
        return False

    def fill_lonely(self):
        while self.check_lonely():
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if len(self.possible_cell_vals[i][j]) == 1:
                        self.set_cell((i, j), self.possible_cell_vals[i][j][0])
        self.check_solved()

    def solve(self):
        self.fill_lonely()
        self.make_assumption(self.next_open_cell())

    def check_for_contradictions(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (len(self.possible_cell_vals[i][j]) == 0) and (self.board[i][j] == 0):
                    return True
        return False    

    def make_assumption(self, cell):
        self.check_solved()
        working_board = np.copy(self.board)
        for val in self.get_possible_cell_vals(cell):
            self.board = np.copy(working_board)
            self.set_cell(cell, val)
            self.fill_lonely()
            if self.check_for_contradictions():
                continue
            self.make_assumption(self.next_open_cell())
            
    def next_open_cell(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return (i,j)

    def check_solved(self):
        for i in range(self.board_size):
            for j in range(1, 1 + self.board_size):
                if j not in self.get_row_vals(i):
                    return False
        print("Solved puzzle:")
        self.print_board()
        stop()

    def print_board(self):
        for i, row in enumerate(self.board):
            for j, char in enumerate(row):
                if (char != 0):
                    print(char, end="")
                else:
                    print('.', end="")
                if (j + 1) % 3 == 0:
                    print(" ", end="")
            print()
            if (i + 1) % 3 == 0:
                print()

if __name__ == "__main__":
    start_time = time.time()
    main()