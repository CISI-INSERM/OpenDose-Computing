from gate_lab import GateLab
from gate_CL import GateCL

# Prend 3 params en entrée : fichier config, fichier csv, LAB / CL

b1 = GateLab("~/GIT/domis/opendose/GATE")
b2 = GateCL("~/GIT/domis/opendose/CL")
b1.getConfigPath()
b2.getConfigPath()