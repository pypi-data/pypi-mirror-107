import pygame
from io import BytesIO
import requests


class board:
    def __init__(self, N):
        self.N = N
        self.colors = [(255,255,255), (255,153,204)]
        self.surface_sz = 640
        self.grid_sz = self.surface_sz // self.N
        self.surface_sz = self.N * self.grid_sz
        self.surface = None
        self.queen = self.read_queen_image()
        self.queen = pygame.transform.scale(self.queen, (self.grid_sz, self.grid_sz))
        self.offset = (self.grid_sz-self.queen.get_width()) // 2

        self.create_board()
    
    def read_queen_image(self):
        url = 'https://github.com/jhan15/nqviz/blob/master/nqviz/queen.png?raw=true'
        r = requests.get(url)
        dataBytesIO = BytesIO(r.content)
        queen_img = pygame.image.load(dataBytesIO)
        return queen_img
    
    def create_board(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.surface_sz, self.surface_sz))

        for row in range(self.N):
            color_ind = row % 2
            for col in range(self.N):
                grid = (col*self.grid_sz, row*self.grid_sz, self.grid_sz, self.grid_sz)
                self.surface.fill(self.colors[color_ind], grid)
                color_ind = (color_ind + 1) % 2
        
        pygame.display.flip()
    
    def place_queen(self, pos):
        x1 = pos[0] * self.grid_sz
        y1 = pos[1] * self.grid_sz
        x2 = (pos[0] + 1) * self.grid_sz
        y2 = (pos[1] + 1) * self.grid_sz

        self.surface.blit(self.queen, (x1+self.offset,y1+self.offset))
        pygame.display.update(x1,y1,x2,y2)
        pygame.event.pump()
        pygame.time.delay(500)
    
    def remove_queen(self, pos):
        x1 = pos[0] * self.grid_sz
        y1 = pos[1] * self.grid_sz
        x2 = (pos[0] + 1) * self.grid_sz
        y2 = (pos[1] + 1) * self.grid_sz
        color_ind = (pos[0] + pos[1]) % 2

        grid = (x1, y1, self.grid_sz, self.grid_sz)
        self.surface.fill(self.colors[color_ind], grid)
        pygame.display.update(x1,y1,x2,y2)
        pygame.event.pump()
        pygame.time.delay(500)

    def quit(self):
        pygame.quit()
