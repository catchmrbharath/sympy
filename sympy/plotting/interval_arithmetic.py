"""
Interval Arithmetic for plotting.
This does not implement interval arithmetic accurately and 
hence cannot be used for other purposes. If you want to use interval 
arithmetic, use mpmath's interval arithmetic.
"""


from sympy.external import import_module
np = import_module('numpy')
import warnings

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
    
    def __init__(self, *args):
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
        return "interval(%f, %f)" % (self.start, self.end)

    def __lt__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            if s.end < t. start:
                return True
            if s.start > t.end:
                return False
            return None
        else:
            return NotImplemented

    def __gt__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            return t.__lt__(s)
        else:
            return NotImplemented

    def __eq__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            if s.start == t.start and s.end == t.end:
                return True
            if not s.__lt__(t) == None:
                return False
            return None
        else:
            return NotImplemented

    def __ne__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            if s.start == t.start and s.end == t.end:
                return False
            elif not s.__le__( t) == None:
                return True
            return None
        else:
            return NotImplemented


    def __le__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            if s.end <= t.start:
                return True
            if s.start > t.end:
                return False
            return None
        else:
            return NotImplemented

    def __ge__(s, t):
        t = interval(t)
        return t.__le__(s)

    def __add__(s, t):
        t = interval(t)
        return interval(s.start + t.start, s.end + t.end)

    def __radd__(s, t):
        t = interval(t)
        return t.__add__(s)

    def __sub__(s, t):
        t = interval(t)
        return interval(s.start - t.end, s.end - t.start)

    def __rsub__(s, t):
        t = interval(t)
        return t.__sub__(s)


    def __rmul__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            return t.__mul__(s)
        else:
            raise NotImplemented

    def __neg__(self):
        return interval(-self.end, - self.start)


    def __mul__(s, t):
        if isinstance(t, (interval, int, float)):
            t = interval(t)
            if s in interval(0):
                #handle 0 * inf cases
                if not np.isfinite(t.start) or not np.isfinite(t.end):
                    return interval(-np.inf, np.inf)

            if t in interval(0):
                #handle 0 * inf cases
                if not np.isfinite(s.start) or not np.isfinite(s.end):
                    return interval(-np.inf, np.inf)

            if s.start >=0:
                #positive * positive
                if t.start >= 0:
                    start = s.start * t.start
                    end = s.end * t.end
                    if np.isnan(start):
                        start = 0
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end)

                #positive * negative 
                elif t.end <=0:
                    start = s.end * t.start
                    end = s.start * t.end
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = 0
                    return interval(start, end)
                
                #positive * both signs
                else:
                    start = s.end * t.start
                    end = s.end * t.end
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end)
            elif s.end <= 0:
                # negative * positive
                if t.start >= 0:
                    start = s.start * t.end
                    end = s.end * t.start
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = 0
                    return interval(start, end)
                #negative * negative
                elif t.end <= 0:
                    start = s.end * t.end
                    end = s.start * t.start
                    if np.isnan(start):
                        start = 0
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end)
                #negative * both sign
                else:
                    start = s.start * t.end
                    end = s.start * t.start
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end)
            else:
                #both signs * positive
                if t.start >= 0:
                    start = s.start * t.end
                    end = s.end * t.end
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end)
                #both signs * negative
                elif t.end <= 0:
                    start = s.end * t.start
                    end = s.start * t.start
                    if np.isnan(start):
                        start = -np.inf
                    if np.isnan(end):
                        end = np.inf
                    return interval(start, end)
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
                    return interval(start, end)
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

    def __div__(s, t):
        t = interval(t)
        #Numerator is 0 
        if s in interval(0):
            if interval(0) in t:
                return interval(-np.inf, np.inf)
            return interval(0) 
       #denominator contains both signs
        if t.start < 0 and t.end > 0:
           return interval(-np.inf, np.inf) 

       #divide by zero
        if t in interval(0):
            if s.start < 0 and s.end > 0:
                return interval(-np.inf, np.inf)
           #Numerator is always positive
            if s.start >= 0:
                start = s.start / t.end
                return interval(0, np.inf)
            #Numerator is always negative
            if s.end <= 0:
                end = s.end / t.end
                return interval(-np.inf, 0)

        #denominator is non positive
        if t.end <= 0:
            s = -s
            t = -t

        #denominator is non negative and start = 0
        if t.start == 0:
            #numerator both signs
            if s.start < 0 and s.end > 0:
                return interval(-np.inf, np.inf)
            #numerator positive
            if s.start >=0:
                start = s.start / t.end
                return interval(start, np.inf)
            #numerator negative
            if s.end <= 0:
                end = s.end / t.end
                return interval(-np.inf, end)
        else:
            if s.start >= 0:
                start = s.start / t.end
                end = s.end / t.start
                #handle inf / 0 and inf / inf
                if np.isnan(start):
                    start = 0
                if np.isnan(end):
                    end = np.inf
                return interval(start, end)
            elif s.end <= 0:
                start = s.start / t.start
                end = s.end / t.end
                if np.isnan(start):
                    start = -np.inf
                if np.isnan(end):
                    end = 0
                return interval(start, end)
            else:
                start = s.start / t.start
                end = s.end / t.start
                if np.isnan(start):
                    start = -np.inf
                if np.isnan(end):
                    end = np.inf
                return interval(start, end)

    def __pow__(s, t):
        if isinstance(t, interval):
            return NotImplemented
        elif isinstance(t, (float, int)):
            if t == int(t):
                return interval(s.start**t, s.end ** t)




#################################################################
#Tests
#################################################################
def test_interval():
    assert interval(1) == interval(1, 1)
    assert interval(1, 2) == interval(1, 2)
    assert (interval(1,1.5) == interval(1, 2)) == None
    assert (interval(0, 1) == interval(2, 3)) == False
    assert (interval(0, 1) == interval(1, 2)) == None
    assert (interval(1, 2) != interval(1, 2)) == False
    assert (interval(1, 3) != interval(2, 3)) == None
    assert (interval(1, 3) != interval(-5, -3)) == True
    inter = interval(-5, 5)
    assert 0 in inter
    assert -5 in inter
    assert 5 in inter
    assert interval(0, 3) in inter
    assert interval(-6, 2) not in inter
    assert -5.05 not in inter
    assert 5.3 not in inter
    interb = interval(-np.inf, np.inf)
    assert 0 in inter
    assert inter in interb
    assert interval(0, np.inf) in interb
    assert interval(-np.inf, 5) in interb
    assert interval(-1e50, 1e50) in interb

def test_interval_add():
    assert interval(1, 2) + interval(2, 3) == interval(3, 5)
    assert 1 + interval(1, 2) == interval(2, 3)
    assert interval(1, 2) + 1 == interval(2, 3)
    assert 1 + interval(0, np.inf) == interval(1, np.inf)
    assert 1 + interval(-np.inf, np.inf) == interval(-np.inf, np.inf)

def test_interval_inequality():
    assert (interval(1, 2) < interval(3, 4)) == True
    assert (interval(1, 2) < interval(2, 4)) == None
    assert (interval(1, 2) < interval(-2, 0)) == False
    assert (interval(1, 2) <= interval(2, 4)) == True
    assert (interval(1, 2) <= interval(1.5, 6)) == None
    assert (interval(2, 3) <= interval(1, 2)) == None
    assert (interval(2, 3) <= interval(1, 1.5)) == False
    assert (interval(5, 8) > interval(2, 3)) == True
    assert (interval(2, 5) > interval(1, 3)) == None
    assert (interval(2, 3) > interval(3.1, 5)) == False
    assert (interval(3, 5) > 2) == True
    assert (interval(1, 2) >= interval(0, 1)) == True
    assert (interval(1, 2) >= interval(0, 1.5)) == None
    assert (interval(1, 2) >= interval(3, 4)) == False
    assert (interval(1, 2) >= 0) == True
    assert (2 > interval(0, 1)) == True

def test_interval_sub():
    assert interval(1, 2) - interval(1, 5) == interval(-4, 1)
    assert interval(1, 2) - 1 == interval(0, 1)
    assert 1 - interval(1, 2) == interval(-1, 0)
    assert 1 - interval(0, np.inf) == interval(-np.inf, 1)
    assert interval(-np.inf, np.inf) + 1 == interval(-np.inf, np.inf)

def test_interval_mul():
    assert interval(1, 5) * interval(2, 10) == interval(2, 50)
    assert interval(-1, 1) * interval( 2, 10) == interval(-10, 10)
    assert interval(-1, 1) * interval(-5, 3) == interval(-5, 5)
    assert interval(1, 3) * 2 == interval(2, 6)
    assert 3 * interval(-1, 2) == interval(-3, 6)

    #inf tests
    assert interval(-5, 0) * np.inf == interval(-np.inf, 0)
    assert interval(-5, 0) * -np.inf == interval(0, np.inf)
    assert interval(0, 1) * np.inf == interval(0, np.inf)
    assert interval(0, 1) * -np.inf == interval(-np.inf, 0)
    assert interval(0, 1) * interval(0, np.inf) == interval(0, np.inf)
    assert interval(-1, 1) * np.inf == interval(-np.inf, np.inf)
    assert interval(-1, 1) * interval(0, np.inf) == interval(-np.inf, np.inf)
    assert interval(-1, 1) * interval(-np.inf, np.inf) == interval(-np.inf, np.inf)
    assert interval(-np.inf, 0) * interval(0, 1) == interval(-np.inf, 0)
    assert interval(-np.inf, 0) * interval(0, 0) * interval(-np.inf, 0)
    assert interval(-np.inf, 0) * interval(-np.inf, np.inf) == \
            interval(-np.inf, np.inf)

    assert interval(-5,0)*interval(-32,28) == interval(-140,160)
    assert interval(2,3) * interval(-1,2) == interval(-3,6)

    assert interval(np.inf, np.inf) * 0 == interval(-np.inf, np.inf)
    assert interval(-np.inf, -np.inf) * 0 == interval(-np.inf, np.inf)
    assert interval(0) * interval(-np.inf,2) == interval(-np.inf,np.inf)
    assert 0 * interval(-2,np.inf) == interval(-np.inf, np.inf)
    assert interval(-2,np.inf) * interval(0) == interval(-np.inf,np.inf)
    assert interval(-np.inf,2) * interval(0) == interval(-np.inf,np.inf)

def test_interval_div():
    assert interval(0.5, 1) / interval(-1, 0) == interval(-np.inf, -0.5)
    assert interval(0, 1) / interval(0, 1) == interval(0, np.inf)
    assert interval(np.inf, np.inf) / interval(np.inf, np.inf) == interval(0, np.inf)
    assert interval(np.inf, np.inf) / interval(2, np.inf) == interval(0, np.inf)
    assert interval(np.inf, np.inf) / interval(2, 2) == interval(np.inf, np.inf)
    assert interval(0, np.inf) / interval(2, np.inf) == interval(0, np.inf)
    assert interval(0, np.inf) / interval(2, 2) == interval(0, np.inf)
    assert interval(2, np.inf) / interval(2, 2) == interval(1, np.inf)
    assert interval(2, np.inf) / interval(2, np.inf) == interval(0, np.inf)
    assert interval(-4, 8) / interval(1, np.inf) == interval(-4, 8)
    assert interval(-4, 8) / interval(0.5, np.inf) == interval(-8, 16)
    assert interval(-np.inf, 8) / interval(0.5, np.inf) == interval(-np.inf, 16)
    assert interval(-np.inf, np.inf) / interval(0.5, np.inf) == interval(-np.inf, np.inf)
    assert interval(8, np.inf) / interval(0.5, np.inf) == interval(0, np.inf)
    assert interval(-8, np.inf) / interval(0.5, np.inf) == interval(-16, np.inf)
    assert interval(-4, 8) / interval(np.inf, np.inf) == interval(0, 0)
    assert interval(0, 8) / interval(np.inf, np.inf) == interval(0, 0)
    assert interval(0, 0) / interval(np.inf, np.inf) == interval(0, 0)
    assert interval(-np.inf, 0) / interval(np.inf, np.inf) == interval(-np.inf, 0)
    assert interval(-np.inf, 8) / interval(np.inf, np.inf) == interval(-np.inf, 0)
    assert interval(-np.inf, np.inf) / interval(np.inf, np.inf) == interval(-np.inf, np.inf)
    assert interval(-8, np.inf) / interval(np.inf, np.inf) == interval(0, np.inf)
    assert interval(0, np.inf) / interval(np.inf, np.inf) == interval(0, np.inf)
    assert interval(8, np.inf) / interval(np.inf, np.inf) == interval(0, np.inf)
    assert interval(np.inf, np.inf) / interval(np.inf, np.inf) == interval(0, np.inf)
    assert interval(-1, 2) / interval(0, 1) == interval(-np.inf, +np.inf)
    assert interval(0, 1) / interval(0, 1) == interval(0.0, +np.inf)
    assert interval(-1, 0) / interval(0, 1) == interval(-np.inf, 0.0)
    assert interval(-0.5, -0.25) / interval(0, 1) == interval(-np.inf, -0.25)
    assert interval(0.5, 1) / interval(0, 1) == interval(0.5, +np.inf)
    assert interval(0.5, 4) / interval(0, 1) == interval(0.5, +np.inf)
    assert interval(-1, -0.5) / interval(0, 1) == interval(-np.inf, -0.5)
    assert interval(-4, -0.5) / interval(0, 1) == interval(-np.inf, -0.5)
    assert interval(-1, 2) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(0, 1) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(-1, 0) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(-0.5, -0.25) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(0.5, 1) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(0.5, 4) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(-1, -0.5) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(-4, -0.5) / interval(-2, 0.5) == interval(-np.inf, +np.inf)
    assert interval(-1, 2) / interval(-1, 0) == interval(-np.inf, +np.inf)
    assert interval(0, 1) / interval(-1, 0) == interval(-np.inf, 0.0)
    assert interval(-1, 0) / interval(-1, 0) == interval(0.0, +np.inf)
    assert interval(-0.5, -0.25) / interval(-1, 0) == interval(0.25, +np.inf)
    assert interval(0.5, 1) / interval(-1, 0) == interval(-np.inf, -0.5)
    assert interval(0.5, 4) / interval(-1, 0) == interval(-np.inf, -0.5)
    assert interval(-1, -0.5) / interval(-1, 0) == interval(0.5, +np.inf)
    assert interval(-4, -0.5) / interval(-1, 0) == interval(0.5, +np.inf)
    assert interval(-1, 2) / interval(0.5, 1) == interval(-2.0, 4.0)
    assert interval(0, 1) / interval(0.5, 1) == interval(0.0, 2.0)
    assert interval(-1, 0) / interval(0.5, 1) == interval(-2.0, 0.0)
    assert interval(-0.5, -0.25) / interval(0.5, 1) == interval(-1.0, -0.25)
    assert interval(0.5, 1) / interval(0.5, 1) == interval(0.5, 2.0)
    assert interval(0.5, 4) / interval(0.5, 1) == interval(0.5, 8.0)
    assert interval(-1, -0.5) / interval(0.5, 1) == interval(-2.0, -0.5)
    assert interval(-4, -0.5) / interval(0.5, 1) == interval(-8.0, -0.5)
    assert interval(-1, 2) / interval(-2, -0.5) == interval(-4.0, 2.0)
    assert interval(0, 1) / interval(-2, -0.5) == interval(-2.0, 0.0)
    assert interval(-1, 0) / interval(-2, -0.5) == interval(0.0, 2.0)
    assert interval(-0.5, -0.25) / interval(-2, -0.5) == interval(0.125, 1.0)
    assert interval(0.5, 1) / interval(-2, -0.5) == interval(-2.0, -0.25)
    assert interval(0.5, 4) / interval(-2, -0.5) == interval(-8.0, -0.25)
    assert interval(-1, -0.5) / interval(-2, -0.5) == interval(0.25, 2.0)
    assert interval(-4, -0.5) / interval(-2, -0.5) == interval(0.25, 8.0)
    assert interval(0, 0) / interval(0, 0) == interval(-np.inf, np.inf)
    assert interval(0, 0) / interval(0, 1) == interval(-np.inf, np.inf)
    assert 1 / interval(2, 4) == interval(0.25, 0.5)

def test_pow():
    assert interval(2, 4) ** 2 == interval(4, 16)


if __name__=='__main__':
    test_interval()
    test_interval_add()
    test_interval_inequality()
    test_interval_sub()
    test_interval_mul()
    test_interval_div()
    test_pow()

