import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')
sns.set_context("poster")


class Point:
    def __init__(self, width, factor,random_V):
        self.x = random.uniform(-width, -width + width/factor)
        self.y = random.uniform(-width, width)
        self.vx = random.uniform(-random_V, random_V)
        self.vy = random.uniform(-random_V, random_V)
        self.factor = factor
        self.width = width
        self.coordinates = []

    def move(self, round):
        self.wall(round)
        self.x += self.vx
        self.y += self.vy

    def wall(self, round):
        if round < 60: # dlugosc trwania sciany
            if (self.x + self.vx <= -self.width) or (self.x + self.vx >= 2 * self.width / self.factor - self.width):
                self.vx = -self.vx
        else:
            if (self.x + self.vx <= -self.width) or (self.x + self.vx >= self. width):
                self.vx = -self.vx
        if (self.y + self.vy <= -self.width) or (self.y + self.vy >= self.width):
            self.vy = -self.vy

    def state_position(self):
        self.coordinates = []
        x = -1
        y = -1
        for i in range(self.factor):
            if self.x == self.width:
                x = self.factor - 1
            if self.y == self.width:
                y = self.factor - 1
            if i * 2 * self.width / self.factor - self.width <= self.x < (i + 1) * 2 * self.width / self.factor\
                    - self.width:
                x = i
                if y != -1:
                    break
            if i * 2 * self.width / self.factor - self.width <= self.y < (i + 1) * 2 * self.width / self.factor\
                    - self.width:
                y = i
                if x != -1:
                    break
        self.coordinates.append(x)
        self.coordinates.append(y)

    def state_speed(self, W):
        x = -1
        y = -1
        for i in range(self.factor):
            if self.vx == W:
                x = self.factor - 1
            if self.vy == W:
                y = self.factor - 1
            if i * 2 * W / self.factor - W <= self.vx < (i + 1) * 2 * W / self.factor - W:
                x = i
                if y != -1:
                    break
            if i * 2 * W / self.factor - W <= self.vy < (i + 1) * 2 * W / self.factor - W:
                y = i
                if x != -1:
                    break
        self.coordinates.append(x)
        self.coordinates.append(y)


class Board:
    def __init__(self, width, factor, number,random_V):
        self.points_list = []
        self.width = width
        for i in range(number):
            point = Point(self.width, factor,random_V)
            self.points_list.append(point)

    def update(self):
        for point in self.points_list:
            point.move()

    def check_collision(self,W):
        for PointA in range(len(self.points_list)):
            for PointB in range(PointA + 1, len(self.points_list)):
                vec = [(self.points_list[PointB].x + self.points_list[PointB].vx)
                       - (self.points_list[PointA].x + self.points_list[PointA].vx),
                       (self.points_list[PointB].y + self.points_list[PointB].vy)
                       - (self.points_list[PointA].y + self.points_list[PointA].vy)]
                distance = length(vec)
                if distance < 0.4:
                    collision(self.points_list[PointA], self.points_list[PointB])


def length(A):  # dlugosc wektora
    return math.sqrt(A[0] ** 2 + A[1] ** 2)


def scalar(A, B):  # iloczyn skalarny
    return A[0] * B[0] + A[1] * B[1]


def collision(A, B):  # zderzenie dwoch punktow

    vec_ab = [B.x - A.x, B.y - A.y]
    len_ab = length(vec_ab)
    versor = [vec_ab[0] / (len_ab + 0.00000001), vec_ab[1] / (len_ab + 0.00000001)]
    vec_va = [A.vx, A.vy]
    vec_vb = [B.vx, B.vy]
    scalar_a = scalar(vec_va, versor)
    scalar_b = scalar(vec_vb, versor)
    VAR = [scalar_a * versor[0], scalar_a * versor[1]]
    VBR = [scalar_b * versor[0], scalar_b * versor[1]]
    VAP = [vec_va[0] - VAR[0], vec_va[1] - VAR[1]]
    VBP = [vec_vb[0] - VBR[0], vec_vb[1] - VBR[1]]
    A.vx = VBR[0] + VAP[0]
    A.vy = VBR[1] + VAP[1]
    B.vx = VAR[0] + VBP[0]
    B.vy = VAR[1] + VBP[1]

def number_of_states(factor, points_list):
    states = []
    numbers = []
    for i in range(factor):
        for j in range(factor):
            for k in range(factor):
                for l in range(factor):
                    states.append([i, j, k, l])
    for i in range(len(states)):
        numbers.append(0)
    for item in points_list:
        numbers[states.index(item.coordinates)] += 1
    return numbers


def calculate_max_speed(points_list):  # funkcja obliczajaca W dla ukladu
    n = len(points_list)
    w1 = 0
    w2 = 0
    for i in range(n):
        w1 += math.fabs(points_list[i].vx)
        w2 += math.fabs(points_list[i].vy)
    if w1 > w2:
        return w1
    return w2


def count_entropy(states):
    entropy = sum(states) * (math.log(sum(states)) - 1)
    for i in states:
        entropy -= (math.log(math.factorial(i)))
    return entropy


def live_plotter(points_list, points, width, spaces, max_speed, y, line):
    x = list(range(len(y)))
    n = len(points_list)
    ticks = list(range(-width, width, (2 * width) // spaces))
    plot_x = []
    plot_y = []
    for i in range(n):
        plot_x.append(points_list[i].x)
        plot_y.append(points_list[i].y)
    if points == [] and line == []:
        plt.ion()
        fig,ax = plt.subplots(1,2, figsize=[30,15])
        line, = ax[1].plot(x, y, 'c')
        ax[0].set_xlim([-width, width])
        ax[0].set_ylim([-width, width])
        ax[1].set_xlim([0,15])
        ax[1].set_ylim([0,100])
        points, = ax[0].plot(plot_x, plot_y, 'co', marker="o", markersize=7) # rozmiar kulek
        ax[0].set_xticks(ticks)
        ax[0].set_yticks(ticks)
        ax[0].set_aspect('equal', 'box')
        plt.show()
    line.set_ydata(y)
    if np.min(y) <= line.axes.get_ylim()[0] or np.max(y) >= line.axes.get_ylim()[1]:
        plt.ylim([0, 1.25*(np.max(y) + np.std(y))])
    points.set_data(plot_x, plot_y)
    plt.pause(1 / (17 * max_speed)) # odswiezanie wykresu 
    return points, line


def main():
    width = 20
    factor = 8
    number = 400
    random_V = 0.15
    board = Board(width, factor, number, random_V)
    max_speed = calculate_max_speed(board.points_list)

    for item in board.points_list:
        item.state_position()
        item.state_speed(max_speed)
    points = []  # do not touch, used in live_plotter
    line = []  # for entropy plot
    entropy = []  # entropy values list, must always be the same length
    for i in range(15):
        entropy.append(0)
    round = 0
    while True:
        board.check_collision(max_speed)
        for item in board.points_list:
            item.move(round)
            item.state_position()
            item.state_speed(max_speed)
        if round % 16 == 3: #czestosc aktualizacji entropii
            states_number = number_of_states(factor, board.points_list)
            entropy.pop(0)
            entropy.append(count_entropy(states_number))  # next entropy value
        # 1.list of points, 2. new_points, 3. size of board, 4. Number of fields, 5. W, 6.entropy list, 7.line
        points, line = live_plotter(board.points_list, points, width, factor, max_speed, entropy, line)
        print(round)
        round += 1


main()
