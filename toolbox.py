import math
import pywt
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from ipywidgets import HBox, FloatSlider, IntSlider
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import display

data = []
data_pure = []
data_with_noise = []
data_shifted = []
data_with_sin = []
labels = ['$x^{-1}$', '$x^0$', '$x^1$', '$x^2$', '$x^3$']
labels_shifted = ['$(x-t)^{-1}$', '$(x-t)^0$', '$(x-t)^1$', '$(x-t)^2$', '$(x-t)^3$']
labels_sin = [x + ' + sin(f \pi x) \cdot a$' for x in ['$x^{-1}', '$x^0', '$x^1', '$x^2', '$x^3']]
x = np.linspace(0, 2, 100)
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
def plot_dwt_result(data, labels, wavelet, ca_axis, cd_axis):
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
        ca_axis.set_title("Approx. Coef")
        ca_axis.plot(ca, label=l)
        cd_axis.set_title("Detail Coef")
        cd_axis.plot(cd, label=l)
        ca_axis.legend()
        cd_axis.legend()
        
        
def plot_dwt_multi_level(data, labels, wavelet, fig, level=None, legend=False):
    plots = fig.subplots(level + 1, 1)
    for n_d in range(len(data)):
        d = data[n_d]
        l = labels[n_d]
        coeffs = pywt.wavedec(d, wavelet, mode=MODE, level=level)
        for n in range(len(coeffs)):
            y = coeffs[-(n+1)][2:-2]
            if np.max(np.abs(y)) < 0.001:
                plots[n].set_ylim(-0.001, 0.001)
            plots[n].plot(y, label=l)
            #print(len(coeffs[-(n+1)]))
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

def plot_fft_result(data, labels, axis, remove_dc):
    for n in range(len(data)):
        d = data[n]
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


def plot_differentation(data, labels, n_diff, axis):
    for n in range(len(data)):
        d = data[n]
        l = labels[n]
        diff = np.diff(d, n_diff)
        #print("Diff Mean:", np.mean(diff))
        axis.plot(diff, label=l)
        axis.set_title("Differentiation")
        axis.legend()
        axis.grid()
        

def plot_differentation_analysis(data, labels, n_diff):
    fig, axis = plt.subplots(1,1)
    plot_differentation(data, labels, n_diff, axis)
