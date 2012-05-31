from sympy import *
from interval_arithmetic import interval
from sympy.utilities import lambdify
import matplotlib.pyplot as plt
import fractions
import time
import math
from lib_interval import interval_sin, interval_cos, interval_log, interval_exp, interval_log10, interval_tan
import numpy as np
#supports the following functions.
MPI = {'sin': interval_sin,
       'cos': interval_cos,
       'exp': interval_exp,
       'log': interval_log,
       'log10': interval_log10,
       'tan' : interval_tan}
x,y = symbols('x y')


func = lambdify((x, y),(y > tan(x)), MPI)

a = np.zeros( (1024, 1024) )
def plotImplicit(func, left, right, top, bottom):
    W = 512.0 # No. of horizontal pixels
    H = 512.0 # No. of vertical pixels
    k = fractions.gcd(W, H)
    k = int(math.log(fractions.gcd(k, 2**int(math.log(k, 2)))))
    IntervalList = []
    PlotList = []
    a = 0
    while a*2**k < W:
        b = 0
        xInter = interval(left + a * 2**k * (right - left)/W, left + (a + 1) * 2**k * (right - left) / W)
        while b*2**k < H:
            yInter = interval(bottom + b * 2**k * (top - bottom) / H, bottom + (b + 1) * 2**k * (top - bottom) / H)
            IntervalList.append([xInter,yInter])
            b += 1
        a += 1
    while k > 0 and len(IntervalList):
        IntervalList, plot = refinePixels(func, IntervalList)
        PlotList.extend(plot)
        k = k - 1
    ylist2 = []
    plt.figure()
    plt.axis([left, right, bottom, top])
    #PlotList.extend(IntervalList)
    xlist = []
    ylist = []
    for plots in PlotList:
        s, t = plots[0].start, plots[0].end
        u, v = plots[1].start, plots[1].end
        xlist.extend([s, s, t, t, None])
        ylist.extend([u, v, v, u, None])
    plt.fill(xlist,ylist, facecolor = 'b', alpha = 0.3, edgecolor = 'None')


        



def refinePixels(func, IntervalList):
    tempIntervalList = []
    plotList = []
    for intervalList in IntervalList:
        if func(intervalList[0], intervalList[1]) == True:
            plotList.append([intervalList[0], intervalList[1]])
        elif func(intervalList[0], intervalList[1]) == None:
            #divide into 4 sub regions
            s = intervalList[0].start
            t = intervalList[0].end
            avgx = intervalList[0].mid
            avgy = intervalList[1].mid
            u, v = intervalList[1].start, intervalList[1].end
            #create intervals
            a = interval(s, avgx)
            b = interval(avgx, t)
            c = interval(u, avgy)
            d = interval(avgy, v)
            tempIntervalList.append([a,c])
            tempIntervalList.append([a,d])
            tempIntervalList.append([b,c])
            tempIntervalList.append([b,d])
    return tempIntervalList, plotList

start_time = time.time()
plotImplicit(func, -np.pi / 2, np.pi / 2, 10.0, -10.0 )
print time.time() - start_time
plt.show()
