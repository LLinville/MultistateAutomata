import random

def indexByTuple(matrix, indexes):
    result = matrix
    for index in indexes:
        result = result[index]
    return result

def indexedRandomMatrix(numDimensions, maxIndex):
    #maxIndex -= 1 #to account for non-inclusive indexing
    if numDimensions == 1:
        return [random.randint(0, maxIndex-1) for i in range(maxIndex)]
    return [indexedRandomMatrix(numDimensions - 1, maxIndex) for i in range(maxIndex)]

def circularSlice(array, starting_index, ending_index):
    if starting_index > ending_index:
        part1 = array[starting_index:]
        part2 = array[:ending_index]
        return part1 + part2
    else:
        return array[starting_index:ending_index]