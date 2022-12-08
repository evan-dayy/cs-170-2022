# KARATSUBA IMPLEMENTATION W/O USING BUILT-IN ARITHMETIC

# Taken from https://www.addiscoder.com/syllabus/2019/
# Originally authored by Jelani Nelson

# first, we memorize how to add single digits to each other
# additionTable[i][j] gives result of i+j for single digits i, j
additionTable = [
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], # 0 + ...
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], # 1 + ...
    ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'], # 2 + ...
    ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], # 3 + ...
    ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13'], # 4 + ...
    ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14'], # 5 + ...
    ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15'], # 6 + ...
    ['7', '8', '9', '10', '11', '12', '13', '14', '15', '16'], # 7 + ...
    ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17'], # 8 + ...
    ['9', '10', '11', '12', '13', '14', '15', '16', '17', '18'] # 9 + ...
]

# we also memorize how to count from 0 to 19
increment = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
             '13', '14', '15', '16', '17', '18', '19']

def stripLeadingZeroes(s):
    i = 0
    while i<len(s) and s[i]=='0':
        i += 1
    if i == len(s):
        return '0'
    else:
        return s[i:]

# take as input x,y as strings of digits
def add(x, y):
    if len(x) < len(y):
        x = '0'*(len(y)-len(x)) + x
    else:
        y = '0'*(len(x)-len(y)) + y
    # now both numbers are n digits
    # the answer will have either n+1 or n digits
    n = len(x)
    
    # we start adding from the rightmost digit
    i = n-1
    carry = 0
    
    result = ['0']*(n+1)
    
    while i >= 0:
        d = additionTable[int(x[i])][int(y[i])]
        if carry == 1:
            d = increment[int(d)]
        result[i+1] =  d[len(d)-1]
        if len(d) == 2:
            carry = 1
        else:
            carry = 0
        i -= 1
        
    if carry == 1:
        result[0] = '1'
        
    return ''.join(stripLeadingZeroes(result))

multiplicationTable = [ # we memorize x*y for x,y being single digits
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

# N^2 MULTIPLICATION

# c is a single digit number, and x is arbitrary length. return c*x.
# c and x are strings
def multiplyDigit(c, x):
    result = ['0']*(len(x)+1)
    carry = '0'
    i = len(x)-1
    while i >= 0:
        d = multiplicationTable[int(c)][int(x[i])]
        d = add(d, carry)
        result[i+1] = d[len(d)-1]
        if len(d) == 2:
            carry = d[0]
        else:
            carry = '0'
        i -= 1
    return ''.join(stripLeadingZeroes(result))

# full multiplication, where both x,y can have arbitrary # of digits
# again x,y are strings of digits
def grade_school_multiply(x, y):
    # make x and y have the same length
    if len(x) < len(y):
        x = '0'*(len(y)-len(x)) + x
    else:
        y = '0'*(len(x)-len(y)) + y
        
    n = len(x)
    result = '0'
    
    i = n-1
    zeroes = ''
    while i >= 0:
        result = add(result, multiplyDigit(y[i], x) + zeroes)
        zeroes += '0'
        i -= 1
    return result

# NOW N^{\log_2 3} MULTIPLICATION VIA KARATSUBA

# doing subtraction by hand is similar to addition. we'll leave doing it from
# scratch as an exercise for you, and here we will just "cheat" and use Python's
# built-in subtraction
def subtract(x, y):
    return str(int(x) - int(y))

def karatsuba_mul(x, y):
    n = max(len(x), len(y))
    x = '0'*(n-len(x)) + x
    y = '0'*(n-len(y)) + y
    
    if n == 1:
        return multiplicationTable[int(x)][int(y)]
    
    xlo = x[n//2:]
    ylo = y[n//2:]
    xhi = x[:n//2]
    yhi = y[:n//2]
    
    A = karatsuba_mul(xhi, yhi)
    B = karatsuba_mul(xlo, ylo)
    E = karatsuba_mul(add(xlo, xhi), add(ylo, yhi))
    
    result = A + '0'*(2*len(xlo))
    result = add(result, subtract(E, add(A, B))+'0'*len(xlo))
    result = add(result, B)
    
    return result


print(karatsuba_mul('24','451'))
print(24*451)
