This is the directory in which all config files used by the VIP client are to be located.

## config files for API setup (for java client code)
- **apiURL.txt** is where you define the VIP CARMIN API REST endpoint
- **apiKey.txt** is where you put your personal userkey, generated from your account page on the VIP portal

## Config files for execution
- **exec_config.txt** (for java client code) and  **exec_config.cfg** (for python client code) are the main configuration files for setting up execution for the java client code. They define:
  - application to be used (GateLab or GateCLforOpenDose)
  - The GateLab CPUparam in case you use it (value between 1 and 4, see GateLab documentation)
  - The name of the file containing the list of source organ IDs (see below)
  - The name of the file containing the list of energies (see below)
  - the type of particle to simulate (e- or gamma)
  - the number of events(primaries) to simulate
  - the LFN of the input data for the simulations
  - the link to the Gate Release to use
  - the path and name of the macfile to use
  - the path to the directory in which you want the report/log files to be written
  - the VIP/grid directory in which you want your outputs to be stored (GateCLforOpenDose only)
- **energies_list.txt** is the list of energies you want to use as parameters for your simulations
- **organs_list.txt** is the list of source organ IDs you want to use as parameters for your simulations

## Config file for getting outputs (for python client code)  
- **get_outputs.cfg** defines the API key to use, the list of executions for which we want to download outputs, the local path to which we want to save files, and the log files.

When modifying these files to customise your executions, please don't change order or syntax as parsing is admittedly not very robust (you are welcome to improve it btw)
