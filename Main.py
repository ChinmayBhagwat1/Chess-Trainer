from pprint import pprint
import pygame as p
from Chess import chess
'''
castling
promotion
check
checkmate
stalemate
'''
checkingPiece = "--"
checkingCo = [-1, -1]
checkornot = False
possMov = []
enpassant = [0, 0]
WIDTH = HEIGHT = 512
DIMENSIONS = 8
possibleMoves = []
SQ_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15
IMAGES = {}
gs = chess.GameState()


def loadImages():
    pieces = ["wR", "wN", "wB", "wQ", "wK",
              "wp", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            "Chess/images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))


def getPossibleMoves(piece, row, col):
    global gs, enpassant, checkornot
    possibleMoves = []
    if piece[1] == "R":
        for i in range(8):
            if col != i:
                possibleMoves.append([row, i])
            if row != i:
                possibleMoves.append([i, col])
    elif piece[1] == "B":
        r = row
        c = col
        while r < 7 and c < 7:
            r = r+1
            c = c+1
            possibleMoves.append([r, c])
        r = row
        c = col
        while r > 0 and c > 0:
            r = r-1
            c = c-1
            possibleMoves.append([r, c])
        r = row
        c = col
        while r < 7 and c > 0:
            r = r+1
            c = c-1
            possibleMoves.append([r, c])
        r = row
        c = col
        while r > 0 and c < 7:
            r = r - 1
            c = c + 1
            possibleMoves.append([r, c])
    elif piece[1] == "N":
        if row+2 < 8 and col+1 < 8:
            possibleMoves.append([row+2, col+1])
        if row+2 < 8 and col-1 > -1:
            possibleMoves.append([row+2, col-1])
        if row-2 > -1 and col+1 < 8:
            possibleMoves.append([row-2, col+1])
        if row-2 > -1 and col-1 > -1:
            possibleMoves.append([row-2, col-1])
        if row+1 < 8 and col+2 < 8:
            possibleMoves.append([row+1, col+2])
        if row+1 < 8 and col-2 > -1:
            possibleMoves.append([row+1, col-2])
        if row-1 > -1 and col+2 < 8:
            possibleMoves.append([row-1, col+2])
        if row-1 > -1 and col-2 > -1:
            possibleMoves.append([row-1, col-2])

    elif piece[1] == "Q":
        for i in range(8):
            if col != i:
                possibleMoves.append([row, i])
            if row != i:
                possibleMoves.append([i, col])
        r = row
        c = col
        while r < 7 and c < 7:
            r = r + 1
            c = c + 1
            possibleMoves.append([r, c])
        r = row
        c = col
        while r > 0 and c > 0:
            r = r - 1
            c = c - 1
            possibleMoves.append([r, c])
        r = row
        c = col
        while r < 7 and c > 0:
            r = r + 1
            c = c - 1
            possibleMoves.append([r, c])
        r = row
        c = col
        while r > 0 and c < 7:
            r = r - 1
            c = c + 1
            possibleMoves.append([r, c])
    elif piece[1] == "K":  # CASTLING
        if col+1 < 8:
            possibleMoves.append([row, col+1])
            if row + 1 < 8:
                possibleMoves.append([row + 1, col + 1])
                possibleMoves.append([row + 1, col])
            if row - 1 > -1:
                possibleMoves.append([row - 1, col + 1])
                possibleMoves.append([row - 1, col])
        if col-1 > -1:
            possibleMoves.append([row, col-1])
            if row + 1 < 8:
                possibleMoves.append([row + 1, col - 1])
                possibleMoves.append([row + 1, col])
            if row - 1 > -1:
                possibleMoves.append([row - 1, col - 1])
                possibleMoves.append([row - 1, col])
    elif piece[1] == "p":
        if piece[0] == "w":
            if row == 6:
                if gs.board[row - 1][col] == '--':
                    possibleMoves.append([row - 2, col])
                    possibleMoves.append([row-1, col])
                if col-1 > -1 and gs.board[row-1][col-1][0] == 'b':
                    possibleMoves.append([row-1, col-1])
                if col+1 < 8 and gs.board[row-1][col+1][0] == 'b':
                    possibleMoves.append([row-1, col+1])
            elif row > 0:
                if gs.board[row - 1][col] == '--':
                    possibleMoves.append([row - 1, col])
                if col - 1 > -1 and gs.board[row-1][col-1][0] == 'b':
                    possibleMoves.append([row - 1, col - 1])
                if col + 1 < 8 and gs.board[row-1][col+1][0] == 'b':
                    possibleMoves.append([row - 1, col + 1])
            if row == 3 and enpassant[0] == 1:
                possibleMoves.append([2, enpassant[1]])
        if piece[0] == "b":
            if row == 1:
                if gs.board[row+1][col] == '--':
                    possibleMoves.append([row + 2, col])
                    possibleMoves.append([row+1, col])
                if col-1 > -1 and gs.board[row+1][col-1][0] == 'w':
                    possibleMoves.append([row+1, col-1])
                if col+1 < 8 and gs.board[row+1][col+1][0] == 'w':
                    possibleMoves.append([row+1, col+1])
            elif row < 7:
                if gs.board[row + 1][col] == '--':
                    possibleMoves.append([row + 1, col])
                if col - 1 > -1 and gs.board[row+1][col-1][0] == 'w':
                    possibleMoves.append([row + 1, col - 1])
                if col + 1 < 8 and gs.board[row+1][col+1][0] == 'w':
                    possibleMoves.append([row + 1, col + 1])
            if row == 4 and enpassant[0] == 1:
                possibleMoves.append([5, enpassant[1]])
    obstacleDetection(possibleMoves, piece, row, col)
    return possibleMoves


def obstacleDetection(possibleMoves, piece, row, col):
    global gs, enpassant
    toBeRemoved = []
    # candidates=[]
    # print(toBeRemoved)
    for i in possibleMoves:
        if gs.board[i[0]][i[1]] != "--":
            # candidates.append(i)
            if i[0] < row:
                if i[1] == col:
                    k = i[0]-1
                    while k > -1:
                        toBeRemoved.append([k, i[1]])
                        k -= 1
            if i[0] > row:
                if i[1] == col:
                    k = i[0]+1
                    while k < 8:
                        toBeRemoved.append([k, i[1]])
                        k += 1
            if i[1] < col:
                if i[0] == row:
                    k = i[1]-1
                    while k > -1:
                        toBeRemoved.append([i[0], k])
                        k -= 1
            if i[1] > col:
                if i[0] == row:
                    k = i[1]+1
                    while k < 8:
                        toBeRemoved.append([i[0], k])
                        k += 1
            if i[0] < row:
                if i[1] < col:
                    k = i[0]-1
                    j = i[1]-1
                    while k > -1 and j > -1:
                        toBeRemoved.append([k, j])
                        k -= 1
                        j -= 1
            if i[0] > row:
                if i[1] > col:
                    k = i[0] + 1
                    j = i[1] + 1
                    while k < 8 and j < 8:
                        toBeRemoved.append([k, j])
                        k += 1
                        j += 1
            if i[0] < row:
                if i[1] > col:
                    k = i[0] - 1
                    j = i[1] + 1
                    while k > -1 and j < 8:
                        toBeRemoved.append([k, j])
                        k -= 1
                        j += 1
            if i[0] > row:
                if i[1] < col:
                    k = i[0] + 1
                    j = i[1] - 1
                    while k < 8 and j > -1:
                        toBeRemoved.append([k, j])
                        k += 1
                        j -= 1
        if piece[0] == gs.board[i[0]][i[1]][0]:
            toBeRemoved.append(i)
    for i in toBeRemoved:
        for j in possibleMoves:
            if i == j:
                possibleMoves.remove(j)
    if checkornot:
        checkMoves = checkMo()
        newMoves = []
        for i in possibleMoves:
            for j in checkMoves:
                if i[0] == j[0] and i[1] == j[1]:
                    newMoves.append(i)
        possibleMoves = newMoves


'''def validMoves(piece,row,col):   

def validOrNot(piece,row1,col1,row2,col2):
    if piece=='wR' or piece=='bR':
'''


def stale(prev):
    global gs
    flag = 0
    for i in range(8):
        for j in range(8):
            if prev[0] == 'w':
                if gs.board[i][j][0] == 'b' and gs.board[i][j][1] != 'K':
                    pm = getPossibleMoves(gs.board[i][j], i, j)
                    if len(pm) != 0:
                        flag = 1
                        break
            if prev[0] == 'b':
                if gs.board[i][j][0] == 'w' and gs.board[i][j][1] != 'K':
                    pm = getPossibleMoves(gs.board[i][j], i, j)
                    if len(pm) != 0:
                        flag = 1
                        break
        if flag == 1:
            break
    if flag == 0:
        return True
    else:
        return False


def checkMo():
    global possMov, gs, checkornot, checkingCo, checkingPiece
    kingplace = [-1, -1]
    checkMoves = []
    if checkornot:
        if checkingPiece[0] == 'w':
            for i in possMov:
                if gs.board[i[0]][i[1]] == 'bK':
                    kingplace = i
        else:
            for i in possMov:
                if gs.board[i[0]][i[1]] == 'wK':
                    kingplace = i
        if checkingPiece[1] == "R":
            if checkingCo[0] == kingplace[0]:
                if checkingCo[1] < kingplace[1]:
                    for j in range(checkingCo[1], kingplace[1]):
                        checkMoves.append([checkingCo[0], j])
                else:
                    for j in range(checkingCo[1], kingplace[1], -1):
                        checkMoves.append([checkingCo[0], j])
            elif checkingCo[1] == kingplace[1]:
                if checkingCo[0] < kingplace[0]:
                    for j in range(checkingCo[0], kingplace[0]):
                        checkMoves.append([j, checkingCo[1]])
                else:
                    for j in range(checkingCo[0], kingplace[0], -1):
                        checkMoves.append([j, checkingCo[1]])
        elif checkingPiece[1] == "B":
            r = checkingCo[0]
            c = checkingCo[1]
            if checkingCo[0] < kingplace[0] and checkingCo[1] < kingplace[1]:
                while r != kingplace[0]-1:
                    checkMoves.append([r, c])
                    r = r + 1
                    c = c + 1
                checkMoves.append([r, c])
            elif checkingCo[0] < kingplace[0] and checkingCo[1] > kingplace[1]:
                while r != kingplace[0]-1:
                    checkMoves.append([r, c])
                    r = r + 1
                    c = c - 1
                checkMoves.append([r, c])
            elif checkingCo[0] > kingplace[0] and checkingCo[1] < kingplace[1]:
                while r != kingplace[0]+1:
                    checkMoves.append([r, c])
                    r = r - 1
                    c = c + 1
                checkMoves.append([r, c])
            elif checkingCo[0] > kingplace[0] and checkingCo[1] > kingplace[1]:
                while r != kingplace[0]+1:
                    checkMoves.append([r, c])
                    r = r - 1
                    c = c - 1
                checkMoves.append([r, c])
        elif checkingPiece[1] == "N":
            checkMoves = []

        elif checkingPiece[1] == "Q":
            if checkingCo[0] == kingplace[0]:
                if checkingCo[1] < kingplace[1]:
                    for j in range(checkingCo[1] + 1, kingplace[1]):
                        checkMoves.append([checkingCo[0], j])
                else:
                    for j in range(checkingCo[1] - 1, kingplace[1], -1):
                        checkMoves.append([checkingCo[0], j])
            elif checkingCo[1] == kingplace[1]:
                if checkingCo[0] < kingplace[0]:
                    for j in range(checkingCo[0] + 1, kingplace[0]):
                        checkMoves.append([j, checkingCo[1]])
                else:
                    for j in range(checkingCo[0] - 1, kingplace[0], -1):
                        checkMoves.append([j, checkingCo[1]])
            r = checkingCo[0]
            c = checkingCo[1]
            if checkingCo[0] < kingplace[0] and checkingCo[1] < kingplace[1]:
                while r != kingplace[0] - 1:
                    checkMoves.append([r, c])
                    r = r + 1
                    c = c + 1
                checkMoves.append([r, c])
            elif checkingCo[0] < kingplace[0] and checkingCo[1] > kingplace[1]:
                while r != kingplace[0] - 1:
                    checkMoves.append([r, c])
                    r = r + 1
                    c = c - 1
                checkMoves.append([r, c])
            elif checkingCo[0] > kingplace[0] and checkingCo[1] < kingplace[1]:
                while r != kingplace[0] + 1:
                    checkMoves.append([r, c])
                    r = r - 1
                    c = c + 1
                checkMoves.append([r, c])
            elif checkingCo[0] > kingplace[0] and checkingCo[1] > kingplace[1]:
                while r != kingplace[0] + 1:
                    checkMoves.append([r, c])
                    r = r - 1
                    c = c - 1
                checkMoves.append([r, c])
        elif checkingPiece[1] == "p":
            checkMoves = []

    return checkMoves


def aroundKing(prev):
    for i in range(8):
        for j in range(8):
            if prev[0] == 'w':
                if gs.board[i][j][0] == 'b' and gs.board[i][j][1] != 'K':
                    pm = getPossibleMoves(gs.board[i][j], i, j)

            if prev[0] == 'b':
                if gs.board[i][j][0] == 'w' and gs.board[i][j][1] != 'K':
                    pm = getPossibleMoves(gs.board[i][j], i, j)


def isCheck(piece, co):
    global possMov, checkingPiece, checkingCo
    possMov = getPossibleMoves(piece, co[0], co[1])
    #obstacleDetection(piece, co[0], co[1])
    flag = False
    checkingPiece = piece
    checkingCo = co
    if piece[1] != 'p':
        for i in possMov:
            if piece[0] == 'w':
                if gs.board[i[0]][i[1]] == "bK":
                    flag = True
            else:
                if gs.board[i[0]][i[1]] == "wK":
                    flag = True
    else:
        for i in possMov:
            if piece[0] == 'w':
                if gs.board[i[0]][i[1]] == "bK" and i[1] != co[1]:
                    flag = True
            else:
                if gs.board[i[0]][i[1]] == "wK" and i[1] != co[1]:
                    flag = True
    return flag


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    global possibleMoves, gs, enpassant, checkornot
    prev = "--"
    row1 = -1
    row2 = -1
    col1 = -1
    col2 = -1
    switch = 0
    # print(gs.board)
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and switch == 0:
                switch = 1
                location1 = p.mouse.get_pos()
                col1 = location1[0]//64
                row1 = location1[1]//64
                prev = gs.board[row1][col1]
                if prev == '--':
                    switch = 0
                possibleMoves = getPossibleMoves(prev, row1, col1)
                # obstacleDetection(prev,row1,col1)

                # print(possibleMoves)
                if checkornot:
                    checkm = checkMo()
                    if prev[1] != 'K':
                        spare = []
                        for i in possibleMoves:
                            for j in checkm:
                                if i[0] == j[0] and i[1] == j[1]:
                                    spare.append(i)
                        possibleMoves = spare
                    else:
                        for i in possibleMoves:
                            for j in checkm:
                                if i[0] == j[0] and i[1] == j[1]:
                                    possibleMoves.remove(i)

            elif e.type == p.MOUSEBUTTONDOWN and switch == 1:
                location2 = p.mouse.get_pos()
                col2 = location2[0] // 64
                row2 = location2[1] // 64
                gs.board[row1][col1] = '--'
                gs.board[row2][col2] = prev
                a = 5
                if prev[0] == "w":
                    a = 0
                else:
                    a = 7
                if row2 == a and prev[1] == "p":
                    pawnPromotion(prev, row2, col2)
                switch = 0
                print(stale(prev))
                checkornot = isCheck(prev, [row2, col2])

            # condition for check

            # print(checkornot)

            # condition for enpassant
            if prev[1] == 'p':
                if prev[0] == 'w':
                    if row1 == 6 and row2 == 4:
                        enpassant[0] = 1
                        enpassant[1] = col2
                    else:
                        enpassant[0] = 0
                else:
                    if row1 == 1 and row2 == 3:
                        enpassant[0] = 1
                        enpassant[1] = col2
                    else:
                        enpassant[0] = 0
            else:
                enpassant[0] = 0

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        #possibleMoves = []


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global possibleMoves
    colors = [p.Color("burlywood"), p.Color("burlywood4"), p.Color("brown1")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r+c) % 2)]
            for i in possibleMoves:
                if r == i[0] and c == i[1]:
                    color = colors[2]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def pawnPromotion(piece, row, col):
    global gs
    gs.board[row][col] = piece[0] + "Q"


main()
