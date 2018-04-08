# -*- coding: utf-8 -*-

##########import package files##########
from scipy import stats
import sys
import datetime
import os as os
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulatorConstant as constant
import Util
#######################################################

# reference of the model: https://www.tandfonline.com/doi/abs/10.1080/14620316.1997.11515538
# 	A validated model to predict the effects of environment on the growth of lettuce (Lactuca sativa L.): Implications for climate change

# Optimum temperature for conversion  of storage to structural dry weight [Celsius]
T_OS = 30.0
# Partitioning coefficient of storage to structural dry weight [g / (g * day * Celsius)]

#TODO there is no source about the value k. In my model, this was changed in my own way so that the model exibits an appropriate transition of head weight. So, need to validate it.
# k = 6.9 * 10.0**(-2)
k = 6.9 * 10.0**(-2) / 4.0
# Factor to convert CO 2  to plant dry weight [-]
psi = 30.0/44.0
# Distance between plants [m]
h = 0.2
# Leaf area ratio [1/(m^2 * kg)]
F_G = 75.0
# Leaf light utilization efficiency [kg(CO_2) / J ]
alpha_m = 14.0 * 10**(-9)
# Photo-respiration constant [kg(CO_2) / (m^2 * s)]
beta = 1.0 * 10**(-7)
# Leaf conductance
tau = 0.002
# Thermal time for the cessation of photosynthesis [Celsius * d]
theta_m = 1600.0
# Optimum temperature for photosynthesis [Celsius]
T_op = 25.0
# Rate constant for the effect of temperature on  photosynthesis [1/Celcius]
phi = 0.02
# Respiration rate constant [g(W_S)/g(W_G)]
R_G = 0.3
# Ontogenetic respiration rate constant [-]
gamma = 3.0
# Rate constant for  the effect of temperature on respiration [1/Celsius]
epsilon = 0.03


# optimal temperature [Celusius]
# reference: Pearson, S. Hadley, P. Wheldon, A.E. (1993), "A reanalysis of the effects of temperature and irradiance on time to flowering in chrysanthemum (Dendranthema grandiflora)"
# https://scholar.google.com/citations?user=_xeFP80AAAAJ&hl=en#d=gs_md_cita-d&p=&u=%2Fcitations%3Fview_op%3Dview_citation%26hl%3Den%26user%3D_xeFP80AAAAJ%26citation_for_view%3D_xeFP80AAAAJ%3Au-x6o8ySG0sC%26tzom%3D420
# Effective temperature is the sub-optimum temperature equivalent of a supra-optimum temperature in terms of developmental rate.
T_o = T_op


