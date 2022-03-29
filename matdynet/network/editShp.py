import networkx as nx
import osmnx as ox

from matdynet.network.network import Network


class EditShp (Network):
    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,n,run):
        self.__run=run
        if self.__run:
            self.__n = n
            self.__config = self.__n.config
            try:
                self.__n.G_shp = nx.read_shp(self.__n.urlShp)
                print("LOG: the shp exist and it is in:",self.__n.urlShp)
            except: print ("WARNING: shp does not finded. Would you like to download it? ")


    # handle shp
    # ---------------------------------------------------------------------------------------
    def setupNetwork(self):
        if self.__run:
            try: self.__n.G_shp = nx.read_shp(self.__n.urlShp)
            except RuntimeError:
                self.__dowloadCityFromOx()
                self.__storeNetwork()
                self.__n.G_shp = nx.read_shp(self.__n.urlShp)

    def __dowloadCityFromOx(self):
        self.__G = ox.graph_from_place(self.__n.city, simplify=True)
        print ("City", self.__n.city,"downloaded and stored in",self.__n.urlShpurl)

    def __storeNetwork(self):
        ox.save_graph_shapefile(self.__G, self.__n.urlShp)

    def processingShp (self):
        print ("WARNING: processing shp todo")


    def test(self):
        print (self.__n.G_shp.nodes)
"""
# to move

    def setupValuesShp(self):
        self.__length = nx.get_edge_attributes(self.__G,"length")
        self.__width=nx.get_edge_attributes(self.__G,"width")


    def castToXml (self):
        # init the graph
        self.__G = nx.convert_node_labels_to_integers(self.__G, first_label=0, label_attribute = "coord")

        # init the xml file
        attrib_et_link={}
        et_network = ET.Element("network",attrib={"name":self.__city})
        et_nodes=ET.SubElement(et_network,"nodes")
        et_links=ET.SubElement(et_network,"links",attrib=attrib_et_link)

        # node root
        for i in range(len(self.__n.G_shp.nodes)):
            ET.SubElement(et_nodes,"node",attrib={"id":str(i),
                                                  "x":str(self.__n.G_shp.nodes[i]['coord'][0]),
                                                  "y":str(self.__n.G_shp.nodes[i]['coord'][1]),
                                                  #'type':"2"
                                                  })

        # link root
        self.__length = nx.get_edge_attributes(self.__n.G_shp,"length")
        self.__width=nx.get_edge_attributes(self.__n.G_shp,"width")

        i = 0
        for ed in self.__G.edges:
            startnode,endnode = ed[0],ed[1]
            l =self.__getLength(startnode,endnode,length)
            c = self.__getCapacity(ed)
            fs = self.__getFreeSpeed (ed)
            p = self.__getPermlanes (ed)
            m = self.__getModes (ed)
            w = self.__getWidth(startnode,endnode,width)

            ET.SubElement(et_links,"link",attrib={"id":str(i),
                                                  "from":str(startnode),
                                                  "to":str(endnode),
                                                  "length":str(l),
                                                  "capacity":str(c),
                                                  "permlanes":str(p),
                                                  "freespeed":str(fs)
                                                  })
            i+=1

        # store network
        tree = ET.ElementTree(et_network)
#        header =['<?xml version="1.0" encoding="utf-8"?>','<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v1.dtd">']
        tree.write(self.__urlXml, pretty_print = True)
        tree.write(self.__urlXml,encoding="utf-8",xml_declaration=True,pretty_print = True)


    # private methods
    def __getCapacity (self, ed):
        #        print ("TODO")
        return 0

    def __getFreeSpeed (self, ed):
        #        print ("TODO")
        return 0

    def __getTypeLink (self, ed):
        
        This method set up the type of the link we have. The type came from the table of states.
        :param ed:
        :return:
        
        #        print ("TODO")
        return 0

    def __getLength ( self, startnode,endnode, length) :
        return  round(length [(startnode,endnode)],3)

    def __getPermlanes (self,ed):
        #        print ("TODO")
        return 0

    def __getModes (self,ed):
        #        print ("TODO")
        return 0

    def __getWidth (self, startnode, endnode,width ):
        try: return width([startnode,endnode])
        except: return 0


    # get methods
    # ---------------------------------------------------------------------------------------

"""

 