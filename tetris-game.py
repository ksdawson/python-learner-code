# SAMS 2018, Programming Section C
#########################################
# Full name: Kameron Dawson
# Andrew ID: ksdawson
#########################################

# DUE DATE: Sunday August 6th, 5pm
# SUBMIT THIS FILE TO AUTOLAB. LATE SUBMISSIONS WILL NOT BE ACCEPTED.

# For this assignment, you will build the game Tetris!
# You should do this by following the instructions in this website:
# https://www.cs.cmu.edu/~112/notes/notes-tetris/

# NOTE: if you choose to add bonus features to your Tetris, please submit the
# base Tetris implementation to hw5 and the bonus implementation to hw5-bonus,
# to help us with grading.

from tkinter import *
import random

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.x = 0
    data.y = 0
    data.z = 0
    data.keysym =  ""
    data.rows = 15
    data.cols = 10
    data.cellSize = 20 
    data.margin = 25
    data.board = [ ]
    data.timerDelay = 400
    data.isGameOver = False
    data.score = 0
    for row in range(0, 15):
        z = [ ]
        for col in range(0, 10):
            z.append("blue")
        data.board.append(z)
    data.emptyColor = "blue"
    
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    newFallingPiece(data)
    
def newFallingPiece(data):
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    fallingPieceCol = len(data.fallingPiece[0])
    data.fallingPieceCol = data.cols//2 - fallingPieceCol//2
    
    if fallingPieceIsLegal(data) == False:
        data.isGameOver = True
    
def drawFallingPiece(canvas, data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                drawCell(canvas, data, row+data.fallingPieceRow, col+data.fallingPieceCol, data.fallingPieceColor)
            else:
                continue

def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow = data.fallingPieceRow + drow
    data.fallingPieceCol = data.fallingPieceCol + dcol
    if fallingPieceIsLegal(data) == False:
        data.fallingPieceRow = data.fallingPieceRow - drow
        data.fallingPieceCol = data.fallingPieceCol - dcol
        return False
    return True
        
def rotatingFallingPiece(data):
    oldNumRows = len(data.fallingPiece)
    oldNumCols = len(data.fallingPiece[0])
    oldRow = data.fallingPieceRow
    oldCenterRow = oldRow + oldNumRows//2
    oldCol = data.fallingPieceCol
    oldCenterCol = oldCol + oldNumCols//2
    oldPiece = data.fallingPiece
    
    colSum = (data.fallingPieceCol*len(data.fallingPiece[0]) + len(data.fallingPiece[0])-1)// len(data.fallingPiece[0])
    rowSum = (data.fallingPieceRow*len(data.fallingPiece) + len(data.fallingPiece)-1)// len(data.fallingPiece)
    
    newNumRows = oldNumCols
    newNumCols = oldNumRows
    newRow = oldRow + oldNumRows/2 - newNumRows/2
    newCenterRow = newRow + newNumRows/2 
    newCol = oldCol + oldNumCols/2 - newNumCols/2
    newCenterCol = newCol + newNumCols/2
    newPiece = []
    
    for row in range(0, newNumRows):
        z = []
        for col in range(0, newNumCols):
            z.append("False")
        newPiece.append(z)
    for row in range(0, newNumRows):
        for col in range(0, newNumCols):
            newPiece[row][col] = oldPiece[col][row]
    
    data.fallingPiece = newPiece
    data.fallingPieceRow = colSum + rowSum - data.fallingPieceCol 
    data.fallingPieceCol = data.fallingPieceRow + colSum - rowSum
    if not fallingPieceIsLegal(data):
        data.fallingPiece = oldPiece 
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol

def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if (data.fallingPieceCol+col<0 or data.fallingPieceCol+col>9 or data.fallingPieceRow+row<0 or data.fallingPieceRow+row>14) or (data.fallingPiece[row][col]==True and data.board[data.fallingPieceRow+row][data.fallingPieceCol+col]!="blue"):
                return False
    return True

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.isGameOver == False:
        if event.keysym == "Up":
            rotatingFallingPiece(data)
        elif event.keysym == "Down":
            moveFallingPiece(data, 1, 0)
        elif event.keysym == "Left":
            moveFallingPiece(data, 0, -1)
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, 1)
    if event.keysym == "r":
        init(data)

def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                data.board[row+data.fallingPieceRow][col+data.fallingPieceCol] = data.fallingPieceColor
            else:
                continue
    newFallingPiece(data)
    while removeFullRow(data) == True:
        continue
    
def timerFired(data):
    if moveFallingPiece(data, 1, 0) == False:
        placeFallingPiece(data)

def removeFullRow(data):
    for row in range(len(data.board)):
        count = True
        for col in range(len(data.board[row])):
            if data.board[row][col] == data.emptyColor:
                count = False
        if count:
            data.board.pop(row)
            z = [ [data.emptyColor] * data.cols]
            data.board = z + data.board
            data.score = data.score + 1
            return True
    return False

def drawCell(canvas, data, row, col, color):
    canvas.create_rectangle(col*data.cellSize+data.margin,row*data.cellSize+data.margin,
        col*data.cellSize+data.margin+data.cellSize,row*data.cellSize+data.margin+data.cellSize,fill=color,width=5)
    
def drawBoard(canvas, data):
    for row in range(0, 15):
        for col in range(0,10):
            drawCell(canvas, data, row, col, data.board[row][col])
        
def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0,0,data.width,data.height,fill="orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    
    if data.isGameOver == False:
        score = str(data.score)
        canvas.create_text(data.width*0.5,data.margin*0.5,text="Score: "+score,fill="blue",font="Times 10 bold")
    
    if data.isGameOver == True:
        canvas.create_rectangle(data.margin,data.margin,data.width-data.margin,data.margin+data.cellSize*2,fill="black") 
        canvas.create_text(data.width*0.5,data.margin+data.cellSize,text="Gameover!",fill="yellow",font="Times 20 italic bold")

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris(rows=15, cols=10, cellSize=20, margin=25):
    # fill in code here!
    width = cols * cellSize + margin * 2
    height = rows * cellSize + margin * 2
    run(width,height)

playTetris()