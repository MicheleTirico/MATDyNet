import networkx as nx
import lxml.etree as ET
import shutil
import gzip

# unzip xml file
def unzipXmlGz (pathIn, pathOut):    ET.parse(gzip.open(pathIn)).write(pathOut)



def ciao (run):
    if run :
        print ('run')
        pathIn="/media/mtirico/DATA/project/matdynet/scenarios/orsay_eqasim_02/orsay_households.xml.gz"
        pathOut="/media/mtirico/DATA/project/matdynet/test/openxml.xml"

        unzipXmlGz(pathIn=pathIn,pathOut=pathOut)
ciao(True)