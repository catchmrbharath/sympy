"""
Interval Arithmetic for plotting.
This does not implement interval arithmetic accurately and 
hence cannot be used for other purposes. If you want to use interval 
arithmetic, use mpmath's interval arithmetic.
"""


from sympy.external import import_module
np = import_module('numpy')

# This module implements interval arithmetic using numpy and
#python floating points. The rounding up and down is not handled
#and hence this is not an accurate implementation of interval
#arithmetic.

#Q: Why use numpy? Why not simply use mpmath's interval arithmetic?
#A: mpmath's interval arithmetic simulates a floating point unit
#and hence is slow, while numpy evaluations are orders of magnitude
#faster. The plotting implemented using mpmath was slow. Hence, we 
#are using numpy.

#Q: Why create a seperate class for intervals? Why not use sympy's
#Interval Sets?
#A: The functionalities that will be required for plotting is quite
#different from what Interval Sets implement.

#Q: Why is rounding up and down according to IEEE754 not handled?
#A: It is not possible to do it in both numpy and python. An external
#library has to used, which defeats the whole purpose ie. speed. Also
#rounding is handled for very few functions in those libraries.

#Q Will my plots be affected?
#A Yes. The interval arithmetic module based on  suffers the same 
#problems as that of floating point arithmetic. Plotting based on 
#mpmath will also implemented for plots that would require high 
#precision. 

class interval(object):
    """ Represents an interval containing floating point as start and 
    end of the interval. The comparision of two intervals is done through
    a three - valued logic, True, False, and None."""
    
    def __init__(self, *args, **kwargs):
        self.is_valid = kwargs.pop('is_valid', True)
        if len(args) == 1:
            if isinstance(args[0], interval):
                self.start, self.end = args[0].start, args[0].end
            else:
                self.start = float(args[0])
                self.end = float(args[0])
        elif len(args) == 2:
            if args[0] < args[1]:
                self.start = float(args[0])
                self.end = float(args[1])
            else:
                self.start = float(args[1])
                self.end = float(args[0])

        else:
            raise ValueError("interval takes a maximum of two float values as \
                    arguments")
    
    def start(self):
        return self.start

    def end(self):
        return self.end

    @property
    def mid(self):
        return (self.start + self.end) / 2.0

    @property
    def width(self):
        return self.end - self.start

    def __repr__(self):
        return "interval(%f, %f)" % (self.start, self.end)

    def __str__(self):
        return "[%f, %f]" % (self.start, self.end)

    def __lt__(s, t):
        if isinstance(t, (int, float)):
            if s.end < t:
                return (True, s.is_valid)
            elif s.start > t:
                return (False, s.is_valid)
            else:
                return (None, s.is_valid)

        if isinstance(t, interval):
            if s.is_valid is False or t.is_valid is False:
                valid = False
            elif s.is_valid is None or t.is_valid is None:
                valid = None
            else:
                valid = True
            if s.end < t. start:
                return (True, valid)
            if s.start > t.end:
                return (False, valid)
            return (None, valid)
        else:
            return NotImplemented

    def __gt__(s, t):
        if isinstance(t, (int, float)):
            t = interval(t)
            return t.__lt__(s)
        elif isinstance(t, interval):
            return t.__lt__(s)
        else:
            return NotImplemented

    def __eq__(s, t):
        if isinstance(t, (int, float)):
            if s.start == t and s.end == t:
                return (True, s.is_valid)
            if s.__lt__(t)[0] is not None:
                return (False, s.is_valid)
            else:
                return (None, s.is_valid)
        if isinstance(t, interval):
            if s.is_valid is False or t.is_valid is False:
                valid = False
            elif s.is_valid is None or t.is_valid is None:
                valid = None
            else:
                valid = True
            if s.start == t.start and s.end == t.end:
                return (True, valid)
            if s.__lt__(t)[0] is not None:
                return (False, valid)
            return (None, valid)
        else:
            return NotImplemented

    def __ne__(s, t):
        if isinstance(t, (int, float)):
            if s.start == t and s.end == t:
                return (False, s.is_valid)
            if s.__lt__(t)[0] is not None:
                return (True, s.is_valid)
            else:
                return (None, s.is_valid)
        if isinstance(t, interval):
            if s.is_valid is False or t.is_valid is False:
                valid = False
            elif s.is_valid is None or t.is_valid is None:
                valid = None
            else:
                valid = True
            if s.start == t.start and s.end == t.end:
                return (False, valid)
            if not s.__lt__(t)[0] == None:
                return (True, valid)
            return (None, valid)
        else:
            return NotImplemented

    def __le__(s, t):
        if isinstance(t, (int, float)):
            if s.end <= t:
                return (True, s.is_valid)
            if s.start > t:
                return (False, s.is_valid)
            else:
                return (None, s.is_valid)

        if isinstance(t, interval):
            if s.is_valid is False or t.is_valid is False:
                valid = False
            elif s.is_valid is None or t.is_valid is None:
                valid = None
            else:
                valid = True
            if s.end <= t.start:
                return (True, valid)
            if s.start > t.end:
                return (False, valid)
            return (None, valid)
        else:
            return NotImplemented

    def __ge__(s, t):
        if isinstance(t, (int, float)):
            t = interval(t)
            return t.__le__(s)
        elif isinstance(t, interval):
            return t.__le__(s)

    def __add__(s, t):
        if isinstance(t, (int, float)):
            if s.is_valid:
                return interval(s.start + t, s.end + t)
            else:
                #invalid value. need not calculate further.
                #But should have the same invalid boolean
                #value
                return interval(s.start + t, s.end + t, is_valid = s.is_valid)

        elif isinstance(t, interval):
            start = s.start + t.start
            end = s.end + t.end
            if s.is_valid and t.is_valid:
                return interval(start, end)
            elif s.is_valid is False or t.is_valid is False:
                return interval(start, end, is_valid = False)
            else:
                return interval(start, end, is_valid = None)
        else:
            raise NotImplemented

    def __radd__(s, t):
        return s.__add__(t)

    def __sub__(s, t):
        if isinstance(t, (int, float)):
            if s.is_valid:
                return interval(s.start - t, s.end - t)
            else:
                return interval(s.start - t, s.end - t, is_valid = s.is_valid)
        elif isinstance(t, interval):
            start = s.start - t.end
            end = s.end - t.start
            if s.is_valid and t.is_valid:
                return interval(s.start - t.end, s.end - t.start)
            elif s.is_valid is False or t.is_valid is False:
                return interval(start, end, is_valid = False)
            else:
                return interval(start, end, is_valid = None)
        else:
            raise NotImplemented


    def __rsub__(s, t):
        if isinstance(t, (int, float)):
            if s.is_valid:
                return interval(t - s.end, t - s.start)
            else:
                return interval(t - s.end, t - s.start, is_valid = False)
        elif isinstance(t, interval):
            start = t.start - s.end
            end = t.end - start
            if s.is_valid and t.is_valid:
                return interval(start, end)
            elif s.is_valid is False or t.is_valid is False:
                return interval(start, end, is_valid = False)
            else:
                return interval(start, end, is_valid = None)

        else:
            raise NotImplemented


    def __rmul__(s, t):
        return s.__mul__(t)

    def __neg__(self):
        if self.is_valid:
            return interval(-self.end, -self.start)
        else:
            return interval(-self.end, -self.start, is_valid = False)

    def __mul__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            valid = True
            if s.is_valid is False or t.is_valid is False:
                valid = False
            elif s.is_valid is None or t.is_valid is None:
                valid = None


            if s in interval(0):
                #handle 0 * inf cases
                if not np.isfinite(t.start) or not np.isfinite(t.end):
                    return interval(-np.inf, np.inf, is_valid = valid)

            if t in interval(0):
                #handle 0 * inf cases
                if not np.isfinite(s.start) or not np.isfinite(s.end):
                    return interval(-np.inf, np.inf, is_valid = valid)

            if s.start >= 0:
                #positive * positive
                if t.start >= 0:
                    start = s.start * t.start
                    end = s.end * t.end
                    if np.isnan(start):
                        start = 0
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end, is_valid = valid)

                #positive * negative 
                elif t.end <= 0:
                    start = s.end * t.start
                    end = s.start * t.end
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = 0
                    return interval(start, end, is_valid = valid)
                
                #positive * both signs
                else:
                    start = s.end * t.start
                    end = s.end * t.end
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end, is_valid = valid)
            elif s.end <= 0:
                # negative * positive
                if t.start >= 0:
                    start = s.start * t.end
                    end = s.end * t.start
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = 0
                    return interval(start, end, is_valid = valid)
                #negative * negative
                elif t.end <= 0:
                    start = s.end * t.end
                    end = s.start * t.start
                    if np.isnan(start):
                        start = 0
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end, is_valid = valid)
                #negative * both sign
                else:
                    start = s.start * t.end
                    end = s.start * t.start
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end, is_valid = valid)
            else:
                #both signs * positive
                if t.start >= 0:
                    start = s.start * t.end
                    end = s.end * t.end
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end, is_valid = valid)
                #both signs * negative
                elif t.end <= 0:
                    start = s.end * t.start
                    end = s.start * t.start
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end, is_valid = valid)
                #both signs * both signs
                else:
                    inters = [s.start * t.start, s.end * t.start, \
                            s.end * t.end, s.start * t.end]
                    if any(np.isnan(inter) for inter in inters):
                        start = -np.inf
                        end = np.inf
                    else:
                        start = max(inters)
                        end = min(inters)
                    return interval(start, end, is_valid = valid)
        else:
            return NotImplemented
   
    def __contains__(self, t):
        t = interval(t)
        return self.start <= t.start and t.end <= self.end

    def __rdiv__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            return t.__div__(s)
        else:
            NotImplemented

    def __truediv__(s, t):
        return s.__div__(t)

    def __rtruediv__(s, t):
        t = interval(t)
        return t.__div__(s)


    def __div__(s, t):
        #Both None and False are handled
        if not s.is_valid:
            #Don't divide as the value is not valid
            return interval(-np.inf, np.inf, is_valid = s.is_valid)
        if isinstance(t, (int, float)):
            if not s.is_valid:
                #Don't divide as the value is not valid
                return interval(-np.inf, np.inf, is_valid = s.is_valid)
            else:
                if t == 0:
                    #Divide by zero encountered. valid nowhere
                    return interval(-np.inf, np.inf, is_valid = False)
                else:
                    return interval(s.start / t, s.end / t)

        elif isinstance(t, interval):
            if t.is_valid is False or s.is_valid is False:
                return interval(-np.inf, np.inf, is_valid = False)
            elif t.is_valid is None or s.is_valid is None:
                return interval(-np.inf, np.inf, is_valid = None)
            else:
                if s in interval(0):
                    if interval(0) in t:
                        return interval(-np.inf, np.inf, is_valid = None)
                    return interval(0)
               #denominator contains both signs, ie being divided by zero
               #return the whole real line with is_valid = None
                if t.start <= 0 and t.end >= 0:
                    return interval(-np.inf, np.inf, is_valid = None)

                #denominator negative
                if t.end < 0:
                    s  = -s
                    t = -t

                #denominator positive
                if s.start >= 0:
                    start = s.start / t.end
                    end = s.end / t.start
                    return interval(start, end)
                elif s.end <= 0:
                    start = s.start / t.start
                    end = s.end / t.end
                    return interval(start, end)
                else:
                    #both signs
                    start = s.start / t. start
                    end = s.end / t.start
                    return interval(start, end)

    def __pow__(s, t):
        if not s.is_valid:
            return s
        if isinstance(t, interval):
            return NotImplemented
        elif isinstance(t, (float, int)):
            if t == int(t):
                if t < 0:
                    return interval(1, 1) / s.__pow__(-t)
                else:
                    if t & 1:
                        return interval(s.start ** t, s.end ** t)
                    else:
                        #both non - positive
                        if s.end <= 0:
                            return interval(s.end ** t, s.start ** t)
                        elif s.start >= 0:
                            return interval(s.start ** t, s.end ** t)
                        else:
                            return interval(0, max(s.start ** t, s.end **t))
            else:
                return NotImplemented
