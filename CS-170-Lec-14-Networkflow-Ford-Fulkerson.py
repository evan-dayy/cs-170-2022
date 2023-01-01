# MAXIMUM FLOW VIA FORD FULKERSON

# input in adj matrix representation
# u[i][j] is capacity of edge (i,j) (0 if edge not present)


def ford_fulkerson(m, s, t):
    n = len(m)
    # used f[i][j]
    f = [[0] * n for _ in range(n)]

    def dfs(u, amt):
        nonlocal t, visited, f, m, n
        if u == t:
            return amt
        for v in range(n):
            if not visited[v]:
                pushing_ava = m[u][v] - f[u][v]
                if pushing_ava > 0:
                    visited[v] = True
                    amt = min(amt, dfs(v, min(amt, pushing_ava)))
                    f[u][v] += amt
                    f[v][u] -= amt
                    return amt
        return 0

    while True:
        visited = [False] * n
        visited[s] = True
        if dfs(s, float("inf")) == 0:
            break
    for i in range(n):
        for j in range(n):
            f[i][j] = max(f[i][j], 0)
    return sum(f[0])


capacities = [
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0]
]

print(ford_fulkerson(capacities, 0, 5))
