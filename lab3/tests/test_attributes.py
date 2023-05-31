import math

def fooMath(a):
    return math.sin(a)

def foo(a,b):
    return a+b

def closure(a):
    def inner(a):
        return 0
    
    return inner

def gen(a):
    yield a
    yield a
    yield a

lam = lambda x: x+1

def second(a):
    return a*a

def first(a):
    return second(2)+a

def firstIn(a):
    b = second
    return b(a)+a

def rec(a):
    if a!=0:
        return a+rec(a-1)
    else: 
        return 0
    

class A:
    a_var = 1

    def a_func(self):
        return "a"
    
    def letter(self):
        return "a"

    def __init__(self,num):
        self.num = num

    @property
    def prop_test(self):
        return self.num
    
class B(A):
    def letter(self):
        return "c"
    
    def b_func(self):
        return "b"

class D(A):
    def letter(self):
        return "d"

class C(B,D):
    pass