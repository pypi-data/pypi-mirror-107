import time
import numpy as np
from numba import njit
from spins2cpu import functions

def looping(latt, X_s, Y_s, Ja, val, nequilibrium):
    t0 = time.time()
    for i in range(nequilibrium):
        cluster(latt, X_s, Y_s, Ja, val)
    t = time.time() - t0
    return t, functions.Average(latt[[0,2]]), functions.Average(latt[[1,3]])

@njit
def cluster(latt, X_s, Y_s, Ja, val):
    k = np.random.randint(0, 4)
    j = np.random.randint(0, Y_s)
    i = np.random.randint(0, X_s)
    P_add = 1 - np.exp( 2 * val * -abs(Ja) )
    lable = np.ones((4, Y_s, X_s)).astype(np.int8)
    stack = [(k,j,i)]
    lable[k,j,i] = 0
    while len(stack) > 0:
        current = stack.pop()
        sign = latt[current]
        k, j, i = current
        kx = 3 - k
        ky = (5 - k) if k > 1 else (1 - k)
        jpp = (j + 1) if (j + 1) < Y_s else 0
        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
        ipp = (i + 1) if (i + 1) < X_s else 0
        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
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

        neighbor_lef = (kx, j, x_inn)
        neighbor_rig = (kx, j, x_ipp)
        neighbor_up1 = (ky, y_jnn, i)
        neighbor_do1 = (ky, y_jpp, i)

        latt[current] *= -1
        if Ja > 0:
            if latt[neighbor_lef] == sign and lable[neighbor_lef] and np.random.rand() < P_add:
                stack.append(neighbor_lef)
                lable[neighbor_lef] = 0
            if latt[neighbor_rig] == sign and lable[neighbor_rig] and np.random.rand() < P_add:
                stack.append(neighbor_rig)
                lable[neighbor_rig] = 0
            if latt[neighbor_up1] == sign and lable[neighbor_up1] and np.random.rand() < P_add:
                stack.append(neighbor_up1)
                lable[neighbor_up1] = 0
            if latt[neighbor_do1] == sign and lable[neighbor_do1] and np.random.rand() < P_add:
                stack.append(neighbor_do1)
                lable[neighbor_do1] = 0
        else:
            if latt[neighbor_lef] == -sign and lable[neighbor_lef] and np.random.rand() < P_add:
                stack.append(neighbor_lef)
                lable[neighbor_lef] = 0
            if latt[neighbor_rig] == -sign and lable[neighbor_rig] and np.random.rand() < P_add:
                stack.append(neighbor_rig)
                lable[neighbor_rig] = 0
            if latt[neighbor_up1] == -sign and lable[neighbor_up1] and np.random.rand() < P_add:
                stack.append(neighbor_up1)
                lable[neighbor_up1] = 0
            if latt[neighbor_do1] == -sign and lable[neighbor_do1] and np.random.rand() < P_add:
                stack.append(neighbor_do1)
                lable[neighbor_do1] = 0

def iteration(latt, X_s, Y_s, Ja, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 2))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update(latt[0], latt[1], latt[2], latt[3], X_s, Y_s, Ja, val)
    for i in range(nworks):
        E0 = update(latt[0], latt[1], latt[2], latt[3], X_s, Y_s, Ja, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[[0,2]]), functions.Average(latt[[1,3]])
    t = time.time() - t0
    return t, Nw, Ew

def update(latt_0, latt_1, latt_2, latt_3, X_s, Y_s, Ja, val):
    # 0
    M0 = ij(latt_0, latt_3, latt_1, 0, X_s, Y_s, Ja, val)
    # 1
    M1 = ij(latt_1, latt_2, latt_0, 1, X_s, Y_s, Ja, val)
    # 2
    M2 = ij(latt_2, latt_1, latt_3, 2, X_s, Y_s, Ja, val)
    # 3
    M3 = ij(latt_3, latt_0, latt_2, 3, X_s, Y_s, Ja, val)
    return (M0 + M1 + M2 + M3)

def ij(latt_0, latt_1, latt_2, color, X_s, Y_s, Ja, val):
    if color == 0:
        lattice0_0 = np.roll(latt_1, -1, axis=1)
        lattice0_1 = latt_2
        lattice1_0 = latt_1
        lattice1_1 = np.roll(latt_2, -1, axis=0)
    elif color == 1:
        lattice0_0 = np.roll(latt_1, -1, axis=1)
        lattice0_1 = np.roll(latt_2, 1, axis=0)
        lattice1_0 = latt_1
        lattice1_1 = latt_2
    elif color == 2:
        lattice0_0 = latt_1
        lattice0_1 = np.roll(latt_2, 1, axis=0)
        lattice1_0 = np.roll(latt_1, 1, axis=1)
        lattice1_1 = latt_2
    else:
        lattice0_0 = latt_1
        lattice0_1 = latt_2
        lattice1_0 = np.roll(latt_1, 1, axis=1)
        lattice1_1 = np.roll(latt_2, -1, axis=0)

    nn_sum = -Ja * ( lattice0_0 + lattice0_1 + lattice1_0 + lattice1_1 ) * latt_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0[:] = latt_0 * move
    return nn_sum

def looping2(latt, X_s, Y_s, Ja, Jb, val, nequilibrium):
    t0 = time.time()
    for i in range(nequilibrium):
        cluster2(latt, X_s, Y_s, Ja, Jb, val)
    t = time.time() - t0
    return t, functions.Average(latt[[0,2]]), functions.Average(latt[[1,3]])

@njit
def cluster2(latt, X_s, Y_s, Ja, Jb, val):
    k = np.random.randint(0, 4)
    j = np.random.randint(0, Y_s)
    i = np.random.randint(0, X_s)
    P_adda = 1 - np.exp( 2 * val * -abs(Ja) )
    P_addb = 1 - np.exp( 2 * val * -abs(Jb) )
    lable = np.ones((4, Y_s, X_s)).astype(np.int8)
    stack = [(k,j,i)]
    lable[k,j,i] = 0
    while len(stack) > 0:
        current = stack.pop()
        sign = latt[current]
        k, j, i = current
        kx = 3 - k
        ky = (5 - k) if k > 1 else (1 - k)
        kz = (2 - k) if k%2 == 0 else (4 - k)
        jpp = (j + 1) if (j + 1) < Y_s else 0
        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
        ipp = (i + 1) if (i + 1) < X_s else 0
        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
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

        neighbor_lef = (kx, j, x_inn)
        neighbor_rig = (kx, j, x_ipp)
        neighbor_up1 = (ky, y_jnn, i)
        neighbor_do1 = (ky, y_jpp, i)

        latt[current] *= -1
        if Ja > 0:
            if latt[neighbor_lef] == sign and lable[neighbor_lef] and np.random.rand() < P_adda:
                stack.append(neighbor_lef)
                lable[neighbor_lef] = 0
            if latt[neighbor_rig] == sign and lable[neighbor_rig] and np.random.rand() < P_adda:
                stack.append(neighbor_rig)
                lable[neighbor_rig] = 0
            if latt[neighbor_up1] == sign and lable[neighbor_up1] and np.random.rand() < P_adda:
                stack.append(neighbor_up1)
                lable[neighbor_up1] = 0
            if latt[neighbor_do1] == sign and lable[neighbor_do1] and np.random.rand() < P_adda:
                stack.append(neighbor_do1)
                lable[neighbor_do1] = 0
        else:
            if latt[neighbor_lef] == -sign and lable[neighbor_lef] and np.random.rand() < P_adda:
                stack.append(neighbor_lef)
                lable[neighbor_lef] = 0
            if latt[neighbor_rig] == -sign and lable[neighbor_rig] and np.random.rand() < P_adda:
                stack.append(neighbor_rig)
                lable[neighbor_rig] = 0
            if latt[neighbor_up1] == -sign and lable[neighbor_up1] and np.random.rand() < P_adda:
                stack.append(neighbor_up1)
                lable[neighbor_up1] = 0
            if latt[neighbor_do1] == -sign and lable[neighbor_do1] and np.random.rand() < P_adda:
                stack.append(neighbor_do1)
                lable[neighbor_do1] = 0

        if abs(Jb) > abs(Ja * 0.1):
            if k == 0:
                i_1 = ipp
                j_2 = jpp
            elif k == 1:
                i_1 = ipp
                j_2 = jnn
            elif k == 2:
                i_1 = inn
                j_2 = jnn
            else:
                i_1 = inn
                j_2 = jpp
            neighbor_0 = (kz, j, i)
            neighbor_1 = (kz, j, i_1)
            neighbor_2 = (kz, j_2, i)
            neighbor_3 = (kz, j_2, i_1)
            if Jb > 0:
                if latt[neighbor_0] == sign and lable[neighbor_0] and np.random.rand() < P_addb:
                    stack.append(neighbor_0)
                    lable[neighbor_0] = 0
                if latt[neighbor_1] == sign and lable[neighbor_1] and np.random.rand() < P_addb:
                    stack.append(neighbor_1)
                    lable[neighbor_1] = 0
                if latt[neighbor_2] == sign and lable[neighbor_2] and np.random.rand() < P_addb:
                    stack.append(neighbor_2)
                    lable[neighbor_2] = 0
                if latt[neighbor_3] == sign and lable[neighbor_3] and np.random.rand() < P_addb:
                    stack.append(neighbor_3)
                    lable[neighbor_3] = 0
            else:
                if latt[neighbor_0] == -sign and lable[neighbor_0] and np.random.rand() < P_addb:
                    stack.append(neighbor_0)
                    lable[neighbor_0] = 0
                if latt[neighbor_1] == -sign and lable[neighbor_1] and np.random.rand() < P_addb:
                    stack.append(neighbor_1)
                    lable[neighbor_1] = 0
                if latt[neighbor_2] == -sign and lable[neighbor_2] and np.random.rand() < P_addb:
                    stack.append(neighbor_2)
                    lable[neighbor_2] = 0
                if latt[neighbor_3] == -sign and lable[neighbor_3] and np.random.rand() < P_addb:
                    stack.append(neighbor_3)
                    lable[neighbor_3] = 0

def iteration2(latt, X_s, Y_s, Ja, Jb, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 2))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update2(latt[0], latt[1], latt[2], latt[3], X_s, Y_s, Ja, Jb, val)
    for i in range(nworks):
        E0 = update2(latt[0], latt[1], latt[2], latt[3], X_s, Y_s, Ja, Jb, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[[0,2]]), functions.Average(latt[[1,3]])
    t = time.time() - t0
    return t, Nw, Ew

def update2(latt_0, latt_1, latt_2, latt_3, X_s, Y_s, Ja, Jb, val):
    # 0
    M0 = ij2(latt_0, latt_3, latt_1, latt_2, 0, X_s, Y_s, Ja, Jb, val)
    # 1
    M1 = ij2(latt_1, latt_2, latt_0, latt_3, 1, X_s, Y_s, Ja, Jb, val)
    # 2
    M2 = ij2(latt_2, latt_1, latt_3, latt_0, 2, X_s, Y_s, Ja, Jb, val)
    # 3
    M3 = ij2(latt_3, latt_0, latt_2, latt_1, 3, X_s, Y_s, Ja, Jb, val)
    return (M0 + M1 + M2 + M3)

def ij2(latt_0, latt_1, latt_2, latt_3, color, X_s, Y_s, Ja, Jb, val):
    if color == 0:
        lattice0_0 = np.roll(latt_1, -1, axis=1)
        lattice0_1 = latt_2
        lattice1_0 = latt_1
        lattice1_1 = np.roll(latt_2, -1, axis=0)
        lattice2_0 = np.roll(latt_3, -1, axis=1)
        lattice2_1 = latt_3
        lattice2_2 = np.roll(latt_3, -1, axis=0)
        lattice2_3 = np.roll(np.roll(latt_3, -1, axis=1), -1, axis=0)
    elif color == 1:
        lattice0_0 = np.roll(latt_1, -1, axis=1)
        lattice0_1 = np.roll(latt_2, 1, axis=0)
        lattice1_0 = latt_1
        lattice1_1 = latt_2
        lattice2_0 = np.roll(np.roll(latt_3, -1, axis=1), 1, axis=0)
        lattice2_1 = np.roll(latt_3, 1, axis=0)
        lattice2_2 = latt_3
        lattice2_3 = np.roll(latt_3, -1, axis=1)
    elif color == 2:
        lattice0_0 = latt_1
        lattice0_1 = np.roll(latt_2, 1, axis=0)
        lattice1_0 = np.roll(latt_1, 1, axis=1)
        lattice1_1 = latt_2
        lattice2_0 = np.roll(latt_3, 1, axis=0)
        lattice2_1 = np.roll(np.roll(latt_3, 1, axis=1), 1, axis=0)
        lattice2_2 = np.roll(latt_3, 1, axis=1)
        lattice2_3 = latt_3
    else:
        lattice0_0 = latt_1
        lattice0_1 = latt_2
        lattice1_0 = np.roll(latt_1, 1, axis=1)
        lattice1_1 = np.roll(latt_2, -1, axis=0)
        lattice2_0 = latt_3
        lattice2_1 = np.roll(latt_3, 1, axis=1)
        lattice2_2 = np.roll(np.roll(latt_3, 1, axis=1), -1, axis=0)
        lattice2_3 = np.roll(latt_3, -1, axis=0)

    nn_sum = ( -Ja * ( lattice0_0 + lattice0_1 + lattice1_0 + lattice1_1 ) - Jb * (lattice2_0 + lattice2_1 + lattice2_2 + lattice2_3) ) * latt_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0[:] = latt_0 * move
    return nn_sum
