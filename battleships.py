#!/usr/bin/env python3

import re
import os
class Battleships(object):

    def __init__(self):
        pass

    def boardlegend(self):
        pass

    def validator(self, message, playerboard, spam=None, flagpos=None):
    #check if data input matches "digit, space, digit", is on board, and new ship is not placed on existing one
        pattern = '[0-9] [0-9]$'
        while True:
            data = input(message)
            if re.match(pattern, data):#digit, space, digit
                x, y = self.position(data)
                around = [playerboard[x][y], playerboard[x][y+1], playerboard[x][y+2], playerboard[x+1][y], playerboard[x+2][y], playerboard[x+2][y+2], playerboard[x+1][y+2], playerboard[x+2][y+1]]#symbols around x+1, y+1
                if playerboard[x+1][y+1] == '*':#there is no ship already
                    if spam == 42:#placment ship have more than 1flag
                        isconnected = 0
                        istouching = 0
                        flagstick = [[x, y+1], [x+1, y], [x+2, y+1], [x+1, y+2]]#possible connection for multiply flag
                        aroundpos = [[x, y], [x, y+1], [x, y+2], [x+1, y], [x+2, y], [x+2, y+2], [x+1, y+2], [x+2, y+1]]#pos around x, y
                        for item in flagpos:#checking connection
                            if item in flagstick:
                                isconnected += 1
                        for item in flagpos:#position arount x+1, y+1 without pos of self ship
                            if item in aroundpos:
                                aroundpos.remove(item)
                        for item in aroundpos:#check if new flag is touching another ship
                            if playerboard[item[0]][item[1]] == '#':
                                istouching += 1
                        if isconnected >= 1 and istouching == 0:
                            input('spełaniam; if isconnected >= 1 and istouching == 0:')
                            break
                        elif isconnected >= 1 and istouching > 0:
                            input('spełniam; elif isconnected >= 1 and istouching > 0:')
                            self.clear()
                            self.printboard(playerboard)
                            print('nowy segment nie może dotykać innego statku')
                            continue
                        else:
                            self.clear()
                            self.printboard(playerboard)
                            print('nowy segment nie przylega do istniejącego już statku')
                            continue
                    if '#' not in around:
                        break
                    else:
                        self.clear()
                        self.printboard(playerboard)
                        print('statek nie może stykać się z innym już istniejącym statkiem')
                        continue
                else:
                    self.clear()
                    self.printboard(playerboard)
                    print('na podanej pozycji jest już statek')
                    continue
            else:
                self.clear()
                self.printboard(playerboard)
                print('podałeś niewłaściwą pozycję, spróbuj ponownie')
                continue
        return data

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def emptyboard(self):
    #make empty board with numerate sides
        board = []
        border = list('$' + ''.join([str(x) for x in range(10)]) + '$')
        board.append(border)
        for n in range(10):
            board.append(list(str(n) + ('*' * 10) + str(n)))
        board.append(border)
        return board

    def printboard(self, board):
        self.clear()
        for n in board:
            print(' '.join(n))
        print('\n' * 4)

    def position(self, pos):
    #return 2 numbers which is x and y on our board
        pos = list(pos)
        x, y = pos[0], pos[2]
        return int(x), int(y)

    def shipplacment(self):
    #placment of ships in player board; 4x1flag 3x2flag 2x3flag 1x4flag
        playerboard = self.emptyboard()
        flags = [4, 3, 2, 1]
        ship = 1
        while flags[3] > 0:

#START# staff for optimization
            flagpos = []
            self.printboard(playerboard)
            pos = self.validator('podaj pozycję {} masztowca(np: \'3 4\' - 3 rząd i 4 kolumna)\npozostało Ci {} - {} masztowców :'.format(ship, flags[ship - 1], ship), playerboard)
            x, y = self.position(pos)
            if ship == 1:
                playerboard[x+1][y+1] = '#'
                flags[ship-1] -= 1
            elif ship == 2 or ship == 3 or ship == 4:
                additionalflag = ship - 1
                while additionalflag > 0:
                    playerboard[x+1][y+1] = '#'
                    flagpos.append([x+1,y+1])
                    self.printboard(playerboard)
                    anotherflag = self.validator('podaj kolejną pozycję {} masztowca :'.format(ship), playerboard, 42, flagpos)
                    x, y = self.position(anotherflag)
                    playerboard[x+1][y+1] = '#'
                    additionalflag -= 1
                flags[ship-1] -= 1
            if flags[ship-1] == 0:
                ship += 1
        self.printboard(playerboard)
        input('Statki ustawione na planszy, naciśniej ENTER aby kontynuować')
        return playerboard
#END# end of mess

    def playershipplacment(self):
        self.clear()
        input('proszę o ustawienie statków przez gracza nr 1, naciśniej ENTER aby kontynuować')
        player1 = self.shipplacment()
        self.clear()
        input('proszę o ustawienie statków przez gracza nr 2, naciśniej ENTER aby kontynuować')
        player2 = self.shipplacment()
        self.clear()
        return player1, player2

    def gamesystem(self):
        self.clear()
        input('Gra w statki\n Aby rozpocząć rozgrywkę naciśniej ENTER')
        player1, player2 = self.playershipplacment()

b = Battleships()
b.playershipplacment()
