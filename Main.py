from pprint import pprint
import pygame as p
from Chess import chess
'''
castling
enpassant
promotion
check
checkmate
stalemate
'''
WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15
IMAGES = {}
possibleMoves = []
gs = chess.GameState()


def loadImages():
    pieces = ["wR", "wN", "wB", "wQ", "wK",
              "wp", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            "Chess/images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))


def getPossibleMoves(piece, row, col):
    global possibleMoves, gs
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
    elif piece[1] == "p":  # enpassant
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
            else:
                pass
                # put promoting condition here
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
            else:
                pass
                # put promoting condition here


def obstacleDetection(piece, row, col):
    global possibleMoves, gs
    toBeRemoved = []
    # candidates=[]
    print(toBeRemoved)
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


'''def validMoves(piece,row,col):   

def validOrNot(piece,row1,col1,row2,col2):
    if piece=='wR' or piece=='bR':
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    global gs

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
                getPossibleMoves(prev, row1, col1)
                obstacleDetection(prev, row1, col1)

                # print(possibleMoves)

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
                # print(prev)
                switch = 0
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
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
