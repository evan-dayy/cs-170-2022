# FIBONACCI

# recursive fibonacci code, memoized to be fast
def fib_memoized(n):
    mem = [None] * (n + 1)

    def fib_memo_helper(n):
        nonlocal mem
        if n <= 1:
            return n
        elif mem[n]:
            return mem[n]
        else:
            mem[n] = fib_memo_helper(n - 1) + fib_memo_helper(n - 2)
            return mem[n]

    return fib_memo_helper(n)


# bottom up DP implementation
def fib_bottom_up(n):
    mem = [None] * (n + 1)
    mem[0], mem[1] = 0, 1
    for i in range(2, n + 1):
        mem[i] = mem[i - 1] + mem[i - 2]
    return mem[n]


# bottom up DP with space saving
def fib_bottom_up_space_saving(n):
    if n <= 1:
        return n
    mem = [0, 1]  # size-2 memory table instead of size-n
    for i in range(2, n + 1):
        z = mem[0] + mem[1]
        mem[0] = mem[1]
        mem[1] = z
    return mem[1]


# SHORTEST PATH IN A DAG

# G[u] is a list of edges, where each element of G[u] is of the form
# [v, w], meaning an edge (u,v) of weight w
def reverse_weighted_graph(G):
    H = [[] for _ in range(len(G))]
    for u in range(len(G)):
        for v, w in G[u]:
            H[v].append([u, w])
    return H


def shortest_path_dag_helper(revG, s, t, mem, choices):
    if t == s:
        return 0
    elif len(revG[t]) == 0:
        return float('infinity')
    elif mem[t]:
        return mem[t]
    else:
        mem[t] = float('infinity')
        for v, w in revG[t]:
            x = shortest_path_dag_helper(revG, s, v, mem, choices) + w
            if x < mem[t]:
                mem[t] = x
                choices[t] = v
        return mem[t]


# return two arrays arrays mem and choices, each of length n
# mem[u] is length of shortest path from s to u
# choices[u] is the vertex on the shortest path from s to u, immediately before u
# (if no path exists, or if u=s, then choices[u] is -1)
def shortest_path_dag_memoized(G, s):
    mem = [None] * len(G)
    choices = [-1] * len(G)
    revG = reverse_weighted_graph(G)
    for t in range(len(G)):
        shortest_path_dag_helper(revG, s, t, mem, choices)
    return mem, choices


def shortest_path_dag_return_path(G, s, t):
    mem, choices = shortest_path_dag_memoized(G, s)
    if mem[t] == float('infinity'):
        return None
    else:
        at = t
        ret = [t]
        while at != s:
            at = choices[at]
            ret.append(at)
        return ret[::-1]


G = [
    [[1, 15], [2, 3]],
    [[3, 1]],
    [[3, 2]],
    [[4, -1]],
    []
]

print(shortest_path_dag_return_path(G, 0, 4))


# # Bellman-Ford as memoized code
#
# def bellman_ford_memo_helper(revG, s, t, k, mem):
#     if k == 0:
#         if s == t:
#             return 0
#         else:
#             return float('infinity')
#     elif not mem[t][k]:
#         return mem[t][k]
#     else:
#         mem[t][k] = bellman_ford_memo_helper(revG, s, t, k - 1, mem)
#         for v, w in revG[t]:
#             mem[t][k] = min(mem[t][k], bellman_ford_memo_helper(revG, s, v, k - 1, mem) + w)
#         return mem[t][k]
#
#
# # returns None if negative cycle detected
# # else returns list of length n, where u'th entry is length of shortest path
# # from s to u
# def bellman_ford_memo(G, s):
#     mem = [[None] * (len(G) + 1) for _ in range(len(G))]
#     revG = reverse_weighted_graph(G)
#     for u in range(len(G)):
#         if bellman_ford_memo_helper(revG, s, t, n, mem) < bellman_ford_memo_helper(revG, s, t, n - 1, mem):
#             return None
#     return [L[n - 1] for L in mem]
#
#
# # Bellman-Ford as bottom-up DP with space saving (two 1d arrays)
# # formulaic conversion to bottom-up DP without being clever
# def bellman_ford_bottom_up_dp(G, s):
#     mem = [[float('infinity')] * 2 for _ in range(len(G))]
#     mem[s][0] = 0
#     revG = reverse_weighted_graph(G)
#     for k in range(len(G) - 1):
#         for u in range(len(G)):
#             mem[u][1] = mem[u][0]
#             for v, w in G[u]:
#                 mem[u][1] = min(mem[u][1], mem[v][0] + w)
#         for u in range(len(G)):
#             mem[u][0] = mem[u][1]
#     return [L[1] for L in mem]
