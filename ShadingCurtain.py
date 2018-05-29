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
from scipy import stats
import datetime
import calendar
import sys
import os as os
import numpy as np
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
import OPVFilm
#import Lettuce
import CropElectricityYeildSimulatorDetail as simulatorDetail
import SimulatorClass
#######################################################


# def getHourlyShadingCurtainDeploymentPatternChangingEachMonthPrep():
# 	'''
# 	calculate the shading curtain deployment start and end hour each month so that the average DLI becomes as optimal (constant.DLIforTipBurn) as possible
# 	The optimal hour is calculated by averaging the solar irradiance each month
# 	'''
#
# 	# get the num of simulation days
# 	simulationDaysInt = util.getSimulationDaysInt()
#
# 	# declare the class and instance
# 	simulatorClass = SimulatorClass.SimulatorClass()
#
# 	##########file import (TucsonHourlyOuterEinvironmentData) start##########
# 	fileName = constant.environmentData
# 	year, \
# 	month, \
# 	day, \
# 	hour, \
# 	hourlyHorizontalDiffuseOuterSolarIrradiance, \
# 	hourlyHorizontalTotalOuterSolarIrradiance, \
# 	hourlyHorizontalDirectOuterSolarIrradiance, \
# 	hourlyHorizontalTotalBeamMeterBodyTemperature, \
# 	hourlyAirTemperature = util.getArraysFromData(fileName, simulatorClass)
# 	##########file import (TucsonHourlyOuterEinvironmentData) end##########
#
# 	# set the imported data
# 	simulatorClass.hourlyHorizontalDirectOuterSolarIrradiance = hourlyHorizontalDirectOuterSolarIrradiance
# 	simulatorClass.hourlyHorizontalDiffuseOuterSolarIrradiance = hourlyHorizontalDiffuseOuterSolarIrradiance
# 	simulatorClass.hourlyHorizontalTotalOuterSolarIrradiance = hourlyHorizontalTotalOuterSolarIrradiance
# 	simulatorClass.hourlyHorizontalTotalBeamMeterBodyTemperature = hourlyHorizontalTotalBeamMeterBodyTemperature
# 	simulatorClass.hourlyAirTemperature = hourlyAirTemperature
#
# 	# set new data which can be derived from the imported data
# 	util.deriveOtherArraysFromImportedData(simulatorClass)
#
# 	################################################################################
# 	##########solar irradiance to OPV calculation with imported data start##########
# 	################################################################################
# 	if constant.ifUseOnlyRealData == True:
#
# 		# calculate with real data
# 		# hourly average [W m^-2]
# 		directSolarRadiationToOPVEastDirection, \
# 		directSolarRadiationToOPVWestDirection, \
# 		diffuseSolarRadiationToOPV, \
# 		albedoSolarRadiationToOPV = simulatorDetail.calcOPVmoduleSolarIrradianceGHRoof(simulatorClass)
#
# 		# set the calculated data
# 		simulatorClass.setDirectSolarRadiationToOPVEastDirection(directSolarRadiationToOPVEastDirection)
# 		simulatorClass.setDirectSolarRadiationToOPVWestDirection(directSolarRadiationToOPVWestDirection)
# 		simulatorClass.setDiffuseSolarRadiationToOPV(diffuseSolarRadiationToOPV)
# 		simulatorClass.setAlbedoSolarRadiationToOPV(albedoSolarRadiationToOPV)
#
# 		# [W m^-2] per hour
# 		totalSolarRadiationToOPV = (simulatorClass.getDirectSolarRadiationToOPVEastDirection() + simulatorClass.getDirectSolarRadiationToOPVWestDirection()) / 2.0 \
# 															 + simulatorClass.getDiffuseSolarRadiationToOPV() + simulatorClass.getAlbedoSolarRadiationToOPV()
#
# 		###################data export start##################
# 		util.exportCSVFile(np.array(
# 			[year, month, day, hour, simulatorClass.getDirectSolarRadiationToOPVEastDirection(), simulatorClass.getDirectSolarRadiationToOPVWestDirection(), \
# 			 simulatorClass.getDiffuseSolarRadiationToOPV(), simulatorClass.getAlbedoSolarRadiationToOPV(), totalSolarRadiationToOPV]).T,
# 											 "hourlyMeasuredSolarRadiations")
# 		###################data export end##################
#
# 		###################data export start##################
# 		util.exportCSVFile(np.array([year, month, day, hour, hourlyHorizontalTotalOuterSolarIrradiance, totalSolarRadiationToOPV]).T,
# 											 "hourlyMeasuredSolarRadiationToHorizontalAndTilted")
# 		###################data export end##################
#
# 		# unit change: [W m^-2] -> [umol m^-2 s^-1] == PPFD
# 		directPPFDToOPVEastDirection = util.convertFromWattperSecSquareMeterToPPFD(directSolarRadiationToOPVEastDirection)
# 		directPPFDToOPVWestDirection = util.convertFromWattperSecSquareMeterToPPFD(directSolarRadiationToOPVWestDirection)
# 		diffusePPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(diffuseSolarRadiationToOPV)
# 		groundReflectedPPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(albedoSolarRadiationToOPV)
# 		# print"diffusePPFDToOPV.shape:{}".format(diffusePPFDToOPV.shape)
#
# 		# set the matrix to the object
# 		simulatorClass.setDirectPPFDToOPVEastDirection(directPPFDToOPVEastDirection)
# 		simulatorClass.setDirectPPFDToOPVWestDirection(directPPFDToOPVWestDirection)
# 		simulatorClass.setDiffusePPFDToOPV(diffusePPFDToOPV)
# 		simulatorClass.setGroundReflectedPPFDToOPV(groundReflectedPPFDToOPV)
#
# 		# unit change: hourly [umol m^-2 s^-1] -> [mol m^-2 day^-1] == daily light integral (DLI) :number of photons received in a square meter per day
# 		directDLIToOPVEastDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVEastDirection)
# 		directDLIToOPVWestDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVWestDirection)
# 		diffuseDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(diffusePPFDToOPV)
# 		groundReflectedDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(groundReflectedPPFDToOPV)
# 		totalDLIToOPV = (directDLIToOPVEastDirection + directDLIToOPVWestDirection) / 2.0 + diffuseDLIToOPV + groundReflectedDLIToOPV
# 		# print "directDLIToOPVEastDirection:{}".format(directDLIToOPVEastDirection)
# 		# print "diffuseDLIToOPV.shape:{}".format(diffuseDLIToOPV.shape)
# 		# print "groundReflectedDLIToOPV:{}".format(groundReflectedDLIToOPV)
#
# 		# set the array to the object
# 		simulatorClass.setDirectDLIToOPVEastDirection(directDLIToOPVEastDirection)
# 		simulatorClass.setDirectDLIToOPVWestDirection(directDLIToOPVWestDirection)
# 		simulatorClass.setDiffuseDLIToOPV(diffuseDLIToOPV)
# 		simulatorClass.setGroundReflectedDLIToOPV(groundReflectedDLIToOPV)
#
# 	########################################################################################################################
# 	################# calculate solar irradiance without real data (estimate solar irradiance) start #######################
# 	########################################################################################################################
# 	elif constant.ifUseOnlyRealData == False:
#
# 		# activate the mode to use the formulas for estimation. This is used for branching the solar irradiance to PV module. See OPVFilm.py
# 		simulatorClass.setEstimateSolarRadiationMode(True)
#
# 		# calculate the solar radiation to the OPV film
# 		# [W m^-2] per hour
# 		estimatedDirectSolarRadiationToOPVEastDirection, \
# 		estimatedDirectSolarRadiationToOPVWestDirection, \
# 		estimatedDiffuseSolarRadiationToOPV, \
# 		estimatedAlbedoSolarRadiationToOPV = simulatorDetail.calcOPVmoduleSolarIrradianceGHRoof(simulatorClass)
# 		estimatedTotalSolarRadiationToOPV = (
# 																				estimatedDirectSolarRadiationToOPVEastDirection + estimatedDirectSolarRadiationToOPVWestDirection) / 2.0 + estimatedDiffuseSolarRadiationToOPV + estimatedAlbedoSolarRadiationToOPV
#
# 		# set the calc results
# 		# [W m^-2] per hour
# 		simulatorClass.setDirectSolarRadiationToOPVEastDirection(estimatedDirectSolarRadiationToOPVEastDirection)
# 		simulatorClass.setDirectSolarRadiationToOPVWestDirection(estimatedDirectSolarRadiationToOPVWestDirection)
# 		simulatorClass.setDiffuseSolarRadiationToOPV(estimatedDiffuseSolarRadiationToOPV)
# 		simulatorClass.setAlbedoSolarRadiationToOPV(estimatedAlbedoSolarRadiationToOPV)
#
# 		# [estimated data] unit change:
# 		estimatedDirectPPFDToOPVEastDirection = util.convertFromWattperSecSquareMeterToPPFD(estimatedDirectSolarRadiationToOPVEastDirection)
# 		estimatedDirectPPFDToOPVWestDirection = util.convertFromWattperSecSquareMeterToPPFD(estimatedDirectSolarRadiationToOPVWestDirection)
# 		estimatedDiffusePPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(estimatedDiffuseSolarRadiationToOPV)
# 		estimatedGroundReflectedPPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(estimatedAlbedoSolarRadiationToOPV)
# 		# print("estimatedDirectPPFDToOPVEastDirection:{}".format(estimatedDirectPPFDToOPVEastDirection))
# 		# print("estimatedDirectPPFDToOPVWestDirection:{}".format(estimatedDirectPPFDToOPVWestDirection))
#
# 		# set the variables
# 		simulatorClass.setDirectPPFDToOPVEastDirection(estimatedDirectPPFDToOPVEastDirection)
# 		simulatorClass.setDirectPPFDToOPVWestDirection(estimatedDirectPPFDToOPVWestDirection)
# 		simulatorClass.setDiffusePPFDToOPV(estimatedDiffusePPFDToOPV)
# 		simulatorClass.setGroundReflectedPPFDToOPV(estimatedGroundReflectedPPFDToOPV)
#
# 		# [estimated data] unit change:
# 		estimatedDirectDLIToOPVEastDirection = util.convertFromHourlyPPFDWholeDayToDLI(estimatedDirectPPFDToOPVEastDirection)
# 		estimatedDirectDLIToOPVWestDirection = util.convertFromHourlyPPFDWholeDayToDLI(estimatedDirectPPFDToOPVWestDirection)
# 		estimatedDiffuseDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(estimatedDiffusePPFDToOPV)
# 		estimatedGroundReflectedDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(estimatedGroundReflectedPPFDToOPV)
# 		# estimatedTotalDLIToOPV = (estimatedDirectDLIToOPVEastDirection + estimatedDirectDLIToOPVWestDirection) / 2.0 + estimatedDiffuseDLIToOPV + estimatedGroundReflectedDLIToOPV
# 		# set the variables
# 		simulatorClass.setDirectDLIToOPVEastDirection(estimatedDirectDLIToOPVEastDirection)
# 		simulatorClass.setDirectDLIToOPVWestDirection(estimatedDirectDLIToOPVWestDirection)
# 		simulatorClass.setDiffuseDLIToOPV(estimatedDiffuseDLIToOPV)
# 		simulatorClass.setGroundReflectedDLIToOPV(estimatedGroundReflectedDLIToOPV)
#
# 		# deactivate the mode to the default value.
# 		simulatorClass.setEstimateSolarRadiationMode(False)
#
# 		# data export of solar irradiance
# 		util.exportCSVFile(np.array([year, month, day, hour,
# 																 simulatorClass.getDirectSolarRadiationToOPVEastDirection(),
# 																 simulatorClass.getDirectSolarRadiationToOPVWestDirection(),
# 																 simulatorClass.getDiffuseSolarRadiationToOPV(),
# 																 simulatorClass.getAlbedoSolarRadiationToOPV(),
# 																 estimatedTotalSolarRadiationToOPV]).T,
# 											 "SolarIrradianceToHorizontalSurface")
# 		################# calculate solar irradiance without real data (estimate the data) end #######################
#
#
# 	###############################################################################################
# 	###################calculate the solar irradiance through multi span roof start################
# 	###############################################################################################
# 	# The calculated irradiance is stored to the object in this function
# 	simulatorDetail.getDirectSolarIrradianceThroughMultiSpanRoof(simulatorClass)
# 	# data export
# 	util.exportCSVFile(
# 		np.array([year, month, day, hour, simulatorClass.integratedT_mat, simulatorClass.getHourlyDirectSolarRadiationAfterMultiSpanRoof(), ]).T,
# 		"directSolarRadiationAfterMultiSpanRoof")
# 	###########################################################################################
# 	###################calculate the solar irradiance through multi span roof end##############
# 	###########################################################################################
#
# 	###########################################################################################
# 	###################calculate the solar irradiance to plants start##########################
# 	###########################################################################################
# 	# get/set cultivation days per harvest [days/harvest]
# 	cultivationDaysperHarvest = constant.cultivationDaysperHarvest
# 	simulatorClass.setCultivationDaysperHarvest(cultivationDaysperHarvest)
#
# 	# get/set OPV coverage ratio [-]
# 	OPVCoverage = constant.OPVAreaCoverageRatio
# 	simulatorClass.setOPVAreaCoverageRatio(OPVCoverage)
#
# 	# get/set OPV coverage ratio during fallow period[-]
# 	OPVCoverageSummerPeriod = constant.OPVAreaCoverageRatioSummerPeriod
# 	simulatorClass.setOPVCoverageRatioSummerPeriod(OPVCoverageSummerPeriod)
#
# 	# get if we assume to have shading curtain
# 	hasShadingCurtain = constant.hasShadingCurtain
# 	simulatorClass.setIfHasShadingCurtain(hasShadingCurtain)
#
# 	# get the direct solar irradiance after penetrating multi span roof [W/m^2]
# 	hourlyDirectSolarRadiationAfterMultiSpanRoof = simulatorClass.getHourlyDirectSolarRadiationAfterMultiSpanRoof()
#
# 	# OPVAreaCoverageRatio = simulatorClass.getOPVAreaCoverageRatio()
# 	OPVAreaCoverageRatio = constant.OPVAreaCoverageRatio
# 	hasShadingCurtain = simulatorClass.getIfHasShadingCurtain()
# 	# ShadingCurtainDeployPPFD = simulatorClass.getShadingCurtainDeployPPFD()
# 	OPVPARTransmittance = constant.OPVPARTransmittance
#
#
# 	# make the list of OPV coverage ratio at each hour changing during summer
# 	OPVAreaCoverageRatioChangingInSummer = OPVFilm.getDifferentOPVCoverageRatioInSummerPeriod(OPVAreaCoverageRatio, simulatorClass)
#
# 	# ############command to print out all array data
# 	# np.set_printoptions(threshold=np.inf)
# 	# print("OPVAreaCoverageRatioChangingInSummer:{}".format(OPVAreaCoverageRatioChangingInSummer))
# 	# np.set_printoptions(threshold=1000)
# 	# ############
#
# 	# consider the transmission ratio of OPV film
# 	hourlyDirectSolarRadiationAfterOPVAndRoof = hourlyDirectSolarRadiationAfterMultiSpanRoof * (1 - OPVAreaCoverageRatioChangingInSummer) \
# 																							+ hourlyDirectSolarRadiationAfterMultiSpanRoof * OPVAreaCoverageRatioChangingInSummer * OPVPARTransmittance
# 	# print "OPVAreaCoverageRatio:{}, HourlyInnerLightIntensityPPFDThroughOPV:{}".format(OPVAreaCoverageRatio, HourlyInnerLightIntensityPPFDThroughOPV)
#
# 	# consider the light reduction by greenhouse inner structures and equipments like pipes, poles and gutters
# 	hourlyDirectSolarRadiationAfterInnerStructure = (1 - constant.GreenhouseShadeProportionByInnerStructures) * hourlyDirectSolarRadiationAfterOPVAndRoof
#
#
# 	transmittanceThroughShadingCurtainChangingEachMonth = getHourlyShadingCurtainDeploymentPatternChangingEachMonthMain(simulatorClass, hourlyDirectSolarRadiationAfterInnerStructure)
#
# 	return transmittanceThroughShadingCurtainChangingEachMonth

# def getHourlyShadingCurtainDeploymentPatternChangingEachMonthMain(simulatorClass, hourlyDirectSolarRadiationAfterInnerStructure):
def getHourlyShadingCurtainDeploymentPatternChangingEachMonthMain(simulatorClass):
	'''
	calculate the shading curtain deployement pattern which changes each month.
	The deployment is judges by comparing the average DLI and the optimal DLI that is defined at CropElectricityYeildSimulatorConstant

	'''

	directSolarIrradianceBeforeShadingCurtain = simulatorClass.directSolarIrradianceBeforeShadingCurtain
	diffuseSolarIrradianceBeforeShadingCurtain = simulatorClass.diffuseSolarIrradianceBeforeShadingCurtain

	totalSolarIrradianceBeforeShadingCurtain = directSolarIrradianceBeforeShadingCurtain + diffuseSolarIrradianceBeforeShadingCurtain
	# print("totalSolarIrradianceBeforeShadingCurtain:{}".format(totalSolarIrradianceBeforeShadingCurtain))

	################### calc shading deployment pattern start ###########################
	if constant.IsShadingCurtainDeployOnlyDayTime == True and constant.IsDifferentShadingCurtainDeployTimeEachMonth == True:

		# 1 = no shading curatin, the transmittance of shading curtain = deploey curtain
		transmittanceThroughShadingCurtainChangingEachMonth = np.zeros(len(totalSolarIrradianceBeforeShadingCurtain))

		#############
		# 1: deploy shading curtain, 0 = not deploy
		shadingHours = {
			# "0":      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			# ,"12":    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			# ,"12-13": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			# , "11-13":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			# , "11-14":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			# , "10-14":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			# , "10-15":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
			# , "9-15": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
			# , "9-16": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
			# , "8-16": [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
			# , "8-17": [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
			# , "7-17": [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
			# , "7-18": [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
			# , "6-18": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
			# , "6-19": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
			# , "5-19": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
			# , "5-20": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
			# , "4-20": [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
			# , "4-21": [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
			# , "3-21": [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
			# , "3-22": [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
			# , "2-22": [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
			# , "2-23": [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
			# , "1-23": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
			# , "0-23": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
			0:    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			, 1:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			, 2:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			, 3:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			, 4:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			, 5:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			, 6:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
			, 7:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
			, 8:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
			, 9:  [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
			, 10: [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
			, 11: [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
			, 12: [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
			, 13: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
			, 14: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
			, 15: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
			, 16: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
			, 17: [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
			, 18: [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
			, 19: [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
			, 20: [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
			, 21: [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
			, 22: [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
			, 23: [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
			, 24: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		}
		# print("len(shadingHours):{}".format(len(shadingHours)))

		##############set the initial values start##############
		# get the num of simulation months, rounding up.
		# e.g. when the simulation period is 1st Jan to 15th Jan, it is 1.
		# e.g. when the simulation period is 1st 16th Nov to 1st Dec, it is 2.
		# simulationMonths = util.getSimulationMonthsInt()

		# unit: hour
		simulationHours = util.getSimulationDaysInt() * constant.hourperDay
		# print("simulationHours:{}".format(simulationHours))

		currnetDate = util.getStartDateDateType()
		currentYear = util.getStartDateDateType().year
		currentMonth = util.getStartDateDateType().month
		currentDay = util.getStartDateDateType().day

		# SimulatedMonths = 1
		hour = 0
		##############set the initial values end##############

		# take date and time
		year = simulatorClass.getYear()
		month = simulatorClass.getMonth()
		day = simulatorClass.getDay()
		hour = simulatorClass.getHour()

		# total sollar irradiance per day which does not cause tipburn. unit conversion: DLI(mol m-2 day) -> W m-2
		# totalSolarIrradiancePerDayNoTipburn = constant.DLIforTipBurn * 1000000.0 / constant.minuteperHour / constant.secondperMinute / constant.wattToPPFDConversionRatio

		# loop each hour
		hour = 0
		while hour < simulationHours:
			# print("hour:{}".format(hour))

			# get the number of days each month
			_, currentMonthDays = calendar.monthrange(currnetDate.year, currnetDate.month)
			# print("currentMonthDays:{}".format(currentMonthDays))

			daysOfEachMonth = (datetime.date(currentYear, currentMonth, currentMonthDays) - currnetDate).days + 1
			# print("daysOfEachMonth:{}".format(daysOfEachMonth))

			# loop for each shading curtain deployment pattern
			for i in range(0, len(shadingHours)):

				# if shading curtain: constant.shadingTransmittanceRatio, if no shading: 1.0 transmittance
				TransmittanceThroughShadingCurtain = np.array([constant.shadingTransmittanceRatio if j == 1 else 1.0 for j in shadingHours[i]])
				# print("TransmittanceThroughShadingCurtain:{}".format(TransmittanceThroughShadingCurtain))

				# extend the shading curatin pattern for whole month
				transmittanceThroughShadingCurtainWholeMonth   = []
				[transmittanceThroughShadingCurtainWholeMonth   .extend(TransmittanceThroughShadingCurtain) for k in range(0, daysOfEachMonth)]
				# print("len(transmittanceThroughShadingCurtainWholeMonth   ):{}".format(len(transmittanceThroughShadingCurtainWholeMonth   )))

				# get the solar irradiance throught shading curtain
				hourlyDirectSolarRadiationAfterShadingCurtain = totalSolarIrradianceBeforeShadingCurtain[hour : hour + daysOfEachMonth * constant.hourperDay] * transmittanceThroughShadingCurtainWholeMonth
				# print("hourlyDirectSolarRadiationAfterShadingCurtain:{}".format(hourlyDirectSolarRadiationAfterShadingCurtain))
				# print("len(hourlyDirectSolarRadiationAfterShadingCurtain):{}".format(len(hourlyDirectSolarRadiationAfterShadingCurtain)))
				# print("sum(hourlyDirectSolarRadiationAfterShadingCurtain):{}".format(sum(hourlyDirectSolarRadiationAfterShadingCurtain)))

				# convert the unit from W m-2 to DLI (mol m-2 day-1)
				DLIAfterShadingCurtain = sum(hourlyDirectSolarRadiationAfterShadingCurtain) / daysOfEachMonth * constant.wattToPPFDConversionRatio * constant.secondperMinute * constant.minuteperHour / 1000000.0
				# print("DLIAfterShadingCurtain:{}".format(DLIAfterShadingCurtain))

				# print("i:{}".format(i))
				# if the average DLI is less than the optimal DLI
				if DLIAfterShadingCurtain <= constant.DLIforTipBurn:
					# store the transmittance which shading curatin deployed
					transmittanceThroughShadingCurtainChangingEachMonth[hour : hour + daysOfEachMonth * constant.hourperDay] = transmittanceThroughShadingCurtainWholeMonth
					# increment hour
					hour += daysOfEachMonth * constant.hourperDay
					# variable update
					# print("before currnetDate:{}".format(currnetDate))
					currnetDate = currnetDate + datetime.timedelta(days = daysOfEachMonth)
					# print("after currnetDate:{}".format(currnetDate))
					currentYear = currnetDate.year
					currentMonth = currnetDate.month

					# move to the next month. break the for loop
					break

				# if the average solar irradiance does not become below the optimal DLI, then store the solar irradiance for shadingHours[24]
				elif i == 24:
					# store the transmittance which shading curatin deployed
					transmittanceThroughShadingCurtainChangingEachMonth[hour : hour + daysOfEachMonth * constant.hourperDay] = transmittanceThroughShadingCurtainWholeMonth
					# increment hour
					hour += daysOfEachMonth * constant.hourperDay
					# variable update
					# print("before currnetDate:{}".format(currnetDate))
					currnetDate = currnetDate + datetime.timedelta(days = daysOfEachMonth)
					# print("after currnetDate:{}".format(currnetDate))
					currentYear = currnetDate.year
					currentMonth = currnetDate.month

					# move to the next month. break the for loop
					break

		# store the data
		simulatorClass.transmittanceThroughShadingCurtainChangingEachMonth = transmittanceThroughShadingCurtainChangingEachMonth

		return transmittanceThroughShadingCurtainChangingEachMonth

	else:
		print("error: please let constant.IsShadingCurtainDeployOnlyDayTime == True and constant.IsDifferentShadingCurtainDeployTimeEachMonth == True")
		####################################################################################################
		# Stop execution here...
		sys.exit()
		# Move the above line to different parts of the assignment as you implement more of the functionality.
		####################################################################################################


# print "hourlyInnerLightIntensityPPFDThroughInnerStructure:{}".format(hourlyInnerLightIntensityPPFDThroughInnerStructure)



# if __name__ == '__main__':
# 	transmittanceThroughShadingCurtainChangingEachMonth = getHourlyShadingCurtainDeploymentPatternChangingEachMonthPrep()
# 	print("transmittanceThroughShadingCurtainChangingEachMonth:{}".format(transmittanceThroughShadingCurtainChangingEachMonth))
#
# 	# export the data



