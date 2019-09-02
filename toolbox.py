import math
import pywt
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

POLYNOMS = [0.5, 0, 1, 2, 3]
POLYNOM_LABELS = ['x^{{{}}}'.format(x) for x in POLYNOMS]

def generate_polynom_data(start, end, steps, seed=None):
    if seed is not None:
        np.random.seed(seed)
    x = np.linspace(start, end, steps)
    data = {}
    data['x'] = x
    data['pure'] = {}
    data['pure']['labels'] = ['$' + x + '$' for x in POLYNOM_LABELS]
    data['pure']['y'] = []

    data['with_noise'] = {}
    data['with_noise']['labels'] = ['$' + x + ' + r(x)$' for x in POLYNOM_LABELS]
    data['with_noise']['y'] = []

    data['shifted'] = {}
    data['shifted']['labels'] = ['$(x+t)^{{{}}}$'.format(x) for x in POLYNOMS]
    data['shifted']['y'] = []

    data['sin'] = {}
    data['sin']['labels'] = ['$' + x + ' + \sin(f \pi x) \cdot a$' for x in POLYNOM_LABELS]
    data['sin']['y'] = []

    for p in POLYNOMS:
        y = x**p
        y_noise = x**p + np.random.rand(len(x))*0.05
        y_shifted = (x + 0.5)**p
        y_sin = x**p + np.sin(20 * np.pi * x) * 0.1
        data['pure']['y'].append(y)
        data['with_noise']['y'].append(y_noise)
        data['shifted']['y'].append(y_shifted)
        data['sin']['y'].append(y_sin)
    return data

data = []
data_pure = []
data_with_noise = []
data_shifted = []
data_with_sin = []
labels = ['$x^{0.5}$', '$x^0$', '$x^1$', '$x^2$', '$x^3$']
labels_shifted = ['$(x+t)^{0.5}$', '$(x+t)^0$', '$(x+t)^1$', '$(x+t)^2$', '$(x+t)^3$']
labels_sin = [x + ' + \sin(f \pi x) \cdot a$' for x in ['$x^{0.5}', '$x^0', '$x^1', '$x^2', '$x^3']]
x = np.linspace(0, 2, 128)
for p in [0.5, 0, 1, 2, 3]:
    y = x**p
    y_noise = x**p + np.random.rand(len(x))*0.1
    y_shifted = (x + 0.5)**p
    y_sin = x**p + np.sin(20 * np.pi * x) * 0.1
    #y = np.concatenate((y, y[:-1][::-1]))
    #y = np.concatenate((y, y[::-1]))
    #y = np.tile(y[:-1],10)
    data_pure.append(y)
    data_with_noise.append(y_noise)
    data_shifted.append(y_shifted)
    data_with_sin.append(y_sin)

data_zero_padded = []
data_zero_padded_labels = []
padding = 50
x_padded = x[:len(x)-padding]

y = np.concatenate((np.zeros(padding), x_padded))
data_zero_padded.append(y)
data_zero_padded_labels.append('$x$')

y = np.concatenate((np.zeros(padding), np.sin(x_padded * 2 * np.pi)))
data_zero_padded.append(y)
data_zero_padded_labels.append('$\sin(2 \pi x)$')

y = np.concatenate((np.zeros(padding), np.sin(x_padded * 10 * np.pi)))
data_zero_padded.append(y)
data_zero_padded_labels.append('$\sin(10 \pi x)$')

y = np.concatenate((np.zeros(padding), np.sin(x_padded * 20 * np.pi)))
data_zero_padded.append(y)
data_zero_padded_labels.append('$\sin(20 \pi x)$')


data_sin_with_noise = []
data_sin_with_noise_labels = []
noise = 1

y = data_zero_padded[1] + (np.random.rand(len(x)) - 0.5) * noise
data_sin_with_noise.append(y)
data_sin_with_noise_labels.append('$\sin(x 2 \pi) + rand$')

y = data_zero_padded[2] + (np.random.rand(len(x)) - 0.5) * noise
data_sin_with_noise.append(y)
data_sin_with_noise_labels.append('$\sin(x 10 \pi) + rand$')

y = data_zero_padded[3] + (np.random.rand(len(x)) - 0.5) * noise
data_sin_with_noise.append(y)
data_sin_with_noise_labels.append('$\sin(x 20 \pi) + rand$')

data = data_pure
#labels += ['$x + sin(20 \pi x)$']
#x = np.linspace(0, 2, 100)
#y = x + np.sin(20 * np.pi * x) * 0.1
#data.append(y)



def print_signals(data, labels):
    lines = []
    fig, ax = plt.subplots(1,1)
    ax.set_title("Signals")
    for i in range(len(data)):
        d = data[i]
        l = labels[i]
        line = plt.plot(x, d, label=l)
        lines += line
    plt.legend()
    plt.grid()
    return fig, lines

MODE='smooth'
def plot_dwt_result(data, labels, wavelet, ca_axis, cd_axis, cd_title="Detailkoeffizienten", colors=None):
    if colors is None:
        colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    for n in range(len(data)):
        d = data[n]
        l = labels[n]
        ca, cd = pywt.dwt(d, wavelet, mode=MODE)
        #print(len(d), len(ca), len(cd))
        l_diff = len(ca) - len(d)//2
        start = l_diff
        end = len(ca) - l_diff
        ca = ca[start:end]
        cd = cd[start:end]
        #ca = ca[0:len(d)//2]
        #cd = cd[0:len(d)//2]
        #print(len(d), len(ca), len(cd))
        if ca_axis:
            ca_axis.set_title("Approximationskoeffizienten")
            ca_axis.plot(ca, label=l, color=colors[n])
        if cd_axis:
            cd_axis.set_title(cd_title)
            cd_axis.plot(cd, label=l, color=colors[n])
        
def plot_dwt_multi_level(data, labels, wavelet, fig, level=None, legend=False, padding=2, axis_limit=0.001):
    plots = fig.subplots(level + 1, 1)
    for n_d in range(len(data)):
        d = data[n_d]
        l = labels[n_d]
        coeffs = pywt.wavedec(d, wavelet, mode=MODE, level=level)
        for n in range(len(coeffs)):
            if padding > 0:
                y = coeffs[-(n+1)][padding:-padding]
            else:
                y = coeffs[-(n+1)]
            if np.max(np.abs(y)) < axis_limit:
                plots[n].set_ylim(-axis_limit, axis_limit)
            plots[n].plot(y, label=l)
            #print(len(coeffs[-(n+1)]))
    if legend:
        for p in plots:
            p.legend()

def plot_dwt_multi_level_single(x, d, wavelet, fig, label='', level=None, legend=False, padding=2, axis_limit=0.1):
    xtick = np.linspace(min(x), max(x), 9)
    plots = fig.subplots(level + 2, 1, sharex=True)
    coeffs = pywt.wavedec(d, wavelet, mode=MODE, level=level)
    plots[0].plot(x, d, '-o', color='C0', ms=2)
    plots[0].set_xticks(xtick)
    plots[0].set_ylabel('Signal')
    for n in range(len(coeffs)):
        if padding > 0:
            y = coeffs[-(n+1)][padding:-padding]
        else:
            y = coeffs[-(n+1)]
        # downsample the x range and shift it
        if n < len(coeffs) - 1:
            x = np.linspace((x[0] + x[1])/2, (x[-1] + x[-2]) / 2, len(y))
            ylabel= '$cD_{}$'.format(n+1)
            color='C1'
        else:
            ylabel= '$cA_{}$'.format(n)
            color='C2'
        plots[n+1].step(x, y, 'o', where='mid', label=label, color=color, ms=2)
        plots[n+1].set_ylabel(ylabel)
        if abs(min(y) - max(y)) < axis_limit:
            y_lim = plots[n+1].get_ylim()
            plots[n+1].set_ylim((y_lim[0] - axis_limit, y_lim[1] + axis_limit))
    if legend:
        for p in plots:
            p.legend()
        
def plot_dwt_approximation_reconstruction(data, labels, wavelet, ca_axis, cd_axis, reconstruct_axis, error_axis):
    for n in range(len(data)):
        d = data[n]
        l = labels[n]
        ca, cd = pywt.dwt(d, wavelet, mode=MODE)
        #print(len(d), len(ca), len(cd))
        reconstruct = pywt.idwt(ca, np.zeros(len(cd)), wavelet, mode=MODE)
        #error = reconstruct[:-1] - d
        error = reconstruct - d
        ca_axis.set_title("Approx. Coef")
        ca_axis.plot(ca, label=l)
        cd_axis.set_title("Detail Coef")
        cd_axis.plot(cd, label=l)
        reconstruct_axis.set_title("Reconstruct w/o Details")
        reconstruct_axis.plot(reconstruct, label=l)
        error_axis.set_title("Reconstruct Error")
        error_axis.plot(error, label=l)


def plot_wavelet_analysis(data, labels, wavelet):
    fig, ax_lst = plt.subplots(2, 1)
    plot_dwt_result(data, labels, wavelet, ax_lst[0], ax_lst[1])
    fig.tight_layout()
    #display(fig)

def plot_fft_result(data, labels, axis, remove_dc=False, window=None):
    for n in range(len(data)):
        d = data[n]
        if window:
            d = d * window(len(d))
        l = labels[n]
        if remove_dc:
            d = d - np.mean(d)
        fft = np.fft.rfft(d)
        axis.plot(abs(fft), label=l)
        axis.set_title("Fourier Amplituden")
        axis.legend()
        axis.grid()


def plot_fft_analysis(data, labels, remove_dc=False):
    fig, ax_lst = plt.subplots(1, 1)
    plot_fft_result(data, labels, ax_lst, remove_dc)


def plot_differentation(data, labels, n_diff, axis, x=None, legend=True, title=True, colors=None):
    if colors is None:
        colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    for n in range(len(data)):
        d = data[n]
        l = labels[n]
        diff = np.diff(d, n_diff)
        #print("Diff Mean:", np.mean(diff))
        if x is None:
            axis.plot(diff, label=l, color=colors[n])
        else:
            axis.plot(x[:-1], diff, label=l, color=colors[n])
        if title:
            axis.set_title("Differentiation")
    if legend:
        axis.legend()

def plot_differentation_analysis(data, labels, n_diff):
    fig, axis = plt.subplots(1,1)
    plot_differentation(data, labels, n_diff, axis)
