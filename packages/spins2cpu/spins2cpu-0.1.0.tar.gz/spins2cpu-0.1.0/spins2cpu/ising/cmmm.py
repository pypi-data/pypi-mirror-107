import logging
import numpy as np
from spins2cpu import functions
from spins2cpu.ising import cmmm_update

kB = 8.61733e-2 # 玻尔兹曼常数(meV/K)

def run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks):
    logging.basicConfig(level=logging.INFO,format="%(message)s",filename=file,filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    N = X * Y
    num = N * 4
    logging.info("{} {:<12} {} {} * {:<8} {} {}".format("configuration:", file.split('_')[0], "lattice dimensions:", X, Y, "Atom number:", num))
    Ni = N * 2
    p = len(J)
    np.seterr(divide='ignore', invalid='ignore')
    arrays_values = np.where(arrays_temperatures < 0.01, 0, 1.0/(arrays_temperatures * kB))
    lav = len(arrays_values)
    if p == 1:
        J = [J[0], J[0]]
        p = 2

    if p == 2:
        Ja, Jb = J[0], J[1]
        logging.info("{} {:<8} {} {} + {:<8} {} {} {} {}".format("init:", init, "iterations:", nequilibrium, nworks, "parameters:", Ja, Jb, "(meV)"))
        if init == "fm":
            logging.info("{:>16} {:>16}".format("Round", "magnetism"))
            latt = functions.Onesint3(4, Y, X)
            m_ave = functions.Average(latt)
            logging.info("{:>16} {:>16.6}".format(0, m_ave))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16}".format("Temperature", "magnetism", "susceptibility", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cmmm_update.iteration2(latt, X, Y, Ja, Jb, arrays_values[i], nequilibrium, nworks)
                m_ave = functions.Average(Nw)
                s_ave = functions.Average2(Nw)
                susceptibility = arrays_values[i] * num * (s_ave - m_ave ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(arrays_temperatures[i], m_ave, susceptibility, Cv, t))
        elif init == "afm1":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt = functions.Onesint3(4, Y, X)
            latt[[1,2]] = -1
            m_ave1 = functions.Average(latt[::3])
            m_ave2 = functions.Average(latt[1:3])
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cmmm_update.iteration2(latt, X, Y, Ja, Jb, arrays_values[i], nequilibrium, nworks)
                a_arr, b_arr = Nw[:,::3], Nw[:,1:3]
                m_ave1 = functions.Average(a_arr)
                m_ave2 = functions.Average(b_arr)
                s_ave1 = functions.Average2(a_arr)
                s_ave2 = functions.Average2(b_arr)
                susceptibility1 = arrays_values[i] * Ni * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * Ni * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        elif init == "afm2":
            logging.info("{:>16} {:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2", "time(s)"))
            latt = functions.Onesint3(4, Y, X)
            latt[[2,3]] = -1
            m_ave1 = functions.Average(latt[:2])
            m_ave2 = functions.Average(latt[2:])
            logging.info("{:>16} {:>16.6}{:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cmmm_update.iteration2(latt, X, Y, Ja, Jb, arrays_values[i], nequilibrium, nworks)
                a_arr, b_arr = np.hsplit(Nw,2)
                m_ave1 = functions.Average(a_arr)
                m_ave2 = functions.Average(b_arr)
                s_ave1 = functions.Average2(a_arr)
                s_ave2 = functions.Average2(b_arr)
                susceptibility1 = arrays_values[i] * Ni * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * Ni * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        else:
            print("Inconsistent parameters...")

    else:
        print("Inconsistent parameters...")
