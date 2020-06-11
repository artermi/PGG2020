from PGG_game import PGG_5G
from player import APlayer
from random import choice, randint

class FAPGG_5G(PGG_5G):
    def __init__(self,r,K,L,alp):
        super().__init__(r,K,L)
        self.player_matrix.clear()
        for i in range(L):
            temp_matrix = []
            for j in range(L):
                temp_matrix.append(APlayer(choice([True,False]),alp))
            self.player_matrix.append(temp_matrix)

    def one_play(self,i,j,rnd):
        goods = 1
        mat = self.player_matrix
        L = self.L
        goods = goods + mat[(i+1) % L][j].allocate('e',rnd)
        goods = goods + mat[(i-1) % L][j].allocate('w',rnd)
        goods = goods + mat[i][(j+1) % L].allocate('n',rnd)
        goods = goods + mat[i][(j-1) % L].allocate('s',rnd)
        #Tell you I'm your north or south
        #+-----------> i+        +------------> i+
        #|    n                  |    s
        #| e  0   w              | w  t  e
        #|    s                  |    n
        #˅                       ˅
        #j+                      j+ 
        #  (origin)                  (I'm your...)
        
        return goods * self.r /5.0

    def the_most(self,a,b,c,d): #north,south,east,west
        lst = [a,b,c,d]
        mst = max(lst)
        dire = ['n','s','e','w']
        for i in range(4):
            if lst[i] == mst:
                return dire[i]
        return '0'

    def two_players_play(self,rnd):
        xi,xj = self.xi,self.xj
        yi,yj = self.yi,self.yj
        mat = self.player_matrix
        L = self.L
        if self.xi > -1:
            profit_x = 1
            profit_x = profit_x + self.one_play((xi+1) % L,xj,rnd)
            profit_x = profit_x + self.one_play((xi-1) % L,xj,rnd)
            profit_x = profit_x + self.one_play(xi,(xj+1) % L,rnd)
            profit_x = profit_x + self.one_play(xi,(xj-1) % L,rnd)

            pye = self.one_play((yi+1) % L,yj,rnd) #east
            pyw = self.one_play((yi-1) % L,yj,rnd) #west
            pyn = self.one_play(yi,(yj-1) % L,rnd) #north
            pys = self.one_play(yi,(yj+1) % L,rnd) #south
            profit_y = 1 + pye + pyw + pyn + pys

            mat[yi][yj].change_strategy(mat[xi][xj],self.K,profit_y,profit_x,self.the_most(pyn,pys,pye,pyw))

        self.xi = -1
        
if __name__ == '__main__':
    game = FAPGG_5G(1.5,0.5,40,0.5)
    for i in range(10001):
        if i % 2 == 0:
            print(i,game.calculate_rate())
#        for i in range(1600):
        if True:
            modi = game.choose_players()
            if not modi:
                continue
            game.two_players_play(i)
