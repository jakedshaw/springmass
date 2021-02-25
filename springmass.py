from numpy import array, linspace


class Spring:
    """A Spring Class"""

    def __init__(self, inc):
        """Attributes for the Spring Mass"""
        self.num = inc[0]
        self.m = inc[1]
        self.k = inc[2]
        self.len = inc[7]
        self.v = array(([inc[3]], [inc[4]]))
        self.x = array(([inc[5]], [inc[6]]))

    def __str__(self):
        """A string describing the object"""
        return f' {self.num}      {self.m}       {self.k}       {self.len}'


class Time:
    """A Time Vector Class"""

    def __init__(self, sec, dt):
        """Attributes for Time Vector"""
        self.sec = sec
        self.dt = dt
        self.sn = int(sec * (1/dt) + 1)
        self.time = linspace(0, sec, self.sn)
        self.delta_e = 'error'

    def __str__(self):
        """A string describing the object"""
        return f'%ΔE = {self.delta_e} %'


class World:
    """Contains Time and Settings"""

    def __init__(self):
        """Attributes for World"""
        pass

    def __str__(self):
        """A string describing World"""
        pass
