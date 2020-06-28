from PGG_game import PGG_5G
from player import APlayer
from random import choice, randint,choices


class FAPGG_5G(PGG_5G):
    def __init__(self,r,K,L,alp):
        super().__init__(r,K,L)
        self.player_matrix.clear()
        for i in range(L): 
            temp_matrix = []
            for j in range(L):
                temp_matrix.append(APlayer(choice([True,False]),alp))
#                temp_matrix.append(APlayer(choices([True,False],[0.1,0.9])[0],alp))
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
        #|   s  n                  |    s
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
        mst_list = []
        for i in range(4):
            if lst[i] == mst:
                mst_list.append(dire[i])

        if len(mst_list) > 0:
            return choice(mst_list)

        return '0'

    def two_players_play(self,rnd):
        xi,xj = self.xi,self.xj
        yi,yj = self.yi,self.yj
        mat = self.player_matrix
        L = self.L
        if self.xi > -1:
            profit_x = self.one_play(xi,xj,rnd)
            profit_x = profit_x + self.one_play((xi+1) % L,xj,rnd)
            profit_x = profit_x + self.one_play((xi-1) % L,xj,rnd)
            profit_x = profit_x + self.one_play(xi,(xj+1) % L,rnd)
            profit_x = profit_x + self.one_play(xi,(xj-1) % L,rnd)

            profit_x = profit_x - 5 if mat[xi][xj].isCoop else profit_x

            pye = self.one_play((yi+1) % L,yj,rnd) #east
            pyw = self.one_play((yi-1) % L,yj,rnd) #west
            pyn = self.one_play(yi,(yj-1) % L,rnd) #north
            pys = self.one_play(yi,(yj+1) % L,rnd) #south
            profit_y = self.one_play(yi,yj,rnd) + pye + pyw + pyn + pys

            profit_y = profit_y - 5 if mat[yi][yj].isCoop else profit_y

            mat[yi][yj].change_strategy(mat[xi][xj],self.K,profit_y,profit_x,self.the_most(pyn,pys,pye,pyw))

        self.xi = -1

    def choose_players(self):
        if super().choose_players():
            return True
        elif self.player_matrix[self.xi][self.xj].isCoop == False:
            return True
        else:
            return False
        
if __name__ == '__main__':
    r = 5
    alp = 0.5
    game = FAPGG_5G(r,0.5,40,alp)
    for i in range(10001):
        if i % 10 == 0:
            print(i,game.calculate_rate())
        for j in range(1600):
#        if True:
            modi = game.choose_players()
            if not modi:
                continue
            game.two_players_play(j + i*1600)

        if i % 20 == 0:
            game.print_pic('pic/' + 'r_'+str(r) + '_alp_'+str(alp) + '_' + str(i).zfill(6) + '.png')
