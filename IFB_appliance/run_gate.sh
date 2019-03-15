#!/bin/bash
#GEANT4 env variables
source /geant4/geant4.10.05-install/bin/geant4.sh
# ROOT env variables
source /cern/root-install/bin/thisroot.sh
# GATE path
export PATH=$PATH:/gate/gate_8.2-install/bin
# cd to the directory where the data are
cd /mnt/gate_data
# run gate
$1/Gate -a [Source_ID,$2][particle,$3][energy,$4][nb,$5] ./mac/$6 > output.log
