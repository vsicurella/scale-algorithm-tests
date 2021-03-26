from random import random
from scaleMaths import *

def symArray(arrayIn, centerInd=0, dbgPrint=False):
    grouping = arrayIn.copy()
    arrayOut = [grouping[centerInd]]
    grouping.remove(arrayOut[0])

    if (dbgPrint):
        print("removed center: {}".format(grouping))

    size = len(grouping)
    isOdd = size % 2
    valueGroupings = {}

    if (dbgPrint):
        print("This is {}.".format("odd" if isOdd else "even"))

    ## find groupings of values
    for num in grouping:
        if (num in valueGroupings.keys()):
            valueGroupings[num] += 1
        else:
            valueGroupings[num] = 1

    if (dbgPrint):
        print("Value Groupings:")
        print(valueGroupings)

    valueKeys = list(valueGroupings.keys())
    oddIndex = []
    for i in range(len(valueKeys)):
        if (valueGroupings[valueKeys[i]] % 2 == 1):
            oddIndex.append(i)

    if (dbgPrint):
        print("Unique values: {}".format(valueKeys))
        print("The odd index is {}".format("N/A" if len(oddIndex) == 0 else oddIndex[0]))

    ## test if can be arranged symmetrically
    valid = (not isOdd and len(oddIndex) == 0)
    valid += (isOdd and len(oddIndex) == 1)

    if (not valid):
        return []

    ## for finding odd index after sorting
    oddVal = -1
    if (isOdd):
        oddVal = valueKeys[oddIndex[0]]

    ## sort by grouping size
    valueKeys.sort(reverse=True)

    ## move odd group to end
    if (isOdd):
        valueKeys.remove(oddVal)
        valueKeys.append(oddVal)

    if (dbgPrint):
        print("Sorted Values: {}".format(valueKeys))

    ## add to array out symmetrically
    i = 0
    ind = 0
    decr = False
    while(i < len(grouping)):
        num = valueGroupings[valueKeys[ind]]
        if (ind != len(valueKeys) - 1):
            num = num // 2
        else:
            decr = True

        for n in range(num):
            arrayOut.append(valueKeys[ind])
            i += 1

        if (not decr):
            ind += 1
        else:
            ind -= 1

    return arrayOut

def simpleGroupings(period, allSizes, scaleSize):
    sizeInd = allSizes.index(scaleSize)
    grouping = [scaleSize]

    notesLeft = period - scaleSize
    subSizeInd = sizeInd - 1
    subSize = allSizes[subSizeInd]

    while (notesLeft > 0):
        while (subSize > notesLeft and subSizeInd > 0):
            subSizeInd -= 1
            subSize = allSizes[subSizeInd]

        q = int(notesLeft / subSize)

        for i in range(q):
            grouping.append(subSize)
            notesLeft -= subSize

    return grouping

def simpleAdjGroupings(period, allSizes, scaleSize):
    sizeInd = allSizes.index(scaleSize)
    grouping = [scaleSize]

    notesLeft = period - scaleSize
    subSizeInd = sizeInd
    subSize = allSizes[subSizeInd]

    while (notesLeft > 0):
        while (subSize > notesLeft and subSizeInd > 0):
            subSizeInd -= 1
            subSize = allSizes[subSizeInd]

        q = int(notesLeft / subSize)

        for i in range(q):
            grouping.append(subSize)
            notesLeft -= subSize

    return grouping

def cascadingGrouping(period, allSizes, scaleSize):
    sizeInd = allSizes.index(scaleSize)
    grouping = [scaleSize]

    notesLeft = period - scaleSize
    subSizeInd = sizeInd
    subSize = scaleSize

    while (notesLeft > 0):
        q = int(notesLeft / subSize)

        if (notesLeft <= subSize and notesLeft in allSizes):
            grouping.append(notesLeft)
            notesLeft = 0

        elif (q >= 2):
            num = q if notesLeft % subSize == 0 else q - (q % 2)
            for n in range(num):
                grouping.append(subSize)
                notesLeft -= subSize

        subSizeInd -= 1
        subSize = allSizes[subSizeInd]

    return grouping

def nestedSymmetricGrouping(period, allSizes, scaleSize):
    sizeInd = allSizes.index(scaleSize)
    grouping = [scaleSize]

    notesLeft = period - scaleSize
    subSizeInd = sizeInd
    subSize = scaleSize

    while (notesLeft > 0):
        q = int(notesLeft / subSize)

        if (notesLeft <= subSize and notesLeft in allSizes):
            grouping.append(notesLeft)
            notesLeft = 0

        elif (q >= 2):
            num = q if notesLeft % subSize == 0 else q - (q % 2)
            for n in range(num):
                grouping.append(subSize)
                notesLeft -= subSize

                # check if notesLeft can be divided equally by next size, retaining symmetry
                if (subSizeInd > 0):
                    sub2Ind = subSizeInd - 1
                    sub2Size = allSizes[sub2Ind]
                    q2 = notesLeft / sub2Size

                    if (q2 == int(q2)):
                        q2 = int(q2)
                        # check symmetry
                        groupSize = len(grouping) - 1
                        isOdd = groupSize % 2

                        if (q2 % 2 == 0):
                            for nr in range(q2):
                                grouping.append(sub2Size)
                                notesLeft -= sub2Size

                            return grouping


        subSizeInd -= 1
        subSize = allSizes[subSizeInd]

    return grouping

def complimentaryGrouping(period, allSizes, scaleSize):
    sizeInd = allSizes.index(scaleSize)
    grouping = [scaleSize]

    notesLeft = period - scaleSize
    subSizeInd = sizeInd
    subSize = scaleSize

    # used to prevent same size being added too many times
    q = int(notesLeft / subSize)
    num = q if notesLeft % subSize == 0 else q - (q % 2)
    n = 0

    while (notesLeft > 0):
        # check if notesLeft can be divided equally by next size, retaining symmetry
        if (subSizeInd > 0):
            sub2Ind = subSizeInd - 1
            sub2Size = allSizes[sub2Ind]
            q2 = notesLeft / sub2Size

            if (q2 == int(q2)):
                q2 = int(q2)
                # check symmetry
                groupSize = len(grouping) - 1

                if (groupSize == 0 or q2 % 2 == 0):
                    for nr in range(q2):
                        grouping.append(sub2Size)
                        notesLeft -= sub2Size

                    return grouping

        if (notesLeft <= subSize and notesLeft in allSizes):
            grouping.append(notesLeft)
            notesLeft = 0

        elif (q > 0 and n < num):
            grouping.append(subSize)
            notesLeft -= subSize
            n += 1

        else:
            subSizeInd -= 1
            subSize = allSizes[subSizeInd]

            q = int(notesLeft / subSize)
            num = q if notesLeft % subSize == 0 else q - (q % 2)
            n = 0

    return grouping

# compare groupings and return the one with the smallest range
def bestGrouping(period, allSizes, scaleSize, dbgPrint=False):
    groupings = []
    #groupings.append(cascadingGrouping(period, allSizes, scaleSize))
    groupings.append(nestedSymmetricGrouping(period, allSizes, scaleSize))
    groupings.append(complimentaryGrouping(period, allSizes, scaleSize))

    ranges = []
    for g in groupings:
        ranges.append(g[0] - g[len(g)-1])

    lengths = []
    for g in groupings:
        lengths.append(len(g))

    scores = []
    for g in range(len(groupings)):
        scores.append((ranges[g] + lengths[g])/2)

    smallestScore = 0
    for s in range(len(scores)):
        if (dbgPrint):
            name = "nested" if s == 0 else "complimentary"
            name += " score is {}, {}".format(scores[s], groupings[s])
            print(name)

        if (scores[s] < scores[smallestScore]):
            smallestScore = s

    return groupings[smallestScore]


def getGroupingOfMOS(period, generator, scaleSize, groupingFunction):
    frac = generator / period
    (sizes, gens) = getMOSData(frac)
    return groupingFunction(period, sizes, scaleSize)

def suggestedScaleSize(allSizes, preferLarger=False):
    size = -1
    dif1 = 10000
    for s in allSizes:
        dif2 = abs(7 - s)
        if (dif2 < dif1 or (preferLarger and dif2 <= dif1)):
            size = s
            dif1 = dif2

    return size

def randomArray(uniqueValues, maxVal, maxNum):
    array = []
    for i in range(uniqueValues):
        val = int(random() * maxVal)
        num = int(random() * maxNum)

        for n in range(num):
            array.append(val)

    return array
