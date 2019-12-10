import vip
import time
import random
import sched
import configparser
import pandas as pd
import math
import re

# get init values from config file
config = configparser.RawConfigParser()	
config.read('../config/exec_config.cfg')
apiKey = config.get('application', 'apikey')
gaterelease = config.get('application', 'gaterelease')
application = config.get('application', 'application')
CPUparam = config.get('application', 'CPUparam')
gateinput = config.get('inputs', 'input')
macfile = config.get('inputs', 'macfile')
outputdir = config.get('inputs', 'outputdir')
jobfile = config.get('jobs', 'jobfile')

# init stuff
vip.setApiKey(apiKey)
maxExecsNb = 2 # should be from the config file no ?

# methods
def readJobList(jobfile):
    joblist = pd.read_csv(jobfile)
    return joblist

def setJobSubmitted(joblist, job, workflowID):
    # set the job status to submitted with a timestamp and set its workflowID
    datetime = time.strftime('%d-%m-%Y %H:%M')
    joblist.loc[job.Index, ['workflowID']] = workflowID
    joblist.loc[job.Index, ['submitted']] = datetime
    return joblist

def setJobFinished(joblist, workflowID):
    # set the job status to finished with a timestamp
    datetime = time.strftime('%d-%m-%Y %H:%M')
    joblist.loc[joblist['workflowID']==workflowID,["finished"]] = datetime
    return joblist

def getNextJob(joblist):
    # return the first job in the list with status not submitted (0)
    for job in joblist.itertuples():
        if job.submitted == 0:
            return job
    return False

def saveJobList(joblist, jobfile):
    # save the joblist to a file
    joblist.to_csv(jobfile, index=None)

def computeSeed (model, source, particle, energy) :
    # do we need this function here ?
    # if all is simulations parameters are pre-calculated and in the joblist CSV we don't need it here

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


def launchExecution(job):
    # job looks like this:
    # Pandas(Index=0, model='AF', source=61, particle='gamma', energy=0.2, primaries=100000000, seed=2614427, cpuParam=2, workflowID='workflow-mBt3pB', submitted=0, finished=0, downloaded=0)
    # you can access model with simply job.model
    # to complete...
    datetime = time.strftime('%d-%m-%Y %H:%M')
    executionName = "test opendose client " + datetime

    result = vip.init_exec('GrepTest/2.0', executionName, {'results-directory':"/vip/Home", 'text':textToSearch,'file':"/vip/Carmin (group)/lorem_ipsum.txt"})

    print ("job id : {}".format(result))


def startJobIfNecessary(joblist, jobfile):
    # main loop
    n_jobs = 0
    max_jobs = 25

    # get list of jobs on vip
    execList = vip.list_executions()
    for anExec in execList:
        if anExec['status'] == "Running":
            n_jobs += 1
        if anExec['status'] == "Finished":
            workflowID = anExec['workflowID']
            status = "Finished"
            # set the job status to finished with a timestamp
            joblist = setJobFinished(joblist, workflowID)
    print("There are {} running jobs" .format(n_jobs))

    # submit new jobs
    for i in range(max_jobs - n_jobs):
        job = getNextJob(joblist)
        if job == False:
            print("No more job to launch, it's over")
            # save joblist to file before exiting
            saveJobList(joblist, jobfile)
            return False
        else:
            print("Starting a job")
            workflowID = launchExecution(job)
            workflowID = 'toto-1337'
            # set the job status to submitted with a timestamp and set its workflowID
            joblist = setJobSubmitted(joblist, job, workflowID)
    # save joblist to file before exiting
    saveJobList(joblist, jobfile)
    return True


def handleExecutions(joblist, jobfile):
    while startJobIfNecessary(joblist, jobfile):
        time.sleep(60)


# main program
print(jobfile, macfile)

# read job list from CSV
joblist = readJobList(jobfile)

# main loop
handleExecutions(joblist, jobfile)

