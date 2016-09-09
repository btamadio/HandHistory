#!/usr/bin/python
class streetAction:
    def __init__(self,street,order,action,amount):
        self.street = street#'P','F','T', or 'F'
        self.order = order   #order in which the action occurred
        self.action = action #'P','F','X','C','R','A','B'
        self.amount = amount  #amout added to pot on this particular action
