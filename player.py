import math
import sys
from random import choices

class Player:
    def __init__(self,strategy):
        # isCoop is initial strategy. True if it's a cooperator.
        # prof is the initial profit
        self.isCoop = strategy #Should be true or fause
        self.newCoop = self.isCoop
        self.prof = 5.0


    def allocate(self):
        #allocate its resource
        self.isCoop = self.newCoop
        if self.isCoop:
            self.prof = self.prof - 1
            return 1.0
        return 0.0

    def gain_profit(self,gain):
        self.prof = self.prof + gain

    def reset(self):
        self.prof = 5.0
        
    def change_strategy(self, neighbour,K): #K is uncertainty
        prob = 0.0
        if self.isCoop == neighbour.isCoop:
            return False

        if (self.prof - neighbour.prof)/K > 10:
            return False
        elif (self.prof - neighbour.prof)/K < -5:
            self.newCoop = neighbour.isCoop
            return True

        else:
            prob = 1.0/(1.0 + math.exp((self.prof - neighbour.prof) /K))

        if choices([True,False],[prob,1.0-prob])[0]:
            self.newCoop = neighbour.isCoop
#            print(prob,neighbour.isCoop,self.isCoop)
            return True
        return False
