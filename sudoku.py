import sys
import math
import random
import copy

def main():
    # file = open("puzzle.txt", "r")
    file = open(sys.argv[1], "r")
    rowStrings = []

    for row in (raw.strip() for raw in file):
        rowStrings.append(list(row))

    print("Original Board")
    originalBoard = Board(rowStrings)
    originalBoard.printBoard()

    population = []

    for i in range(500):
        s = SolveAttempt(originalBoard)
        s.randomFill(originalBoard)
        population.append(s.getFitness())

    population.sort(key = lambda x : x["fitness"])

    print("Best attempt")
    population[0]["board"].printBoard()

    for i in range(500):  
        print(population[i])
    

class Board:
    def __init__(self, board):
        self.board = board
        self.boardSize = len(self.board)

    def printBoard(self):
        for row in self.board:
            print(row)

class SolveAttempt():
    def __init__(self, board):

        self.myBoard = copy.deepcopy(board)
        self.boardSize = board.boardSize

    def getRow(self, row):
        return self.myBoard.board[row]

    def getCol(self, col):
        colList = []
        for row in self.myBoard.board:
            colList.append(row[col])
        return colList

    def getSec(self, sec):
        secList = []

        secX = sec % 3
        secY = math.floor(sec / 3)

        for i in range(3):
            secList += self.myBoard.board[secY*3+i][secX*3:secX*3+3]
        return secList

    def getFitness(self):
        fitness = 0
        for i in range(self.boardSize):
            row = self.getRow(i)
            col = self.getCol(i)
            sec = self.getSec(i)

            for j in range(len(row)):
                if row.count(str(j)) > 1:
                    fitness += 1

            for k in range(len(col)):
                if col.count(str(k)) > 1:
                    fitness += 1

            for l in range(len(sec)):
                if sec.count(str(l)) > 1:
                    fitness += 1

        # self.printAttempt()
        return {"board" : self.myBoard, "fitness" : fitness}
    
    def randomFill(self, original):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if not original.board[i][j].isdigit():
                    self.myBoard.board[i][j] = str(random.randint(1,9))
    
    def printAttempt(self):
        print()
        for row in self.myBoard.board:
            print(row)
    
if __name__ == "__main__":
    main()