import sys

def main():
    my_puzzle = Puzzle(sys.argv[1])
    my_puzzle.printBoard()

    print(my_puzzle.getRow(0))
    print(my_puzzle.getCol(0))

class Puzzle:
    def __init__(self, filename):
        self.puzzle = open(filename, "r")
        self.board = []
        for row in (raw.strip() for raw in self.puzzle):
            self.board.append(row)
    
    def getRow(self, row):
        return list(self.board[row])

    def getCol(self, col):
        colStr = []
        for row in self.board:
            colStr.append(row[col])
        return colStr

    def getSec(self, sec):
        

    def printBoard(self):
        for row in self.board:
            print(row)

if __name__ == "__main__":
    main()