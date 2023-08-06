import time
import numpy as np
from spins2cpu import functions

def iteration2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
               X_s, Y_s, Ja, J0, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, J0, val)
    for i in range(nworks):
        E0 = update2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, J0, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt_0_0), functions.Average(latt_0_1), functions.Average(latt_0_2), functions.Average(latt_0_3),\
                functions.Average(latt_1_0), functions.Average(latt_1_1), functions.Average(latt_1_2), functions.Average(latt_1_3)
    t = time.time() - t0
    return t, Nw, Ew

def update2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, J0, val):
    # 0
    M0 = ij2(latt_0_0, latt_0_3, latt_0_1, latt_0_2, latt_1_0, latt_1_3, latt_1_1, 0, X_s, Y_s, Ja, J0, val)
    # 1
    M1 = ij2(latt_0_1, latt_0_2, latt_0_0, latt_0_3, latt_1_1, latt_1_2, latt_1_0, 1, X_s, Y_s, Ja, J0, val)
    # 2
    M2 = ij2(latt_0_2, latt_0_1, latt_0_3, latt_0_0, latt_1_2, latt_1_1, latt_1_3, 2, X_s, Y_s, Ja, J0, val)
    # 3
    M3 = ij2(latt_0_3, latt_0_0, latt_0_2, latt_0_1, latt_1_3, latt_1_0, latt_1_2, 3, X_s, Y_s, Ja, J0, val)
    # 4
    N0 = ij2(latt_1_0, latt_1_3, latt_1_1, latt_1_2, latt_0_0, latt_0_3, latt_0_1, 4, X_s, Y_s, Ja, J0, val)
    # 5
    N1 = ij2(latt_1_1, latt_1_2, latt_1_0, latt_1_3, latt_0_1, latt_0_2, latt_0_0, 5, X_s, Y_s, Ja, J0, val)
    # 6
    N2 = ij2(latt_1_2, latt_1_1, latt_1_3, latt_1_0, latt_0_2, latt_0_1, latt_0_3, 6, X_s, Y_s, Ja, J0, val)
    #7
    N3 = ij2(latt_1_3, latt_1_0, latt_1_2, latt_1_1, latt_0_3, latt_0_0, latt_0_2, 7, X_s, Y_s, Ja, J0, val)
    return (M0 + M1 + M2 + M3 + N0 + N1 + N2 + N3)

def ij2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, color, X_s, Y_s, Ja, J0, val):
    if color == 0:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = np.roll(latt_1_2, -1, axis=0)
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = latt_0_2
        lattice0_2 = latt_0_3
        lattice1_0 = latt_0_1
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(np.roll(latt_0_3, -1,axis=1), -1, axis=0)
    elif color == 1:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = latt_1_2
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(latt_0_3, 1, axis=0)
        lattice1_0 = latt_0_1
        lattice1_1 = latt_0_2
        lattice1_2 = np.roll(latt_0_3, -1, axis=1)
    elif color == 2:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, 1, axis=1)
        lattice_2 = latt_1_2
        lattice0_0 = latt_0_1
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(np.roll(latt_0_3, 1, axis=1), 1, axis=0)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = latt_0_2
        lattice1_2 = latt_0_3
    elif color == 3:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, 1, axis=1)
        lattice_2 = np.roll(latt_1_2, -1, axis=0)
        lattice0_0 = latt_0_1
        lattice0_1 = latt_0_2
        lattice0_2 = np.roll(latt_0_3, 1, axis=1)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(latt_0_3, -1, axis=0)
    elif color == 4:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, -1, axis=1)
        lattice_2 = latt_1_2
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = latt_0_2
        lattice0_2 = latt_0_3
        lattice1_0 = latt_0_1
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(np.roll(latt_0_3, -1,axis=1), -1, axis=0)
    elif color == 5:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, -1, axis=1)
        lattice_2 = np.roll(latt_1_2, 1, axis=0)
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(latt_0_3, 1, axis=0)
        lattice1_0 = latt_0_1
        lattice1_1 = latt_0_2
        lattice1_2 = np.roll(latt_0_3, -1, axis=1)
    elif color == 6:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = np.roll(latt_1_2, 1, axis=0)
        lattice0_0 = latt_0_1
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(np.roll(latt_0_3, 1, axis=1), 1, axis=0)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = latt_0_2
        lattice1_2 = latt_0_3
    else:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = latt_1_2
        lattice0_0 = latt_0_1
        lattice0_1 = latt_0_2
        lattice0_2 = np.roll(latt_0_3, 1, axis=1)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(latt_0_3, -1, axis=0)

    nn_sum = ( -J0 * ( lattice_0 + lattice_1 + lattice_2 ) - Ja * ( lattice0_0 + lattice0_1 + lattice0_2 + lattice1_0 + lattice1_1 + lattice1_2 ) ) * latt_0_0
    if val == 0:
        acceptance = 2.0 * nn_sum
        move = np.where(acceptance > 0, -1, 1)
    else:
        randval = np.random.rand(Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0_0[:] = latt_0_0 * move
    return nn_sum

def iteration3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, J0, J1, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, J0, J1, val)
    for i in range(nworks):
        E0 = update3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, J0, J1, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt_0_0), functions.Average(latt_0_1), functions.Average(latt_0_2), functions.Average(latt_0_3),\
                functions.Average(latt_1_0), functions.Average(latt_1_1), functions.Average(latt_1_2), functions.Average(latt_1_3)
    t = time.time() - t0
    return t, Nw, Ew

def update3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, J0, J1, val):
    # 0
    M0 = ij3(latt_0_0, latt_0_3, latt_0_1, latt_0_2, latt_1_0, latt_1_3, latt_1_1, latt_1_2, 0, X_s, Y_s, Ja, J0, J1, val)
    # 1
    M1 = ij3(latt_0_1, latt_0_2, latt_0_0, latt_0_3, latt_1_1, latt_1_2, latt_1_0, latt_1_3, 1, X_s, Y_s, Ja, J0, J1, val)
    # 2
    M2 = ij3(latt_0_2, latt_0_1, latt_0_3, latt_0_0, latt_1_2, latt_1_1, latt_1_3, latt_1_0, 2, X_s, Y_s, Ja, J0, J1, val)
    # 3
    M3 = ij3(latt_0_3, latt_0_0, latt_0_2, latt_0_1, latt_1_3, latt_1_0, latt_1_2, latt_1_1, 3, X_s, Y_s, Ja, J0, J1, val)
    # 4
    N0 = ij3(latt_1_0, latt_1_3, latt_1_1, latt_1_2, latt_0_0, latt_0_3, latt_0_1, latt_0_2, 4, X_s, Y_s, Ja, J0, J1, val)
    # 5
    N1 = ij3(latt_1_1, latt_1_2, latt_1_0, latt_1_3, latt_0_1, latt_0_2, latt_0_0, latt_0_3, 5, X_s, Y_s, Ja, J0, J1, val)
    # 6
    N2 = ij3(latt_1_2, latt_1_1, latt_1_3, latt_1_0, latt_0_2, latt_0_1, latt_0_3, latt_0_0, 6, X_s, Y_s, Ja, J0, J1, val)
    #7
    N3 = ij3(latt_1_3, latt_1_0, latt_1_2, latt_1_1, latt_0_3, latt_0_0, latt_0_2, latt_0_1, 7, X_s, Y_s, Ja, J0, J1, val)
    return (M0 + M1 + M2 + M3 + N0 + N1 + N2 + N3)

def ij3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, color, X_s, Y_s, Ja, J0, J1, val):
    if color == 0:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = np.roll(latt_1_2, -1, axis=0)
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = latt_0_2
        lattice0_2 = latt_0_3
        lattice1_0 = latt_0_1
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(np.roll(latt_0_3, -1,axis=1), -1, axis=0)
        lattice0 = np.roll(np.roll(latt_1_3, -1, axis=1), -1, axis=0)
        lattice1 = latt_1_3
        lattice2 = np.roll(latt_1_3, -1, axis=0)
    elif color == 1:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = latt_1_2
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(latt_0_3, 1, axis=0)
        lattice1_0 = latt_0_1
        lattice1_1 = latt_0_2
        lattice1_2 = np.roll(latt_0_3, -1, axis=1)
        lattice0 = np.roll(latt_1_3, -1, axis=1)
        lattice1 = np.roll(latt_1_3, 1, axis=0)
        lattice2 = latt_1_3
    elif color == 2:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, 1, axis=1)
        lattice_2 = latt_1_2
        lattice0_0 = latt_0_1
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(np.roll(latt_0_3, 1, axis=1), 1, axis=0)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = latt_0_2
        lattice1_2 = latt_0_3
        lattice0 = latt_1_3
        lattice1 = np.roll(np.roll(latt_1_3, 1, axis=1), 1, axis=0)
        lattice2 = np.roll(latt_1_3, 1, axis=1)
    elif color == 3:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, 1, axis=1)
        lattice_2 = np.roll(latt_1_2, -1, axis=0)
        lattice0_0 = latt_0_1
        lattice0_1 = latt_0_2
        lattice0_2 = np.roll(latt_0_3, 1, axis=1)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(latt_0_3, -1, axis=0)
        lattice0 = np.roll(latt_1_3, -1, axis=0)
        lattice1 = np.roll(latt_1_3, 1, axis=1)
        lattice2 = np.roll(np.roll(latt_1_3, 1, axis=1), -1, axis=0)
    elif color == 4:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, -1, axis=1)
        lattice_2 = latt_1_2
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = latt_0_2
        lattice0_2 = latt_0_3
        lattice1_0 = latt_0_1
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(np.roll(latt_0_3, -1,axis=1), -1, axis=0)
        lattice0 = np.roll(latt_1_3, -1, axis=0)
        lattice1 = latt_1_3
        lattice2 = np.roll(np.roll(latt_1_3, -1, axis=1), -1, axis=0)
    elif color == 5:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, -1, axis=1)
        lattice_2 = np.roll(latt_1_2, 1, axis=0)
        lattice0_0 = np.roll(latt_0_1, -1, axis=1)
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(latt_0_3, 1, axis=0)
        lattice1_0 = latt_0_1
        lattice1_1 = latt_0_2
        lattice1_2 = np.roll(latt_0_3, -1, axis=1)
        lattice0 = np.roll(np.roll(latt_1_3, -1, axis=1), 1, axis=0)
        lattice1 = np.roll(latt_1_3, 1, axis=0)
        lattice2 = np.roll(latt_1_3, -1, axis=1)
    elif color == 6:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = np.roll(latt_1_2, 1, axis=0)
        lattice0_0 = latt_0_1
        lattice0_1 = np.roll(latt_0_2, 1, axis=0)
        lattice0_2 = np.roll(np.roll(latt_0_3, 1, axis=1), 1, axis=0)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = latt_0_2
        lattice1_2 = latt_0_3
        lattice0 = np.roll(latt_1_3, 1, axis=0)
        lattice1 = np.roll(np.roll(latt_1_3, 1, axis=1), 1, axis=0)
        lattice2 = latt_1_3
    else:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = latt_1_2
        lattice0_0 = latt_0_1
        lattice0_1 = latt_0_2
        lattice0_2 = np.roll(latt_0_3, 1, axis=1)
        lattice1_0 = np.roll(latt_0_1, 1, axis=1)
        lattice1_1 = np.roll(latt_0_2, -1, axis=0)
        lattice1_2 = np.roll(latt_0_3, -1, axis=0)
        lattice0 = latt_1_3
        lattice1 = np.roll(latt_1_3, 1, axis=1)
        lattice2 = np.roll(latt_1_3, -1, axis=0)

    nn_sum = ( -J0 * ( lattice_0 + lattice_1 + lattice_2 ) - Ja * ( lattice0_0 + lattice0_1 + lattice0_2 + lattice1_0 + lattice1_1 + lattice1_2 ) -
                J1 * ( lattice0 + lattice1 + lattice2 ) ) * latt_0_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0_0[:] = latt_0_0 * move
    return nn_sum
