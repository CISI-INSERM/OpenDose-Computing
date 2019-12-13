from gate import Gate
import os
import time
import random
import signal

class GateLab(Gate):

	notdoneyet = True
	exit_message = "No jobs to launch in this list, safe exit"

	def __init__(self, args):
		Gate.__init__(self, args)

	def getFakeList(self):
		fakeList = [{'workflowID': 1, 'status': "Running"},
					{'workflowID': 2, 'status': "Finished"},
					{'workflowID': 3, 'status': "Pending"},
					{'workflowID': 4, 'status': "Pending"},
					{'workflowID': 5, 'status': "Pending"},
					{'workflowID': 6, 'status': "Pending"},
					]
		return fakeList

	def handleExecutions(self, joblist, jobfile):
		global notdoneyet
		notdoneyet = self.submitJobs(joblist, jobfile, 0)
		# if notdoneyet:
		while notdoneyet:
			result = input("Jobs are launched, do you want more to be launched ? yes / no\n")
			if result == "yes":
				n_jobs = self.checkJobs()
				if self.maxExecsNb - n_jobs > 0:
					notdoneyet = self.submitJobs(joblist, jobfile, n_jobs)
				if not notdoneyet: # double negation 
					break
				time.sleep(5)
			else:
				break
		else:
			self.exitApplication()

	def submitJobs(self, joblist, jobfile, n_jobs):
		for i in range(self.maxExecsNb - n_jobs):
			job = self.getNextJob(joblist)
			if job == False:
				print("No more job to launch, it's over")
				# save joblist to file before exiting
				self.saveJobList(joblist, jobfile)
				return False
			else:
				print("Starting a job")
				workflowID = self.launchExecution(job)
				#TODO : add a test if the launch has failed => do not change the job status
				# set the job status to submitted with a timestamp and set its workflowID
				joblist = self.setJobSubmitted(joblist, job, workflowID)
		# save joblist to file before exiting
		self.saveJobList(joblist, jobfile)
		# Real value is true but for testing we stop after one bunch of jobs
		return True

	def checkJobs(self):
		n_jobs = 0
		# get list of jobs on vip
		if os.environ['DEBUG_VIP'] != "1": 
			# retrieve workflowIDs
			execList = vip.list_executions()
		else:
			execList = self.getFakeList()
		for anExec in execList:
			if anExec['status'] == "Running":
				n_jobs += 1
	        # better to check for finished jobs in another script
	        # if anExec['status'] == "Finished":
	        #     workflowID = anExec['workflowID']
	        #     status = "Finished"
	        #     # set the job status to finished with a timestamp
	        #     joblist = setJobFinished(joblist, workflowID)
	        #TODO : check if a job is in held => change status at held in joblist + send a mail
		print("There are {} running jobs" .format(n_jobs))
		return n_jobs

	def checkHeldJobs(self):
		held_jobs = []
		if os.environ['DEBUG_VIP'] != "1": 
			# retrieve workflowIDs
			execList = vip.list_executions()
		else:
			execList = self.getFakeList()
		for anExec in execList:
			if anExec['status'] == "Held":
				held_jobs.append(anExec['workflowID'])
		

	
	def getNextJob(self, joblist):
		# return the first job in the list with status not submitted (0)
		for job in joblist.itertuples():
			if job.submitted == "0":
				return job
		return False

	def saveJobList(self, joblist, jobfile):
		# save the joblist to a file
		joblist.to_csv(jobfile, index=None)

	def launchExecution(self, job):
		# job looks like this:
		# Pandas(Index=0, model='AF', source=61, particle='gamma', energy=0.2, primaries=100000000, seed=2614427, cpuParam=2, workflowID='workflow-mBt3pB', submitted=0, finished=0, downloaded=0)
		# you can access model with simply job.model
		# to complete...
		datetime = time.strftime('%d-%m-%Y %H:%M')
		executionName = "test opendose client " + datetime
		if os.environ['DEBUG_VIP'] != "1": 
			execID = vip.init_exec('GrepTest/2.0', executionName, {'results-directory':"/vip/Home", 'text':textToSearch,'file':"/vip/Carmin (group)/lorem_ipsum.txt"})
		else:
			execID = "workflow-" + str(random.randrange(1000))
		#TODO : simulate a fake execution in a thread in a random time
		print ("job id : {}".format(execID))
		return execID

	def setJobSubmitted(self, joblist, job, workflowID):
		# set the job status to submitted with a timestamp and set its workflowID
		datetime = time.strftime('%d-%m-%Y %H:%M')
		joblist.loc[job.Index, ['workflowID']] = workflowID
		joblist.loc[job.Index, ['submitted']] = datetime
		return joblist

	def handler(self, signum, frame):
		print(" Interruption signal catched")
		global notdoneyet, exit_message
		notdoneyet = False
		exit_message = "Safe exit"

	def exitApplication(self):
		print(exit_message)