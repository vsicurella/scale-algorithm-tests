from math import *

def array_sum(array):
    s = 0
    for n in array:
        s += n
    return s

def get_cf(num, maxdepth=20, round0thresh=10e-6):
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

    for x in range(2, int(number**0.5)+1):
        #print("{} % {} = {}".format(number, x, number % x))
        if (number % x == 0):
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

#dummy replacement for accidentally deleted function
def getMOSData(fracIn):
    cf = get_cf(fracIn)
    (dts, cidx) = diophantines(cf)

    ds = []
    ns = []

    for i in dts:
        ds.append(i[1][1])
        ns.append(i[1][0])

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

def edos_mos_scales(edo):
    cps = coprimes(edo)
    for p in cps:
        mosdata = getMOSData(p/edo)
        print("MOS Data of {}\{}".format(p, edo))
        d = mosdata[0]
        n = mosdata[1]
        for size in range(len(d)):
            print("{}\{}, ".format(n[size], d[size]), end="")
        print('\n')
