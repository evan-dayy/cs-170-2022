def print_patterns(matrix, n):
    res = [[' '] * (len(matrix[0]) ** n) for _ in range(len(matrix) ** n)]
    res[0][0] = 'X'
    flag = matrix[0][0] == " "
    rules = {(i, j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] == "X"}
    for k in range(n):
        d0 = len(matrix) ** k
        d1 = len(matrix[0]) ** k
        for i in range(d0):
            for j in range(d1):
                for x, y in rules:
                    res[i + x * d0][j + y * d1] = res[i][j]
        if flag:
            for i in range(d0):
                for j in range(d1):
                    res[i][j] = " "
    for row in res:
        print(''.join(row))


matrix = [
    [" ", "X", "X", " "],
    ["X", " ", " ", "X"],
    [" ", "X", "X", " "]
]

print_patterns(matrix, 2)
