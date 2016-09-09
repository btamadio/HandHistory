#!/usr/bin/python
from session import session
import sys
p=session(sys.argv[1])
p.parseHands()
rakePaidByMe = 0.0
amountWonByMe = 0.0
numHandWon = 0
for hand in p.hands:
    totalWon = 0.0
    totalRake = 0.0

    print hand.id
    for player in hand.players:
        totalWon += player.amountWon
        totalWon += player.rakePaid
        totalRake+=player.rakePaid
        if player.isMe:
            rakePaidByMe += player.rakePaid*.25
            amountWonByMe += player.amountWon*.25
            if player.amountWon > 0:
                numHandWon +=1
        print player.position,'\t',player.amountWon,'\t',player.rakePaid
    print '\t',round(totalWon,2),'\t',totalRake
print 'rake paid by  me: $',rakePaidByMe
print 'amount won by me: $',amountWonByMe
print 'hands I won:',numHandWon
print 'total hands:',len(p.hands)
                    #    print 'total winnings:',round(totalWon,2),'rake paid: ',hand.preRakePot-hand.postRakePot,'number of winners = ',hand.nWinners
#

#        for i in range(1,hand.actionCounter+1):
#            for player in hand.players:
#                print player.amountWon
##                 for action in player.actions:
#                     if action.order == i:
#                         if player.isMe:
#                             pass
# #                            print action.order,action.street,player.position+' [Me]',action.action,action.amount,player.amountWon
#                         else:
#                             pass
# #
#                            print action.order,action.street,player.position,action.action,action.amount
