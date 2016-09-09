#!/usr/bin/python
#Class to parse Bovada Hand histories
import sys,os,glob

class hand:
    def __init__(self,id=0):
        self.id=id
        self.text = ''
        self.time = ''
        self.date = ''
        self.BBsize = 0
        self.players = [player(1),player(2),player(3),player(4),player(5),player(6)]
    def getMe(self):
        for player in self.players:
            if player.isMe:
                return player
        print 'No player is marked as me.'
        sys.exit(1)
    def getBB(self):
        for player in self.players:
            if player.position == 'BB':
                return player
    def getSB(self):
        for player in self.players:
            if player.position == 'SB':
                return player
    def getBTN(self):
        for player in self.players:
            if player.position == 'BTN':
                return player            
    def getUTG(self):
        for player in self.players:
            if player.position == 'UTG':
                return player
    def getUTG1(self):
        for player in self.players:
            if player.position == 'UTG1':
                return player                
    def getUTG2(self):
        for player in self.players:
            if player.position == 'UTG2':
                return player
    def getNPlayers(self):
        nPlayers = 0
        for player in self.players:
            if player.holeCards[0] != '':
                nPlayers+=1
        return nPlayers
class player:
    def __init__(self,num):
        self.num = num
        self.isMe = False
        self.position = ''
        self.holeCards = ['','']
        self.startingStack = 0
        
class session:
    def __init__(self,fileName):
        self.fileName = fileName#glob.glob(dir.rstrip('/')+'/*.txt')
        self.hands=[]
        self.thisHand = hand()
    def parseHands(self):
        for line in open(self.fileName):
            if 'Ignition Hand #' in line:
                self.hands.append(hand(0))
                self.thisHand = self.hands[-1]
                self.thisHand.id=line.split()[2][1:]
                self.thisHand.time = line.rstrip()[-8:]
                self.thisHand.date = line[-21:-11]
                self.thisHand.BBsize = float(self.fileName.split('$')[2].split('-')[0])
            #starting stack, position, and identify me
            if 'in chips' in line:
                playerIdx = self.getPlayerIdx(line)
                startingStack = float(line[line.index('$')+1:line.index('in chips')]) / self.thisHand.BBsize
                self.thisHand.players[playerIdx].startingStack = startingStack
                if '[ME]' in line:
                    self.thisHand.players[playerIdx].isMe = True
                self.thisHand.players[playerIdx].position = self.getPosition(line)
            if 'Card dealt to a spot' in line:
                if 'Small Blind' in line and self.thisHand.getSB():
                    self.thisHand.getSB().holeCards = self.getHoleCards(line)
                elif 'Big Blind' in line and self.thisHand.getBB():
                    self.thisHand.getBB().holeCards = self.getHoleCards(line)
                elif 'UTG+2' in line and self.thisHand.getUTG2():
                    self.thisHand.getUTG2().holeCards = self.getHoleCards(line)                    
                elif 'UTG+1' in line and self.thisHand.getUTG1():
                    self.thisHand.getUTG1().holeCards = self.getHoleCards(line)                                                                
                elif 'UTG ' in line and self.thisHand.getUTG():
                    self.thisHand.getUTG().holeCards = self.getHoleCards(line)                                                                
                elif 'Dealer' in line and self.thisHand.getBTN():
                    self.thisHand.getBTN().holeCards = self.getHoleCards(line)                                                                
            self.hands[-1].text+=line
    def getHoleCards(self,line):
        return line[line.index('Card dealt to a spot')+22:-4].split()
    def getPlayerIdx(self,line):
        return int(line[line.index('Seat')+5])-1
    def getPosition(self,line):
        if 'Dealer' in line:
            return 'BTN'
        elif 'UTG+2' in line:
            return 'UTG2'
        elif 'UTG+1' in line:
            return 'UTG1'
        elif 'UTG' in line:
            return 'UTG'
        elif 'Small Blind' in line:
            return 'SB'
        elif 'Big Blind' in line:
            return 'BB'

p=session(sys.argv[1])
p.parseHands()
for hand in p.hands:
    print hand.getNPlayers(),' players'
        #    print hand.id,hand.date,hand.time,hand.BBsize,hand.getMe().position,hand.getMe().startingStack,hand.getMe().holeCards

