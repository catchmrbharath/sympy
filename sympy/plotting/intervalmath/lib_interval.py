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
    if isinstance(x, (int, float)):
        if x <= 0:
            return interval(-np.inf, np.inf, is_valid = False)
        else:
            return interval(np.log(x))
    elif isinstance(x, interval):
        if not x.is_valid:
            return interval(-np.inf, np.inf, is_valid = x.is_valid)
        elif x.end <= 0:
            return interval(-np.inf, np.inf, is_valid = False)
        elif x.start <= 0:
            return interval(-np.inf, np.inf, is_valid = None)

        return interval(np.log(x.start), np.log(x.end))

#Monotonic
def log10(x):
    if isinstance(x, (int, float)):
        if x <= 0:
            return interval(-np.inf, np.inf, is_valid = False)
        else:
            return interval(np.log(x))
    elif isinstance(x, interval):
        if not x.is_valid:
            return interval(-np.inf, np.inf, is_valid = x.is_valid)
        elif x.end <= 0:
            return interval(-np.inf, np.inf, is_valid = False)
        elif x.start <= 0:
            return interval(-np.inf, np.inf, is_valid = None)
        return interval(np.log10(x.start), np.log10(x.end))
    else:
        raise NotImplemented

#Monotonic
def atan(x):
    if isinstance(x, (int, float)):
        return interval(np.arctan(x))
    elif isinstance(x, interval):
        start = np.arctan(x,start)
        end = np.arctan(x.end)
        return interval(start, end, is_valid = x.is_valid)
    else:
        raise NotImplemented


#periodic
def sin(x):
    if isinstance(x, (int, float)):
        return interval(np.sin(x))
    elif isinstance(x, interval):
        if not (np.isfinite(x.start) and np.isfinite(x.end)):
            return interval(-1, 1, is_valid = x.is_valid)
        na, a = divmod(x.start, np.pi / 2.0)
        nb, b = divmod(x.end, np.pi / 2.0)
        start = min(np.sin(x.start), np.sin(x.end))
        end = max(np.sin(x.start), np.sin(x.end))
        if nb - na > 4:
            return interval(-1, 1, is_valid = x.is_valid)
        elif na == nb:
            return interval(start, end, x.is_valid)
        else:
            if (na - 1) // 4 != (nb - 1) // 4:
                #sin has max
                end = 1
            if (na - 3) // 4 != (nb - 3) // 4:
                #sin has min
                start = -1
            return interval(start, end, x.is_valid)
    else:
        raise NotImplemented

#periodic
def cos(x):
    if isinstance(x, (int, float)):
        return interval(np.sin(x))
    elif isinstance(x, interval):
        if not (np.isfinite(x.start) and np.isfinite(x.end)):
            return interval(-1, 1, is_valid = x.is_valid)
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
            return interval(-1, 1, is_valid = x.is_valid)
        elif na == nb:
            #in the same quadarant
            return interval(start, end, is_valid = x.is_valid)
        else:
            if (na) // 4 != (nb) // 4:
                #cos has max
                end = 1
            if (na - 2) // 4 != (nb - 2) // 4:
                #cos has min
                start = -1
            return interval(start, end, is_valid = x.is_valid)
    else:
        raise NotImplemented

def tan(x):
    return sin(x) / cos(x)

#Monotonic
def sqrt(x):
    if isinstance(x, (int, float)):
        return interval(np.sqrt(x))
    elif isinstance(x, interval):
        if x.end < 0:
            return interval(-np.inf, np.inf, is_valid = False)
        elif x.start < 0:
            return interval(-np.inf, np.inf, is_valid = None)
        else:
            return interval(np.sqrt(x.start), np.sqrt(x.end), is_valid = x.is_valid)
    else:
        raise NotImplemented
