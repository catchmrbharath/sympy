from interval_arithmetic import interval
import numpy as np
"Library for interval arithmetic. Contains all the implemented functions for \
interval arithmetic"

#Monotonic
def exp(x):
    x = interval(x)
    return interval(np.exp(x.start), np.exp(x.end))

#Monotonic
def log(x):
    x = interval(x)
    if x.end <= 0:
        return inteval(-np.inf, -np.inf)
    elif x.start <= 0:
        return interval(-np.inf, np.log(x.end))
    else:
        return interval(np.log(x.start), np.log(x.end))

#Monotonic
def log10(x):
    x = interval(x)
    if x.end <= 0:
        return inteval(-np.inf, -np.inf)
    elif x.start <= 0:
        return interval(-np.inf, np.log10(x.end))
    else:
        return interval(np.log10(x.start), np.log10(x.end))

#Monotonic
def atan(x):
    x = interval(x)
    return interval(np.atan(x.start), np.atan(x.end))


#periodic
def sin(x):
    x = interval(x)
    if not (np.isfinite(x.start) and np.isfinite(x.end)):
        return interval(-1, 1)
    na, a = divmod(x.start, np.pi / 2.0)
    nb, b = divmod(x.end, np.pi / 2.0)
    start = min(np.sin(x.start), np.sin(x.end))
    end = max(np.sin(x.start), np.sin(x.end))
#    print na, nb
    if nb - na > 4:
        return interval(-1, 1)
    elif na == nb:
        return interval(start, end)
    else:
        #print na, nb
        if (na - 1) // 4 != (nb - 1) // 4:
            #sin has max
            end = 1
        if (na - 3) // 4 != (nb - 3) // 4:
            #sin has min
            start = -1
        return interval(start, end)

#periodic
def cos(x):
    x = interval(x)
    if not (np.isfinite(x.start) and np.isfinite(x.end)):
        return interval(-1, 1)
    na, a = divmod(x.start, np.pi / 2.0)
    nb, b = divmod(x.end, np.pi / 2.0)
    if x.start < 0:
        na = -1 - na
    if x.end < 0:
        nb = -1 - nb
    start = min(np.cos(x.start), np.cos(x.end))
    end = max(np.cos(x.start), np.cos(x.end))
    if nb - na > 4:
        #differ more than 2*pi
        return interval(-1, 1)
    elif na == nb:
        #in the same quadarant
        return interval(start, end)
    else:
        if (na) // 4 != (nb) // 4:
            #cos has max
            end = 1
        if (na - 2) // 4 != (nb - 2) // 4:
            #cos has min
            start = -1
        return interval(start, end)

def tan(x):
    return sin(x) / cos(x)

