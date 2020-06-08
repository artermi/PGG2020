import math
import sys
from random import choices

class Player:
    def __init__(self,strategy):
        # isCoop is initial strategy. True if it's a cooperator.
        # prof is the initial profit
        self.isCoop = strategy #Should be true or false
        self.newCoop = self.isCoop

    def allocate(self):
        #allocate its resource
        #self.isCoop = self.newCoop
        if self.isCoop:
            return 1.0
        return 0.0
        
    def change_strategy(self, neighbour,K, self_prof,neigh_prof): #K is uncertainty
        prob = 0.0
        if self.isCoop == neighbour.isCoop:
            print("WRONG!! they shouldn't be the same!!")
            exit()

        if (self_prof - neigh_prof)/K > 10:
            return False
        elif (self_prof - neigh_prof)/K < -5:
            self.isCoop = neighbour.isCoop
            return True

        else:
            prob = 1.0/(1.0 + math.exp((self_prof - neigh_prof) /K))

        if choices([True,False],[prob,1.0-prob])[0]:
            self.isCoop = neighbour.isCoop
            return True
        return False
