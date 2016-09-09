#!/usr/bin/python
from player import player
class hand:
    def __init__(self,id=0):
        self.id=id
        self.text = ''
        self.time = ''
        self.date = ''
        self.SBsize = 0
        self.BBsize = 0
        self.players = [player(1),player(2),player(3),player(4),player(5),player(6)]
        self.actionCounter = 0
        self.streetCounter = 0
        self.preRakePot = 0.0
        self.postRakePot = 0.0
        self.nWinners = 0
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
