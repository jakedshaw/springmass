from numpy import array, append, reshape, float64, arange, hypot
from scipy.fftpack import rfft, rfftfreq
from datetime import datetime
from os import system
from numba import njit


def clear():
    """Clears Terminal"""
    _ = system('clear')


def calc_length(inc1, inc2):
    """calculates spring length"""
    inc1.append(hypot(inc1[5], inc1[6]))
    inc2.append(hypot(inc2[5] - inc1[5], inc2[6] - inc1[6]))
    return inc1, inc2


def euler_pos_vel(s1, s2, dt, k1, l1, m1, k2, l2, m2, final):
    """generates position and velocity vectors"""
    ax, ay, bx, by, cx, cy, dx, dy = s1.x[0], s1.x[1], s1.v[0], s1.v[1], s2.x[0], s2.x[1], s2.v[0], s2.v[1]
    xx1, xy1, vx1, vy1, xx2, xy2, vx2, vy2 = [], [], [], [], [], [], [], []
    i = 0
    print('|  0%')
    while i < final:

        norm = hypot(cx - ax, cy - ay)

        ode1x = -k1 * (hypot(ax, ay) - l1) * ax / (m1 * hypot(ax, ay)) + k2 * (norm - l2) * (cx - ax) / (m1 * norm)
        ode1y = -k1*(hypot(ax, ay)-l1)*ay/(m1*hypot(ax, ay)) + k2*(norm - l2)*(cy - ay)/(m1 * norm) - 9.81

        ode2x = -k2 * (norm - l2) * (cx - ax) / (m2 * norm)
        ode2y = -k2 * (norm - l2) * (cy - ay) / (m2 * norm) - 9.81

        ax = ax + bx * dt
        bx = bx + ode1x * dt
        cx = cx + dx * dt
        dx = dx + ode2x * dt

        ay = ay + by * dt
        by = by + ode1y * dt
        cy = cy + dy * dt
        dy = dy + ode2y * dt

        xx1.append(ax)
        vx1.append(bx)
        xx2.append(cx)
        vx2.append(dx)

        xy1.append(ay)
        vy1.append(by)
        xy2.append(cy)
        vy2.append(dy)

        i += 1
    print('| 100 %')
    return xx1, xy1, vx1, vy1, xx2, xy2, vx2, vy2


@njit(nogil=True, parallel=True)
def euler_pos_vel1(x1, v1, x2, v2, dt, k1, l1, m1, k2, l2, m2, final):
    """generates position and velocity vectors"""
    acc = array([0, -9.81])
    res, dp = 1000, int(final / 100)
    s1x, s1v, s2x, s2v = x1, v1, x2, v2
    e, f, i, j, k, fin = 0, 1, 0, 0, 0, (arange(res) + 1)
    print('|  0%')
    while i < final:

        norm = hypot(x2[0, j] - x1[0, j], x2[1, j] - x1[1, j])
        ode1 = -k1 * (hypot(x1[0, j], x1[1, j]) - l1) * x1[:, j] / (m1 * hypot(x1[0, j], x1[1, j])) + k2 * (norm - l2) * (x2[:, j] - x1[:, j]) / (m1 * norm) + acc
        ode2 = -k2 * (norm - l2) * (x2[:, j] - x1[:, j]) / (m2 * norm) + acc

        a = reshape(x1[:, j] + v1[:, j] * dt, (2, 1))
        b = reshape(v1[:, j] + ode1 * dt, (2, 1))
        c = reshape(x2[:, j] + v2[:, j] * dt, (2, 1))
        d = reshape(v2[:, j] + ode2 * dt, (2, 1))

        x1 = append(x1, a, axis=1)
        v1 = append(v1, b, axis=1)
        x2 = append(x2, c, axis=1)
        v2 = append(v2, d, axis=1)

        if i % res == 0 and i >= res:
            per = int(i/dp)
            if per % 10 == 0:
                if not per == e:
                    print('| ', per, '%')
                    e = per
            s1x, s1v, s2x, s2v = append(s1x, x1[:, fin], axis=1), append(s1v, v1[:, fin], axis=1), append(s2x, x2[:, fin], axis=1), append(s2v, v2[:, fin], axis=1)
            x1, v1, x2, v2 = array(([s1x[0, -1]], [s1x[1, -1]])), array(([s1v[0, -1]], [s1v[1, -1]])), array(([s2x[0, -1]], [s2x[1, -1]])), array(([s2v[0, -1]], [s2v[1, -1]]))
            k += 1
        j = i - (k * res)
        i += 1
    print('| 100 %')
    s1x, s1v, s2x, s2v = append(s1x, x1, axis=1), append(s1v, v1, axis=1), append(s2x, x2, axis=1), append(s2v, v2, axis=1)
    return s1x, s1v, s2x, s2v


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
    x1f = rfft(s1.x[0, :] + s1.x[0, 0])
    x2f = rfft(s2.x[0, :] + s2.x[0, 0])
    y1f = rfft(s1.x[1, :] + s1.x[1, 0])
    y2f = rfft(s2.x[1, :] + s2.x[1, 0])
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
    x1, v1, x2, v2, dt, k1, l1, m1, k2, l2, m2 = s1.x, s1.v, s2.x, s2.v, t.dt, s1.k, s1.len, s1.m, s2.k, s2.len, s2.m
    final = t.sn-1
    # xx1, xy1, vx1, vy1, xx2, xy2, vx2, vy2 = euler_pos_vel(s1, s2, dt, k1, l1, m1, k2, l2, m2, final)
    # s1.x, s1.v, s2.x, s2.v = array((xx1, xy1)), array((vx1, vy1)), array((xx2, xy2)), array((vx2, vy2))
    s1.x, s1.v, s2.x, s2.v = euler_pos_vel1(x1, v1, x2, v2, dt, k1, l1, m1, k2, l2, m2, final)
    pro_time = datetime.now() - begin
    clear()
    print(f'processing time: {pro_time}\n')
    t = calc_energy(s1, s2, t)
    ft = fourier_calc(s1, s2, t)
    dat_arr = data_array(s1, s2, t, ft)
    return s1, s2, ft, dat_arr
