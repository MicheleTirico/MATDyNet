import os

from matdynet.config import config
from matdynet.network.stateSet import StateSet
import lxml.etree as ET

class Transit ():
    """ table variables
    G_shp   :   graph from he shp file
    G_sim   :   graph to use in simulation (to cast in xml)
    G_states:   simplified graph with states (to cast in xml)
    """

    # constructor
    def __init__(self, con):
        self.config=con


