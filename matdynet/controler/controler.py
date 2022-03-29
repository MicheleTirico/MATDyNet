import os

from matdynet.analysis.analysis import Analysis
from matdynet.config import config
from matdynet.learning.learning import Learning


class Controler:

    #  constructor
    # ---------------------------------------------------------------------------------------
    def __init__(self,con,net,en):
        self.__config = con
        self.__n=net
        self.__nMax = int(self.__config.getVal("simulation","parameter","name","numsim")) #self.__sim.getMaxSim()
        self.__analysis=Analysis(self.__config,self.__n)
        self.__en=en
        self.__learning=Learning(self.__config,self.__n)

    #  private methods
    # ---------------------------------------------------------------------------------------
    def __getNameSim (self, step):  return "sim-{:0>4}".format(step)

    def __runIterations (self):
        exit = os.system("java -jar "+ self.__config.getUrl("jar"))
        if exit == 256 :
            print("jar file not found, try with the absolute path",self.__config.getAbsolutePath())
            os.system("java -jar "+ self.__config.getAbsolutePath()+"/"+self.__config.getUrl("jar"))

    def __pushFiles(self, name_sim):
        # create the folder for the sim
        os.system("mkdir "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+name_sim)
        # create the file of log (TODO)
        os.system("touch "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/"+self.__config.getUrl("scenario")+"_"+name_sim+"_log.md")
        # push outputs in outputs/sims/sim-...
        os.system("cp -r "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/* "+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+name_sim+"/")
        # delete all files in output
    #    os.system("rm -r " +self.__config.getAbsolutePath()+self.__config.getUrl("tmp")+"/output/*")

    #  display
    # ---------------------------------------------------------------------------------------
    def __displayStartSim (self, run):
        if run :            print ("start, max step =",self.__nMax)

    def __displayEndSim (self, run):
        if run :            print ("end sim after steps ",self.__nMax)

    def __displayStartStep (self, run, step):
        if run :            print ("step:",step)

    def __displayEndStep (self, run, step):
        if run :            print ("the step of simulation ended:",step)

    #  run
    # ---------------------------------------------------------------------------------------
    def run (self, printAll):
        self.__displayStartSim(printAll)

        self.__analysis.initPersonsXml()
        step = 1
        while step <= self.__nMax :
            name_sim= self.__getNameSim(step)
            self.__displayStartStep (printAll, step)
        #    self.__runIterations()
            self.__analysis.updatePersons(step)
            self.__analysis.writePersons(step)
            self.__analysis.compute(step)
            self.__learning.compute(step)
        #    self.__analysis.compute(step)
            # compute analysis
            #    self.__analysis.displayTest("here")
            # to do inside
            # create the step <step nstep=step>
            #   add the value score




            # compute learning

            # update network
            #    self.__en.updateStateNetwork(step)

            # push files (todo: add learning and analysis files, chech all others)
            self.__pushFiles(name_sim)
            step +=1
            self.__displayEndStep(printAll,step)

        self.__displayEndSim(printAll)

def __test (run):
    if run :
        url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet/"


#        config = Config(url)
#        controler = Controler(config,network,en)
__test (False)
