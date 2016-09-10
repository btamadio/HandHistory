#!/usr/bin/python
#Class to parse Bovada Hand histories
from hand import hand
from streetAction import streetAction
import sys
class session:
    def __init__(self,fileName):
        self.fileName = fileName
        self.hands=[]
        self.thisHand = hand()
    def parseHands(self):
        for line in open(self.fileName):
            if 'Ignition Hand #' in line:
#                print line.split('#')[1].split()[0]
                self.hands.append(hand(0))
                self.thisHand = self.hands[-1]
                #self.thisHand.id=int(line.split()[2][1:])
                self.thisHand.id=int(line.split('#')[1].split()[0])
#                print 'parsing hand #',self.thisHand.id
                self.thisHand.time = line.rstrip()[-8:]
                self.thisHand.date = line[-21:-11]
                self.thisHand.BBsize = float(self.fileName.split('$')[2].split('-')[0])
                self.thisHand.SBsize = float(self.fileName.split('$')[1].split('-')[0])

            self.thisHand.text+=line
            #starting stack, players positions, and identify me
            if 'in chips' in line:
                playerIdx = self.getPlayerIdx(line)
                startingStack = float(line[line.index('$')+1:line.index('in chips')]) / self.thisHand.BBsize
                self.thisHand.players[playerIdx].startingStack = startingStack
                if '[ME]' in line:
                    self.thisHand.players[playerIdx].isMe = True
                self.thisHand.players[playerIdx].position = self.getPosition(line)
            #identify hole cards
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
            if '*** FLOP ***' in line or '*** TURN ***' in line or '*** RIVER ***' in line:
                self.thisHand.streetCounter+=1

            #parse actions
            if self.isActionLine(line):
                self.thisHand.actionCounter+=1

                streets = ['P','F','T','R']
                newAction = streetAction(streets[self.thisHand.streetCounter],self.thisHand.actionCounter,self.getAction(line),self.getAmount(line))
                actionPlayer = self.getPlayer(line)
                actionPlayer.actions.append(newAction)
                actionPlayer.amountWon-=self.getAmount(line)
                #print newAction.order,newAction.street,actionPlayer.position,newAction.action,newAction.amount,actionPlayer.amountWon
            if 'Return uncalled' in line:
                winner = self.getPlayer(line)
                winner.amountWon+=self.getAmount(line)
            if 'Hand result' in line:
                self.thisHand.postRakePot+=self.getAmount(line)
                winner = self.getPlayer(line)
                winner.amountWon+=self.getAmount(line)
                self.thisHand.nWinners+=1
            if 'Total Pot' in line:
                self.thisHand.preRakePot=self.getAmount(line)
                if self.thisHand.getBB():
                    self.thisHand.getBB().amountWon-=1
                if self.thisHand.getSB():
                    self.thisHand.getSB().amountWon-=self.thisHand.SBsize/self.thisHand.BBsize
                for player in self.thisHand.players:
                    if player.amountWon > 0:
                        player.rakePaid+=(self.thisHand.preRakePot-self.thisHand.postRakePot)/self.thisHand.nWinners
    def getHoleCards(self,line):
        return line[line.index('Card dealt to a spot')+22:-4].split()
    def getPlayerIdx(self,line):
        if 'Seat' in line:
            return int(line[line.index('Seat')+5])-1
        return -1
    def getPlayer(self,line):
        if 'Dealer' in line:
            return self.thisHand.getBTN()
        elif 'UTG+2' in line:
            return self.thisHand.getUTG2()
        elif 'UTG+1' in line:
            return self.thisHand.getUTG1()
        elif 'UTG' in line:
            return self.thisHand.getUTG()
        elif 'Small Blind' in line:
            return self.thisHand.getSB()
        elif 'Big Blind' in line:
            return self.thisHand.getBB()
        return
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
        return
    def isActionLine(self,line):
        if self.getAction(line) != '':
            return True
        return False
    def getAction(self,line):
        if 'All-in' in line:
            return 'A'
        if 'Checks' in line:
            return 'X'
        if 'Posts' in line:
            return 'P'
        if 'Calls' in line:
            return 'C'
        if 'Bets' in line:
            return 'B'
        if 'Raises' in line:
            return 'R'
        if 'Folds' in line:
            return 'F'
        return ''
    def getAmount(self,line):
        for word in line.split():
            if '$' in word:
                return float(word.split('$')[1].strip('()'))/self.thisHand.BBsize
        return 0.0
