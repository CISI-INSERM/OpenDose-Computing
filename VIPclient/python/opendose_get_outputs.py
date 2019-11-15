import vip
import pandas
from datetime import datetime
import concurrent.futures
import configparser


def downloadFile(vipPath, localPath, logline, logfile, errorlogfile, wID):
	# This function calls CARMIN API to actually download the ouputs of the simulation,
	# as per passed parameters. It logs results (success or error)
	download_result = False
	print (wID + ": start downloading...")
	current_date = datetime.now()
	current_date_string = current_date.strftime("%d/%m/%Y %H:%M:%S")
	# Log download success or error in CSV format, as of:
	# model,source,particle,energy,primaries,seed,cpuParam,workflowID,filepath_on_vip,local_file_name,download_date
	download_result = vip.download (vipPath, localPath)
	if  download_result == True :
		print (wID + ": download successful on " + current_date_string)
		logfile.write(logline + "," + local_file_name + "," + current_date_string+ "\n")
	else :
		print (wID + ": download error")
		errorlogfile.write(logline + "," + current_date_string+ "\n")


# Read config file
config = configparser.RawConfigParser()
config.read('get_outputs.cfg')

# setup API key from config file where it is defined
apiKey = config.get('auth', 'ApiKey')
vip.setApiKey(apiKey)

# Get list of workflows ID for which we need to get the output
workflow_list=config.get('inputs', 'workflow_list')
tab = pandas.read_csv(workflow_list)

# Get success log file name
downloaded_list=config.get('logs','success_log')
# Get error log file name
error_list=config.get('logs','error_log')
# Get list of workflows for which we have already downloaded output
tab_downloaded = pandas.read_csv(downloaded_list)
# set local path/dir in which downloaded files will be stored
local_path = config.get('inputs', 'local_path')

# init executor for downloading in a pool of parallel threads
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
futures = []

# Loop over list of workflows to get their ID + corresponding simulation param values
for x in tab.itertuples():
	# Get workflow ID
	this_workflowID = x.workflowID
	# verify if the output from this workflow has not already been downloaded
	already_downloaded = False
	for w in tab_downloaded.itertuples():
		if w.workflowID == this_workflowID :
			already_downloaded = True
	if already_downloaded == True :
		print (this_workflowID + ": already downloaded, not doing it again")
	else :
		# construct output file name using parameters from the simulation
		if x.particle == "gamma":
			this_particle = "photons"
		else:
			this_particle = "electrons"
		this_outputFileName = x.model + "_" + str(x.source) + "_" + this_particle + "_" + str(x.energy) + "_" + str(x.primaries) + ".tar.gz"
		local_file_name = local_path + this_outputFileName
		# Get output file path for given workflow
		execution_results = vip.get_exec_results(this_workflowID)
		result_path = execution_results[0]['path']
		# construct log line using parameters from the simulation
		logline = x.model + "," + str(x.source) + "," + this_particle + "," + str(x.energy) + "," + str(x.primaries) + "," + str(x.seed) + "," + str(x.cpuParam) + "," + this_workflowID + "," + result_path 
		# Open result and error log files in append mode to update them
		f = open(downloaded_list,"a")
		errlog = open(error_list,"a")
		# Download output (in parallel threads when possible)
		future = executor.submit(downloadFile, result_path, local_file_name, logline, f, errlog, this_workflowID)
		futures.append(future)
		# close log files
		f.close
		errlog.close
	
# wait for all parallel threads to finish
print ("waiting for last running downloads to complete...")
concurrent.futures.wait(futures)
print ("everything completed !")

