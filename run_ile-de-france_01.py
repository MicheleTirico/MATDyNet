from matdynet.controler.controler import Controler
from matdynet.network.network import Network
from matdynet.network.editNetwork import EditNetwork
from matdynet.config import config

# setup parameters
url = "/home/mtirico/project/matdynet/scenarios/ile_de_france/config_sim.xml"
absPath = "/home/mtirico/project/matdynet"

# config
c = config.Config(url,absPath)
#c.setAbsolutePath(absPath)
u = config.Urls(c)
u.deleteExistingFiles()
u.deleteExistingOutputs()
u.createFolders()

# setup network
n=Network(c)
n.initStates()
""" those methods are used when we do not have the initial xml file and we use shp files 
nshp=EditShp(n,False)       # initialize class
nshp.processingShp()        # TODO, transformer initial shp to a new shp for the project (stage ? )
nshp.setupNetwork()         # download and store the shp if not founded
"""
en=EditNetwork(c)
# nsim.initNetworkStates()    # method to use when we have a shapefile<
# c.initConfigStep(0)
en.initNetworkStatesFromXml()    # method to use when we have an existing network.xml and we want to add states. We do not consider here the properties of the network

ct = Controler (c,n,en)

ct.run (True)


