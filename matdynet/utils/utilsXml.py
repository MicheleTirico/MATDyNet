import networkx as nx
import lxml.etree as ET
import shutil



def createXmlStates(urlXml,G_shp,scenario,state,initStates):
    """
    this method give the xml of the network with the state of each link
    :param urlXml: the url where store the graph
    :param G: the graph modelled with nx and which came from shapefiles
    :param scenario: the name of the scenario
    :param state: the state to setup
    :return:
    """


    # input : where store the xml, the
    # init the graph
    G = nx.convert_node_labels_to_integers(G_shp, first_label=0, label_attribute = "coord")

    # init the xml file
    attrib_et_link={}
    et_network = ET.Element("network",attrib={"scenario":str(scenario),"type":"networkStates","initStates":initStates})
    et_nodes=ET.SubElement(et_network,"nodes")
    et_links=ET.SubElement(et_network,"links",attrib=attrib_et_link)

    # link root
    length=nx.get_edge_attributes(G_shp,"length")
    width=nx.get_edge_attributes(G_shp,"width")

    # node root
    for i in range(len(G.nodes)):
        ET.SubElement(et_nodes,"node",attrib={"id":"("+str(G.nodes[i]['coord'][0])+", "+str(G.nodes[i]['coord'][0])+")",
                                              "x":str(G.nodes[i]['coord'][0]),
                                              "y":str(G.nodes[i]['coord'][1]),
                                              })


    i = 0
    for ed in G_shp.edges:
        startnode,endnode = ed[0],ed[1]
        l = getLength(startnode,endnode,length)
        w = getWidth(startnode,endnode,width)
        ET.SubElement(et_links,"link",attrib={"id":str(i),
                                              "from":str(startnode),
                                              "to":str(endnode),
                                              "length":str(l),
                                              "width":str(w),
                                              "state":str(state)
                                              })
        i+=1

    # store network
    tree = ET.ElementTree(et_network)
    tree.write(urlXml, pretty_print = True)
    tree.write(urlXml,encoding="utf-8",xml_declaration=True,pretty_print = True)

def getLength ( startnode,endnode, length) :
    return  round(length [(startnode,endnode)],3)

def getWidth (startnode, endnode,width ):
    try: return width([startnode,endnode])
    except: return 0

def createXmlSim(urlSim,urlStates,scenario):
    """
    this method give the xml of the network with the state of each link
    :param urlXml: the url where store the graph
    :param urlXstates: the network of states
    :param scenario: the name of the scenario
    :return:
    """

    shutil.copyfile(urlStates,urlSim)
    tree=ET.parse(urlSim)
    network=tree.getroot()
    nodes=network[0]
    links=network[1]



    # store network
#    tree = ET.ElementTree(et_network)
#    tree.write(urlXml, pretty_print = True)
#    tree.write(urlXml,encoding="utf-8",xml_declaration=True,pretty_print = True)

def getState (link):
    pass

def getNxGfromXml(urlXml):
    G=nx.empty_graph()


def test (run):
    if run :
        urlXml="/media/mtirico/DATA/project/matdynet/scenarios/orsay/test.xml"
        urlXstates="/media/mtirico/DATA/project/matdynet/scenarios/orsay/networkStates.xml"
        scenario="orsay"
        createXmlSim(urlXml,urlXstates,scenario)

test(True)