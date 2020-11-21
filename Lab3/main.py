from math import cos, pi, sqrt, sin, hypot, atan2
from itertools import repeat
from random import randrange
import numpy as np
from matplotlib.widgets import Slider
from matplotlib import pyplot as plt


N = 1024
TEST_AMPLITUDES = [1, 3, 5, 8, 10, 12, 16]
TEST_PHASES = [pi / 6, pi / 4, pi / 3, pi / 2, 3 * pi / 4, pi]

ERROR_LEVEL = 0.001
POLY_COUNT = 30


def signal_point(x, N):
    return 10 * cos((2 * pi * x) / N)


def fourier_path(func, sequence, j, N):
    result = sum(x * func(2 * pi * i * j / N) for i, x in enumerate(sequence))
    return (2 / N) * result


def fourier_spectrum(sequence):
    N = len(sequence)
    spectrum_list = []
    for j in range(N):
        cosine = fourier_path(cos, sequence, j, N)
        sine = fourier_path(sin, sequence, j, N)
        amplitude = hypot(sine, cosine)
        phase = atan2(sine, cosine)
        spectrum_list.append((amplitude, phase if abs(amplitude) > ERROR_LEVEL else 0))

    return spectrum_list


def fast_fourier_spectrum(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if N == 1:
        return x

    X_even = fast_fourier_spectrum(x[::2])
    X_odd = fast_fourier_spectrum(x[1::2])
    factor = np.exp(-2j * np.pi * np.arange(N) / N)
    result = np.concatenate([X_even + factor[:N // 2] * X_odd, X_even + factor[N // 2:] * X_odd])
    return result


def get_phase(x):
    return - np.arctan2(np.imag(x), np.real(x))


def get_fast_fourier_spectrum(spectrum):
    fft_result = fast_fourier_spectrum(spectrum)
    N = len(spectrum)
    amplitudes = [abs(x) * 2 / N for x in fft_result]
    phases = [get_phase(x) if amplitudes[i] > ERROR_LEVEL else 0 for i, x in enumerate(fft_result)]
    return list(zip(amplitudes, phases))


def spectrum_point(index, j, N, amplitude, phase):
    return amplitude * cos((2 * pi * index * j / N) - phase)


def polyharmonic(index, N, repeats, spectrum):
    return sum(spectrum_point(index, j, N, spectrum[j][0], spectrum[j][1]) for j in range(repeats))


def restore_signal(spectrum):
    sequence = []
    N = len(spectrum)
    for i in range(N):
        sequence.append(polyharmonic(i, N, N // 2 - 1, spectrum))

    return sequence


def randoms_from(values, length=None):
    _range = range(length) if length is not None else repeat(0)
    values_len = len(values)
    for _ in _range:
        yield values[randrange(0, values_len)]


def filter_signal(spectrum, filter_predicate):
    length = len(spectrum)
    half_length = length // 2

    sequence = []
    for item in enumerate(spectrum):
        index, value = item
        if index > half_length:
            index = length - index

        sequence.append(value if filter_predicate(index) else (0, 0))

    return list(sequence)


def print_plot(signals, labels, w, h):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'darkorange', 'sienna', 'navy', 'blueviolet', 'gray']
    plots = []
    fig = plt.figure(figsize=(15, 7))
    plt.grid(True)

    for i, unit in enumerate(signals):
        plt.subplot(h, w, i + 1)
        tempPlot, = plt.plot(unit, color=colors[i])
        plots.append(tempPlot)

    plt.figlegend(plots, labels, loc='upper left')
    return plots


def main():
    labels = ["Оригинальный сигнал", "Восстановленый сигнал", "Амплитудный спектр", "Фазовый спектр"]

    # Task 2
    original_signal = [signal_point(i, N) for i in range(N)]

    spectrum = fourier_spectrum(original_signal)
    amplitude, phase = zip(*spectrum)
    restored_signal = restore_signal(spectrum)
    plots = print_plot([original_signal, restored_signal, amplitude, phase], labels, 2, 2)


    # Prepase polyharmonic signal
    test_spectrum = [(0, 0)] + list( zip(list(randoms_from(TEST_AMPLITUDES, POLY_COUNT)), list(randoms_from(TEST_PHASES, POLY_COUNT))))
    polyharmonic_original_signal = [polyharmonic(i, N, len(test_spectrum), test_spectrum) for i in range(N)]


    # Task 3
    spectrum = fourier_spectrum(polyharmonic_original_signal)
    amplitude, phase = zip(*spectrum)
    restored_signal = restore_signal(spectrum)

    plots = print_plot([polyharmonic_original_signal, restored_signal, amplitude, phase], labels, 2, 2)


    # Task 4
    spectrum = get_fast_fourier_spectrum(polyharmonic_original_signal)
    amplitude, phase = zip(*spectrum)
    restored_signal = restore_signal(spectrum)

    plots = print_plot([polyharmonic_original_signal, restored_signal, amplitude, phase], labels, 2, 2)

    # Task 5
    spectrum = fourier_spectrum(polyharmonic_original_signal)
    amplitude, phase = zip(*spectrum)

    spectrum_high = filter_signal(spectrum, lambda x: x < 15)
    spectrum_low = filter_signal(spectrum, lambda x: x > 15)
    spectrum_medium = filter_signal(spectrum, lambda x: (x > 5) and (x < 15))

    amplitude_hign, phase_high = zip(*spectrum_high)
    amplitude_low, phase_low = zip(*spectrum_low)
    amplitude_medium, phase_medium = zip(*spectrum_medium)

    signal_high = restore_signal(spectrum_high)
    signal_low = restore_signal(spectrum_low)
    signal_medium = restore_signal(spectrum_medium)

    labels = ["Оригинальный сигнал", "Спектр амплитудный", "Спектр фазовый", "ВЧ-фильтр", "ВЧ-спектр амплитудный", "ВЧ-спектр фазовый"]
    plots = print_plot([polyharmonic_original_signal, amplitude, phase, signal_high, amplitude_hign, phase_high], labels, 3, 2)

    labels = ["НЧ-фильтр", "НЧ-спектр амплитудный", "НЧ-спектр фазовый", "Фильтр(5:15) - сигнал", "Фильтр(5:15) - спектр амплитудный", "Фильтр(5:15) - спектр фазовый"]
    plots = print_plot([signal_low, amplitude_low, phase_low, signal_medium, amplitude_medium, phase_medium], labels, 3, 2)

    plt.show()

if __name__ == '__main__':
    main()
