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
        self.__urlPersons=self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/"+self.__config.getUrl("persons")
        self.__urlInputPlans=self.__config.getAbsolutePath()+"/scenarios/"+self.__config.getUrl('scenario')+"/"+self.__config.getUrl("plans")
        self.__urlNetworkStates=self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/"+self.__config.getUrl("network_states")

    def getPersons(self):   return self.__persons

    def __getUrlOutputPlans(self):
        self.__urlPlans=   self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/"+self.__config.getUrl("output_plans")+".xml.gz"
        return self.__urlPlans

    def compute(self,step):
        if self.__typeAnalysis=="score":
            self.__computeScore(step)
        else: print ("ERROR: no type of analysis have bee set")

    def initPersonsXml (self):
        root_out = ET.Element("persons",attrib={"scenario":self.__config.getUrl("scenario")})
        tree_out= ET.ElementTree (root_out)
        tree_in = ET.parse(self.__urlInputPlans)
        root_in = tree_in.getroot()
        for person_in in root_in:
            id = person_in.attrib["id"]
            ET.SubElement(root_out,"person",attrib={"id":id})
            p = Person(id)
            self.__persons.addPerson(p)
        tree_out.write(self.__urlPersons,pretty_print = True)

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
        tree = ET.parse(self.__urlPersons)
        root = tree.getroot()
        for person in root:
            id=person.attrib["id"]
            try:    steps =person[0]
            except: steps=ET.SubElement(person,"steps")
            s=ET.SubElement(steps,"step",{"nstep":str(step)})
            p = self.__persons.getPerson(id)
            scores = p.getScore(step)
            avSc=p.getScore(step)
            ET.SubElement(s,"value",{"name":"averagescore"}).text=str(avSc)
            ET.SubElement(s,"value",{"name":"route"}).text=p.getRouteAsString(step)

        tree.write(self.__urlPersons,pretty_print=True)

    def updatePersons (self,step):
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
                                a=route.text.split(" ")
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
        for each pensor:
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
        tree_persons=ET.parse(self.__urlPersons)
        root_persons=tree_persons.getroot()
        tree_network=ET.parse(self.__urlNetworkStates)
        root_network=tree_network.getroot()
        links=root_network[1]
        for person in root_persons:
            steps=person[0]
            s = steps.find("step",{"nstep":str(step)})
            for value in s:
                name =value.attrib["name"]
                route=""
                if name=="averagescore":valueScore=float(value.text)
                elif name=="route":     route=value.text.split(" ")
            for id_link in route:
                link=links.findall("./link[@id='"+str(id_link)+"']")[0]
                steps_links=link[0]
                s=steps_links.findall("./step[@nstep='"+str(step)+"']")
                if (len(s)==0):
                    s=ET.SubElement(steps_links,"step",{"nstep":str(step)})
                    ET.SubElement(s,"value",{"name":"scoresum"}).text=str(valueScore)
                    ET.SubElement(s,"value",{"name":"pathCount"}).text="1"
                    ET.SubElement(s,"value",{"name":"averagescore"}).text=str(valueScore)
                else:
                    s=s[0]
                    scoreTag=s.findall("./value[@name='scoresum']")[0]
                    oldScoreVal=float(scoreTag.text)
                    pathCountTag=s.findall("./value[@name='pathCount']")[0]
                    oldPathCountVal=int(pathCountTag.text)
                    scoreTag.text=str(oldScoreVal+valueScore)
                    pathCountTag.text=str(oldPathCountVal+1)

        tree_network.write(self.__urlNetworkStates,pretty_print=True)

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