import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import figure
figure(num=None, figsize=(3.5, 2), dpi=150, facecolor='w', edgecolor='k')


objects = ('Światłowód', 'LTE', 'Wielościeżkowa')
y_pos = np.arange(len(objects))
# performance = [13.34, 148, 34.18]
performance = [15.62, 133.11, 46]

plt.bar(y_pos, performance, align='center', alpha=1, color=['tab:orange', 'tab:blue', 'tab:green'])
plt.xticks(y_pos, objects)
plt.ylabel('Czas transmisji [s]')
plt.tight_layout()
# plt.savefig('b_100_times.png')
plt.savefig('b_2s50_times.png')
