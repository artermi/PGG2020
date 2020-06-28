from PGG_game import PGG_5G
from player import APlayer
from random import choice, randint,choices
from pathlib import Path
import sys

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
        mat = self.player_matrix
        L = self.L
        goods = mat[i][j].allocate('o',rnd)
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

        profit_x = self.one_play(xi,xj,rnd)
        profit_x = profit_x + self.one_play((xi+1) % L,xj,rnd)
        profit_x = profit_x + self.one_play((xi-1) % L,xj,rnd)
        profit_x = profit_x + self.one_play(xi,(xj+1) % L,rnd)
        profit_x = profit_x + self.one_play(xi,(xj-1) % L,rnd)

        profit_x = profit_x - 5 if mat[xi][xj].isCoop else profit_x

        profit_y = self.one_play(yi,yj,rnd)
        pye = self.one_play((yi+1) % L,yj,rnd) #east
        pyw = self.one_play((yi-1) % L,yj,rnd) #west
        pyn = self.one_play(yi,(yj-1) % L,rnd) #north
        pys = self.one_play(yi,(yj+1) % L,rnd) #south
        profit_y = profit_y + pye + pyw + pyn + pys

        profit_y = profit_y - 5 if mat[yi][yj].isCoop else profit_y

        mat[yi][yj].change_strategy(mat[xi][xj],self.K,profit_y,profit_x,self.the_most(pyn,pys,pye,pyw))


    def choose_players(self):
        if super().choose_players():
            return True
        elif self.player_matrix[self.xi][self.xj].isCoop == False:
            return True
        else:
            return False

def do_all_mode():
    rlist = [3.74,3.747,3.748,3.75,3.76,3.78,3.80,3.82,3.84,3.86,3.88,3.90,
            3.92,3.94,3.96,3.98,4.00,4.05,4.10,4.15,4.20,4.30,4.40,4.50,
            4.60,4.70,4.80,4.90,5.00,5.10,5.20,5.30,5.40,5.44,5.49,5.5]

    alps = [0,0.5,1]
    paths = []
    for alp in alps:
        path = 'alp_' + str(int(alp * 10)).zfill(3)
        Path(path).mkdir(parents=True, exist_ok=True)
        paths.append((path,alp))

    for path in paths:
        p, alp = path

        for r in rlist:
            filename = p + '/' + p + '_' + 'r_' +  str(int(r * 1000) ) + '.dat'
            f = open(filename,"a")
            print('Now doing:' + filename)

            game = FAPGG_5G(r,0.5,40,alp) #r,K,L alp
            for i in range(10001):
                if i % 500 == 0:
                    per_c = game.calculate_rate()
                    f.write(str(i).zfill(6) + ' ' + '%.3f'%(per_c) + '\n')
                    print(i,per_c)

                for j in range(1600):
                    modi = game.choose_players()
                    if not modi:
                        continue
                #If the strategy is not modified, no need to play the game
                    game.two_players_play(j + i * 1600)
            f.close()
        
if __name__ == '__main__':
    msg0 = 'type "python FAPGG_game.py" if you want to run the big simulation'
    msg1 = 'type "python FAPGG_game.py rate alpha path" if just want to try'
    msg2 = 'for example "python FAPGG_game.py 4 0.5 r4a5"'
    print(msg0)
    print(msg1)
    print(msg2)

    if len(sys.argv) < 2:
        do_all_mode()
        sys.exit()

    #read from argv
    r = float(sys.argv[1])
    alp = float(sys.argv[2])
    path = sys.argv[3]

    game = FAPGG_5G(r,0.5,40,alp)
    for i in range(10001):
        if i % 100 == 0:
            print(i,game.calculate_rate())
        for j in range(1600):
#        if True:
            modi = game.choose_players()
            if not modi:
                continue
            game.two_players_play(j + i*1600)

        if i % 20 == 0:
            game.print_pic(path + '/' + 'r_'+str(r) + '_alp_'+str(alp) + '_' + str(i).zfill(6))
    
