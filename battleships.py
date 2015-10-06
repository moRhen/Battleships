#!/usr/bin/env python3

import re
import os
class Battleships(object):

    def __init__(self):
        pass

    def boardlegend(self):
        pass

#2 validators#some equal patterns#need optimization#############################
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
                        for item in flagpos:#position arount x+1, y+1 without pos of placing ship itself
                            if item in aroundpos:
                                aroundpos.remove(item)
                        for item in aroundpos:#check if new flag is touching another ship
                            if playerboard[item[0]][item[1]] == '#':
                                istouching += 1
                        if isconnected >= 1 and istouching == 0:#if parts connected and dont touch another ship return data
                            break
                        elif isconnected >= 1 and istouching > 0:
                            self.clear()
                            self.printboard(playerboard)
                            print('nowy segment nie może dotykać innego statku')
                            continue
                        else:
                            self.clear()
                            self.printboard(playerboard)
                            print('nowy segment nie przylega do istniejącego już statku')
                            continue
                    if '#' not in around:#for 1flag or starting flag, if not touchng another ship return data
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

    def shoot(self, shipboard, hitboard, hits, message):
        pattern = '[0-9] [0-9]$'
        while True:
            data = input(message)
            if re.match(pattern, data):#digit, space, digit
                x, y = self.position(data)
                if hitboard[x+1][y+1] == '*':
                    if shipboard[x+1][y+1] == '#':
                        hitboard[x+1][y+1] = '#'
                        hits += 1
                        self.clear()
                        self.printboard(hitboard)
                        print('Trafiony')
                        input('Naciśnij ENTER, aby kontynuować')

                    elif shipboard[x+1][y+1] == '*':
                        hitboard[x+1][y+1] = '-'
                        self.clear()
                        self.printboard(hitboard)
                        print('Pudło')
                        break
                else:
                    self.clear()
                    self.printboard(hitboard)
                    print('Ta pozycja została już ostrzelana')
                    continue
            else:
                self.clear()
                self.printboard(hitboard)
                print('podałeś niewłaściwą pozycję, spróbuj ponownie')
                continue
        return hitboard, hits
################################################################################

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
        flags, ship = [4, 3, 2, 1], 1
        while flags[3] > 0:#until whole ship is placed
            flagpos = []
            self.printboard(playerboard)
            pos = self.validator('podaj pozycję {} masztowca(np: \'3 4\' - 3 rząd i 4 kolumna)\npozostało Ci {} - {} masztowców :'.format(ship, flags[ship - 1], ship), playerboard)
            x, y = self.position(pos)
            if ship == 1:#for 1flag
                playerboard[x+1][y+1] = '#'
                flags[ship-1] -= 1
            elif ship == 2 or ship == 3 or ship == 4:#for more than 1 flag
                additionalflag = ship
                while additionalflag > 1:
                    playerboard[x+1][y+1] = '#'#for 2flags
                    flagpos.append([x+1,y+1])#tracking ship segments
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
        input('Gra w statki dla dwóch graczy\n Aby rozpocząć rozgrywkę naciśniej ENTER')
        player1, player2 = self.playershipplacment()
        player1hit = self.emptyboard()
        player2hit = self.emptyboard()
        hits1, hits2 = 0, 0
        while hits1 <= 20 or hits2 <= 20:#play until one of player hit 20 times   
            player1hit, hits1 = self.shoot(player2, player1hit, hits1, 'Proszę o oddanie strzału przez gracza 1 (np: \'3 4\' - 3 rząd i 4 kolumna\n)')
            player2hit, hits2 = self.shoot(player1, player2hit, hits2, 'Proszę o oddanie strzału przez gracza 2 (np: \'3 4\' - 3 rząd i 4 kolumna\n)')
        if hits1 == 20:
            print('Gratulacje, gracz 1 wygrywa')
        elif hits2 == 20:
            print('Gratulacje, gracz 2 wygrywa')


b = Battleships()
b.gamesystem()
