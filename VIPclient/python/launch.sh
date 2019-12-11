#!/usr/bin/bash
export OPENDOSE_PATH=$HOME/GIT/domis/opendose/VIPclient

#python3 portal.py -h
python3 portal.py --config "$OPENDOSE_PATH/config/exec_config.cfg" --jobs "$OPENDOSE_PATH/config/AF_batch.csv" --type "LAB"