# Running Gate for OpenDose in a VM on the IFB cloud: How To

## Start and prepare the VM

Launch CentOS appliance on Biosphère

SSH to it (and su)

Run configuration to make it a "Gate appliance"
(summary in recette.sh, soon to be integrated at build time in a specific appliance)
```bash
# add wget & unzip that are not here by default
yum -y install wget
yum -y install unzip
# install Boutiques
pip install boutiques
# Get Gate docker image
docker pull opengatecollaboration/gate
```
Get the data (summary in get_data.sh) and the running script
```bash
wget https://github.com/CISI-INSERM/OpenDose-Computing/raw/master/Boutiques/gate-opendose-descriptor-docker.json
wget https://github.com/CISI-INSERM/OpenDose-Computing/raw/master/Boutiques/input_example-docker.json
wget https://github.com/CISI-INSERM/OpenDose-Computing/raw/master/inputs/OpenDoseInputData2018-11-14.zip
wget https://github.com/CISI-INSERM/OpenDose-Computing/raw/master/IFB_appliance/run_gate.sh
chmod a+x run_gate.sh
# unzip input data
unzip OpenDoseInputData2018-11-14.zip
```

## Run OpenDose stuff

### OPTION 1: run docker directly

Run gate in the docker container with the parameter values you want:
(1: path to Gate, 2:source_id, 3:particle, 4:energy, 5:nb_primaries, 6:macfile)
```bash
docker run -v /home/centos:/mnt/gate_data opengatecollaboration/gate bash -c "/mnt/gate_data/run_gate.sh /gate/gate_8.2-install/bin 95 e- 0.005 1000 main_AF.mac"
```
### OPTION 2: run through boutiques
```bash
bosh exec launch gate-opendose-descriptor-docker.json input_example-docker.json
```	
