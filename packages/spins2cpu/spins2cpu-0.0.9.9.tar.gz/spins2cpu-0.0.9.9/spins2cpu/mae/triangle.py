import logging
import numpy as np
from spins2cpu import functions
from spins2cpu.mae import triangle_update

kB = 8.61733e-2 # 玻尔兹曼常数(meV/K)

def run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks):
    logging.basicConfig(level=logging.INFO,format="%(message)s",filename=file,filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    N = X * Y
    num = N
    logging.info("{} {:<12} {} {} * {:<8} {} {}".format("configuration:", file.split('_')[0], "lattice dimensions:", X, Y, "Atom number:", num))
    Ns = num / 2
    p = len(J)
    np.seterr(divide='ignore', invalid='ignore')
    arrays_values = np.where(arrays_temperatures < 0.01, 0, 1.0/(arrays_temperatures * kB))
    lav = len(arrays_values)
    if p == 1:
        Ja = J[0]
        JA = A[0]
        X_s = X // 2
        Y_s = Y // 2
        logging.info("{} {:<8} {} {} + {:<8} {} {} {:<8} {} {} {}".format("init:", init, "iterations:", nequilibrium, nworks, "parameters:", Ja, "(meV)",
            "anisotropy:", JA, "(meV)"))
        if init == "fm":
            logging.info("{:>16} {:>16}".format("Round", "magnetism(z)"))
            latt = functions.OnesZN(4, Y_s, X_s)
            m_ave = functions.Average(latt[:,2])
            logging.info("{:>16} {:>16.6}".format(0, m_ave))
            logging.info("{:>16} {:>16} {:>18} {:>16} {:>16}".format(
                "Temperature", "magnetism(z)", "susceptibility(z)", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = triangle_update.iteration(latt, X_s, Y_s, Ja, JA, arrays_values[i], nequilibrium, nworks)
                m_ave = functions.Average(Nw)
                s_ave = functions.Average2(Nw)
                susceptibility = arrays_values[i] * N * (s_ave - m_ave ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / N
                logging.info("{:>16.2f} {:>16.6f} {:>18.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave, susceptibility, Cv, t))
                if arrays_values[i] == 0:
                    if (i+1) < lav:
                        t, Nw, Ew = triangle_update.iteration(latt, X_s, Y_s, Ja, JA, arrays_values[i+1], nequilibrium, 0)
                    if (i+2) < lav:
                        t, Nw, Ew = triangle_update.iteration(latt, X_s, Y_s, Ja, JA, arrays_values[i+2], nequilibrium, 0)
        elif init == "afm1":
            logging.info("{:>16} {:>16}".format("Round", "magnetism(z)"))
            latt = functions.OnesZN(4, Y_s, X_s)
            latt[[1,3],2] = -1
            m_ave1 = functions.Average(latt[[0,2],2])
            m_ave2 = functions.Average(latt[[1,3],2])
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>18} {:>18} {:>16} {:>16}".format(
                "Temperature", "magnetism1(z)", "magnetism2(z)", "susceptibility1(z)", "susceptibility2(z)", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = triangle_update.iteration(latt, X_s, Y_s, Ja, JA, arrays_values[i], nequilibrium, nworks)
                arr_a, arr_b = np.hsplit(Nw,2)
                m_ave1 = functions.Average(arr_a)
                m_ave2 = functions.Average(arr_b)
                s_ave1 = functions.Average2(arr_a)
                s_ave2 = functions.Average2(arr_b)
                susceptibility1 = arrays_values[i] * Ns * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * Ns * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / N
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>18.6f} {:>18.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
                if arrays_values[i] == 0:
                    if (i+1) < lav:
                        t, Nw, Ew = triangle_update.iteration(latt, X_s, Y_s, Ja, JA, arrays_values[i+1], nequilibrium, 0)
                    if (i+2) < lav:
                        t, Nw, Ew = triangle_update.iteration(latt, X_s, Y_s, Ja, JA, arrays_values[i+2], nequilibrium, 0)
        else:
            print("Inconsistent parameters...")

    else:
        print("Inconsistent parameters...")
