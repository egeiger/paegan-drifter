import numpy as np
from shapely.geometry import Point
from datetime import datetime, timedelta
from paegan.transport.models.transport import Transport
from paegan.transport.location4d import Location4D
from paegan.transport.model_controller import ModelController
from paegan.drifters.models.wind import WindForcing
from paegan.drifters.particles.drifter import Drifter


class CompareDrifters(object):
    """
        This controls a set of drifter comparisons with
        different forcing datasets
    """
    def __init__(self, **kwargs):
        if "tracks" in kwargs:
            self._drifter_tracks = kwargs.pop("tracks", [])
        else:
            raise ValueError("You must supply a list of tracks" +\
            " (location4d arrays) with the [tracks] keyword")
        
        self._wind_model = kwargs.pop("wind_model", None)
        self.drifters = []
        for track in self._drifter_tracks:
            self.drifters.append(Drifter(locations=track))
        self.time_step = kwargs.pop("time_step")
        self.num_steps = kwargs.pop("num_steps")
        
    def run(self, hydrodatasets, **kwargs):
        _wind_path = kwargs.get("winddataset", None)
        num_particles = 1
        models = [Transport(horizDisp=0., vertDisp=0.)]
        if self._wind_model != None:
            models.append(WindForcing())
            
        for drifter in self.drifters:
            start_location4d = drifter.locations[0]
            start_time = start_location4d.time
            start_lat = start_location4d.latitude
            start_lon = start_location4d.longitude
            start_depth = start_location4d.depth
            time_step = self.time_step
            num_steps = self.num_steps
            model = ModelController(latitude=start_lat, longitude=start_lon,
                depth=start_depth, start=start_time, step=time_step, 
                nstep=num_steps, npart=num_particles, models=models, 
                use_bathymetry=False, use_shoreline=True,
                time_chunk=10, horiz_chunk=10)
            for hydromodel in hydrodatasets:
                model.run(hydromodel, wind=_wind_path)
                drifter.add_virtual_drifter(model.particles[0])
                                    
