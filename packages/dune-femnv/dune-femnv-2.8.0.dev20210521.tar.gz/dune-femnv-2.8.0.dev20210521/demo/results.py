from math import log
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import pickle

def sigfig(num, sig_figs):
    return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))

def wp(polOrder=''):
    main_file = open('results/pickled_results' + polOrder, 'w')
    eoc_file = open('results/eocs' + polOrder, 'w')
    sym_file1 = open('results/latex_symmetry1' + polOrder, 'w')
    sym_file2 = open('results/latex_symmetry2' + polOrder, 'w')
    sym_file1.write('Method')
    sym_file2.write('Symmetric')
    x = np.array([32, 128, 512, 2048, 8096])
    legend = []
    for filename in sorted(os.listdir('pickle' + polOrder)):
        f = open('pickle' + polOrder + '/' + filename, 'rb')
        data = []
        while 1:
            try:
                data.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        model = filename.split("_")[0]
        method = filename.split("_", 2)[1].split("_")[0]
        solver = filename.split("_", 3)[2].split(".")[0]
        if polOrder == '':
            order = 'k=2'
        else:
            order = 'k=' + polOrder
        try:
            current_model
        except:
            current_model = model
            main_file.write('###### ' + model + '\n')
            markers = ['+','d','*','.','^','v','o','x','D','<','>','s','p','8']
            eoc_file.write('###### ' + model + '\n')
            eoc_file.write('         L^2    H^1    |A:D^2 e_h|_H^-1 |A:D^2 e_h|_L^2\n')
            eoc_latex_file = open('results/eoclatex_' + model + polOrder, 'w')
            print('starting results output')
        if model != current_model:
            current_model = model
            main_file.write('###### ' + model + '\n')
            plt.close('all')
            legend = []
            markers = ['+','d','*','.','^','v','o','x','D','<','>','s','p','8']
            eoc_file.write('\n')
            eoc_file.write('###### ' + model + '\n')
            eoc_file.write('         L^2    H^1    |A:D^2 e_h|_H^-1 |A:D^2 e_h|_L^2\n')
            eoc_latex_file.close()
            eoc_latex_file = open('results/eoclatex_' + model + polOrder, 'w')
        main_file.write('# ' + method + ', ' + solver + ', ' + order + '\n')
        if data == []:
            print('deleting unfinished test', filename)
            os.remove('pickle' + polOrder + '/' + filename)
        elif isinstance(data[0][1], list):
            main_file.write('Grid  |e_h|_L^2  EOC     |e_h|_H^1  EOC     |A:D^2 e_h|_H^-1 EOC     |A:D^2 e_h|_L^2 EOC     Iterations  Time\n')
            eoc = []
            error_old = [None] * 4
            for eoc_loop in range(0, len(data)):
                error = data[eoc_loop].pop(1)
                for i in range (0, len(error)):
                    if eoc_loop == 0:
                        eoc.append('-')
                    else:
                        try:
                            eoc[i] = log(error[i]/error_old[i])/log(0.5)
                            eoc[i] = sigfig(eoc[i], 3)
                        except:
                            eoc[i] = '-'
                    error_old[i] = error[i]
                    try:
                        data[eoc_loop].insert(2*i + 1, sigfig(error[i], 4))
                    except:
                        data[eoc_loop].insert(2*i + 1, '-')
                    data[eoc_loop].insert(2*i + 2, eoc[i])
                data[eoc_loop][-1] = sigfig(data[eoc_loop][-1], 3)
            for entry in data:
                if len(entry) == 7:
                    entry[5:5] = ('-', '-', '-', '-')
                main_file.write('{: <5} {: <10} {: <7} {: <10} {: <7} {: <16} {: <7} {: <15} {: <7} {: <11} {:}'.format(\
                str(entry[0]), str(entry[1]), str(entry[2]), str(entry[3]), str(entry[4]), str(entry[5]), \
                str(entry[6]), str(entry[7]), str(entry[8]), str(entry[9]), str(entry[10])) + '\n')
            legend.append(method)

            if model == 'advection2' and method == 'var':
                pass
            elif model == 'nonD' and method == 'var':
                pass
            else:
                l2_eoc = [data[i][2] for i in range(0, len(data))]
                l2_eoc = [None if v is '-' else v for v in l2_eoc]
                if len(l2_eoc) < 5:
                    l2_eoc.append(None)
                l2_eoc = np.array(l2_eoc).astype(np.double)
                mask = np.isfinite(l2_eoc)
                plt.figure(0)
                plt.semilogx(x[mask], l2_eoc[mask], marker=markers[-1])
                plt.legend(legend, fontsize=13)
                plt.axis([120, 8110, 0, 3.8])
                plt.ylabel('EOC of L^2 error', fontsize=13)
                plt.xlabel('Number of Elements (log)', fontsize=13)
                plt.tick_params(axis='both', which='major', labelsize=13)
                plt.gcf().subplots_adjust(bottom=0.15, left=0.14)
                plt.autoscale()
                plt.savefig('plots/' + model + '_l2eoc' + polOrder + '.png')

                h1_eoc = [data[i][4] for i in range(0, len(data))]
                h1_eoc = [None if v is '-' else v for v in h1_eoc]
                print(model, method, solver)
                if len(h1_eoc) < 5:
                    h1_eoc.append(None)
                h1_eoc = np.array(h1_eoc).astype(np.double)
                mask = np.isfinite(h1_eoc)
                plt.figure(1)
                plt.semilogx(x[mask], h1_eoc[mask], marker=markers[-1])
                plt.legend(legend, fontsize=13)
                plt.axis([120, 8110, 1.2, 2.2])
                plt.ylabel('EOC of H^1 error', fontsize=13)
                plt.xlabel('Number of Elements (log)', fontsize=13)
                plt.tick_params(axis='both', which='major', labelsize=13)
                plt.gcf().subplots_adjust(bottom=0.15, left=0.14)
                plt.autoscale()
                plt.savefig('plots/' + model + '_h1eoc' + polOrder + '.png')

                iterations = [data[i][9] for i in range(0, len(data))]
                iterations = [None if v is '-' else v for v in iterations]
                if len(iterations) < 5:
                    iterations.append(None)
                iterations = np.array(iterations).astype(np.double)
                mask = np.isfinite(iterations)
                plt.figure(2)
                plt.semilogx(x[mask], iterations[mask], marker=markers[-1])
                plt.legend(legend, fontsize=13)
                plt.axis([30, 8110, 1, 12])
                plt.ylabel('Number of Iterations', fontsize=13)
                plt.xlabel('Number of Elements (log)', fontsize=13)
                plt.tick_params(axis='both', which='major', labelsize=13)
                plt.gcf().subplots_adjust(bottom=0.15, left=0.14)
                plt.autoscale()
                plt.savefig('plots/' + model + '_iter' + polOrder + '.png')

                time = [data[i][10] for i in range(0, len(data))]
                time = [None if v is '-' else v for v in time]
                if len(time) < 5:
                    time.append(None)
                time = np.array(time).astype(np.double)
                mask = np.isfinite(time)
                plt.figure(3)
                plt.loglog(x[mask], time[mask], marker=markers[-1])
                plt.legend(legend, fontsize=13)
                plt.axis([30, 8110, 0.001, 20])
                plt.ylabel('Time taken in s (log)', fontsize=13)
                plt.xlabel('Number of Elements (log)', fontsize=13)
                plt.tick_params(axis='both', which='major', labelsize=13)
                plt.gcf().subplots_adjust(bottom=0.15, left=0.14)
                plt.autoscale()
                plt.savefig('plots/' + model + '_time' + polOrder + '.png')

                l2_error = [data[i][1] for i in range(0, len(data))]
                l2_error = [None if v is '-' else v for v in l2_error]
                if len(l2_error) < 5:
                    l2_error.append(None)
                l2_error = np.array(l2_error).astype(np.double)
                mask = np.isfinite(l2_error)
                plt.figure(4)
                plt.loglog(x[mask], l2_error[mask], marker=markers[-1])
                plt.legend(legend, fontsize=13)
                plt.axis([30, 8110, 1e-6, 0.25])
                plt.ylabel('L^2 error (log)', fontsize=13)
                plt.xlabel('Number of Elements (log)', fontsize=13)
                plt.tick_params(axis='both', which='major', labelsize=13)
                plt.gcf().subplots_adjust(bottom=0.15, left=0.14)
                plt.autoscale()
                plt.savefig('plots/' + model + '_l2error' + polOrder + '.png')

                h1_error = [data[i][3] for i in range(0, len(data))]
                h1_error = [None if v is '-' else v for v in h1_error]
                if len(h1_error) < 5:
                    h1_error.append(None)
                h1_error = np.array(h1_error).astype(np.double)
                mask = np.isfinite(h1_error)
                plt.figure(5)
                plt.loglog(x[mask], h1_error[mask], marker=markers[-1])
                plt.legend(legend, fontsize=13)
                plt.axis([30, 8110, 1e-3, 2.5])
                plt.ylabel('H^1 error (log)', fontsize=13)
                plt.xlabel('Number of Elements (log)', fontsize=13)
                plt.tick_params(axis='both', which='major', labelsize=13)
                plt.gcf().subplots_adjust(bottom=0.15, left=0.14)
                plt.autoscale()
                plt.savefig('plots/' + model + '_h1error' + polOrder + '.png')
                markers.pop()

            try:
                eoc_file.write('{: <8} {: <6} {: <6} {: <16} {:}'.format(method, \
                str(sigfig((data[-1][2] + data[-2][2] + data[-3][2])/3, 4)), \
                str(sigfig((data[-1][4] + data[-2][4] + data[-3][4])/3, 4)), \
                str(sigfig((data[-1][6] + data[-2][6] + data[-3][6])/3, 4)), \
                str(sigfig((data[-1][8] + data[-2][8] + data[-3][8])/3, 4))))
            except:
                eoc_file.write('{: <8} {: <6} {: <6} {: <16} {:}'.format(method, \
                str(sigfig((data[-1][2] + data[-2][2] + data[-3][2])/3, 4)), \
                str(sigfig((data[-1][4] + data[-2][4] + data[-3][4])/3, 4)), \
                str('-'), str('-')))
            eoc_file.write('\n')

            try:
                eoc_latex_file.write(method + ' & ' + str(sigfig((data[-1][2] + data[-2][2] + data[-3][2])/3, 4)) + ' & ' + \
                str(sigfig((data[-1][4] + data[-2][4] + data[-3][4])/3, 4)) + ' & ' + \
                str(sigfig((data[-1][6] + data[-2][6] + data[-3][6])/3, 4)) + ' & ' + \
                str(sigfig((data[-1][8] + data[-2][8] + data[-3][8])/3, 4)) + ' \\\\\n')
            except:
                eoc_latex_file.write(method + ' & ' + str(sigfig((data[-1][2] + data[-2][2] + data[-3][2])/3, 4)) + ' & ' + \
                str(sigfig((data[-1][4] + data[-2][4] + data[-3][4])/3, 4)) + ' \\\\\n')

            latex_file = open('results/latex_' + model + '_' + method + '_' + solver + polOrder, 'w')
            for entry in data:
                if polOrder != 'NL':
                    latex_file.write(str(entry[0]) + ' & ' + str(entry[1]) + ' & ' +  str(entry[2]) + ' & ' \
                    + str(entry[3]) + ' & ' +  str(entry[4]) + ' & ' +  str(entry[5]) + ' & ' +  str(entry[6]) \
                    + ' & ' +  str(entry[7]) + ' & ' +  str(entry[8]) + ' \\\\\n')
                else:
                    latex_file.write(str(entry[0]) + ' & ' + str(entry[1]) + ' & ' +  str(entry[2]) + ' & ' \
                    + str(entry[3]) + ' & ' +  str(entry[4]) + ' \\\\\n')
            latex_file.close()

            if model == 'nonD':
                if solver == 'cg':
                    symmetric = 'yes'
                else:
                    symmetric = 'no'
                sym_file1.write(' & \\textbf{' + method + '}')
                sym_file2.write(' & ' + symmetric)
        main_file.write('\n')
    main_file.close()
    eoc_file.close()
    sym_file1.write('\\\\\n \\hline')
    sym_file1.close()
    sym_file2.close()
    eoc_latex_file.close()
