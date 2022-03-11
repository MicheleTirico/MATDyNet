import networkx as nx
"""classe per fare un nx file per analizzare dopo 
"""
class Network ():
    __n = nx.Graph()

    def __init__(self):
        pass

    def buildNetwork(self):
        """
        :return:
        """
        pass
    def getNetwork(self):   return self.__n

    def setStateLink(self):
        pass

    def transformLink (self,idLink,statefrom,stateto):
        pass

def test (run):
    if run :
        print ("go")

test (True)