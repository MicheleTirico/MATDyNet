
import shutil
import xml
from xml.dom import minidom
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
    __roots = []            # the list of roots
    # roots = urls, simulation, iterations

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

    # private methods
    # ---------------------------------------------------------------------------------------
    def __setTags (self):
        for elem in self.__tree.iter():  self.__tags.append(elem.tag)
        self.__tags = list(set(self.__tags))

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
        get the map of the values in a root with a tag and and an attribute
        :param root:
        :param tag:
        :param attrib:
        :return:
        """
        l =[]
        root = self.__root.find(root)
        for e in root.iter(tag):
            if e.get(attrib_name) == attrib_val:
                l.append(e.text)
        return l

    def getNames(self,root):
        return list(self.getValsUrl().keys())

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
                               self.getUrl("url_output")+"/"+self.getUrl("scenario")+'/sims/sim-0000',
                               ]
    def __setListUrlFromAndTo (self):
        self.__list_url_from = [self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("network"),
                                self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("plans"),
                                self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("network"),
                                self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("plans"),
                                self.getUrl("url_scenarios")+"/"+self.getUrl("scenario")+"/"+self.getUrl("config_iter")
                                ]
        self.__list_url_to= ["outputs/"+self.getUrl("scenario") +"/sims/sim-0000/network_0000.xml",
                             "outputs/"+self.getUrl("scenario") +"/sims/sim-0000/plans_0000.xml",
                             ".tmp/network_tmp.xml",
                             ".tmp/plans_tmp.xml",
                             ".tmp/config_tmp.xml"
                             ]


    # handle folders
# ---------------------------------------------------------------------------------------
    def getCompleteUrls(self):
        return self.__completeUrls

    def createFolders (self) :
        exit = 0
        for url in self.__completeUrls:
            try :os.mkdir(url)
            except:
                exit = 1
                print (url, "no set up output")
                FileExistsError
        return exit

    def createFoldersAbs (self,absolutePath) :
        exit = 0
        for url in self.__completeUrls:
            try :os.mkdir(absolutePath+"/"+url)
            except:
                exit = 1
                print (url, "no set up output")
                FileExistsError
        return exit

    def deleteExistingFiles(self):
        for url in  [self.getUrl("url_output"),self.getUrl("tmp")]:
            os.system("rm -r "+url)

    def deleteExistingFilesAbs(self,absolutePath):
        for url in[absolutePath+"/"+self.getUrl("url_output"),absolutePath+"/"+self.getUrl("tmp")] :
            os.system("rm -r "+url)

# push files
# ---------------------------------------------------------------------------------------

    def pushAllFiles (self):
        for i in range(0,len(self.__list_url_from)):#    print (i, list_from_abs[i],list_to_abs[i])
            shutil.copyfile(self.__list_url_from[i],self.__list_url_to[i])

    def pushAllFilesAbs (self,absolutePath):
        list_from_abs = [absolutePath+a for a in self.__list_url_from]
        list_to_abs = [absolutePath+a for a in self.__list_url_to]
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

class Simulation (Config):
    __config = 0
    def __init__(self, config ):
        self.__config = config

    def getMaxSim (self):
        pass


def test (run):
    if run:
        url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
        c = Config(url);
    #    print ("tags:", c.getTags(),"\n","roots", c.getRoots(),"\n","url", c.getValsUrl(),"\n","simulation",c.getValsSimulation(),"\n","iterations",c.getValsIteration())#   print ("vals:", c.getValsOfRoot('url'))
        u=Urls(c)
        u.deleteExistingFilesAbs("/home/mtirico/project/matdynet/")
        u.createFoldersAbs("/home/mtirico/project/matdynet/")
        u.pushAllFilesAbs("/home/mtirico/project/matdynet/")
        u.pushAllFiles()
test(False)
