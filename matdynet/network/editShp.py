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
