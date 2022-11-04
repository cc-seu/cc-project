from numpy.fft import fft
from numpy import linspace, sin, pi, power, ceil, log2, arange, random
from matplotlib import pyplot as plt
from scipy.signal import butter, lfilter, freqz
import numpy as np
import scipy
from scipy import signal


def fft_func(fs, data):
    len_ = len(data)
    n = int(power(2, ceil(log2(len_))))
    fft_y_ = (fft(data, n)) / len_ * 2
    fre_ = arange(int(n / 2)) * fs / n
    fft_y_ = fft_y_[range(int(n / 2))]
    return fre_, fft_y_


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y  # Filter requirements.


if __name__ == '__main__':
    Fs = 62

    X, step = [], []
    j = 0
    file_path = 'C:\\Users\\陈哥\\Desktop\\standard.txt'
    with open(file=file_path, mode='r+', encoding='utf-8') as g:
        lines = g.readlines()
        for line in lines:
            value = [float(s) for s in line.split()]
            X.append((value[1] - 1799) / 10)
            step.append(j)
            j = j + 1

    X_smooth = scipy.signal.savgol_filter(X, 21, 5)

    order = 6
    fs = 62.0  # sample rate, Hz
    cutoff = 10  # desired cutoff frequency of the filter, Hz # Get the filter coefficients so we can check its frequency response.
    b, a = butter_lowpass(cutoff, fs, order)  # Plot the frequency response.
    w, h = freqz(b, a, worN=800)
    plt.subplot(3, 1, 1)
    plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
    plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
    plt.axvline(cutoff, color='k')
    plt.xlim(0, 0.5 * fs)
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()  # Demonstrate the use of the filter. # First make some data to be filtered.
    data = X
    y = butter_lowpass_filter(data, cutoff, fs, order)
    plt.subplot(3, 1, 2)
    plt.plot(step, data, 'b-', label='data')
    plt.plot(step, y, 'g-', linewidth=2, label='butter_filtered')
    plt.plot(step,X_smooth,'r-',label='savgol_filter')
    plt.xlabel('Time [sec]')
    plt.grid()
    plt.legend()
    plt.subplots_adjust(hspace=0.35)



    fre, fft_y = fft_func(Fs, y)
    plt.subplot(3, 1, 3)
    plt.plot(fre,abs(fft_y))
    plt.grid()
    plt.show()
