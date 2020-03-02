from scaleGroupings import *
from scaleMaths import *

def random_symmetry_test():
    arrays = []
    for i in range(2, 10):
        for n in range(10):
            arrays.append(randomArray(i + 1, 20, 7))

    symmetricArrays = []
    for i in range(len(arrays)):
        desc = "{}:\t{} original: {}".format(i + 1, len(arrays[i]) - 1, arrays[i])
        arraySym = symArray(arrays[i], 0, False)
        if (len(arraySym) > 0):
            desc += "\t\tsymmetric: {}".format(arraySym)
            symmetricArrays.append(arraySym)
        else:
            desc += "\t\tnotsymmetric"
        print(desc)

    print("Total arrays: {}\tSymmetric arrays: {}".format(len(arrays), len(symmetricArrays)))

def getEDOMOSData(maxEDO):
    edomosdata = {}

    for d in range(5, maxEDO+1):
        cps = coprimes(d, True)
        edodata = {}

        if (len(cps) > 0):
            for p in cps:
                mosdata = getMOSData(p / d)
                edodata[p] = mosdata

            edomosdata[d] = edodata

    return edomosdata

def mosDataTest():
    data = getEDOMOSData(12)
    edos = list(data.keys())
    for edo in edos:
        print("{}-EDO:".format(edo))
        primes = list(data[edo].keys())
        for p in primes:
            d = data[edo][p][0]
            n = data[edo][p][1]
            print("{}/{}: ".format(p, edo), end="")
            for size in range(len(d)):
                print("{}/{}, ".format(n[size], d[size]), end="")
            print()
        print()

def groupingTest(groupingFunction):
    data = getEDOMOSData(53)

    edos = list(data.keys())
    for edo in edos:
        print("{}-EDO:".format(edo))
        primes = list(data[edo].keys())
        for p in primes:
            allSizes = data[edo][p][0][1:]

            scaleSize = suggestedScaleSize(allSizes)
            grouping = groupingFunction(edo, allSizes, scaleSize)

            symmetric = symArray(grouping)

            print("{}/{}, {}: {}\tsymmetric: {}".format(p, edo, scaleSize, grouping, "YES" if len(symmetric) > 0 else "NO"))

        print()

def printMOSGrouping(period, generator, size, groupingFunction=nestedSymmetricGrouping):
    print("{}/{}, {}: {}".format(generator, period, size, getGroupingOfMOS(period, generator, size, groupingFunction)))

#printMOSGrouping(22, 9, 7, bestGrouping)

groupingTest(bestGrouping)