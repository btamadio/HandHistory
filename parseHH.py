#!/usr/bin/python
from session import session
import sys
p=session(sys.argv[1])
p.parseHands()
for hand in p.hands:
    #print hand.getNPlayers(),' players'
    print hand.id,hand.date,hand.time,hand.BBsize,hand.getMe().position,hand.getMe().startingStack,hand.getMe().holeCards
    print hand.text
