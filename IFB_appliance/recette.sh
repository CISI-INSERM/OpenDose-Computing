#!/bin/bash
# add wget & unzip that are not here by default
yum install wget
yum install unzip
# install Boutiques
sudo pip install boutiques
# Get Gate docker image
docker pull opengatecollaboration/gate