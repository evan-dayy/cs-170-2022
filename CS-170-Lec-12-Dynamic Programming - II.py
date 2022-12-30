# Floyd-Warshall Algorithm
"""
- Define the functions f(i, j, k): return the shortest path from i to j
using only the k in {1, ..., k}. We want return f(*, *, n)
- Recursive relationship:
    if k == 0: suggesting that we cannot using any edges
        when i == j: return 0
        when i != j: return w(i, j)
    else:
        f(i, j, k) = min(
                            f(i, j, k - 1) -- I choose not to pick k
                            f(i, k, k - 1) + f(k, j, k - 1) -- pick k
                        )
"""


def floyd_warshall(G):
    T = [[float('infinity')] * len(G) for _ in range(len(G))]
    for u in range(len(G)):
        T[u][u] = 0
        for v, w in G[u]:
            T[u][v] = w
    for k in range(len(G)):
        for i in range(len(G)):
            for j in range(len(G)):
                T[i][j] = min(T[i][j], T[i][k] + T[k][j])
    return T


def floyd_warshall_memo_helper(D, mem, i, j, k):
    if k == 0:
        return D[i][j]
    elif mem[i][j][k] is not None:
        return mem[i][j][k]
    else:
        mem[i][j][k] = min(floyd_warshall_memo_helper(D, mem, i, j, k - 1),
                           floyd_warshall_memo_helper(D, mem, i, k, k - 1)
                           + floyd_warshall_memo_helper(D, mem, k, j, k - 1))
        return mem[i][j][k]


def floyd_warshall_memo(G):
    mem = [[[None] * len(G) for _ in range(len(G))] for _ in range(len(G))]
    D = [[float('infinity')] * len(G) for _ in range(len(G))]
    for u in range(len(G)):
        D[u][u] = 0
        for v, w in G[u]:
            D[u][v] = w
    for i in range(len(G)):
        for j in range(len(G)):
            D[i][j] = floyd_warshall_memo_helper(D, mem, i, j, len(G) - 1)
    return D


# formulaic implementation of bottom up DP for floyd warshall with O(n^2) memory
def floyd_warshall_bottom_up(G):
    mem = [[[float('infinity')] * 2 for _ in range(len(G))] for _ in range(len(G))]
    for u in range(len(G)):
        mem[u][u][0] = 0
        for v, w in G[u]:
            mem[u][v][0] = w
    for k in range(len(G)):
        for i in range(len(G)):
            for j in range(len(G)):
                mem[i][j][1] = min(mem[i][j][0], mem[i][k][0] + mem[k][j][0])
        # now copy answer for current k into cells for k-1, to prep for next loop iteration
        for i in range(len(G)):
            for j in range(len(G)):
                mem[i][j][0] = mem[i][j][1]
    ret = [[None] * len(G) for _ in range(len(G))]
    for i in range(len(G)):
        for j in range(len(G)):
            ret[i][j] = mem[i][j][1]
    return ret


G = [
    [[1, 15], [2, 3]],
    [[3, 1]],
    [[3, 2]],
    [[4, -1]],
    []
]

# print(floyd_warshall(G), "\n")
# print(floyd_warshall_memo(G), "\n")
# print(floyd_warshall_bottom_up(G), "\n")


# ====================================================================================
# Longest Increasing Subsequence

# LIS length amongst A[i:n] when all elts in subsequence must be
# > A[last]


def lis_memo_helper(A, mem, last, i):
    if i == len(A):
        return 0
    elif mem[last][i] is not None:
        return mem[last][i]
    else:
        mem[last][i] = lis_memo_helper(A, mem, last, i + 1)
        if A[i] > A[last]:
            mem[last][i] = max(mem[last][i], 1 + lis_memo_helper(A, mem, i, i + 1))
        return mem[last][i]


def longest_increasing_subsequence_memo(A):
    B = [-float('infinity')] + A
    mem = [[None] * len(B) for _ in range(len(B))]
    return lis_memo_helper(B, mem, 0, 1)


# bottom up implementation with space saving
def longest_increasing_subsequence_bottom_up(A):
    A = [-float('infinity')] + A
    mem = [[0] * 2 for _ in range(len(A))]
    for i in range(len(A) - 1, -1, -1):
        for last in range(i):
            mem[last][1] = mem[last][0]
            if A[i] > A[last]:
                mem[last][1] = max(mem[last][1], 1 + mem[i][0])
        for last in range(i):
            mem[last][0] = mem[last][1]
    return mem[0][1]


# print(longest_increasing_subsequence_memo([2, 8, 3, 4]))
# print(longest_increasing_subsequence_bottom_up([2, 8, 3, 4]))


# ====================================================================================
# Edit Distance

# we want to change string s into string t using as few "edits" as possible
# an edit can do any one of the following three things:
# 1) remove any character from s (or t), from any position  (bath -> bat)
# 2) insert any character into s (or t), at any position (cat -> coat)
# 3) substitute any character in s (or t) for another one, at any position
#    (e.g. dag --> dog)

# edit distance between s[i:] and t[j:]
def ed_helper(s, t, i, j, mem):
    if i == len(s):
        return len(t) - j
    elif j == len(t):
        return len(s) - i
    elif mem[i][j] is not None:
        return mem[i][j]
    else:
        A = 1 + ed_helper(s, t, i + 1, j, mem)  # delete s[i]
        B = 1 + ed_helper(s, t, i, j + 1, mem)  # insert t[j] right before s[i]
        C = 1 + ed_helper(s, t, i + 1, j + 1, mem)  # substitute s[i] for t[j]
        if s[i] == t[j]:
            C -= 1  # don't need to do the substitution if chars already equal
        mem[i][j] = min(A, B, C)
        return mem[i][j]


def edit_distance(s, t):
    mem = [[None] * len(t) for _ in range(len(s))]
    return ed_helper(s, t, 0, 0, mem)


def edit_distance_bottom_up(s, t):
    m = len(s)
    n = len(t)
    dp = [[float("inf")] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            left = dp[i][j - 1] + 1
            up = dp[i - 1][j] + 1
            left_up = dp[i - 1][j - 1]
            if s[i - 1] != t[j - 1]:
                left_up += 1
            dp[i][j] = min(left, up, left_up)
    return dp[-1][-1]


# print(edit_distance('coasfsdgfdhgfat', 'cofasdtasdasdasdasdasdasdasd'))
# print(edit_distance_bottom_up('coasfsdgfdhgfat', 'cofasdtasdasdasdasdasdasdasd'))


# Matrix Chain Multiplication
# there are matrices A_1,...,A_n, with A_i being s_i x s_{i+1}
# We would like to multiply them and can parenthesize the multiplication
# however we want to be as fat as possible (assume that multiplying an m x n
# times an n x p matrix takes mnp time). Find the cost of an optimal
# parenthesization

# Idea: In any parenthesization there is a last multiplication that is performed
# then we have to recursively optimally multiply all matrices to the left of
# that multiplication and to the right, then do that final multiplication
# Try all possibilities for which multiplication will be the last

def mcm_helper(s, i, j, mem):
    if i == j:
        return 0
    elif mem[i][j] is not None:
        return mem[i][j]
    else:
        mem[i][j] = float('infinity')
        for k in range(i, j):
            mem[i][j] = min(mem[i][j],
                            mcm_helper(s, i, k, mem)
                            + mcm_helper(s, k + 1, j, mem)
                            + s[i] * s[k + 1] * s[j + 1])
            return mem[i][j]


def matrix_chain_mult(s):
    mem = [[None] * len(s) for _ in range(len(s))]
    return mcm_helper(s, 0, len(s) - 2, mem)


# best to multiply 3x2 with 2x1, then 3x3 with resulting 3x1
# that is, (A x (B x C)) is better here than ((A x B) x C)
print(matrix_chain_mult([3, 3, 2, 1]))


# # Traveling Salesman Problem
#
# # complete graph where w(i,j) is stored as W[i][j]
# # S is a bitmask of which vertices we have yet to visit
# def tsp_helper(W, i, S, mem):
#     if S == 0:
#         return 0
#     elif mem[i][S] != None:
#         return mem[i][S]
#     else:
#         mem[i][S] = float('infinity')
#         for j in range(len(W)):
#             if S & (1 << j) != 0:
#                 mem[i][S] = min(mem[i][S], W[i][j] + tsp_helper(W, j, S ^ (1 << j), mem))
#         return mem[i][S]
#
#
# # must start at vertex 0 and visit every other vertex
# def tsp_memoized(W):
#     mem = [[None] * (1 << len(W)) for _ in range(len(W))]
#     return tsp_helper(W, 0, (1 << len(W)) - 2, mem)
#
#
# points = [
#     [0, 0],
#     [0, 1],
#     [0, 2],
#     [10, 0],
#     [10, 1],
#     [10, 2],
# ]
#
# W = [[None] * len(points) for _ in range(len(points))]
# for i in range(len(points)):
#     for j in range(len(points)):
#         W[i][j] = ((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2) ** 0.5
#
# print(tsp_memoized(W))

