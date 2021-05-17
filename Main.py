from __future__ import print_function
from pprint import pprint
import pygame as p
from Chess import chess
from Chess import engine
import re
import sys
import time
from itertools import count
from collections import namedtuple
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

global hist

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
        # if checkingPiece[0] == 'w':
        #     for i in possMov:
        #         if gs.board[i[0]][i[1]] == 'bK':
        #             kingplace = i
        if checkingPiece[0] == 'b':
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


def aroundKing(prev, row, col):
    for i in range(8):
        for j in range(8):
            if prev[0] == 'w':
                if gs.board[i][j][0] == 'b' and gs.board[i][j][1] != 'K':
                    pm = getPossibleMoves(gs.board[i][j], i, j)
                    pmk = getPossibleMoves(prev, row, col)
                    for x in pm:
                        for y in pmk:
                            if x[0] == y[0] and x[1] == y[1]:
                                possibleMoves.remove(x)
            if prev[0] == 'b':
                if gs.board[i][j][0] == 'w' and gs.board[i][j][1] != 'K':
                    pm = getPossibleMoves(gs.board[i][j], i, j)
                    pmk = getPossibleMoves(prev, row, col)
                    for x in pm:
                        for y in pmk:
                            if x[0] == y[0] and x[1] == y[1]:
                                possibleMoves.remove(x)


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
    global hist,listy,click_flagger
    hist = [engine.Position(
        engine.initial, 0, (True, True), (True, True), 0, 0)]
    searcher = engine.Searcher()
    p.init()
    screen = p.display.set_mode((WIDTH+192, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    global possibleMoves, gs, enpassant, checkornot
    prev = "--"
    row1 = -1
    row2 = -1
    col1 = -1
    col2 = -1
    switch = 0
    isWhiteturn = True
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
                if location1[0] > WIDTH or location1[1] > HEIGHT:
                    break
                col1 = location1[0]//64
                row1 = location1[1]//64
                prev = gs.board[row1][col1]
                if prev == '--':
                    switch = 0
                if (prev[0] == 'w'):
                    possibleMoves = getPossibleMoves(prev, row1, col1)
                    if prev[1] == 'K':
                        aroundKing(prev, row1, col1)
                else:
                    switch = 0
                # obstacleDetection(prev,row1,col1)
                # print(possibleMoves)
                if checkornot and checkingPiece[0] == 'b':
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
                if location2[0] > WIDTH or location2[1] > HEIGHT:
                    break
                col2 = location2[0] // 64
                row2 = location2[1] // 64
                flagger = 0
                for z in possibleMoves:
                    if z[0] == row2 and z[1] == col2:
                        flagger = 1
                        gs.board[row1][col1] = '--'
                        gs.board[row2][col2] = prev
                        isWhiteturn = not(isWhiteturn)
                if flagger == 0:
                    switch = 0
                    break
                click_flagger=0
                a = 5
                if prev[0] == "w":
                    a = 0
                else:
                    a = 7
                if row2 == a and prev[1] == "p":
                    pawnPromotion(prev, row2, col2)
                switch = 0
                checkornot = isCheck(prev, [row2, col2])
                ##
                drawGameState(screen, gs)
                clock.tick(MAX_FPS)
                p.display.flip()
                ##
                list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                stringco = list1[col1]+str(8-row1)+list1[col2]+str(8-row2)

                engine.print_pos(hist[-1])

                if hist[-1].score <= -engine.MATE_LOWER:
                    print("You lost")
                    break

                # We query the user until she enters a (pseudo) legal move.
                move = None

                while move not in hist[-1].gen_moves():
                    print(stringco)
                    # input replace kar bc
                    match = re.match('([a-h][1-8])'*2, stringco)
                    if match:
                        move = engine.parse(match.group(
                            1)), engine.parse(match.group(2))
                    else:
                        # Inform the user when invalid input (e.g. "help") is entered
                        print("Please enter a move like g8f6")
                hist.append(hist[-1].move(move))

                # After our move we rotate the board and print it again.
                # This allows us to see the effect of our move.
                engine.print_pos(hist[-1].rotate())

                if hist[-1].score <= -engine.MATE_LOWER:
                    print("You won")
                    break

                # Fire up the engine to look for a move.
                start = time.time()
                for _depth, move, score in searcher.search(hist[-1], hist):
                    if time.time() - start > 1:
                        break

                if score == engine.MATE_UPPER:
                    print("Checkmate!")

                # The black player moves from a rotated position, so we have to
                # 'back rotate' the move before printing it.
                frome = engine.render(119-move[0])
                toe = engine.render(119-move[1])
                print("My move:", frome + toe)
                # black plays here
                for i in range(len(list1)):
                    if list1[i] == frome[0]:
                        colb1 = i
                rowb1 = 8-int(frome[1])
                for i in range(len(list1)):
                    if list1[i] == toe[0]:
                        colb2 = i
                rowb2 = 8-int(toe[1])
                temp = gs.board[rowb1][colb1]
                gs.board[rowb1][colb1] = '--'
                gs.board[rowb2][colb2] = temp
                hist.append(hist[-1].move(move))

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

click_flagger=0
listy= []
def drawBoard(screen):
    global click_flagger,listy
    red = (200, 0, 0)
    blue = (0, 0, 200)
    bright_red = (255, 0, 0)
    bright_blue = (0, 0, 255)
    bright_green = (0, 255, 0)
    white = (255, 255, 255)

    global possibleMoves
    colors = [p.Color("burlywood"), p.Color("burlywood4"), p.Color("brown1")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r+c) % 2)]
            for i in possibleMoves:
                if r == i[0] and c == i[1]:
                    color = colors[2]
            if click_flagger==1:
                if r==listy[0] and c == listy[1]:
                    color = bright_green
                if r==listy[2] and c == listy[3]:
                    color = bright_green
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    mouse = p.mouse.get_pos()
    click = p.mouse.get_pressed()
    smallText = p.font.Font("freesansbold.ttf", 20)
    if 544+128 > mouse[0] > 544 and 224+64 > mouse[1] > 224:
        p.draw.rect(screen, bright_blue, (544, 224, 128, 64))
        text = smallText.render("HINT", True, red, bright_blue)
        # for e in p.event.get():
        if click[0] == 1:
            click_flagger=1
            listy=Hint()
            for r in range(DIMENSIONS):
                for c in range(DIMENSIONS):
                    color = colors[((r+c) % 2)]
                    for i in possibleMoves:
                        if r == i[0] and c == i[1]:
                            color = colors[2]
                    if r==listy[0] and c == listy[1]:
                        color = bright_green
                    if r==listy[2] and c == listy[3]:
                        color = bright_green
                    p.draw.rect(screen, color, p.Rect(
                        c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    else:
        p.draw.rect(screen, blue, (544, 224, 128, 64))
        text = smallText.render("HINT", True, red, blue)

    textRect = text.get_rect()
    textRect.center = ((544+(128/2)), (224+32))
    screen.blit(text, textRect)


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


def Hint():
    global hist
    searcher = engine.Searcher()
    list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    #stringco = list1[col1]+str(8-row1)+list1[col2]+str(8-row2)
    print("Hi")
    # Fire up the engine to look for a move.
    start = time.time()
    for _depth, move, score in searcher.search(hist[-1], hist):
        if time.time() - start > 1:
            break

    frome = engine.render(move[0])
    toe = engine.render(move[1])

    for i in range(len(list1)):
        if list1[i] == frome[0]:
            colb1 = i
    rowb1 = 8-int(frome[1])
    for i in range(len(list1)):
        if list1[i] == toe[0]:
            colb2 = i
    rowb2 = 8-int(toe[1])
    listy=[rowb1,colb1,rowb2,colb2]
    return listy

main()
