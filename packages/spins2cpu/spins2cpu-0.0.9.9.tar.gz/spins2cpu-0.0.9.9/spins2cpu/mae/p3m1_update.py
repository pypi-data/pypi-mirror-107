import time
import numpy as np
from numba import njit
from spins2cpu import functions

def initdist(latt, X_s, Y_s, ku):
    randsign = np.random.choice([-1,1],size=(2, 4, 3, Y_s, X_s))
    randvals = np.random.rand(2, 4, 3, Y_s, X_s)
    trial = np.zeros((2, 4, 3, Y_s, X_s))
    sign = np.where(np.abs(latt) < 0.1, randsign, np.sign(latt))
    if ku > 0.1:
        trialxy = np.sqrt( np.log( 1 - randvals[:,:,2] * ( 1 - np.exp(-ku) ) ) / (-ku) )
    else:
        trialxy = np.sqrt( randvals[:,:,2] )
    trial[:,:,2] = np.sign(sign[:,:,2]) * np.sqrt(1 - trialxy ** 2)
    randxy = np.sqrt(randvals[:,:,0] ** 2 + randvals[:,:,1] ** 2)
    tridiv = trialxy / randxy
    trial[:,:,0] = np.sign(sign[:,:,0]) *randvals[:,:,0] * tridiv
    trial[:,:,1] = np.sign(sign[:,:,1]) *randvals[:,:,1] * tridiv
    return trial

def iteration2(latt, X_s, Y_s, Ja, J0, JA, val, nequilibrium, nworks):
    t0 = time.time()
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    ju = Ja * val
    ku = JA * val
    for i in range(nequilibrium):
        if ju > 3:
            randvaln = initdist(latt, X_s, Y_s, ku)
        else:
            randvaln = functions.NormalrandNN(2, 4, Y_s, X_s)
        randvals = np.random.rand(2, 4, Y_s, X_s)
        Etot = update2(latt, randvaln, randvals, X_s, Y_s, Ja, J0, JA, val)
    for i in range(nworks):
        if ju > 3:
            randvaln = initdist(latt, X_s, Y_s, ku)
        else:
            randvaln = functions.NormalrandNN(2, 4, Y_s, X_s)
        randvals = np.random.rand(2, 4, Y_s, X_s)
        Etot = update2(latt, randvaln, randvals, X_s, Y_s, Ja, J0, JA, val)
        Ew[i] = Etot
        Nw[i] = functions.Average(latt[0,0,2]), functions.Average(latt[0,1,2]), functions.Average(latt[0,2,2]), functions.Average(latt[0,3,2]),\
                functions.Average(latt[1,0,2]), functions.Average(latt[1,1,2]), functions.Average(latt[1,2,2]), functions.Average(latt[1,3,2])
    t = time.time() - t0
    return t, Nw, Ew

@njit
def update2(latt, randvaln, randvals, X_s, Y_s, Ja, J0, JA, val):
    nn_sum = 0
    nn_p = 0
    for l in range(2):
        for k in range(4):
            for j in range(Y_s):
                for i in range(X_s):
                    lo = 1 - l
                    k1 = 3 - k
                    k2 = (5 - k) if k > 1 else (1 - k)
                    k3 = (2 - k) if k%2 == 0 else (4 - k)
                    ipp = (i + 1) if (i + 1) < X_s else 0
                    inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
                    jpp = (j + 1) if (j + 1) < Y_s else 0
                    jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
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

                    if l == 0:
                        if k == 0:
                            i_1 = i
                            j_2 = jpp
                        elif k == 1:
                            i_1 = i
                            j_2 = j
                        elif k == 2:
                            i_1 = inn
                            j_2 = j
                        else:
                            i_1 = inn
                            j_2 = jpp
                    else:
                        if k == 0:
                            i_1 = ipp
                            j_2 = j
                        elif k == 1:
                            i_1 = ipp
                            j_2 = jnn
                        elif k == 2:
                            i_1 = i
                            j_2 = jnn
                        else:
                            i_1 = i
                            j_2 = j

                    energy0 = ( latt[l,k,0,j,i] * ( -Ja * ( latt[l,k1,0,j,x_ipp] + latt[l,k1,0,j,x_inn] +
                                                            latt[l,k2,0,y_jpp,i] + latt[l,k2,0,y_jnn,i] +
                                                            latt[l,k3,0,y_jnn,x_inn] + latt[l,k3,0,y_jpp,x_ipp] ) -
                                                     J0 * ( latt[lo,k,0,j,i] + latt[lo,k1,0,j,i_1] + latt[lo,k2,0,j_2,i] ) ) +
                                latt[l,k,1,j,i] * ( -Ja * ( latt[l,k1,1,j,x_ipp] + latt[l,k1,1,j,x_inn] +
                                                            latt[l,k2,1,y_jpp,i] + latt[l,k2,1,y_jnn,i] +
                                                            latt[l,k3,1,y_jnn,x_inn] + latt[l,k3,1,y_jpp,x_ipp] ) -
                                                     J0 * ( latt[lo,k,1,j,i] + latt[lo,k1,1,j,i_1] + latt[lo,k2,1,j_2,i] ) ) +
                                latt[l,k,2,j,i] * ( -Ja * ( latt[l,k1,2,j,x_ipp] + latt[l,k1,2,j,x_inn] +
                                                            latt[l,k2,2,y_jpp,i] + latt[l,k2,2,y_jnn,i] +
                                                            latt[l,k3,2,y_jnn,x_inn] + latt[l,k3,2,y_jpp,x_ipp] ) -
                                                     J0 * ( latt[lo,k,2,j,i] + latt[lo,k1,2,j,i_1] + latt[lo,k2,2,j_2,i] ) ) )
                    ez =  -JA * latt[l,k,2,j,i] ** 2
                    Erandn = ( randvaln[l,k,0,j,i] * ( -Ja * ( latt[l,k1,0,j,x_ipp] + latt[l,k1,0,j,x_inn] +
                                                               latt[l,k2,0,y_jpp,i] + latt[l,k2,0,y_jnn,i] +
                                                               latt[l,k3,0,y_jnn,x_inn] + latt[l,k3,0,y_jpp,x_ipp] ) -
                                                        J0 * ( latt[lo,k,0,j,i] + latt[lo,k1,0,j,i_1] + latt[lo,k2,0,j_2,i] ) ) +
                               randvaln[l,k,1,j,i] * ( -Ja * ( latt[l,k1,1,j,x_ipp] + latt[l,k1,1,j,x_inn] +
                                                               latt[l,k2,1,y_jpp,i] + latt[l,k2,1,y_jnn,i] +
                                                               latt[l,k3,1,y_jnn,x_inn] + latt[l,k3,1,y_jpp,x_ipp] ) -
                                                        J0 * ( latt[lo,k,1,j,i] + latt[lo,k1,1,j,i_1] + latt[lo,k2,1,j_2,i] ) ) +
                               randvaln[l,k,2,j,i] * ( -Ja * ( latt[l,k1,2,j,x_ipp] + latt[l,k1,2,j,x_inn] +
                                                               latt[l,k2,2,y_jpp,i] + latt[l,k2,2,y_jnn,i] +
                                                               latt[l,k3,2,y_jnn,x_inn] + latt[l,k3,2,y_jpp,x_ipp] ) -
                                                        J0 * ( latt[lo,k,2,j,i] + latt[lo,k1,2,j,i_1] + latt[lo,k2,2,j_2,i] ) ) -
                               JA * randvaln[l,k,2,j,i] ** 2 )
                    Eold = ez + energy0
                    Eflip = ez - energy0
                    arrE = np.array([Eflip, Erandn, Eold])
                    Esort = np.argsort(arrE)
                    if val == 0:
                        if Esort[0] == 0:
                            latt[l,k,:,j,i] *= -1
                        elif Esort[0] == 1:
                            latt[l,k,:,j,i] = randvaln[l,k,:,j,i]
                    else:
                        if Esort[0] == 0:
                            latt[l,k,:,j,i] *= -1
                        elif Esort[0] == 1:
                            latt[l,k,:,j,i] = randvaln[l,k,:,j,i]
                        else:
                            if Esort[1] == 0:
                                if randvals[l,k,j,i] < np.exp( 2.0 * val * energy0 ):
                                    latt[l,k,:,j,i] *= -1
                            elif Esort[1] == 1:
                                DeltaE = Eold - Erandn
                                if randvals[l,k,j,i] < np.exp( val * DeltaE ):
                                    latt[l,k,:,j,i] = randvaln[l,k,:,j,i]

                    nn_sum += energy0
                    nn_p += ez
    return ( nn_p + nn_sum / 2.0 )

def iteration3(latt, X_s, Y_s, Ja, J0, J1, JA, val, nequilibrium, nworks):
    t0 = time.time()
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    ju = Ja * val
    ku = JA * val
    for i in range(nequilibrium):
        if ju > 3:
            randvaln = initdist(latt, X_s, Y_s, ku)
        else:
            randvaln = functions.NormalrandNN(2, 4, Y_s, X_s)
        randvals = np.random.rand(2, 4, Y_s, X_s)
        Etot = update3(latt, randvaln, randvals, X_s, Y_s, Ja, J0, J1, JA, val)
    for i in range(nworks):
        if ju > 3:
            randvaln = initdist(latt, X_s, Y_s, ku)
        else:
            randvaln = functions.NormalrandNN(2, 4, Y_s, X_s)
        randvals = np.random.rand(2, 4, Y_s, X_s)
        Etot = update3(latt, randvaln, randvals, X_s, Y_s, Ja, J0, J1, JA, val)
        Ew[i] = Etot
        Nw[i] = functions.Average(latt[0,0,2]), functions.Average(latt[0,1,2]), functions.Average(latt[0,2,2]), functions.Average(latt[0,3,2]),\
                functions.Average(latt[1,0,2]), functions.Average(latt[1,1,2]), functions.Average(latt[1,2,2]), functions.Average(latt[1,3,2])
    t = time.time() - t0
    return t, Nw, Ew

@njit
def update3(latt, randvaln, randvals, X_s, Y_s, Ja, J0, J1, JA, val):
    nn_sum = 0
    nn_p = 0
    for l in range(2):
        for k in range(4):
            for j in range(Y_s):
                for i in range(X_s):
                    lo = 1 - l
                    k1 = 3 - k
                    k2 = (5 - k) if k > 1 else (1 - k)
                    k3 = (2 - k) if k%2 == 0 else (4 - k)
                    ipp = (i + 1) if (i + 1) < X_s else 0
                    inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
                    jpp = (j + 1) if (j + 1) < Y_s else 0
                    jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
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

                    if l == 0:
                        if k == 0:
                            i_1 = i
                            j_2 = jpp
                            x_0 = i
                            x_1 = i
                            x_2 = ipp
                            y_0 = j
                            y_1 = jpp
                            y_2 = jpp
                        elif k == 1:
                            i_1 = i
                            j_2 = j
                            x_0 = i
                            x_1 = i
                            x_2 = ipp
                            y_0 = jnn
                            y_1 = j
                            y_2 = j
                        elif k == 2:
                            i_1 = inn
                            j_2 = j
                            x_0 = inn
                            x_1 = inn
                            x_2 = i
                            y_0 = jnn
                            y_1 = j
                            y_2 = j
                        else:
                            i_1 = inn
                            j_2 = jpp
                            x_0 = inn
                            x_1 = inn
                            x_2 = i
                            y_0 = j
                            y_1 = jpp
                            y_2 = jpp
                    else:
                        if k == 0:
                            i_1 = ipp
                            j_2 = j
                            x_0 = ipp
                            x_1 = ipp
                            x_2 = i
                            y_0 = jpp
                            y_1 = j
                            y_2 = j
                        elif k == 1:
                            i_1 = ipp
                            j_2 = jnn
                            x_0 = ipp
                            x_1 = ipp
                            x_2 = i
                            y_0 = j
                            y_1 = jnn
                            y_2 = jnn
                        elif k == 2:
                            i_1 = i
                            j_2 = jnn
                            x_0 = i
                            x_1 = i
                            x_2 = inn
                            y_0 = j
                            y_1 = jnn
                            y_2 = jnn
                        else:
                            i_1 = i
                            j_2 = j
                            x_0 = i
                            x_1 = i
                            x_2 = inn
                            y_0 = jpp
                            y_1 = j
                            y_2 = j

                    energy0 = ( latt[l,k,0,j,i] * ( -Ja * ( latt[l,k1,0,j,x_ipp] + latt[l,k1,0,j,x_inn] +
                                                            latt[l,k2,0,y_jpp,i] + latt[l,k2,0,y_jnn,i] +
                                                            latt[l,k3,0,y_jnn,x_inn] + latt[l,k3,0,y_jpp,x_ipp] ) -
                                                     J0 * ( latt[lo,k,0,j,i] + latt[lo,k1,0,j,i_1] + latt[lo,k2,0,j_2,i] ) -
                                                     J1 * ( latt[lo,k3,0,y_0,x_0] + latt[lo,k3,0,y_1,x_1] + latt[lo,k3,0,y_2,x_2] ) ) +
                                latt[l,k,1,j,i] * ( -Ja * ( latt[l,k1,1,j,x_ipp] + latt[l,k1,1,j,x_inn] +
                                                            latt[l,k2,1,y_jpp,i] + latt[l,k2,1,y_jnn,i] +
                                                            latt[l,k3,1,y_jnn,x_inn] + latt[l,k3,1,y_jpp,x_ipp] ) -
                                                     J0 * ( latt[lo,k,1,j,i] + latt[lo,k1,1,j,i_1] + latt[lo,k2,1,j_2,i] ) -
                                                     J1 * ( latt[lo,k3,1,y_0,x_0] + latt[lo,k3,1,y_1,x_1] + latt[lo,k3,1,y_2,x_2] ) ) +
                                latt[l,k,2,j,i] * ( -Ja * ( latt[l,k1,2,j,x_ipp] + latt[l,k1,2,j,x_inn] +
                                                            latt[l,k2,2,y_jpp,i] + latt[l,k2,2,y_jnn,i] +
                                                            latt[l,k3,2,y_jnn,x_inn] + latt[l,k3,2,y_jpp,x_ipp] ) -
                                                     J0 * ( latt[lo,k,2,j,i] + latt[lo,k1,2,j,i_1] + latt[lo,k2,2,j_2,i] ) -
                                                     J1 * ( latt[lo,k3,2,y_0,x_0] + latt[lo,k3,2,y_1,x_1] + latt[lo,k3,2,y_2,x_2] ) ) )
                    ez =  -JA * latt[l,k,2,j,i] ** 2
                    Erandn = ( randvaln[l,k,0,j,i] * ( -Ja * ( latt[l,k1,0,j,x_ipp] + latt[l,k1,0,j,x_inn] +
                                                               latt[l,k2,0,y_jpp,i] + latt[l,k2,0,y_jnn,i] +
                                                               latt[l,k3,0,y_jnn,x_inn] + latt[l,k3,0,y_jpp,x_ipp] ) -
                                                        J0 * ( latt[lo,k,0,j,i] + latt[lo,k1,0,j,i_1] + latt[lo,k2,0,j_2,i] ) -
                                                        J1 * ( latt[lo,k3,0,y_0,x_0] + latt[lo,k3,0,y_1,x_1] + latt[lo,k3,0,y_2,x_2] ) ) +
                               randvaln[l,k,1,j,i] * ( -Ja * ( latt[l,k1,1,j,x_ipp] + latt[l,k1,1,j,x_inn] +
                                                               latt[l,k2,1,y_jpp,i] + latt[l,k2,1,y_jnn,i] +
                                                               latt[l,k3,1,y_jnn,x_inn] + latt[l,k3,1,y_jpp,x_ipp] ) -
                                                        J0 * ( latt[lo,k,1,j,i] + latt[lo,k1,1,j,i_1] + latt[lo,k2,1,j_2,i] ) -
                                                        J1 * ( latt[lo,k3,1,y_0,x_0] + latt[lo,k3,1,y_1,x_1] + latt[lo,k3,1,y_2,x_2] ) ) +
                               randvaln[l,k,2,j,i] * ( -Ja * ( latt[l,k1,2,j,x_ipp] + latt[l,k1,2,j,x_inn] +
                                                               latt[l,k2,2,y_jpp,i] + latt[l,k2,2,y_jnn,i] +
                                                               latt[l,k3,2,y_jnn,x_inn] + latt[l,k3,2,y_jpp,x_ipp] ) -
                                                        J0 * ( latt[lo,k,2,j,i] + latt[lo,k1,2,j,i_1] + latt[lo,k2,2,j_2,i] ) -
                                                        J1 * ( latt[lo,k3,2,y_0,x_0] + latt[lo,k3,2,y_1,x_1] + latt[lo,k3,2,y_2,x_2] ) ) -
                               JA * randvaln[l,k,2,j,i] ** 2 )
                    Eold = ez + energy0
                    Eflip = ez - energy0
                    arrE = np.array([Eflip, Erandn, Eold])
                    Esort = np.argsort(arrE)
                    if val == 0:
                        if Esort[0] == 0:
                            latt[l,k,:,j,i] *= -1
                        elif Esort[0] == 1:
                            latt[l,k,:,j,i] = randvaln[l,k,:,j,i]
                    else:
                        if Esort[0] == 0:
                            latt[l,k,:,j,i] *= -1
                        elif Esort[0] == 1:
                            latt[l,k,:,j,i] = randvaln[l,k,:,j,i]
                        else:
                            if Esort[1] == 0:
                                if randvals[l,k,j,i] < np.exp( 2.0 * val * energy0 ):
                                    latt[l,k,:,j,i] *= -1
                            elif Esort[1] == 1:
                                DeltaE = Eold - Erandn
                                if randvals[l,k,j,i] < np.exp( val * DeltaE ):
                                    latt[l,k,:,j,i] = randvaln[l,k,:,j,i]

                    nn_sum += energy0
                    nn_p += ez
    return ( nn_p + nn_sum / 2.0 )
