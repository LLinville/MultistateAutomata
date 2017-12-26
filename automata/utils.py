import random
import math

randomColorOrder = [[[
    (random.randint(0,255),
     random.randint(0, 255),
     random.randint(0, 255)) for x in range(50)] for y in range(50)] for z in range(50)]

def indexByTuple(matrix, indexes):
    result = matrix[:]
    for index in indexes:
        result = result[index]
    return result

def indexedRandomMatrix(numDimensions, maxIndex, randomStateCreator):
    if numDimensions == 0:
        return randomStateCreator()
    return [indexedRandomMatrix(numDimensions - 1, maxIndex, randomStateCreator) for i in range(maxIndex)]

def randomState(stateDepths):
    return [random.randint(0, stateDepth - 1) for stateDepth in stateDepths]

def circularSlice(array, starting_index, ending_index):
    starting_index %= len(array)
    ending_index %= len(array)
    if starting_index > ending_index:
        part1 = array[starting_index:]
        part2 = array[:ending_index]
        return part1 + part2
    else:
        return array[starting_index:ending_index]

def stateToRandomColor(state):
    colorsFromStates = []
    if not isinstance(state[0], list):
        state = [state]
    for substate in state:
        substate.sort()
        x = y = z = 0
        if len(substate) >= 1:
            x = substate[0]
        if len(substate) >= 2:
            y = substate[1]
        if len(substate) >= 3:
            z = substate[2]

        colorsFromStates.append(randomColorOrder[x][y][z])
    return reduce(lambda x,y: (x[0]^y[0], x[1]^y[1], x[2]^y[2]), colorsFromStates)

def stateToColor(state, stateUpperBound):
    r = 1.0 * state[0] / stateUpperBound * 255
    g = b = r

    if len(state) is 2:
        g = 1.0 * state[1] / stateUpperBound * 255
        b = 0
    elif len(state) is 3:
        g = 1.0 * state[1] / stateUpperBound * 255
        b = 1.0 * state[2] / stateUpperBound * 255

    r, g, b = int(r), int(g), int(b)
    # if r+g+b > 200 * 3 :
    #     print r, b, g
    return (r, g, b)

def randomLines():
    grid = [[0 for i in range(10)] for j in range(10)]
    for layer in range(1000):
        if(random.random() < 0.5):
            randomRow = random.randint(0, 9)
            randState = random.randint(0, 9)
            grid[randomRow] = [randState for col in range(10)]
        else:
            randCol = random.randint(0, 9)
            randState = random.randint(0, 9)
            for row in range(10):
                grid[row][randCol] = randState

    return grid

def toXY(theta, radius):
    return radius * math.cos(theta), radius * math.sin(theta)

def toPolar(x, y):
    return math.atan2(y, x) / 2.0 / math.pi, math.sqrt(x * x + y * y)

def rotateXY(x, y, theta):
    polar = toPolar(x, y)
    return toXY(polar[0] + theta, polar[1])

def normalKernel(width, standardDeviations = 3):
    return [1.0 / math.sqrt(2 * math.pi) * math.exp(-(x - 1) ** 2 / 2) for x in [0 - width / 2]]