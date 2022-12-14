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


def stripLeadingZeros(s):
    i = 0
    while i < len(s) and s[i] == "0":
        i += 1
    if i == len(s):
        return "0"
    return s[i:]


def add(x, y):
    if len(x) < len(y):
        x = "0" * (len(y) - len(x)) + x
    else:
        y = "0" * (len(x) - len(y)) + y
    n = len(x)
    res = ["0"] * (n + 1)
    carry = 0
    for i in range(n - 1, -1, -1):
        d = additionTable[int(x[i])][int(y[i])]
        if carry == 1:
            d = increment[int(d)]
        res[i + 1] = d[-1]
        if len(d) == 2:
            carry = 1
        else:
            carry = 0
    if carry ==GO 1:
        res[0] = "1"
    return "".join(stripLeadingZeros(res))


def multipleDigit(c, x):
    n = len(x)
    res = ["0"] * (n + 1)
    carry = "0"
    for i in range(n - 1, -1, -1):
        d = multiplicationTable[int(c)][int(x[i])]
        d = add(d, carry)
        res[i + 1] = d[-1]
        if len(d) == 2:
            carry = d[0]
        else:
            carry = "0"
    if carry != "0":
        res[0] = carry
    return "".join(stripLeadingZeros(res))


def grade_school_multiple(x, y):
    if len(x) < len(y):
        x = "0" * (len(y) - len(x)) + x
    else:
        y = "0" * (len(x) - len(y)) + y
    n = len(x)
    result = "0"
    zeros = ""
    for i in range(n - 1, -1, -1):
        result = add(result, multipleDigit(y[i], x) + zeros)
        zeros += "0"
    return result


def subtract(x, y):
    return str(int(x) - int(y))


def Karatsuba(x, y):
    n = max(len(x), len(y))
    x = '0' * (n - len(x)) + x
    y = '0' * (n - len(y)) + y
    if n == 1:
        return multiplicationTable[int(x)][int(y)]

    x_low = x[n // 2:]
    x_high = x[:n // 2]
    y_low = y[n // 2:]
    y_high = y[:n // 2]

    A = Karatsuba(x_high, y_high)
    B = Karatsuba(x_low, y_low)
    E = Karatsuba(add(x_low, x_high), add(y_low, y_high))

    result = A + "0" * 2 * len(x_low)
    result = add(result, B)
    result = add(result, subtract(E, add(A, B)) + "0" * len(x_low))
    return result


print(add("29", "19"))
print(multipleDigit("8", "29"))
print(grade_school_multiple("123", "123"))
print(Karatsuba("123", "123"))
print(123 * 123)

