import sys, select, tty, termios
from random import randint, shuffle, choice
from time import sleep

def placeTetromino(t, board, pos):
    for x in range(len(t)):
        for y in range(len(t)):
            try:
                arr = list(board[y+pos[1]])
                if t[y][x] != ' ':
                    arr[x+pos[0]] = t[y][x]
                board[y+pos[1]] = ''.join(arr)
            except:
                pass

def drawTetromino(t, pos):
    for y in range(len(t)):
        sys.stdout.write(f'\x1b[{pos[1]+2+y};{pos[0]*2+3}H')
        for x in range(len(t)):
            char = t[y][x]
            if char == 'i':
                sys.stdout.write('\x1b[36m[]')
            elif char == 'j':
                sys.stdout.write('\x1b[34m[]')
            elif char == 'l':
                sys.stdout.write('\x1b[33m[]')
            elif char == 'o':
                sys.stdout.write('\x1b[38;5;226m[]')
            elif char == 'z':
                sys.stdout.write('\x1b[31m[]')
            elif char == 't':
                sys.stdout.write('\x1b[35m[]')
            elif char == 's':
                sys.stdout.write('\x1b[32m[]')
            else:
                sys.stdout.write('\x1b[2C')
    sys.stdout.write('\x1b[0m')

def doesPieceFit(t, board, pos):
    for y in range(len(t)):
        for x in range(len(t)):
            if t[y][x] != ' ':
                if pos[0]+x < 0 or pos[0]+x > 9:
                    return False
                if pos[1]+y > 19:
                    return False
                try:
                    if board[pos[1]+y][pos[0]+x] != ' ':
                        return false
                except:
                    return False

    return True

def drawShadow(t, board, pos):
    offset = 0
    while True:
        if doesPieceFit(t, board, (pos[0], pos[1] + offset)):
            offset += 1
        else:
            break

    sys.stdout.write('\x1b[38;5;244m')
    for y in range(len(t)):
        sys.stdout.write(f'\x1b[{pos[1]+1+y+offset};{pos[0]*2+3}H')
        for x in range(len(t)):
            char = t[y][x]
            if char == ' ':
                sys.stdout.write('\x1b[2C')
            else:
                sys.stdout.write('::')
    sys.stdout.write('\x1b[0m')

def checkLines(board):
    for y, line in enumerate(board):
        filled = True
        for x in range(10):
            if line[x] == ' ':
                filled = False

        if filled:
            board[y] = '=========='

    return board

def clearLines(board):
    b = [line for line in board if '=' not in line]
    n = 20-len(b)
    for x in range(n):
        b.insert(0, ' '*10)

    return b

def rotate(t, n):
    new = t

    if len(t) == 3:
        if n == 0:
            new = t
        elif n == 1:
            new = [[t[2][0], t[1][0], t[0][0]], [t[2][1], t[1][1], t[0][1]], [t[2][2], t[1][2], t[0][2]]]
        elif n == 2:
            new = [[t[2][2], t[2][1], t[2][0]], [t[1][2], t[1][1], t[1][0]], [t[0][2], t[0][1], t[0][0]]]
        elif n == 3:
            new = [[t[0][2], t[1][2], t[2][2]], [t[0][1], t[1][1], t[2][1]], [t[0][0], t[1][0], t[2][0]]]

    elif len(t) == 4:
        if n == 0:
            new = t
        elif n == 1:
            new = [[t[3][0], t[2][0], t[1][0], t[0][0]], [t[3][1], t[2][1], t[1][1], t[0][1]], [t[3][2], t[2][2], t[1][2], t[0][2]], [t[3][3], t[2][3], t[1][3], t[0][3]]]
        elif n == 2:
            new = [[t[3][3], t[3][2], t[3][1], t[3][0]], [t[2][3], t[2][2], t[2][1], t[2][0]], [t[1][3], t[1][2], t[1][1], t[1][0]], [t[0][3], t[0][2], t[0][1], t[0][0]]]
        elif n == 3:
            new = [[t[0][3], t[1][3], t[2][3], t[3][3]], [t[0][2], t[1][2], t[2][2], t[3][2]], [t[0][1], t[1][1], t[2][1], t[3][1]], [t[0][0], t[1][0], t[2][0], t[3][0]]]

    return new

def printBoard(board):
    sys.stdout.write('\x1b[1;1H.:====================:.\x1b[1B\x1b[40D')
    for line in board:
        sys.stdout.write('||')
        for char in line:
            if char == 'i':
                sys.stdout.write('\x1b[36m[]')
            elif char == 'j':
                sys.stdout.write('\x1b[34m[]')
            elif char == 'l':
                sys.stdout.write('\x1b[33m[]')
            elif char == 'o':
                sys.stdout.write('\x1b[38;5;226m[]')
            elif char == 'z':
                sys.stdout.write('\x1b[31m[]')
            elif char == 't':
                sys.stdout.write('\x1b[35m[]')
            elif char == 's':
                sys.stdout.write('\x1b[32m[]')
            elif char == '=':
                sys.stdout.write('\x1b[37m==')
            else:
                sys.stdout.write('\x1b[0m  ')
        sys.stdout.write('\x1b[0m||\x1b[1B\x1b[40D')
    sys.stdout.write('\':====================:\'\x1b[1B\x1b[40D')

def printNext(n, h):
    sys.stdout.write('\x1b[1;27H.:========:.')
    for x in range(4):
        sys.stdout.write('\x1b[12D\x1b[1B||        ||')
    sys.stdout.write('\x1b[12D\x1b[1B\':==Next==:\'')

    if n != -1:
        if len(n) == 3:
            sys.stdout.write('\x1b[3;30H')
        else:
            sys.stdout.write('\x1b[2;29H')

        for line in n:
            for char in line:
                if char == 'i':
                    sys.stdout.write('\x1b[36m[]')
                elif char == 'j':
                    sys.stdout.write('\x1b[34m[]')
                elif char == 'l':
                    sys.stdout.write('\x1b[33m[]')
                elif char == 'o':
                    sys.stdout.write('\x1b[38;5;226m[]')
                elif char == 'z':
                    sys.stdout.write('\x1b[31m[]')
                elif char == 't':
                    sys.stdout.write('\x1b[35m[]')
                elif char == 's':
                    sys.stdout.write('\x1b[32m[]')
                else:
                    sys.stdout.write('\x1b[0m  ')
            sys.stdout.write(f'\x1b[{len(n)*2}D\x1b[1B')

    sys.stdout.write('\x1b[8;27H.:========:.')
    for x in range(4):
        sys.stdout.write('\x1b[12D\x1b[1B||        ||')
    sys.stdout.write('\x1b[12D\x1b[1B\':==Hold==:\'')

    if h != -1:
        if len(h) == 3:
            sys.stdout.write('\x1b[10;30H')
        else:
            sys.stdout.write('\x1b[9;29H')

        for line in h:
            for char in line:
                if char == 'i':
                    sys.stdout.write('\x1b[36m[]')
                elif char == 'j':
                    sys.stdout.write('\x1b[34m[]')
                elif char == 'l':
                    sys.stdout.write('\x1b[38;5;208m[]')
                elif char == 'o':
                    sys.stdout.write('\x1b[38;5;226m[]')
                elif char == 'z':
                    sys.stdout.write('\x1b[31m[]')
                elif char == 't':
                    sys.stdout.write('\x1b[35m[]')
                elif char == 's':
                    sys.stdout.write('\x1b[32m[]')
                else:
                    sys.stdout.write('\x1b[0m  ')
            sys.stdout.write(f'\x1b[{len(h)*2}D\x1b[1B')

def gameOver():
    frame = 0
    while True:
        sys.stdout.write('\x1b[2J\x1b[0;0H')

        c = ''
        sys.stdin.flush()
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = ord(sys.stdin.read(1))
            if c == 27:
                _ = sys.stdin.read(1)
                dir = sys.stdin.read(1)
                if dir == 'A': # up
                    pass
                if dir == 'B': # down
                    pass
                if dir == 'D': # left
                    pass
                if dir == 'C': # right
                    pass

            if c in [10, 13]:
                break

        sys.stdout.write('\x1b[1;1H.:====================:.\x1b[1B\x1b[40D')
        for y in range(20):
            sys.stdout.write('||                    ||\x1b[1B\x1b[40D')
        sys.stdout.write('\':====================:\'\x1b[1B\x1b[40D')

        printNext(-1, -1)

        sys.stdout.write('\x1b[3;8;HGame Over!\x1b[2B\x1b[10DPress enter\x1b[1B\x1b[11Dto continue')

        sys.stdout.write('\x1b[1;1H')
        sys.stdout.flush()
        frame += 1
        sleep(1/240)


def controls():
    global controlScheme

    frame = 0
    while True:
        sys.stdout.write('\x1b[2J\x1b[0;0H')

        selection = 0

        c = ''
        sys.stdin.flush()
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = ord(sys.stdin.read(1))
            if c == 27:
                _ = sys.stdin.read(1)
                dir = sys.stdin.read(1)
                if dir == 'A': # up
                    pass
                if dir == 'B': # down
                    pass
                if dir == 'D': # left
                    controlScheme = 'qwerty'
                if dir == 'C': # right
                    controlScheme = 'colemak'

            if c in [10, 13]:
                break

        sys.stdout.write('\x1b[2;3;H\x1b[0m\x1b[37m')
        if controlScheme == 'colemak':
            sys.stdout.write('[qwerty] \x1b[30m\x1b[47m[colemak]')
        else:
            sys.stdout.write('\x1b[30m\x1b[47m[qwerty]\x1b[0m [colemak]')
        sys.stdout.write('\x1b[1;1;H\x1b[0m')

        sys.stdout.write('\x1b[4;3;H')
        if controlScheme == 'colemak':
            sys.stdout.write('  w   p    ^  \x1b[1B\x1b[14D')
            sys.stdout.write('a   s    <   >\x1b[1B\x1b[14D')
            sys.stdout.write('  r        v  \x1b[1B\x1b[14D')
            sys.stdout.write('z c   m')
        else:
            sys.stdout.write('  w   r    ^  \x1b[1B\x1b[14D')
            sys.stdout.write('a   d    <   >\x1b[1B\x1b[14D')
            sys.stdout.write('  s        v  \x1b[1B\x1b[14D')
            sys.stdout.write('z c   m')

        sys.stdout.write('\x1b[2B\x1b[7DPress enter to continue')

        sys.stdout.write('\x1b[1;1H')
        sys.stdout.flush()
        frame += 1
        sleep(1/240)

def menu():
    tty.setcbreak(sys.stdin.fileno())

    selection = 0

    frame = 0
    while True:
        sys.stdout.write('\x1b[2J\x1b[0;0H')

        c = ''
        sys.stdin.flush()
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = ord(sys.stdin.read(1))
            if c == 27:
                _ = sys.stdin.read(1)
                dir = sys.stdin.read(1)
                if dir == 'A': # up
                    selection -= 1
                    if selection < 0:
                        selection = 3
                if dir == 'B': # down
                    selection += 1
                    if selection > 3:
                        selection = 0
                if dir == 'D': # left
                    pass
                if dir == 'C': # right
                    pass

            if c in [10, 13]:
                if selection == 0:
                    return 'play'
                elif selection == 2:
                    controls()
                elif selection == 3:
                    return 'exit'

        sys.stdout.write('\x1b[2;3H')
        sys.stdout.write('\x1b[31m████████\x1b[38;5;240m╗\x1b[38;5;208m███████\x1b[38;5;240m╗\x1b[38;5;226m████████\x1b[38;5;240m╗\x1b[32m██████\x1b[38;5;240m╗\x1b[36m ██\x1b[38;5;240m╗\x1b[35m███████\x1b[38;5;240m╗\x1b[1B\x1b[45D')
        sys.stdout.write('\x1b[38;5;240m╚══\x1b[31m██\x1b[38;5;240m╔══╝\x1b[38;5;208m██\x1b[38;5;240m╔════╝╚══\x1b[38;5;226m██\x1b[38;5;240m╔══╝\x1b[32m██\x1b[38;5;240m╔══\x1b[32m██\x1b[38;5;240m╗\x1b[36m██\x1b[38;5;240m║\x1b[35m██\x1b[38;5;240m╔════╝\x1b[1B\x1b[45D')
        sys.stdout.write('   \x1b[31m██\x1b[38;5;240m║   \x1b[38;5;208m█████\x1b[38;5;240m╗     \x1b[38;5;226m██\x1b[38;5;240m║   \x1b[32m██████\x1b[38;5;240m╔╝\x1b[36m██\x1b[38;5;240m║\x1b[35m███████\x1b[38;5;240m╗\x1b[1B\x1b[45D')
        sys.stdout.write('   \x1b[31m██\x1b[38;5;240m║   \x1b[38;5;208m██\x1b[38;5;240m╔══╝     \x1b[38;5;226m██\x1b[38;5;240m║   \x1b[32m██\x1b[38;5;240m╔══\x1b[32m██\x1b[38;5;240m╗\x1b[36m██\x1b[38;5;240m║╚════\x1b[35m██\x1b[38;5;240m║\x1b[1B\x1b[45D')
        sys.stdout.write('   \x1b[31m██\x1b[38;5;240m║   \x1b[38;5;208m███████\x1b[38;5;240m╗   \x1b[38;5;226m██\x1b[38;5;240m║   \x1b[32m██\x1b[38;5;240m║  \x1b[32m██\x1b[38;5;240m║\x1b[36m██\x1b[38;5;240m║\x1b[35m███████\x1b[38;5;240m║\x1b[1B\x1b[45D')
        sys.stdout.write('\x1b[38;5;240m   ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝\x1b[1B\x1b[45D\x1b[0m')

        sys.stdout.write('\x1b[9;24;H')
        sys.stdout.write('   PLAY   \x1b[1B\x1b[10D')
        sys.stdout.write('HIGHSCORES\x1b[1B\x1b[10D')
        sys.stdout.write(' CONTROLS \x1b[1B\x1b[10D')
        sys.stdout.write('   EXIT   \x1b[1B\x1b[10D')
        sys.stdout.write(f'\x1b[{9+selection};23;H>\x1b[10C<')

        sys.stdout.write('\x1b[1;1H')
        sys.stdout.flush()
        frame += 1
        sleep(1/240)


def main():
    tty.setcbreak(sys.stdin.fileno())

    tetrominoes = [
        ['    ', 'iiii', '    ', '    '],
        ['j  ', 'jjj', '   '],
        ['  l', 'lll', '   '],
        ['    ', ' oo ', ' oo ', '    '],
        [' ss', 'ss ', '   '],
        [' t ', 'ttt', '   '],
        ['zz ', ' zz', '   ']
    ]

    board = [' '*10 for y in range(20)]

    bag = [0, 1, 2, 3, 4, 5, 6]
    shuffle(bag)
    p = bag[0]
    bag.remove(p)
    px, py = 3, 0
    pr = 0
    hold = -1

    score = 0

    frame = 0
    while True:
        sys.stdout.write('\x1b[2J\x1b[0;0H')

        c = 0
        sys.stdin.flush()
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = ord(sys.stdin.read(1))
            if c == 27:
                _ = sys.stdin.read(1)
                dir = sys.stdin.read(1)
                print('abc')
                rold = pr
                frame = 1
                if dir == 'A': # up
                    pr = (pr+2)%4
                if dir == 'D': # left
                    pr = (pr-1)%4
                if dir == 'C': # right
                    pr = (pr+1)%4

                fit = True
                if p == 0:
                    if (rold == 0 and pr == 1) or (rold == 3 and pr == 2):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-2, py)):
                            px -= 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py)):
                            px += 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-2, py+1)):
                            px -= 2
                            py += 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py-2)):
                            px += 1
                            py -= 2
                        else:
                            fit = False
                    if (rold == 1 and pr == 0) or (rold == 2 and pr == 3):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+2, py)):
                            px += 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py)):
                            px -= 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+2, py-1)):
                            px += 2
                            py -= 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py+2)):
                            px -= 1
                            py += 2
                        else:
                            fit = False
                    if (rold == 1 and pr == 2) or (rold == 0 and pr == 3):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py)):
                            px -= 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+2, py)):
                            px += 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py-2)):
                            px -= 1
                            py -= 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+2, py+1)):
                            px += 2
                            py += 1
                        else:
                            fit = False
                    if (rold == 2 and pr == 1) or (rold == 3 and pr == 0):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py)):
                            px += 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-2, py)):
                            px -= 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py+2)):
                            px += 1
                            py += 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-2, py-1)):
                            px -= 2
                            py -= 1
                        else:
                            fit = False
                elif p == 3:
                    pass
                else:
                    if (rold == 0 and pr == 1) or (rold == 2 and pr == 1):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py)):
                            px -= 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py-1)):
                            px -= 1
                            py -= 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py+2)):
                            py += 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py+2)):
                            px -= 1
                            py += 2
                        else:
                            fit = False
                    if (rold == 1 and pr == 0) or (rold == 1 and pr == 2):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py)):
                            px += 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py+1)):
                            px += 1
                            py += 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py-2)):
                            py -= 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py-2)):
                            px += 1
                            py -= 2
                        else:
                            fit = False
                    if (rold == 2 and pr == 3) or (rold == 0 and pr == 3):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py)):
                            px += 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py-1)):
                            px += 1
                            py -= 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py+2)):
                            py += 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px+1, py+2)):
                            px += 1
                            py += 2
                        else:
                            fit = False
                    if (rold == 3 and pr == 2) or (rold == 3 and pr == 0):
                        if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                            pass
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py)):
                            px -= 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py+1)):
                            px -= 1
                            py += 1
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py-2)):
                            py -= 2
                        elif doesPieceFit(rotate(tetrominoes[p], pr), board, (px-1, py-2)):
                            px -= 1
                            py -= 2
                        else:
                            fit = False

                if fit == False:
                    if dir == 'D': # left
                        pr = (pr+1)%4
                    if dir == 'C': # right
                        pr = (pr-1)%4

            if c == 99: # c
                controls()

            if c == 109: # m
                m = menu()
                if m == 'exit':
                    return 'exit'

            if c == 119: # w
                if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py + 1)):
                    py += 1
                else:
                    frame = 1
                    # placeTetromino(rotate(tetrominoes[p], pr), board, (px, py))
                    # p = bag[0]
                    # bag.remove(p)
                    # if len(bag) == 0:
                    #     bag = [0, 1, 2, 3, 4, 5, 6]
                    #     shuffle(bag)
                    # score += 10

                    # px, py = 3, 0
                    # pr = 0

            if c == 97: # a
                fit = True
                for y in range(len(tetrominoes[p])):
                    for x, c in enumerate(rotate(tetrominoes[p], pr)[y]):
                        if c != ' ':
                            if not px+x > 0:
                                fit = False

                if not doesPieceFit(rotate(tetrominoes[p], pr), board, (px - 1, py)):
                    fit = False

                if fit:
                    px -= 1

            if (c == 114 and controlScheme == 'colemak') or (c == 115 and controlScheme == 'qwerty'): # r
                while True:
                    if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py + 1)):
                        py += 1
                    else:
                        placeTetromino(rotate(tetrominoes[p], pr), board, (px, py))
                        p = bag[0]
                        bag.remove(p)
                        if len(bag) == 0:
                            bag = [0, 1, 2, 3, 4, 5, 6]
                            shuffle(bag)
                        score += 10

                        px, py = 3, 0
                        pr = 0

                        break

            if (c == 115 and controlScheme == 'colemak') or (c == 100 and controlScheme == 'qwerty'): # s
                fit = True
                for y in range(len(tetrominoes[p])):
                    for x, c in enumerate(rotate(tetrominoes[p], pr)[y]):
                        if c != ' ':
                            if not px+x < 9:
                                fit = False

                if not doesPieceFit(rotate(tetrominoes[p], pr), board, (px + 1, py)):
                    fit = False

                if fit:
                    px += 1

            if c == 122: # z
                if hold != -1:
                    t = hold
                    hold = p
                    p = t
                else:
                    hold = p
                    p = bag[0]
                    bag.remove(p)
                    if len(bag) == 0:
                        bag = [0, 1, 2, 3, 4, 5, 6]
                        shuffle(bag)
                px, py = 3, 0
                pr = 0
                if not doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                    break # game over

        if (c == 112 and controlScheme == 'colemak') or (c == 114 and controlScheme == 'qwerty'): # p
            board = [' '*10 for y in range(20)]

            bag = [0, 1, 2, 3, 4, 5, 6]
            shuffle(bag)
            p = bag[0]
            bag.remove(p)
            px, py = 3, 0
            pr = 0
            hold = -1

            score = 0

        if not frame%10:
            board = clearLines(board)
        board = checkLines(board)

        printBoard(board)
        if hold != -1:
            printNext(tetrominoes[bag[0]], tetrominoes[hold])
        else:
            printNext(tetrominoes[bag[0]], -1)

        drawShadow(rotate(tetrominoes[p], pr), board, (px, py))
        drawTetromino(rotate(tetrominoes[p], pr), (px, py))

        if not frame%120:
            score += 0.1

            if doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py + 1)):
                py += 1
            else:
                placeTetromino(rotate(tetrominoes[p], pr), board, (px, py))
                p = bag[0]
                bag.remove(p)
                if len(bag) == 0:
                    bag = [0, 1, 2, 3, 4, 5, 6]
                    shuffle(bag)
                score += 10
                px, py = 3, 0
                pr = 0
                if not doesPieceFit(rotate(tetrominoes[p], pr), board, (px, py)):
                    break # game over

        sys.stdout.write('\x1b[1;1H')
        sys.stdout.flush()
        frame += 1
        sleep(1/240)

if __name__ == '__main__':
    try:
        oldTerminal = termios.tcgetattr(sys.stdin)
        sys.stdout.write('\x1b[?25l')

        global controlScheme
        controlScheme = 'colemak'

        m = menu()

        if m == 'play':
            while True:
                m = main()
                if m == 'exit':
                    break
                gameOver()

    finally:
        sys.stdout.write('\x1b[0m\x1b[0;0H\x1b[2J\x1b[?25h')
        sys.stdout.flush()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldTerminal)
