import numpy as np

from matdynet.config import config
from matdynet.network.network import Network


class Learning :
    """
    parameters
    agents=link
    state=search in states.xml
    environment=scores of individuals
    actions=move to one of other state
    reward=score
    policy=maximise reward
    """
    def __init__(self,config,network):
        print("LOG: init learning")
        self.config = config
        self.network=network
        self.typeLearning = self.config.getLearning("typelearning")
        self.nStates=len(self.network.states.getStates())
        self.gamma=float(self.config.getLearning("gamma"))
        self.alpha=float(self.config.getLearning("alpha"))

    def compute(self,step):
        if self.typeLearning=="qtable": self.__computeQtable(step)
        else: print ("ERROR: learning typy not set")

    def __computeQtable(self,step):
        print("LOG: start compute qtable")

def __test (run):
    if run:
        url = "/home/mtirico/project/matdynet/scenarios/equil_02/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"

        # config
        c = config.Config(url)
        c.setAbsolutePath(absPath)
        u = config.Urls(c)
        #u.deleteExistingFiles()
        u.createFolders()

        n=Network(c)
        l = Learning(c,n)
        step=1
        l.compute(step)




__test(True)