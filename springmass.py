import numpy as np
from matplotlib import pyplot as plt
from math import hypot
from os import system

class Spring():
    """A Spring Class"""

    def __init__(self, m, k, l, vx0, vy0, x0, y0):
        """Attributes for the Spring Mass"""
        self.m = m
        self.k = k
        self.l = l
        self.x0 = x0
        self.y0 = y0
        self.v = np.array(([vx0], [vy0]))
        self.x = np.array(([x0], [y0]))

    def __str__(self):
        """A string describing the object"""
        return f"M = {self.m} kg, k = {self.k} N/m, l = {self.l} m"


class Time():
    """A Time Vector Class"""

    def __init__(self, sec, dt):
        """Attributes for Time Vector"""
        self.sec = sec
        self.dt = dt
        self.sn = int(sec * (1/dt) + 1)
        self.time = np.linspace(0, sec, self.sn)

    def __str__(self):
        """A string describing the object"""
        return f"sec = {self.sec} s, dt = {self.dt} s, sn = {self.sn}"


def euler_pos_vel(s1, s2, t):
    """Generates the position and velocity vectors"""
    i = 0
    while i < t.sn-1:
        x1 = s1.x[:, i] + s1.v[:, i] * t.dt
        v1 = s1.v[:, i] + ode1(s1, s2, i) * t.dt
        x2 = s2.x[:, i] + s2.v[:, i] * t.dt
        v2 = s2.v[:, i] + ode2(s1, s2, i) * t.dt
        s1.x = np.append(s1.x, np.array(([x1[0]], [x1[1]])), axis=1)
        s1.v = np.append(s1.v, np.array(([v1[0]], [v1[1]])), axis=1)
        s2.x = np.append(s2.x, np.array(([x2[0]], [x2[1]])), axis=1)
        s2.v = np.append(s2.v, np.array(([v2[0]], [v2[1]])), axis=1)
        i += 1
    return s1, s2


def ode1(s1, s2, i):
    """Runs ODE_1"""
    return -s1.k * (hypot(s1.x[0, i], s1.x[1, i]) - s1.l) * s1.x[:, i] / (s1.m * hypot(s1.x[0, i], s1.x[1, i])) + s2.k * (hypot(s2.x[0, i] - s1.x[0, i], s2.x[1, i] - s1.x[1, i]) - s2.l) * (s2.x[:, i] - s1.x[:, i]) / (s1.m * hypot(s2.x[0, i] - s1.x[0, i], s2.x[1, i] - s1.x[1, i])) + np.array([0, -9.81])


def ode2(s1, s2, i):
    """Runs ODE_2"""
    return -s2.k * (hypot(s2.x[0, i] - s1.x[0, i], s2.x[1, i] - s1.x[1, i]) - s2.l) * (s2.x[:, i] - s1.x[:, i]) / (s2.m * hypot(s2.x[0, i] - s1.x[0, i], s2.x[1, i] - s1.x[1, i])) + np.array([0, -9.81])


def get_num():
    """Gets last image number, adds one, writes and returns the number"""
    filename = 'assets/imgnum'
    num = np.loadtxt(filename)
    num += 1
    number = np.array([int(num)])
    np.savetxt(filename, number)
    return int(num)


def reset_num():
    """Resets and prints the image number"""
    filename = 'assets/imgnum'
    num = np.array([0])
    system('rm -r assets')
    system('mkdir assets')
    np.savetxt(filename, num)



def plot_ani(s1, s2, t):
    """Generates Second Plot - Animated"""
    fig, ax = plt.subplots(num='Animated Plot')
    ax.set(xlabel='x position (m)', ylabel='y position (m)', title='Spring Oscillation in two Dimensions', xlim=[-5, 5], ylim=[-10, 1])
    sn = int((t.sn-1)/50)

    for i in np.arange(sn):
        x = (0, s1.x[0, i*50], s2.x[0, i*50] + s2.x0)
        y = (0, s1.x[1, i*50], s2.x[1, i*50] + s2.y0)
        frame = ax.scatter(x, y, c='black')
        frame2, = ax.plot(x, y, c='black')
        plt.draw()
        plt.pause(0.05)
        frame.remove()
        frame2.remove()


def plot(s1, s2, t):
    """Generates First Plot"""

    n = plt.subplot(3, 1, 1, projection='3d') # North Plot
    n.plot3D(t.time, s1.x[0, :], s1.x[1, :], label='Spring 1')
    n.plot3D(t.time, s2.x[0, :] + s2.x0, s2.x[1, :] + s2.y0, label='Spring 2')
    n.set(xlabel='time (s)', ylabel='x position (m)', zlabel='y position (m)', title='Spring Oscillation in two Dimensions')

    m = plt.subplot(3, 1, 2) # Middle Plot
    m.plot(t.time, s1.x[1, :], label='Spring 1')
    m.plot(t.time, s2.x[1, :] + s2.y0, label='Spring 2')
    m.set(xlabel='time (s)', ylabel='y position (m)')

    s = plt.subplot(3, 1, 3) # South Plot
    s.plot(t.time, s1.x[0, :], label='Spring 1')
    s.plot(t.time, s2.x[0, :] + s2.x0, label='Spring 2')
    s.set(xlabel='time (s)', ylabel='x position (m)')

    number = get_num()
    plt.savefig(f'assets/springmass_{number}.png')
    plt.show()