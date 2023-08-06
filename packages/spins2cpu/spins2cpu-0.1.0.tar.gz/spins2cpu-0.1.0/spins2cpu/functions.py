import numpy as np

def Average(arr):
    return np.sum(arr) / arr.size

def Average2(arr):
    return np.sum(arr**2) / arr.size

def Normalrand(Y, X):
    arr = np.random.randn(3, Y, X)
    return arr / np.sqrt(arr[0]**2 + arr[1]**2 + arr[2]**2)

def NormalrandN(n, Y, X):
    arr = np.zeros((n, 3, Y, X))
    for i in range(n):
        arr[i] = Normalrand(Y, X)
    return arr

def NormalrandNN(n, m, Y, X):
    arr = np.zeros((n, m, 3, Y, X))
    for i in range(n):
        arr[i] = NormalrandN(m, Y, X)
    return arr

def Onesint(Y, X):
    return np.ones((Y, X)).astype(np.int8)

def Onesint3(Z, Y, X):
    return np.ones((Z, Y, X)).astype(np.int8)

def Onesint4(n, Z, Y, X):
    return np.ones((n, Z, Y, X)).astype(np.int8)

def Onesint5(n, m, Z, Y, X):
    return np.ones((n, m, Z, Y, X)).astype(np.int8)

def OnesZ(Y, X):
    arr = np.zeros((3, Y, X))
    arr[2] = 1
    return arr

def OnesZN(n, Y, X):
    arr = np.zeros((n, 3, Y, X))
    arr[:,2] = 1
    return arr

def OnesZNN(n, m, Y, X):
    arr = np.zeros((n, m, 3, Y, X))
    arr[:,:,2] = 1
    return arr

def Uniformint(Y, X):
    return (2 * (np.random.randint(0, 2, (Y, X)) - 0.5)).astype(np.int8)

def Uniformint3(Z, Y, X):
    return (2 * (np.random.randint(0, 2, (Z, Y, X)) - 0.5)).astype(np.int8)

def Uniformint4(n, Z, Y, X):
    return (2 * (np.random.randint(0, 2, (n, Z, Y, X)) - 0.5)).astype(np.int8)

def Uniformint5(n, m, Z, Y, X):
    return (2 * (np.random.randint(0, 2, (n, m, Z, Y, X)) - 0.5)).astype(np.int8)
