#!/usr/bin/env python3

import re
import os
class Battleships(object):

    def __init__(self):
        pass

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def errormessage(self, message, board):
        self.clear
        self.printboard(board)
        print(message)
        input('Naciśnij ENTER, aby kontynuować')

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
                            self.errormessage('Nowy segment nie może dotykać innego statku', playerboard)
                            continue
                        else:
                            self.errormessage('Nowy segment nie przylega do istniejącego już statku', playerboard)
                            continue
                    if '#' not in around:#for 1flag or starting flag, if not touchng another ship return data
                        break
                    else:
                        self.errormessage('Statek nie może stykać się z innym już istniejącym statkiem', playerboard)
                        continue
                else:
                    self.errormessage('Na podanej pozycji jest już statek', playerboard)
                    continue
            else:
                self.errormessage('Podałeś niewłaściwą pozycję, spróbuj ponownie', playerboard)
                continue
        return data

    def shoot(self, shipboard, hitboard, hits, message):
        pattern = '[0-9] [0-9]$'
        while True:
            if hits == 20:#if win break
                break
            self.printboard(hitboard)
            data = input(message)
            if re.match(pattern, data):#digit, space, digit
                x, y = self.position(data)
                if hitboard[x+1][y+1] == '*':
                    if shipboard[x+1][y+1] == '#':
                        hitboard[x+1][y+1] = '#'
                        hits += 1
                        self.errormessage('Trafiony', hitboard)

                    elif shipboard[x+1][y+1] == '*':
                        hitboard[x+1][y+1] = '-'
                        self.errormessage('Pudło', hitboard)
                        break
                else:
                    self.errormessage('Ta pozycja została już ostrzelana', hitboard)
                    continue
            else:
                self.errormessage('Podałeś niewłaściwą pozycję, spróbuj ponownie', hitboard)
                continue
        return hitboard, hits

    def shipplacment(self):
    #placment of ships in player board; 4x1flag 3x2flag 2x3flag 1x4flag
        playerboard = self.emptyboard()
        flags, ship = [4, 3, 2, 1], 1
        while flags[3] > 0:#until whole ship is placed
            flagpos = []
            self.printboard(playerboard)
            pos = self.validator('Podaj pozycję {} masztowca(np: \'3 4\' - 3 rząd i 4 kolumna)\nPozostało Ci {} - {} masztowców :'.format(ship, flags[ship - 1], ship), playerboard)
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
                    anotherflag = self.validator('Podaj kolejną pozycję {} masztowca :'.format(ship), playerboard, 42, flagpos)
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
        input('Gra w statki dla dwóch graczy\nAby rozpocząć rozgrywkę naciśniej ENTER')
        player1, player2 = self.playershipplacment()
        player1hit = self.emptyboard()
        player2hit = self.emptyboard()
        hits1, hits2 = 0, 0
        while hits1 != 20 and hits2 != 20:#play until one of player hit 20 times
            player1hit, hits1 = self.shoot(player2, player1hit, hits1, 'Proszę o oddanie strzału przez gracza1 (np: \'3 4\' - 3 rząd i 4 kolumna)\n')
            if hits1 == 20:#if player1 wins, break before player2 shoot
                break
            player2hit, hits2 = self.shoot(player1, player2hit, hits2, 'Proszę o oddanie strzału przez gracza2 (np: \'3 4\' - 3 rząd i 4 kolumna)\n')
        if hits1 == 20:#player1 win
            print('\nGratulacje, gracz 1 wygrywa, wszystkie statki zatopione :)')
        elif hits2 == 20:#player2 win
            print('\nGratulacje, gracz 2 wygrywa, wszystkie statki zatopione :)')
        print('Koniec rozgrywki')

if __name__ == "__main__":
    Battleships().gamesystem()
