def floyd_marshall(G):
    n = len(G)
    memo = {}
    res = [[float("inf")] * n for _ in range(n)]

    def helper(x, y, k):
        nonlocal memo, res
        if k == 0:
            return res[x][y]
        if (x, y, k) in memo:
            return memo[(x, y, k)]
        memo[(x, y, k)] = min(helper(x, y, k - 1),
                              helper(x, k, k - 1) + helper(k, y, k - 1))
        return memo[(x, y, k)]

    for u in range(n):
        res[u][u] = 0
        for v, w in G[u]:
            res[u][v] = w
    for i in range(n):
        for j in range(n):
            res[i][j] = helper(i, j, n - 1)
    return res


G = [
    [[1, 15], [2, 3]],
    [[3, 1]],
    [[3, 2]],
    [[4, -1]],
    []
]


print(floyd_marshall(G), "\n")


def floyd_marshall_Bottom_up(G):
    n = len(G)
    dp = [[[float("inf")] * 2 for _ in range(n)] for _ in range(n)]
    for u in range(n):
        dp[u][u][0] = 0
        for v, w in G[u]:
            dp[u][v][0] = w

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dp[i][j][1] = min(dp[i][j][0],
                                  dp[i][k][0] + dp[k][j][0])
        for i in range(n):
            for j in range(n):
                dp[i][j][0] = dp[i][j][1]

    res = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            res[i][j] = dp[i][j][0]
    return res


G = [
    [[1, 15], [2, 3]],
    [[3, 1]],
    [[3, 2]],
    [[4, -1]],
    []
]


print(floyd_marshall_Bottom_up(G), "\n")