import springmass as spring
import calculations as calc
import settings as s
import plotting as p
import data


def default_data():
    """creates/resets default data"""
    set_vec = [0.000_1, 0, 0]  # dt, code, tails
    run_prog(set_vec)


def run_prog(set_vec):
    """runs simulation"""
    set_vec = [set_vec[0], set_vec[1], set_vec[2], 'y', 'y', 'n']  # dt, code, tails, save, plot, load, num
    print("Press ENTER to continue or type 'q' to quit:  ", end='')
    a = input()
    if a == '':
        s.clear()
        select_scenario(set_vec)
    elif a == 'q':
        s.clear()
        quit()
    else:
        s.clear()
        print('Invalid Entry!\n')
        run_prog(set_vec)


def select_scenario(set_vec):
    """runs scenario"""
    # get initial data
    inc1, inc2, dat_arr, set_vec = s.main_options(set_vec)

    # generate data
    if set_vec[5] == 'n':
        # time input
        sec = s.simulation_time()
        # calculate spring length
        inc1, inc2 = calc.calc_length(inc1, inc2)
        # create objects/data
        s1, s2, t = spring.Spring(inc1), spring.Spring(inc2), spring.Time(sec, set_vec[0])
        # gets and appends num
        set_vec.append(data.get_num())
        # runs calc
        s1, s2, ft, dat_arr = calc.run_calc(s1, s2, t)
        # saves data
        data.save_data(set_vec[6], dat_arr)
    else:
        sst, ft = dat_arr[0], dat_arr[1]
        s1, s2, t = sst[0], sst[1], sst[2]
        set_vec.append('null')

    # plot data
    p.run_plot(s1, s2, t, ft, set_vec)
    if set_vec[5] == 'n':
        print(f'Data saved in:  trials/trial_{set_vec[6]}\n')
    run_prog(set_vec)


if __name__ == '__main__':
    s.clear()
    print('Welcome to Spring Mass Simulator!\n')
    default_data()
