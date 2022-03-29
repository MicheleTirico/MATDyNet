import numpy as np

from matdynet.config import config
from matdynet.learning.learning import Learning
from matdynet.network.network import Network
import xml.etree.ElementTree as ET

class Agents(Learning):

    def __init__(self,l):
        self.l=l
        print (self.l.gamma)
        self.__initAgents()

    def __initAgents(self):
        """
        for link in networkStates:
            create agent
            set state
            init q table
        :return:
        """
        self.__agents={}
        tree=ET.parse(self.l.config.urlNetworkStates)
        network=tree.getroot()
        links=network[1]
        for link in links:
            state=link.attrib["state"]
            id=link.attrib["id"]
            a=Agent(super()) # NO, NON POSSO INIZIALIZZARE AGENTS

    def getQtable(self,step,agent): print ("TODO")


class Agent () :
    # qtable = matrix to each step

    # constructor
    def __init__(self, agents):
        self.__agents=agents
        self.__initQtable()
        self.__initQtable()

    # init
    def __initQtable(self):     self.__qtable ={0:np.zeros((self.__agents.l.nStates,self.__agents.l.nStates))}

    # get
    def getQtable(self):                return self.__qtable
    def getStepQtable(self,step):       return self.__qtable[step]

    # set
    def setQtable(self,step,table):     self.__qtable[step]=table

    # display
    def displayTest(self):              print(self.__agents)
    def displayQtable(self):            print(self.__qtable)

def __test(run):
    if run==True:
        url = "/home/mtirico/project/matdynet/scenarios/equil_02/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"

        # config
        c = config.Config(url)
        c.setAbsolutePath(absPath)
        c.initConfig()
        u = config.Urls(c)
        #u.deleteExistingFiles()
        u.createFolders()


        n=Network(c)
        l = Learning(c,n)
        ags = Agents(l)
        a=Agent(ags)
        a.displayQtable()

        step=1



__test(True)