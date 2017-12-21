import pygame
from pygame.locals import *
from automata.Polar2DAutomata import Polar2DAutomata
from automata.Cartesian2DAutomata import Cartesian2DAutomata
from random import *
from numpy import *
import time

class AutomataDisplay:
    def __init__(self, screenDimensions, automaton):
        pygame.init()
        self.screen = pygame.display.set_mode(screenDimensions)
        self.automaton = automaton
        self.screenDimensions = screenDimensions
        self.resetDisplay()

    def run(self):
        running = True
        rownum = 0
        self.drawTable(300, 300)
        while running:
            if rownum == self.screenDimensions[1]:
                self.doneDrawing = True

            startTime = time.time()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = 0

                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.resetDisplay()
                        self.automaton.randomizeRules()
                        rownum = 0
                    if event.key == K_UP:
                        self.resetDisplay()
                        self.automaton.randomizeState()
                        rownum = 0
                    if event.key == K_DOWN:
                        rownum = 0
                        self.doneDrawing = False

            if not self.doneDrawing:
                for cellIndex, cellColor in enumerate(self.automaton.getCellColors()):
                    self.screen.set_at((cellIndex, rownum), cellColor)

                lineDrawnTime = time.time()

                rownum += 1
                # rownum = rownum if rownum <=1000 else 0
                if rownum >= self.screenDimensions[1]:
                    self.doneDrawing = True

                self.automaton.step()

                stepTime = time.time()

                if rownum % 100 == 0:
                    pygame.display.flip()

                flipTime = time.time()

                print "\n\nline draw: " + str(lineDrawnTime - startTime) + "\nstep: " + str(stepTime - lineDrawnTime) + "\nflip: " + str(flipTime - stepTime)

        pygame.quit()

    def drawTable(self, x, y):
        tableSurface = pygame.surfarray.make_surface(array(self.automaton.getTransitionTableImage()))
        self.screen.blit(tableSurface, (x, y))

    def resetDisplay(self):
        self.screen.fill((0, 0, 0))
        self.drawTable(300, 300)
        self.doneDrawing = False
        pygame.display.flip()


automaton = Cartesian2DAutomata(200)
transitionTable = [[(1.0 * x / automaton.transitionSlots, 1.0 * y / automaton.transitionSlots)
                    for x in range(automaton.transitionSlots)]
                    for y in range(automaton.transitionSlots)]
automaton.setTransitionTable(transitionTable)
automaton.randomizeState()
#automaton.randomizeRules()
display = AutomataDisplay((600,600), automaton)
display.run()
