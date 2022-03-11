import networkx as nx
import osmnx as ox
import os
import lxml.etree as ET

from matdynet.setup import config


class Network:
    # __url         = is the complete path+name file to use. If it is not in the folder, we download it

    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self, con):
        self.__config = con
        self.__sim = config.Simulation(self.__config)
        self.__urls = config.Urls(self.__config)
        self.__shp = self.__config.getValWith2Attrib("urls","url",["name","type"],["network_shp","file"])
        self.__city = os.path.splitext(self.__shp)[0]
        self.__url = self.__config.getAbsolutePath()+"/scenarios/"+self.__urls.getUrl("scenario")+"/"+self.__urls.getUrl("network_shp")
        try:    self.__G = nx.read_shp(self.__url)
        except: print ("shp does not finded. Would you like to download it? ")

    def dowloadCityFromOx(self):
        self.__G = ox.graph_from_place(self.__city, simplify=True)
        print ("City", self.__city,"downloaded and stored in",self.__url)

    def storeNetwork(self):
        ox.save_graph_shapefile(self.__G, self.__url)

    def setupNetwork(self):
        try: self.__G = nx.read_shp(self.__url)
        except RuntimeError:
            self.dowloadCityFromOx()
            self.storeNetwork()
            self.__G = nx.read_shp(self.__url)

    def castToXml (self):
        nodes=self.__G.nodes
        edges=self.__G.edges
        print (nodes,edges)

        self.__G = nx.convert_node_labels_to_integers(self.__G, first_label=0, label_attribute = "coord")

        # PARAMETERS
        root ="network"
        name_network=self.__city
        attrib_et_link={}
        et_network = ET.Element(root,attrib={"name":self.__city})
        et_nodes=ET.SubElement(et_network,"nodes")
        et_links=ET.SubElement(et_network,"links",attrib=attrib_et_link)
        urltest = self.__config.getAbsolutePath()+"/resources/test2.xml"



#        self.__G = nx.convert_node_labels_to_integers(self.__G, first_label=0, label_attribute = "coord")

        for i in range(len(self.__G.nodes)):
            ET.SubElement(et_nodes,"node",attrib={"id":str(i),"x":str(self.__G.nodes[i]['coord'][0]), "y":str(self.__G.nodes[i]['coord'][1]),'type':"2"})

        idvar  = nx.get_edge_attributes(self.__G, "id")
        length = nx.get_edge_attributes(self.__G,"length")
        width=nx.get_edge_attributes(self.__G,"width")

        for key, item in enumerate(width):
            if width.get(key) == None:
                print(width[key])
            print(key,item,width.get(key))

        l = round(length [(0,1)],3)
        i = 0
        exp=0
        for ed in self.__G.edges:

            startnode,endnode = ed[0],ed[1]
            l = round(length [(startnode,endnode)],3)
            try: w = width([startnode,endnode])
            except: exp+=1
            ET.SubElement(et_links,"link",attrib={"id":str(i),"from":str(startnode),"to":str(endnode),"length":str(l)})


            i+=1
        print (exp)
#            print (ed,ed[0])
#        for i in range(len(self.__G.edges)):
#            self.__G.edges()[i]
#            endnode =  self.__G.edge()[i][1]
        #    ET.SubElement(et_links,"link",attrib={'id': str(idvar[(startnode, endnode)]),                   'from': str(startnode),        'to':   str(endnode)})


        # store network
        tree = ET.ElementTree(et_network)
        tree.write(urltest, pretty_print = True)

    """
        start = 0
        network = ET.Element("test",attrib={"name":"nameFile"})

        urltest = self.__config.getAbsolutePath()+"/resources/test2.xml"
        tree = ET.ElementTree(network)
        with open(urltest, 'w') as f:
        
        """

    # get methods
    # ---------------------------------------------------------------------------------------
    def getGraph(self): return self.__G
    def getUrl(self):   return self.__url

def test (run):
    if run:
        url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
        c = config.Config(url)
        c.setAbsolutePath("/home/mtirico/project/matdynet/")
        n = Network(c)
        print (n.getUrl())
        n.setupNetwork()

        n.castToXml()
        # G = n.getGraph()


test(True)

