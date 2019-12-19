from email.mime.text import MIMEText
from gate import Gate
import os
import time
import random
import signal
import numpy as np
import smtplib, ssl
import getpass
from socket import gaierror

class GateLab(Gate):

	# Time to wait in second before checking for jobs status
	exit_message = "No jobs to launch in this list, safe exit"

	def __init__(self, args):
		self.notdoneyet = True
		Gate.__init__(self, args)
		self.handleExecutions()

	def getFakeList(self):
		fakeList = [{'identifier': 1, 'status': "Running"},
					{'identifier': "workflow-EPrOSZ", 'status': "Finished"},
					{'identifier': "workflow-DaNIel", 'status': "Held"},
					{'identifier': 4, 'status': "Killed"},
					{'identifier': 5, 'status': "Killed"},
					{'identifier': 6, 'status': "Killed"},
					]
		return fakeList

	def handleExecutions(self):
		n_free_slots = 0
		# Is it necessary to checkJobs here as we won't be able to launch several time the same jobfile ?
		# => workflowID won't be identical in two different jobfile
		self.tryNewSubmit()
		# if notdoneyet:
		while self.notdoneyet:
			result = input("Jobs are launched, do you want more to be launched ? yes / no\n")
			if result == "yes":
				# check if there is a free slot on VIP
				self.tryNewSubmit()
				# check if jobs are finished
				self.checkFinishedJobs()
				# check if jobs are held
				self.checkHeldJobs()
				# wait before new check
				if self.notdoneyet:
					time.sleep(5)
			else:
				break
		else:
			self.exitApplication()

	def tryNewSubmit(self):
		n_free_slots = self.getFreeSlots()
		if n_free_slots:
			self.submitJobs(n_free_slots)

	# Retrieve running jobs and return available slots from vip list executions
	def getFreeSlots(self):
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

		return self.maxExecsNb - n_jobs

	def submitJobs(self, n_free_slots):
		for i in range(n_free_slots):
			job = self.getNextJob()
			if job == False:
				print("No more job to launch, it's over")
				# save self.joblist to file before exiting
				self.saveJobList()
				# breaks jobs' execution's 
				self.notdoneyet = false
			else:
				print("Starting job: ", job.workflowID)
				workflowID = self.launchExecution(job)
				#TODO : add a test if the launch has failed => do not change the job status
				# set the job status to submitted with a timestamp and set its workflowID
				self.setJobSubmitted(job, workflowID)
		# save self.joblist to file before exiting
		self.saveJobList()

	def checkFinishedJobs(self):
		# Just a short name
		l = self.joblist
		changed = False
		# get list of jobs on vip
		if os.environ['DEBUG_VIP'] != "1": 
			# retrieve workflowIDs
			execList = vip.list_executions()
		else:
			execList = self.getFakeList()

		for anExec in execList:
			if anExec['status'] == "Finished" and (l.loc[l['workflowID']==anExec['identifier'],["finished"]]).values[0][0] == 0:
				print("Job id ", anExec['identifier'], " finished")
				changed = True
				self.setJobFinished(anExec['identifier'])
		if changed:	
			self.saveJobList()


	def checkHeldJobs(self):
		# Just a short name
		l = self.joblist
		changed = False

		if os.environ['DEBUG_VIP'] != "1": 
			# retrieve workflowIDs
			execList = vip.list_executions()
		else:
			execList = self.getFakeList()

		for anExec in execList:
			# Here we define that if the workflow of the exec_list is Held
			# we define the finished value of the joblist to 2
			# this imply that we have delt with this case (email sent)
			if anExec['status'] == "Held" and (l.loc[l['workflowID']==anExec['identifier'],["finished"]]).values[0][0] != 2:
				print("Job id ", anExec['identifier'], " held")
				changed = True
				self.setJobHeld(anExec['identifier'])
				self.sendMail(anExec['identifier'])
		if changed:	
			self.saveJobList()

	def getNextJob(self):
		# return the first job in the list with status not submitted (0)
		for job in self.joblist.itertuples():
			if job.submitted == "0":
				return job
		return False

	def saveJobList(self):
		# save the self.joblist to a file
		self.joblist.to_csv(self.jobfile, index=None)

	def launchExecution(self, job):
		# job looks like this:
		# Pandas(Index=0, model='AF', source=61, particle='gamma', energy=0.2, primaries=100000000, seed=2614427, cpuParam=2, workflowID='workflow-mBt3pB', submitted=0, finished=0, downloaded=0)
		# you can access model with simply job.model
		gaterelease = self.config["gaterelease"]
		application = self.config["application"]
		CPUparam = self.config["CPUparam"]
		gateinput = self.config["gateinput"]
		macfile = self.config["macfile"]
		outputdir = self.config["outputdir"]
		# build the -a [...] string passed to Gate via Gatelab through parameter "phaseSpace"
		alias_string= "-a [Source_ID," + str(job.source) + "][particle," + str(job.particle) + "][energy," + str(job.energy) + "][nb," + str(job.primaries) + "][seed," + str(job.seed) + "]"

		executionName = "OpenDose_GateLab" + "_" + job.model + "_" + str(job.source) + "_" + str(job.particle) + "_" + str(job.energy) + "_" + str(job.primaries)
		datetime = time.strftime('%d-%m-%Y %H:%M')
		print (datetime + " - Launching execution " + executionName)

		if os.environ['DEBUG_VIP'] != "1": 
			execID = vip.init_exec(application, executionName, {'CPUestimation':CPUparam, 'ParallelizationType':"stat", 'GateRelease':gaterelease, 'NumberOfParticles':job.particle, 'GateInput':gateinput, 'phaseSpace':alias_string})
		else:
			execID = "workflow-" + str(random.randrange(1000))
		#TODO : simulate a fake execution in a thread in a random time
		print ("execution id : " + execID)
		return execID
		

	def setJobSubmitted(self, job, workflowID):
		# set the job status to submitted with a timestamp and set its workflowID
		datetime = time.strftime('%d-%m-%Y %H:%M')
		self.joblist.loc[job.Index, ['workflowID']] = workflowID
		self.joblist.loc[job.Index, ['submitted']] = datetime

	def setJobFinished(self, workflowID):
		# set the job status to finished with a timestamp
		datetime = time.strftime('%d-%m-%Y %H:%M')
		self.joblist.loc[self.joblist['workflowID']==workflowID,["finished"]] = datetime

	def setJobHeld(self, workflowID):
		# set the job status to held
		self.joblist.loc[self.joblist['workflowID']==workflowID,["finished"]] = 2

	# Email sending via SSL (http://zetcode.com/python/smtplib/)
	def sendMail(self, workflowID):
		print("Email send to ", self.config['email'])
		smtp_server = "smtp.inserm.fr"
		port = 587

		password = getpass.getpass("Type your password and press enter : ")
		receiver = self.config['email']
		sender = self.config['email']
		user = self.config['email']

		msg = 	''.join(("Hi,\nYour workflow ", 
						 workflowID,
						 " is in held status.\n",
						 "Regards"))

		msg = MIMEText(msg)

		msg['Subject'] = '[opendose] Held workflow'
		msg['From'] = 'opendose@gatelab.com'
		msg['To'] = receiver

		# Secure SSL context
		# Try to log in o server and send email
		try : 
			with smtplib.SMTP("smtp.inserm.fr", port) as server:
			    server.starttls() # Secure the connection
			    server.login(user, password)
			    server.sendmail(sender, receiver, msg.as_string())
		except Exception as e:
			print(e)
		finally:
			print("Mail successfully sent to ", receiver)



	def handler(self, signum, frame):
		print(" Interruption signal catched")
		global exit_message
		self.notdoneyet = False
		exit_message = "Safe exit"

