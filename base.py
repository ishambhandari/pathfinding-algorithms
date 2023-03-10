import pygame

size = width, height = 900, 800
WIDTH = 900

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Nodebox:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width 
        self.y = col* width 
        self.color = WHITE
        self.neighbors = []
        self.width = width 
        self.total_rows = total_rows

    def get_pos(self):
        return self.row , self.col
    
    def is_closed(self):
        return self.color == GREY 

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == PURPLE
    def is_end(self):
        return self.color == RED 
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = GREY 

    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_start(self):
        self.color = PURPLE 
    def make_end(self):
        self.color = TURQUOISE 

    def make_path(self):
        self.color = RED 
    def draw(self, win):
        pygame.draw.rect(win, self.color,(self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows- 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self,other):
        return False

def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            nodebox = Nodebox(i,j,gap,rows)
            grid[i].append(nodebox)
    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))

        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))
def draw(win, grid, rows,width):
    win.fill(WHITE)
    for row in grid:
        for nodebox in row:
            nodebox.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y,x = pos
    row = y//gap
    col = x // gap
    return row,col
    

