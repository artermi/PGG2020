from player import Player
from random import choice, randint

class PGG_5G:
    def __init__(self,r,K,L):
        #rate, noise and size
        self.r = r
        self.K = K
        self.L = L

        #x is the chosen player that need to suggest y its strategy
        self.xi = -1
        self.xj = -1
        self.yi = -1
        self.yj = -1

        self.first = True
        self.player_matrix = []
        for i in range(L):
            temp_matrix = []
            for j in range(L):
                temp_matrix.append(Player(choice([True,False])))
            self.player_matrix.append(temp_matrix)

    def one_play(self,i,j):
        #each we asked the players of grid[i][j] to play
        goods = self.player_matrix[i][j].allocate()
        goods = goods + self.player_matrix[(i+1) % self.L][j].allocate() + self.player_matrix[(i-1) % self.L][j].allocate() 
        goods = goods + self.player_matrix[i][(j+1) % self.L].allocate() + self.player_matrix[i][(j-1) % self.L].allocate()

        return goods * self.r / 5.0 #just record the gain


    def two_players_play(self):
        if self.xi > -1: #Means x and y have different strateies
            L = self.L
            profit_x = self.one_play(self.xi,self.xj)
            profit_x = profit_x + self.one_play((self.xi+1)%L,self.xj) + self.one_play((self.xi-1)%L,self.xj)
            profit_x = profit_x + self.one_play(self.xi,(self.xj+1)%L) + self.one_play(self.xi,(self.xj-1)%L)
            if self.player_matrix[self.xi][self.xj].isCoop:
                profit_x = profit_x - 5

            profit_y = self.one_play(self.yi,self.yj)
            profit_y = profit_y + self.one_play((self.yi+1)%L,self.yj) + self.one_play((self.yi-1)%L,self.yj)
            profit_y = profit_y + self.one_play(self.yi,(self.yj+1)%L) + self.one_play(self.yi,(self.yj-1)%L)
            if self.player_matrix[self.yi][self.yj].isCoop:
                profit_y = profit_y - 5
            
            self.player_matrix[self.yi][self.yj].change_strategy(self.player_matrix[self.xi][self.xj],self.K,profit_y,profit_x)

        self.xi = -1


    def choose_players(self):
        i = randint(0,self.L-1)
        j = randint(0,self.L-1)

        rand_neigh = choice(['u','d','l','r'])
        if rand_neigh == 'l':
            self.yi = (i-1)%self.L
            self.yj = j

        elif rand_neigh == 'r':
            self.yi = (i+1)%self.L
            self.yj = j
        
        elif rand_neigh == 'u':
            self.yi = i
            self.yj = (j+1)%self.L

        else:
            self.yi = i
            self.yj = (j-1)%self.L

        #I use self.xi to see if the x,y use the same strategies
        if self.player_matrix[self.yi][self.yj].isCoop != self.player_matrix[i][j].isCoop:
            self.xi = i
            self.xj = j
        else:
            self.xi = -1

        return self.xi > -1 #means two players do not use the same strategy


    def calculate_rate(self):
        coor = 0
        ttl = self.L * self.L
        for i in range(self.L):
            for j in range(self.L):
                if self.player_matrix[i][j].isCoop:
                    coor = coor + 1
        return coor/ttl


if __name__ == '__main__':
#    """
    game = PGG_5G(5,0.5,40)

    for i in range(100000):
        if i % 500 == 0:
            per_c = game.calculate_rate()
            print(i,per_c)
        for j in range(1600):
            modi = game.choose_players()
            if not modi:
                continue
        #If the strategy is not modified, no need to play the game
            game.two_players_play()

    
    """
    for j in range(25):
        game = PGG_5G(5*(0.7+0.02*j),0.5,40)

        for i in range(100000):
            game.invest_and_play()
            game.modify_strategies()
        print((0.8+0.02*j),game.calculate_c())
    """
