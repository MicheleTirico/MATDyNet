from matdynet.config import config
import xml.etree.ElementTree as ET

class StateSet ():
    __states = {}

    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,con):
        print ("LOG: setup the states")
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
            attrib_line = ["id","modes","from","to","freespeed","capacity","permlanes","dir"]
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

    # methods for lines
    def __getLine (self,attrib_list,element):
        line = {}
        for attrib in attrib_list:
            try:    line[attrib] = element.attrib[attrib]
            except: print ("WARNING: problem with the states.xml flie. The attrib \""+attrib+"\" is not founded in \""+element.tag+"\"")
        return line

    def __pushStateInBucket(self,name, state):    self.__states[name]=state

    # get methods
    # ---------------------------------------------------------------------------------------
    def getStates(self):    return self.__states
    def getState(self,name):    return self.__states[name]

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
        url = "/home/mtirico/project/matdynet/scenarios/orsay/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"

        c = config.Config(url)
        c.setAbsolutePath(absPath)

        n=Network(c)
        ns = StateSet(c)

__test(False)