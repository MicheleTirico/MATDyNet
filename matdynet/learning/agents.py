import numpy as np

import xml.etree.ElementTree as ET

class Agents():

    def __init__(self,config,network):#    print("LOG: init agents")
        self.__config = config
        self.__network=network

    def initAgents(self):
        """
        for link in networkStates:
            create agent
            set state
            init q table
        :return:
        """
        self.__agents={}
        tree=ET.parse(self.__config.urlNetworkStatesOut)
        network=tree.getroot()
        links=network[1]
        for link in links:
            state=link.attrib["state"]
            id=link.attrib["id"]
            listStates=self.__network.states.getListStates()
            agent =Agent(self.__config,self.__network)
            agent.setId(id)
            agent.setParams(self.__config.getSimulation("numsim"),listStates,listStates)
            agent.initQtable()
            agent.setInitState(state)
            self.__agents[id]=agent


    def getAgent(self,idAgent):             return self.__agents[str(idAgent)]
    def getQtable(self,idAgent):            return self.__agents[str(idAgent)].getQtable()
    def getQtableStep(self,idAgent,step):   return self.__agents[str(idAgent)].getQtable()
    def getAgents(self):                    return self.__agents
    def displayAgents(self):                print (self.__agents)

class Agent (Agents) :
    # constructor
    def __init__(self,config,network):
            super(Agent, self).__init__(config,network)
            self.__stepScore= {}

    # setup
    def setParams(self,numSim,listStates,listActions):
        self.__setNsim(numSim)
        self.__setListStates(listStates)
        self.__setListActions(listActions)

    def initQtable(self):
        self.__qtable = np.zeros(shape=(
            self.__numSim+1,
            len(self.__listStates),
            len(self.__listActions)))

    # private set methods
    def __setListStates(self,listStates):       self.__listStates=listStates

    def __setListActions(self,listActions):     self.__listActions=listActions

    def __setNsim(self,numSim):                 self.__numSim=int(numSim)

    # set methods
    def setId(self,id):                         self.__id=id

    def setInitState(self,state):
        self.__initState=state
        self.__stepState={0,state}

    def setValue(self,step,state,action,value):#    print (step,state,action)
        self.__qtable[step,state,action]=value


    def setScore(self,step,score):              self.__stepScore[int(step)]=score

    def setStepState (self,step,state):         self.__stepState[int(step)]=state

    # get methods
    def getId (self):                           return self.__id
    def getInitState(self):                     return  self.__initState
    def getStepScore(self,step):
        return self.__stepScore[step]
        try:                    return self.__stepScore[step]
        except KeyError:
            print("WARNING: (class: agents, method: getStepScore) no score for the agent",self.__id,"is avaible at step",step)
            return 0

    def getScores(self):            return self.__stepScore
    def getQtable(self):            return self.__qtable
    def getQtableValue(self,step,posState,posAction):   return self.__qtable[step,posState,posAction]
    def getQtableStep(self,step):
        if step<= self.__numSim:    return self.__qtable[int(step)]
        else: print("WARNING: step is out of range")
    def getMaxVal(self,step,posState): return max(self.__qtable[step,posState])

    # display
    def displayQtable(self):    print (self.__qtable)