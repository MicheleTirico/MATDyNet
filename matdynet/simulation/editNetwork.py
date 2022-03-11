from matdynet.setup import config


class EditNetwork (object):
    __config = 0    # config class
    __sim = 0       # config.simulation class
    __method = 0    # this is the method that we want to use

    def __init__(self, con , sim ):
        self.__config = con
        self.__sim = sim
        self.__method = self.__config.getValWith2Attrib("simulation","parameter",["name","type"],["editnetwork","method"])

    def getconfig (self):   return self.__config

    def getMethod (self):   return self.__method

    def swichMethod (self):
        if self.__method =="random":
            pass
        elif self.method == "test":
            print ("test")
        else:
            print("the method is not correct")

class Random(EditNetwork):

    def __init__(self,con,sim):
        super().__init__(con,sim)


def test (run):
    if run :
        url = "/home/mtirico/project/matdynet/resources/config_sim.xml"
        absPath = "/home/mtirico/project/matdynet"
        c = config.Config(url)
        s = config.Simulation(c)

        en = EditNetwork(c,s)
        print (en.getMethod())
        r = Random(c,s)

test(True)