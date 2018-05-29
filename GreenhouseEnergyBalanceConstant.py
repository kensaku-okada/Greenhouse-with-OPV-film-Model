# -*- coding: utf-8 -*-

#############command to print out all array data
# np.set_printoptions(threshold=np.inf)
# print ("directSolarRadiationToOPVWestDirection:{}".format(directSolarRadiationToOPVWestDirection))
# np.set_printoptions(threshold=1000)
#############

# ####################################################################################################
# # Stop execution here...
# sys.exit()
# # Move the above line to different parts of the assignment as you implement more of the functionality.
# ####################################################################################################

##########import package files##########
import datetime
import sys
import os
import numpy as np
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
#######################################################

# the heat transfer coefficient [W m-2 Celsius degree] (ASHRAE guide and data book fundamentals, 1981)
# source: https://www.crcpress.com/Greenhouses-Advanced-Technology-for-Protected-Horticulture/Hanan/p/book/9780849316982
# Hanan, J.J. (1998). Chapter 2 Structures: locations, styles, and covers. Greenhouses: advanced technology for protected horticulture (56). CRC Press. Boca Raton, FL.
# I directly got this value from a confidential research thesis in Kacira Lab at CEAC in University of Arizona
U =  6.3
# if the roof is made from double PE
# U =  4.0

# e Stefan-Boltzmann's constant [W m-2 K-4]
delta = 5.67 * 10.0**(-8)

# transmissitiy of thermal radiation (not solar radiation) for the single layer high density polyethylene
# source:Nadia Sabeh, tomato greenhouse roadmap - a guide to greenhouse tomato production, page 24, https://www.amazon.com/Tomato-Greenhouse-Roadmap-Guide-Production-ebook/dp/B00O4CPO42
tau_tc = 0.8
# source: S. Zhu, J. Deltour, S. Wang, 1998, Modeling the thermal characteristics of greenhouse pond systems,
# tau_tc = 0.42

# average emissivity of the interior surface, assuming the high density polyethylene
# source: S. Zhu, J. Deltour, S. Wang, 1998, Modeling the thermal characteristics of greenhouse pond systems,
# epsilon_i = 0.53
# source: Tomohiro OKADA, Ryohei ISHIGE, and Shinji ANDO, 2016, Analysis of Thermal Radiation Properties of Polyimide and Polymeric Materials Based on ATR-IR spectroscopy
# This paper seems to be more reliable at a content of research
epsilon_i = 0.3

################## constnats for Q_e, latent heat transfer by plant transpiration start #######################
# another source: http://edis.ifas.ufl.edu/pdffiles/ae/ae45900.pdf
# specific heat constant pressure [MJ kg-1 Celsius-1]
c_p = 1.013 * 10.0**(-3)

# atmospheric pressure at 700m elevation [KPa]
# source: http://www.fao.org/docrep/X0490E/x0490e07.htm
# source: Water Evaluation And Planning System, user guide, page 17, https://www.sei.org/projects-and-tools/tools/weap/
# elevation of the model [m]
elevation = 700
P = 101.3 * ((293 - 0.0065 * elevation)/293)**5.26

# ratio of molecular weight of water vapor to dry air [0.622]
epsilon = 0.622
# latent heat of water vaporization [MJ kg-1]
# source: https://en.wikipedia.org/wiki/Latent_heat
# lambda_ = 2.2264705
# this source gives a different number 2.45, :http://www.fao.org/docrep/X0490E/x0490e07.htm
# source:  Water Evaluation And Planning System, user guide, page 17, https://www.sei.org/projects-and-tools/tools/weap/
lambda_ = 2.45


# Specific heat of dry air [J kg-1 K-1]
C_p = 1010.0

# the density of air [kg m-3]
rho = 1.204

# the soild flux [W m-2]. It was assumed this value is zero due to the significantly small impact to the model and difficulty of estimation
F = 0.0

################## constnats for Q_e, latent heat transfer by plant transpiration end #######################




