from matdynet.config import config
import xml.etree.ElementTree as ET

class StateSet ():
    __states = {}

    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,con):
        print ("LOG: network/stateSet.py. Init states")
        self.__config = con
        self.__urlStatesXml = self.__config.getAbsolutePath()+"/scenarios/"+self.__config.getUrl("scenario")+"/"+self.__config.getUrl("states")
        self.__tree = ET.parse(self.__urlStatesXml)
        self.__root = self.__tree.getroot()
        self.__setup ()

    # setup
    # ---------------------------------------------------------------------------------------
    def __setup(self):
        for s_xml in self.__root.iter("state"):
            name = s_xml.attrib["name"]
            state = State(name)
            self.__pushStateInBucket(name,state)
            attrib_line = ["modes","freespeed","capacity","permlanes","dir"] # id, from and to are not needed (I think,not sure for shp files)
            for element_state_xml in s_xml:
                if element_state_xml.tag == "description":
                    state.setDescription(element_state_xml.text)
                elif element_state_xml.tag == "geometry":
                    maxWidth = element_state_xml.attrib["maxwidth"]
                    minWidth = element_state_xml.attrib["minwidth"]
                    state.setMaxWidth (maxWidth)
                    state.setMinWidth (minWidth)
                else:
                    line = self.__getLine(attrib_line,element_state_xml)
                    state.setLine(line)
        self.__listStates=list(self.__states.keys())

    # methods for lines
    def __getLine (self,attrib_list,element):
        line = {}
        for attrib in attrib_list:
            try:    line[attrib] = element.attrib[attrib]
            except: print ("WARNING: (network/stateSet.py, cl __getLine) problem with the states.xml file. The attrib \""+attrib+"\" is not founded in \""+element.tag+"\"")
        return line

    def __pushStateInBucket(self,name, state):    self.__states[name]=state

    # get methods
    # ---------------------------------------------------------------------------------------
    def getStates(self):        return self.__states
    def getState(self,name):    return self.__states[name]

    def getListStates(self):    return list(self.__states.keys())
    def getPosState(self,state):
        try:                    return(self.__listStates.index(state))
        except ValueError:      print("ERROR: the state",state,"has ot been defined")

class State:
    def __init__(self,name):
        self.__name=name
        self.__description = ""
        self.__lines =  []

    def setName(self,val):          self.__name = val
    def setDescription(self,val):   self.__description = val
    def setLine(self,val):          self.__lines.append(val)
    def setMaxWidth(self,val):      self.__maxWidth = val
    def setMinWidth(self,val):      self.__minWidth = val

    def getName(self):              return self.__name
    def getDescription(self):       return self.__description
    def getLines(self):             return self.__lines
    def getMaxWidth(self):          return self.__maxWidth
    def getMinWidth(self):          return self.__minWidth

def __test(run):
    if run :
        url = "/home/mtirico/project/matdynet/scenarios/equil_02/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"

        c = config.Config(url,absPath)
        c.setAbsolutePath(absPath)

        ss=StateSet(con=c)
        ss.getState("c1")

__test(False)