from .scenario import config
import subprocess

subprocess.call(['java','-jar','resources/matsim-python-1.0.jar'])
# get parameters
# parameters = config.getparameters()

