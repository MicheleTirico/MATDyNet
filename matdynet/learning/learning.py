import numpy as np
import random as rd

from matdynet.config import config
from matdynet.learning.agents import Agents
from matdynet.network.network import Network

import lxml.etree as ET

class Learning ():
    def __init__(self,config,network):
        print("LOG: init learning")
        self.config = config
        self.network=network
        self.states=self.network.states
        self.typeLearning = self.config.getLearning("typelearning")
        self.nStates=len(self.network.states.getStates())
        self.epsilonMin=float(self.config.getLearning("epsilonmin"))
        self.gamma=float(self.config.getLearning("gamma"))
        self.alpha=float(self.config.getLearning("alpha"))
        self.nsim=int(self.config.getSimulation("numsim"))
        self.__agents=Agents(config,network)
        self.__initAgents()
        rd.seed(self.config.randomSeed)

    def __initAgents(self):
        self.__agents.initAgents()

    def compute(self,step):
        if      self.typeLearning=="qtable":    self.__computeQtable(step)
        elif    self.typeLearning=="random":    self.__testRandom(step)
        else:   print ("ERROR: learning type not set")

    def __computeRandom(self,step):
        listStates=self.network.states.getListStates()
        tree_networkStates=ET.parse(self.config.urlNetworkStatesOut)
        root_networkStates=tree_networkStates.getroot()
        links_networkStates=root_networkStates.find("links")
        for link in links_networkStates:
            steps=link.findall("steps")[0]
            newStep=ET.SubElement(steps,"step",{"nstep":str(step)})
            newState=listStates[rd.randint(0,len(listStates)-1)]
            ET.SubElement(newStep,"value",{"name":"state"}).text=newState
        tree_networkStates.write(self.config.urlNetworkStatesOut, pretty_print = True)

    def __computeQtable_old_01(self,step):
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
            posState=self.network.states.getPosState(state)
            posAction=posState # action is like states
        #    newState=self.__selectActionGreedy(step,agent,self.network.states.getListStates(),posState)
            newState=self.__selectActionRandom(self.network.states.getListStates())
            posActionNewState=self.network.states.getPosState(newState)
            print ("zzzzzzzzzzzzzzzzzz",posActionNewState,type(posActionNewState))
            QvalueOld= agent.getQtableValue(step,posState,posActionNewState)
            reward=agent.getStepScore(step) # score
            maxval=agent.getMaxVal(step,posState)
            QvalueNew=round(QvalueOld+self.alpha*(reward+self.gamma*maxval-QvalueOld),3)
            print ("----------------",QvalueNew,QvalueOld,self.alpha,reward,self.gamma,maxval)
            agent.setValue(step,posState,posActionNewState,QvalueNew)
            print (agent.getQtableStep(step))
            # write on the xml
            tree=ET.parse(self.config.urlNetworkStatesOut)
            root=tree.getroot()
            links=root[1]
            link=links.findall("./link[@id='"+str(id_link)+"']")[0]
            steps=link[0]
            try:                s=steps.findall("./step[@nstep='"+str(step)+"']")[0]
            except IndexError:  s=ET.SubElement(steps,"step",{"nstep":str(step)})
            ET.SubElement(s,"value",{"name":"state"}).text=newState
            tree.write(self.config.urlNetworkStatesOut, pretty_print = True)

    def __computeQtable_old_02(self,step):
        for agent in self.__agents.getAgents().values():
            id_agent=agent.getId()
            print (agent.getStates(),agent.getScores())
            state=agent.getStepState(step-1)
            statePos=self.network.states.getPosState(state)
#            action=self.__selectActionGreedy(step-1,agent,self.network.states.getListStates(),statePos)
            action=self.__selectActionRandom(self.network.states.getListStates())
            actionPos=self.network.states.getPosState(action)
            Qvalue=agent.getQtableValue(step-1,statePos,actionPos)
            reward=agent.getStepScore(step) # score
            maxval=agent.getMaxVal(step-1,statePos)
            QvalueNew=Qvalue+self.alpha*(reward+self.gamma*maxval-Qvalue)
            agent.setValue(step,statePos,actionPos,QvalueNew)
            agent.setStepState(step,action)
            print (id_agent,agent.getStates(),agent.getScores(),sep="\n")
            print("state",state,statePos)
            print ("action",action,actionPos)
            agent.displayQtable()
            # write on the xml
            tree=ET.parse(self.config.urlNetworkStatesOut)
            root=tree.getroot()
            links=root[1]
            link=links.findall("./link[@id='"+str(id_agent)+"']")[0]
            steps=link[0]
            try:                s=steps.findall("./step[@nstep='"+str(step)+"']")[0]
            except IndexError:  s=ET.SubElement(steps,"step",{"nstep":str(step)})
            ET.SubElement(s,"value",{"name":"state"}).text=action
            tree.write(self.config.urlNetworkStatesOut, pretty_print = True)

    def __computeQtable (self,step):
        for agent in self.__agents.getAgents().values():
            id_agent=agent.getId()
            state=agent.getStepState(step-1)
            posState=self.network.states.getPosState(state)
            action=self.__selectActionGreedy(step-1,agent,self.network.states.getListStates(),posState)
#            action=self.__selectActionRandom(self.network.states.getListStates())
            posAction=self.network.states.getPosState(action)
            QvalueOld=agent.getQtableValue(step-1,posState,posAction)
            reward=agent.getStepScore(step-1)
        #    reward=rd.uniform(0,1)
            maxQ=agent.getMaxVal(step-1,posState)
            QvalueNew=QvalueOld+self.alpha*(reward+self.gamma*maxQ-QvalueOld)
            # update Qnew
            agent.setQtableValue(step,posState,posAction,QvalueNew)
            agent.setStepState(step,action)

            print ("---------------------------------")
            print (id_agent,agent.getStates(),agent.getScores())
            print(state,posState,action,posAction)
            print('learning',QvalueOld,QvalueNew,reward,maxQ)
            agent.displayQtable()

            # write on the xml
            tree=ET.parse(self.config.urlNetworkStatesOut)
            root=tree.getroot()
            links=root[1]
            link=links.findall("./link[@id='"+str(id_agent)+"']")[0]
            steps=link[0]
            try:                s=steps.findall("./step[@nstep='"+str(step)+"']")[0]
            except IndexError:  s=ET.SubElement(steps,"step",{"nstep":str(step)})
            ET.SubElement(s,"value",{"name":"state"}).text=action
            tree.write(self.config.urlNetworkStatesOut, pretty_print = True)


    def __testRandom(self,step):
        for agent in self.__agents.getAgents().values():
            # TEST RANDOM
            actionPos= rd.randint(0,rd.randint(0,len(self.network.states.getListStates())-1))
            statePos= rd.randint(0,rd.randint(0,len(self.network.states.getListStates())-1))
            action=self.network.states.getListStates()[actionPos]
            agent.setValue(step,statePos,actionPos,rd.uniform(0,1))
            agent.setStepState(step,action)

            # write on the xml
            tree=ET.parse(self.config.urlNetworkStatesOut)
            root=tree.getroot()
            links=root[1]
            link=links.findall("./link[@id='"+str(agent.getId())+"']")[0]
            steps=link[0]
            try:                s=steps.findall("./step[@nstep='"+str(step)+"']")[0]
            except IndexError:  s=ET.SubElement(steps,"step",{"nstep":str(step)})
            ET.SubElement(s,"value",{"name":"state"}).text=action
            tree.write(self.config.urlNetworkStatesOut, pretty_print = True)

    def __selectActionRandom(self,actions): return actions[rd.randint(0,len(actions)-1)]
    def __selectActionGreedy(self,step,agent, actions,posState):
        epsilon = max(self.epsilonMin,1-step/self.nsim)
        if rd.uniform(0,1) < epsilon:
            return actions[rd.randint(0,len(actions)-1)]
        else:
            listActions=agent.getValActions(step,posState)
            maxVal =max(listActions)
            posMax=listActions.index(maxVal)
            return actions[posMax]

    def updateAgents(self,step):
        """
        open the networkstates.xml and
        for each agent in the agent set, setup the state
        :return:
        """
        tree=ET.parse(self.config.urlNetworkStatesOut)      #print ("--------------------------------",self.config.urlNetworkStatesOut)
        network=tree.getroot()
        links=network[1]
        for link in links:
            steps=link[0]
            try:
                s=steps.findall("./step[@nstep='"+str(step)+"']")
                s=s[0]
                averageScore=float(s.findall("./value[@name='scoreaverage']")[0].text)
                agent=self.__agents.getAgent(link.attrib['id'])
                agent.setScore(step,averageScore)
            except IndexError:  print ("WARNING: (class: learning, method: updateAgents) the agent",link.attrib['id'],"has not a score")

    def getAgents(self):    return self.__agents.getAgents().values()

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