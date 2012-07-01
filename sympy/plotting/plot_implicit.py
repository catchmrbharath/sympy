"""Implicit plotting module for SymPy

The module implements a data series called ImplicitSeries which is used by
``Plot`` class to plot implicit plots for different backends. The module
implements plotting using interval arithmetic.

See Also
========
sympy.plotting.plot

References
==========
- Jeffrey Allen Tupper. Reliable Two-Dimensional Graphing Methods for
Mathematical Formulae with Two Free Variables.

- Jeffrey Allen Tupper. Graphing Equations with Generalized Interval
Arithmetic. Master's thesis. University of Toronto, 1996

"""

from plot import BaseSeries, Plot
from experimental_lambdify import experimental_lambdify
from intervalmath import interval
from sympy.core.relational import Equality, GreaterThan, LessThan
from sympy.external import import_module
from sympy import sympify, Expr
from sympy.core.compatibility import set_union

np = import_module('numpy')


class ImplicitSeries(BaseSeries):
    """ Representation for Implicit plot """
    is_implicit = True

    def __init__(self, expr, var_start_end_x, var_start_end_y):
        super(ImplicitSeries, self).__init__()
        self.expr = sympify(expr)
        self.var_x = sympify(var_start_end_x[0])
        self.start_x = float(var_start_end_x[1])
        self.end_x = float(var_start_end_x[2])
        self.var_y = sympify(var_start_end_y[0])
        self.start_y = float(var_start_end_y[1])
        self.end_y = float(var_start_end_y[2])
        self.get_points = self.get_meshes

    def __str__(self):
        return ('Implicit equation: %s for '
                '%s over %s and %s over %s') % (
                str(self.expr),
                str(self.var_x),
                str((self.start_x, self.end_x)),
                str(self.var_y),
                str((self.start_y, self.end_y)))

    def get_meshes(self):
        WIDTH = 2048   #TODO: Add as an attribute which can be changed
        HEIGHT = 2048  #TODO: Add as an attribute which can be changed
        is_equality = isinstance(self.expr, Equality)
        func = experimental_lambdify((self.var_x, self.var_y), self.expr, use_interval=True)
        xinterval = interval(self.start_x, self.end_x)
        yinterval = interval(self.start_y, self.end_y)
        #TODO: Have a fallback algorithm for functions that are not implemented
        try:
            temp = func(xinterval, yinterval)
        except AttributeError:
            raise NotImplementedError("Some functions in the expression %s are \
                                    not supported. Kindly report this as a bug" % str(self.expr))
        #contour array, acts like a bitmap
        contour = np.zeros((WIDTH, HEIGHT))
        k = 5 #Best case by trial and error
        interval_list = []

        xsample = np.linspace(self.start_x, self.end_x, WIDTH / 2**k + 1)
        ysample = np.linspace(self.start_y, self.end_y, HEIGHT / 2**k + 1)

        xinter = [interval(x1, x2) for x1, x2 in zip(xsample[:-1], xsample[1:])]
        yinter = [interval(y1, y2) for y1, y2 in zip(ysample[:-1], ysample[1:])]
        interval_list = [[x, y] for x in xinter for y in yinter]
        plot_list = []

        #recursive call refinepixels which subdivides the intervals which are neither
        # True nor False according to the expression.
        def refine_pixels(interval_list):
            temp_interval_list = []
            plot_list = []
            for intervals in interval_list:

                #Convert the array indices to x and y values
                intervalx = intervals[0]
                intervaly = intervals[1]
                func_eval = func(intervalx, intervaly)
                #The expression is valid in the interval. Change the contour array
                #values to 1.
                if func_eval[1] is False or func_eval[0] is False:
                    pass
                elif func_eval == (True, True) and not is_equality:
                    plot_list.append([intervalx, intervaly])
                elif func_eval[1] is None or func_eval[0] is None \
                        or is_equality:
                    #Subdivide
                    avgx = intervalx.mid
                    avgy = intervaly.mid
                    a = interval(intervalx.start, avgx)
                    b = interval(avgx, intervalx.end)
                    c = interval(intervaly.start, avgy)
                    d = interval(avgy, intervaly.end)
                    temp_interval_list.append([a, c])
                    temp_interval_list.append([a, d])
                    temp_interval_list.append([b, c])
                    temp_interval_list.append([b, d])
            return temp_interval_list, plot_list
        k = 5
        while k >= 0 and len(interval_list):
            interval_list, plot_list_temp = refine_pixels(interval_list)
            plot_list.extend(plot_list_temp)
            k = k - 1
        #Check whether the expression represents an equality
        #If it represents an equality, then none of the intervals
        #would have satisfied the expression due to floating point
        #differences. Add all the undecided values to the plot.
        #equality_dict = defaultdict()
        #interval_list = convert_dict(interval_list)
        
        if isinstance(self.expr, (Equality, GreaterThan, LessThan)):
            for intervals in interval_list:
                intervalx = intervals[0]
                intervaly = intervals[1]
                func_eval = func(intervalx, intervaly)
                if func_eval[1] and func_eval[0] is not False:
                    plot_list.append([intervalx, intervaly])
        xvals, yvals = matplot_lib_plotlist(plot_list)
        return xvals, yvals


def plot_implicit(expr, var_start_end_x, var_start_end_y, **kwargs):
    """A plot function to plot implicit equations / inequations.

    The input arguments are:
    expr : The equation / inequation that is to be plotted.
    var_start_end_x: A tuple of length 3, with the first element representing
    the variable and the next two elements representing the range
    var_start_end_y: A tuple of length 3, with the first element representing
    the variable and the next two elements representing the range

    Examples:
    ---------

    Plot expressions:
    >>> from sympy import plot_implicit, cos, sin, symbols, Eq
    >>> x, y = symbols('x y')
    >>> p1 = plot_implicit(Eq(y, x ** 2), (x, -5, 5), (y, -5, 5), show=False)
    >>> p2 = plot_implicit(Eq(x ** 2 + y ** 2, 3), (x, -3, 3), (y, -3, 3), show=False)
    >>> p3 = plot_implicit(y ** 2 < x ** 3 - x, (x, -4, 4), (y, -4, 4), show=False)
    >>> p4 = plot_implicit(y > sin(x), (x, -5, 5), (y, -2, 2), show=False)
"""

    assert isinstance(expr, Expr)
    free_symbols = expr.free_symbols
    range_symbols = set([var_start_end_x[0], var_start_end_y[0]])
    symbols = set_union(free_symbols, range_symbols)
    if len(symbols) > 2:
        raise NotImplementedError("Implicit plotting is not implemented for "
                                    "more than 2 variables")
    series_argument = ImplicitSeries(expr, var_start_end_x, var_start_end_y)
    show = kwargs.pop('show', True)
    p = Plot(series_argument, **kwargs)
    if show:
        p.show()
    return p

def matplot_lib_plotlist(interval_list):
    xlist = []
    ylist = []
    for intervals in interval_list:
        intervalx = intervals[0]
        intervaly = intervals[1]
        xlist.extend([intervalx.start, intervalx.start, intervalx.end, intervalx.end, None])
        ylist.extend([intervaly.start, intervaly.end, intervaly.end, intervaly.start, None])
    return xlist, ylist

def convert_dict(interval_list):
    from collections import defaultdict
    a = defaultdict(list)
    for intervals in interval_list:
        temp = (intervals[0].start, intervals[0].end)
        a[temp].append(intervals[1])

    interval_list = []
    for key in a:
        if(len(a[key]) > 14):
            xinter = np.linspace(key[0], key[1], 5) 
            ta = interval(xinter[0], xinter[1])
            tb = interval(xinter[1], xinter[2])
            tc = interval(xinter[2], xinter[3])
            td = interval(xinter[3], xinter[4])
            temp_list = [[ta, y] for y in a[key]]
            interval_list.extend(temp_list)
            temp_list = [[tb, y] for y in a[key]]
            interval_list.extend(temp_list)
            temp_list = [[tc, y] for y in a[key]]
            interval_list.extend(temp_list)
            temp_list = [[td, y] for y in a[key]]
            interval_list.extend(temp_list)
        else:
            xinterval = interval(key[0], key[1])
            interval_list.extend([[xinterval, y] for y in a[key]])
    return interval_list

            

