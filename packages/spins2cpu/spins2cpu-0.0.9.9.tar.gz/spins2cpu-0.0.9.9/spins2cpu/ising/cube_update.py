import time
import numpy as np
from numba import njit
from spins2cpu import functions

def looping(latt, X_s, Y_s, Z_s, Ja, val, nequilibrium):
    t0 = time.time()
    for i in range(nequilibrium):
        cluster(latt, X_s, Y_s, Z_s, Ja, val)
    t = time.time() - t0
    return t, functions.Average(latt[[0,2,5,7]]), functions.Average(latt[[1,3,4,6]])

@njit
def cluster(latt, X_s, Y_s, Z_s, Ja, val):
    l = np.random.randint(0, 8)
    k = np.random.randint(0, Z_s)
    j = np.random.randint(0, Y_s)
    i = np.random.randint(0, X_s)
    P_add = 1 - np.exp( 2 * val * -abs(Ja) )
    lable = np.ones((8, Z_s, Y_s, X_s)).astype(np.int8)
    stack = [(l,k,j,i)]
    lable[l,k,j,i] = 0
    while len(stack) > 0:
        current = stack.pop()
        sign = latt[current]
        l, k, j, i = current
        lx = (11 - l) if l > 3 else (3 - l)
        lz = (l - 4) if l > 3 else (l + 4)
        kpp = (k + 1) if (k + 1) < Z_s else 0
        knn = (k - 1) if (k - 1) > -1  else (Z_s - 1)
        jpp = (j + 1) if (j + 1) < Y_s else 0
        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
        ipp = (i + 1) if (i + 1) < X_s else 0
        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
        if l == 0:
            ly = 1
            x_inn = i
            x_ipp = ipp
            y_jnn = j
            y_jpp = jpp
            z_knn = knn
            z_kpp = k
        elif l == 1:
            ly = 0
            x_inn = i
            x_ipp = ipp
            y_jnn = jnn
            y_jpp = j
            z_knn = knn
            z_kpp = k
        elif l == 2:
            ly = 3
            x_inn = inn
            x_ipp = i
            y_jnn = jnn
            y_jpp = j
            z_knn = knn
            z_kpp = k
        elif l == 3:
            ly = 2
            x_inn = inn
            x_ipp = i
            y_jnn = j
            y_jpp = jpp
            z_knn = knn
            z_kpp = k
        if l == 4:
            ly = 5
            x_inn = i
            x_ipp = ipp
            y_jnn = j
            y_jpp = jpp
            z_knn = k
            z_kpp = kpp
        elif l == 5:
            ly = 4
            x_inn = i
            x_ipp = ipp
            y_jnn = jnn
            y_jpp = j
            z_knn = k
            z_kpp = kpp
        elif l == 6:
            ly = 7
            x_inn = inn
            x_ipp = i
            y_jnn = jnn
            y_jpp = j
            z_knn = k
            z_kpp = kpp
        else:
            ly = 6
            x_inn = inn
            x_ipp = i
            y_jnn = j
            y_jpp = jpp
            z_knn = k
            z_kpp = kpp

        neighbor_lef = (lx, k, j, x_inn)
        neighbor_rig = (lx, k, j, x_ipp)
        neighbor_up1 = (ly, k, y_jnn, i)
        neighbor_do1 = (ly, k, y_jpp, i)
        neighbor_top = (lz, z_kpp, j, i)
        neighbor_bot = (lz, z_knn, j, i)

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
            if latt[neighbor_top] == sign and lable[neighbor_top] and np.random.rand() < P_add:
                stack.append(neighbor_top)
                lable[neighbor_top] = 0
            if latt[neighbor_bot] == sign and lable[neighbor_bot] and np.random.rand() < P_add:
                stack.append(neighbor_bot)
                lable[neighbor_bot] = 0

def iteration(latt, X_s, Y_s, Z_s, Ja, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update(latt[0], latt[1], latt[2], latt[3],
                    latt[4], latt[5], latt[6], latt[7], X_s, Y_s, Z_s, Ja, val)
    for i in range(nworks):
        E0 = update(latt[0], latt[1], latt[2], latt[3],
                    latt[4], latt[5], latt[6], latt[7], X_s, Y_s, Z_s, Ja, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[0]), functions.Average(latt[1]), functions.Average(latt[2]), functions.Average(latt[3]),\
                functions.Average(latt[4]), functions.Average(latt[5]), functions.Average(latt[6]), functions.Average(latt[7])
    t = time.time() - t0
    return t, Nw, Ew

def update(latt_0, latt_1, latt_2, latt_3,
           latti0, latti1, latti2, latti3, X_s, Y_s, Z_s, Ja, val):
    # 0
    M0 = ij(latt_0, latt_3, latt_1, latti0, 0, X_s, Y_s, Z_s, Ja, val)
    # 1
    M1 = ij(latt_1, latt_2, latt_0, latti1, 1, X_s, Y_s, Z_s, Ja, val)
    # 2
    M2 = ij(latt_2, latt_1, latt_3, latti2, 2, X_s, Y_s, Z_s, Ja, val)
    # 3
    M3 = ij(latt_3, latt_0, latt_2, latti3, 3, X_s, Y_s, Z_s, Ja, val)
    # 4
    N0 = ij(latti0, latti3, latti1, latt_0, 4, X_s, Y_s, Z_s, Ja, val)
    # 5
    N1 = ij(latti1, latti2, latti0, latt_1, 5, X_s, Y_s, Z_s, Ja, val)
    # 6
    N2 = ij(latti2, latti1, latti3, latt_2, 6, X_s, Y_s, Z_s, Ja, val)
    #7
    N3 = ij(latti3, latti0, latti2, latt_3, 7, X_s, Y_s, Z_s, Ja, val)
    return (M0 + M1 + M2 + M3 + N0 + N1 + N2 + N3)

def ij(latt_0, latt_1, latt_2, latti0, color, X_s, Y_s, Z_s, Ja, val):
    if color == 0:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = latt_2
        lattice1_0 = latt_1
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
    elif color == 1:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = latt_1
        lattice1_1 = latt_2
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
    elif color == 2:
        lattice0_0 = latt_1
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = latt_2
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
    elif color == 3:
        lattice0_0 = latt_1
        lattice0_1 = latt_2
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
    elif color == 4:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = latt_2
        lattice1_0 = latt_1
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)
    elif color == 5:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = latt_1
        lattice1_1 = latt_2
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)
    elif color == 6:
        lattice0_0 = latt_1
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = latt_2
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)
    else:
        lattice0_0 = latt_1
        lattice0_1 = latt_2
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)

    nn_sum = -Ja * ( lattice0_0 + lattice0_1 + lattice1_0 + lattice1_1 + lattice2_0 + lattice2_1 ) * latt_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Z_s, Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0[:] = latt_0 * move
    return nn_sum

def iteration2(latt, X_s, Y_s, Z_s, Ja, Jb, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        E0 = update2(latt[0], latt[1], latt[2], latt[3],
                     latt[4], latt[5], latt[6], latt[7], X_s, Y_s, Z_s, Ja, Jb, val)
    for i in range(nworks):
        E0 = update2(latt[0], latt[1], latt[2], latt[3],
                     latt[4], latt[5], latt[6], latt[7], X_s, Y_s, Z_s, Ja, Jb, val)
        Ew[i] = np.sum(E0) / 2
        Nw[i] = functions.Average(latt[0]), functions.Average(latt[1]), functions.Average(latt[2]), functions.Average(latt[3]),\
                functions.Average(latt[4]), functions.Average(latt[5]), functions.Average(latt[6]), functions.Average(latt[7])
    t = time.time() - t0
    return t, Nw, Ew

def update2(latt_0, latt_1, latt_2, latt_3,
            latti0, latti1, latti2, latti3, X_s, Y_s, Z_s, Ja, Jb, val):
    # 0
    M0 = ij2(latt_0, latt_3, latt_1, latt_2, latti0, latti3, latti1, 0, X_s, Y_s, Z_s, Ja, Jb, val)
    # 1
    M1 = ij2(latt_1, latt_2, latt_0, latt_3, latti1, latti2, latti0, 1, X_s, Y_s, Z_s, Ja, Jb, val)
    # 2
    M2 = ij2(latt_2, latt_1, latt_3, latt_0, latti2, latti1, latti3, 2, X_s, Y_s, Z_s, Ja, Jb, val)
    # 3
    M3 = ij2(latt_3, latt_0, latt_2, latt_1, latti3, latti0, latti2, 3, X_s, Y_s, Z_s, Ja, Jb, val)
    # 4
    N0 = ij2(latti0, latti3, latti1, latti2, latt_0, latt_3, latt_1, 4, X_s, Y_s, Z_s, Ja, Jb, val)
    # 5
    N1 = ij2(latti1, latti2, latti0, latti3, latt_1, latt_2, latt_0, 5, X_s, Y_s, Z_s, Ja, Jb, val)
    # 6
    N2 = ij2(latti2, latti1, latti3, latti0, latt_2, latt_1, latt_3, 6, X_s, Y_s, Z_s, Ja, Jb, val)
    #7
    N3 = ij2(latti3, latti0, latti2, latti1, latt_3, latt_0, latt_2, 7, X_s, Y_s, Z_s, Ja, Jb, val)
    return (M0 + M1 + M2 + M3 + N0 + N1 + N2 + N3)

def ij2(latt_0, latt_1, latt_2, latt_3, latti0, latti1, latti2, color, X_s, Y_s, Z_s, Ja, Jb, val):
    if color == 0:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = latt_2
        lattice1_0 = latt_1
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
        lattic_i_0 = np.roll(latt_3, -1, axis=2)
        lattic_i_1 = latt_3
        lattic_i_2 = np.roll(latt_3, 1, axis=1)
        lattic_i_3 = np.roll(np.roll(latt_3, -1, axis=2), -1, axis=1)
        lattic_d_0 = np.roll(np.roll(latti1, -1, axis=2), 1, axis=0)
        lattic_d_1 = np.roll(latti2, 1, axis=0)
        lattic_d_2 = np.roll(latti1, 1, axis=0)
        lattic_d_3 = np.roll(np.roll(latti2, -1, axis=1), 1, axis=0)
        lattic_u_0 = np.roll(latti1, -1, axis=2)
        lattic_u_1 = latti2
        lattic_u_2 = latti1
        lattic_u_3 = np.roll(latti2, -1, axis=1)
    elif color == 1:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = latt_1
        lattice1_1 = latt_2
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
        lattic_i_0 = np.roll(np.roll(latt_3, -1, axis=2), 1, axis=1)
        lattic_i_1 = np.roll(latt_3, 1, axis=1)
        lattic_i_2 = latt_3
        lattic_i_3 = np.roll(latt_3, -1, axis=2)
        lattic_d_0 = np.roll(np.roll(latti1, -1, axis=2), 1, axis=0)
        lattic_d_1 = np.roll(np.roll(latti2, 1, axis=1), 1, axis=0)
        lattic_d_2 = np.roll(latti1, 1, axis=0)
        lattic_d_3 = np.roll(latti2, 1, axis=0)
        lattic_u_0 = np.roll(latti1, -1, axis=2)
        lattic_u_1 = np.roll(latti2, 1, axis=1)
        lattic_u_2 = latti1
        lattic_u_3 = latti2
    elif color == 2:
        lattice0_0 = latt_1
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = latt_2
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
        lattic_i_0 = np.roll(latt_3, 1, axis=1)
        lattic_i_1 = np.roll(np.roll(latt_3, 1, axis=2), 1, axis=1)
        lattic_i_2 = np.roll(latt_3, 1, axis=2)
        lattic_i_3 = latt_3
        lattic_d_0 = np.roll(latti1, 1, axis=0)
        lattic_d_1 = np.roll(np.roll(latti2, 1, axis=1), 1, axis=0)
        lattic_d_2 = np.roll(np.roll(latti1, 1, axis=2), 1, axis=0)
        lattic_d_3 = np.roll(latti2, 1, axis=0)
        lattic_u_0 = latti1
        lattic_u_1 = np.roll(latti2, 1, axis=1)
        lattic_u_2 = np.roll(latti1, 1, axis=2)
        lattic_u_3 = latti2
    elif color == 3:
        lattice0_0 = latt_1
        lattice0_1 = latt_2
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = np.roll(latti0, 1, axis=0)
        lattice2_1 = latti0
        lattic_i_0 = latt_3
        lattic_i_1 = np.roll(latt_3, 1, axis=2)
        lattic_i_2 = np.roll(np.roll(latt_3, 1, axis=2), -1, axis=1)
        lattic_i_3 = np.roll(latt_3, 1, axis=1)
        lattic_d_0 = np.roll(latti1, 1, axis=0)
        lattic_d_1 = np.roll(latti2, 1, axis=0)
        lattic_d_2 = np.roll(np.roll(latti1, 1, axis=2), 1, axis=0)
        lattic_d_3 = np.roll(np.roll(latti2, -1, axis=1), 1, axis=0)
        lattic_u_0 = latti1
        lattic_u_1 = latti2
        lattic_u_2 = np.roll(latti1, 1, axis=2)
        lattic_u_3 = np.roll(latti2, -1, axis=1)
    elif color == 4:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = latt_2
        lattice1_0 = latt_1
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)
        lattic_i_0 = np.roll(latt_3, -1, axis=2)
        lattic_i_1 = latt_3
        lattic_i_2 = np.roll(latt_3, 1, axis=1)
        lattic_i_3 = np.roll(np.roll(latt_3, -1, axis=2), -1, axis=1)
        lattic_u_0 = np.roll(np.roll(latti1, -1, axis=2), -1, axis=0)
        lattic_u_1 = np.roll(latti2, -1, axis=0)
        lattic_u_2 = np.roll(latti1, -1, axis=0)
        lattic_u_3 = np.roll(np.roll(latti2, -1, axis=1), -1, axis=0)
        lattic_d_0 = np.roll(latti1, -1, axis=2)
        lattic_d_1 = latti2
        lattic_d_2 = latti1
        lattic_d_3 = np.roll(latti2, -1, axis=1)
    elif color == 5:
        lattice0_0 = np.roll(latt_1, -1, axis=2)
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = latt_1
        lattice1_1 = latt_2
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)
        lattic_i_0 = np.roll(np.roll(latt_3, -1, axis=2), 1, axis=1)
        lattic_i_1 = np.roll(latt_3, 1, axis=1)
        lattic_i_2 = latt_3
        lattic_i_3 = np.roll(latt_3, -1, axis=2)
        lattic_u_0 = np.roll(np.roll(latti1, -1, axis=2), -1, axis=0)
        lattic_u_1 = np.roll(np.roll(latti2, 1, axis=1), -1, axis=0)
        lattic_u_2 = np.roll(latti1, -1, axis=0)
        lattic_u_3 = np.roll(latti2, -1, axis=0)
        lattic_d_0 = np.roll(latti1, -1, axis=2)
        lattic_d_1 = np.roll(latti2, 1, axis=1)
        lattic_d_2 = latti1
        lattic_d_3 = latti2
    elif color == 6:
        lattice0_0 = latt_1
        lattice0_1 = np.roll(latt_2, 1, axis=1)
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = latt_2
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)
        lattic_i_0 = np.roll(latt_3, 1, axis=1)
        lattic_i_1 = np.roll(np.roll(latt_3, 1, axis=2), 1, axis=1)
        lattic_i_2 = np.roll(latt_3, 1, axis=2)
        lattic_i_3 = latt_3
        lattic_u_0 = np.roll(latti1, -1, axis=0)
        lattic_u_1 = np.roll(np.roll(latti2, 1, axis=1), -1, axis=0)
        lattic_u_2 = np.roll(np.roll(latti1, 1, axis=2), -1, axis=0)
        lattic_u_3 = np.roll(latti2, -1, axis=0)
        lattic_d_0 = latti1
        lattic_d_1 = np.roll(latti2, 1, axis=1)
        lattic_d_2 = np.roll(latti1, 1, axis=2)
        lattic_d_3 = latti2
    else:
        lattice0_0 = latt_1
        lattice0_1 = latt_2
        lattice1_0 = np.roll(latt_1, 1, axis=2)
        lattice1_1 = np.roll(latt_2, -1, axis=1)
        lattice2_0 = latti0
        lattice2_1 = np.roll(latti0, -1, axis=0)
        lattic_i_0 = latt_3
        lattic_i_1 = np.roll(latt_3, 1, axis=2)
        lattic_i_2 = np.roll(np.roll(latt_3, 1, axis=2), -1, axis=1)
        lattic_i_3 = np.roll(latt_3, 1, axis=1)
        lattic_u_0 = np.roll(latti1, -1, axis=0)
        lattic_u_1 = np.roll(latti2, -1, axis=0)
        lattic_u_2 = np.roll(np.roll(latti1, 1, axis=2), -1, axis=0)
        lattic_u_3 = np.roll(np.roll(latti2, -1, axis=1), -1, axis=0)
        lattic_d_0 = latti1
        lattic_d_1 = latti2
        lattic_d_2 = np.roll(latti1, 1, axis=2)
        lattic_d_3 = np.roll(latti2, -1, axis=1)

    nn_sum = ( -Ja * ( lattice0_0 + lattice0_1 + lattice1_0 + lattice1_1 + lattice2_0 + lattice2_1 ) -
                Jb * ( lattic_i_0 + lattic_i_1 + lattic_i_2 + lattic_i_3 +
                       lattic_d_0 + lattic_d_1 + lattic_d_2 + lattic_d_3 +
                       lattic_u_0 + lattic_u_1 + lattic_u_2 + lattic_u_3 ) ) * latt_0
    if val == 0:
        move = np.where(nn_sum > 0, -1, 1)
    else:
        randval = np.random.rand(Z_s, Y_s, X_s)
        new_nn = np.where(nn_sum > 0, 0, nn_sum)
        acceptance = randval - np.exp( 2.0 * val * new_nn )
        move = np.where(acceptance < 0, -1, 1)

    latt_0[:] = latt_0 * move
    return nn_sum
