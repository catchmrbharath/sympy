from sympy.plotting.intervalmath import interval
import numpy as np
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

def test_power():
    assert interval(1, 2) ** 2 == interval(1, 4)
    assert interval(-1, 1) ** -2 == interval(1, np.inf)
    assert interval(-1, 1) ** 2 == interval(0, 1)
    assert interval(0.5, 1) ** 2 == interval(0.25, 1)
