# Python Code for the above approach
m, n, k = 4, 3, 6
count = 0


# This function is used to create an empty m*n board
def makeBoard(board):
    for i in range(m):
        for j in range(n):
            board[i][j] = '_'


# This function displays our board
def displayBoard(board):
    for i in range(m):
        for j in range(n):
            print(" ", board[i][j], " ", end="")
        print()
    print()


def attack(i, j, a, board):
    if (i + 2) < m and (j - 1) >= 0:
        board[i + 2][j - 1] = a
    if (i - 2) >= 0 and (j - 1) >= 0:
        board[i - 2][j - 1] = a
    if (i + 2) < m and (j + 1) < n:
        board[i + 2][j + 1] = a
    if (i - 2) >= 0 and (j + 1) < n:
        board[i - 2][j + 1] = a
    if (i + 1) < m and (j + 2) < n:
        board[i + 1][j + 2] = a
    if (i - 1) >= 0 and (j + 2) < n:
        board[i - 1][j + 2] = a
    if (i + 1) < m and (j - 2) >= 0:
        board[i + 1][j - 2] = a
    if (i - 1) >= 0 and (j - 2) >= 0:
        board[i - 1][j - 2] = a


def canPlace(i, j, board):
    if board[i][j] == '_':
        return True
    else:
        return False


def place(i, j, k, a, board, new_board):
    # Copy the configurations of old board to new board
    for y in range(m):
        for z in range(n):
            new_board[y][z] = board[y][z]

    # Place the knight at [i][j] position on new board
    new_board[i][j] = k

    # Mark all the attacking positions of newly placed knight on the new board
    attack(i, j, a, new_board)


# Function for placing knights on board such that they don't attack each other
def kkn(k, sti, stj, board):
    # If there are no knights left to be placed, display the board and increment the count
    if k == 0:
        displayBoard(board)
        global count
        count += 1
    else:
        # Loop for checking all the positions on m*n board
        for i in range(sti, m):
            for j in range(stj, n):
                # Is it possible to place knight at [i][j] position on board?
                if canPlace(i, j, board):
                    # Create a new board and place the new knight on it
                    new_board = [["_" for x in range(n)] for y in range(m)]
                    place(i, j, 'K', 'A', board, new_board)
                    # Call the function recursively for (k-1) leftover knights
                    kkn(k - 1, i, j, new_board)

                    # Delete the new board to free up the memory
                    # del new_board
            stj = 0


board = [[0 for x in range(n)] for y in range(m)]

# Make all the places are empty
makeBoard(board)

kkn(k, 0, 0, board)

print("Total number of solutions :", count)
