import random

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