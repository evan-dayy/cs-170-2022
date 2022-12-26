# MATRIX class (from scratch, but one could also use numpy)

from heapq import *

from numpy import sort

nla


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


# STRASSEN IMPLEMENTATION

# return smallest power of 2 that is >= n
def hyperceil(n):
    if n == 0:
        return 1
    j = 0
    m = n
    while m > 0:
        j += 1
        m >>= 1
    if 1 << (j - 1) == n:
        return n
    else:
        return 1 << j


# assumes A and B are square matrices of same size
# A and B should be Matrix objects
def strassen_multiply(A, B):
    def strassen_recurse(X, Y):
        n = len(X.vals)
        if n == 1:
            return Matrix([[X.vals[0][0] * Y.vals[0][0]]])
        # X = [A B], Y = [E F]  XY = [AE + BG   AF + BH]
        #     [C D]      [G H],      [CE + DG   CF + DH]
        A = [[None] * (n // 2) for _ in range(n // 2)]
        B = [[None] * (n // 2) for _ in range(n // 2)]
        C = [[None] * (n // 2) for _ in range(n // 2)]
        D = [[None] * (n // 2) for _ in range(n // 2)]
        E = [[None] * (n // 2) for _ in range(n // 2)]
        F = [[None] * (n // 2) for _ in range(n // 2)]
        G = [[None] * (n // 2) for _ in range(n // 2)]
        H = [[None] * (n // 2) for _ in range(n // 2)]
        for i in range(n // 2):
            for j in range(n // 2):
                A[i][j] = X.vals[i][j]
                B[i][j] = X.vals[i][j + n // 2]
                C[i][j] = X.vals[i + n // 2][j]
                D[i][j] = X.vals[i + n // 2][j + n // 2]
                E[i][j] = Y.vals[i][j]
                F[i][j] = Y.vals[i][j + n // 2]
                G[i][j] = Y.vals[i + n // 2][j]
                H[i][j] = Y.vals[i + n // 2][j + n // 2]
        A = Matrix(A)
        B = Matrix(B)
        C = Matrix(C)
        D = Matrix(D)
        E = Matrix(E)
        F = Matrix(F)
        G = Matrix(G)
        H = Matrix(H)
        P1 = strassen_recurse(A, F - H)
        P2 = strassen_recurse(A + B, H)
        P3 = strassen_recurse(C + D, E)
        P4 = strassen_recurse(D, G - E)
        P5 = strassen_recurse(A + D, E + H)
        P6 = strassen_recurse(B - D, G + H)
        P7 = strassen_recurse(A - C, E + F)
        topleft = P5 + P4 - P2 + P6
        topright = P1 + P2
        botleft = P3 + P4
        botright = P1 + P5 - P3 - P7
        ans = [[None] * n for _ in range(n)]
        for i in range(n // 2):
            for j in range(n // 2):
                ans[i][j] = topleft.vals[i][j]
                ans[i][j + n // 2] = topright.vals[i][j]
                ans[i + n // 2][j] = botleft.vals[i][j]
                ans[i + n // 2][j + n // 2] = botright.vals[i][j]
        return Matrix(ans)

    assert (len(A.vals) == len(A.vals[0]) and
            len(B.vals) == len(B.vals[0]) and
            len(A.vals) == len(B.vals))

    n = hyperceil(len(A.vals))
    AA = [[0] * n for _ in range(n)]
    BB = [[0] * n for _ in range(n)]
    for i in range(len(A.vals)):
        for j in range(len(A.vals)):
            AA[i][j] = A.vals[i][j]
            BB[i][j] = B.vals[i][j]
    CC = strassen_recurse(Matrix(AA), Matrix(BB))
    C = [[0] * len(A.vals) for _ in range(len(A.vals))]
    for i in range(len(A.vals)):
        for j in range(len(A.vals)):
            C[i][j] = CC.vals[i][j]
    return Matrix(C)


M = Matrix([[1, 1], [1, 0]])
Q = strassen_multiply(M, M)
print(strassen_multiply(Q, Q))  # M^4 via Strassen
print(M ** 4)  # M^4 w/o Strassen


# MERGESORT

def merge(A, B):
    ret = []
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            ret.append(A[i])
            i += 1
        else:
            ret.append(B[j])
            j += 1
    return ret + A[i:] + B[j:]


def merge_sort(A):
    if len(A) <= 1:
        return A[:]
    else:
        return merge(merge_sort(A[:len(A) // 2]), merge_sort(A[len(A) // 2:]))


print(merge_sort([10, 8, 6, 4]))


# DETERMINISTIC SELECTION IN LINEAR TIME

def fast_select(A, k):
    def fast_select_helper(A, k):
        if len(A) < 5:
            return sorted(A)[k]
        B = [[None] * 5 for _ in range(len(A) // 5)]
        for i in range((len(A) // 5) * 5):  # rounded down to nearest multiple of 5
            B[i // 5][i % 5] = A[i]
        for i in range(len(B)):
            B[i].sort()
        AA = [L[2] for L in B]  # list of medians of each group
        p = fast_select(AA, len(AA) // 2)  # p is median of medians

        L = list(filter(lambda x: x < p, A))  # all elts of A less than p
        R = list(filter(lambda x: x > p, A))  # all elts of A greater than p

        if k == len(L):
            return p
        elif k < len(L):
            return fast_select_helper(L, k)
        else:
            return fast_select_helper(R, k - len(L) - 1)

    M = list(zip(A, list(range(len(A)))))  # ensure that all elts of A are distinct
    print(M)
    return fast_select_helper(M, k)[0]


L = [10, 1, 4, 2, 9, 8, 21, 42, 85]
print(sort(L))
print(fast_select(L, 4))
print(sorted(L)[3])


def decToBinary(n):
    # array to store
    # binary number
    binaryNum = [0] * n

    # counter for binary array
    i = 0
    while n > 0:
        # storing remainder
        # in binary array
        binaryNum[i] = n % 2
        n = int(n / 2)
        i += 1

    # printing binary array
    # in reverse order
    for j in range(i - 1, -1, -1):
        print(binaryNum[j], end="")


# Driver Code
n = 17
decToBinary(n)
