import springmass as spring

def run_prog():
    """Runs Simulation"""
    # Initial Conditions
    #print('Careful with values!
    #print('M 1 in kg = ', end='')
    M1 = 2 #int(input())
    #print('k 1 in N/m = ', end='')
    k1 = 20 #int(input())
    #print('M 2 in kg = ', end='')
    M2 = 1 #int(input())
    #print('k 2 in N/m = ', end='')
    k2 = 15 #int(input())
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
