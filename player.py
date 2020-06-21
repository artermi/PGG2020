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
            return False
            """
            print("WRONG!! they shouldn't be the same!!")
            exit()
            """

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

class APlayer(Player):
    def __init__(self,strategy,alpha):
        super().__init__(strategy)
        self.alp = alpha
        self.nei = 'o' #nei for the neighbour to give money. nei can be n,s,e,w
        self.rnd = 0
        self.strD = False

    def allocate(self,nei,rnd):
        if super().allocate() == 1.0 or self.nei == 'o':
            return 1.0

        if self.rnd != rnd:
            self.strD = choices([True,False],[self.alp,1-self.alp])[0]
            self.rnd = rnd
        if self.strD:
            return 4.0 if nei == self.nei else 0.0
        return 1.0

    def change_strategy(self,nei,K,sprof,nprof,mos):
        chan = super().change_strategy(nei,K,sprof,nprof) 
        self.nei = mos
        return chan

