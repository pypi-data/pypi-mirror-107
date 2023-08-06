import pygame
from random import shuffle
from .board import board


class Nqueen:
    def __init__(self, N):
        self.N = N
        self.cb = board(self.N)
        self.num_cb = [[0] * self.N for _ in range(self.N)]
        self.finished = False
        self.start_procedure()
    
    def start_procedure(self):
        while True:
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            
            if not self.finished:
                if self.backtracking():
                    self.finished = True
    
        self.cb.quit()

    def backtracking(self):
        cols = [i for i in range(self.N)]
        shuffle(cols)

        if self.solver(cols, 0) == False:
            print('Solution does not exist!')
            return False

        return True

    def solver(self, cols, col):
        if col == self.N:
            return True
        
        rows = [i for i in range(self.N)]
        shuffle(rows)

        for row in rows:
            if self.is_safe(row, cols[col]):
                self.num_cb[row][cols[col]] = 1
                self.cb.place_queen((cols[col], row))

                if self.solver(cols, col+1) == True:
                    return True
                
                self.num_cb[row][cols[col]] = 0
                self.cb.remove_queen((cols[col], row))
        
        return False

    def is_safe(self, row, col):
        for i in range(self.N):
            if self.num_cb[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.num_cb[i][j] == 1:
                return False
        for i, j in zip(range(row, self.N, 1), range(col, -1, -1)):
            if self.num_cb[i][j] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, self.N, 1)):
            if self.num_cb[i][j] == 1:
                return False
        for i, j in zip(range(row, self.N, 1), range(col, self.N, 1)):
            if self.num_cb[i][j] == 1:
                return False
    
        return True

if __name__ == "__main__":
    nq = Nqueen(6)
    