import pygame
from pygame.locals import *
from automata.simplexnoise import *
from automata.MultistateAutomata import MultistateAutomata
import random
from automata.utils import *

pygame.init()
screen = pygame.display.set_mode((1000, 600))

running = 1

ca = rownum = None

cellsWidth = 400

def reset():
    global ca
    ca = MultistateAutomata((
        [[random.randint(0,1)] for i in range(cellsWidth)],
        [indexedRandomMatrix(3, 2)]
    ))
    global rownum
    rownum = 0
    screen.fill((0,0,0))

reset()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        if event.type == MOUSEBUTTONDOWN:
            reset()

    for substate in ca.getCells():
        for index, cellValue in enumerate(substate):
            value = cellValue
            screen.set_at((index, rownum), ((value*255)%256, (value*255)%256, (value*255)%256))

    rownum += 1
    rownum = rownum if rownum <=400 else 0
    ca.step()
    #ca.mutateCells(1)

    pygame.display.flip()

pygame.quit()
