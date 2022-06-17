import os

import networkx as nx
import lxml.etree as ET
import gzip
import shutil

from matdynet.plans.transit import Transit
from matdynet.config import config

class SetIdSchedule (Transit):
    # constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,con,tran,run):
        super(SetIdSchedule, self).__init__(con)
        self.transit=tran

        if run: self.__compute()

    def __compute (self):

        print ("LOG: (setIdSchedule) start create new transit_schedule.xml")
        #print (self.config.urlTransitScheduleOut)
        print (self.config.urlTransitSchedule)

        shutil.copyfile(self.config.urlTransitSchedule,self.config.urlTransitScheduleTmp)

        # open transit schedule
        schedule_tree=ET.parse(self.config.urlTransitScheduleTmp)
        schedule_root=schedule_tree.getroot()


        # open maplinkstate
        map_tree=ET.parse((self.config.urlMapLinkState))
        map_root=map_tree.getroot()

        transitStops=schedule_tree.find("./transitStops")
        minimalTransferTimes=schedule_tree.find("./minimalTransferTimes")

        for stopFacifacilities in transitStops:
            linkRefId=stopFacifacilities.attrib["linkRefId"]
            map_link_net=map_root.find("./map[@link_net='"+linkRefId+"']")
            map_link_state=map_link_net.attrib["link_states"]

            """
            # modify id
            id_old=stopFacifacilities.attrib["id"]
            id_new=id_old.replace(linkRefId,map_link_state)
            stopFacifacilities.set("id",id_new)
            """

            # modify linkRefId
            stopFacifacilities.set("linkRefId",map_link_state)
        """
        for relation in minimalTransferTimes:
            link=
            map_link_net=map_root.find("./map[@link_net='"+linkRefId+"']")
            map_link_state=map_link_net.attrib["link_states"]
            print (relation)
            fromStop_old=
        """


        schedule_tree.write(self.config.urlTransitScheduleTmp)



        print (self.config.urlTransitScheduleTmp)

        print ("LOG: (setIdSchedule) end create new transit_schedule.xml")
