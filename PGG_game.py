from player import Player
from random import choice, randint

class PGG_5G:
    def __init__(self,r,K,L):
        #rate, noise and size
        self.r = r
        self.K = K
        self.L = L
        self.changed_x = -1
        self.changed_y = -1
        self.first = True
        self.player_matrix = []
        for i in range(L):
            temp_matrix = []
            for j in range(L):
                temp_matrix.append(Player(choice([True,False])))
            self.player_matrix.append(temp_matrix)

    def one_play(self,i,j):
        goods = 1
        goods = goods + self.player_matrix[(i+1) % self.L][j].allocate() + self.player_matrix[(i-1) % self.L][j].allocate() 
        goods = goods + self.player_matrix[i][(j+1) % self.L].allocate() + self.player_matrix[i][(j-1) % self.L].allocate()

        goods = goods * self.r
        #Now it's time to distribute gains
        self.player_matrix[i][j].gain_profit(goods/5.0)
        self.player_matrix[(i+1)%self.L][j].gain_profit(goods/5.0)
        self.player_matrix[(i-1)%self.L][j].gain_profit(goods/5.0)
        self.player_matrix[i][(j+1)%self.L].gain_profit(goods/5.0)
        self.player_matrix[i][(j-1)%self.L].gain_profit(goods/5.0)


    def invest_and_play(self):
        # after players invest, play right then
        if self.changed_x > -1 or self.first:
            for i in range(self.L):
                for j in range(self.L):
                    self.player_matrix[i][j].reset()

            for i in range(self.L):
                for j in range(self.L):
                    #Here, everyone invests
                    self.one_play(i,j)
            self.first = False
            self.changed_x = -1
            return True
        return False


    def modify_strategies(self):
        i = randint(0,self.L-1)
        j = randint(0,self.L-1)
        rand_neigh = choice(['u','d','l','r'])
        if rand_neigh == 'l':
            if self.player_matrix[(i-1)%self.L][j].change_strategy(self.player_matrix[i][j],self.K):
                self.changed_x = (i-1)%self.L
                self.changed_y = j

        elif rand_neigh == 'r':
            if self.player_matrix[(i+1)%self.L][j].change_strategy(self.player_matrix[i][j],self.K):
                self.changed_x = (i+1)%self.L
                self.changed_y = j
        
        elif rand_neigh == 'u':
            if self.player_matrix[i][(j+1)%self.L].change_strategy(self.player_matrix[i][j],self.K):
                self.changed_x = i
                self.changed_y = (j+1)%self.L

        else:
            if self.player_matrix[i][(j-1)%self.L].change_strategy(self.player_matrix[i][j],self.K):
                self.changed_x = i
                self.changed_y = (j-1)%self.L

    def calculate_c(self):
        coor = 0
        ttl = self.L * self.L
        for i in range(self.L):
#            tmp = []
            for j in range(self.L):
#                tmp.append(1 if self.player_matrix[i][j].isCoop else 0)
                if self.player_matrix[i][j].isCoop:
                    coor = coor + 1
#            print(tmp)
        return coor/ttl


if __name__ == '__main__':
    """
    game = PGG_5G(5,0.5,40)

    for i in range(100000):
        cal = game.invest_and_play()
        game.modify_strategies()
        if not cal:
            continue
        per_c = game.calculate_c()
        print(per_c)
        if per_c == 0 or per_c == 1:
            break
    
    """
    for j in range(25):
        game = PGG_5G(5*(0.7+0.02*j),0.5,40)

        for i in range(100000):
            game.invest_and_play()
            game.modify_strategies()
        print((0.8+0.02*j),game.calculate_c())
#    """
