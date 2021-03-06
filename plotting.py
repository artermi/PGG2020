import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import statistics

def main(path,mode):
    xa = [] #X axis, can be r/G or alpha
    cr = [] #rate of cooperator

    for fi in os.listdir(path):
        xi = 0
        if mode == 1: #classic, file name is sim_5000.dat
            xi = float(fi[4:8])/5000
        elif mode == 2: #classic, file name is alp_000_r_4000.dat
            xi = float(fi[10:14])/5000
        elif mode == 3: #do different alpha, file name is alp_000_r_4000.dat
            xi = float(fi[4:7])/10
        else:
            pass

        xa.append(xi)
        with open(path + '/' + fi,'r') as f:
            all_num = []
            for line in f:
                rnd, per = int(line.split()[0]), float(line.split()[1])
                if rnd < 5000:
                    continue
                all_num.append(per)
            cr.append(statistics.mean(all_num))


    plt.plot(xa,cr,'ro')
    plt.legend([path])
    plt.show()

def create_list(path,mode):
    xa = [] #X axis, can be r/G or alpha
    cr = [] #rate of cooperator

    for fi in os.listdir(path):
        xi = 0
        if mode == 1: #classic, file name is sim_5000.dat
            xi = float(fi[4:8])/5000
        elif mode == 2: #classic, file name is alp_000_r_4000.dat
            xi = float(fi[10:14])/5000
        elif mode == 3: #do different alpha, file name is alp_000_r_4000.dat
            xi = float(fi[4:7])/10
        else:
            pass

        xa.append(xi)
        with open(path + '/' + fi,'r') as f:
            all_num = []
            for line in f:
                rnd, per = int(line.split()[0]), float(line.split()[1])
                if rnd < 5000:
                    continue
                all_num.append(per)
            cr.append(statistics.mean(all_num))

    return zip(*sorted(zip(xa,cr)))


def plot_r():
    paths = ['alp_000', 'alp_005','alp_010']
    style = ['--','-.',':']
    dlist = []
    for p,s in zip(paths,style):

        dlist.append((create_list(p,2),s))

    for xy,s in dlist:
        x,y = xy
        plt.plot(x,y,s)

    #α
    plt.legend(['α = 0', 'α = 0.5', 'α = 1'])
    plt.ylabel('coop.%')
    plt.xlabel('r/G')
    plt.show()

if __name__ == '__main__':
    print('type "python plotting.py path n"to plot the things in this path')
    print('n = 1 if want to do classic, n = 2 if want to do classic in different alpha')
    print('n = 3 if want to plot co vs alpha.')

    plot_r()
    sys.exit()

    if len(sys.argv) < 2:
        sys.exit()

    path = sys.argv[1]
    mode = int(sys.argv[2])
    main(path,mode)


