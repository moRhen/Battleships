#!/usr/bin/env python3

import re
import os
class Battleships(object):

    def __init__(self):
        pass

    def boardlegend(self):
        pass

    def validator(self, message, playerboard):
    #check if data input matches "digit, space, digit", is on board, and new ship is not placed on existing one
        pattern = '[0-9] [0-9]$'
        trololo = 42
        while True:
            data = input(message)
            if re.match(pattern, data):
                x, y = self.position(data)

                if playerboard[x+1][y+1] == '*':
                    around = [playerboard[x][y], playerboard[x][y+1], playerboard[x][y+2], playerboard[x+1][y], playerboard[x+2][y], playerboard[x+2][y+2], playerboard[x+1][y+2], playerboard[x+2][y+1]]

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

    def validator2(self, data):
        pass

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

    def ptboardtest(self, board):
    #do kontroli
        print('\n' * 1)
        for n in board:
            print(' '.join(n))
        print('\n' * 1)


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
                    self.printboard(playerboard)
                    anotherflag = self.validator('podaj kolejną pozycję {} masztowca :'.format(ship), playerboard)
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
        self.clear
        input('kontrolka ENTER')
        self.ptboardtest(player1)
        self.ptboardtest(player2)


b = Battleships()

b.playershipplacment()

