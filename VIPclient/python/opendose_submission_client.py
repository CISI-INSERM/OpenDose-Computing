import vip
import time
import random
import sched
import configparser
import math
import re

# get init values from config file
config = configparser.RawConfigParser()	
config.read('config/exec_config.cfg')
apiKey = config.get('application', 'apikey')
gaterelease = config.get('application', 'gaterelease')
application = config.get('application', 'application')
CPUparam = config.get('application', 'CPUparam')
input = config.get('inputs', 'input')
organs =  config.get('inputs', 'organs')
energies = config.get('inputs', 'energies')
particle = 	config.get('inputs', 'particle')
primaries = config.get('inputs', 'primaries')
macfile = config.get('inputs', 'macfile')
outputdir = config.get('inputs', 'outputdir')
reportdir = config.get('reporting', 'reportdir')
reportfile = config.get('reporting', 'reportfile')
# init stuff
vip.setApiKey(apiKey)
maxExecsNb = 2
currentJobs = {}
nextIndexToLaunch = 0

# methods
def computeSeed (model, source, particle, energy) :
	# This function computes a seed for Opendose Gate simulations, by combining
	# numerical values extracted from the simulation input parameters.
	# This ensures all simulations have a different seed, and that there is 
	# enough gaps between seeds to guarantee that subjobs (splitted by GateLab)
	# also have a different seed too.

	# define numerical value corresponding to chosen model
    # if model is AF (adult female), m=0. If model is AM (adult male), m=500
	m = 0
	mregex = re.compile('AM')
	if mregex.search(model) :
		m = 500

	# define numerical value corresponding to chosen particle
	# if particle is an electron, p = 0. If particle is a photon, p=200. 
	p = 0
	pregex = re.compile('gamma')
	if pregex.search(particle) :
		p = 200

	# get numerical value from source organ ID
	s = int(source)
	# get numerical value from source energy
	e = float(energy)
	
	# calculate seed
	# get from energy an int value between 1 and 9999, with a minimal step of 1OO between each
	a = int(1200 * math.log(e*1000) - 1930)
	# get from model, particle and source organ a unique int value
	b = m+p+s;
	
	# make a unique number from all that
	computedSeed = 10000*b + a;
	# convert to string and return result
	seed_as_string = str(computedSeed)
	return seed_as_string		



def launchExecution(textToSearch):

    datetime = time.strftime('%d-%m-%Y %H-%M')
    executionName = "test opendose client " + datetime

    result = vip.init_exec('GrepTest/2.0', executionName, {'results-directory':"/vip/Home", 'text':textToSearch,'file':"/vip/Carmin (group)/lorem_ipsum.txt"})

    print ("job id : {}".format(result))


def handleExecutions(textsToSearch):
    while startJobIfNecessary(textsToSearch):
        time.sleep(60)
    


def startJobIfNecessary(textsToSearch):
    # main loop
    global nextIndexToLaunch
    runningExecs = getRunningExecs()
    runningExecsNb = len(runningExecs)
    print("There are {} running jobs" .format(runningExecsNb))
    for i in range(maxExecsNb - runningExecsNb):
        if nextIndexToLaunch >= len(textsToSearch):
            print("No more job to launch, it's over")
            return False

        print("Starting a job")
        launchExecution(textsToSearch[nextIndexToLaunch])
        nextIndexToLaunch += 1

    return True

        

def getRunningExecs():
    runningExecs = []
    execList = vip.list_executions()
    for anExec in execList:
        if anExec['status'] == "Running":
            runningExecs.append(anExec)
    return runningExecs

	
	

print (outputdir)
# test script

testWords = ["sed", "Donec", "max", "vitae", "dign", "wroooooooong", "ipsum", "nisi"]
#handleExecutions(testWords)


