from matdynet.network.network import Network
from matdynet.network.editShp import EditShp
from matdynet.network.editNetwork import EditNetwork
from matdynet.config import config

# setup parameters
from matdynet.simulation import controler

url = "/home/mtirico/project/matdynet/scenarios/orsay/config_sim.xml"
absPath = "/home/mtirico/project/matdynet"

# config
c = config.Config(url)
c.setAbsolutePath(absPath)
u = config.Urls(c)
u.deleteExistingFiles()
u.createFolders()

# setup network
n=Network(c)
nshp=EditShp(n, False)          # initialize class
nshp.processingShp()        # TODO, transfrm initial shp to a new shp for the project (stage ? )
nshp.setupNetwork()         # download and store the shp if not founded

nsim=EditNetwork(n)
nsim.initNetworkStatesFromShp()
nsim.createXmlNetworkFromShp()

ct = controler.Controler (c)
# ct.run (False)

#nsim.createXmlSim()

#nsim.plotGraph()

#nshp.castToXml()            # cast the shp in xml. todo: add methods for setup, move to sim

#nstates=NetworkStates(n)    # setup the network states
# setStatesInXml()


"""
# setup network
n = network.Network(c)
n.setupNetwork()
G = n.getGraph()
n.castToXml()

# push files
u.pushAllFiles()
s = config.Simulation(c)

# parameters simulation
s = config.Simulation(c)
nMax = s.getMaxSim()


 # dowload file if not exist (name city and path where file exist)
# store file if not exist (path where store network)
# cast file in xml

# run
ct = controler.Controler (c)
#ct.run (False)


"""
