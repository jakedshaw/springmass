import springmass as spring


def run_prog():
    """Runs Simulation"""
    # Initial Conditions
    M1 = 0.7500  # kg
    k1 = 20.000  # N/m
    M2 = 0.5000  # kg
    k2 = 20.000  # N/m
    print('Time in sec = ', end='')
    sec = int(input())
    dt = 0.001

    # Create the Objects
    s1 = spring.Spring(M1, k1, 0.4, -0.5, -0.5, -0.2, -0.3)
    s2 = spring.Spring(M2, k2, 0.4, -1, 0, -0.2, -0.7)
    t = spring.Time(sec, dt)

    # Generate the Data
    s1, s2 = spring.euler_pos_vel(s1, s2, t)
    print('spring 1:', s1)
    print('spring 2:', s2)
    print('time:', t)

    # Plot the Data
    spring.plot_ani(s1, s2, t)
    spring.plot(s1, s2, t)

if __name__ == '__main__':
    run_prog()