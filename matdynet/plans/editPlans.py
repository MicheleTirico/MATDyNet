from matdynet.config.config import Config
from matdynet.plans.plans import Plans


class EditPlans(Plans):
    def __int__(self,p,c):
        self.plans=p
        self.config=c


def a(run):
    if run:
        print ('run')


a(False)