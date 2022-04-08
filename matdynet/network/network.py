import networkx as nx
import os

from matdynet.config import config
from matdynet.network.stateSet import StateSet
import lxml.etree as ET


class Network ():
    """ table variables
    G_shp   :   graph from he shp file
    G_sim   :   graph to use in simulation (to cast in xml)
    G_states:   simplified graph with states (to cast in xml)
    """

    # constructor
    def __init__(self, con):
        self.config = con
        self.sim = config.Simulation(self.config)
        self.urls = config.Urls(self.config)
        self.scenario =self.urls.getUrl("scenario")
        self.shp = self.config.getValWith2Attrib("urls","url",["name","type"],["network_shp","file"])
        self.city = os.path.splitext(self.shp)[0]
        self.urlShp = self.config.getAbsolutePath()+"/scenarios/"+self.urls.getUrl("scenario")+"/"+self.urls.getUrl("network_shp")
        self.urlXml = self.config.getAbsolutePath()+"/scenarios/"+self.urls.getUrl("scenario")+"/"+self.urls.getUrl("network") # for the sim
        self.urlNetwork=self.config.getAbsolutePath()+"/scenarios/"+self.urls.getUrl("scenario")+"/"+self.urls.getUrl("network")
        self.urlNetworkSim=self.config.getAbsolutePath()+"/"+self.urls.getUrl("url_output")+"/"+self.urls.getUrl("scenario")+"/"+self.urls.getUrl("networksim")
        self.urlNetworkToRemove=self.config.getAbsolutePath()+"/"+self.urls.getUrl("tmp")+"/netToRemove.xml"

        # deprecated
        self.urlXmlStates = self.config.getAbsolutePath()+"/"+self.urls.getUrl("url_output")+"/"+self.urls.getUrl("scenario")+"/"+self.urls.getUrl("network_states")

        # init
        self.states = StateSet(self.config)
        self.__setupNetwork()

    # setup
    def __setupNetwork (self):
        try:
            self.G_shp=nx.read_shp(self.urlShp)
            self.G_shp = nx.convert_node_labels_to_integers(self.G_shp, first_label=0, label_attribute = "coord")
        except RuntimeError: print("LOG: no graph from shapefile are fixed. Probably because we not need it")
        self.G_sim = nx.Graph()
        self.G_states = nx.Graph()

    def plotGraph(self):    nx.draw(self.G_shp)

    # get methods
    def getGraphShp(self):       return self.G_shp
    def getGraphSim(self):       return self.G_sim
    def getGraphStates(self):       return self.G_states

    # map states-network
    # ---------------------------------------------------------------------------------------
    def initMapLinks(self):
        self.__mapLinks={}
        tree_net=ET.parse(self.config.urlNetworkTmp)
        root_net=tree_net.getroot()
        links_net=root_net.findall("links")[0]
        for link in links_net:
            attributes=link.find("attributes")
            id_link_states=attributes.findall("./attribute[@name='"+"id_link_states"+"']")[0].text
            self.__mapLinks[int(link.attrib["id"])]=int(id_link_states)

    def getMap(self):   return self.__mapLinks

"""
network: classe generale
network shp per gestire la transformazione in xml dei files shp
    da aggiungere : metodi per il setup dei parametri e per il primo cast

network states: contiene gli states e i metodi della gestione delle performances associati ai link


network sim: contiene metodi per generare il xml da poi usare nella simulazione 


"""

