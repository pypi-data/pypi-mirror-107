import logging
import numpy as np
from spins2cpu import functions
from spins2cpu.ising import cube_update

kB = 8.61733e-2 # 玻尔兹曼常数(meV/K)

def run(file, init, X, Y, Z, J, arrays_temperatures, nequilibrium, nworks):
    logging.basicConfig(level=logging.INFO,format="%(message)s",filename=file,filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    N = X * Y * Z
    num = N
    logging.info("{} {:<12} {} {} * {} * {:<8} {} {}".format("configuration:", file.split('_')[0], "lattice dimensions:", X, Y, Z, "Atom number:", num))
    Ns = num / 2
    p = len(J)
    np.seterr(divide='ignore', invalid='ignore')
    arrays_values = np.where(arrays_temperatures < 0.01, 0, 1.0/(arrays_temperatures * kB))
    lav = len(arrays_values)
    if p == 1:
        Ja = J[0]
        X_s = X // 2
        Y_s = Y // 2
        Z_s = Z // 2
        logging.info("{} {:<8} {} {} + {:<8} {} {} {}".format("init:", init, "iterations:", nequilibrium, nworks, "parameters:", Ja, "(meV)"))
        if init == "fm":
            logging.info("{:>16} {:>16}".format("Round", "magnetism"))
            latt = functions.Onesint4(8, Z_s, Y_s, X_s)
            m_ave = functions.Average(latt)
            logging.info("{:>16} {:>16.6}".format(0, m_ave))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16}".format("Temperature", "magnetism", "susceptibility", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cube_update.iteration(latt, X_s, Y_s, Z_s, Ja, arrays_values[i], nequilibrium, nworks)
                m_ave = functions.Average(Nw)
                s_ave = functions.Average2(Nw)
                susceptibility = arrays_values[i] * num * (s_ave - m_ave ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(arrays_temperatures[i], m_ave, susceptibility, Cv, t))
        elif init == "afm1":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt = functions.Onesint4(8, Z_s, Y_s, X_s)
            latt[[1,3,4,6]] = -1
            m_ave1 = functions.Average(latt[[0,2,5,7]])
            m_ave2 = functions.Average(latt[[1,3,4,6]])
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cube_update.iteration(latt, X_s, Y_s, Z_s, Ja, arrays_values[i], nequilibrium, nworks)
                a_arr = Nw[:,[0,2,5,7]]
                b_arr = Nw[:,[1,3,4,6]]
                m_ave1 = functions.Average(a_arr)
                m_ave2 = functions.Average(b_arr)
                s_ave1 = functions.Average2(a_arr)
                s_ave2 = functions.Average2(b_arr)
                susceptibility1 = arrays_values[i] * Ns * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * Ns * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        elif init == "random":
            logging.info("{:>16} {:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2", "time(s)"))
            latt = functions.Uniformint4(8, Z_s, Y_s, X_s)
            m_ave1 = functions.Average(latt[[0,2,5,7]])
            m_ave2 = functions.Average(latt[[1,3,4,6]])
            logging.info("{:>16} {:>16.6f} {:>16.6f}".format(0, m_ave1, m_ave2))
            for i in range(1,21):
                val = i + np.random.rand() + 1
                t, m_ave1, m_ave2 = cube_update.looping(latt, X_s, Y_s, Z_s, Ja, val, nequilibrium)
                logging.info("{:>16} {:>16.6f} {:>16.6f}{:>16.6f}".format(i, m_ave1, m_ave2, t))
                if abs(m_ave1) > 0.99 and abs(m_ave2) > 0.99:
                    break
            if m_ave1 * m_ave2 > 0.5:
                logging.info("init: fm")
                logging.info("{:>16} {:>16} {:>16} {:>16} {:>16}".format("Temperature", "magnetism", "susceptibility", "specific heat", "time(s)"))
                for i in range(lav):
                    t, Nw, Ew = cube_update.iteration(latt, X_s, Y_s, Z_s, Ja, arrays_values[i], nequilibrium, nworks)
                    m_ave = functions.Average(Nw)
                    s_ave = functions.Average2(Nw)
                    susceptibility = arrays_values[i] * num * (s_ave - m_ave ** 2)
                    Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                    logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(arrays_temperatures[i], m_ave, susceptibility, Cv, t))
            elif m_ave1 * m_ave2 < -0.5:
                logging.info("init: afm1")
                logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                    "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
                for i in range(lav):
                    t, Nw, Ew = cube_update.iteration(latt, X_s, Y_s, Z_s, Ja, arrays_values[i], nequilibrium, nworks)
                    arr_a, arr_b = np.hsplit(Nw,2)
                    m_ave1 = functions.Average(arr_a)
                    m_ave2 = functions.Average(arr_b)
                    s_ave1 = functions.Average2(arr_a)
                    s_ave2 = functions.Average2(arr_b)
                    susceptibility1 = arrays_values[i] * Ns * (s_ave1 - m_ave1 ** 2)
                    susceptibility2 = arrays_values[i] * Ns * (s_ave2 - m_ave2 ** 2)
                    Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                    logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                        arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
    elif p == 2:
        Ja, Jb = J[0], J[1]
        X_s = X // 2
        Y_s = Y // 2
        Z_s = Z // 2
        logging.info("{} {:<8} {} {} + {:<8} {} {} {} {}".format("init:", init, "iterations:", nequilibrium, nworks, "parameters:", Ja, Jb, "(meV)"))
        if init == "fm":
            logging.info("{:>16} {:>16}".format("Round", "magnetism"))
            latt = functions.Onesint4(8, Z_s, Y_s, X_s)
            m_ave = functions.Average(latt)
            logging.info("{:>16} {:>16.6}".format(0, m_ave))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16}".format("Temperature", "magnetism", "susceptibility", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cube_update.iteration2(latt, X_s, Y_s, Z_s, Ja, Jb, arrays_values[i], nequilibrium, nworks)
                m_ave = functions.Average(Nw)
                s_ave = functions.Average2(Nw)
                susceptibility = arrays_values[i] * num * (s_ave - m_ave ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(arrays_temperatures[i], m_ave, susceptibility, Cv, t))
        elif init == "afm1":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt = functions.Onesint4(8, Z_s, Y_s, X_s)
            latt[[1,3,4,6]] = -1
            m_ave1 = functions.Average(latt[[0,2,5,7]])
            m_ave2 = functions.Average(latt[[1,3,4,6]])
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cube_update.iteration2(latt, X_s, Y_s, Z_s, Ja, Jb, arrays_values[i], nequilibrium, nworks)
                a_arr = Nw[:,[0,2,5,7]]
                b_arr = Nw[:,[1,3,4,6]]
                m_ave1 = functions.Average(a_arr)
                m_ave2 = functions.Average(b_arr)
                s_ave1 = functions.Average2(a_arr)
                s_ave2 = functions.Average2(b_arr)
                susceptibility1 = arrays_values[i] * Ns * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * Ns * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        elif init == "random":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt = functions.Uniformint4(8, Z_s, Y_s, X_s)
            for i in range(6):
                if i == 6: val = 0
                else:
                    val = np.random.rand() ** 2 + i
                t, Nw, Ew = cube_update.iteration2(latt, X_s, Y_s, Z_s, Ja, Jb, val, nequilibrium, 0)
                m_ave1 = functions.Average(latt[[0,2,5,7]])
                m_ave2 = functions.Average(latt[[1,3,4,6]])
                logging.info("{:>16} {:>16.6} {:>16.6}{:>16.6}".format(i, m_ave1, m_ave2, t))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = cube_update.iteration2(latt, X_s, Y_s, Z_s, Ja, Jb, arrays_values[i], nequilibrium, nworks)
                a_arr = Nw[:,[0,2,5,7]]
                b_arr = Nw[:,[1,3,4,6]]
                m_ave1 = functions.Average(a_arr)
                m_ave2 = functions.Average(b_arr)
                s_ave1 = functions.Average2(a_arr)
                s_ave2 = functions.Average2(b_arr)
                susceptibility1 = arrays_values[i] * Ns * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * Ns * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        else:
            print("Inconsistent parameters...")

    else:
        print("Inconsistent parameters...")
