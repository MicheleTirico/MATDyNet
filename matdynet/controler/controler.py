import os
import shutil

from matdynet.analysis.analysis import Analysis
from matdynet.learning.learning import Learning
import lxml.etree as ET

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
#        exit=os.system("java -jar "+self.__config.urlJarTmp + " " +self.__config.urlConfigTmp)
    #    com = "java -cp "+self.__config.urlJar +" org.eqasim.ile_de_france.RunSimulation --config-path "+self.__config.urlConfigTmp
        nameJar=self.__config.nameJar
        print ("----------------",nameJar)
        com="java -Xmx14G -cp "+self.__config.nameJar+" org.eqasim.ile_de_france.RunSimulation --config-path "+self.__config.urlConfigTmp #"/media/mtirico/DATA/project/matdynet/.tmp/orsay_config.xml"
        exit=os.system(com)
        if exit == 256 :
            print("ERROR: jar file not found in ",self.__config.urlJar)

    def __pushExitFiles(self, name_sim):
        # create the folder for the sim
        os.system("mkdir "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+name_sim)
        # create the file of log (TODO)
        os.system("touch "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/"+self.__config.getUrl("scenario")+"_"+name_sim+"_log.md")
        # push outputs in outputs/sims/sim-...
        os.system("cp -r "+self.__config.getAbsolutePath()+"/"+self.__config.getUrl("tmp")+"/output/* "+self.__config.getUrl("url_output")+"/"+self.__config.getUrl("scenario")+"/sims/"+name_sim+"/")

    def __pushFiles(self,pathIn,pathOut):
        for i in range(len(pathIn)):
        #    os.system("cp -r "+ pathIn[i]+" "+pathOut[i])
            try:            shutil.copyfile(pathIn[i],pathOut[i])
            except FileNotFoundError: print ("WARNING: (controler, pushFiles) file","was not founded:",pathIn[i])

    def __pushFolders(self,pathIn,pathOut):
        for i in range(len(pathIn)):            os.system("cp -r "+ pathIn[i]+" "+pathOut[i])

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
        pathIn=[
            self.__config.urlFacilities,           # facilities
            self.__config.urlHouseholds,           # households
            self.__config.urlNetwork,           # network
            self.__config.urlPlans,             # population
            self.__config.urlTransitSchedule,   # transit_schedule
            self.__config.urlTransitVehicles,   # transit_vehicles
            self.__config.urlConfigSim,         # config_sim
            self.__config.urlConfig,            # conig_iter
            self.__config.urlStates,            # states
        ]

        pathOutTmp=[
            self.__config.urlFacilitiesTmp,           # facilities
            self.__config.urlHouseholdsTmp,           # households
            self.__config.urlNetworkTmp,           # network
            self.__config.urlPlansTmp,             # population
            self.__config.urlTransitScheduleTmp,   # transit_schedule
            self.__config.urlTransitVehiclesTmp,   # transit_vehicles
            self.__config.urlConfigSimTmp,         # config_sim
            self.__config.urlConfigTmp,            # conig_iter
            self.__config.urlStatesTmp,            # states
        ]
        pathOutOutputs=[
            self.__config.urlFacilitiesOut,        # facilities
            self.__config.urlHouseholdsOut,        # households
            self.__config.urlNetworkOut,           # network
            self.__config.urlPlansOut,             # population
            self.__config.urlTransitScheduleOut,   # transit_schedule
            self.__config.urlTransitVehiclesOut,   # transit_vehicles
            self.__config.urlConfigSimOut,         # config_sim
            self.__config.urlConfigOut,            # conig_iter
            self.__config.urlStatesOut,            # states
        ]
        """
        pathFolderIn=[self.__config.urlJar]
        pathFolderOutTmp=[self.__config.urlTmp]
        pathFolderOutOutput=[self.__config.urlJarOut]
        """

        self.__pushFiles(pathIn=pathIn,pathOut=pathOutTmp)
        self.__pushFiles(pathIn=pathIn,pathOut=pathOutOutputs)

        self.__analysis.initPersonsXml()
        step = 1
        self.__en.editNetwork(0,self.__config.urlNetworkStatesOut,self.__config.urlNetworkTmp)

        while step <= self.__nMax:
            self.__n.initMapLinks()
            self.__displayStartStep(printAll, step)
            self.__config.initConfigStep(step)
            self.__runIterations()
            self.__pushIterations()
            self.__analysis.updatePersons(step)
            self.__analysis.writePersons(step)
            self.__analysis.compute(step)
            self.__learning.updateAgents(step)
            self.__learning.compute(step)
            self.__en.editNetwork(step,self.__config.urlNetworkStatesOut,self.__config.urlNetworkTmp)

            # push the plans.xml file obtained from the previous sim to tmp directory
            if self.__config.pushPlansFromPreviousSimulation and step>=2:
                pathIn=self.__config.urlOutputSim+"output/output_plans.xml.gz"
                pathOut=self.__config.urlOutputSim+"output/output_plans.xml"
                tree=ET.parse(pathIn)
                tree.write(pathOut)
                self.__pushFiles(pathIn=[pathOut],
                                 pathOut=[self.__config.urlPlansTmp])

            self.__pushFiles(pathIn=[self.__config.urlConfigTmp,self.__config.urlNetworkTmp,self.__config.urlPlansTmp],
                             pathOut=[self.__config.urlConfigOut,self.__config.urlNetworkOut,self.__config.urlPlansOut])

            self.__displayEndStep(printAll,step)
            step+=1

        """
        for agent in self.__learning.getAgents():
            print ("\n-------------------- agent =",agent.getId())
            print ("states",agent.getStates())
            print ("scores",agent.getScores())
            agent.displayQtableStep()
        """
        self.__displayEndSim(printAll)

def __test (run):
    if run :
        url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet/"
__test (False)





