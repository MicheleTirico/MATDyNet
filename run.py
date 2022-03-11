from matdynet.setup import config
from matdynet.setup import network
from matdynet.simulation import controler

# setup parameters
url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
absPath = "/home/mtirico/project/matdynet"

c = config.Config(url);
c = config.Config(url)
c.setAbsolutePath(absPath)
u = config.Urls(c)
u.deleteExistingFiles()
u.createFolders()

# push files
u.pushAllFiles()
s = config.Simulation(c)

# parameters simulation
s = config.Simulation(c)
nMax = s.getMaxSim()

# setup network
n = network.Network(c)
n.setupNetwork()
G = n.getGraph()
n.castToXml()

 # dowload file if not exist (name city and path where file exist)
# store file if not exist (path where store network)
# cast file in xml

# run
ct = controler.Controler (c)
#ct.run (False)

