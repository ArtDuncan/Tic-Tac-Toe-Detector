import time
import sys

board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
turn = 0
done = False

#Loops through the array storing the board checking for empty spaces
def checkFull(board):
    done = True
    for x in board:
        if x == 0:
            done = False
    return done

#Asks user to make a move and does it
def makeMove(board):
    validMove = False
    #Loops in case nonvalid move input
    while validMove == False:
        validMove = True
        if(turn%2 == 0):
            print("It is X's turn, please ", end="")
        if(turn%2 == 1):
            print("It is O's turn, please ", end="")
        location = input("Input a move: ")

        #Checks if the input is valid
        try:
            spot = int(location)
        except ValueError:
            validMove = False

        if validMove==False or int(location) < 1 or int(location) > 9 or board[int(location)-1] != 0:
            validMove = False
            print("Invalid move, please try again.", end=" ")
    #Updates the board
    board[int(location)-1] = (turn % 2) + 1

def importPosition(board, input):
    xs = 0
    ys = 0
    global turn
    for x in range(0, len(board)):
        test = input.read(1)
        #print(test)
        if test == "0":
            board[x] = 0
        elif test == "1":
            board[x] = 1
            xs = xs+1
        elif test == "2":
            board[x] = 2
            ys = ys+1
        input.read(1)
    print("{0} x's found, {1} y's found".format(xs, ys))
    if xs == ys:
        turn = 2
    elif xs == ys+1:
        turn = 1
    else:
        for x in range(0, len(board)):
            board[x] = 0
        print("Improper board detected. Import Failed")
    return board

def checkWin(board):
    winner = 0
    #Checks horizontal win possibilities
    if (board[0] == 1 or board[0] == 2) and board[0] == board[1] and board[0] == board[2]:
        winner = board[0]
        return winner
    if (board[3] == 1 or board[3] == 2) and board[3] == board[4] and board[3] == board[5]:
        winner = board[3]
        return winner
    if (board[6] == 1 or board[6] == 2) and board[6] == board[7] and board[6] == board[8]:
        winner = board[6]
        return winner
    #Checks vertical win possibilities
    if (board[0] == 1 or board[0] == 2) and board[0] == board[3] and board[0] == board[6]:
        winner = board[0]
        return winner
    if (board[1] == 1 or board[1] == 2) and board[1] == board[4] and board[1] == board[7]:
        winner = board[1]
        return winner
    if (board[2] == 1 or board[2] == 2) and board[2] == board[5] and board[2] == board[8]:
        winner = board[2]
        return winner
    #Checks diagonal win possibilites
    if (board[0] == 1 or board[0] == 2) and board[0] == board[4] and board[0] == board[8]:
        winner = board[0]
        return winner
    if (board[2] == 1 or board[2] == 2) and board[2] == board[4] and board[2] == board[6]:
        winner = board[2]
        return winner
    return winner

#Prints out the board
def showBoard2(board):
    for x in range(3):
        for y in range(3):
            if board[x*3+y] == 1:
                print(" X ", end="")
            elif board[x*3+y] == 2:
                print(" O ", end="")
            elif board[x*3+y] == 0:
                print("   ", end="")
            if (y)%3 != 2:
                print("|", end="")
        if x != 2:
            print("\n-----------")
    print()

#Game code
showBoard2(board)
winner = 0
#mode = input("Send an X to start or the text file to import a board: ")
if len(sys.argv) > 1:
    #print("Argument Detected")
    importInfo = open(sys.argv[1], "r")
    board = importPosition(board, importInfo)
    importInfo.close()
    showBoard2(board)
    winner = checkWin(board)
while winner == 0:
    makeMove(board)
    showBoard2(board)
    if checkFull(board) == True:
        break
    winner = checkWin(board)
    turn = turn + 1

if winner == 0:
    print("Game is a draw")
elif winner == 1:
    print("Winner is X")
elif winner == 2:
    print("Winner is O")
print("Game Over!")