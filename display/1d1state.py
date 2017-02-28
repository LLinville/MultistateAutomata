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

cellsWidth = 8

#how many values each state can take
stateDepths = [4, 4]

def randomStateProvider(maxIndex):
    return [random.randint(0, maxIndex) for i in range(maxIndex)]

def reset():
    global ca
    ca = MultistateAutomata(
        [[random.randint(0,stateDepth-1) for stateDepth in stateDepths] for i in range(cellsWidth)],
        [indexedRandomMatrix(3, stateDepth, randomStateProvider) for stateDepth in stateDepths],
        stateDepths
    )
    global rownum
    rownum = 0
    screen.fill((0,0,0))
    print ca.crossStateRules

def resetState():
    global ca
    ca = MultistateAutomata(
        [[random.randint(0, stateDepth - 1) for stateDepth in stateDepths] for i in range(cellsWidth)],
        ca.ruleTable,
        stateDepths,
        ca.crossStateRules
    )
    global rownum
    rownum = 0
    screen.fill((0, 0, 0))

reset()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        if event.type == MOUSEBUTTONDOWN:
            reset()
        if event.type == KEYDOWN:
            resetState()

    for cellIndex, cellValue in enumerate(ca.getCells()):
        screen.set_at((cellIndex, rownum), stateToColor(cellValue, max(stateDepths)))

    pygame.draw.line(screen, (0, 0, 0), (500, rownum), (500 + len(ca.getCells()), rownum), 1)
    for mutatedIndex in ca.applyCrossStateRules():
        screen.set_at((mutatedIndex + 500, rownum), (255,255,255))

    rownum += 1
    rownum = rownum if rownum <=400 else 0
    ca.step()

    if rownum % 10 == 0:
        pygame.display.flip()

pygame.quit()
