from xml.dom import minidom


def getParameters(url, value):
    """
    in : of the config file, the kind of parameter
    out: the dictionary { name of parameter:value}
    """
    dic = {}
    file = minidom.parse(url)
    simulation = file.getElementsByTagName(value)
    for e in simulation:
        dic[e.attributes["name"].value] = e.firstChild.data
    return dic

"""
def getValues(url, label):
    pass


class Xmleditor:
    __help = "null"
    __id = ""

    def __init__(self, id):
        self.__id = id

    def getid(self):
        return self.__id

    def gethelp(self):
        print(self.__help)


class Reader (Xmleditor):
    pass


class Writer (Xmleditor):
    pass
"""
