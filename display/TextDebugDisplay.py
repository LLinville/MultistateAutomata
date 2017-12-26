from numpy import array

from automata.Cartesian2DAutomata import Cartesian2DAutomata
import automata.utils as utils
import pygame

automaton = Cartesian2DAutomata(1)
automaton.randomizeState()
#automaton.randomizeRules()
transitionTable = [[(1.0 * x / automaton.transitionSlots, 1.0 * y / automaton.transitionSlots)
                    for x in range(automaton.transitionSlots)]
                    for y in range(automaton.transitionSlots)]
automaton.setTransitionTable(transitionTable)

pygame.init()
screen = pygame.display.set_mode((400,400))


def drawTable(x, y):
    tableSurface = pygame.surfarray.make_surface(array(automaton.getTransitionTableImage()))
    screen.blit(tableSurface, (x, y))
    pygame.display.flip()


drawTable(0,0)
for a in range(100):
    print automaton.cells[0]
    automaton.step()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0