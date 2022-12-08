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

print(add("12", "94"))
