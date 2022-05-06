from matdynet.analysis.persons import Person, Persons
from matdynet.config.config import Config
from matdynet.network.network import Network

import lxml.etree as ET
import gzip

class Analysis:
    def __init__(self,config,network):
        self.__config = config
        self.__network=network
        self.__typeAnalysis = self.__config.getValsSimulation()["nameAnalysis"]
        self.__G=self.__network.G_sim
        self.__persons = Persons(self.__config.getUrl("scenario"))
    #    self.__urlPersons=self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/"+self.__config.getUrl("persons")
    #    self.__urlInputPlans=self.__config.getAbsolutePath()+"/scenarios/"+self.__config.getUrl('scenario')+"/"+self.__config.getUrl("plans")
        self.__urlNetworkStates=self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/"+self.__config.getUrl("network_states")

    def getPersons(self):   return self.__persons

    def __getUrlOutputPlans(self):
        self.__urlPlans=   self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/"+self.__config.getUrl("output_plans")+".xml.gz"
        return self.__urlPlans

    def compute(self,step):
        if self.__typeAnalysis=="score":    self.__computeScore(step)
        else:                               print ("ERROR: no type of analysis have been set")

    def initPersonsXml (self):
        root_out = ET.Element("persons",attrib={"scenario":self.__config.getUrl("scenario")})
        tree_out= ET.ElementTree (root_out)
        tree_in = ET.parse(self.__config.urlPlans)
        root_in = tree_in.getroot()
        for person_in in root_in:
            id = person_in.attrib["id"]
            ET.SubElement(root_out,"person",attrib={"id":id})
            p = Person(id)
            self.__persons.addPerson(p)
        tree_out.write(self.__config.urlPersonsOut,pretty_print = True)

    def initPersonsFromPlans (self):
        """
        deprecated
        :return:
        """
        with gzip.open(self.__getUrlOutputPlans(), 'rb') as f:    tree = ET.parse(f)
        root = tree.getroot()
        for person in root :
            try:
                id = person.attrib["id"]
                p = Person(id)
                self.__persons.addPerson(p)
            except KeyError: pass

    def writePersons(self,step):
        tree = ET.parse(self.__config.urlPersonsOut)
        root = tree.getroot()
        for person in root:
            id=person.attrib["id"]
            try:    steps =person[0]
            except: steps=ET.SubElement(person,"steps")
            s=ET.SubElement(steps,"step",{"nstep":str(step)})
            p = self.__persons.getPerson(id)
            avSc=round(float(p.getScore(step)),self.__config.roundscoreaverage)
#            print (avSc,type(avSc))
            ET.SubElement(s,"value",{"name":"averagescore"}).text=str(avSc)
            ET.SubElement(s,"value",{"name":"route"}).text=p.getRouteAsString(step)

        tree.write(self.__config.urlPersonsOut,pretty_print=True)

    def updatePersons (self,step):      # this method update the class persons, not the persons.xml file
        with gzip.open(self.__getUrlOutputPlans(), 'rb') as f:
            tree = ET.parse(f)
            for person in tree.getroot() :
                try:
                    id = person.attrib["id"]
                    for plan in person.findall("plan"):
                        if plan.attrib["selected"] == "yes":
                            links= []
                            score=plan.attrib["score"]
                            mix =[]
                            for leg in plan.findall('leg'):
                                route = leg.find("route")
                                try:                    a=route.text.split(" ")
                                except AttributeError:  print("WARNING: no route for the agent",id)
                                mix.append(a)
                            if len(mix)==0: links = mix
                            else:
                                links=mix[0]
                                for i in range(1,len(mix)):
                                    l = mix[i][1:]
                                    for a in l: links.append(a)
                    p = self.__persons.getPerson(id)
                    p.setScore(step,score)
                    p.setRoute(step,links)
                    self.__persons.addPerson(p)
                except KeyError: pass

    def __computeScore(self,step):
        """
        compute for each agent the average score:
        for each pearson:
            score <- get score
            routeStr <- get route
            for each link in routeStr:
                scoreSum += score
                linkSum += i
                i+=1
            xmlLink(step) scoreSum/linkSum
        :param step:
        :return:
        """
        tree_persons=ET.parse(self.__config.urlPersonsOut)
        root_persons=tree_persons.getroot()
        tree_network=ET.parse(self.__config.urlNetworkStatesOut)
        root_network=tree_network.getroot()
        links_network=root_network.findall("links")[0]#root_network[1]
        for person in root_persons:#            print (person.attrib)
            steps=person[0]
            s = steps.find("step",{"nstep":str(step)})
            for value in s:
                name =value.attrib["name"]
                route=""
                if name=="averagescore":valueScore=float(value.text)
                elif name=="route":     route=value.text.split(" ")
            for id_link in route:
                id_link_state=self.__network.getMap()[int(id_link)]
                link=links_network.findall("./link[@id='"+str(id_link_state)+"']")[0]
                steps_links=link[0]
            #    s=steps_links.findall("./step[@nstep='"+str(step)+"']")
                try:                    s=steps_links.findall("./step[@nstep='"+str(step)+"']")[0]
                except IndexError:
                    s=ET.SubElement(steps_links,"step",{"nstep":str(step)})
                try:                    scoreTag=s.findall("./value[@name='scoresum']")[0]
                except IndexError:
                    scoreTag=ET.SubElement(s,"value",{"name":"scoresum"})
                    scoreTag.text=str(valueScore)
                oldScoreVal=float(scoreTag.text)
                try:                    pathCountTag=s.findall("./value[@name='pathCount']")[0]
                except IndexError:
                    pathCountTag=ET.SubElement(s,"value",{"name":"pathCount"})
                    pathCountTag.text="1"
                """
                stepOldTag=steps_links.findall("./step[@nstep='"+str(step-1)+"']")[0]
                stateOldVal=stepOldTag.findall("./value[@name='state']")[0].text
                try:                    stateTag=s.findall("./value[@name='state']")[0]
                except IndexError:
                    stateTag=ET.SubElement(s,"value",{"name":"state"})
                    stateTag.text=stateOldVal
                """
                oldPathCountVal=int(pathCountTag.text)
                scoreSum=oldScoreVal+valueScore
                scoreTag.text=str(round(scoreSum,self.__config.roundscoresum))
                pathCountVal=oldPathCountVal+1
                pathCountTag.text=str(pathCountVal)

                try:                    scoreaverage=s.findall("./value[@name='scoreaverage']")[0]
                except IndexError:
                    scoreAv=ET.SubElement(s,"value",{"name":"scoreaverage"})
                    scoreAv.text=str(scoreSum/pathCountVal)
        tree_network.write(self.__config.urlNetworkStatesOut,pretty_print=True)

    def getTypeAnalysis(self):  return self.__typeAnalysis

    def displayTest (self,text):    print ("class Analysis, I'm",text)

    def __getLink(self,root,id): return         root.find("link",{"id":str(id)})

def __test (run):
    if run :
        url = "/home/mtirico/project/matdynet/scenarios/equil_02/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"

        # config
        con = Config(url)
        con.setAbsolutePath(absPath)
        net = Network(con)

        a = Analysis(con,net)
        a.initPersonsFromPlans()
        step=2
        a.compute(step)
    #    step=4
    #    a.compute(step)

        persons = a.getPersons()


__test(False)