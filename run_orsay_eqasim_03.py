from matdynet.controler.controler import Controler
from matdynet.network.createNetworkStates import CreateNetworkStates
from matdynet.network.network import Network
from matdynet.config import config
from matdynet.network.createNetworkFromXml import CreateNetworkFromXml
from matdynet.plans.setIdSchedule import SetIdSchedule
from matdynet.plans.transit import Transit

url = "/home/mtirico/project/matdynet/scenarios/orsay_eqasim_03/orsay_config_sim.xml"
absPath = "/home/mtirico/project/matdynet"

# config
c = config.Config(url,absPath)
#c.setAbsolutePath(absPath)
u = config.Urls(c)
u.deleteExistingTmp()
u.deleteExistingOutputs()
u.createFolders()

# setup network
n=Network(c)
n.initStates()

#en=EditNetwork(c)
# nsim.initNetworkStates()    # method to use when we have a shapefile<
# c.initConfigStep(0)
#en.initNetworkStatesFromXml()    # method to use when we have an existing network.xml and we want to add states. We do not consider here the properties of the network

cns=CreateNetworkStates(c,n,True)
cnfx= CreateNetworkFromXml(c,n,True)


# transit
t=Transit(c)
sid=SetIdSchedule(c,t,True)

#ct = Controler (c,n,en)

#ct.run (True)




