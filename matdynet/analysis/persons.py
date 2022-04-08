class Persons:
    def __init__(self,scenario):
        self.__scenario=scenario
        self.__persons={}

    #def setPathPersons(self,url ):self.__urlPersons = url
 
    def getPersons (self):          return self.__persons
    def getPerson(self,id):         return self.__persons[id]
    def addPerson (self,person):    self.__persons[person.id]=person

class Person():
    def __init__(self,id):
        self.id=str(id)
        self.__route =[]
        self.__dictStepScore={}
        self.__dictStepRoute={}
        self.__averageScore=0

    def setScore(self,step,score):
        try:    self.__dictStepScore[str(step)]=score
        except KeyError:    print ("ERROR: cannot se the score for the person",id,"at step",step)

    def setRoute(self,step,route):
        try:    self.__dictStepRoute[str(step)]=route
        except KeyError:    print ("ERROR: cannot se the score for the person",id,"at step",step)

    def getRoute(self):     return self.__route
    def getId(self):        return self.id
    def getScore(self,step):
        try:               return self.__dictStepScore[str(step)]
        except KeyError:    print ("ERROR: no score is defined for the person",self.id,"at step",step)

    def getRoute(self,step):
        try:               return self.__dictStepRoute[str(step)]
        except KeyError:    print ("ERROR: no score is defined for the person",self.id,"at step",step)

    def getRouteAsString(self,step):
        l = ""
        for i in self.__dictStepRoute[str(step)]:
            l+=str(i)+" "
        return l[:-1]
"""
    def getAverageScore(self,step):
        a=0
        self.__averageScore = a/len(self.__dictStepScore)
        return self.__averageScore
"""


