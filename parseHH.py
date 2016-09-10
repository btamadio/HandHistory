#!/usr/bin/python
from session import session
import sys,glob,pprint
fileList = glob.glob(sys.argv[1]+'/*RING*.txt')
sessions = []
dateDict = {}
for fileName in fileList:
    if '$0.10-$0.25' in fileName:
        p = session(fileName)
        print 'Parsing hand history file',fileName
        p.parseHands()
        sessions.append(p)

rakePaidByMe = 0.0
amountWonByMe = 0.0
numHands = 0
numAces = 0
numKings = 0
numQueens = 0

amountWonWithAces = 0.0
amountWonWithKings = 0.0
amountWonWithQueens = 0.0
for session in sessions:
    date = session.hands[0].date
    if date not in dateDict:
        dateDict[date]=len(session.hands)
    else:
        dateDict[date]+=len(session.hands)
    for hand in session.hands:
        numHands+=1
        for player in hand.players:
            if player.isMe:
                rakePaidByMe+=player.rakePaid*hand.BBsize
                amountWonByMe+=player.amountWon*hand.BBsize
                if player.holeCards[0].startswith('A') and player.holeCards[1].startswith('A'):
                    numAces+=1
                    amountWonWithAces += player.amountWon*hand.BBsize
                if player.holeCards[0].startswith('K') and player.holeCards[1].startswith('K'):
                    numKings+=1
                    amountWonWithKings += player.amountWon*hand.BBsize
                    if player.amountWon < 0:
                        print 'lost $',round(-1*player.amountWon*hand.BBsize,2)
                        print hand.text
                if player.holeCards[0].startswith('Q') and player.holeCards[1].startswith('Q'):
                    numQueens+=1
                    amountWonWithQueens += player.amountWon*hand.BBsize                    
                
print 'number of hands = ',numHands
print 'rake paid by me =$',round(rakePaidByMe,2)
print 'amount won by me =$',round(amountWonByMe,2)
print 'rake paid / 100 hands = $',round(rakePaidByMe/(numHands/100.),2)
print 'amount won / 100 hands = $',round(amountWonByMe/(numHands/100.),2)

print 'times dealt aces = ',numAces
print 'times dealt kings = ',numKings
print 'times dealt queens = ',numQueens

print 'fraction dealt aces = ',round(numAces/numHands,4)
print 'fraction dealt kings = ',round(numKings/numHands,4)
print 'fraction dealt queens = ',round(numQueens/numHands,4)

print 'amount won with Aces = $',round(amountWonWithAces,2)
print 'amount won with Kings = $',round(amountWonWithKings,2)
print 'amount won with Queens = $',round(amountWonWithQueens,2)


print 'average = $',round(amountWonWithAces/numAces,2)
print 'average = $',round(amountWonWithKings/numKings,2)
print 'average = $',round(amountWonWithQueens/numQueens,2)



pprint.pprint(dateDict)
sys.exit(0)
