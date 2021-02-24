from os import system, walk
import data
import main


def clear():
    """Clears Terminal"""
    _ = system('clear')


def simulation_time():
    try:
        print('Run for how many seconds? ', end='')
        sec = input()
        if sec < '':
            clear()
            return simulation_time()
        sec = int(sec)
        if sec <= 0:
            clear()
            print('Positive, Non-Zero Integers only!\n')
            return simulation_time()
        clear()
        return sec
    except ValueError:
        clear()
        print('Integers only!\n')
        return simulation_time()


def init_arr(a):
    """Returns Initial Conditions"""
    if a == '1':  # #s1   m1    k1     vx1    vy1    x1     y1     s2   m2     k2    vx2    vy2     x2    y2
        inc1, inc2 = [1, 0.75, 20.00, -0.50, -0.20, 0.000, -0.30], [2, 0.50, 20.00, -1.00, -0.20, 0.00, -0.80]
    elif a == '2':
        inc1, inc2 = [1, 5.00, 20.00, -0.50, -0.20, 0.000, -0.30], [2, 0.50, 20.00, -1.00, -0.20, 0.00, -0.80]
    elif a == '3':
        inc1, inc2 = [1, 10.00, 2000, 3.00, 0.000, 0.000, -5.00], [2, 0.50, 2000, 0.000, 0.000, 0.00, -6.00]
    else:
        inc1, inc2 = [1, 0.500, 20.00, 0.500, 0.000, 0.00, -0.50], [2, 0.005, 1.00, 0.000, -1.00, 0.00, -2.00]
    return inc1, inc2


def enter_data():
    """enter custom values"""
    inc1, inc2 = [1], [2]
    print("Coming Soon ('b' to go back)")
    a = input()
    if a == 'b':
        clear()
        return inc1, inc2
    else:
        clear()
        return enter_data()

    print('Careful with values! (currently a little buggy)\n #   m    k     vx    vy    x     y\n')
    for i in range(2):
        print(f' {i + 1} ', end='')
        for j in range(6):
            if i == 0:
                inc1.append(float(input()))
                clear()
                print(f'Careful with values!\n # :   m    k     vx    vy    x     y\n{inc1}', end='')
            else:
                inc2.append(float(input()))
                clear()
                print(f'Careful with values!\n # :   m    k     vx    vy    x     y\n{inc1}\n{inc2}', end='')
    clear()
    print(
        'Your Values:\n'
        ' # :   m    k     vx    vy    x     y\n'
        f'{inc1}\n'
        f'{inc2}\n\n'
        'Happy with values? (y/n) ', end=''
    )

    a = input()
    if a == 'n':
        inc1, inc2 = enter_data()
    clear()
    return inc1, inc2


def load_data(set_vec):
    """loads data"""
    try:
        print("Load which trial? ('b' to go back)\n")
        dir_num = 0
        for _, dirs, _ in walk('trials/'):
            for i in dirs:
                print(f" '{dir_num}' ", end='')
                dir_num += 1
            if dir_num == 0:
                clear()
                print('No saved files!\n')
                main.run_prog(set_vec)
        print('\n\nEnter Test Number: ', end='')
        num = input()
        if num == 'b':
            clear()
            main.select_scenario(set_vec)
        num = int(num)
        if num >= dir_num or num < 0:
            clear()
            print('No such file!\n')
            return load_data(set_vec)
        clear()
        return num
    except ValueError:
        clear()
        print('Integers only!\n')
        return load_data(set_vec)


def set_time_step(set_vec):
    """set time step"""
    print(
        "Time Step Options ('b' to go back): \n\n"
        "------------------------------------\n\n"
        " '0'     0.001 s         low        \n\n"
        " '1'     0.0001 s       medium      \n\n"
        " '2'     0.00001 s       high       \n\n"
    )

    a = input()
    if a == '0':
        set_vec[0] = 0.001
    elif a == '1':
        set_vec[0] = 0.000_1
    elif a == '2':
        set_vec[0] = 0.000_01
    elif a == 'b':
        clear()
        main.select_scenario(set_vec)
    else:
        clear()
        return set_time_step(set_vec)
    clear()
    return set_vec


def set_tails(set_vec):
    """set tails"""
    print(
        "Trajectory Options ('b' to go back):\n\n"
        "------------------------------------\n\n"
        " '0'     trajectory tracing         \n\n"
        " '1'     short trajectory tails     \n\n"
        " '2'     no tracing/tails           \n\n"
    )

    a = input()
    if a == '0':
        set_vec[2] = 0
    elif a == '1':
        set_vec[2] = 1
    elif a == '2':
        set_vec[2] = 2
    elif a == 'b':
        clear()
        main.select_scenario(set_vec)
    else:
        clear()
        return set_tails(set_vec)
    clear()
    return set_vec


def init_set(set_vec):
    """Settings Screen"""
    inc1, inc2, dat_arr = [], [], 'empty'
    # set_vec = dt, code, tails, save, plot, load, num
    print(
        "Options ('b' to go back):\n\n"
        "------------------------------------\n\n"
        " 'e' enter custom values\n\n"
        " 'l' load saved data\n\n"
        " 'd' delete saved data\n\n"
        "------------------------------------\n\n"
        " 's' change time step\n\n"
        " 't' change trajectory tracing\n\n"
    )
    a = input()
    clear()
    if a == 'q':
        clear()
        quit()
    elif a == 'e':
        inc1, inc2 = enter_data()
        main.select_scenario(set_vec) # Temporary
    elif a == 'l':
        num = load_data(set_vec)
        dat_arr = data.load_data(num)
        set_vec[3], set_vec[5] = 'n', 'y'
    elif a == 'd':
        data.reset_num()
        print('Data Deleted!\n')
        main.default_data()
    elif a == 's':
        set_vec = set_time_step(set_vec)
        main.select_scenario(set_vec)
    elif a == 't':
        set_vec = set_tails(set_vec)
        main.select_scenario(set_vec)
    elif a == 'b':
        main.select_scenario(set_vec)
    else:
        clear()
        return init_set(set_vec)
    return inc1, inc2, dat_arr, set_vec


def main_options(set_vec):
    """main options"""
    print("Select Scenario (1/2/3/4) or type 'm' for more options:  ", end='')
    a = input()
    clear()
    dat_arr = 'empty'
    if a == 'q':
        clear()
        quit()
    elif a == 'm':
        inc1, inc2, dat_arr, set_vec = init_set(set_vec)
        return inc1, inc2, dat_arr, set_vec
    elif a == '1' or a == '2' or a == '3' or a == '4':
        inc1, inc2 = init_arr(a)
        return inc1, inc2, dat_arr, set_vec
    else:
        print('Invalid Entry!\n')
        return main_options(set_vec)
