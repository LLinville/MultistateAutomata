import pygame
from pygame.locals import *
from automata.simplexnoise import *
from automata.MultistateAutomata import MultistateAutomata
import random
from automata.utils import *
from automata.RandomDistribution import RandomDistribution
import time

from automata.RuleGenerator import RuleGenerator

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

running = 1

ca = rownum = None

cellsWidth = 500

doneDrawing = False

#how many values each state can take
stateDepths = [2]

randomDistribution = RandomDistribution(min(stateDepths) - 1)
rulegenerator = RuleGenerator()

def randomSubstateProvider():
    #return random.randint(0, min(stateDepths) - 1)
    return randomDistribution.getValue()

def reset():
    global ca
    global randomDistribution
    randomDistribution = RandomDistribution(min(stateDepths) - 1)
    ca = MultistateAutomata(
        [[random.randint(0,stateDepth-1) for stateDepth in stateDepths] for i in range(cellsWidth)],
        [rulegenerator.getRandomSingleStateRule(stateDepth, True) for stateDepth in stateDepths],
        stateDepths,
        numCrossStateRules=0
    )
    global rownum
    rownum = 0
    screen.fill((0,0,0))
    for subrule in ca.ruleTable:
        for row in subrule:
            print row
        print "\n"
    print ca.crossStateRules
    #print randomDistribution.distribution

    global doneDrawing
    doneDrawing = False

def resetState():
    global ca
    global randomDistribution
    randomDistribution = RandomDistribution(min(stateDepths) - 1)

    automataCrossStateRules = ca.crossStateRules
    ca = MultistateAutomata(
        [[random.randint(0, stateDepth - 1) for stateDepth in stateDepths] for i in range(cellsWidth)],
        ca.ruleTable,
        stateDepths
    )

    ca.crossStateRules = automataCrossStateRules
    global rownum
    rownum = 0
    screen.fill((0, 0, 0))

    global doneDrawing
    doneDrawing = False

reset()

while running:
    startTime = time.time()
    for event in pygame.event.get():
        #print event.type
        if event.type == QUIT:
            running = 0

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                reset()
            if event.key == K_UP:
                resetState()
            if event.key == K_DOWN:
                rownum = 0
                doneDrawing = False

    if not doneDrawing:
        for cellIndex, cellValue in enumerate(ca.getCells()):
            screen.set_at((cellIndex, rownum), stateToColor(cellValue, max(stateDepths) - 1))

        pygame.draw.line(screen, (0, 0, 0), (500, rownum), (500 + len(ca.getCells()), rownum), 1)

        for neighborhoodIndex, neighborhoodStates in enumerate(ca.getNeighborhoods()):
            neighborhoodStates.sort()
            screen.set_at((neighborhoodIndex + 500, rownum), stateToRandomColor(ca.getNeighborhoods()[neighborhoodIndex]))

        lineDrawnTime = time.time()

        rownum += 1
        #rownum = rownum if rownum <=1000 else 0
        if rownum >= 1000:
            doneDrawing = True

        ca.step()

        stepTime = time.time()

        if rownum % 100 == 0:
            pygame.display.update(pygame.Rect(10, 10, 200, 200))

        flipTime = time.time()

    #print "\n\nline draw: " + str(lineDrawnTime - startTime) + "\nstep: " + str(stepTime - lineDrawnTime) + "\nflip: " + str(flipTime - stepTime)

pygame.quit()

