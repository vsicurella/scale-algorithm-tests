from scaleMaths import *
from primes import *

def numFactorsOf(number, prime):
    if number % prime > 0:
        return 0
    
    reduced = number / prime

    return 1 + numFactorsOf(reduced, prime)

class Fraction:
    def __init__(self, numerator, denominator):
        self.n = numerator
        self.d = denominator
        self.value = numerator / denominator

    def getNumerator(self):
        return self.n

    def getDenominator(self):
        return self.d
    
    def isEqualTo(self, fraction):
        return self.n == fraction.n and self.d == fraction.d
    
    def toString(self):
        return "{}/{}".format(self.n, self.d)
    
    def toCents(self):
        return ratio_to_cents(self.value)

class Factorization:
    def __init__(self, numerator, denominator):
        self.factors = {}

        num_red = numerator
        num_i = 0

        while True:
            if num_red in PRIMES:
                self.factors[num_red] = 1
                break

            if num_i >= NUM_PRIMES:
                break

            factor = PRIMES[num_i]

            fNum = numFactorsOf(num_red, factor)
            if fNum > 0:
                self.factors[factor] = fNum
                quotient = factor ** fNum
                num_red /= quotient
            
            num_i += 1

        den_red = denominator
        den_i = 0

        # these will be negated
        while True:
            if den_red in PRIMES:
                if den_red in self.factors:
                    self.factors[den_red] -= 1
                else:
                    self.factors[den_red] = -1
                break

            if den_i >= NUM_PRIMES:
                break

            factor = PRIMES[den_i]

            fNum = numFactorsOf(den_red, factor)

            if fNum > 0:
                if factor in self.factors:
                    self.factors[factor] -= fNum
                else:
                    self.factors[factor] = -fNum
                quotient = factor ** self.factors[factor]
                den_red /= quotient

            den_i += 1
    
    def getPrimeList(self):
        return self.factors.keys()
    
    def getFraction(self):
        num = 1
        den = 1

        fNum = 0
        for prime in self.getPrimeList():
            fNum = self.factors[prime]
            if fNum > 0:
                num *= prime ** fNum
            elif fNum < 0:
                den *= prime ** (-fNum)

        return Fraction(num, den)


class ConvergentsList:
    def __init__(self, centsResolution=5, endPeriod=1200.0, maxFractions=25):
        self.data = {}
        self.cents = []
        self.ratios = []

        self.resolution = centsResolution
        self.period = endPeriod

        cents = centsResolution
        while cents <= endPeriod:
            self.cents.append(cents)

            ratio = cents_to_ratio(cents)
            self.ratios.append(ratio)

            (dens, nums) = getAllConvergents(ratio)

            fractions = []
            numFractions = maxFractions
            if len(dens) < numFractions:
                numFractions = len(dens)
                
            for i in range(numFractions):
                if nums[i] > 0:
                    fractions.append(Fraction(nums[i], dens[i]))
            
            self.data[cents] = fractions

            cents = cents + centsResolution


    def getCentsData(self, cents):
        if cents in self.cents:
            return self.data[cents]
        
        low = 0
        hi = 0

        for c in self.cents:
            if c < cents:
                low = c
            elif c > cents:
                hi = c
                break
        
        low_d = cents - low
        hi_d = hi - cents

        if low_d < hi_d:
            return self.data[low]
        return self.data[hi]
    
    def printList(self):
        for cents in self.data:
            fractions = self.data[cents]
            fractionStrings = [ f.toString() for f in fractions ]
            print("{}: {}".format(cents, fractionStrings))
    
    def FromData(data, period):
        newList = ConvergentsList(period, period)
        newList.data = data
        newList.cents = data.keys()
        newList.ratios = [ cents_to_ratio(x) for x in newList.cents ]
        return newList

def fractionInCentsWindow(cents, fraction, window):
    fractionCents = ratio_to_cents(fraction.value)
    diff = abs(cents - fractionCents)
    if diff >= window[0] and diff <= window[1]:
        return True
    return False

class QuantizeParams:
    def __init__(self, usedPrimes,  centsWindow=(5, 25)):
        self.primes = [ x for x in usedPrimes if is_prime(x) ]
        self.centsWindow = centsWindow


    def filterMap(self, convergentsList):
        data = {}

        for centsKey in convergentsList.data:
            
            fractions = convergentsList.data[centsKey]

            windowedFractions = [ x for x in fractions if fractionInCentsWindow(centsKey, x, self.centsWindow)]

            filteredFractions = []

            for fraction in windowedFractions:
                factors = Factorization(fraction.getNumerator(), fraction.getDenominator())
                fractionPrimes = factors.getPrimeList()
                
                fits = True
                for prime in fractionPrimes:
                    if prime not in self.primes:
                        fits = False
                        break

                if fits:
                    filteredFractions.append(fraction)

            if len(filteredFractions) > 0:
                data[centsKey] = filteredFractions

        return ConvergentsList.FromData(data, convergentsList.period)

class QuantizeMap:
    def __init__(self, convergentsList):
        self.data = []
        tones = {}

        for centsKey in convergentsList.data:
            fractions = convergentsList.data[centsKey]
            
            if len(fractions) == 1:
                tones[fractions[0].toString()] = fractions[0]
            else:
                for i in range(len(fractions)):
                    frac = fractions[i]

                    duplicate = False
                    for j in range(i, len(fractions)):
                        if frac.isEqualTo(fractions[j]):
                            duplicate = True
                            break
                    
                    if duplicate:
                        nextFrac = fractions[i+1]
                        tones[nextFrac.toString()] = nextFrac
                    else:
                        tones[frac.toString()] = frac

                    break
        
        self.tones = [ tones[frac] for frac in tones.keys() ]
        numTones = len(self.tones)

        # assuming list does not include unison or period
        unisonLow = self.tones[numTones - 1].toCents() - convergentsList.period
        unisonHigh = self.tones[0].toCents()

        self.data.append(0)
        self.data.append(unisonLow * 0.5)
        self.data.append(unisonHigh * 0.5)

        for i in range(numTones):
            if i == 0:
                prevTone = 0
            else:
                prevTone = self.tones[i-1].toCents()

            if i == (numTones - 1):
                nextTone = convergentsList.period
            else:
                nextTone = self.tones[i+1].toCents()

            tone = self.tones[i].toCents()

            low = tone - (tone - prevTone) * 0.5
            high = tone + (nextTone - tone) * 0.5
            
            self.data.append(tone)
            self.data.append(low)
            self.data.append(high)

        periodLow = convergentsList.period - (convergentsList.period - self.tones[numTones - 1].toCents()) * 0.5
        periodHigh = convergentsList.period + self.tones[0].toCents() * 0.5

        self.data.append(convergentsList.period)
        self.data.append(periodLow)
        self.data.append(periodHigh)

    def printMap(self):
        numTones = len(self.tones) + 2 # unison & octave
        for i in range(numTones):
            target = self.data[i * 3]
            low = self.data[i * 3 + 1]
            high = self.data[i * 3 + 2]
            print("{}\t{}\t{}".format(target, low, high))

    def printFloatMap(self):
        numTones = len(self.tones) + 2 # unison & octave
        for i in range(numTones):
            target = clean(self.data[i * 3], 3)
            low = clean(self.data[i * 3 + 1], 3)
            high = clean(self.data[i * 3 + 2], 3)
            print("{}, {}, {},".format(target, low, high))

period = 1200
steps = 12
resolution = period / steps
tolerance = resolution * 0.5

fullMap = ConvergentsList(resolution, period)

limit3_5 = QuantizeParams([2,3,5], (0, tolerance))
limit3_7 = QuantizeParams([2,3,7], (0, tolerance))
limit_bp = QuantizeParams([3,5,7,11,13], (0, tolerance))

map_limit_3_5 = limit3_5.filterMap(fullMap)
print("map_limit_3_5:")
print(map_limit_3_5.printList())
quantize_map_limit_3_5 = QuantizeMap(map_limit_3_5)
quantize_map_limit_3_5.printFloatMap()
print()

map_limit_3_7 = limit3_7.filterMap(fullMap)
print("map_limit_3_7:")
print(map_limit_3_7.printList())
quantize_map_limit_3_7 = QuantizeMap(map_limit_3_7)
quantize_map_limit_3_7.printFloatMap()
print()

map_bp = limit_bp.filterMap(fullMap)
print("map_bp:")
print(map_bp.printList())
quantize_map_bp = QuantizeMap(map_bp)
quantize_map_bp.printFloatMap()
print()

