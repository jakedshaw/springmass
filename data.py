from numpy import array, save, load
import settings
from os import system


def get_num():
    """gets last image number, adds one, writes and returns number"""
    filename = 'trials/imgnum.npy'
    num = load(filename)
    new_num = array([int(num + 1)])
    save(filename, new_num, allow_pickle=True)
    system(f'mkdir trials/trial_{int(num)}')
    return int(num)


def reset_num():
    """resets and prints image number"""
    filename = 'trials/imgnum.npy'
    num = array([0])
    system('rm -r trials')
    system('mkdir trials')
    save(filename, num, allow_pickle=True)


def save_data(num, dat_arr):
    """saves data in npy file"""
    filename = f'trials/trial_{num}/{num}_data.npy'
    save(filename, dat_arr, allow_pickle=True)


def load_data(num):
    """loads data from npy file"""
    settings.clear()
    dat_arr = load(f'trials/trial_{num}/{num}_data.npy', allow_pickle=True)
    return dat_arr
