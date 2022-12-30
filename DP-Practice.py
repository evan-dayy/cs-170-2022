def planting_tree(trees):
    n = len(trees)
    memo = {}

    def helper(i):
        nonlocal trees
        if i == 0:
            return trees[0]
        if i == 1:
            return max(trees[0], trees[1])
        if i in memo:
            return memo[i]
        memo[i] = max(helper(i - 1), trees[i] + helper(i - 2))
        return memo[i]

    return helper(n - 1)


print(planting_tree([10, 20, 6, 7, 100]))


def decoding(s, d, l):
    memo = {}
    n = len(s)

    def helper(idx):
        nonlocal n, s, d, l
        if idx > n:
            return 0
        if idx == n:
            return 1
        if idx in memo:
            return memo[idx]
        res = 0
        for i in range(1, l + 1):
            if s[idx: idx + i] in d:
                res += helper(idx + i)
        memo[idx] = res
        return memo[idx]

    return helper(0)


print(decoding("101011", {"1": "A", "01": "B", "101": "C", "10": "D"}, 3))


def string_shuffling(x, y, z):
    memo = {}
    nx = len(x)
    ny = len(y)
    nz = len(z)
    if nx + ny != nz:
        return False

    def helper(i, j):
        nonlocal nx, ny, nz
        if i == nx and j == ny:
            return True
        elif i == nx:
            return y[j:] == z[i + j:]
        elif j == ny:
            return x[i:] == z[i + j:]

        if x[i] == z[i + j] and y[j] == z[i + j]:
            memo[(i, j)] = helper(i + 1, j) or helper(i, j + 1)
        elif x[i] == z[i + j]:
            memo[(i, j)] = helper(i + 1, j)
        elif y[j] == z[i + j]:
            memo[(i, j)] = helper(i, j + 1)
        else:
            memo[(i, j)] = False
        return memo[(i, j)]

    return helper(0, 0)


y = "ALGORITHM"
z = "efficientALGORITHM"


# print(string_shuffling(x, y, z))


def string_shuffling_bottom_up(x, y, z):
    nx = len(x)
    ny = len(y)
    nz = len(z)
    if nx + ny != nz:
        return False
    dp = [True] * (nx + 1)
    i = nx - 1
    j = ny - 1
    while j >= 0:
        while i >= 0:
            if x[i] == z[i + j + 1] and y[j] == z[i + j + 1]:
                dp[i] = dp[i + 1] or dp[i]
                i -= 1
            elif x[i] == z[i + j + 1]:
                dp[i] = dp[i + 1]
                i -= 1
            elif y[j] == z[i + j + 1]:
                dp[i] = dp[i]
                j -= 1
            else:
                return False
        if j != 0:
            # print(y[: j + 1])
            # print(z[:nz - nx - (ny - j) + 1])
            return y[: j + 1] == z[:nz - nx - (ny - j) + 1]
    return dp[0]


x = "efficient"
y = "ALGORITHM"
z = "ALGORefficienITHM"


# print(string_shuffling(x, y, z))
# print(string_shuffling_bottom_up(x, y, z))


def burst_balloons(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    memo = {}

    def dp(i, j):
        nonlocal nums
        if (i, j) in memo:
            return memo[(i, j)]
        if j - i < 2:
            return 0
        res = 0
        for k in range(i + 1, j):
            cost = nums[k] * nums[i] * nums[j]
            res = max(res, cost + dp(i, k) + dp(k, j))
        memo[(i, j)] = res
        return memo[(i, j)]

    return dp(0, n - 1)


print(burst_balloons([3, 1, 5, 8]))
