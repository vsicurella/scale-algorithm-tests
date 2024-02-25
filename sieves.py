from scaleGroupings import * 
from scaleMaths import *

import os

class ScaleData:
    def __init__(self, p_cents, g_cents, size):
        self.p_cents = p_cents
        self.g_cents = g_cents
        self.size = size

        self.scale = []

        self.p = clean(cents_to_ratio(self.p_cents), 6)
        self.g = clean(cents_to_ratio(self.g_cents), 6)

        deg = 0
        for n in range(size - 1):
            deg += self.g_cents
            if deg >= self.p_cents:
                deg -= self.p_cents
            if deg <= 0:
                break
            deg = clean(deg)
            self.scale.append(deg)

        self.scale.sort()
        self.scale.append(self.p_cents)

        self.steps = {}
        self.pattern = None

        lastDeg = 0
        for deg in self.scale:
            step = clean(deg - lastDeg, 6)
            if step not in self.steps:
                self.steps[step] = 1
            else:
                self.steps[step] += 1
            lastDeg = deg
        
        stepSizes = list(self.steps.keys())
        if len(stepSizes) == 1:
            return
        elif len(stepSizes) > 2:
            raise "Not a MOS!"

        stepSizes.sort()
        (self.s, self.L) = stepSizes
        
        self.ns = self.steps[self.s]
        self.nL = self.steps[self.L]

        self.pattern = "{}L{}s".format(self.nL, self.ns)


    def getGenApproximations(self):
        (dens, nums) = getAllConvergents(log(self.g)/log(self.p))

        self.g_cents = ratio_to_cents(self.g)
        index = 0
        # find the first one with an error less than 5 cents
        for i in range(len(nums)):
            index = i
            n_g = 1200.0 / dens[i] * nums[i]
            if abs(n_g - self.g_cents) < 5:
                break
        
        return "{}\{}".format(nums[index], dens[index])
    

class MosData:
    def __init__(self, g_cents, p_cents):
        self.g_cents = g_cents
        self.p_cents = p_cents

        cfDefaultDepth = 20
        cfRound0 = 1e-5

        ratio = self.g_cents / self.p_cents;
        inv =  clean(1.0 / ratio)

        if int(inv) == inv:
            cfRound0 = 1e-6
        
        (self.mos_pers, self.mos_gens) = getAllConvergents(ratio, cfDefaultDepth, cfRound0)

    def hasScaleSize(self, size):
        return size in self.mos_pers
    
    def getScale(self, size):
        return ScaleData(self.p_cents, self.g_cents, size)

class SieveData:
    def __init__(self, size, scales, tolerance):
        self.size = size
        self.scales = scales

        self.brackets = []

        # find generator ranges
        g_start = 0
        g_end = 0
        lastPattern = ""
        for i in range(len(scales) - 1):
            scale = scales[i]

            g = scale.g_cents

            if g_start == 0:
                g_start = g
                g_end = g
                lastPattern = scale.pattern
                continue
            
            if lastPattern == scale.pattern and clean(g - g_end) <= tolerance:
                g_end = g
                continue

            # new range starts
            self.addBracket(g_start, g_end, scale.pattern)
            
            lastPattern = scale.pattern
            g_start = g
            g_end = g

        # closing bracket
        lastScale = scales[len(scales) - 2]
        self.addBracket(g_start, lastScale.g_cents, lastScale.pattern)
        

    def addBracket(self, start, end, pattern):
        g_range = (clean(start), clean(end))
        self.brackets.append((g_range, pattern))


def build_sieves(scale_maps, tolerance):
    sizes = list(scale_maps.keys())

    sieves = []

    for size in sizes:
        sieve = SieveData(size, scale_maps[size], tolerance)
        sieves.append(sieve)

    return sieves



# check_sizes = [ 7, 10, 11, 17 ]
check_sizes = list(range(5, 31 + 1))

def build_data(period, g_res=0.01, g_start=0.0, g_end=600.0):

    p = period

    scale_map = {}
    g = g_start
    if g == 0:
        g = g_res

    while g < g_end:
        mosses = MosData(g, p)
        
        for size in check_sizes:
            if size not in scale_map:
                scale_map[size] = []

            # check for edos?

            if mosses.hasScaleSize(size):
                scales = scale_map.get(size)
                scale = mosses.getScale(size)
                if scale.pattern:
                    scales.append(scale)
        
        g = clean(g + g_res)

    return scale_map

def save_scales(scale_map):
    path = "C:/Users/Vincenzo/Documents/ScaleData/"

    try:
        os.mkdir(path)
    except:
        pass

    name = "scales_complete.csv"
    tempName = name + ".temp"

    filepath = path + name
    tempfile = path + tempName

    with open(tempfile, 'w') as file:

        line = "{},{},{},{},{},{},{},{}\n"
        header = line.format("size" ,"generator", "period" , "L", "s", "nL" ,"ns", "scale")
        file.write(header)
        
        sizes = scale_map.keys()
        for size in sizes:
            scales = scale_map[size]

            for scale in scales:
                scalestr = " ".join([ str(c) for c in scale.scale])
                file.write(line.format(scale.size, scale.g_cents, scale.p_cents, scale.L, scale.s, scale.nL, scale.ns, '\"{}\"'.format(scalestr)))

    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

    os.rename(tempfile, filepath)

def save_sieves(period, sieves):
    path = "C:/Users/Vincenzo/Documents/ScaleData/"

    try:
        os.mkdir(path)
    except:
        pass

    name = "sieves.csv"
    tempName = name + ".temp"

    filepath = path + name
    tempfile = path + tempName

    with open(tempfile, 'w') as file:
        line_temp = "{},{},{},{},{}\n"
        header = line_temp.format("size", "period", "start", "end", "pattern")
        file.write(header)
        
        for sieve in sieves:
            size = sieve.size

            for bracket in sieve.brackets:
                (g_range, pattern) = bracket
                line = line_temp.format(size, period, clean(g_range[0], 6), clean(g_range[1], 6), pattern)
                file.write(line)

    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

    os.rename(tempfile, filepath)


period = 1200.0
tolerance = 0.01

scale_data = build_data(period, tolerance)
# save_scales(scale_data)

sieve_data = build_sieves(scale_data, tolerance)
save_sieves(period, sieve_data)
