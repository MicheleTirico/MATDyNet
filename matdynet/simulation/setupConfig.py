

class Config:
    __help = "null"
    __url = 0
    __id = ""

    def __init__(self, id):
        self.__id = id

    def getid(self):
        return self.__id

    def gethelp(self):
        print(self.__help)

    def seturl(self, url):
        self.__url = url

    def geturl(self):
        return __url

class Confignetwork (Config):
    pass


class Configpopulation (Config):
    pass


class ConfigParameters(Config):
    pass
