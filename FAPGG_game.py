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
    def one_play(self,i,j):
        goods = 1
        mat = self.player_matrix
        L = self.L
        goods = goods + mat[(i+1) % L][j].allocate('e')
        goods = goods + mat[(i-1) % L][j].allocate('w')
        goods = goods + mat[i][(j+1) % L].allocate('n')
        goods = goods + mat[i][(j-1) % L].allocate('s')
        #Tell you I'm your north or south
        #+ - - - - - - - > i+
        #|      n(s)  
        #| e(w)  0   w(e)
        #|      s(n)
        #˅
        #j+

        return goods * self.r /5.0
    def the_most(a,b,c,d): #north,south,east,west
        lst = [a,b,c,d]
        mst = max(lst)
        dire = ['n','s','e','w']
        for i in range(4):
            if lis[i] == mst:
                return dire[i]
        return '0'
    def two_players_play(self):
        xi,xj = self.xi,self.xj
        yi,yj = self.yi,self.yj
        mat = self.player_matrix
        L = self.L
        if self.xi > -1:
            profit_x = 1
            profit_x = profit_x + self.one_play((xi+1) % L,xj)
            profit_x = profit_x + self.one_play((xi-1) % L,xj)
            profit_x = profit_x + self.one_play(xi,(xj+1) % L)
            profit_x = profit_x + self.one_play(xi,(xj-1) % L)

            pye = self.one_play((yi+1) % L,yj) #east
            pyw = self.one_play((yi-1) % L,yj) #west
            pyn = self.one_play(yi,(yj-1) % L) #north
            pys = self.one_play(yi,(yj+1) % L) #south
            profit_y = 1 + pye + pyw + pyn + pys

            mat[yi][yj].change_strategy(mat[xi][xj],self.K,profit_y,profit_x,self.the_most(pyn,pys,pye,pyw))

        self.xi = -1
        
if __name__ == '__main__':
    game = FAPGG_5G(5,0.5,40,0.5)
    for i in range(10001):
        if i % 500 == 0:
            print(i,game.calculate_rate())
        for i in range(1600):
            modi = game.choose_players()
            if not modi:
                continue
            game.two_players_play()
