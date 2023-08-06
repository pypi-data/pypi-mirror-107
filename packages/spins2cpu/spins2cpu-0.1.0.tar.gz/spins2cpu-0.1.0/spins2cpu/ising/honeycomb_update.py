import time
import numpy as np
from numba import njit
from spins2cpu import functions

def looping(latt, X_s, Y_s, Ja, val, nequilibrium):
    t0 = time.time()
    for i in range(nequilibrium):
        cluster(latt, X_s, Y_s, Ja, val)
    t = time.time() - t0
    return t, functions.Average(latt[0]), functions.Average(latt[1])

@njit
def cluster(latt, X_s, Y_s, Ja, val):
    l = np.random.randint(0, 2)
    k = np.random.randint(0, 4)
    j = np.random.randint(0, Y_s)
    i = np.random.randint(0, X_s)
    P_add = 1 - np.exp( 2 * val * -abs(Ja) )
    lable = np.ones((2, 4, Y_s, X_s)).astype(np.int8)
    stack = [(l,k,j,i)]
    lable[l,k,j,i] = 0
    while len(stack) > 0:
        current = stack.pop()
        sign = latt[current]
        l, k, j, i = current
        lo = 1 - l
        k1 = 3 - k
        k2 = (5 - k) if k > 1 else (1 - k)
        jpp = (j + 1) if (j + 1) < Y_s else 0
        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
        ipp = (i + 1) if (i + 1) < X_s else 0
        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
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

        neighbor_0 = (lo, k, j, i)
        neighbor_1 = (lo, k1, j, i_1)
        neighbor_2 = (lo, k2, j_2, i)

        latt[current] *= -1
        if Ja > 0:
            if latt[neighbor_0] == sign and lable[neighbor_0] and np.random.rand() < P_add:
                stack.append(neighbor_0)
                lable[neighbor_0] = 0
            if latt[neighbor_1] == sign and lable[neighbor_1] and np.random.rand() < P_add:
                stack.append(neighbor_1)
                lable[neighbor_1] = 0
            if latt[neighbor_2] == sign and lable[neighbor_2] and np.random.rand() < P_add:
                stack.append(neighbor_2)
                lable[neighbor_2] = 0
        else:
            if latt[neighbor_0] == -sign and lable[neighbor_0] and np.random.rand() < P_add:
                stack.append(neighbor_0)
                lable[neighbor_0] = 0
            if latt[neighbor_1] == -sign and lable[neighbor_1] and np.random.rand() < P_add:
                stack.append(neighbor_1)
                lable[neighbor_1] = 0
            if latt[neighbor_2] == -sign and lable[neighbor_2] and np.random.rand() < P_add:
                stack.append(neighbor_2)
                lable[neighbor_2] = 0

def iteration(latt, X_s, Y_s, Ja, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 2))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update(latt[0,0], latt[0,1], latt[0,2], latt[0,3], latt[1,0], latt[1,1], latt[1,2], latt[1,3], X_s, Y_s, Ja, val)
    for i in range(nworks):
        E0 = update(latt[0,0], latt[0,1], latt[0,2], latt[0,3], latt[1,0], latt[1,1], latt[1,2], latt[1,3], X_s, Y_s, Ja, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[0]), functions.Average(latt[1])
    t = time.time() - t0
    return t, Nw, Ew

def update(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, val):
    # 0
    M0 = ij(latt_0_0, latt_1_0, latt_1_3, latt_1_1, 0, X_s, Y_s, Ja, val)
    # 4
    N0 = ij(latt_1_0, latt_0_0, latt_0_3, latt_0_1, 4, X_s, Y_s, Ja, val)
    # 1
    M1 = ij(latt_0_1, latt_1_1, latt_1_2, latt_1_0, 1, X_s, Y_s, Ja, val)
    # 5
    N1 = ij(latt_1_1, latt_0_1, latt_0_2, latt_0_0, 5, X_s, Y_s, Ja, val)
    # 2
    M2 = ij(latt_0_2, latt_1_2, latt_1_1, latt_1_3, 2, X_s, Y_s, Ja, val)
    # 6
    N2 = ij(latt_1_2, latt_0_2, latt_0_1, latt_0_3, 6, X_s, Y_s, Ja, val)
    # 3
    M3 = ij(latt_0_3, latt_1_3, latt_1_0, latt_1_2, 3, X_s, Y_s, Ja, val)
    #7
    N3 = ij(latt_1_3, latt_0_3, latt_0_0, latt_0_2, 7, X_s, Y_s, Ja, val)
    return (M0 + M1 + M2 + M3 + N0 + N1 + N2 + N3)

def ij(latt_0_0, latt_1_0, latt_1_1, latt_1_2, color, X_s, Y_s, Ja, val):
    if color == 0:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = np.roll(latt_1_2, -1, axis=0)
    elif color == 1:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = latt_1_2
    elif color == 2:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, 1, axis=1)
        lattice_2 = latt_1_2
    elif color == 3:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, 1, axis=1)
        lattice_2 = np.roll(latt_1_2, -1, axis=0)
    elif color == 4:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, -1, axis=1)
        lattice_2 = latt_1_2
    elif color == 5:
        lattice_0 = latt_1_0
        lattice_1 = np.roll(latt_1_1, -1, axis=1)
        lattice_2 = np.roll(latt_1_2, 1, axis=0)
    elif color == 6:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = np.roll(latt_1_2, 1, axis=0)
    else:
        lattice_0 = latt_1_0
        lattice_1 = latt_1_1
        lattice_2 = latt_1_2

    nn_sum = -Ja * ( lattice_0 + lattice_1 + lattice_2 ) * latt_0_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0_0[:] = latt_0_0 * move
    return nn_sum

def looping2(latt, X_s, Y_s, Ja, Jb, val, nequilibrium):
    t0 = time.time()
    for i in range(nequilibrium):
        cluster2(latt, X_s, Y_s, Ja, Jb, val)
    t = time.time() - t0
    return t, functions.Average(latt[0]), functions.Average(latt[1])

@njit
def cluster2(latt, X_s, Y_s, Ja, Jb, val):
    l = np.random.randint(0, 2)
    k = np.random.randint(0, 4)
    j = np.random.randint(0, Y_s)
    i = np.random.randint(0, X_s)
    P_adda = 1 - np.exp( 2 * val * -abs(Ja) )
    P_addb = 1 - np.exp( 2 * val * -abs(Jb) )
    lable = np.ones((2, 4, Y_s, X_s)).astype(np.int8)
    stack = [(l,k,j,i)]
    lable[l,k,j,i] = 0
    while len(stack) > 0:
        current = stack.pop()
        sign = latt[current]
        l, k, j, i = current
        lo = 1 - l
        k1 = 3 - k
        k2 = (5 - k) if k > 1 else (1 - k)
        k3 = (2 - k) if k%2 == 0 else (4 - k)
        jpp = (j + 1) if (j + 1) < Y_s else 0
        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
        ipp = (i + 1) if (i + 1) < X_s else 0
        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
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

        neighbor_0 = (lo, k, j, i)
        neighbor_1 = (lo, k1, j, i_1)
        neighbor_2 = (lo, k2, j_2, i)

        latt[current] *= -1
        if Ja > 0:
            if latt[neighbor_0] == sign and lable[neighbor_0] and np.random.rand() < P_adda:
                stack.append(neighbor_0)
                lable[neighbor_0] = 0
            if latt[neighbor_1] == sign and lable[neighbor_1] and np.random.rand() < P_adda:
                stack.append(neighbor_1)
                lable[neighbor_1] = 0
            if latt[neighbor_2] == sign and lable[neighbor_2] and np.random.rand() < P_adda:
                stack.append(neighbor_2)
                lable[neighbor_2] = 0
        else:
            if latt[neighbor_0] == -sign and lable[neighbor_0] and np.random.rand() < P_adda:
                stack.append(neighbor_0)
                lable[neighbor_0] = 0
            if latt[neighbor_1] == -sign and lable[neighbor_1] and np.random.rand() < P_adda:
                stack.append(neighbor_1)
                lable[neighbor_1] = 0
            if latt[neighbor_2] == -sign and lable[neighbor_2] and np.random.rand() < P_adda:
                stack.append(neighbor_2)
                lable[neighbor_2] = 0

        if abs(Jb) > abs(Ja * 0.1):
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

            neighbor_lef = (l, k1, j, x_inn)
            neighbor_rig = (l, k1, j, x_ipp)
            neighbor_up1 = (l, k2, y_jnn, i)
            neighbor_do1 = (l, k2, y_jpp, i)
            neighbor_up2 = (l, k3, y_jnn, x_inn)
            neighbor_do2 = (l, k3, y_jpp, x_ipp)
            if Jb > 0:
                if latt[neighbor_lef] == sign and lable[neighbor_lef] and np.random.rand() < P_addb:
                    stack.append(neighbor_lef)
                    lable[neighbor_lef] = 0
                if latt[neighbor_rig] == sign and lable[neighbor_rig] and np.random.rand() < P_addb:
                    stack.append(neighbor_rig)
                    lable[neighbor_rig] = 0
                if latt[neighbor_up1] == sign and lable[neighbor_up1] and np.random.rand() < P_addb:
                    stack.append(neighbor_up1)
                    lable[neighbor_up1] = 0
                if latt[neighbor_up2] == sign and lable[neighbor_up2] and np.random.rand() < P_addb:
                    stack.append(neighbor_up2)
                    lable[neighbor_up2] = 0
                if latt[neighbor_do1] == sign and lable[neighbor_do1] and np.random.rand() < P_addb:
                    stack.append(neighbor_do1)
                    lable[neighbor_do1] = 0
                if latt[neighbor_do2] == sign and lable[neighbor_do2] and np.random.rand() < P_addb:
                    stack.append(neighbor_do2)
                    lable[neighbor_do2] = 0
            else:
                if latt[neighbor_lef] == -sign and lable[neighbor_lef] and np.random.rand() < P_addb:
                    stack.append(neighbor_lef)
                    lable[neighbor_lef] = 0
                if latt[neighbor_rig] == -sign and lable[neighbor_rig] and np.random.rand() < P_addb:
                    stack.append(neighbor_rig)
                    lable[neighbor_rig] = 0
                if latt[neighbor_up1] == -sign and lable[neighbor_up1] and np.random.rand() < P_addb:
                    stack.append(neighbor_up1)
                    lable[neighbor_up1] = 0
                if latt[neighbor_up2] == -sign and lable[neighbor_up2] and np.random.rand() < P_addb:
                    stack.append(neighbor_up2)
                    lable[neighbor_up2] = 0
                if latt[neighbor_do1] == -sign and lable[neighbor_do1] and np.random.rand() < P_addb:
                    stack.append(neighbor_do1)
                    lable[neighbor_do1] = 0
                if latt[neighbor_do2] == -sign and lable[neighbor_do2] and np.random.rand() < P_addb:
                    stack.append(neighbor_do2)
                    lable[neighbor_do2] = 0

def iteration2(latt, X_s, Y_s, Ja, Jb, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 2))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update2(latt[0,0], latt[0,1], latt[0,2], latt[0,3], latt[1,0], latt[1,1], latt[1,2], latt[1,3], X_s, Y_s, Ja, Jb, val)
    for i in range(nworks):
        E0 = update2(latt[0,0], latt[0,1], latt[0,2], latt[0,3], latt[1,0], latt[1,1], latt[1,2], latt[1,3], X_s, Y_s, Ja, Jb, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[0]), functions.Average(latt[1])
    t = time.time() - t0
    return t, Nw, Ew

def update2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, Jb, val):
    # 0
    M0 = ij2(latt_0_0, latt_0_3, latt_0_1, latt_0_2, latt_1_0, latt_1_3, latt_1_1, 0, X_s, Y_s, Ja, Jb, val)
    # 4
    N0 = ij2(latt_1_0, latt_1_3, latt_1_1, latt_1_2, latt_0_0, latt_0_3, latt_0_1, 4, X_s, Y_s, Ja, Jb, val)
    # 1
    M1 = ij2(latt_0_1, latt_0_2, latt_0_0, latt_0_3, latt_1_1, latt_1_2, latt_1_0, 1, X_s, Y_s, Ja, Jb, val)
    # 5
    N1 = ij2(latt_1_1, latt_1_2, latt_1_0, latt_1_3, latt_0_1, latt_0_2, latt_0_0, 5, X_s, Y_s, Ja, Jb, val)
    # 2
    M2 = ij2(latt_0_2, latt_0_1, latt_0_3, latt_0_0, latt_1_2, latt_1_1, latt_1_3, 2, X_s, Y_s, Ja, Jb, val)
    # 6
    N2 = ij2(latt_1_2, latt_1_1, latt_1_3, latt_1_0, latt_0_2, latt_0_1, latt_0_3, 6, X_s, Y_s, Ja, Jb, val)
    # 3
    M3 = ij2(latt_0_3, latt_0_0, latt_0_2, latt_0_1, latt_1_3, latt_1_0, latt_1_2, 3, X_s, Y_s, Ja, Jb, val)
    #7
    N3 = ij2(latt_1_3, latt_1_0, latt_1_2, latt_1_1, latt_0_3, latt_0_0, latt_0_2, 7, X_s, Y_s, Ja, Jb, val)
    return (M0 + M1 + M2 + M3 + N0 + N1 + N2 + N3)

def ij2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, color, X_s, Y_s, Ja, Jb, val):
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

    nn_sum = ( -Ja * ( lattice_0 + lattice_1 + lattice_2 ) - Jb * ( lattice0_0 + lattice0_1 + lattice0_2 + lattice1_0 + lattice1_1 + lattice1_2 ) ) * latt_0_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0_0[:] = latt_0_0 * move
    return nn_sum

def looping3(latt, X_s, Y_s, Ja, Jb, Jc, val, nequilibrium):
    t0 = time.time()
    for i in range(nequilibrium):
        cluster3(latt, X_s, Y_s, Ja, Jb, Jc, val)
    t = time.time() - t0
    return t, functions.Average(latt[0]), functions.Average(latt[1])

@njit
def cluster3(latt, X_s, Y_s, Ja, Jb, Jc, val):
    l = np.random.randint(0, 2)
    k = np.random.randint(0, 4)
    j = np.random.randint(0, Y_s)
    i = np.random.randint(0, X_s)
    P_adda = 1 - np.exp( 2 * val * -abs(Ja) )
    P_addb = 1 - np.exp( 2 * val * -abs(Jb) )
    P_addc = 1 - np.exp( 2 * val * -abs(Jc) )
    lable = np.ones((2, 4, Y_s, X_s)).astype(np.int8)
    stack = [(l,k,j,i)]
    lable[l,k,j,i] = 0
    while len(stack) > 0:
        current = stack.pop()
        sign = latt[current]
        l, k, j, i = current
        lo = 1 - l
        k1 = 3 - k
        k2 = (5 - k) if k > 1 else (1 - k)
        k3 = (2 - k) if k%2 == 0 else (4 - k)
        jpp = (j + 1) if (j + 1) < Y_s else 0
        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
        ipp = (i + 1) if (i + 1) < X_s else 0
        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
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

        neighbor_0 = (lo, k, j, i)
        neighbor_1 = (lo, k1, j, i_1)
        neighbor_2 = (lo, k2, j_2, i)

        latt[current] *= -1
        if Ja > 0:
            if latt[neighbor_0] == sign and lable[neighbor_0] and np.random.rand() < P_adda:
                stack.append(neighbor_0)
                lable[neighbor_0] = 0
            if latt[neighbor_1] == sign and lable[neighbor_1] and np.random.rand() < P_adda:
                stack.append(neighbor_1)
                lable[neighbor_1] = 0
            if latt[neighbor_2] == sign and lable[neighbor_2] and np.random.rand() < P_adda:
                stack.append(neighbor_2)
                lable[neighbor_2] = 0
        else:
            if latt[neighbor_0] == -sign and lable[neighbor_0] and np.random.rand() < P_adda:
                stack.append(neighbor_0)
                lable[neighbor_0] = 0
            if latt[neighbor_1] == -sign and lable[neighbor_1] and np.random.rand() < P_adda:
                stack.append(neighbor_1)
                lable[neighbor_1] = 0
            if latt[neighbor_2] == -sign and lable[neighbor_2] and np.random.rand() < P_adda:
                stack.append(neighbor_2)
                lable[neighbor_2] = 0

        if abs(Jb) > abs(Ja * 0.1):
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

            neighbor_lef = (l, k1, j, x_inn)
            neighbor_rig = (l, k1, j, x_ipp)
            neighbor_up1 = (l, k2, y_jnn, i)
            neighbor_do1 = (l, k2, y_jpp, i)
            neighbor_up2 = (l, k3, y_jnn, x_inn)
            neighbor_do2 = (l, k3, y_jpp, x_ipp)
            if Jb > 0:
                if latt[neighbor_lef] == sign and lable[neighbor_lef] and np.random.rand() < P_addb:
                    stack.append(neighbor_lef)
                    lable[neighbor_lef] = 0
                if latt[neighbor_rig] == sign and lable[neighbor_rig] and np.random.rand() < P_addb:
                    stack.append(neighbor_rig)
                    lable[neighbor_rig] = 0
                if latt[neighbor_up1] == sign and lable[neighbor_up1] and np.random.rand() < P_addb:
                    stack.append(neighbor_up1)
                    lable[neighbor_up1] = 0
                if latt[neighbor_up2] == sign and lable[neighbor_up2] and np.random.rand() < P_addb:
                    stack.append(neighbor_up2)
                    lable[neighbor_up2] = 0
                if latt[neighbor_do1] == sign and lable[neighbor_do1] and np.random.rand() < P_addb:
                    stack.append(neighbor_do1)
                    lable[neighbor_do1] = 0
                if latt[neighbor_do2] == sign and lable[neighbor_do2] and np.random.rand() < P_addb:
                    stack.append(neighbor_do2)
                    lable[neighbor_do2] = 0
            else:
                if latt[neighbor_lef] == -sign and lable[neighbor_lef] and np.random.rand() < P_addb:
                    stack.append(neighbor_lef)
                    lable[neighbor_lef] = 0
                if latt[neighbor_rig] == -sign and lable[neighbor_rig] and np.random.rand() < P_addb:
                    stack.append(neighbor_rig)
                    lable[neighbor_rig] = 0
                if latt[neighbor_up1] == -sign and lable[neighbor_up1] and np.random.rand() < P_addb:
                    stack.append(neighbor_up1)
                    lable[neighbor_up1] = 0
                if latt[neighbor_up2] == -sign and lable[neighbor_up2] and np.random.rand() < P_addb:
                    stack.append(neighbor_up2)
                    lable[neighbor_up2] = 0
                if latt[neighbor_do1] == -sign and lable[neighbor_do1] and np.random.rand() < P_addb:
                    stack.append(neighbor_do1)
                    lable[neighbor_do1] = 0
                if latt[neighbor_do2] == -sign and lable[neighbor_do2] and np.random.rand() < P_addb:
                    stack.append(neighbor_do2)
                    lable[neighbor_do2] = 0

        if abs(Jc) > abs(Ja * 0.1):
            neighbor_a = (lo, k3, y_0, x_0)
            neighbor_b = (lo, k3, y_1, x_1)
            neighbor_c = (lo, k3, y_2, x_2)
            if Jc > 0:
                if latt[neighbor_a] == sign and lable[neighbor_a] and np.random.rand() < P_addc:
                    stack.append(neighbor_a)
                    lable[neighbor_a] = 0
                if latt[neighbor_b] == sign and lable[neighbor_b] and np.random.rand() < P_addc:
                    stack.append(neighbor_b)
                    lable[neighbor_b] = 0
                if latt[neighbor_c] == sign and lable[neighbor_c] and np.random.rand() < P_addc:
                    stack.append(neighbor_c)
                    lable[neighbor_c] = 0
            else:
                if latt[neighbor_a] == -sign and lable[neighbor_a] and np.random.rand() < P_addc:
                    stack.append(neighbor_a)
                    lable[neighbor_a] = 0
                if latt[neighbor_b] == -sign and lable[neighbor_b] and np.random.rand() < P_addc:
                    stack.append(neighbor_b)
                    lable[neighbor_b] = 0
                if latt[neighbor_c] == -sign and lable[neighbor_c] and np.random.rand() < P_addc:
                    stack.append(neighbor_c)
                    lable[neighbor_c] = 0

def iteration3(latt, X_s, Y_s, Ja, Jb, Jc, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 2))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update3(latt[0,0], latt[0,1], latt[0,2], latt[0,3], latt[1,0], latt[1,1], latt[1,2], latt[1,3], X_s, Y_s, Ja, Jb, Jc, val)
    for i in range(nworks):
        E0 = update3(latt[0,0], latt[0,1], latt[0,2], latt[0,3], latt[1,0], latt[1,1], latt[1,2], latt[1,3], X_s, Y_s, Ja, Jb, Jc, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[0]), functions.Average(latt[1])
    t = time.time() - t0
    return t, Nw, Ew

def update3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, X_s, Y_s, Ja, Jb, Jc, val):
    # 0
    M0 = ij3(latt_0_0, latt_0_3, latt_0_1, latt_0_2, latt_1_0, latt_1_3, latt_1_1, latt_1_2, 0, X_s, Y_s, Ja, Jb, Jc, val)
    # 4
    N0 = ij3(latt_1_0, latt_1_3, latt_1_1, latt_1_2, latt_0_0, latt_0_3, latt_0_1, latt_0_2, 4, X_s, Y_s, Ja, Jb, Jc, val)
    # 1
    M1 = ij3(latt_0_1, latt_0_2, latt_0_0, latt_0_3, latt_1_1, latt_1_2, latt_1_0, latt_1_3, 1, X_s, Y_s, Ja, Jb, Jc, val)
    # 5
    N1 = ij3(latt_1_1, latt_1_2, latt_1_0, latt_1_3, latt_0_1, latt_0_2, latt_0_0, latt_0_3, 5, X_s, Y_s, Ja, Jb, Jc, val)
    # 2
    M2 = ij3(latt_0_2, latt_0_1, latt_0_3, latt_0_0, latt_1_2, latt_1_1, latt_1_3, latt_1_0, 2, X_s, Y_s, Ja, Jb, Jc, val)
    # 6
    N2 = ij3(latt_1_2, latt_1_1, latt_1_3, latt_1_0, latt_0_2, latt_0_1, latt_0_3, latt_0_0, 6, X_s, Y_s, Ja, Jb, Jc, val)
    # 3
    M3 = ij3(latt_0_3, latt_0_0, latt_0_2, latt_0_1, latt_1_3, latt_1_0, latt_1_2, latt_1_1, 3, X_s, Y_s, Ja, Jb, Jc, val)
    #7
    N3 = ij3(latt_1_3, latt_1_0, latt_1_2, latt_1_1, latt_0_3, latt_0_0, latt_0_2, latt_0_1, 7, X_s, Y_s, Ja, Jb, Jc, val)
    return (M0 + M1 + M2 + M3 + N0 + N1 + N2 + N3)


def ij3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3, color, X_s, Y_s, Ja, Jb, Jc, val):
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

    nn_sum = ( -Ja * ( lattice_0 + lattice_1 + lattice_2 ) - Jb * ( lattice0_0 + lattice0_1 + lattice0_2 + lattice1_0 + lattice1_1 + lattice1_2 ) -
                Jc * ( lattice0 + lattice1 + lattice2 ) ) * latt_0_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0_0[:] = latt_0_0 * move
    return nn_sum
