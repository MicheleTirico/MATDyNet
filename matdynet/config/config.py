import shutil
import xml.etree.ElementTree as ET
import os

class Config:
    __url_config_sim= ""    # the complete path of the .xml file
    __urls = {}             # the dic url: val in the tag urls
    __simulation = {}       # the dic of parameters for the simulation: param: val
    __iterations = {}       # the dic of parameters for the iteration: param: val
    __tree = 0              # etree
    __root = 0              # etree
    __tags = []             # the list of all tags
    __roots = []            # the list of roots = urls, simulation, iterations
    __absolutePath = ""     # the root of the project

    #  constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self, url_config):
        self.__url_config_sim = url_config
        self.__tree = ET.parse(url_config)
        self.__root = self.__tree.getroot()
        self.__urls = self.__setDic("urls")
        self.__simulation = self.__setDic("simulation")
        self.__iterations = self.__setDic("iterations")
        self.__setTags()
        self.__setRoots()
        self.initConfig()

    def __init__(self, url_config,absolutePath):
        self.setAbsolutePath(absolutePath)
        self.__url_config_sim = url_config
        self.__tree = ET.parse(url_config)
        self.__root = self.__tree.getroot()
        self.__urls = self.__setDic("urls")
        self.__simulation = self.__setDic("simulation")
        self.__iterations = self.__setDic("iterations")
        self.__setTags()
        self.__setRoots()
        self.initConfig()

    def initConfig(self):
        # urls dir
        self.urlOutput          =self.__absolutePath+"/"+self.getUrl("url_output")+"/"+self.getUrl("scenario")
        self.urlOutputIter      =self.__absolutePath+"/"+self.getUrl("tmp")+"/output/"
        self.urlTmp             =self.__absolutePath+"/"+self.getUrl("tmp")

        # urls names
        self.nameNetwork        = self.getUrl("network").replace(".xml.gz","")
        self.nameNetworkXml     = self.getUrl("network").replace(".gz","")
        self.namePlans          = self.getUrl("plans").replace(".xml.gz","")
        self.nameJar            = self.getUrl("jar").replace(" ","")

        # urls Edit
        self.urlPlansEdit       =self.__absolutePath+"/"+self.getUrl("url_output")+"/"+self.getUrl("scenario")+"/"+self.namePlans+"_edit.xml"

        # parameters
        self.headerNetworkXml="""<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">\n\n"""
        self.nSimMax= int(self.getVal("simulation","parameter","name","numsim"))
        self.randomSeed=self.__getRandomSeed()
        self.pushPlansFromPreviousSimulation=bool(self.getVal("simulation","parameter","name","pushPlansFromPreviousSimulation"))
        self.initStates=self.getVal("simulation","parameter","name","initStates")

        # parameters round
        self.roundscore=int(self.getVal("analysis","parameter","name","roundscore"))
        self.roundscoresum=int(self.getVal("analysis","parameter","name","roundscoresum"))
        self.roundscoreaverage=int(self.getVal("analysis","parameter","name","roundscoreaverage"))
        self.roundqvalue=int(self.getVal("learning","parameter","name","roundqvalue"))

        # url jar
        self.urlJar             = self.__absolutePath+"/"+self.getUrl("jar")

        # url in scenario
        root=self.__absolutePath+"/"+self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")
        self.urlConfig          =root+"/"+self.getUrl("config_iter")
        self.urlConfigSim       =root+"/"+self.getUrl("configsim")
        self.urlNetwork         =root+"/"+self.getUrl("network")
        self.urlPlans           =root+"/"+self.getUrl("plans")
        self.urlStates          =root+"/"+self.getUrl("states")
        self.urlShp             ='TODO'
        self.urlOutputPlans     =root+"/"+self.getUrl("output_plans")
        self.urlFacilities      =root+"/"+self.getUrl("facilities")
        self.urlHouseholds      =root+"/"+self.getUrl("households")
        self.urlTransitSchedule =root+"/"+self.getUrl("transit_schedule")
        self.urlTransitVehicles =root+"/"+self.getUrl("transit_vehicles")

        # url tmp
        root= self.__absolutePath+"/"+self.getUrl("tmp")
        self.urlFacilitiesTmp           =root+"/"+self.getUrl("facilities")
        self.urlHouseholdsTmp           =root+"/"+self.getUrl("households")
        self.urlNetworkTmp              =root+"/"+self.getUrl("network") # "/network_tmp.xml"
        self.urlPlansTmp                =root+"/"+self.getUrl("plans")#/plans_tmp.xml"
        self.urlTransitScheduleTmp      =root+"/"+self.getUrl("transit_schedule")
        self.urlTransitVehiclesTmp      =root+"/"+self.getUrl("transit_vehicles")
        self.urlConfigSimTmp            =root+"/"+self.getUrl("configsim")
        self.urlConfigTmp               =root+"/"+self.getUrl("config_iter") #/config_tmp.xml"
        self.urlStatesTmp               =root+"/"+self.getUrl("states")
        self.urlJarTmp                  =root+"/"+self.getUrl("jar")
        self.urlNetworkXml              =root+"/"+self.nameNetworkXml
        self.urlNetworkXmlName          =root+"/"+self.nameNetwork

        # url output root
        root=self.__absolutePath+"/"+self.getUrl("url_output")+"/"+self.getUrl("scenario")
        self.urlFacilitiesOut              =root+"/"+self.getUrl("facilities")
        self.urlHouseholdsOut              =root+"/"+self.getUrl("households")
        self.urlConfigSimOut            =root+"/"+self.getUrl("configsim")
        self.urlConfigOut               =root+"/"+self.getUrl("network")
        self.urlStatesOut                =root+"/"+self.getUrl("states")
        self.urlJarOut                  =root+"/"+self.getUrl("jar")
        self.urlNetworkStatesOut        =root+"/"+self.getUrl("network_states") # to use when you save at the end
        self.urlShpOut                  ="TODO"
        self.urlPersonsOut              =root+"/"+self.getUrl("persons")
        self.urlMapLinkState               =root+"/"+self.getUrl("maplinkstate")
        
    def __getRandomSeed(self):
        try:
            return int(self.getVal("learning","parameter","name","randomseed"))
        except TypeError:
            pass

    def initConfigStep(self,step):
        root= self.__absolutePath+"/"+self.getUrl("url_output")+"/"+self.getUrl("scenario")+"/sims/"+self.getNameSim(step)+"/"

        # url output sim
        self.urlNetworkOut             =root+self.getUrl("network")
        self.urlPlansOut               =root+self.getUrl("plans")#+".gz" #"output/output_plans.xml.gz" #
        self.urlTransitScheduleOut     =root+self.getUrl("transit_schedule")
        self.urlTransitVehiclesOut     =root+self.getUrl("transit_vehicles")
        self.urlConfigOut              =root+self.getUrl("config_iter")
        #        self.urlOutputPlansOut         =root+self.getUrl("output_plans")
        #        self.urlPlansOld               =self.__absolutePath+"/"+self.getUrl("url_output")+"/"+self.getUrl("scenario")+"/sims/"+self.getNameSim(step-1)+"/output/output_plans.xml"

        # url dir
        self.urlOutputSim              =root

        # create folder to store sim
        os.system("mkdir "+root)

    def getNameSim (self, step):  return "sim-{:0>4}".format(step)

    def setAbsolutePath (self,absolutePath):    self.__absolutePath = absolutePath
    # set methods
    # ---------------------------------------------------------------------------------------
    def __setTags (self):
        for elem in self.__tree.iter():  self.__tags.append(elem.tag)
        self.__tags = list(set(self.__tags))

    # private methods
    # ---------------------------------------------------------------------------------------

    def __setDic ( self, tag ):
        dic = {}
        for i in self.__root.find(tag): dic[i.attrib["name"]]=  i.text
        return dic

    def __setRoots (self):
        for c in self.__root:
            self.__roots.append(c.tag)

    # get methods
    # ---------------------------------------------------------------------------------------
    def getRoots (self): return self.__roots
    def getValsUrl(self) : return self.__urls
    def getValsSimulation(self) : return self.__simulation
    def getValsIteration(self) : return self.__iterations
    def getValsOfRoot (self, root ):
        """
        The method is used to get the dictionary from a root tag
        :param tag: one of roots ?
        :return:
        """
        dic ={}
        try :
            for i in self.__root.find(root):
                dic[i.attrib["name"]]=  i.text
            return dic
        except:
            print (root, "is not a tag in config")
            print ("try a tag in the list:", self.getRoots())
            return 1
    def getTags (self ) :
        """
        :return: all tags in the xml
        """
        return self.__tags
    def getValsWithAttrib (self, root, tag, attrib_name, attrib_val):
        """
        get the map of the values in a root with a tag and an attribute
        :param root:
        :param tag:
        :param attrib:
        :return: a list of values with the attrib ok
        """
        l =[]
        root = self.__root.find(root)
        for e in root.iter(tag):
            if e.get(attrib_name) == attrib_val:
                l.append(e.text)
        return l
    def getValWith2Attrib (self, root, tag, attrib_name, attrib_val):
        """
        eg: config.getValWith2Attrib("urls","url",["name","type"],["network_shp","file"])
        get the map of the values in a root with a tag and an attribute
        :param root:
        :param tag:
        :param attrib:
        :return: a list of values with the attrib ok
        """
        root = self.__root.find(root)
        for e in root.iter(tag):
            if e.get(attrib_name[0]) == attrib_val[0] and e.get(attrib_name[1]) == attrib_val[1]  :
                return e.text
    def getNames(self,root):    return list(self.getValsUrl().keys())
    def getVal (self, root, tag, attrib_name, attrib_val):
        # stop when find the first value of
        root = self.__root.find(root)
        for e in root.iter(tag):
            if e.get(attrib_name) == attrib_val:
                return e.text.replace(" ","")
        print ("value not funded. Try",self.getNames(root))
        print (attrib_val,attrib_name)
        quit()

    def getAbsolutePath (self):            return self.__absolutePath
    def getUrl (self,val): return self.getVal("urls","url","name",val).replace(" ","")
    def getLearning(self,val):return self.getVal("learning","parameter","name",val).replace(" ","")
    def getSimulation (self,val): return self.getVal("simulation","parameter","name",val).replace(" ","")

class Urls (Config):
    __config = 0
    __completeUrls = []
    __list_url_from = [ ]
    __list_url_to= [ ]

    #  constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,config):
        self.__config = config
        self.__setListCompletePath()
        self.__setListUrlFromAndTo()

    #  private methods
    # ---------------------------------------------------------------------------------------

    def __setListCompletePath (self):
        self.__completeUrls = [self.getUrl("tmp")+"/",
                               self.getUrl("tmp")+"/output",
                               self.getUrl("url_output"),
                               self.getUrl("url_output")+"/"+self.getUrl("scenario"),
                               self.getUrl("url_output")+"/"+self.getUrl("scenario")+'/sims',
                  #             self.getUrl("url_output")+"/"+self.getUrl("scenario")+'/sims/sim-0000',
                               ]

    def __setListUrlFromAndTo (self):
        self.__list_url_from = [
            #self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("networksim"),
             #                   self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("plans"),
        #                        self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("networksim"),
                                self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("plans"),
                                self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("config_iter")
                                ]
        self.__list_url_to= [
            #self.getUrl("url_output")+"/"+self.getUrl("scenario") +"/sims/sim-0000/network_sim-0000.xml",
             #                self.getUrl("url_output")+"/"+self.getUrl("scenario") +"/sims/sim-0000/plans_sim-0000.xml",
        #                     self.getUrl("tmp")+"/network_tmp.xml",
                             self.getUrl("tmp")+"/plans_tmp.xml",
                             self.getUrl("tmp")+"/config_tmp.xml"
                             ]


    # handle folders
# ---------------------------------------------------------------------------------------
    def getCompleteUrls(self):  return self.__completeUrls

    def createFolders (self) :
        exit = 0
        for url in self.__completeUrls:
            try :os.mkdir(url)
            except FileExistsError:
                exit = 1
            #    print (url, "no set up output")
        return exit

    def createFoldersAbs (self,absolutePath) :
        exit = 0
        for url in self.__completeUrls:
            try :os.mkdir(absolutePath+"/"+url)
            except FileExistsError:
                exit = 1
                print (url, "no set up output")
        return exit

    def deleteExistingTmp(self):
        try:    shutil.rmtree(self.getUrl("tmp"))
        except FileNotFoundError : pass
        except OSError: pass
        #os.system("rm -r "+self.getUrl("tmp")+"/*")
#        for url in  [self.getUrl("tmp")]:            os.system("rm -r "+url)

    def deleteExistingFiles(self):
        self.deleteExistingTmp()
        self.deleteExistingOutputs()

    def deleteExistingOutputs (self):
        try:    shutil.rmtree(self.__config.urlOutput)
        except FileNotFoundError:pass
        #os.system("rm -r " +self.__config.urlOutput)

# push files
# ---------------------------------------------------------------------------------------

    def pushAllFiles (self):
        for i in range(0,len(self.__list_url_from)):#    print (i, list_from_abs[i],list_to_abs[i])
            shutil.copyfile(self.__list_url_from[i],self.__list_url_to[i])

    def pushAllFilesAbs (self,absolutePath):
        list_from_abs = [absolutePath+"/"+a for a in self.__list_url_from]
        list_to_abs = [absolutePath+"/"+a for a in self.__list_url_to]
        for i in range(0,len(self.__list_url_from)):#    print (i, list_from_abs[i],list_to_abs[i])
            shutil.copyfile(list_from_abs[i],list_to_abs[i])

    # get methods
# ---------------------------------------------------------------------------------------
    def getUrl (self, name):
        """
        get the text from the name of the url. remove all spaces
        :param name: get the name associated to the tag url
        :return: the text of the url without spaces
        """
        try:    return  self.__config.getValsUrl()[name].replace(" ","")
        except:
            print ("exit 1. there are the name:",name," Try:",self.__config.getNames("urls"))
            return ""

    def getUrlAbs(self,useAbs, name):
        """
        get the text from the name of the url. remove all spaces
        :param name: get the name associated to the tag url
        :return: the text of the url without spaces
        """

        try:
            if useAbs:
                return  self.__config.getAbsolutePath()+"/"+ self.__config.getValsUrl()[name].replace(" ","")
            else:
                return  self.__config.getValsUrl()[name].replace(" ","")
        except:
            print ("exit 1. there are the name:",name," Try:",self.__config.getNames("urls"))
            return ""

class Simulation (Config):
    __config = 0
    __maxSimStep = 0

    def __init__(self, config ):
        self.__config = config

    def getMaxSim (self):   return int(self.__config.getVal("simulation","parameter","name","numsim"))

    def getParam (self, name):
        """
        get the text from the name of the url. remove all spaces
        :param name: get the name associated to the tag url
        :return: the text of the url without spaces
        """
        try:    return  self.__config.getValsSimulation()[name].replace(" ","")
        except:
            print ("exit 1. there are the name:",name," Try:",self.__config.getNames("urls"))
            return ""

def test (run):
    if run:
        url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
        c = Config(url)
    #    print ("tags:", c.getTags(),"\n","roots", c.getRoots(),"\n","url", c.getValsUrl(),"\n","simulation",c.getValsSimulation(),"\n","iterations",c.getValsIteration())#   print ("vals:", c.getValsOfRoot('url'))
        u=Urls(c)
        u.deleteExistingFilesAbs("/home/mtirico/project/matdynet/")
        u.createFoldersAbs("/home/mtirico/project/matdynet/")
        u.pushAllFilesAbs("/home/mtirico/project/matdynet/")
        u.pushAllFilesAbs("/home/mtirico/project/matdynet/")
        s = Simulation(c)
        print (s.getMaxSim())

        u.getUrlAbs(True,"url_output")
test(False)
