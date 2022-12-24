# THREE DIFFERENT ALGORITHMS TO COMPUTE nth FIBONACCI NUMBER
# (which recall from class has Theta(n) digits)
# MATRIX class (from scratch, but one could also use numpy)
from functools import *


class Matrix:
    # A should be a list of lists with the matrix entries
    def __init__(self, A):
        self.vals = [[None] * len(A[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(A[0])):
                self.vals[i][j] = A[i][j]

    @classmethod
    def identity(cls, n):
        v = [[0] * n for _ in range(n)]
        for i in range(n):
            v[i][i] = 1
        return cls(v)

    def __add__(self, other):
        v = [[None] * len(self.vals[0]) for _ in range(len(self.vals))]
        for i in range(len(self.vals)):
            for j in range(len(self.vals[0])):
                v[i][j] = self.vals[i][j] + other.vals[i][j]
        return Matrix(v)

    def __mul__(self, other):  # O(n^3) matrix mult
        C = [[0] * len(other.vals[0]) for _ in range(len(self.vals))]
        for i in range(len(C)):
            for j in range(len(C[0])):
                for k in range(len(self.vals[0])):
                    # note Python uses Karatsuba for this *, built-in
                    C[i][j] += self.vals[i][k] * other.vals[k][j]
        return Matrix(C)

    def __sub__(self, other):
        v = [[None] * len(self.vals[0]) for _ in range(len(self.vals))]
        for i in range(len(self.vals)):
            for j in range(len(self.vals[0])):
                v[i][j] = self.vals[i][j] - other.vals[i][j]
        return Matrix(v)

    # use repeated squaring to only do O(log k) matrix multiplies
    def __pow__(self, k):
        # print(self)
        if k == 0:
            return Matrix.identity(len(self.vals))
        else:
            A = self ** (k // 2)  # recursively call __pow__
            A *= A
            if k & 1 == 1:
                A *= self
            return A

    def __string__(self):
        return 'M' + str(self.vals)

    def __repr__(self):
        return 'M' + str(self.vals)


# exponential time, in n
# @cache

def fib_recursive(n):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    else:
        memo[n] = fib_recursive(n - 1) + fib_recursive(n - 2)
        return memo[n]


# Theta(n^2) time
def fib_iterative(n):
    if n <= 1:
        return n
    x = 0
    y = 1
    for i in range(n - 1):
        z = x + y
        x = y
        y = z
    return z


# Theta(n^{log_2 3}) time, since Python integer multiplication uses Karatsuba
def fib_matrix(n):
    if n <= 1:
        return n
    A = Matrix([[1, 1], [1, 0]])
    A **= n - 1
    return A.vals[0][0]


memo = {}
# print(fib_recursive(150))
# print(fib_iterative(100))
print(fib_matrix(8))

