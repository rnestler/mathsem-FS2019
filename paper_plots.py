#!/usr/bin/env python
from toolbox import *

SIZE_BIG = [5.8, 3.2]
SIZE_SMALL = [5.8, 1.7]

plt.rcParams["figure.figsize"] = SIZE_BIG
#plt.rcParams.update({'font.size': 20})
plt.rcParams.update({'pgf.rcfonts': False})

polynom_data = generate_polynom_data(0, 2, 256)

plt.rcParams["figure.figsize"] = SIZE_SMALL
data = polynom_data['pure']['y']
labels = polynom_data['pure']['labels']

for i,y in enumerate(data):
    plt.plot(polynom_data['x'], y, label=labels[i])

plt.legend()
plt.savefig('polynomials_signals.pgf')
plt.savefig('polynomials_signals.pdf')


plt.rcParams["figure.figsize"] = SIZE_BIG
fig, ax_lst = plt.subplots(2, 1, sharex=True)
plot_dwt_result(data, labels, 'db1', ax_lst[0], ax_lst[1])
fig.legend(loc="center right", borderaxespad=0.1, labels=labels)
plt.tight_layout()
plt.subplots_adjust(right=0.85)

plt.savefig('polynomials_signals_db1.pgf')
plt.savefig('polynomials_signals_db1.pdf')

# differentiation

plt.rcParams["figure.figsize"] = SIZE_SMALL
fig, axis = plt.subplots(1,1)
plot_differentation(data, labels, 1, axis, legend=False, title=False)
fig.legend(loc="center right", borderaxespad=0.1, labels=labels)
plt.tight_layout()
plt.subplots_adjust(right=0.85)
plt.savefig('polynomials_signals_diff.pgf')
plt.savefig('polynomials_signals_diff.pdf')


# db1 and db2 analysis

plt.rcParams["figure.figsize"] = SIZE_BIG
fig, ax_lst = plt.subplots(2, 1, sharex=True)

plot_dwt_result(data[1:], labels[1:], 'db2', None, ax_lst[0], cd_title='db2')
plot_dwt_result(data[1:], labels[1:], 'db3', None, ax_lst[1], cd_title='db3')
ax_lst[0].ticklabel_format(useOffset=False, style='sci', scilimits=(0,0))
ax_lst[1].ticklabel_format(useOffset=False, style='sci', scilimits=(0,0))

fig.legend(loc="center right", borderaxespad=0.1, labels=labels[1:])
plt.tight_layout()
plt.subplots_adjust(right=0.85)

plt.savefig('polynomials_signals_db2_3.pgf')
plt.savefig('polynomials_signals_db2_3.pdf')


# Signale mit Rauchen
data = polynom_data['with_noise']['y'][1:]
labels = polynom_data['with_noise']['labels'][1:]


plt.rcParams["figure.figsize"] = SIZE_BIG
fig, ax_lst = plt.subplots(2, 1, sharex=True)

for i,y in enumerate(data):
    ax_lst[0].plot(polynom_data['x'], y, label=labels[i])

plot_differentation(data, labels, 1, ax_lst[1], x=polynom_data['x'], legend=False, title=False)
fig.legend(loc="center right", borderaxespad=0.1, labels=labels)
plt.tight_layout()
plt.subplots_adjust(right=0.8)

plt.savefig('polynomials_noise_signals.pgf')
plt.savefig('polynomials_noise_signals.pdf')
