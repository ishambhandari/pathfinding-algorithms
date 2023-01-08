import pygame
from queue import PriorityQueue
from base import *

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

screen = pygame.display.set_mode(size)
pygame.init()

image_1 = pygame.image.load('djk.png').convert_alpha()
image_2 = pygame.image.load('astar.png').convert_alpha()

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        screen.blit(self.image,(self.rect.x,self.rect.y))
        
        return action



def display_page():
    alg_button1 = Button(100,200,image_1)
    alg_button2 = Button(100, 500, image_2)
    run = True
    while run:

        screen.fill((0,0,255))
        if alg_button1.draw():
            main(screen,width,'djk')
        if alg_button2.draw():
            main(screen, width,'as')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()

def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def final_path(came_from, end,draw):
    while end in came_from:
        end = came_from[end]
        end.make_path()
        draw()




def dijsktra(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score = {spot:float("inf") for row in grid for spot in row}
    g_score[start] = 0

    # f_score = {spot:float("inf") for row in grid for spot in row}
    # f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            final_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                # f_score[neighbor] = temp_g_score + hneighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((temp_g_score, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current!=start:
            current.make_closed()

def astar(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score = {spot:float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot:float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            final_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current!=start:
            current.make_closed()



        

    
def main(win,width,alg):
    ROWS = 50 
    grid = make_grid(ROWS,WIDTH)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            #LEFT CLICK
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,WIDTH)
                nodebox = grid[row][col]
                if not start and nodebox != end:
                    start = nodebox
                    start.make_start()
                elif not end and nodebox != start:
                    end = nodebox
                    end.make_end()

                elif nodebox != end and nodebox != start:
                    nodebox.make_barrier()
                
            #RIGHT CLICK
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos,ROWS,width)
                nodebox= grid[row][col]
                nodebox.reset()
                if nodebox == start:
                    start = None
                elif nodebox == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for nodebox in row:
                            nodebox.update_neighbors(grid)

                    if alg == 'djk':  
                        dijsktra(lambda: draw(win,grid,ROWS, width), grid, start, end)
                    else: 
                        astar(lambda: draw(win,grid,ROWS,width),grid,start,end)

                if event.key == pygame.K_n:
                    start = None
                    end = None
                    grid = make_grid(ROWS,WIDTH)


    pygame.quit()


# main(screen,WIDTH)
display_page()


