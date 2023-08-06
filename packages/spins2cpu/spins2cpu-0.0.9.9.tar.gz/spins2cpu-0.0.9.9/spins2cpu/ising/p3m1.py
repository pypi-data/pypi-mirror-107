import logging
import numpy as np
from spins2cpu import functions
from spins2cpu.ising import p3m1_update

kB = 8.61733e-2 # 玻尔兹曼常数(meV/K)

def run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks):
    logging.basicConfig(level=logging.INFO,format="%(message)s",filename=file,filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    N = X * Y
    num = N * 2
    logging.info("{} {:<12} {} {} * {:<8} {} {}".format("configuration:", file.split('_')[0], "lattice dimensions:", X, Y, "Atom number:", num))
    p = len(J)
    np.seterr(divide='ignore', invalid='ignore')
    arrays_values = np.where(arrays_temperatures < 0.01, 0, 1.0/(arrays_temperatures * kB))
    lav = len(arrays_values)
    if p == 1:
        J = [J[0], J[0]]
        p = 2

    if p == 2:
        Ja, J0 = J[0], J[1]
        X_s = X // 2
        Y_s = Y // 2
        logging.info("{} {:<8} {} {} + {:<8} {} {} {} {}".format("init:", init, "iterations:", nequilibrium, nworks, "parameters:", Ja, J0, "(meV)"))
        if init == "fm":
            logging.info("{:>16} {:>16}".format("Round", "magnetism"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = functions.Onesint(Y_s, X_s)
            latt_0_3 = functions.Onesint(Y_s, X_s)
            latt_1_0 = functions.Onesint(Y_s, X_s)
            latt_1_1 = functions.Onesint(Y_s, X_s)
            latt_1_2 = functions.Onesint(Y_s, X_s)
            latt_1_3 = functions.Onesint(Y_s, X_s)
            m_ave = functions.Average(latt_0_0 + latt_0_1 + latt_0_2 + latt_0_3 + latt_1_0 + latt_1_1 + latt_1_2 + latt_1_3) / 8.0
            logging.info("{:>16} {:>16.6}".format(0, m_ave))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16}".format("Temperature", "magnetism", "susceptibility", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                   X_s, Y_s, Ja, J0, arrays_values[i], nequilibrium, nworks)
                m_ave = functions.Average(Nw)
                s_ave = functions.Average2(Nw)
                susceptibility = arrays_values[i] * num * (s_ave - m_ave ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(arrays_temperatures[i], m_ave, susceptibility, Cv, t))
        elif init == "afm1":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = functions.Onesint(Y_s, X_s)
            latt_0_3 = functions.Onesint(Y_s, X_s)
            latt_1_0 = -functions.Onesint(Y_s, X_s)
            latt_1_1 = -functions.Onesint(Y_s, X_s)
            latt_1_2 = -functions.Onesint(Y_s, X_s)
            latt_1_3 = -functions.Onesint(Y_s, X_s)
            m_ave1 = functions.Average(latt_0_0 + latt_0_1 + latt_0_2 + latt_0_3) / 4.0
            m_ave2 = functions.Average(latt_1_0 + latt_1_1 + latt_1_2 + latt_1_3) / 4.0
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                         X_s, Y_s, Ja, J0, arrays_values[i], nequilibrium, nworks)
                arr_a, arr_b = np.hsplit(Nw,2)
                m_ave1 = functions.Average(arr_a)
                m_ave2 = functions.Average(arr_b)
                s_ave1 = functions.Average2(arr_a)
                s_ave2 = functions.Average2(arr_b)
                susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * N * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        elif init == "afm2":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = -functions.Onesint(Y_s, X_s)
            latt_0_3 = -functions.Onesint(Y_s, X_s)
            latt_1_0 = functions.Onesint(Y_s, X_s)
            latt_1_1 = functions.Onesint(Y_s, X_s)
            latt_1_2 = -functions.Onesint(Y_s, X_s)
            latt_1_3 = -functions.Onesint(Y_s, X_s)
            m_ave1 = functions.Average(latt_0_0 + latt_0_1 + latt_1_0 + latt_1_1) / 4.0
            m_ave2 = functions.Average(latt_0_2 + latt_0_3 + latt_1_2 + latt_1_3) / 4.0
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                         X_s, Y_s, Ja, J0, arrays_values[i], nequilibrium, nworks)
                arr_a = Nw[:,[0,1,4,5]]
                arr_b = Nw[:,[2,3,6,7]]
                m_ave1 = functions.Average(arr_a)
                m_ave2 = functions.Average(arr_b)
                s_ave1 = functions.Average2(arr_a)
                s_ave2 = functions.Average2(arr_b)
                susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * N * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        elif init == "afm3":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = -functions.Onesint(Y_s, X_s)
            latt_0_3 = -functions.Onesint(Y_s, X_s)
            latt_1_0 = -functions.Onesint(Y_s, X_s)
            latt_1_1 = -functions.Onesint(Y_s, X_s)
            latt_1_2 = functions.Onesint(Y_s, X_s)
            latt_1_3 = functions.Onesint(Y_s, X_s)
            m_ave1 = functions.Average(latt_0_0 + latt_0_1 + latt_1_2 + latt_1_3) / 4.0
            m_ave2 = functions.Average(latt_0_2 + latt_0_3 + latt_1_0 + latt_1_1) / 4.0
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration2(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                         X_s, Y_s, Ja, J0, arrays_values[i], nequilibrium, nworks)
                arr_a = Nw[:,[0,1,6,7]]
                arr_b = Nw[:,[2,3,4,5]]
                m_ave1 = functions.Average(arr_a)
                m_ave2 = functions.Average(arr_b)
                s_ave1 = functions.Average2(arr_a)
                s_ave2 = functions.Average2(arr_b)
                susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * N * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        else:
            print("Inconsistent parameters...")

    elif p == 3:
        Ja, J0, J1 = J[0], J[1], J[2]
        X_s = X // 2
        Y_s = Y // 2
        logging.info("{} {:<8} {} {} + {:<8} {} {} {} {} {}".format("init:", init, "iterations:", nequilibrium, nworks, "parameters:", Ja, J0, J1, "(meV)"))
        if init == "fm":
            logging.info("{:>16} {:>16}".format("Round", "magnetism"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = functions.Onesint(Y_s, X_s)
            latt_0_3 = functions.Onesint(Y_s, X_s)
            latt_1_0 = functions.Onesint(Y_s, X_s)
            latt_1_1 = functions.Onesint(Y_s, X_s)
            latt_1_2 = functions.Onesint(Y_s, X_s)
            latt_1_3 = functions.Onesint(Y_s, X_s)
            m_ave = functions.Average(latt_0_0 + latt_0_1 + latt_0_2 + latt_0_3 + latt_1_0 + latt_1_1 + latt_1_2 + latt_1_3) / 8.0
            logging.info("{:>16} {:>16.6}".format(0, m_ave))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16}".format("Temperature", "magnetism", "susceptibility", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                   X_s, Y_s, Ja, J0, J1, arrays_values[i], nequilibrium, nworks)
                m_ave = functions.Average(Nw)
                s_ave = functions.Average2(Nw)
                susceptibility = arrays_values[i] * num * (s_ave - m_ave ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(arrays_temperatures[i], m_ave, susceptibility, Cv, t))
        elif init == "afm1":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = functions.Onesint(Y_s, X_s)
            latt_0_3 = functions.Onesint(Y_s, X_s)
            latt_1_0 = -functions.Onesint(Y_s, X_s)
            latt_1_1 = -functions.Onesint(Y_s, X_s)
            latt_1_2 = -functions.Onesint(Y_s, X_s)
            latt_1_3 = -functions.Onesint(Y_s, X_s)
            m_ave1 = functions.Average(latt_0_0 + latt_0_1 + latt_0_2 + latt_0_3) / 4.0
            m_ave2 = functions.Average(latt_1_0 + latt_1_1 + latt_1_2 + latt_1_3) / 4.0
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                         X_s, Y_s, Ja, J0, J1, arrays_values[i], nequilibrium, nworks)
                arr_a, arr_b = np.hsplit(Nw,2)
                m_ave1 = functions.Average(arr_a)
                m_ave2 = functions.Average(arr_b)
                s_ave1 = functions.Average2(arr_a)
                s_ave2 = functions.Average2(arr_b)
                susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * N * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        elif init == "afm2":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = -functions.Onesint(Y_s, X_s)
            latt_0_3 = -functions.Onesint(Y_s, X_s)
            latt_1_0 = functions.Onesint(Y_s, X_s)
            latt_1_1 = functions.Onesint(Y_s, X_s)
            latt_1_2 = -functions.Onesint(Y_s, X_s)
            latt_1_3 = -functions.Onesint(Y_s, X_s)
            m_ave1 = functions.Average(latt_0_0 + latt_0_1 + latt_1_0 + latt_1_1) / 4.0
            m_ave2 = functions.Average(latt_0_2 + latt_0_3 + latt_1_2 + latt_1_3) / 4.0
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                         X_s, Y_s, Ja, J0, J1, arrays_values[i], nequilibrium, nworks)
                arr_a = Nw[:,[0,1,4,5]]
                arr_b = Nw[:,[2,3,6,7]]
                m_ave1 = functions.Average(arr_a)
                m_ave2 = functions.Average(arr_b)
                s_ave1 = functions.Average2(arr_a)
                s_ave2 = functions.Average2(arr_b)
                susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * N * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        elif init == "afm3":
            logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism1", "magnetism2"))
            latt_0_0 = functions.Onesint(Y_s, X_s)
            latt_0_1 = functions.Onesint(Y_s, X_s)
            latt_0_2 = -functions.Onesint(Y_s, X_s)
            latt_0_3 = -functions.Onesint(Y_s, X_s)
            latt_1_0 = -functions.Onesint(Y_s, X_s)
            latt_1_1 = -functions.Onesint(Y_s, X_s)
            latt_1_2 = functions.Onesint(Y_s, X_s)
            latt_1_3 = functions.Onesint(Y_s, X_s)
            m_ave1 = functions.Average(latt_0_0 + latt_0_1 + latt_1_2 + latt_1_3) / 4.0
            m_ave2 = functions.Average(latt_0_2 + latt_0_3 + latt_1_0 + latt_1_1) / 4.0
            logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave1, m_ave2))
            logging.info("{:>16} {:>16} {:>16} {:>16} {:>16} {:>16} {:>16}".format(
                "Temperature", "magnetism1", "magnetism2", "susceptibility1", "susceptibility2", "specific heat", "time(s)"))
            for i in range(lav):
                t, Nw, Ew = p3m1_update.iteration3(latt_0_0, latt_0_1, latt_0_2, latt_0_3, latt_1_0, latt_1_1, latt_1_2, latt_1_3,
                                                         X_s, Y_s, Ja, J0, J1, arrays_values[i], nequilibrium, nworks)
                arr_a = Nw[:,[0,1,6,7]]
                arr_b = Nw[:,[2,3,4,5]]
                m_ave1 = functions.Average(arr_a)
                m_ave2 = functions.Average(arr_b)
                s_ave1 = functions.Average2(arr_a)
                s_ave2 = functions.Average2(arr_b)
                susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
                susceptibility2 = arrays_values[i] * N * (s_ave2 - m_ave2 ** 2)
                Cv = arrays_values[i] ** 2 * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
                logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f} {:>16.6f}".format(
                    arrays_temperatures[i], m_ave1, m_ave2, susceptibility1, susceptibility2, Cv, t))
        else:
            print("Inconsistent parameters...")

    else:
        print("Inconsistent parameters...")
