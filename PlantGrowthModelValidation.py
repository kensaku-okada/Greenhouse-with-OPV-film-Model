# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 21 April 2018
#######################################################

# ####################################################################################################
# np.set_printoptions(threshold=np.inf)
# print "hourlySolarIncidenceAngle:{}".format(np.degrees(hourlySolarIncidenceAngle))
# np.set_printoptions(threshold=1000)
# ####################################################################################################

# ####################################################################################################
# # Stop execution here...
# sys.exit()
# # Move the above line to different parts of the assignment as you implement more of the functionality.
# ####################################################################################################

##########import package files##########
import os as os
import numpy as np
import sys
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulatorConstant as constant
import Util
import datetime
import Lettuce
import PlantGrowthModelE_J_VanHentenConstant as VanHentenConstant
import SimulatorClass
import PlantGrowthModelE_J_VanHenten


def importPlantGrowthModelValidationData(fileName, simulatorClass):

	# fileData = Util.readData(fileName, "", skip_header=1,d='\t')
	fileData = Util.readData(fileName, "", skip_header=1,d=',')
	print("fileData.shape:{}".format(fileData.shape))
	# ####################################################################################################
	# # np.set_printoptions(threshold=np.inf)
	# np.set_printoptions(threshold=np.inf)
	# print("filedata:{}".format(fileData))
	# np.set_printoptions(threshold=1000)
	# ####################################################################################################

	year = np.zeros(fileData.shape[0], dtype=int)
	month = np.zeros(fileData.shape[0], dtype=int)
	day = np.zeros(fileData.shape[0], dtype=int)
	hour = np.zeros(fileData.shape[0], dtype=int)
	GHSolarIrradiance = np.zeros(fileData.shape[0])
	GHAirTemperature = np.zeros(fileData.shape[0])

	for i in range(0, fileData.shape[0]):
		year[i] = int(fileData[i][0])
		month[i] = int(fileData[i][1])
		day[i] = int(fileData[i][2])
		hour[i] = int(fileData[i][3])
		GHSolarIrradiance[i] = fileData[i][4]
		GHAirTemperature[i] = fileData[i][5]

	# print("year[0]:{}".format(year[0]))
	# set the imported values to the object
	simulatorClass.setYear(year)
	simulatorClass.setMonth(month)
	simulatorClass.setDay(day)
	simulatorClass.setHour(hour)
	# simulatorClass.GHSolarIrradianceValidationData = GHSolarIrradiance
	simulatorClass.directSolarIrradianceToPlants = GHSolarIrradiance/2.0
	simulatorClass.diffuseSolarIrradianceToPlants = GHSolarIrradiance/2.0

	simulatorClass.GHAirTemperatureValidationData = GHAirTemperature

	return simulatorClass

########################################################################################################################################
# Note: To run this file and validation, please change constant.SimulationStartDate and constant.SimulationEndDate accordingly
########################################################################################################################################

# data import
# get the num of simulation days
simulationDaysInt = Util.getSimulationDaysInt()

# declare the class and instance
simulatorClass = SimulatorClass.SimulatorClass()

# set spececific numbers to the instance
# simulatorDetail.setSimulationSpecifications(simulatorClass)

##########file import (TucsonHourlyOuterEinvironmentData) start##########
fileName = constant.environmentData
year, \
month, \
day, \
hour, \
hourlyHorizontalDiffuseOuterSolarIrradiance, \
hourlyHorizontalTotalOuterSolarIrradiance, \
hourlyHorizontalDirectOuterSolarIrradiance, \
hourlyHorizontalTotalBeamMeterBodyTemperature, \
hourlyAirTemperature = Util.getArraysFromData(fileName, simulatorClass)
##########file import (TucsonHourlyOuterEinvironmentData) end##########

# # set the imported data
# simulatorClass.hourlyHorizontalDirectOuterSolarIrradiance = hourlyHorizontalDirectOuterSolarIrradiance
# simulatorClass.hourlyHorizontalDiffuseOuterSolarIrradiance = hourlyHorizontalDiffuseOuterSolarIrradiance
# simulatorClass.hourlyHorizontalTotalOuterSolarIrradiance = hourlyHorizontalTotalOuterSolarIrradiance
# simulatorClass.hourlyHorizontalTotalBeamMeterBodyTemperature = hourlyHorizontalTotalBeamMeterBodyTemperature
# simulatorClass.hourlyAirTemperature = hourlyAirTemperature


# import the weather data with which you want to validate the plant growth model. This data overwrite the originally imported data above.
fileName = constant.plantGrowthModelValidationData
importPlantGrowthModelValidationData(fileName, simulatorClass)

# set new data which can be derived from the imported data
Util.deriveOtherArraysFromImportedData(simulatorClass)

FWPerHead, WFreshWeightIncrease, WAccumulatedFreshWeightIncrease, WHarvestedFreshWeight = PlantGrowthModelE_J_VanHenten.calcUnitDailyFreshWeightE_J_VanHenten1994(simulatorClass)

# data export
Util.exportCSVFile(np.array([simulatorClass.getYear(),simulatorClass.getMonth(), simulatorClass.getDay(), simulatorClass.getHour(), \
														 FWPerHead, WFreshWeightIncrease, WHarvestedFreshWeight]).T, "plantGrowthModelValidationdata")

# print("day:{}".format(day))
# print("simulatorClass.getDay():{}".format(simulatorClass.getDay()))
# print("simulatorClass.getDay().shape:{}".format(simulatorClass.getDay().shape))
# print("FWPerHead.shape:{}".format(FWPerHead.shape))

# Util.exportCSVFile(np.array([year,month, day, hour, \
# 														 FWPerHead, WFreshWeightIncrease, WHarvestedFreshWeight]).T, "plantGrowthModelValidationdata")
