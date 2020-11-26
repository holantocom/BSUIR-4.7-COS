from matplotlib import pyplot as plt
import numpy as np
from random import gauss
from matplotlib.widgets import Slider, Button, RadioButtons
import time


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
    'Медианный фильтр': averaged_antialiasing
}

def main():

    fig = plt.figure(figsize=(10, 4))
    img = plt.imread('website.jpg')
    rows, cols, colors = img.shape

    axes = plt.axes([0.05, 0.7, 0.25, 0.03])
    slider = Slider(axes, '${}$'.format('Ядро'), 1, 17, valinit=3, valfmt=r'$%d$', valstep=2)

    rax = plt.axes([0.05, 0.4, 0.25, 0.25])
    radio = RadioButtons(rax, ('Без редактирования', 'Медианный фильтр', 'Размытие'), active=0)

    plt.axes([0.27, 0.1, 0.8, 0.8])
    plt.xticks([])
    plt.yticks([])
    image = plt.imshow(img)

    def update(label):
        window = slider.val
        m = filter_algorithm(img, window, LABELS[label])
        image.set_data(m)
        image.axes.figure.canvas.draw()

    radio.on_clicked(update)
    plt.show()

    # mu, sigma = 0, 0.84089642  # mean and standard deviation
    # s = np.random.normal(mu, sigma, (7, 7))
    # print(s)


if __name__ == '__main__':
    main()
