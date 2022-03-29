import os
import random

import networkx as nx
import lxml.etree as ET

from matdynet.network.network import Network
from matdynet.network.stateSet import StateSet
from matdynet.config import config


class EditNetwork (Network):
    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,con):
        super(EditNetwork, self).__init__(con)
        self.__config=con
        self.__initStates = self.__config.getSim("initStates")


    # init networks sim and states
    # ---------------------------------------------------------------------------------------
    def initNetworkStatesFromShp(self):
        if self.__initStates == "random":
            print ("WARNING: todo, create init random")
        else:
            print("LOG: create the networkStates.xml with the same state",self.__initStates)
            self.__createXmlStatesFromShp()

    def initNetworkStatesFromXml(self):
        if self.__initStates == "random":
            print ("WARNING: todo, create init random")
        else:
            print("LOG: create the networkStates.xml with the same state",self.__initStates)
            self.__createXmlStatesFromXml()

    def createXmlNetworkFromShp (self):
        print ("LOG: create the network.xml file")
        self.__createXmlNetworkFromShp()

    def addStateToXmlNetwork (self):
        print ("LOG: add state to the network.xml file")
        self.__addStateToXmlNetwork()

    # create xml state networks
    # ---------------------------------------------------------------------------------------
    def __createXmlStatesFromXml(self):
        """
        this method create a new networkStates.xml file from an existing network.xml and add the states.
        NB: It remove all information about the network.
        To use those information, you need to implement a new method.
        :return:
        """
        # init the xml file
        sim_tree = ET.Element("network",attrib={"scenario":str(self.scenario),"type":"networkStates","initStates":self.__initStates})
        sim_nodes=ET.SubElement(sim_tree,"nodes")
        sim_links=ET.SubElement(sim_tree,"links")

        # open the file network.xml
        states_tree = ET.parse(self.urlNetwork)
        states_root=states_tree.getroot()

        # create nodes
        for node in states_root[0]:
            ET.SubElement(sim_nodes,"node",attrib=node.attrib)

        # create links
        er=0
        w=str(0)
        for link in states_root[1]: #            print (link)
            try: w= link.attrib["width"]
            except: er=1
            l =ET.SubElement(sim_links,"link",attrib={"id":link.attrib["id"],
                                                   "state":self.__initStates,
                                                   "from":link.attrib["from"],
                                                   "to": link.attrib["to"],
                                                   "length":link.attrib["length"],
                                                   "width":str(w)
                                                   })

            self.__initSteps(link=l)

        if er==1: print("WARNING: at least one link has no width")

        # store network
        tree= ET.ElementTree (sim_tree)
        tree.write(self.urlXmlStates, pretty_print = True)
        tree.write(self.urlXmlStates,encoding="utf-8",xml_declaration=True,pretty_print = True)

    def __createXmlStatesFromShp(self):
        """
        this method give the xml of the network with the state of each link
        :param urlXml: the url where store the graph
        :param G: the graph modelled with nx and which came from shapefiles
        :param scenario: the name of the scenario
        :param state: the state to setup
        :return:
        """
        # init the graph
        G = self.__n.G_shp #nx.convert_node_labels_to_integers(self.__n.G_shp, first_label=0, label_attribute = "coord")

        # init the xml file
        attrib_et_link={}
        et_network = ET.Element("network",attrib={"scenario":str(self.__n.scenario),"type":"networkStates","initStates":self.__initStates})
        et_nodes=ET.SubElement(et_network,"nodes")
        et_links=ET.SubElement(et_network,"links",attrib=attrib_et_link)

        length=nx.get_edge_attributes(G,"length")
        width=nx.get_edge_attributes(G,"width")

        for i in range(len(G.nodes)):
            ET.SubElement(et_nodes,"node",attrib={"id":str(i),# "("+str(self.__n.G_shp.nodes[i]['coord'][0])+", "+str(self.__n.G_shp.nodes[i]['coord'][0])+")",
                                                  "x":str(G.nodes[i]['coord'][0]),
                                                  "y":str(G.nodes[i]['coord'][1]), })

        i = 0
        for ed in self.__n.G_shp.edges:
            startnode,endnode = ed[0],ed[1]
            l = self.__getLength(startnode,endnode,length)
            w = self.__getWidth(startnode,endnode,width)
            ET.SubElement(et_links,"link",attrib={"id":str(i),
                                                  "from":str(startnode),
                                                  "to":str(endnode),
                                                  "length":str(l),
                                                  "width":str(w),
                                                  "state":str(self.__initStates)      })
            i+=1
            # to check init steps
            self.__initSteps(ed)

        # store network
        tree = ET.ElementTree(et_network)
        tree.write(self.__n.urlXmlStates, pretty_print = True)
        tree.write(self.__n.urlXmlStates,encoding="utf-8",xml_declaration=True,pretty_print = True)

    # create xml networks
    # ---------------------------------------------------------------------------------------
    def __createXmlNetworkFromShp(self):
        """
        this method create the network.xml to use for the simulation
        :return: none
        """
        print ("LOG: create the network.xml file to push in simulation")
        states = self.__states.getStates()

        # init the xml file
        sim_tree = ET.Element("network",attrib={"scenario":str(self.__n.scenario),"type":"networksimulation","initStates":self.__initStates,"datafrom":"shp"})
        sim_nodes=ET.SubElement(sim_tree,"nodes")
        sim_links=ET.SubElement(sim_tree,"links")

        # open the file networkStates.xml
        states_tree = ET.parse(self.__n.urlXmlStates)
        states_root=states_tree.getroot()

        for node in states_root[0]:
            ET.SubElement(sim_nodes,"node",attrib=node.attrib)

        id = 0
        for link in states_root[1]:
            stateName = link.attrib["state"]
            s=self.__states.getState(stateName)
            lines=s.getLines()
            link_from = link.attrib["from"]
            link_to = link.attrib["to"]
            for line in lines:
                line["id"]=str(id)
                line["state"]=stateName
                line["idstatenetwork"]=link.attrib["id"]
                line["length"]=link.attrib["length"]
                line["width"]=link.attrib["width"]
                line["allowedstates"]=self.__getListAllowedStates(link) # TODO
                if line["dir"]=="from-to":
                    line["from"]=link_from
                    line["to"]=link_to
                else:
                    line["from"]=link_to
                    line["to"]=link_from
                ET.SubElement(sim_links,"link",attrib=line)
                id+=1

        # store network
        tree= ET.ElementTree (sim_tree)
        tree.write(self.__n.urlNetwork, pretty_print = True)
        tree.write(self.__n.urlNetwork,encoding="utf-8",xml_declaration=True,pretty_print = True)

    def __addStateToXmlNetwork(self):
        # init the xml file
        network = ET.Element("network",{"name":str(self.scenario)})
        self.__setAttribute(network,"state",self.__initStates)
        self.__setAttribute(network,"scenario",self.scenario)
        self.__setAttribute(network,"datafrom","xml")
        sim_nodes=ET.SubElement(network,"nodes")
        sim_links=ET.SubElement(network,"links")
        # open the file networkStates.xml
        states_tree = ET.parse(self.urlXmlStates)
        states_root=states_tree.getroot()
        # create nodes
        for node in states_root[0]:  ET.SubElement(sim_nodes,"node",attrib=node.attrib)
        # create links
        for link in states_root[1]:
            s=self.states.getState(link.attrib["state"])
            lines=s.getLines()
            line=lines[0]
            sim_link=ET.SubElement(sim_links,"link",attrib={"id":link.attrib["id"],
                                                     "from":link.attrib["from"],
                                                     "to": link.attrib["to"],
                                                     "capacity":line["capacity"],
                                                     "freespeed":line["freespeed"],
                                                     "permlanes":line["permlanes"],
                                                     "length":link.attrib["length"]})

            self.__setAttribute(sim_link,"state",self.__initStates)
            self.__setAttribute(sim_link,"width",link.attrib["width"])

        toAdd = """<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">\n\n"""
        self.__addHeaderAndStoreXml(root=network,toAdd=toAdd,newf=self.urlNetworkSim,pathTmp=self.urlNetworkToRemove)

    def __addHeaderAndStoreXml (self,root, toAdd,newf,pathTmp):
        tree= ET.ElementTree (root)
        tree.write(pathTmp,pretty_print = True)
        f = open(pathTmp,'r')
        newf = open(newf,'w')
        lines = f.readlines()
        newf.write(toAdd)
        for line in lines:  newf.write(line)
        newf.close()
        f.close()
        os.remove(self.urlNetworkToRemove)

    def __setAttribute(self,root,name,val):
        try:                attributes=root[0]
        except IndexError:  attributes= ET.SubElement(root,"attributes",{})
        attribute= ET.SubElement(attributes,"attribute",{"name":name,"class":"java.lang.String"})
        attribute.text=val

    # ---------------------------------------------------------------------------------------
    def __getListAllowedStates (self,link):
        return ""

    # update network states
    """ create a temporal graph
      <step name="it.number it">
          <value name="score"> xxxx </value>       
      </step>
    """
    # ---------------------------------------------------------------------------------------

    def __initSteps (self,link):
        steps = ET.SubElement(link,"steps",{"name":"steps"})
    #    step = ET.SubElement(steps,"step",{})

    def __setStepVal(self,root,nStep,nameVal,val):
        try:    step=root[0]
        except: step = ET.SubElement(root,"step",{"nStep":str(nStep)})
        value = ET.SubElement(step,"value",{"name":nameVal})
        value.text=val

    def updateStateNetwork(self,nStep):
        # open the file networkStates.xml
        states_tree = ET.parse(self.__n.urlXmlStates)
        states_root=states_tree.getroot()

        for link in states_root[1]:
            name= "name analysis"
            val= str(random.randrange(0,100)) # value of analysis
            newState="state"
            self.__setStepVal(root=link[0],nStep=nStep,nameVal=name,val=val)
            self.__setStepVal(root=link[0],nStep=nStep,nameVal="state",val=newState)

        tree= ET.ElementTree (states_root)
        tree.write(self.__n.urlXmlStates)

    # handle and get informations about shapefile
    # ---------------------------------------------------------------------------------------
    def __getLength (self, startnode,endnode, length) : return  round(length [(startnode,endnode)],3)

    def __getWidth (self, startnode, endnode,width ):
        try: return width([startnode,endnode])
        except: return 0

def __test (run):
    if run :
        print ("test")
        # setup parameters
        url = "/home/mtirico/project/matdynet/scenarios/equil_02/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"
        # config
        c = config.Config(url)
        c.setAbsolutePath(absPath)
        n=Network(c)
        en = EditNetwork(n)
        en.addStateToXmlNetwork()

        en.updateStateNetwork(3)
        en.updateStateNetwork(4)
        en.updateStateNetwork(3)

__test (False)