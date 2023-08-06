import argparse, os
import numpy as np

def check(num):
    if num < 10:
        num = 10
    if num % 2 != 0:
        num += 1
    return num

def main():
    parser = argparse.ArgumentParser(description='spins2cpu: A Monte Carlo Simulation Code for the Phase Transition in 2D/3D Materials',
                                     epilog='''
configurations: \t init:                       \t parameters:  \t model:
triangle        \t fm, random                  \t Ja           \t ising, mae \t
cmmm            \t fm, afm1, afm2              \t Ja, Jb       \t ising      \t (M3)
ammm            \t fm, afm1, afm2, afm3, afm4  \t Ja, Jb, Jc   \t ising      \t (CQ)
square          \t fm, afm1, random            \t Ja, Jb       \t ising, mae \t (M4)
rectangle       \t fm, afm1, random            \t Ja, Jb, Jc   \t ising      \t
honeycomb       \t fm, afm1, random            \t Ja, Jb, Jc   \t ising      \t (M6)
p6mmm           \t fm, afm1, afm2, afm3        \t Ja, J0, J1   \t ising, mae \t (1H)
i_p6mmm         \t fm, afm1, afm2, afm3        \t Ja, J0, J1   \t ising, mae \t (M3×3)
p3m1            \t fm, afm1, afm2, afm3        \t Ja, J0, J1   \t ising, mae \t (1T)
kagome          \t fm, random                  \t Ja           \t ising      \t
cube            \t fm, afm1, random            \t Ja, Jb       \t ising      \t

default values:
x, y, z = 120, 120, 30
iterations for equilibrium, works = 100, 100
exchange coupling (meV) = 1.0
magnetic anisotropy (meV) = 0.1
temperatures = 0, 15, 5, 15, 60, 1

Example:
spins2cpu -x 500 -y 500 -c square -t 35 -r
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version", action="version", version="spins2cpu 0.1.0")
    parser.add_argument('-x', "--length",      type=int, default=120)
    parser.add_argument('-y', "--width",       type=int, default=120)
    parser.add_argument('-z', "--height",      type=int, default=30)
    parser.add_argument('-e', "--equilibrium", type=int, default=100)
    parser.add_argument('-w', "--works",       type=int, default=100)
    parser.add_argument('-p', "--parameters",   type=float, default=[1.0], nargs='+')
    parser.add_argument('-a', "--mae",          type=float, default=[0.1], nargs='+')
    parser.add_argument('-t', "--temperatures", type=float, default=[0, 15, 5, 15, 60, 1], nargs='+')
    parser.add_argument('-s', "--sample", action='store_true', help="show sample")
    parser.add_argument('-r', "--export", action='store_true', help="plot figures after iterations")
    parser.add_argument('-o', "--plot", type=str, help="plot figures from .log file")
    parser.add_argument('-m', "--model",   default="ising",    type=str.lower, choices=['ising', 'mae'])
    parser.add_argument('-i', "--init",    default="fm",       type=str.lower, choices=['fm', 'afm1', 'afm2','afm3', 'afm4', 'random'])
    parser.add_argument('-c', "--config",  default="triangle", type=str.lower,
                        choices=['triangle', 'cmmm', 'ammm', 'square', 'rectangle', 'honeycomb', 'p6mmm', 'i_p6mmm', 'p3m1', 'kagome', 'cube'])
    args = parser.parse_args()

    X = check(args.length)
    Y = check(args.width)
    Z = check(args.height)
    config = args.config
    init = args.init

    i = len(args.temperatures)
    if i == 1:
        arrays_temperatures = np.arange(args.temperatures[0])
    elif i == 2:
        arrays_temperatures = np.arange(args.temperatures[0], args.temperatures[1])
    else:
        k = i // 3
        args.temperatures = args.temperatures[:k * 3]
        arrays_temperatures = np.arange(args.temperatures[0], args.temperatures[1], args.temperatures[2])
        j = 1
        while j < k:
            arrays_temperatures=np.concatenate((arrays_temperatures,
                np.arange(args.temperatures[j * 3], args.temperatures[j * 3 + 1], args.temperatures[j * 3 + 2])))
            j += 1

    nequilibrium = args.equilibrium
    nworks = args.works
    J = args.parameters
    A = args.mae

    if args.plot and os.path.exists(args.plot):
        from spins2cpu import plots
        plots.main(args.plot)
    elif args.sample:
        from spins2cpu import plots, sample
        f = open('honeycomb_500_500.log', 'w')
        print(sample.honeycomb)
        print(sample.honeycomb, file=f)
        f.close()
        plots.main('honeycomb_500_500.log')
    else:
        if args.model == "ising":
            if config == "triangle":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import triangle
                triangle.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "cmmm":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import cmmm
                cmmm.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "ammm":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import ammm
                ammm.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "square":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import square
                square.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "rectangle":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import rectangle
                rectangle.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "honeycomb":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import honeycomb
                honeycomb.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "p6mmm":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import p6mmm
                p6mmm.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "i_p6mmm":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import i_p6mmm
                i_p6mmm.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "p3m1":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import p3m1
                p3m1.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "kagome":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2cpu.ising import kagome
                kagome.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            elif config == "cube":
                file = '{}_{}_{}_{}.log'.format(config, X, Y, Z)
                from spins2cpu.ising import cube
                cube.run(file, init, X, Y, Z, J, arrays_temperatures, nequilibrium, nworks)
            else:
                print("Inconsistent parameters...")
        elif args.model == "mae":
            if config == "triangle":
                file = '{}_mae_{}_{}.log'.format(config, X, Y)
                from spins2cpu.mae import triangle
                triangle.run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks)
            elif config == "square":
                file = '{}_mae_{}_{}.log'.format(config, X, Y)
                from spins2cpu.mae import square
                square.run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks)
            elif config == "p6mmm":
                file = '{}_mae_{}_{}.log'.format(config, X, Y)
                from spins2cpu.mae import p6mmm
                p6mmm.run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks)
            elif config == "i_p6mmm":
                file = '{}_mae_{}_{}.log'.format(config, X, Y)
                from spins2cpu.mae import i_p6mmm
                i_p6mmm.run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks)
            elif config == "p3m1":
                file = '{}_mae_{}_{}.log'.format(config, X, Y)
                from spins2cpu.mae import p3m1
                p3m1.run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks)
            else:
                print("Inconsistent parameters...")
        else:
            print("Inconsistent parameters...")

        if args.export and os.path.exists(file):
            from spins2cpu import plots
            plots.main(file)
