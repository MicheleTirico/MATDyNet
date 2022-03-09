from matdynet.config import config

# setup parameters
url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
c = config.Config(url);
u = config.Urls(c)
u.deleteExistingFiles()
u.createFolders()

# push files
u.pushAllFiles()


s = config.Simulation(c)


#name_scenario = u.url("equil")
