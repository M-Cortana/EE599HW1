import numpy as np
import math
import copy

def egcd(a, b):
    # return [r, s, t], r = a*s + b*tß
    rm2 = a
    rm1 = b
    r = rm2 % rm1
    q = rm2 // rm1

    sm2 = 1
    sm1 = 0
    s = sm2 - q*sm1

    tm2 = 0
    tm1 = 1
    t = tm2 - q*tm1
    while r != 0:
        rm2 = rm1
        rm1 = r
        r = rm2 % rm1
        q = rm2 // rm1
        tm2 = tm1
        tm1 = t
        t = tm2 - q*tm1

        sm2 = sm1
        sm1 = s
        s = sm2 - q*sm1
    return [rm1, int(sm1), int(tm1)]

def inv(a, p):
    # return 1/a in Zp field
    [r, c, k] = egcd(a, p)
    return c % p

class num:
    def __init__(self, n, p):
        #Num is in Zp, and the value is n
        self.n = n % p
        self.p = p
    
    def __add__(self, other):
        if type(self) != type(other):
            return num((self.n + other) % self.p, self.p)
        if self.p != other.p:
            raise Exception("Numbers are not in the same Zp")
        return num((self.n + other.n) % self.p, self.p)
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        if type(self) != type(other):
            return num((self.n - other) % self.p, self.p)
        if self.p != other.p:
            raise Exception("Numbers are not in the same Zp")
        return num((self.n - other.n) % self.p, self.p)
    def __rsub__(self, other):
        return -1*(self - other)
    def __mul__(self, other):
        if type(self) != type(other):
            return num((self.n * other) % self.p, self.p)
        if self.p != other.p:
            raise Exception("Numbers are not in the same Zp")
        return num((self.n * other.n) % self.p, self.p)
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        if type(self) != type(other):
            return num((self.n * inv(other, self.p)) % self.p, self.p)
        if self.p != other.p:
            raise Exception("Numbers are not in the same Zp")
        return num((self.n * inv(other.n, self.p)) % self.p, self.p)
    def __rtruediv__(self, other):
        return inv(self / other)
    def __pow__(self, other):
        res = num(1, self.p)
        while other > 0:
            other -= 1
            res *= self
        return res
    def __eq__(self, other):
        if self.n == other.n and self.p == other.p:
            return 1
        else:
            return 0
class point:
    def __init__(self, x0, y0, a0, b0, p0):
        self.x = num(x0, p0)
        self.y = num(y0, p0)
        self.a = num(a0, p0)
        self.b = num(b0, p0)
        self.p = p0
    def __add__(self, other):
        if self == 0:
            return other
        if other == 0:
            return self
        if self.a != other.a or self.b != other.b or self.p != other.p:
            raise Exception("Points are not on the same curve")
        if self.x == other.x and self.y == other.y:
            lam = (3*self.x**2 + self.a) / (2*self.y)
        else:
            lam = (other.y - self.y)/(other.x - self.x)
        x3 = lam * lam - self.x - other.x
        y3 = lam * (self.x - x3) - self.y
        res = copy.copy(self)
        res.x = x3
        res.y = y3
        return res
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        tmp = copy.copy(other)
        tmp.y.n = -tmp.y.n
        return self + tmp
    def __mul__(self, other):
        p = 1
        tmp = copy.copy(self)
        res = 0
        while p <= other:
            if (other & p) != 0:
                res += tmp
            tmp += tmp
            p *= 2
        return res
    def __rmul__(self, other):
        return self * other
    def __str__(self):
        return "(%d, %d)" % (self.x.n, self.y.n)
    def __repr__(self):
        return "[(%d, %d) on E(%d): y^2 = x^3 + %d*x + %d mod %d]" % (self.x.n, self.y.n, self.p, self.a.n, self.b.n, self.p)
