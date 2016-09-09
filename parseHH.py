#!/usr/bin/python
from session import session
import sys
p=session(sys.argv[1])
p.parseHands()
for hand in p.hands:
    if hand.id >0:
        print hand.id
        for i in range(1,hand.actionCounter+1):
            for player in hand.players:
                for action in player.actions:
                    if action.order == i:
                        if player.isMe:
                            print action.order,action.street,player.position+' [Me]',action.action,action.amount
                        else:
                            print action.order,action.street,player.position,action.action,action.amount
