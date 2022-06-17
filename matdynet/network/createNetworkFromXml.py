import os

import networkx as nx
import lxml.etree as ET
import gzip
import shutil

from matdynet.network.network import Network
from matdynet.config import config

class CreateNetworkFromXml (Network):
    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,con,net,run):
        super(CreateNetworkFromXml, self).__init__(con)
        self.network=net
        keepBus=True
        keepArtificial=True
        if run:
            #self.__compute_with_keep_artificial()
#            self.__compute_with_keep_bus()
            self.__compute_keep(0)

    def __compute_keep(self,step):
        print ("LOG: (CreateNetworkFromXml) start create Network")

        # init network.xml
        network = ET.Element("network",{"name":str(self.scenario)})
        self.setAttribute(network,"state",self.config.initStates)
        self.setAttribute(network,"scenario",self.scenario)
        self.setAttribute(network,"datafrom","xml")
        self.setAttribute(network,"step",str(step))
        sim_nodes=ET.SubElement(network,"nodes")
        sim_links=ET.SubElement(network,"links")

        # open networkStates.xml
        states_tree = ET.parse(self.config.urlNetworkStatesOut)
        states_root=states_tree.getroot()

        # create nodes
        for node in states_root[0]:  ET.SubElement(sim_nodes,"node",attrib=node.attrib)

        # open maplinkstate.xml
        map_tree = ET.parse(self.config.urlMapLinkState)
        map_root=map_tree.getroot()

        # create links
        sim_id_link=1
        states_links=states_root.findall("./links")[0]

        for states_link in states_links:

            map_link_net=map_root.find("./map[@link_states='"+states_link.attrib["id"]+"']")
        #    print (map_link_net.attrib["link_net_init"])
        #    if map_link_net==None: print ("peppe")

        #            if map_link_net.attrib["link_net"]==str(114109):                print ("peppe")
        #    print (map_link_net)
            link_attributes=states_link.find("attributes")
            isbusline=link_attributes.findall("./attribute[@name='isbusline']")[0].text
            isArtificial=link_attributes.findall("./attribute[@name='isartificial']")[0].text
        #    map_link_net.set("link_net_step-"+str(step),states_link.attrib["id"])

            if isArtificial==True:
                sim_link=ET.SubElement(sim_links,"link",attrib={"id":states_link.attrib["id"],
                                                            "from":link_attributes.findall("./attribute[@name='from']")[0].text,
                                                            "to":link_attributes.findall("./attribute[@name='to']")[0].text,
                                                            "length":link_attributes.findall("./attribute[@name='length']")[0].text,
                                                            "freespeed":link_attributes.findall("./attribute[@name='freespeed']")[0].text,
                                                            "capacity":link_attributes.findall("./attribute[@name='capacity']")[0].text,
                                                            "permlanes":link_attributes.findall("./attribute[@name='permlanes']")[0].text,
                                                            "oneway":link_attributes.findall("./attribute[@name='oneway']")[0].text,
                                                            "modes":link_attributes.findall("./attribute[@name='modes']")[0].text
                                                                })
            else:
                if step==0:
                    state=link_attributes.findall("./attribute[@name='initstate']")[0].text      # handle step 0
                else:
                    stepsTag = states_link.find("steps")
                    stepTag=stepsTag.findall("./step[@nstep='"+str(step)+"']")[0]
                    state=stepTag.findall("./value[@name='state']")[0].text

                s=self.states.getState(state)
                for line in s.getLines():
                    modes=line["modes"]
                    dir=list(line["dir"].split("-"))
                    id=str(sim_id_link)+"_step_"+str(step)
                #    map_link_net.set("link_net_step-"+str(step),id)
                    if isbusline=="True" and "car" in line["modes"]:modes="bus,pt,"+line["modes"]
                    sim_link=ET.SubElement(sim_links,"link",attrib={"id":id,
                                                                    "from":states_link.attrib[dir[0]],
                                                                    "to": states_link.attrib[dir[1]],
                                                                    "capacity":line["capacity"],
                                                                    "freespeed":line["freespeed"],
                                                                    "permlanes":line["permlanes"],
                                                                    "modes":modes,
                                                                    "length":states_link.attrib["length"]})

                    self.setAttribute(sim_link,"state",state)
                    #    self.setAttribute(sim_link,"width",link_attributes.findall("./attribute[@name='width']")[0].text)
                    self.setAttribute(sim_link,"id_link_states",states_link.attrib["id"])

                    # set all attributes from networkStates.xml
                    states_attributes=states_link.find("attributes")
                    try:
                        for att in states_attributes:   self.setAttribute(sim_link,att.attrib["name"],str(att.text))
                    except TypeError:                   pass

                    sim_id_link+=1


        fileXml=self.config.urlNetworkXml#self.config.urlTmp+"/networkXml.xml"
        fileXmlGz=self.config.urlNetworkTmp #self.config.urlTmp+"/networkOrsay.xml.gz"
        self.network.addHeaderAndStoreXml(root=network,toAdd=self.config.headerNetworkXml,newf=fileXml,pathTmp=self.urlNetworkToRemove)
        with open(fileXml, 'rb') as f_in:
            with gzip.open(fileXmlGz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # store map
        print (self.config.urlMapLinkState)
        map_tree.write(self.config.urlMapLinkState, pretty_print = True)

        print ("LOG: (CreateNetworkFromXml) end create Network")

    def __compute_with_keep_bus(self):
        print ("LOG: (CreateNetworkFromXml) start create Network")
        step=0

        # init network.xml
        network = ET.Element("network",{"name":str(self.scenario)})
        self.setAttribute(network,"state",self.config.initStates)
        self.setAttribute(network,"scenario",self.scenario)
        self.setAttribute(network,"datafrom","xml")
        self.setAttribute(network,"step",str(step))
        sim_nodes=ET.SubElement(network,"nodes")
        sim_links=ET.SubElement(network,"links")

        # open networkStates.xml
        states_tree = ET.parse(self.config.urlNetworkStatesOut)
        states_root=states_tree.getroot()

        # create nodes
        for node in states_root[0]:  ET.SubElement(sim_nodes,"node",attrib=node.attrib)

        # create links
        sim_id_link=1
        states_links=states_root.findall("./links")[0]
        for link in states_links:
            try:        # keep all links with tokeep attribute
                link_attributes=link.find("attributes")
                sim_link=ET.SubElement(sim_links,"link",attrib={"id":link.attrib["id"],
                                                                "from":link_attributes.findall("./attribute[@name='from']")[0].text,
                                                                "to":link_attributes.findall("./attribute[@name='to']")[0].text,
                                                                "length":link_attributes.findall("./attribute[@name='length']")[0].text,
                                                                "freespeed":link_attributes.findall("./attribute[@name='freespeed']")[0].text,
                                                                "capacity":link_attributes.findall("./attribute[@name='capacity']")[0].text,
                                                                "permlanes":link_attributes.findall("./attribute[@name='permlanes']")[0].text,
                                                                "oneway":link_attributes.findall("./attribute[@name='oneway']")[0].text,
                                                                "modes":link_attributes.findall("./attribute[@name='modes']")[0].text
                                                                })

            except KeyError:    # all others links
                if step==0:     state=link.attrib["state"]      # handle step 0
                else:
                    stepsTag = link.find("steps")
                    stepTag=stepsTag.findall("./step[@nstep='"+str(step)+"']")[0]
                    state=stepTag.findall("./value[@name='state']")[0].text

                s=self.states.getState(state)
                for line in s.getLines():
                    dir=list(line["dir"].split("-"))
                    sim_link=ET.SubElement(sim_links,"link",attrib={"id":str(sim_id_link)+"_step_"+str(step),#link.attrib["id"],
                                                                    "from":link.attrib[dir[0]],
                                                                    "to": link.attrib[dir[1]],
                                                                    "capacity":line["capacity"],
                                                                    "freespeed":line["freespeed"],
                                                                    "permlanes":line["permlanes"],
                                                                    "modes":line["modes"],
                                                                    "length":link.attrib["length"]})

                    self.setAttribute(sim_link,"state",state)
                    self.setAttribute(sim_link,"width",link.attrib["width"])
                    self.setAttribute(sim_link,"id_link_states",link.attrib["id"])

                    # set all attributes from networkStates.xml
                    states_attributes=link.find("attributes")
                    try:
                        for att in states_attributes:   self.setAttribute(sim_link,att.attrib["name"],str(att.text))
                    except TypeError:                   pass

                    sim_id_link+=1

        fileXml=self.config.urlNetworkXml#self.config.urlTmp+"/networkXml.xml"
        fileXmlGz=self.config.urlNetworkTmp #self.config.urlTmp+"/networkOrsay.xml.gz"
        self.network.addHeaderAndStoreXml(root=network,toAdd=self.config.headerNetworkXml,newf=fileXml,pathTmp=self.urlNetworkToRemove)
        with open(fileXml, 'rb') as f_in:
            with gzip.open(fileXmlGz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


        print ("LOG: (CreateNetworkFromXml) end create Network")



    def __compute_with_keep_artificial(self):
        print ("LOG: (CreateNetworkFromXml) start create Network")
        step=0

        # init network.xml
        network = ET.Element("network",{"name":str(self.scenario)})
        self.setAttribute(network,"state",self.config.initStates)
        self.setAttribute(network,"scenario",self.scenario)
        self.setAttribute(network,"datafrom","xml")
        self.setAttribute(network,"step",str(step))
        sim_nodes=ET.SubElement(network,"nodes")
        sim_links=ET.SubElement(network,"links")

        # open networkStates.xml
        states_tree = ET.parse(self.config.urlNetworkStatesOut)
        states_root=states_tree.getroot()

        # create nodes
        for node in states_root[0]:  ET.SubElement(sim_nodes,"node",attrib=node.attrib)

        # create links
        sim_id_link=1
        states_links=states_root.findall("./links")[0]
        for link in states_links:
            try:        # keep all links with isartificial attribute
                isartificial=link.attrib["isartificial"]
                link_attributes=link.find("attributes")
                sim_link=ET.SubElement(sim_links,"link",attrib={"id":link.attrib["id"],
                                                                "from":link_attributes.findall("./attribute[@name='from']")[0].text,
                                                                "to":link_attributes.findall("./attribute[@name='to']")[0].text,
                                                                "length":link_attributes.findall("./attribute[@name='length']")[0].text,
                                                                "freespeed":link_attributes.findall("./attribute[@name='freespeed']")[0].text,
                                                                "capacity":link_attributes.findall("./attribute[@name='capacity']")[0].text,
                                                                "permlanes":link_attributes.findall("./attribute[@name='permlanes']")[0].text,
                                                                "oneway":link_attributes.findall("./attribute[@name='oneway']")[0].text,
                                                                "modes":link_attributes.findall("./attribute[@name='modes']")[0].text
                                                                })

            except KeyError:    # all others links
                if step==0:     state=link.attrib["state"]      # handle step 0
                else:
                    stepsTag = link.find("steps")
                    stepTag=stepsTag.findall("./step[@nstep='"+str(step)+"']")[0]
                    state=stepTag.findall("./value[@name='state']")[0].text

                s=self.states.getState(state)
                for line in s.getLines():
                    dir=list(line["dir"].split("-"))
                    sim_link=ET.SubElement(sim_links,"link",attrib={"id":str(sim_id_link),#link.attrib["id"],
                                                                    "from":link.attrib[dir[0]],
                                                                    "to": link.attrib[dir[1]],
                                                                    "capacity":line["capacity"],
                                                                    "freespeed":line["freespeed"],
                                                                    "permlanes":line["permlanes"],
                                                                    "modes":line["modes"],
                                                                    "length":link.attrib["length"]})

                    self.setAttribute(sim_link,"state",state)
                    self.setAttribute(sim_link,"width",link.attrib["width"])
                    self.setAttribute(sim_link,"id_link_states",link.attrib["id"])

                    # set all attributes from networkStates.xml
                    states_attributes=link.find("attributes")
                    try:
                        for att in states_attributes:   self.setAttribute(sim_link,att.attrib["name"],str(att.text))
                    except TypeError:                   pass

                    sim_id_link+=1

        fileXml=self.config.urlNetworkXml#self.config.urlTmp+"/networkXml.xml"
        fileXmlGz=self.config.urlNetworkTmp #self.config.urlTmp+"/networkOrsay.xml.gz"
        self.network.addHeaderAndStoreXml(root=network,toAdd=self.config.headerNetworkXml,newf=fileXml,pathTmp=self.urlNetworkToRemove)
        with open(fileXml, 'rb') as f_in:
            with gzip.open(fileXmlGz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print ("LOG: (CreateNetworkFromXml) end create Network")

    """
    DEPRECATED
    """
    def __initNetwork(self):
        print ("LOG: (CreateNetworkFromXml) start create Network")
        step=0

        # init network.xml
        network = ET.Element("network",{"name":str(self.scenario)})
        self.setAttribute(network,"state",self.config.initStates)
        self.setAttribute(network,"scenario",self.scenario)
        self.setAttribute(network,"datafrom","xml")
        self.setAttribute(network,"step",str(step))
        sim_nodes=ET.SubElement(network,"nodes")
        sim_links=ET.SubElement(network,"links")

        # open networkStates.xml
        states_tree = ET.parse(self.config.urlNetworkStatesOut)
        states_root=states_tree.getroot()
        states_links=states_root.findall("./links")[0]

        # create nodes
        for sim_node in states_root[0]:
            ET.SubElement(sim_nodes,"node",attrib=sim_node.attrib)

        # create links
        modes=["car","walk","pt","bike"]

        for states_link in states_links:
            states_id=states_link.attrib["id"]
            states_n1=states_link.attrib["n1"]
            states_n2=states_link.attrib["n2"]
            nodes=[states_n1,states_n2]
            for mode in modes:
                sim_link=ET.SubElement(sim_links,"link",attrib={"id":str(states_id+"_"+mode+"_"+str(1)),
                                                                "from":str(states_n1),
                                                                "to":str(states_n2),
                                                                "capacity":str(0),
                                                                "freespeed":str(0),
                                                                "permlanes":str(0),
                                                                "modes":mode,
                                                                "length":str(0)
                                                                })
                sim_link=ET.SubElement(sim_links,"link",attrib={"id":str(states_id+"_"+mode+"_"+str(2)),
                                                                "from":str(states_n2),
                                                                "to":str(states_n1),
                                                                "capacity":str(0),
                                                                "freespeed":str(0),
                                                                "permlanes":str(0),
                                                                "modes":mode,
                                                                "length":str(0)
                                                                })



        fileXml=self.config.urlNetworkXml#self.config.urlTmp+"/networkXml.xml"
        fileXmlGz=self.config.urlNetworkTmp #self.config.urlTmp+"/networkOrsay.xml.gz"
        self.network.addHeaderAndStoreXml(root=network,toAdd=self.config.headerNetworkXml,newf=fileXml,pathTmp=self.urlNetworkToRemove)
        with open(fileXml, 'rb') as f_in:
            with gzip.open(fileXmlGz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)



