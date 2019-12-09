import vip
import time
import random
import sched
import configparser

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


