import lxml.etree as ET
import os

from matdynet.network.network import Network


class CreateNetworkStates (Network):
    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,con,net,run):
        super(CreateNetworkStates, self).__init__(con)
        self.network=net
        print ("LOG: (CreateNetworStates) start to create networkStates.xml")
        if run: self.__compute()


    def __compute(self):
        print ("LOG: (CreateNetworStates) start to create networkStates.xml")

        # init the networkStates.xml file
        states_tree = ET.Element("network",attrib={"scenario":str(self.scenario),"type":"networkStates","initstates":self.config.initStates})
        states_nodes=ET.SubElement(states_tree,"nodes")
        states_links=ET.SubElement(states_tree,"links")

        # open the file network.xml
        net_tree = ET.parse(self.urlNetwork)
        net_root=net_tree.getroot()
        net_nodes=net_root.find("nodes")
        net_links=net_root.find("links")

        # init maplinkstate.xml
        maps_tree= ET.Element("maps",attrib={})

        # create nodes
        for net_node in net_nodes:    ET.SubElement(states_nodes,"node",attrib=net_node.attrib)

        # create links
        er=0
        net_list_links=[]
        c_n_link=0
        c_states=0
        for net_link in net_links:
            c_n_link+=1
            id_link=net_link.attrib["id"]
            net_link_from=net_link.attrib["from"]
            net_link_to=net_link.attrib["to"]
            id_states="state_"+str(id_link)

            # handle bus and artificial
            if self.__isLinkArtificial(net_link):
                states_link=ET.SubElement(states_links,"link",attrib={
                    "id":id_link,
                    "from":net_link.attrib["from"],
                    "to":net_link.attrib["to"],
                    "length":net_link.attrib["length"]
                })
                self.setAttribute(states_link,"from",net_link.attrib["from"])
                self.setAttribute(states_link,"to",net_link.attrib["to"])
                self.setAttribute(states_link,"length",net_link.attrib["length"])
                self.setAttribute(states_link,"freespeed",net_link.attrib["freespeed"])
                self.setAttribute(states_link,"capacity",net_link.attrib["capacity"])
                self.setAttribute(states_link,"permlanes",net_link.attrib["permlanes"])
                self.setAttribute(states_link,"oneway",net_link.attrib["oneway"])
                self.setAttribute(states_link,"modes",net_link.attrib["modes"])
                self.setAttribute(states_link,"idinit",id_link)
                self.setAttribute(states_link,"isbusline",self.__isModeInModes("bus",net_link.attrib["modes"]))
                self.setAttribute(states_link,"isartificial",self.__isModeInModes("artificial",net_link.attrib["modes"]))
                ET.SubElement(maps_tree,"map",attrib={"link_net":net_link.attrib["id"],"link_states":id_states})
                c_states+=1
            else:
                if self.__isLinkInList(net_list_links,net_link_from,net_link_to)==False:
                    states_link=ET.SubElement(states_links,"link",attrib={"id":id_link,
                                                                          "from":net_link.attrib["from"],
                                                                          "to": net_link.attrib["to"],
                                                                          "length":net_link.attrib["length"],
                                                                          })
                    steps=ET.SubElement(states_link,"steps",{"name":"steps"})
                    s=ET.SubElement(steps,"step",{"nstep":str(0)})
                    ET.SubElement(s,"value",{"name":"state"}).text=self.config.initStates
                    self.__initSteps(link=states_link)
                    net_attributes=ET.SubElement(states_link,"attributes")

                    try:
                        for attribute in net_attributes:
                            name=attribute.attrib["name"]
                            val=attribute.text
                            self.setAttributeWithAttributes(net_attributes,name,str(val))
                    except TypeError: pass

                    self.setAttributeWithAttributes(net_attributes,"from",net_link.attrib["from"])
                    self.setAttributeWithAttributes(net_attributes,"to",net_link.attrib["to"])
                    self.setAttributeWithAttributes(net_attributes,"length",net_link.attrib["length"])
                    self.setAttributeWithAttributes(net_attributes,"modes",net_link.attrib["modes"])
                    self.setAttributeWithAttributes(net_attributes,"freespeed",net_link.attrib["freespeed"])
                    self.setAttributeWithAttributes(net_attributes,"capacity",net_link.attrib["capacity"])
                    self.setAttributeWithAttributes(net_attributes,"permlanes",net_link.attrib["permlanes"])
                    self.setAttributeWithAttributes(net_attributes,"oneway",net_link.attrib["oneway"])
                    self.setAttributeWithAttributes(net_attributes,"isartificial",False)
                    self.setAttributeWithAttributes(net_attributes,"isbusline",self.__isBusLine(net_link.attrib["modes"]))
                    self.setAttributeWithAttributes(net_attributes,"allowedstates","TODO")
                    self.setAttributeWithAttributes(net_attributes,"initstate",self.config.initStates)
                    self.setAttributeWithAttributes(net_attributes,"idinit",id_link)
                    ET.SubElement(maps_tree,"map",attrib={"link_net":net_link.attrib["id"],"link_states":id_states})
                    print (states_links.findall("./link[@id='"+str(id_states)+"']"),id_states,net_link.attrib["from"],net_link.attrib["to"])
                    c_states+=1
                else:
                    states_link=states_links.findall("./link[@id='"+str(id_states)+"']")
                    print (net_link_from,net_link_to,states_link,id_states)

            net_list_links.append([str(net_link_from), str(net_link_to)])

        print (c_states,c_n_link)

        if er==1:    print("WARNING: at least one link has no width")

        # store network
        tree= ET.ElementTree (states_tree)
        tree.write(self.config.urlNetworkStatesOut, pretty_print = True)
        tree.write(self.config.urlNetworkStatesOut,encoding="utf-8",xml_declaration=True,pretty_print = True)

        # store map
        tree=ET.ElementTree(maps_tree)
        tree.write(self.config.urlMapLinkState, pretty_print = True)

        # create edges
        print ("LOG: (CreateNetworStates) end to create networkStates.xml")


    def __compute_old(self):
        print ("LOG: (CreateNetworStates) start to create networkStates.xml")

        # init the xml file
        sim_tree = ET.Element("network",attrib={"scenario":str(self.scenario),"type":"networkStates","initstates":self.config.initStates})
        sim_nodes=ET.SubElement(sim_tree,"nodes")
        sim_links=ET.SubElement(sim_tree,"links")

        # open the file network.xml
        states_tree = ET.parse(self.urlNetwork)
        states_root=states_tree.getroot()
        states_nodes=states_root.find("nodes")
        states_links=states_root.find("links")

        # init maplinkstate.xml
        maps_tree= ET.Element("maps",attrib={})

        mapLinksNodes={}
        listLinksStates=[]
        # create nodes
        for node in states_nodes:    ET.SubElement(sim_nodes,"node",attrib=node.attrib)

        # create links
        er=0
        list_links=[]
        c_id_state=0
        c_n_link=0
        for states_link in states_links:
            c_n_link+=1
            id_link=states_link.attrib["id"]
            link_from=states_link.attrib["from"]
            link_to=states_link.attrib["to"]
            id_states="state_"+str(c_id_state)
            mapLinksNodes[id_link]=[link_from,link_to]

            # handle bus and artificial
            if self.__isLinkArtificial(states_link):# or self.__isLinkBusLine(link):
                states_link =ET.SubElement(sim_links,"link",attrib={
                    "id":id_states,
                    "from":states_link.attrib["from"],
                    "to":states_link.attrib["to"],
                    "length":states_link.attrib["length"]
                })
                self.setAttribute(states_link,"from",states_link.attrib["from"])
                self.setAttribute(states_link,"to",states_link.attrib["to"])
                self.setAttribute(states_link,"length",states_link.attrib["length"])
                self.setAttribute(states_link,"freespeed",states_link.attrib["freespeed"])
                self.setAttribute(states_link,"capacity",states_link.attrib["capacity"])
                self.setAttribute(states_link,"permlanes",states_link.attrib["permlanes"])
                self.setAttribute(states_link,"oneway",states_link.attrib["oneway"])
                self.setAttribute(states_link,"modes",states_link.attrib["modes"])
                self.setAttribute(states_link,"idinit",id_link)
                listLinksStates.append([id_link,id_states])

            # handle artificial
                if self.__isLinkArtificial(states_link):
                    self.setAttribute(states_link,"isartificial",True)
                    self.setAttribute(states_link,"initstate","staticstate")
                    self.setAttribute(states_link,"allowedStates","nothing")
                else:
                    self.setAttribute(states_link,"isartificial",False)

                # handle bus lines
                if self.__isLinkBusLine(states_link)   :
                    self.setAttribute(states_link,"isbusline",True)
                    self.setAttribute(states_link,"initstate",self.config.initStates)
                    self.setAttribute(states_link,"allowedstates","TODO")
                else:
                    self.setAttribute(states_link,"isbusline",False)
                    self.setAttribute(states_link,"initstate",self.config.initStates)
            elif self.__isLinkBusLine(states_link):
                pass
            else:
                #    ET.SubElement(maps_tree,"map",attrib={"link_net":link.attrib["id"],"link_states":id_states})
                if self.__isLinkInList(list_links,link_from,link_to)==False:
                    c_id_state+=1

                    l =ET.SubElement(sim_links,"link",attrib={"id":id_states,
                                                              "from":states_link.attrib["from"],
                                                              "to": states_link.attrib["to"],
                                                              "length":states_link.attrib["length"],
                                                              })
                    steps=ET.SubElement(states_link,"steps",{"name":"steps"})
                    s=ET.SubElement(steps,"step",{"nstep":str(0)})
                    ET.SubElement(s,"value",{"name":"state"}).text=self.config.initStates
                    self.__initSteps(link=l)

                    states_attributes=ET.SubElement(states_link,"attributes")
                    net_atttributes=states_link.find("attributes")

                    try:
                        for attribute in net_atttributes:
                            name=attribute.attrib["name"]
                            val=attribute.text
                            self.setAttributeWithAttributes(states_attributes,name,str(val))
                    except TypeError: pass

                    self.setAttributeWithAttributes(states_attributes,"from",states_link.attrib["from"])
                    self.setAttributeWithAttributes(states_attributes,"to",states_link.attrib["to"])
                    self.setAttributeWithAttributes(states_attributes,"length",states_link.attrib["length"])
                    self.setAttributeWithAttributes(states_attributes,"modes",states_link.attrib["modes"])
                    self.setAttributeWithAttributes(states_attributes,"freespeed",states_link.attrib["freespeed"])
                    self.setAttributeWithAttributes(states_attributes,"capacity",states_link.attrib["capacity"])
                    self.setAttributeWithAttributes(states_attributes,"permlanes",states_link.attrib["permlanes"])
                    self.setAttributeWithAttributes(states_attributes,"oneway",states_link.attrib["oneway"])
                    self.setAttributeWithAttributes(states_attributes,"isartificial",False)
                    self.setAttributeWithAttributes(states_attributes,"isbusline",self.__isBusLine(states_link.attrib["modes"]))
                    self.setAttributeWithAttributes(states_attributes,"allowedstates","TODO")
                    self.setAttributeWithAttributes(states_attributes,"initstate",self.config.initStates)
                    self.setAttributeWithAttributes(states_attributes,"idinit",id_link)

                    listLinksStates.append([id_link,id_states])


            ET.SubElement(maps_tree,"map",attrib={"link_net":states_link.attrib["id"],"link_states":id_states})


            list_links.append([str(link_from),str(link_to)])

        print (c_id_state,c_n_link)

        if er==1:    print("WARNING: at least one link has no width")

        # store network
        tree= ET.ElementTree (sim_tree)
        tree.write(self.config.urlNetworkStatesOut, pretty_print = True)
        tree.write(self.config.urlNetworkStatesOut,encoding="utf-8",xml_declaration=True,pretty_print = True)

        # store map
        tree=ET.ElementTree(maps_tree)
        tree.write(self.config.urlMapLinkState, pretty_print = True)

        # create edges
        print ("LOG: (CreateNetworStates) end to create networkStates.xml")

    def __isModeInModes(self,mode,modes):
        if mode in modes:   return True
        else:               return False
        
    def __isBusLine(self,modes):
        if "bus" in modes:            return True
        else:               return False

    def     __isLinkBusLine(self,link):
        if "bus" in link.attrib["modes"]:   return True
        else:       return False

    def __isLinkArtificial(self,link):
        if "artificial" in link.attrib["modes"]:   return True
        else:       return False

    def __isLinkInList(self,list_links,link_from,link_to):
        test=False
        for link in list_links:
             if link==[link_to,link_from]: return True
        return test

    def __compute_no_check_directed_links(self):
        print ("LOG: (CreateNetworStates) start to create networkStates.xml")

        # init the xml file
        sim_tree = ET.Element("network",attrib={"scenario":str(self.scenario),"type":"networkStates","initstates":self.config.initStates})
        sim_nodes=ET.SubElement(sim_tree,"nodes")
        sim_links=ET.SubElement(sim_tree,"links")

        # open the file network.xml
        states_tree = ET.parse(self.urlNetwork)
        states_root=states_tree.getroot()
        nodes=states_root.find("nodes")
        links=states_root.find("links")

        # create nodes
        for node in nodes:
            ET.SubElement(sim_nodes,"node",attrib=node.attrib)

        # create links
        er=0
        w=str(0)
        for link in links:
            try: w= link.attrib["width"]
            except: er=1
            states_link =ET.SubElement(sim_links,"link",attrib={"id":link.attrib["id"],
                                                      "state":self.config.initStates,
                                                      "from":link.attrib["from"],
                                                      "to": link.attrib["to"],
                                                      "length":link.attrib["length"],
                                                      "width":str(w)
                                                      })
            steps=ET.SubElement(states_link,"steps",{"name":"steps"})
            s=ET.SubElement(steps,"step",{"nstep":str(0)})
            ET.SubElement(s,"value",{"name":"state"}).text=self.config.initStates

        if er==1: print("WARNING: at least one link has no width")

        # store network
        tree= ET.ElementTree (sim_tree)
        tree.write(self.config.urlNetworkStatesOut, pretty_print = True)
        tree.write(self.config.urlNetworkStatesOut,encoding="utf-8",xml_declaration=True,pretty_print = True)

        # create edges
        print ("LOG: (CreateNetworStates) end to create networkStates.xml")

    def __initSteps (self,link):        steps = ET.SubElement(link,"steps",{"name":"steps"})

