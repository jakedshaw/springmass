from numpy import array, append, reshape, float64, arange
from scipy.fftpack import rfft, rfftfreq
from datetime import datetime
from math import hypot
from os import system


def calc_length(inc1, inc2):
    """calculates spring length"""
    inc1.append(hypot(inc1[5], inc1[6]))
    inc2.append(hypot(inc2[5] - inc1[5], inc2[6] - inc1[6]))
    return inc1, inc2


def euler_pos_vel(s1, s2, t):
    """generates position and velocity vectors"""
    res, dp = 1000, int((t.sn - 1) / 100)
    a, b, i, j, k, fin = 0, 1, 0, 0, 0, (arange(res) + 1)
    x1, v1, x2, v2, dt, k1, l1, m1, k2, l2, m2 = s1.x, s1.v, s2.x, s2.v, t.dt, s1.k, s1.len, s1.m, s2.k, s2.len, s2.m
    print('|                    |  0%')
    while i < t.sn-1:
        x1 = append(x1, reshape((x1[:, j] + v1[:, j] * dt), (2, 1)), axis=1)
        v1 = append(v1, reshape((v1[:, j] + ode1(x1[:, j], x2[:, j], k1, l1, m1, k2, l2) * dt), (2, 1)), axis=1)
        x2 = append(x2, reshape((x2[:, j] + v2[:, j] * dt), (2, 1)), axis=1)
        v2 = append(v2, reshape((v2[:, j] + ode2(x1[:, j], x2[:, j], k2, l2, m2) * dt), (2, 1)), axis=1)
        if i % res == 0 and i >= res:
            per = int(i/dp)
            if per % 10 == 0:
                if not per == a:
                    _ = system('clear')
                    print('|', end='')
                    for x in range(b):
                        print('**', end='')
                    b += 1
                    c = 11 - b
                    for x in range(c):
                        print('  ', end='')
                    print(f'| {per}%')
                    a = per
            s1.x, s1.v, s2.x, s2.v = append(s1.x, x1[:, fin], axis=1), append(s1.v, v1[:, fin], axis=1), append(s2.x, x2[:, fin], axis=1), append(s2.v, v2[:, fin], axis=1)
            x1, v1, x2, v2 = array(([s1.x[0, -1]], [s1.x[1, -1]])), array(([s1.v[0, -1]], [s1.v[1, -1]])), array(([s2.x[0, -1]], [s2.x[1, -1]])), array(([s2.v[0, -1]], [s2.v[1, -1]]))
            k += 1
        j = i - (k * res)
        i += 1
    _ = system('clear')
    print('|********************| 100%')
    s1.x, s1.v, s2.x, s2.v = append(s1.x, x1, axis=1), append(s1.v, v1, axis=1), append(s2.x, x2, axis=1), append(s2.v, v2, axis=1)
    return s1, s2


def ode1(x1, x2, k1, l1, m1, k2, l2):
    """runs ODE1"""
    x21 = hypot(x2[0] - x1[0], x2[1] - x1[1])
    return -k1 * (hypot(x1[0], x1[1]) - l1) * x1 / (m1 * hypot(x1[0], x1[1])) + k2 * (x21 - l2) * (x2 - x1) / (m1 * x21) + array([0, -9.81])


def ode2(x1, x2, k2, l2, m2):
    """runs ODE2"""
    x21 = hypot(x2[0] - x1[0], x2[1] - x1[1])
    return -k2 * (x21 - l2) * (x2 - x1) / (m2 * x21) + array([0, -9.81])


def calc_energy(s1, s2, t):
    """calculates system energy"""
    energy = []
    for i in [0, t.sn-1]:
        energy.append(float64((9.81 * s1.m * s1.x[1, i]) + (9.81 * s2.m * s2.x[1, i])).item() + (s1.m * (hypot(s1.v[0, i], s1.v[1, i]))**2)/2 + (s2.m * (hypot(s2.v[0, i], s2.v[1, i]))**2)/2 + (s1.k*(s1.len-hypot(s1.x[0, i], s1.x[1, i]))**2)/2 + (s2.k*(hypot(s2.x[0, i]-s1.x[0, i], s2.x[1, i]-s1.x[1, i])-s2.len)**2)/2)
    delta_e = (energy[0] - energy[1]) / ((energy[0] + energy[1]) / 2)
    t.delta_e = '%.3f' % delta_e
    return t


def fourier_calc(s1, s2, t):
    """calculates rapid fft"""
    x1f = rfft(s1.x[0, :] + s1.x0)
    x2f = rfft(s2.x[0, :] + s2.x0)
    y1f = rfft(s1.x[1, :] + s1.y0)
    y2f = rfft(s2.x[1, :] + s2.y0)
    tf = rfftfreq(t.sn, t.dt)
    return array((x1f, x2f, y1f, y2f, tf))


def data_array(s1, s2, t, ft):
    """creates data array"""
    sst = array((s1, s2, t), dtype=object)
    dat_arr = array((sst, ft), dtype=object)
    return dat_arr


def run_calc(s1, s2, t):
    """run data generation"""
    begin = datetime.now()
    s1, s2 = euler_pos_vel(s1, s2, t)
    pro_time = datetime.now() - begin
    print(f'processing time: {pro_time}\n')
    t = calc_energy(s1, s2, t)
    ft = fourier_calc(s1, s2, t)
    dat_arr = data_array(s1, s2, t, ft)
    return s1, s2, ft, dat_arr
