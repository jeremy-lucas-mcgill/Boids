import pygame
import numpy as np
import random as rd
from cell import Cell

#initalize pygame
pygame.init()

#constants and parameters
width = 1000
height = 800
grid_width = width//10
grid_height = height//10
cell_width = width // grid_width
cell_height = height // grid_height
timeDelay = 10
num_quads_per_side = 10
num_cells = 100
learning_rate = 0.1

#create the screen
screen = pygame.display.set_mode((width,height))

#create the grid
grid = np.zeros((grid_width, grid_height))

#utility functions
def initalizeCells(num):
    for _ in range(num):
        c = Cell(rd.randrange(0,grid_width,1), rd.randrange(0,grid_height,1), rd.random()/2 + 0.01)
        quad_width = grid_width/num_quads_per_side
        quad_height = grid_height/num_quads_per_side
        quad_width_num = int(c.pos[0] // quad_width)
        quad_height_num = int(c.pos[1] // quad_height)
        c.quad = [quad_width_num,quad_height_num]
        quads[quad_width_num][quad_height_num].add(c)
        cells.append(c)
def initalizeCellDirection():
    for c in cells:
        c.setDirection(rd.random() * 2 - 1, rd.random() * 2 - 1)
def setCellDirection():
    for c in cells:
        #find the average speed in their quad
        speed = 0
        direction = [0,0]
        num = len(quads[c.quad[0]][c.quad[1]])
        for nc in quads[c.quad[0]][c.quad[1]]:
            speed += nc.speed
            direction[0] += nc.direction[0]
            direction[1] += nc.direction[1]
        avg_speed = speed/num
        c.speed += (avg_speed - c.speed) * learning_rate
        #align direction
        avg_direction = [direction[0]/num, direction[1]/num]
        new_x_dir = c.direction[0] + (avg_direction[0] - c.direction[0]) * learning_rate
        new_y_dir = c.direction[1] + (avg_direction[1] - c.direction[1]) * learning_rate
        c.setDirection(new_x_dir,new_y_dir)

def moveCells():
    for c in cells:
        #make sure that cells wrap over the grid
        c.moveDirection()
        c.pos[0] = c.pos[0] % grid_width
        c.pos[1] = c.pos[1] % grid_height
        #check health
        if (c.health <= 0):
            cells.remove(c)
        #add cell to quadrant
        quad_width = grid_width/num_quads_per_side
        quad_height = grid_height/num_quads_per_side
        quad_width_num = int(c.pos[0] // quad_width)
        quad_height_num = int(c.pos[1] // quad_height)
        quads[c.quad[0]][c.quad[1]].remove(c)
        quads[quad_width_num][quad_height_num].add(c)
        c.quad = [quad_width_num, quad_height_num]
def drawCells():
    #draw cells
    for c in cells:
        pygame.draw.rect(screen,c.color, (c.pos[0] * cell_width, c.pos[1] * cell_height, cell_width, cell_height))
#initalize cells
cells = []
quads = [[set() for _ in range(num_quads_per_side)] for _ in range(num_quads_per_side)]
initalizeCells(num_cells)
initalizeCellDirection()
#simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    #control update speed
    pygame.time.delay(timeDelay)
    #blank black screen
    screen.fill((175,225,175))
    setCellDirection()
    moveCells()
    drawCells()
    #print([len(j) for i in quads for j in i])
    pygame.display.flip()
pygame.quit()