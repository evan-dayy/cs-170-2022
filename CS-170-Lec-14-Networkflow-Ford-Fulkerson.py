# MAXIMUM FLOW VIA FORD FULKERSON

# input in adj matrix representation
# u[i][j] is capacity of edge (i,j) (0 if edge not present)
def ford_fulkerson(u, s, t):
    n = len(u)
    f = [[0] * n for _ in range(n)]
    visited = []

    def push_flow(v, amt):
        nonlocal n, u, t, f, visited
        if v == t:
            return amt
        for w in range(n):
            if not visited[w]:
                residual = u[v][w] - f[v][w]
                if residual > 0:
                    visited[w] = True
                    amt = min(amt, push_flow(w, min(amt, residual)))
                    f[v][w] += amt
                    f[w][v] -= amt
                    return amt
        return 0

    while True:
        visited = [False] * n
        visited[s] = True
        if push_flow(s, float('infinity')) == 0:
            break

    for i in range(n):
        for j in range(n):
            f[i][j] = max(f[i][j], 0)
    return f


capacities = [
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]

print(ford_fulkerson(capacities, 0, 5))
