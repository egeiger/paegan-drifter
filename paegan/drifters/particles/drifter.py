from paegan.transport.location4d import Location4D
from paegan.transport.particles.particle import Particle

class Drifter(Particle):
    """
    """
    def __init__(self, **kwargs):
        self._locations = kwargs.get("locations", [])
        self.virtual_drifters = []
        
    def add_virtual_drifter(self, drifter):
        self.virtual_drifters.append(drifter)
        
