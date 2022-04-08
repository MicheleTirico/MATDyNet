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
        self.__nMax=self.__config.nSimMax
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
            os.system("java -jar "+ self.__config.getUrl("jar"))

    def __pushExitFiles(self, name_sim):
        # create the folder for the sim
        os.system("mkdir "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+name_sim)
        # create the file of log (TODO)
        os.system("touch "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/"+self.__config.getUrl("scenario")+"_"+name_sim+"_log.md")
        # push outputs in outputs/sims/sim-...
        os.system("cp -r "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/* "+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+name_sim+"/")
        # delete all files in output
    #    os.system("rm -r " +self.__config.getAbsolutePath()+self.__config.getUrl("tmp")+"/output/*")

    """
    

    def __pushFilesTmp_DEPRECATED(self,step): # deprecated
        pathOut=[self.__config.urlNetworkTmp,self.__config.urlConfigTmp,self.__config.urlPlansTmp]
        pathIn=[]
        for v in ["networksim","config_iter","plans"]: pathIn.append(self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+self.__getNameSim(step-1)+"/"+self.__config.getUrl(v))
        for i in range(len(pathOut)):
            com = "cp "+pathIn[i]+" "+pathOut[i]
            os.system(com)

    def __pushInitFiles_DEPRECATED(self,name_sim,step): # DEPRECATED
        # push networkSim.xml to network_tmp.xml
        command= "cp "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+self.__getNameSim(step-1)+"/"+"network_"+self.__getNameSim(step-1)+".xml "+self.__config.urlNetworkTmp
        os.system(command)
        # plans
        command= "cp "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+self.__getNameSim(step-1)+"/"+"network_"+self.__getNameSim(step-1)+".xml "+self.__config.urlPlansTmp
        os.system(command)
    """

    def __pushFiles(self,pathIn,pathOut):
        for i in range(len(pathIn)):        os.system("cp "+ pathIn[i]+" "+pathOut[i])

    def __pushIterations (self):            os.system("cp -r "+self.__config.urlOutputIter+" "+self.__config.urlOutputSim+"/")

    def __pushFilesTmp(self,step):
        # TO PUSH = config network, plans
        pathIn=[self.__config.urlNetworkOut,self.__config.urlConfigOut,self.__config.urlPlansOut]
        pathOut=[self.__config.urlNetworkTmp,self.__config.urlConfigTmp,self.__config.urlPlansTmp]
        for i in range(len(pathOut)):            os.system("cp "+ pathIn[i]+" "+pathOut[i])

    def __getPathStepBefore(self,step):
        list=[]
        for v in ["networksim","config_iter","plans"]:list.append(self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+self.__getNameSim(step-1)+"/"+self.__config.getUrl(v))
        return list

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
        self.__config.initConfigStep(0)     # setup files output (first step:files network, networkstates, config, plans, outputplals)
        self.__pushFiles(pathIn=[self.__config.urlConfig,self.__config.urlPlans],                     pathOut=[self.__config.urlConfigTmp,self.__config.urlPlansTmp])
        self.__pushFiles(pathIn=[self.__config.urlConfig,self.__config.urlPlans,self.__config.urlNetwork],
                         pathOut=[self.__config.urlConfigOut,self.__config.urlPlansOut,self.__config.urlNetworkOut])
        self.__analysis.initPersonsXml()
        step = 1
        self.__en.editNetwork(0,self.__config.urlNetworkStatesOut,self.__config.urlNetworkTmp)
        while step <= self.__nMax :
            self.__n.initMapLinks()
            self.__displayStartStep (printAll, step)
            self.__config.initConfigStep(step)
        #    self.__runIterations()
            self.__pushIterations()
            self.__analysis.updatePersons(step)
            self.__analysis.writePersons(step)
            self.__analysis.compute(step)
            self.__learning.compute(step)
            self.__en.editNetwork(step,self.__config.urlNetworkStatesOut,self.__config.urlNetworkTmp)
            self.__pushFiles(pathIn=[self.__config.urlConfigTmp,self.__config.urlNetworkTmp,self.__config.urlPlansTmp],
                             pathOut=[self.__config.urlConfigOut,self.__config.urlNetworkOut,self.__config.urlPlansOut])



            #    self.__en.writeXml(step)
            #    self.__pushFiles(pathIn=[self.__config.urlNetworkTmp],pathOut=[self.__config.urlNetworkOut])






            # update network
            #    self.__en.updateStateNetwork(step)

            # push files (todo: add learning and analysis files, chech all others)
            #    self.__pushExitFiles(name_sim)
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





