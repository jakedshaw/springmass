import settings as s
import numpy as np
from matplotlib import pyplot as plt


def plot_ani(s1, s2, t, save, num, tails):
    """generates animated and 3d plot"""
    a = max([max([abs(max(s1.x[0, :] + s1.x[0, 0], key=abs)), abs(max(s2.x[0, :] + s2.x[0, 0], key=abs))]), (max([abs(max(s1.x[1, :] + s1.x[1, 0], key=abs)), abs(max(s2.x[1, :] + s2.x[1, 0], key=abs))]) / 2)])

    fig, ax = plt.subplots(num='Animated Plot')
    ax.set(xlabel='x position (m)', ylabel='y position (m)', title='Spring Oscillation in two Dimensions', xlim=[-a, a], ylim=[-2 * a, 0])
    plt.figtext(.022, .025, f' dt = {t.dt} s\n%ΔE = {t.delta_e} %')
    skip_constant = int(5/(t.dt*100))
    sn = int((t.sn-1)/skip_constant)

    j = []
    for i in np.arange(sn):
        i *= skip_constant
        x = (0, s1.x[0, i] + s1.x[0, 0], s2.x[0, i] + s2.x[0, 0])
        y = (0, s1.x[1, i] + s1.x[1, 0], s2.x[1, i] + s2.x[1, 0])

        if tails == 1:
            j, k = [], 1
            while k < 5000:
                m = i - k
                if m > 0:
                    j.append(m)
                k += 1
        else:
            j.append(i)

        f0 = ax.scatter(x, y, c='black')
        if not tails == 2:
            f1, = ax.plot(s1.x[0, j] + s1.x[0, 0], s1.x[1, j] + s1.x[1, 0], c='#1f77b4')
            f2, = ax.plot(s2.x[0, j] + s2.x[0, 0], s2.x[1, j] + s2.x[1, 0], c='#ff7f0e')
        f3, = ax.plot(x, y, c='black')
        f4 = plt.figtext(.8, .8, '%.2f s' % t.time[i])
        plt.draw()
        plt.pause(0.005)  # If simulation too fast/slow, change value
        f0.remove()
        if not tails == 2:
            f1.remove()
            f2.remove()
        f3.remove()
        f4.remove()

    ax.plot(s1.x[0, j], s1.x[1, j], c='#1f77b4')
    ax.plot(s2.x[0, :] + s2.x[0, 0], s2.x[1, :] + s2.x[1, 0], c='#ff7f0e')

    if save == 'y':
        plt.savefig(f'trials/trial_{num}/{num}_2d_traj.png')

    nn = plt.subplot(projection='3d', xlim=[0, t.time[-1]])
    nn.plot3D(t.time, s1.x[0, :] + s1.x[0, 0], s1.x[1, :] + s1.x[1, 0], label='Spring 1')
    nn.plot3D(t.time, s2.x[0, :] + s2.x[0, 0], s2.x[1, :] + s2.x[1, 0], label='Spring 2')
    nn.set(xlabel='time (s)', ylabel='x position (m)', zlabel='y position (m)', title='Spring Oscillation in two Dimensions')

    if save == 'y':
        plt.savefig(f'trials/trial_{num}/{num}_3d_traj.png')
    plt.show()


def plot(s1, s2, t, save, num):
    """generates trajectory plot"""

    plt.figure(num='Trajectory')

    top = plt.subplot(2, 1, 1, xlim=[0, t.time[-1]])
    top.plot(t.time, s1.x[1, :] + s1.x[1, 0], label='Spring 1')
    top.plot(t.time, s2.x[1, :] + s2.x[1, 0], label='Spring 2')
    top.set(ylabel='y position (m)', title='Spring Oscillation in two Dimensions')

    b = plt.subplot(2, 1, 2, xlim=[0, t.time[-1]])
    b.plot(t.time, s1.x[0, :] + s1.x[0, 0], label='Spring 1')
    b.plot(t.time, s2.x[0, :] + s2.x[0, 0], label='Spring 2')
    b.set(ylabel='x position (m)', xlabel='time (s)')

    plt.figtext(.022, .025, f' dt = {t.dt} s\n%ΔE = {t.delta_e} %')

    if save == 'y':
        plt.savefig(f'trials/trial_{num}/{num}_2d_proj.png')
    plt.show()


def fourier_plot(ft, save, num, tt):
    """generates fourier transformation plot"""

    plt.figure(num='Fourier Transformation')

    t = plt.subplot(2, 1, 1, xlim=[0.05, 4])
    t.plot(ft[4], abs(ft[2]), label='Spring 1 y')
    t.plot(ft[4], abs(ft[3]), label='Spring 2 y')
    t.set(ylabel='y direction', title='Spring Oscillation Fourier Transform')

    b = plt.subplot(2, 1, 2, xlim=[0.05, 4])
    b.plot(ft[4], abs(ft[0]), label='Spring 1 x')
    b.plot(ft[4], abs(ft[1]), label='Spring 2 x')
    b.set(xlabel='frequency (hz)', ylabel='x direction')

    plt.figtext(.022, .025, f' dt = {tt.dt} s\n%ΔE = {tt.delta_e} %')

    if save == 'y':
        plt.savefig(f'trials/trial_{num}/{num}_fourier.png')
    plt.show()


def re_run(set_vec):
    """asks if the simulation should be rerun"""
    print('Rerun last simulation? (y/n) ', end='')
    a = input()
    if a == 'y':
        set_vec[3], set_vec[4] = 'n', 'y'
        s.clear()
        return set_vec
    elif a == 'n':
        s.clear()
        return set_vec
    else:
        s.clear()
        print('Invalid Entry!\n')
        return re_run(set_vec)


def run_plot(s1, s2, t, ft, set_vec):  # dt, code, tails, save, plot, load, num
    """runs plots"""
    while set_vec[4] == 'y':
        print(' #     Mass(kg)    k(N/m)    length(m)\n---   --------   ------   ---------')
        print(f'{s1}\n{s2}\n\n {t}\n\nRunning... (Close Figures to Continue)')
        plot_ani(s1, s2, t, set_vec[3], set_vec[6], set_vec[2])
        plot(s1, s2, t, set_vec[3], set_vec[6])
        fourier_plot(ft, set_vec[3], set_vec[6], t)
        set_vec[4] = 'n'
        s.clear()
        set_vec = re_run(set_vec)
    s.clear()
