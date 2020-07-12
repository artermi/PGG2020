# SPEC of Advanced-PGG programs

In this python program, I simulate the process of PGG game with D-strategy (with it, the players distribute 4 units their asset to the most-gaining-neighbour and 1 unit to the game centred themselves.). 

## The process of the Advanced-PGG game
The Advanced PGG game program is a fixed $\alpha$ version. That is, all the players play the game with a fixed $\alpha$. As a result, I call it FAPGG game.
The FAPGG goes mainly the same as the origin PGG game, only with the D-strategy as mentioned.
To name the neighbours of a player, say player\[i][j], the player\[i-1][j], player\[i+1][j], player\[i][j-1], player\[i][j+1] as the north, south, east, west neighbour (for the computer coordinate, \[i-1][j] is on the top of \[i][j], so \[i-1][j] is the north neighbour). 

The players have these two strategies:
1. N-Strategy: Non-cooperating strategy. The player that plays this strategy allocates nothing to any game, even to the game centred itself.
2. C-Strategy: Cooperating strategy. The player that plays this strategy allocates 1 unit to itself and 4 unit to its neighbours. It can be further divided into 2 strategies:

    1. C0-Strategy: allocates every neighbour 1 units.
    2. D-Strategy: allocates all 4 units of assets to the most-asset neighbour. (For example, if it gets 1,1,1,4 units from the north, south, east, west neighbour respectively, it recorded the west neighbour as the most-asset neighbour. In the next round, the player will allocate 4 units of assets  to its west neighbour if it plays D-Strategy.) 
    
    In each round, C-Strategy players will play D-strategy with probability of $\alpha$ and C0-strategy with probability of $1-\alpha$. Initially, the players recorded the most earned neighbour as ***None***, so it will play C0-Strategy even if it should play D-strategy in the first round.

To be more specific, the process goes as follow:

1. Initialize the game: Create a 40 by 40 square of players, and assign players C-strategy or N-strategy with a probability of 50-50.
2. Random pick: Pick one player (x) and one of its neighbours (y) randomly.
3. Around-games play: for the player x and y; we charge all its neighbours {xn,xs,xe,xw}, {yn,ys,ye,yw}, and themselves to play one unit game. 
    * Unit game: Take the player 0 as the central player. To execute a unit game w.r.t. to player 0,  all its neighbour, says {0n,0s,0w,0w}, each one allocates its asset to this game according to its strategy. 
    * After this game, player 0 will record from which neighbour it gets the most assets. (If more than one player allocate the most assets, it will randomly record one of these neighbours as the most-asset). 
4. Comparison: After the around-game play, now we know the gains of player x and player y. Then player x would have the probability of F(Gx, Gy) to change its strategy to that of player y. F is the Fermi function, and Gx and Gy stand for the total gains of player x and y.
5. Repeat Step 2 to 4 for 1,600,000 or more times. Named the process from Step 2 to 4 "a unit MC step".

## How To Run The Program
To run the program, you must make sure the ***`PGGgame.py`***, ***`player.py`***, and ***`FAPGGgame.py`*** are in the same directory. To further generate the gif that shows the dynamic status of the game, make sure ***`genimage.py`***, ***`arail.ttf`***, and ***`pngtogif.py`*** are in the same directory.

### How to Run the FAPGG game?
The whole programs are written in python 3.7. Make sure to run under this environment and use `panda `or `pip` to install some library if necessary.

If you want to run the FAPGG game with $r= 5, \alpha = 0.7$ ($r$ is the synergy factor) and store the status images in directory $r5a7$, type the following command in your command line:

```
$ python FAPGG_game.py 5 0.7 r5a7
```

In the terminal, it shows like this:

```
type "python FAPGG_game.py" if you want to run the big simulation
type "python FAPGG_game.py rate alpha path" if just want to try
for example "python FAPGG_game.py 4 0.5 r4a5"
0 0.494375
100 0.9925
200 1.0
300 1.0
400 1.0
500 1.0
600 1.0
```

`600 1.0` implies the program is in the `600th` big iteration (every 1600 MC steps makes a big iteration) and the rate of cooperator (Players with C-strategy/ All Player) is now `1.0`.

In the directory `r5a7`, it generates png files like this:
![r_5.0_alp_0.7_000020.png](https://i.imgur.com/dU83dhd.png)

The colours indicate to which neighbour each player allocates their assets. 

To see the dynamic evolution of this game, type this to your terminal:

```
$ python png_to_gif.py r5a7 d_r5a7
```
It generates a `d_r5a7.gif` file like this:
![](https://i.imgur.com/FTPmrDq.gif)

This is a simplified vesion of the gif: only pick 10 pngs. To save time, the game stop processing if the rate of cooperator reachs 1 or 0.

### How to Run the FAPGG game with many $\alpha$ and $r$ ?

If you want to generate data of cooperator rate with different $\alpha$ and $r$, you may simply type this to your terminal:
```
$ python FAPGG_game.py
```

Then it generates three directories: `alp_000`, `alp_005`, and `alp_010` (In `alp_000`, all data are under the condition of $\alpha = 0$, so for the other directories.) In each directory, there are files with the name of `alp_XXX_r_OOOO.dat` in it. `XXX` is the $\alpha$ of this game (multiplied by 10) and `OOOO` is the synergy rate (multiplied by 1000)

In each file, it record the rate of cooperator in every 500 big iteration.

For example: 
```
$ cat alp_000/alp_000_r_3748.dat
000000 0.486
000500 0.000
001000 0.000
001500 0.000
002000 0.000
002500 0.000
003000 0.000
003500 0.000
004000 0.000
004500 0.000
005000 0.000
005500 0.000
006000 0.000
006500 0.000
007000 0.000
```
This shows the cooperator rates in each iterations. 

To generate different $\alpha$ and $r$, modify the `do_all_mode` function in the 90th line of 'FAPGG_game.py':

``` python
90  def do_all_mode():
91      rlist = [3,3.1,3.15,3.17,3.2,3.25,3.3,3.35,3.4,3.5,3.6,
92              3.74,3.747,3.748,3.75,3.76,3.78,3.80,3.82,3.84,3.86,3.88,3.90,
93              3.92,3.94,3.96,3.98,4.00,4.05,4.10,4.15,4.20,4.30,4.40,4.50,
94              4.60,4.70,4.80,4.90,5.00,5.10,5.20,5.30,5.40,5.44,5.49,5.5]
95      alps = [0,0.5,1]
```
Add or delete the $r,\alpha$ values that is required or not.



To generate the data with the same $r$ in different $\alpha$. Type this to the terminal:

```
$ python FAPGG_game.py alpha
```

It generates directories `r_4000`, `r_4500` and `r_5000` implies that in each directory, all the data have the same synergy rate (but different $\alpha$). 

To generate different $\alpha$ and $r$, modify the `do_alpha` function in the 129th line of 'FAPGG_game.py':

```python
129  def do_alpha_mode():
130      rs = [4,4.5,5]
131      alps = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
```

### Plotting
To plot the data, here is a `plotting.py` file for plotting.

To plot the data of directory `X`, type this:
```
$ python plotting.py X n
```
n = 1 if the `.dat` file names look like `sim_5000.dat` (This is for the old PGG game.)
n = 2 if the `.dat` file names look like `alp_000_r_4000.dat` and plotting according to the $\alpha$. (X-axis is the $\alpha$, the polyline is under the same $r$.)
n = 3 if the `.dat` file names look like `alp_000_r_4000.dat` and plotting according to the $r$. (x-axis is the $r$, the polyline is under the same $\alpha$.)

I also have written the `plot_r` function in line 65, which support the overlay analysis.

```python
65 def plot_r():
66     paths = ['alp_000', 'alp_005','alp_010']
67     style = ['--','-.',':']
68     dlist = []
69     for p,s in zip(paths,style):
70
71         dlist.append((create_list(p,2),s))
72
73     for xy,s in dlist:
74         x,y = xy
75         plt.plot(x,y,s)
76
77     #α
78     plt.legend(['α = 0', 'α = 0.5', 'α = 1'])
79     plt.ylabel('coop.%')
80     plt.xlabel('r/G')
81     plt.show()
```

Modify line 66 to add or remove the directories desired or not.
Modify line 67 to change the style of the polylines. (Here is the [Line style reference](https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.plot.html).)
Modify line 71 `(create_list(p,2)` from 2 to 3 if the current analysis is with respect to different $\alpha$.
Modify line 78 to note the polylines.


Contact:
Colin Cleveland 
Mail: colin.cleveland.formal@gmail.com
