additionTable = [
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],  # 0 + ...
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # 1 + ...
    ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],  # 2 + ...
    ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],  # 3 + ...
    ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],  # 4 + ...
    ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],  # 5 + ...
    ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],  # 6 + ...
    ['7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],  # 7 + ...
    ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],  # 8 + ...
    ['9', '10', '11', '12', '13', '14', '15', '16', '17', '18']  # 9 + ...
]

# we also memorize how to count from 0 to 19
increment = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
             '13', '14', '15', '16', '17', '18', '19']

multiplicationTable = [  # we memorize x*y for x,y being single digits
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18'],
    ['0', '3', '6', '9', '12', '15', '18', '21', '24', '27'],
    ['0', '4', '8', '12', '16', '20', '24', '28', '32', '36'],
    ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45'],
    ['0', '6', '12', '18', '24', '30', '36', '42', '48', '54'],
    ['0', '7', '14', '21', '28', '35', '42', '49', '56', '63'],
    ['0', '8', '16', '24', '32', '40', '48', '56', '64', '72'],
    ['0', '9', '18', '27', '36', '45', '54', '63', '72', '81']
]


def strip(s):
    for i in range(len(s)):
        if i < len(s) and s[i] == "0":
            continue
        else:
            return s[i:]
    return "0"


def add(x, y):
    n = max(len(x), len(y))
    x = "0" * (n - len(x)) + x
    y = "0" * (n - len(y)) + y
    i = n - 1
    carry = 0
    res = ["0"] * (n + 1)
    while i >= 0:
        temp = additionTable[int(x[i])][int(y[i])]
        if carry == 1:
            temp = increment[int(temp)]
        res[i + 1] = temp[-1]
        if len(temp) == 2:
            carry = 1
        else:
            carry = 0
        i -= 1
    if carry == 1:
        res[0] = "1"
    return "".join(strip(res))


print(add("1212121", "234"))
print(" ---- ")


def multiple_digit(c, x):
    n = len(x)
    res = ["0"] * (n + 1)
    i = n - 1
    carry = "0"
    while i >= 0:
        temp = multiplicationTable[int(c)][int(x[i])]
        temp = add(carry, temp)
        if len(temp) == 2:
            carry = temp[0]
        else:
            carry = "0"
        res[i + 1] = temp[-1]
        i -= 1
    return "".join(strip(res))


print(multiple_digit("2", "1233"))


def multiple(x, y):
    n = max(len(x), len(y))
    x = "0" * (n - len(x)) + x
    y = "0" * (n - len(y)) + y
    result = "0"
    i = n - 1
    zeros = ""
    while i >= 0:
        result = add(result, multiple_digit(y[i], x) + zeros)
        zeros += "0"
        i -= 1
    return result


print(multiple("123333", "12"))
print(123333 * 12)


def subtract(x, y):
    return str(int(x) - int(y))


def karasuba_mul(x, y):
    n = max(len(x), len(y))
    x = "0" * (n - len(x)) + x
    y = "0" * (n - len(y)) + y

    # base case
    if n == 1:
        return multiplicationTable[int(x)][int(y)]

    xlo = x[n // 2:]
    xhi = x[: n // 2]
    ylo = y[n // 2:]
    yhi = y[:n // 2]

    A = karasuba_mul(xhi, yhi)
    B = karasuba_mul(xlo, ylo)
    E = karasuba_mul(add(xlo, xhi), add(ylo, yhi))

    res = A + "0" * len(xlo) * 2
    res = add(res, B)
    res = add(res, subtract(E, add(A, B)) + "0" * len(xlo))

    return res


print(karasuba_mul("123333", "12"))
print(123333 * 12)
