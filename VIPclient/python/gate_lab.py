from gate import Gate

class GateLab(Gate):

	def __init__(self, args):
		Gate.__init__(self, args)

	def getFakeList():
		fakeList = [{'workflowID': 001, 'status': "running"},
					{'workflowID': 002, 'status': "finished"},
					{'workflowID': 003, 'status': "pending"},
					{'workflowID': 004, 'status': "pending"},
					{'workflowID': 005, 'status': "pending"},
					{'workflowID': 006, 'status': "pending"},
					]

	def startJobIfNecessary(self, joblist, jobfile):
		print("startJobIfNecessary")
	    # main loop
	    n_jobs = 0

	    # get list of jobs on vip
	    if os.environ['DEBUG_VIP'] != "1" : 
	    	execList = vip.list_executions()
	    else
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
	    return True
	    # submit new jobs
	    for i in range(self.maxExecsNb - n_jobs):
	        job = getNextJob(joblist)
	        if job == False:
	            print("No more job to launch, it's over")
	            # save joblist to file before exiting
	            saveJobList(joblist, jobfile)
	            return False
	        else:
	            print("Starting a job")
	            workflowID = launchExecution(job)
	            # set the job status to submitted with a timestamp and set its workflowID
	            joblist = setJobSubmitted(joblist, job, workflowID)
	    # save joblist to file before exiting
	    saveJobList(joblist, jobfile)
	    return True
	