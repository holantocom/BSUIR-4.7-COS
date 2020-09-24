import math

from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

N = 32
KN = lambda N: (3 * N) // 4
PHASES = {'0': 0, r'\pi/2': math.pi / 2}
EXPECTED_ROOT_MEAN_SQUARE = 0.707
EXPECTED_AMPLITUDE = 1

LABELS = [
    'Фурье-(Погр-А)',
    'Погр-СКЗ-const',
    'Погр-СКЗ-dynamic'
]


def amplitude_by_fourier(sequence):
    N = len(sequence)
    sin_sum, cos_sum = 0, 0
    for i, y in enumerate(sequence):
        angle = 2 * math.pi * i / N
        sin_sum += y * math.sin(angle)
        cos_sum += y * math.cos(angle)
    sin_sum *= 2/N
    cos_sum *= 2/N
    return math.sqrt(sin_sum**2 + cos_sum**2)


def harmonic_point(x, N, phase):
    return math.sin((2 * math.pi * x) / N + phase)


def root_mean_square_constant(sequence):
    N = len(sequence)
    return math.sqrt(1 / (N + 1) * sum(x ** 2 for x in sequence))


def root_mean_square_dynamic(sequence):
    N = len(sequence)
    return math.sqrt(1 / (N + 1) * sum(x ** 2 for x in sequence) - (1 / (N + 1) * sum(sequence)) ** 2)


def harmonic_list(M, N, phase):
    sequence = []
    for i in range(M):
        sequence.append(harmonic_point(i, N, phase))
    return sequence


def calc_parameters(KN, N, phase):
    #graphs = {"rmsc": [], "rmsd": [], "rmsc_error": [], "rmsd_error": [], "fourier_error": []}
    graphs = {"rmsc_error": [], "rmsd_error": [], "fourier_error": []}
    K = KN(N)
    for x in range(K, 5 * N):
        sequence = harmonic_list(x, N, phase)

        rmsc = root_mean_square_constant(sequence)
        rmsd = root_mean_square_dynamic(sequence)
        fourier = amplitude_by_fourier(sequence)

        # graphs["rmsc"].append(rmsc)
        # graphs["rmsd"].append(rmsd)
        graphs["rmsc_error"].append({"x": x / N, "y": EXPECTED_ROOT_MEAN_SQUARE - rmsc})
        graphs["rmsd_error"].append({"x": x / N, "y": EXPECTED_ROOT_MEAN_SQUARE - rmsd})
        graphs["fourier_error"].append({"x": x / N, "y": EXPECTED_AMPLITUDE - fourier})

    return graphs


def point_converter(graph):
    xticks = []
    yticks = []
    for point in graph:
        xticks.append(point["x"])
        yticks.append(point["y"])

    return {"x": xticks, "y": yticks}


def graph_controller(K, N):

    def update(x):
        X = int(x)
        l = 0
        for i, phase_unit in enumerate(PHASES.items()):
            desc, phase = phase_unit
            graphs = calc_parameters(KN, X, phase)

            for j, graph in graphs.items():
                points = point_converter(graph)
                plots[l].set_xdata(points["x"])
                plots[l].set_ydata(points["y"])
                l += 1

    plots = []
    fig = plt.figure(figsize=(15, 7))
    plt.grid(True)

    for i, phase_unit in enumerate(PHASES.items()):
        desc, phase = phase_unit
        graphs = calc_parameters(KN, N, phase)
        plt.subplot(1, 2, i + 1)
        l = 0

        for j, graph in graphs.items():
            points = point_converter(graph)
            tempPlot, = plt.plot(points["x"], points["y"], label='${}$'.format(LABELS[l]))
            plots.append(tempPlot)
            l += 1
        plt.legend(loc='best')


    axes = plt.axes([0.37, 0.93, 0.25, 0.03])
    slider = Slider(axes, '${}$'.format('N'), 2, 128, valinit=N, valfmt=r'$%d$')
    slider.on_changed(update)

    return slider


def main():
    keep = graph_controller(KN, N)
    plt.show()


if __name__ == '__main__':
    main()
