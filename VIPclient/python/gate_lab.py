from gate import Gate
import os
import time
import random

class GateLab(Gate):

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

	def handleExecutions(self):
		while self.startJobIfNecessary(joblist, jobfile):
	        time.sleep(60)

	def startJob(self):
		n_jobs = 0
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
				# set the job status to submitted with a timestamp and set its workflowID
				joblist = self.setJobSubmitted(joblist, job, workflowID)
		# save joblist to file before exiting
		self.saveJobList(joblist, jobfile)

	def startJobIfNecessary(self, joblist, jobfile):
		print("startJobIfNecessary")
		# main loop
		n_jobs = 0

		# get list of jobs on vip
		if os.environ['DEBUG_VIP'] != "1": 
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
		print("There are {} running jobs" .format(n_jobs))
		# submit new jobs
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
				# set the job status to submitted with a timestamp and set its workflowID
				joblist = self.setJobSubmitted(joblist, job, workflowID)
		# save joblist to file before exiting
		self.saveJobList(joblist, jobfile)
		return False
	
	def getNextJob(self, joblist):
		# return the first job in the list with status not submitted (0)
		for job in joblist.itertuples():
			if job.submitted == 0:
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
		print ("job id : {}".format(execID))
		return execID

	def setJobSubmitted(self, joblist, job, workflowID):
		# set the job status to submitted with a timestamp and set its workflowID
		datetime = time.strftime('%d-%m-%Y %H:%M')
		joblist.loc[job.Index, ['workflowID']] = workflowID
		joblist.loc[job.Index, ['submitted']] = datetime
		return joblist