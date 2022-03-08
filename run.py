import subprocess
import os
import shutil
from os.path import exists

# parameters
root="/home/mtirico/project/matdynet/"
name_scenario ="equil"
name_network="network.xml"
name_plans="plans100.xml"
name_config_iter="config.xml"
num_sim = 2

os.system("rm -r "+"outputs")
os.system("rm -r "+".tmp")


# create folder in py: outputs (name as scenario in py)
try:    os.mkdir("outputs") ## improve with root from
except: FileExistsError

try:    os.mkdir("outputs/"+name_scenario) ## improve with root from
except: FileExistsError

try:    os.mkdir("outputs/"+name_scenario+'/sims') ## improve with root from
except: FileExistsError

try:    os.mkdir("outputs/"+name_scenario+'/sims/sim-0000') ## improve with root from
except: FileExistsError

try:    os.mkdir(".tmp/") ## improve with root from
except: FileExistsError

try:    os.mkdir(".tmp/output/") ## improve with root from
except: FileExistsError

# push initial network and plan in sim_step0
shutil.copyfile("scenarios/"+name_scenario+"/"+name_network,"outputs/"+name_scenario +"/sims/sim-0000/network_0000.xml")
shutil.copyfile("scenarios/"+name_scenario+"/"+name_plans,"outputs/"+name_scenario +"/sims/sim-0000/plans_0000.xml")

# push initial files in tmp
shutil.copyfile("scenarios/"+name_scenario+"/"+name_network, ".tmp/network_tmp.xml")
shutil.copyfile("scenarios/"+name_scenario+"/"+name_plans, root+".tmp/plans_tmp.xml")
shutil.copyfile("scenarios/"+name_scenario+"/"+name_config_iter, ".tmp/config_tmp.xml")


# while sim < max :
# clean folder output in ms
# clean folder scenario ms
# push file config_iter.xml, network, plans in matsim
# start sim: run subprocess
# create folder sim_step in py/outputs
# cp network_step in output ms to py/outputs/sim_step
# analysis
# replan network (in py)

" setup root"
step = 1

while step <= num_sim :
    print ("-----------------------------------------\n",step,"\n-----------------------------------------")
    name_sim = "sim-{:0>4}".format(step)
    print(name_sim)
    os.system("java -jar matsim-python.jar")
    os.mkdir("outputs/"+name_scenario+"/sims/"+name_sim)
    os.system("touch .tmp/output/"+name_scenario+"_"+name_sim+"_log.md")
    os.system("cp -r .tmp/output/* outputs/"+name_scenario+"/sims/"+name_sim+"/")
    os.system("rm ./tmp/output/*")
    step+=1






