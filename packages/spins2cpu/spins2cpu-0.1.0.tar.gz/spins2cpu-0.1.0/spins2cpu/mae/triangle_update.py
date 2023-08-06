import time
import numpy as np
from numba import njit
from spins2cpu import functions

def iteration(latt, X_s, Y_s, Ja, JA, val, nequilibrium, nworks):
    t0 = time.time()
    Nw = np.zeros((nworks, 2))
    Ew = np.zeros(nworks)
    ju = Ja * val
    ku = JA * val
    for i in range(nequilibrium):
        if ju > 3:
            randvaln = initdist(latt, X_s, Y_s, ku)
        else:
            randvaln = functions.NormalrandN(4, Y_s, X_s)
        randvals = np.random.rand(4, Y_s, X_s)
        Etot = update(latt, randvaln, randvals, X_s, Y_s, Ja, JA, val)
    for i in range(nworks):
        if ju > 3:
            randvaln = initdist(latt, X_s, Y_s, ku)
        else:
            randvaln = functions.NormalrandN(4, Y_s, X_s)
        randvals = np.random.rand(4, Y_s, X_s)
        Etot = update(latt, randvaln, randvals, X_s, Y_s, Ja, JA, val)
        Ew[i] = Etot
        Nw[i] = functions.Average(latt[::2,2]), functions.Average(latt[1::2,2])
    t = time.time() - t0
    return t, Nw, Ew

def initdist(latt, X_s, Y_s, ku):
    randsign = np.random.choice([-1,1],size=(4, 3, Y_s, X_s))
    randvals = np.random.rand(4, 3, Y_s, X_s)
    trial = np.zeros((4, 3, Y_s, X_s))
    sign = np.where(np.abs(latt) < 0.1, randsign, np.sign(latt))
    if ku > 0.1:
        trialxy = np.sqrt( np.log( 1 - randvals[:,2] * ( 1 - np.exp(-ku) ) ) / (-ku) )
    else:
        trialxy = np.sqrt( randvals[:,2] )
    trial[:,2] = np.sign(sign[:,2]) * np.sqrt(1 - trialxy ** 2)
    randxy = np.sqrt(randvals[:,0] ** 2 + randvals[:,1] ** 2)
    tridiv = trialxy / randxy
    trial[:,0] = np.sign(sign[:,0]) *randvals[:,0] * tridiv
    trial[:,1] = np.sign(sign[:,1]) *randvals[:,1] * tridiv
    return trial

@njit
def update(latt, randvaln, randvals, X_s, Y_s, Ja, JA, val):
    nn_sum = 0
    nn_p = 0
    for k in range(4):
        for j in range(Y_s):
            for i in range(X_s):
                ipp = (i + 1) if (i + 1) < X_s else 0
                inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
                jpp = (j + 1) if (j + 1) < Y_s else 0
                jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
                kx = 3 - k
                ky = (5 - k) if k > 1 else (1 - k)
                kz = (2 - k) if k%2 == 0 else (4 - k)
                if k == 0:
                    x_inn = i
                    x_ipp = ipp
                    y_jnn = j
                    y_jpp = jpp
                elif k == 1:
                    x_inn = i
                    x_ipp = ipp
                    y_jnn = jnn
                    y_jpp = j
                elif k == 2:
                    x_inn = inn
                    x_ipp = i
                    y_jnn = jnn
                    y_jpp = j
                else:
                    x_inn = inn
                    x_ipp = i
                    y_jnn = j
                    y_jpp = jpp

                energy0 = -Ja * ( latt[k,0,j,i] * ( latt[kx,0,j,x_ipp] + latt[kx,0,j,x_inn] + latt[ky,0,y_jpp,i] + latt[ky,0,y_jnn,i] + latt[kz,0,y_jnn,x_inn] + latt[kz,0,y_jpp,x_ipp] ) +
                                  latt[k,1,j,i] * ( latt[kx,1,j,x_ipp] + latt[kx,1,j,x_inn] + latt[ky,1,y_jpp,i] + latt[ky,1,y_jnn,i] + latt[kz,1,y_jnn,x_inn] + latt[kz,1,y_jpp,x_ipp] ) +
                                  latt[k,2,j,i] * ( latt[kx,2,j,x_ipp] + latt[kx,2,j,x_inn] + latt[ky,2,y_jpp,i] + latt[ky,2,y_jnn,i] + latt[kz,2,y_jnn,x_inn] + latt[kz,2,y_jpp,x_ipp] ) )
                ez = -JA * latt[k,2,j,i] ** 2
                Erandn = ( -Ja * ( randvaln[k,0,j,i] * ( latt[kx,0,j,x_ipp] + latt[kx,0,j,x_inn] + latt[ky,0,y_jpp,i] + latt[ky,0,y_jnn,i] + latt[kz,0,y_jnn,x_inn] + latt[kz,0,y_jpp,x_ipp] ) +
                                   randvaln[k,1,j,i] * ( latt[kx,1,j,x_ipp] + latt[kx,1,j,x_inn] + latt[ky,1,y_jpp,i] + latt[ky,1,y_jnn,i] + latt[kz,1,y_jnn,x_inn] + latt[kz,1,y_jpp,x_ipp] ) +
                                   randvaln[k,2,j,i] * ( latt[kx,2,j,x_ipp] + latt[kx,2,j,x_inn] + latt[ky,2,y_jpp,i] + latt[ky,2,y_jnn,i] + latt[kz,2,y_jnn,x_inn] + latt[kz,2,y_jpp,x_ipp] ) ) -
                              JA * randvaln[k,2,j,i] ** 2 )
                Eold = ez + energy0
                Eflip = ez - energy0
                arrE = np.array([Eflip, Erandn, Eold])
                Esort = np.argsort(arrE)
                if val == 0:
                    if Esort[0] == 0:
                        latt[k,:,j,i] *= -1
                    elif Esort[0] == 1:
                        latt[k,:,j,i] = randvaln[k,:,j,i]
                else:
                    if Esort[0] == 0:
                        latt[k,:,j,i] *= -1
                    elif Esort[0] == 1:
                        latt[k,:,j,i] = randvaln[k,:,j,i]
                    else:
                        if Esort[1] == 0:
                            if randvals[k,j,i] < np.exp( 2.0 * val * energy0 ):
                                latt[k,:,j,i] *= -1
                        elif Esort[1] == 1:
                            DeltaE = Eold - Erandn
                            if randvals[k,j,i] < np.exp( val * DeltaE ):
                                latt[k,:,j,i] = randvaln[k,:,j,i]

                nn_sum += energy0
                nn_p += ez
    return ( nn_p + nn_sum / 2.0 )
