#!/usr/bin/python
import sys,os,glob
class hand:
    def __init__(self,id):
        self.id=id
        self.myPos=''
        self.myHoleCards = ['','']
        self.text = ''
        self.time = ''
        self.sbHoleCards = ['','']
        self.bbHoleCards = ['','']
        self.utgHoleCards = ['','']
        self.utg1HoleCards = ['','']
        self.utg2HoleCards = ['','']
        self.btnHoleCards = ['','']
        
class parser:
    def __init__(self,dir):
        self.fileList = glob.glob(dir.rstrip('/')+'/*.txt')
        self.hands=[]
    def parseHands(self):
        for fileName in self.fileList:
            for line in open(fileName):
                if 'Ignition Hand #' in line:
                    self.hands.append(hand(0))
                    self.hands[-1].id=line.split()[2][1:]
                    self.hands[-1].time = line.rstrip()[-8:]
                    self.hands[-1].date = line[-21:-10]
                if '[ME]' in line and 'Card dealt to a spot' in line:
                    self.hands[-1].myHoleCards = self.getHoleCards(line)
                if '[ME]' in line and 'Seat' in line and 'sit out' not in line:
                    self.hands[-1].myPos = line[line.index('Seat ')+8:line.index('[ME]')]
                if 'Card dealt to a spot' in line:
                    if 'Small Blind' in line:
                        self.hands[-1].sbHoleCards = self.getHoleCards(line)
                    elif 'Big Blind' in line:
                        self.hands[-1].bbHoleCards = self.getHoleCards(line)
                    elif 'UTG ' in line:
                        self.hands[-1].utgHoleCards = self.getHoleCards(line)
                    elif 'UTG+1' in line:
                        self.hands[-1].utg1HoleCards = self.getHoleCards(line)
                    elif 'UTG+2' in line:
                        self.hands[-1].utg2HoleCards = self.getHoleCards(line)
                    elif 'Dealer' in line:
                        self.hands[-1].btnHoleCards = self.getHoleCards(line)
                        
            self.hands[-1].text+=line
    def getHoleCards(sefl,aline):
        return aline[aline.index('Card dealt to a spot')+22:-4].split()

p=parser(sys.argv[1])
p.parseHands()
for hand in p.hands:
    print(hand.id,hand.date,hand.time,hand.myPos,hand.myHoleCards,hand.sbHoleCards,hand.bbHoleCards,hand.utgHoleCards,hand.utg1HoleCards,hand.utg2HoleCards,hand.btnHoleCards)
#p.parseHands()
