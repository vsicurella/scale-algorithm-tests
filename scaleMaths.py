from math import *
from primes import *

def clean(num, prec=10):
    return round(num * 10 ** prec) * (10 ** -prec)

def ratio_to_cents(ratio):
    return log(ratio)/log(2) * 1200

def cents_to_ratio(cents):
    return 2 ** (cents / 1200)

def array_sum(array):
    s = 0
    for n in array:
        s += n
    return s

def get_cf(num, maxdepth=20, round0thresh=1e-5):
    n = num
    cf = [] # the continued fraction
    for i in range(maxdepth):
        cf.append(int(n))
        n -= cf[i]

        if (n > round0thresh):
            n = 1 / n
        else:
            break

    return cf

def is_prime(number):
    if number == LAST_PRIME:
        return True

    if number < LAST_PRIME:
        return number in PRIMES

    sqroot = int(number**0.5)+1

    # slow, suboptimal
    if sqroot > LAST_PRIME:
        for i in range(LAST_PRIME, sqroot + 1):
            if number % i == 0:
                return False
        return True

    # fast lookup
    pindex = 0
    factor = PRIMES[0]
    while factor < sqroot:
        factor = PRIMES[pindex]
        if number % factor == 0:
            return False;

    return True;

def coprimes(numIn, getHalf=False):
    maxNum = numIn if not getHalf else int(numIn/2 + 1)
    out = []
    for i in range(2, maxNum):
        num = numIn
        mod = i
        while (mod > 1):
            num = num % mod
            (num, mod) = (mod, num)
        if (mod > 0):
             out.append(i)

    return out      

def prime_gen(maxn):
    primes = []

    for n in range(2, maxn):
        if (is_prime(n)):
            primes.append(n)

    return primes

def rational_gen(maxn):

    primes = prime_gen(int(maxn*1.5))
    rationals = []

    for p in primes:
        for n in range(1, maxn):
            if (n < p):
                rationals.append(n/p)
            else:
                break;

    return rationals;

def get_convergent(cf, depth=-1):
    if (depth >= len(cf) or depth < 0):
        depth = len(cf) - 1;

    (num, den) = (1, cf[depth])
    
    for d in range(depth, 0, -1):
        cfdigit = cf[d-1]
        num += cfdigit * den
        (num, den) = (den, num)
        
    return (den, num)

def diophantines(cfIn):
    if (len(cfIn) < 1):
        return

    dts = []
    cidx = []
    #it = 0
    
    triplet = (((-1+cfIn[0], 1),(1,0)),(cfIn[0],1))
    dts.append(triplet)
    #cidx.append(it)
    ((p0, p1),(g,p)) = triplet
    triplet = (((g,p),p1),(p1[0]+g,p1[1]+p))

    for d in range(1, len(cfIn)):
        for i in range(cfIn[d]):
            dts.append(triplet)
            #it += 1
            ((p0, p1),gp) = triplet
            if (d % 2 == 0):
                p0 = gp
            else:
                p1 = gp

            triplet = ((p0, p1), (p0[0]+p1[0], p0[1]+p1[1]))
        #cidx.append(it)

    return (dts, cidx)

def getAllConvergents(fracIn, cfMaxDepth=20, cf0Round=1e-5):
    cf = get_cf(fracIn, cfMaxDepth, cf0Round)

    ds = []
    ns = []

    if len(cf) > 2:
        (dts, cidx) = diophantines(cf)

        for i in dts:
            ds.append(i[1][1])
            ns.append(i[1][0])

    elif len(cf) == 2:
        ds = [1] + list(range(1, cf[1] + 1))
        ns = [0] + [1] * cf[1]

    return (ds, ns)

def get_convergent_indicies(cfIn):
    idx = [0]
    s = 0
    for d in cfIn[1:]:
        s += d
        idx.append(s)
    return idx

def et_scale(period, divisions, inCents=False):
    scale = []
    step = period ** (1.0 / divisions)
    for d in range(divisions):
        if (not inCents):
            scale.append(step ** (d+1))
        else:
            scale.append(log(step**(d+1))/log(2))
    return scale

def mos_scale(periodNum, genNum, size, doLog=False):
    p = periodNum if not doLog else log(periodNum)
    g = genNum if not doLog else log(genNum)
    #didn't acutally need

    # ratio = g/p;
    # if (doLog):
    #     ratio = log(g)/log(p)

    # g_cents = 


def compatible_edos(numNotes, highestDivision):
    edoMosSizes = []
    # edoMosSizes = [ 2:highestDivision = [ coprime MOS Sizes = [(n=[...], d=[...])...]...]...]
    # edoMosSize[0][0][0][0] = first numerator of first coprime of first edo
    for edo in range (numNotes+1, highestDivision+1):
        cprimes = coprimes(edo, True)
        mos = []
        for p in cprimes:
            mosdata=diophantines(get_cf(p/edo))
            #format into ([dens...], [nums...])
            dens = []
            nums = []
            
            for size in mosdata[0]:
                dens.append(size[1][1])
                nums.append(size[1][0])

            mos.append((dens, nums))
            
        edoMosSizes.append(mos)

    #find all MOS scales that support a size "numNotes"
    edosOut = []
    for edo in edoMosSizes:
        for mos in edo:
            if numNotes in mos[0]:
                edosOut.append((mos[0][len(mos[0])-1], mos[1][len(mos[1])-1]))

    #print results
    print("MOS Scales that support scale size {}:".format(numNotes))
    size = 0
    for edo in edosOut:
        if edo[0] != size:
            size = edo[0]
            print()
            print("S{}N{}\t".format(numNotes, size), end="")

        print("{}\{},\t".format(edo[1], size), end="")

    print()

    return edosOut

def printMOSOfET(numberOfTones):
    cp = coprimes(numberOfTones)
    for n in cp:
        data = getAllConvergents(n/numberOfTones)
        print("{}/{}:".format(n, numberOfTones))
        pgStr = ""
        sizeStr = ""
        for i in range(len(data[0])):
            pgStr += "{}/{}, ".format(data[1][i], data[0][i])
            sizeStr += "{}, ".format(data[0][i])

        print("\tP/G: " + pgStr)
        print("\tEDOs: " + sizeStr)
        print("\tSize: {}".format(len(data[0])))
        print()

def numSizesOfMOSinET(numberOfTones, filterTrivialSizes=True):
    cp = coprimes(numberOfTones, True)
    #sizeCount = list(zip(range(1, numberOfTones + 1), [0] * numberOfTones))
    seedsOfScaleSizes = {size: [] for size in range(1, numberOfTones + 1)}

    for n in cp:
        data = getAllConvergents(n/numberOfTones)
        [sizes, generators] = data
        seed = "{}/{}".format(n, numberOfTones)
        for i in range(1, len(sizes)):
            listOfSeeds = seedsOfScaleSizes[sizes[i]]
            if (seed not in listOfSeeds):
                listOfSeeds.append(seed)

    # count the size of each scale size bucket
    sizeCount = {x: len(seedsOfScaleSizes[x]) for x in seedsOfScaleSizes.keys()}

    # sort by bucket size
    sortedSizes = sorted(sizeCount.keys(), key=lambda s: sizeCount[s], reverse=True)

    print("Sizes of MOS scales of {}-ET:".format(numberOfTones))
    for s in sortedSizes:
        if (not filterTrivialSizes or (filterTrivialSizes and sizeCount[s] > 0 and s not in [1, 2, 3, numberOfTones])):
            print("{}x {}-note MOS scales".format(sizeCount[s], s))
            print("\tSeeds: {}\n".format(seedsOfScaleSizes[s]))

