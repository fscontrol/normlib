import math
from normlib.ro_parameters import ROParameters

class ROState:
    def __init__(self, ro_state: ROParameters):
        for key, value in ro_state.__dict__.items():
            setattr(self, key, value)

    @property
    def y(self):
        return self.q_perm/self.q_feed

    @property
    def q_conc(self):
        return self.q_feed - self.q_perm
    @property
    def ndp(self):
        return (self.p_feed + self.p_conc) / 2 - self.p_perm - self.p_osmotic

    @property
    def p_osmotic(self):
        if self.c_feed_concentrate < 20000:
            return (self.c_feed_concentrate * (self.temp + 320)) / 491000
        else:
            return (0.0117 * self.c_feed_concentrate - 34) / 14.23 * (self.temp + 320) / 345

    @property
    def c_feed_concentrate(self):
        return self.c_feed * (math.log(1 / (1 - self.y)) / self.y)

    @property
    def tcf(self):
        if self.temp >= 25:
            return math.exp(2640 * (1 / 298 - 1 / (273 + self.temp)))
        else:
            return math.exp(3020 * (1 / 298 - 1 / (273 + self.temp)))

    @property
    def k_water_perm(self):
        return self.q_perm/self.tcf/self.square/self.ndp

    @property
    def k_salt_perm(self):
        return self.c_perm*self.q_perm/self.tcf/self.square/(self.c_feed_concentrate-self.c_perm)

    @property
    def k_hydraulic_pressure(self):
        return self.ndp/(self.q_feed - self.q_perm/2)/self.water_viscosity

    @property
    def water_viscosity(self):
        temp = self.temp
        tds = self.c_feed_concentrate
        mu_water = 0.02414 * math.pow(10, 247.8 / (temp + 133.15))
        if tds == 0:
            return mu_water
        salt_mass_fraction = tds / 1_000_000
        viscosity_ratio = 1 + 0.0816 * salt_mass_fraction + 0.0122 * math.pow(salt_mass_fraction, 2)
        return mu_water * viscosity_ratio

if __name__ == '__main__':
    params = ROParameters(p_feed=15, p_conc= 13.5, p_perm=0, square=4400,
                          c_feed=10000, q_feed=10, q_perm=5, c_perm=0, temp=25)
    state = RoState(params)
    print(state.ndp) # 0.75
    print(state.p_osmotic) # 0.000162
    print(state.tcf)
    print(state.k_water_perm*1000) # 0.