import random

def indexByTuple(matrix, indexes):
    result = matrix[:]
    for index in indexes:
        result = result[index]
    return result

def indexedRandomMatrix(numDimensions, maxIndex, randomStateCreator):
    if numDimensions == 1:
        return randomStateCreator(maxIndex)
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

    if len(state) > 1:
        g = 1.0 * state[1] / stateUpperBound * 255
    else:
        g = r

    if len(state) > 2:
        b = 1.0 * state[2] / stateUpperBound * 255
    else:
        b = r

    return (r, g, b)