from normlib.ro_parameters import ROParameters
from normlib.ro_state import ROState
import math

class RONormalizer:
    def __init__(self, standard:ROState):
        self.standard = standard

    def normalize(self, state:ROState):
        ans = {}
        self.state = state
        ans["normalized_feed"] = self.state.q_perm*self.standard.ndp/self.state.ndp*self.standard.tcf/self.state.tcf
        ans["normalized_salt"] = self.state.c_perm*self.standard.ndp/self.state.ndp*self.state.c_feed_concentrate/self.standard.c_feed_concentrate
        ans["water_permeability"]= self.state.k_water_perm
        ans["salt_permeability"]= self.state.k_salt_perm
        return ans

if __name__ == '__main__':
    standard = ROParameters(p_feed=15, p_conc= 13.5, p_perm=0, square=4400, c_feed=10000, q_feed=10, q_perm=5, c_perm=5, temp=25)
    state = ROParameters(p_feed=15.3, p_conc= 13.5, p_perm=0, square=4400, c_feed=9000, q_feed=10, q_perm=5, c_perm=7, temp=20)
    normalizer = RONormalizer(ROState(standard))
    print(normalizer.normalize(ROState(state))) # {'normalized_feed': 4.0, 'water_permeability': 0.0, 'salt_permeability': 0.0}