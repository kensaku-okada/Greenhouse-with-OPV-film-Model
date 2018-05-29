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
import Lettuce
import CropElectricityYeildSimulatorConstant as constant
import GreenhouseEnergyBalanceConstant as energyBalanceConstant
import Util
from dateutil.relativedelta import *
from time import strptime
#######################################################

def getGHEnergyConsumptionByCoolingHeating(simulatorClass):
	'''
	all of the energy data calculated in this function is the average energy during each hour, not the total energy during eah hour.

	reference:
		1
		Unknown author, Greenhouse Steady State Energy Balance Model
		https://fac.ksu.edu.sa/sites/default/files/lmhdr_lthlth_wlrb.pdf
		or
		http://ecoursesonline.iasri.res.in/mod/page/view.php?id=1635
		accessed on May 18 2018
		2
		Idso, S. B. 1981.  A set of equations for full spectrum and 8-µm to 14-µm and 10.5-µm to
		12.5-µm thermal radiation from cloudless skies. Water Resources Research, 17: 295-
		304.

	'''

	# get the necessary data
	# unit: W m-2
	directSolarIrradianceToPlants = simulatorClass.directSolarIrradianceToPlants
	# unit: W m-2
	diffuseSolarIrradianceToPlants = simulatorClass.diffuseSolarIrradianceToPlants
	# unit: Celsius degree
	hourlyAirTemperatureOutside = simulatorClass.getImportedHourlyAirTemperature()
	# unit: -
	relativeHumidityOutside = simulatorClass.hourlyRelativeHumidity

	# the amount of direct and diffuse shortwave solar radiation in the greenhouse [W m-2]
	################# get Q_sr start ################
	'''
	in the reference papre, the formula is,
	Q_sr = tau_c * S_l * I_sr * A_f
	where tau_c is transmissivity of the greenhouse covering materials for solar radiation,
	S_l is shading level, and I_sr is the amount of solar radiation energy received per unit are and per unit time on a horizontal surface outside the greenhouse [W m2]. 
	However, since tau_c * S_l * I_sr is already calculated as the sum of directSolarIrradianceToPlants and diffuseSolarIrradianceToPlants, I arranged the formula as below.
	'''
	# unit: W m-2
	totalSolarIrradianceToPlants = directSolarIrradianceToPlants + diffuseSolarIrradianceToPlants

	Q_sr = totalSolarIrradianceToPlants
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("Q_sr:{}".format(Q_sr))
	# np.set_printoptions(threshold=1000)
	# ############
	################# get Q_sr end ################

	# latent heat energy flux due to plant transpiration [W m-2]
	################# get Q_lh (Q_e) start ################
	# '''
	# todo delete this comment if not necessary
	# # rate of transpiration [Kg_H2O sec-1 m-2]
	# # according to Ricardo Aroca et al. (2008). Mycorrhizal and non-mycorrhizal Lactuca sativa plants exhibit contrasting responses to exogenous ABA during drought stress and recovery
	# this value was around 6.6 [mg_H2O hour-1 cm-2]. This should be converted as below.
	# '''
	# ET = 6.6 / 1000.0 / (constant.secondperMinute * constant.minuteperHour) * 10000.0

	Q_lh = getLatentHeatTransferByTranspiration(simulatorClass, totalSolarIrradianceToPlants)
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("Q_lh:{}".format(Q_lh))
	# np.set_printoptions(threshold=1000)
	# ############
	################# get Q_lh (Q_e) end ################

	# sensible heat from conduction and convection through the greenhouse covering material [W m-2]
	################# get Q_sh (Q_cd in reference 1) start ################
	# # the area of greenhouse covers [m2]
	# A_c = constant.greenhouseTotalRoofArea

	# inside (set point) air temperature [Celsius degree]
	T_iC = Lettuce.getGreenhouseTemperatureEachHour(simulatorClass)
	# inside air temperature [K]
	T_iK = T_iC + 273.0

	# outside air temperature [C]
	T_oC = hourlyAirTemperatureOutside
	# outside air temperature [K]
	T_oK = hourlyAirTemperatureOutside + 273.0

	Q_sh = energyBalanceConstant.U * (T_iC - T_oC)
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("Q_sh:{}".format(Q_sh))
	# np.set_printoptions(threshold=1000)
	# ############
	################# get Q_sh (Q_cd in reference 1) end ################

	# net thermal radiation through the greenhouse covers to the atmosphere [W m-2], the difference between the thermal radiation emitted from the surface and the thermal radiation gained from the atmosphere
	################# get Q_lw (Q_t in reference 1) start ################
	# ambient vapor pressure outside [Pa]
	# source:　https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf
	_, e_a = getSturatedAndActualVaporPressure(T_oC, relativeHumidityOutside)
	# print("e_a.shape:{}".format(e_a.shape))

	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("e_a:{}".format(e_a))
	# np.set_printoptions(threshold=1000)
	# ############

	# apparent emissivity of the sky (Idso, 1981)
	# source: reference 2
	epsilon_sky = 0.7 - 5.95 * 10.0**(-7) * e_a * math.e**(1500.0 / T_oK)
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("epsilon_sky.shape:{}, epsilon_sky:{}".format(epsilon_sky.shape, epsilon_sky))
	# np.set_printoptions(threshold=1000)
	# ############

	# transmissivity of the shading shading curtain
	tau_os = constant.shadingTransmittanceRatio

	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("T_o:{}".format(T_o))
	# np.set_printoptions(threshold=1000)
	# ############
	# the sky temperature (the  Swinbank  model  (1963) ) [K]
	T_sky = 0.0522 * T_oK**1.5
	# print("T_sky.shape:{}".format(T_sky.shape))

	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("T_sky:{}".format(T_sky))
	# np.set_printoptions(threshold=1000)
	# ############

	Q_lw = energyBalanceConstant.delta * energyBalanceConstant.tau_tc * tau_os * \
				(energyBalanceConstant.epsilon_i * T_iK**4.0 - epsilon_sky * T_sky**4.0)

	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("Q_lw.shape:{}, Q_lw:{}".format(Q_lw.shape, Q_lw))
	# np.set_printoptions(threshold=1000)
	# ############
	################# get Q_lw (Q_t in reference 1) end ################

	# energy removed by ventilation air or added by heating[W m-2]
	################# get Q_v start ################
	# if positive, cooling. if negative, heating
	Q_v = getQ_v(simulatorClass, Q_sr, Q_lh, Q_sh, Q_lw)
	# Q_v = Q_sr - Q_lh - Q_sh - Q_lw
	# print("Q_v.shape:{}".format(Q_v.shape))
	################# get Q_v end ################

	# # this energy is used for heating. So sum only the minus value of Q_v
	# totalFuelEnergyConsumptionForPlants =
	# # this energy is used for cooling with pad and fan systems. So sum only the positive value of Q_v
	# totalElectricityConsumptionForPlants =
	# return totalFuelEnergyConsumptionForPlants, totalElectricityConsumptionForPlants

	# set the data to the object. all units are W m-2
	simulatorClass.Q_v["coolingOrHeatingEnergy W m-2"] = Q_v
	simulatorClass.Q_sr["solarIrradianceToPlants W m-2"] = Q_sr
	simulatorClass.Q_lh["latentHeatByTranspiration W m-2"] = Q_lh
	simulatorClass.Q_sh["sensibleHeatFromConductionAndConvection W m-2"] = Q_sh
	simulatorClass.Q_lw["longWaveRadiation W m-2"] = Q_lw
	# print("Q_sr.shape:{}".format(Q_sr.shape))
	# print("Q_lh.shape:{}".format(Q_lh.shape))
	# print("Q_sh.shape:{}".format(Q_sh.shape))
	# print("Q_lw.shape:{}".format(Q_lw.shape))

	# return Q_v


def getLatentHeatTransferByTranspiration(simulatorClass, totalSolarIrradianceToPlants):
	'''
	reference:
	1
	Pollet, S. and Bleyaert, P. 2000.
	APPLICATION OF THE PENMAN-MONTEITH MODEL TO CALCULATE THE EVAPOTRANSPIRATION OF HEAD LETTUCE (Lactuca sativa L. var.capitata) IN GLASSHOUSE CONDITIONS
	https://www.actahort.org/books/519/519_15.htm
	2
	Andriolo, J.L., da Luz, G.L., Witter, M.H., Godoi, R.S., Barros, G.T., Bortolotto, O.C.
	(2005). Growth and yield of lettuce plant under salinity. Horticulture Brasileira,
	23(4), 931-934.

	'''

	# greenhouse air temperature [Celsius degree]
	T_a = simulatorClass.getImportedHourlyAirTemperature()

	hourlyDayOrNightFlag = simulatorClass.hourlyDayOrNightFlag
	relativeHumidityInGH = np.array([constant.setPointHumidityDayTime if i == constant.daytime else constant.setPointHumidityNightTime for i in hourlyDayOrNightFlag])

	# leaf temperature [Celsius degree]. It was assumed that the difference between the leaf temperature and the air temperature was always 2. This is just an assumption of unofficial experiment at Kacira Lab at CEAC in University of Arizona
	T_l = T_a + 2.0
	# dimention of leaf [m]. This is just an assumption of unofficial experiment at Kacira Lab at CEAC in University of Arizona
	d = 0.14

	# arerodynamic resistance of the leaf [s m-1]
	# source: reference No 1, Pollet et al. 2000
	r_a = 840.0 * (d/abs(T_l - T_a))**(1.0/4.0)
	# print("r_a:{}".format(r_a))

	# the leaf area index [-]
	# source: reference No 2, Andriolo et al. 2005
	L = 4.3

	# arerodynamic resistance of the crop [s m-1]
	# source: reference No 1, Pollet et al. 2000
	r_b = r_a /(2.0 * L)
	# print("r_b:{}".format(r_b))


	# short wave radiation [W m-2]
	# Need to figure out why dividing the solar irradiance inside by 0.844. see the differnce. -> This is probably because the suthor considered some light prevention by internal equipment. Considering the definition, it should be same as the soalr irradiance to plants
	# I_s = 0.844 * totalSolarIrradianceToPlants
	I_s = totalSolarIrradianceToPlants

	############### calc the vapor pressure deficit start ###############
	# saturated vapore pressure [Pa]
	# source: http://cronklab.wikidot.com/calculation-of-vapour-pressure-deficit
	# source: https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf
	e_s, e_a = getSturatedAndActualVaporPressure(T_a, relativeHumidityInGH)
	# vapor pressure deficit [Pa]
	D = e_s - e_a
	############### calc the vapor pressure deficit end ###############

	# the stomatal resistance [sec m-1]
	# source: reference No 1, Pollet et al. 2000
	r_s = 164.0*(31.029+I_s)/(6.740+I_s) * (1 + 0.011*(D - 3.0)**2) * (1 + 0.016*(T_a - 16.4)**2)

	# crop resistance　[sec m-1]
	# source: reference No 1, Pollet et al. 2000
	r_c = r_s / L

	################## calc psychrometric constant start ##################
	print("energyBalanceConstant.c_p / (energyBalanceConstant.epsilon * energyBalanceConstant.lambda_:{}".format(energyBalanceConstant.c_p / (energyBalanceConstant.epsilon * energyBalanceConstant.lambda_)))
	print("energyBalanceConstant.P:{}".format(energyBalanceConstant.P))
	# psychrometric constant
	# source: http://www.fao.org/docrep/X0490E/x0490e07.htm
	gamma = energyBalanceConstant.c_p * energyBalanceConstant.P / (energyBalanceConstant.epsilon * energyBalanceConstant.lambda_)
	# gamma = 0.665 * 10**(-3) * energyBalanceConstant.P
	# print("gamma:{}".format(gamma))

	gamma_star = gamma * (1 + r_c / r_b)
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("gamma_star:{}".format(gamma_star))
	# np.set_printoptions(threshold=1000)
	# ############

	################## calc psychrometric constant end ##################

	# slope of saturation vapore pressure - temperature curve [kPa C-1]
	# source: http://www.fao.org/docrep/X0490E/x0490e0k.htm
	# source: http://edis.ifas.ufl.edu/pdffiles/ae/ae45900.pdf
	s = 4098.0 * 610.8 * math.e**((17.27*T_a)/(T_a + 273.3)) / ((T_a + 273.3)**2.0)
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("s:{}".format(s))
	# np.set_printoptions(threshold=1000)
	# ############

	# net radiation at the crop surface == above the canopy [W m-2]
	R_n = totalSolarIrradianceToPlants

	# The Penman-Monteith equation
	Q_e = s * (R_n - energyBalanceConstant.F) / (s + gamma_star) + (energyBalanceConstant.rho * energyBalanceConstant.C_p * D / r_b) / (s + gamma_star)

	return Q_e


def getSturatedAndActualVaporPressure(actualT, relativeHumidity):
	e_s = 610.7 * 10.0**((7.5 * actualT)/(237.3+actualT))
	e_a = e_s * relativeHumidity
	return e_s, e_a


def getQ_v(simulatorClass, Q_sr, Q_lh, Q_sh, Q_lw):
	'''
	consider the greenhouse size (floor area, roofa are, wall area), calc Q_v
	'''

	# unit: W
	Q_srW = Q_sr * constant.greenhouseFloorArea
	# unit: W
	Q_lhW = Q_lh * constant.greenhouseCultivationFloorArea
	# unit: W
	Q_shW = Q_sh * (constant.greenhouseTotalRoofArea + constant.greenhouseSideWallArea)
	# unit: W
	# it was assumed the greenhouse ceiling area (not the roof area because it would be strange that we get more long wave radiation as the angle of the roof increases) was same as the floor area.
	Q_lwW = Q_lw * constant.greenhouseFloorArea

	# unit: W
	Q_vW = Q_srW - (Q_lhW + Q_shW + Q_lwW)

	simulatorClass.Q_vW["coolingOrHeatingEnergy W"] = Q_vW
	simulatorClass.Q_srW["solarIrradianceToPlants W"] = Q_srW
	simulatorClass.Q_lhW["sensibleHeatFromConductionAndConvection W"] = Q_lhW
	simulatorClass.Q_shW["latentHeatByTranspiration W"] = Q_shW
	simulatorClass.Q_lwW["longWaveRadiation W"] = Q_lwW

	# unit: W m-2
	return Q_vW / constant.greenhouseFloorArea


def getGHHeatingEnergyCostForPlants(requiredHeatingEnergyForPlants, simulatorClass):
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("requiredHeatingEnergyForPlants:{}".format(requiredHeatingEnergyForPlants))
	# np.set_printoptions(threshold=1000)
	# ############

	# unit: W
	requiredHeatingEnergyConsumptionForPlants = {"W": requiredHeatingEnergyForPlants / constant.heatingEquipmentEfficiency}
	# unit conversion: W (= J sec-1) -> MJ
	requiredHeatingEnergyConsumptionForPlants["MJ"] = requiredHeatingEnergyConsumptionForPlants["W"] * constant.secondperMinute * constant.minuteperHour / 1000000.0
	# unit conversion: MJ -> ft3
	requiredHeatingEnergyConsumptionForPlants["ft3"] = requiredHeatingEnergyConsumptionForPlants["MJ"] / constant.naturalGasSpecificEnergy["MJ ft-3"]
	print("requiredHeatingEnergyConsumptionForPlants:{}".format(requiredHeatingEnergyConsumptionForPlants))

	# get the price of natural gas
	fileName = constant.ArizonaPriceOfNaturalGasDeliveredToResidentialConsumers
	# import the file removing the header
	fileData = Util.readData(fileName, relativePath="", skip_header=5, d=',')
	# print ("fileData.shape:{}".format(fileData.shape))

	# reverse the file data becasue the data starts from the newest date. requiredHeatingEnergyForPlants starts from the old time.
	fileData = fileData[::-1]
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print ("fileData:{}".format(fileData))
	# np.set_printoptions(threshold=1000)
	# ############

	# unit ft3 month-1
	monthlyRequiredGHHeatingEnergyForPlants = getMonthlyRequiredGHHeatingEnergyForPlants(requiredHeatingEnergyConsumptionForPlants["ft3"], simulatorClass)
	# set the data to the object
	simulatorClass.monthlyRequiredGHHeatingEnergyForPlants = monthlyRequiredGHHeatingEnergyForPlants

	monthlyHeatingCostForPlants = np.zeros(monthlyRequiredGHHeatingEnergyForPlants.shape[0])

	index = 0
	for fileDataLine in fileData:

		# split first column into month and year
		month = strptime(fileDataLine[0].split()[0],'%b').tm_mon
		# print("month:{}".format(month))
		year = fileDataLine[0].split()[1]

		# unit: USD thousand ft-3
		monthlyNaturalGasPrice = float(fileDataLine[1])
		# print("monthlyNaturalGasPrice:{}".format(monthlyNaturalGasPrice))

		# exclude the data out of the set start month and end month
		if datetime.date(int(year), int(month), 1) + relativedelta(months=1) <= Util.getStartDateDateType() or \
						datetime.date(int(year), int(month), 1) > Util.getEndDateDateType():
		# if datetime.date(int(year[i]), int(month[i]), 1) + relativedelta(months=1) <= Util.getStartDateDateType() or \
		# 				datetime.date(int(year[i]), int(month[i]), 1) > Util.getEndDateDateType():
				continue

		monthlyHeatingCostForPlants[index] = (monthlyNaturalGasPrice / 1000.0) * monthlyRequiredGHHeatingEnergyForPlants[index]
		# print "monthlyData:{}".format(monthlyData)
		index += 1

	print("monthlyHeatingCostForPlants:{}".format(monthlyHeatingCostForPlants))

	totalHeatingCostForPlants = sum(monthlyHeatingCostForPlants)

	return totalHeatingCostForPlants


def getMonthlyRequiredGHHeatingEnergyForPlants(requiredHeatingEnergyConsumptionForPlants, simulatorClass):

	month = simulatorClass.getMonth()

	numOfMonths = Util.getSimulationMonthsInt()
	monthlyRequiredGHHeatingEnergyForPlants = np.zeros(numOfMonths)
	monthIndex = 0
	# insert the initial value
	monthlyRequiredGHHeatingEnergyForPlants[0] = requiredHeatingEnergyConsumptionForPlants[0]
	for i in range(1, month.shape[0]):

		monthlyRequiredGHHeatingEnergyForPlants[monthIndex] += requiredHeatingEnergyConsumptionForPlants[i]
		if month[i - 1] != month[i]:
			# move onto the next month
			monthIndex += 1

	return monthlyRequiredGHHeatingEnergyForPlants


def getGHCoolingEnergyCostByCooling(requiredCoolingEnergyForPlants, simulatorClass):
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("requiredCoolingEnergyForPlants:{}".format(requiredCoolingEnergyForPlants))
	# np.set_printoptions(threshold=1000)
	# ############

	# unit: W
	requiredCoolingEnergyConsumptionForPlants = {"W": requiredCoolingEnergyForPlants / constant.PadAndFanCOP}

	# unit conversion W -> kWh
	requiredCoolingEnergyConsumptionForPlants["kWh"] = requiredCoolingEnergyConsumptionForPlants["W"] / 1000.0
	# ############command to print out all array data
	# np.set_printoptions(threshold=np.inf)
	# print("requiredCoolingEnergyConsumptionForPlants[\"kWh\"]:{}".format(requiredCoolingEnergyConsumptionForPlants["kWh"]))
	# np.set_printoptions(threshold=1000)
	# ############

	# get the imported electricity retail price
	# unit: cent kWh-1
	monthlyElectricityRetailPrice = simulatorClass.monthlyElectricityRetailPrice
	# print("monthlyElectricityRetailPrice:{}".format(monthlyElectricityRetailPrice))

	# unit kWh month-1
	monthlyRequiredGHCoolingEnergyForPlants = getMonthlyRequiredGHCoolingEnergyForPlants(requiredCoolingEnergyConsumptionForPlants["kWh"], simulatorClass)
	# set the data to the object
	simulatorClass.monthlyRequiredGHCoolingEnergyForPlants = monthlyRequiredGHCoolingEnergyForPlants

	# unit: usd month-1
	monthlyCoolingCostForPlants = np.zeros(monthlyRequiredGHCoolingEnergyForPlants.shape[0])

	index = 0
	for monthlyData in monthlyElectricityRetailPrice:

		year = monthlyData[1]
		month = monthlyData[0]
		# exclude the data out of the set start month and end month
		# print("monthlyData:{}".format(monthlyData))
		if datetime.date(int(year), int(month), 1) + relativedelta(months=1) <= Util.getStartDateDateType() or \
						datetime.date(int(year), int(month), 1) > Util.getEndDateDateType():
				continue

		# the electricity retail cost for cooling. unit: USD month-1
		monthlyCoolingCostForPlants[index] = (monthlyData[2] / 100.0 ) * monthlyRequiredGHCoolingEnergyForPlants[index]
		index += 1

	print("monthlyCoolingCostForPlants:{}".format(monthlyCoolingCostForPlants))

	totalCoolingCostForPlants = sum(monthlyCoolingCostForPlants)

	return totalCoolingCostForPlants

# 	electricityCunsumptionByPad = getElectricityCunsumptionByPad(simulatorClass)
# 	electricityCunsumptionByFan = getElectricityCunsumptionByFan(simulatorClass)
# def getElectricityCunsumptionByPad(simulatorClass):
# def getElectricityCunsumptionByFan(simulatorClass):


def getMonthlyRequiredGHCoolingEnergyForPlants(requiredCoolingEnergyConsumptionForPlants, simulatorClass):

	month = simulatorClass.getMonth()

	numOfMonths = Util.getSimulationMonthsInt()
	monthlyRequiredGHCoolingEnergyForPlants = np.zeros(numOfMonths)
	monthIndex = 0
	# insert the initial value
	monthlyRequiredGHCoolingEnergyForPlants[0] = requiredCoolingEnergyConsumptionForPlants[0]
	for i in range(1, month.shape[0]):

		monthlyRequiredGHCoolingEnergyForPlants[monthIndex] += requiredCoolingEnergyConsumptionForPlants[i]
		if month[i - 1] != month[i]:
			# move onto the next month
			monthIndex += 1

	return monthlyRequiredGHCoolingEnergyForPlants

