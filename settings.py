from os import system, walk
import calculations as calc
import pandas as pd
import data
import main


def clear():
    """Clears Terminal"""
    _ = system('clear')


def simulation_time():
    try:
        print('Run for how many seconds? ', end='')
        sec = input()
        clear()
        if sec < '':
            return simulation_time()
        sec = int(sec)
        if sec <= 0:
            print('Positive, Non-Zero Integers only!\n')
            return simulation_time()
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
    inc1, inc2 = calc.calc_length(inc1, inc2)
    return inc1, inc2


def check_float(spring_attributes):
    print('Careful with values! (currently a little buggy)\n\n', spring_attributes, '\n\nValue = ', end='')
    try:
        a = input()
        clear()
        a = float(a)
        return a
    except ValueError:
        clear()
        return check_float(spring_attributes)


def confirm_values(inc1, inc2, spring_attributes, set_vec):
    print('Your Values:\n\n', spring_attributes, '\n\nHappy with values? (y/n) ', end='')
    a = input()
    clear()
    if a == 'n':
        return enter_data(set_vec)
    elif a == 'y':
        return inc1, inc2
    else:
        return confirm_values(inc1, inc2, spring_attributes, set_vec)


def invalid_values(inc1, inc2, set_vec):
    try:
        inc1, inc2 = calc.calc_length(inc1, inc2)
        return inc1, inc2
    except ValueError:
        print('Invalid Values!\n\nRetry? (y/n)', end='')
        a = input()
        clear()
        if a == 'y':
            return enter_data(set_vec)
        elif a == 'n':
            main.select_scenario(set_vec)
        else:
            return invalid_values(inc1, inc2, set_vec)


def enter_data(set_vec):
    """enter custom values"""
    num = (1, 2)
    one, two = [1], [2]
    col = ['   Mass   ', '     k     ', '    vx    ', '    vy    ', '     x    ', '     y    ']
    inc1, inc2 = [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ']
    spring_attributes = pd.DataFrame((inc1, inc2), index=num, columns=col)
    for i in range(2):
        print(f' {i + 1} ', end='')
        for j in range(6):
            if i == 0:
                inc1[j] = check_float(spring_attributes)
                one.append(inc1[j])
                spring_attributes = pd.DataFrame((inc1, inc2), index=num, columns=col)
                clear()
            else:
                inc2[j] = check_float(spring_attributes)
                two.append(inc2[j])
                spring_attributes = pd.DataFrame((inc1, inc2), index=num, columns=col)
                clear()
    inc1, inc2 = confirm_values(one, two, spring_attributes, set_vec)
    inc1, inc2 = invalid_values(inc1, inc2, set_vec)
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
        clear()
        if num == 'b':
            main.select_scenario(set_vec)
        num = int(num)
        if num >= dir_num or num < 0:
            print('No such file!\n')
            return load_data(set_vec)
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
    clear()
    if a == '0':
        set_vec[0] = 0.001
    elif a == '1':
        set_vec[0] = 0.000_1
    elif a == '2':
        set_vec[0] = 0.000_01
    elif a == 'b':
        main.select_scenario(set_vec)
    else:
        return set_time_step(set_vec)
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
    clear()
    if a == '0':
        set_vec[2] = 0
    elif a == '1':
        set_vec[2] = 1
    elif a == '2':
        set_vec[2] = 2
    elif a == 'b':
        main.select_scenario(set_vec)
    else:
        return set_tails(set_vec)
    return set_vec


def init_set(set_vec):
    """Settings Screen"""
    inc1, inc2, dat_arr = [], [], 'empty'
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
        quit()
    elif a == 'e':
        inc1, inc2 = enter_data(set_vec)
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
        return init_set(set_vec)
    return inc1, inc2, dat_arr, set_vec


def main_options(set_vec):
    """main options"""
    print("Select Scenario (1/2/3/4) or type 'm' for more options:  ", end='')
    a = input()
    clear()
    dat_arr = 'empty'
    if a == 'q':
        quit()
    elif a == 'm':
        inc1, inc2, dat_arr, set_vec = init_set(set_vec)
        return inc1, inc2, dat_arr, set_vec
    elif a == '1' or a == '2' or a == '3' or a == '4':
        inc1, inc2 = init_arr(a)
        return inc1, inc2, dat_arr, set_vec
    else:
        return main_options(set_vec)
