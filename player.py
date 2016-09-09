#!/usr/bin/python
from streetAction import streetAction
class player:
    def __init__(self,num):
        self.num = num
        self.isMe = False
        self.position = ''
        self.holeCards = ['','']
        self.startingStack = 0.0
        self.actions=[]
        self.amountWon=0.0
        self.rakePaid=0.0
