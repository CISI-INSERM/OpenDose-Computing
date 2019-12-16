#!/bin/bash

# Path used to retrieve input jobs file
# In exec_config.cfg, jobfile must be defined from VIPclient directory
export OPENDOSE_PATH="$(dirname "$(pwd)")"
export DEBUG_VIP=1

#python3 portal.py -h
python3 portal.py --config "$OPENDOSE_PATH/config/exec_config.cfg"
