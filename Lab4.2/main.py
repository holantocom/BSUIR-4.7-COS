from matplotlib import pyplot as plt
import numpy as np
from random import gauss
from matplotlib.widgets import Slider, Button, RadioButtons
from tkinter import filedialog


convolution = np.array([
        [[0.5], [0.75], [0.5]],
        [[0.75], [1], [0.75]],
        [[0.5], [0.75], [0.5]]
])

clarity = np.array([
        [[-1], [-1], [-1]],
        [[-1], [9], [-1]],
        [[-1], [-1], [-1]]
])

gauss = np.array([
        [[0.05472157], [0.11098164], [0.05472157]],
        [[0.11098164], [0.22508352], [0.11098164]],
        [[0.05472157], [0.11098164], [0.05472157]]
])


def matrix_antialiasing(m, filter, dv):
    mul = np.multiply(m, filter)
    lev1 = np.sum(mul, axis=0)
    lev2 = np.sum(lev1, axis=0)
    ans = []
    for el in lev2:
        nel = int(el * dv)
        nel = nel if nel <= 255 else 255
        nel = nel if nel >= 0 else 0
        ans.append(nel)
    return ans


def convolution_matrix_antialiasing(m, depth):
    return matrix_antialiasing(m, convolution, 1 / 6)


def gauss_antialiasing(m, depth):
    return matrix_antialiasing(m, gauss, 1)


def improving_clarity_antialiasing(m, depth):
    return matrix_antialiasing(m, clarity, 1)


def default(m, depth):
    return m[len(m) // 2][len(m[0]) // 2]


def averaged_antialiasing(m, depth):
    plain = [[] for i in range(depth)]
    answer = []
    for row in m:
        for el in row:
            for k, v in enumerate(el):
                plain[k].append(v)

    for k, v in enumerate(plain):
        plain[k] = sorted(plain[k])
        answer.append(plain[k][len(plain[k]) // 2])

    return answer


def filter_algorithm(m, window, func):
    if not (window % 2):
        raise Exception("Sorry, even number")

    if func.__name__ != "averaged_antialiasing":
        window = 3

    answer = m.tolist()
    rows, cols, colors = m.shape
    hw = window // 2

    for i in range(hw, rows - hw):
        for j in range(hw, cols - hw):
            points = []
            for k in range(-hw, hw + 1):
                points.append(m[i + k][j - hw:j + hw + 1])
            answer[i][j] = func(points, colors)

    return answer


LABELS = {
    'Без редактирования': default,
    'Медианный фильтр': averaged_antialiasing,
    'Матрица свертки': convolution_matrix_antialiasing,
    'Улучшение четкости': improving_clarity_antialiasing,
    'Размытие по Гаусс': gauss_antialiasing
}

def main():

    fig = plt.figure(figsize=(10, 4))
    img = plt.imread('website.jpg')

    axload = plt.axes([0.05, 0.8, 0.25, 0.075])
    bload = Button(axload, 'Открыть изображение')

    axes = plt.axes([0.05, 0.7, 0.25, 0.03])
    slider = Slider(axes, '${}$'.format('Ядро'), 1, 17, valinit=3, valfmt=r'$%d$', valstep=2)

    rax = plt.axes([0.05, 0.4, 0.25, 0.25])
    radio = RadioButtons(rax, LABELS.keys(), active=0)

    plt.axes([0.27, 0.1, 0.8, 0.8])
    plt.xticks([])
    plt.yticks([])
    image = plt.imshow(img)

    def load(val):
        filename = filedialog.askopenfilename(initialdir="/", title="Image", filetypes=[("IMG", "*.jpg;*jpeg;*.png")])
        img = plt.imread(filename)
        image.set_data(img)
        image.axes.figure.canvas.draw()

    def update(label):
        window = slider.val
        m = filter_algorithm(img, window, LABELS[label])
        image.set_data(m)
        image.axes.figure.canvas.draw()

    bload.on_clicked(load)
    radio.on_clicked(update)
    plt.show()


if __name__ == '__main__':
    main()
