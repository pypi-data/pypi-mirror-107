import time
import numpy as np
from numba import njit
from spins2cpu import functions

def iteration2(latt, X, Y, Ja, Jb, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 4))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        randvals = np.random.rand(4, Y, X)
        E0 = update2(latt, randvals, X, Y, Ja, Jb, val)
    for i in range(nworks):
        randvals = np.random.rand(4, Y, X)
        E0 = update2(latt, randvals, X, Y, Ja, Jb, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[0]), functions.Average(latt[1]), functions.Average(latt[2]), functions.Average(latt[3])
    t = time.time() - t0
    return t, Nw, Ew

class grid:
    def __init__(self, X, Y, position):
        k, j, i = position
        kx = 3 - k
        ky1 = (5 - k) if k > 1 else (1 - k)
        ky2 = (2 - k) if k%2 == 0 else (4 - k)
        jpp = (j + 1) if (j + 1) < Y  else 0
        jnn = (j - 1) if (j - 1) > -1 else (Y - 1)
        ipp = (i + 1) if (i + 1) < X  else 0
        inn = (i - 1) if (i - 1) > -1 else (X - 1)
        if k == 0:
            x_inn = i
            x_ipp = ipp
            y_jnn = j
            y_jpp = jpp
            i2_oo = i
        elif k == 1:
            x_inn = i
            x_ipp = ipp
            y_jnn = jnn
            y_jpp = j
            i2_oo = ipp
        elif k == 2:
            x_inn = inn
            x_ipp = i
            y_jnn = jnn
            y_jpp = j
            i2_oo = i
        else:
            x_inn = inn
            x_ipp = i
            y_jnn = j
            y_jpp = jpp
            i2_oo = inn
        self.lef = (kx, j, x_inn)
        self.rig = (kx, j, x_ipp)
        self.up1 = (ky1, y_jnn, i)
        self.do1 = (ky1, y_jpp, i)
        self.up2 = (ky2, y_jnn, i2_oo)
        self.do2 = (ky2, y_jpp, i2_oo)

def cluster(latt, X, Y, Ja, Jb, val):
    k = np.random.randint(0, 4)
    j = np.random.randint(0, Y)
    i = np.random.randint(0, X)
    sign = latt[k,j,i]
    P_addx = 1 - np.exp( 2 * val * -Ja )
    P_addy = 1 - np.exp( 2 * val * -Jb )
    lable = functions.Onesint3(4, Y, X)
    stack = [(k,j,i)]
    lable[k,j,i] = 0
    while len(stack) > 0:
        current = stack.pop()
        latt[current] = -sign
        neighbor = grid(X, Y, current)
        if latt[neighbor.lef] == sign and lable[neighbor.lef] and np.random.rand() < P_addx:
            stack.append(neighbor.lef)
            lable[neighbor.lef] = 0
        if latt[neighbor.rig] == sign and lable[neighbor.rig] and np.random.rand() < P_addx:
            stack.append(neighbor.rig)
            lable[neighbor.rig] = 0 
        if latt[neighbor.up1] == sign and lable[neighbor.up1] and np.random.rand() < P_addy:
            stack.append(neighbor.up1)
            lable[neighbor.up1] = 0 
        if latt[neighbor.up2] == sign and lable[neighbor.up2] and np.random.rand() < P_addy:
            stack.append(neighbor.up2)
            lable[neighbor.up2] = 0 
        if latt[neighbor.do1] == sign and lable[neighbor.do1] and np.random.rand() < P_addy:
            stack.append(neighbor.do1)
            lable[neighbor.do1] = 0 
        if latt[neighbor.do2] == sign and lable[neighbor.do2] and np.random.rand() < P_addy:
            stack.append(neighbor.do2)
            lable[neighbor.do2] = 0

@njit
def update2(latt, randvals, X, Y, Ja, Jb, val):
    nn_sum = 0
    for k in range(4):
        for j in range(Y):
            for i in range(X):
                ipp = (i + 1) if (i + 1) < X  else 0
                inn = (i - 1) if (i - 1) >= 0 else (X - 1)
                jpp = (j + 1) if (j + 1) < Y  else 0
                jnn = (j - 1) if (j - 1) >= 0 else (Y - 1)
                if k == 0:
                    energy = latt[0,j,i] * ( -Ja * ( latt[3,j,i] + latt[3,j,ipp] ) -
                                              Jb * ( latt[1,j,i] + latt[1,jpp,i] +
                                                     latt[2,j,i] + latt[2,jpp,i] ) )
                elif k == 1:
                    energy = latt[1,j,i] * ( -Ja * ( latt[2,j,i] + latt[2,j,ipp] ) -
                                              Jb * ( latt[0,j,i] + latt[0,jnn,i] +
                                                     latt[3,j,ipp] + latt[3,jnn,ipp] ) )
                elif k == 2:
                    energy = latt[2,j,i] * ( -Ja * ( latt[1,j,i] + latt[1,j,inn] ) -
                                              Jb * ( latt[3,j,i] + latt[3,jnn,i] +
                                                     latt[0,j,i] + latt[0,jnn,i] ) )
                else:
                    energy = latt[3,j,i] * ( -Ja * ( latt[0,j,i] + latt[0,j,inn] ) -
                                              Jb * ( latt[2,j,i] + latt[2,jpp,i] +
                                                     latt[1,j,inn] + latt[1,jpp,inn] ) )

                if val == 0:
                    if energy < 0:
                        pass
                    else:
                        latt[k,j,i] *= -1
                else:
                    if energy < 0:
                        if randvals[k,j,i] < np.exp( 2.0 * val * energy ):
                            latt[k,j,i] *= -1
                    else:
                        latt[k,j,i] *= -1

                nn_sum += energy

    return nn_sum
