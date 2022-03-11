import os

from matdynet.setup import config

class Controler:
    __config = 0       # config python class
    __sim = 0       # sim class in config
    __urls = 0       # urls class
    __nMax = 0      # max number of steps

    #  constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self, con):
        self.__config = con
        self.__sim = config.Simulation(self.__config)
        self.__urls = config.Urls(self.__config)
        self.__nMax = self.__sim.getMaxSim()

    #  private methods
    # ---------------------------------------------------------------------------------------
    def __getNameSim (self, step):
        return "sim-{:0>4}".format(step)

    def __runIterations (self):
        exit = os.system("java -jar "+ self.__urls.getUrl("jar"))
        if exit == 256 :
            print("jar file not found, try with the absolute path",self.__config.getAbsolutePath())
            os.system("java -jar "+ self.__config.getAbsolutePath()+"/"+self.__urls.getUrl("jar"))

    def __pushFiles(self, name_sim):
        # create the folder for the sim
        os.system("mkdir "+self.__urls.getUrlAbs(True,"url_output")+"/"+self.__urls.getUrl("scenario")+"/sims/"+name_sim)
        # create the file of log (TODO)
        os.system("touch "+self.__urls.getUrl("tmp")+"/output/"+self.__urls.getUrl("scenario")+"_"+name_sim+"_log.md")
        # push outputs in outputs/sims/sim-...
        os.system("cp -r "+self.__urls.getUrl("tmp")+"/output/* "+self.__urls.getUrl("url_output")+"/"+self.__urls.getUrl("scenario")+"/sims/"+name_sim+"/")
        # delete all files in output
        os.system("rm -r " +self.__urls.getUrl("tmp")+"/output/*")

    #  print
    # ---------------------------------------------------------------------------------------
    def __printStartSim (self, run):
        if run :
            print ("start, max step =",self.__nMax)

    def __printEndSim (self, run):
        if run :
            print ("end sim after steps ",self.__nMax)

    def __printStartStep (self, run, step):
        if run :
            print ("step:",step)

    def __printEndStep (self, run, step):
        if run :
            print ("the step of simulation eded:",step)

    #  run
    # ---------------------------------------------------------------------------------------
    def run (self, printAll):
        self.__printStartSim(printAll)
        step = 1
        while step <= self.__nMax :
            name_sim= self.__getNameSim(step)
            self.__printStartStep (printAll, step)
            self.__runIterations()
            self.__pushFiles(name_sim)
            step +=1
            self.__printEndStep(printAll,step)

        self.__printEndSim(printAll)

def test (run):
    if run :
        url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet/"

        c = config.Config(url);
        c = config.Config(url)
        c.setAbsolutePath(absPath)
        u = config.Urls(c)
        u.deleteExistingFilesAbs(url)
        u.createFoldersAbs(url)

        # push files
        u.pushAllFilesAbs(url)
        s = config.Simulation(c)

        # parameters simulation
        s = config.Simulation(c)
        nMax = s.getMaxSim()


test (False)