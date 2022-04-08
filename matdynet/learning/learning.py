import numpy as np
import random as rd

from matdynet.config import config
from matdynet.learning.agents import Agents
from matdynet.network.network import Network

import lxml.etree as ET


class Learning ():
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
        self.states=self.network.states
        self.typeLearning = self.config.getLearning("typelearning")
        self.nStates=len(self.network.states.getStates())
        self.gamma=float(self.config.getLearning("gamma"))
        self.alpha=float(self.config.getLearning("alpha"))
        self.nsim=int(self.config.getSimulation("numsim"))
        self.__agents=Agents(config,network)
        self.__initAgents()
        rd.seed(self.config.randomSeed)

    def __initAgents(self):
        self.__agents.initAgents()

    def compute(self,step):
        if self.typeLearning=="qtable":     self.__computeQtable(step)
        elif self.typeLearning=="random":   self.__computeRandom(step)
        else: print ("ERROR: learning typy not set")

    def __computeRandom(self,step):
        listStates= self.network.states.getListStates()
        tree_networkStates=ET.parse(self.config.urlNetworkStatesOut)
        root_networkStates=tree_networkStates.getroot()
        links_networkStates=root_networkStates.find("links")

        for link in links_networkStates:
            steps=link.findall("steps")[0]
            newStep=ET.SubElement(steps,"step",{"nstep":str(step)})
            newState=listStates[rd.randint(0,len(listStates)-1)]
            ET.SubElement(newStep,"value",{"name":"state"}).text=newState
        tree_networkStates.write(self.config.urlNetworkStatesOut, pretty_print = True)

    def __computeQtable(self,step):
        print("LOG: start compute qtable")
        """
        input: 
            alpha= learning rate
            gamma=discount factor
            epsilon=small value (0.01)
        for each agent:
            a <- new action selected with e-greedy
            s' <- a 
            Q(s',a') <- Q(s,a)+alpha[R+gamma max[Q(s',a)-Q(s,a)]
            s <- s'            
            update qtab
        """

        for agent in self.__agents.getAgents().values():
            id_link=agent.getId()
            state=agent.getInitState()
            newState=self.__selectActionRandom(self.network.states.getListStates())
            posState=self.network.states.getPosState(state)
            posAction=posState # action is like states
            QvalueOld= agent.getQtableValue(step,posState,posAction)
            reward=agent.getStepScore(step) # score
            maxval=agent.getMaxVal(step,posState)
            QvalueNew=QvalueOld+self.alpha*(reward+self.gamma*maxval-QvalueOld)
            agent.setValue(step,posState,posAction,QvalueNew)
            # write on the xml
            tree=ET.parse(self.config.urlNetworkStatesOut)
            root=tree.getroot()
            links=root[1]
            link=links.findall("./link[@id='"+str(id_link)+"']")[0]
            steps=link[0]
            try:                s=steps.findall("./step[@nstep='"+str(step)+"']")[0]
            except IndexError:  s=ET.SubElement(steps,"step",{"nstep":str(step)})
            ET.SubElement(s,"value",{"name":"state"}).text=state
            tree.write(self.config.urlNetworkStatesOut, pretty_print = True)

    def __selectActionRandom(self,actions): return actions[rd.randint(0,len(actions)-1)]

    def updateAgents(self,step):
        """
        open the networkstates.xml and
        for each agent in the agent set, setup the state
        :return:
        """
        tree=ET.parse(self.config.urlNetworkStates)
        print ("--------------------------------",self.config.urlNetworkStates)
        network=tree.getroot()
        links=network[1]
        for link in links:
            steps=link[0]
            try:
                s=steps.findall("./step[@nstep='"+str(step)+"']")
                s=s[0]
                averageScore=s.findall("./value[@name='averagescore']")[0]
                averagescore=float(averageScore.text)
                agent=self.__agents.getAgent(link.attrib['id'])
                agent.setScore(step,averagescore)
                print (averagescore)

            except IndexError:  print ("WARNING: (class: learning, method: updateAgents) the agent",link.attrib['id'],"has not a score")



def __test (run):
    if run:
        url = "/home/mtirico/project/matdynet/scenarios/equil_02/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"

        # config
        c = config.Config(url,absPath)
        u = config.Urls(c)

        n=Network(c)
        l = Learning(c,n)
        step=1
        l.updateAgents(step)
        l.compute(step)
        """
        step=2
        l.updateAgents(step)
        l.compute(step)
        """



__test(False)