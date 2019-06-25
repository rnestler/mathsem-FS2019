from toolbox import *

plt.rcParams["figure.figsize"] = [5.8, 3.3]
#plt.rcParams.update({'font.size': 20})
plt.rcParams.update({'pgf.rcfonts': False})

polynom_data = generate_polynom_data(0, 2, 256)

#plt.figure(figsize=(5.8, 3.3))
data = polynom_data['pure']['y']
labels = polynom_data['pure']['labels']
for i,y in enumerate(data):
    plt.plot(polynom_data['x'], y, label=labels[i])

plt.legend()
plt.savefig('polynomials_signals.pgf')
plt.savefig('polynomials_signals.pdf')

fig, ax_lst = plt.subplots(2, 1, sharex=True)
plot_dwt_result(data, labels, 'db1', ax_lst[0], ax_lst[1])
fig.legend(loc="center right", borderaxespad=0.1, labels=labels)
plt.tight_layout()
plt.subplots_adjust(right=0.85)

plt.savefig('polynomials_signals_db1.pgf')
plt.savefig('polynomials_signals_db1.pdf')
