import matplotlib.pyplot as plt
import numpy as np


x = np.array([32, 128, 512])
markers = ['+','d','*','.','^','v','o','x','D','<','>','s','p','8']
plt.figure(0)
feng = np.array([33.667, 137.332, 552.29])
plt.loglog(x, feng, marker=markers[-1])
h1D2 = np.array([1007, 4850.96, 20392.293])
plt.loglog(x, h1D2, marker=markers[-1])
h1H = np.array([125.10808, 493.957855, 1969.689768])
plt.loglog(x, h1H, marker=markers[-1])
l2D2 = np.array([4821.9, 82391, 1366998])
plt.loglog(x, l2D2, marker=markers[-1])
l2H = np.array([3085.579, 52460.6, 854928])
plt.loglog(x, l2H, marker=markers[-1])
mu = np.array([7655.376, 87304.34, 1376306.958])
plt.loglog(x, mu, marker=markers[-1])
nvdg = np.array([33.96, 137.52, 552.4])
plt.loglog(x, nvdg, marker=markers[-1])
plt.legend(['feng', 'h1D2', 'h1H', 'l2D2', 'l2H', 'mu', 'nvdg'])
#plt.axis([120, 2100, 0, 3.8])
plt.ylabel('Condition Number for System Matrix (log)')
plt.xlabel('Number of Elements (log)')
plt.savefig('plots/condition2')
