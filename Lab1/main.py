from math import pi, sin, asin, atan, tan
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def harmonic_single(amplitude, frequency, phase, N, i):
    return amplitude * sin((2 * pi * frequency * i) / N + phase)


def harmonic(amplitude, frequency, phase, N):
    signal = []
    x = []
    for i in range(N):
        x.append(i/N)
        signal.append(harmonic_single(amplitude=amplitude, frequency=frequency, phase=phase, N=N, i=i))
    return (x, signal)


def polyharmonic_controller(params, N):

    def update(x):
        phases = list(map(lambda x: x.val, slidersFreq))
        for i, param in enumerate(params):
            params[i] = (param[0], phases[i], param[2])
        phases = list(map(lambda x: x.val, slidersAmp))
        for i, param in enumerate(params):
            params[i] = (phases[i], param[1], param[2])
        plot.set_ydata(polyharmonic(params, N))

    fig = plt.figure(figsize=(20, 5))
    plt.title("Задание 3")
    plt.grid(True)
    plt.subplots_adjust(left=0.4)
    plot, = plt.plot(polyharmonic(params, N))

    slidersFreq = []
    for i, param in enumerate(params):
        axes = plt.axes([0.05, 0.8-i*0.06, 0.25, 0.03])
        slider = Slider(axes, '${}$'.format(i), 0, 15, valinit=param[1], valfmt=r'$%1.2f$')
        slider.on_changed(update)
        slidersFreq.append(slider)

    slidersAmp = []
    for i, param in enumerate(params):
        axes = plt.axes([0.05, 0.5 - i * 0.06, 0.25, 0.03])
        slider = Slider(axes, '${}$'.format(i), 0, 15, valinit=param[0], valfmt=r'$%1.2f$')
        slider.on_changed(update)
        slidersAmp.append(slider)
    return slidersFreq + slidersAmp


def polyharmonic(params, N):
    signal = []
    for i in range(N):
        signal.append(sum(harmonic_single(amplitude=param[0], frequency=param[1], phase=param[2], N=N, i=i) for param in params))
    return list(signal)


def polyharmonic_linear(amplitude, frequency, phase, N):
    signals = []
    new_amplitude = amplitude
    new_frequency = frequency
    new_phase = phase
    formula = lambda param, i: param * (i % N) * 0.005
    for i in range(N):
        signals.append(harmonic_single(amplitude=new_amplitude, frequency=new_frequency, phase=new_phase, N=N, i=i%N))
        #new_phase = formula(phase, i)
        #new_amplitude = formula(amplitude, i)
        new_frequency = formula(frequency, i)
    return list(signals)


def harmonic_controller(N):

    def update(x):
        N = int(x)
        for phase in phases:
            axes = harmonic(amplitude=10, frequency=2, phase=phase, N=N)
            plot1.set_ydata(axes[1])
            plot1.set_xdata(axes[0])

        for f in freq:
            axes = harmonic(amplitude=10, frequency=f, phase=0, N=N)
            plot2.set_ydata(axes[1])
            plot2.set_xdata(axes[0])

        for a in ampl:
            axes = harmonic(amplitude=a, frequency=3, phase=0, N=N)
            plot3.set_ydata(axes[1])
            plot3.set_xdata(axes[0])

    fig = plt.figure(figsize=(15, 7))
    
    # 2a
    phases = [0, pi / 6, pi / 4, pi / 2, pi]
    plt.subplot(3, 1, 1)
    for phase in phases:
        axes = harmonic(amplitude=10, frequency=2, phase=phase, N=N)
        plot1, = plt.plot(axes[0], axes[1], label='${}={}$'.format('ф', round(phase, 2)))

    plt.title("Задание 2.a. A, f - const")
    plt.grid(True)
    plt.legend(loc='lower right')

    # 2b
    freq = [5, 4, 2, 6, 3]
    plt.subplot(3, 1, 2)
    for f in freq:
        axes = harmonic(amplitude=10, frequency=f, phase=0, N=N)
        plot2, = plt.plot(axes[0], axes[1], label='${}={}$'.format('f', f))

    plt.title("Задание 2.б. A, ф - const")
    plt.grid(True)
    plt.legend(loc='lower right')

    # 2c
    ampl = [2, 3, 6, 5, 1]
    plt.subplot(3, 1, 3)
    for a in ampl:
        axes = harmonic(amplitude=a, frequency=3, phase=0, N=N)
        plot3, = plt.plot(axes[0], axes[1], label='${}={}$'.format('A', a))

    plt.title("Задание 2.c. f, ф - const")
    plt.grid(True)
    plt.legend(loc='lower right')

    axes = plt.axes([0.05, 0.9, 0.25, 0.03])
    slider = Slider(axes, '${}$'.format('N'), 32, 2048, valinit=N, valfmt=r'$%1.2f$')
    slider.on_changed(update)

    return slider


def main():

    N = 512
    keep1 = harmonic_controller(N)

    # 3
    params = [
        (1, 1, 0),
        (1, 2, pi / 4),
        (1, 3, pi / 6),
        (1, 4, 2 * pi),
        (1, 5, pi)
    ]
    keep = polyharmonic_controller(params, N)


    # 4
    fig = plt.figure(figsize=(15, 7))
    plt.title("Задание 4")
    plt.grid(True)
    plt.plot(polyharmonic_linear(amplitude=10, frequency=1, phase=0, N=N))

    plt.show()


if __name__ == '__main__':
    main()