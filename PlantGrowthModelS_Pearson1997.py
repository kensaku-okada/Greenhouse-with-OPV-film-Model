# -*- coding: utf-8 -*-

##########import package files##########
import sys
import os as os
import numpy as np
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
import PlantGrowthModelS_Pearson1997Constant as PearsonConstant
#######################################################

# command to show all array data
# np.set_printoptions(threshold=np.inf)
# print ("hourlyHorizontalDirectOuterSolarIrradiance:{}".format(hourlyHorizontalDirectOuterSolarIrradiance))
# np.set_printoptions(threshold=1000)

# ####################################################################################################
# # Stop execution here...
# sys.exit()
# # Move the above line to different parts of the assignment as you implement more of the functionality.
# ####################################################################################################


def calcUnitDailyFreshWeightS_Pearson1997(simulatorClass):
	'''
	reference: S. Pearson, T. R. Wheeler, P. Hadley & A. E. Wheldon, 1997, "A validated model to predict the effects of environment on the growth of lettuce (Lactuca sativa L.): Implications for climate change"
	https://www.researchgate.net/publication/286938495_A_validated_model_to_predict_the_effects_of_environment_on_the_growth_of_lettuce_Lactuca_sativa_L_Implications_for_climate_change
						D. G. SWEENEY, D. W. HAND, G. SLACK AND J. H. M. THORNLEY, 1981, "Modelling the Growth of Winter Lettuce": http://agris.fao.org/agris-search/search.do?recordID=US201301972216

	:return:
	'''

	cultivationDaysperHarvest = simulatorClass.getCultivationDaysperHarvest()
	# OPVAreaCoverageRatio = simulatorClass.getOPVAreaCoverageRatio()
	# hasShadingCurtain = simulatorClass.getIfHasShadingCurtain()
	# ShadingCurtainDeployPPFD = simulatorClass.getShadingCurtainDeployPPFD()

	simulationDaysInt = util.getSimulationDaysInt()

	##################################
	##### input variables start #####
	##################################
	# Temperature [Clusius]
	# TODO estimate the greenhouse temperature inside by comparing the imported data and Poly's data
	# it was assumed that the canopy temperature is instantaneously adjusted to the setpoint temperature at each hour.
	T_a = getGreenhouseTemperatureEachDay(simulatorClass)

	# Horizontal irradiance above the canopy (PAR) [W/m^2]
	directSolarIrradianceToPlants = simulatorClass.directSolarIrradianceToPlants
	diffuseSolarIrradianceToPlants = simulatorClass.diffuseSolarIrradianceToPlants
	totalSolarIrradianceToPlants = directSolarIrradianceToPlants + diffuseSolarIrradianceToPlants
	# convert the unit from [average W / m^2 each hour] to [J / m^2 each day]
	J = util.convertWattPerSquareMeterEachHourToJoulePerSaureMeterEachDay(totalSolarIrradianceToPlants)

	# CO_2 concentration [kg(CO_2) / m^3]
	# it is temporarily assumed that all hourly CO2 concentration is 400 [ppm] = 775 [kg / m^3] 355 [ppm] = 688 [kg / m^3]
	# You can convert the unit of CO2 concentration at https://www.lenntech.com/calculators/ppm/converter-parts-per-million.htm
	C = np.array([775.0] * T_a.shape[0])

	# Thermal time [Celsius * d]: calculating thermal time by totalling the mean temperatures for each day during each cultivation period.
	# theta = getThermalTime(T_a)
	theta = np.zeros(T_a.shape[0])

	print("T_a:{}".format(T_a))
	print("J:{}".format(J))
	print("C:{}".format(C))

	# ####################################################################################################
	# # Stop execution here...
	# sys.exit()
	# # Move the above line to different parts of the assignment as you implement more of the functionality.
	# ####################################################################################################

	##################################
	##### input variables end #####
	##################################

	# dependent variables
	# Structured dry weight [g]
	W_G = np.zeros(T_a.shape[0])
	# Storage (non-structural) dry weight [g]
	W_S = np.zeros(T_a.shape[0])
	# The plant dry weight (excluding roots) [g]
	W = np.zeros(T_a.shape[0])

	# initial values
	# reference:
	# it was estimated from the reference of SWEENEY et al. (1981) saying "The cropping area was divided into three east-west strips (5.49 m X 1.83 m) with 0.6 m wide pathways on either side." and
	# its initial values W_G(1) (= 1.9 * 10^(-6) kg) and W_S(1) (= 1.9 * 10^(-6) kg), and Pearson et al (1997) saying "... the initial  dry  weight  of  transplants  comprised 80%  structural  and  20%  storage  material, since  Goudriaan  et  al.  (1985)  indicated  that storage dry weight rarely exceeds 25%  of the total dry matter."
	# input initial data [g]
	# W_G[0] = 1.9*10**(-3.0)*2 * 0.8 * constant.greenhouseCultivationFloorArea / (5.49 * 1.83)
	W_G[0] = 1.9*10**(-3.0)*2 * 0.8
	# Storage dry weight  [g]
	W_S[0] = 1.9*10**(-3.0)*2 * 0.2

	# It was assumed to take 2 days to the next cultivation cycle assuming "transplanting  shock  prevented growth during the first 48 h"
	# initial total dry weight
	W[0] = W_G[0] + W_S[0]
	theta[0] = T_a[0]

	# print("W_G[0]:{}".format(W_G[0]))
	# print("W_S[0]:{}".format(W_S[0]))

	# loop counter
	i = 1
	# reference: Pearson et al. (1997)
	# It was assumed that the germination and growth before transplanting were done at the growth chamber. The simulation period starts when the first cycle lettuces were planted in a greenhouse.
	while i < simulationDaysInt:
		print("i-1:{}, W_G[i-1]:{}, W_S[i-1]:{}".format(i-1, W_G[i-1],W_S[i-1]))
		# the sub-optimal equivalent of a supra-optimal temperature) eq 8
		T_e = PearsonConstant.T_o - abs(PearsonConstant.T_o - T_a[i-1])
		print("T_e:{}".format(T_e))

		# the increase in structured dry weight
		# dW_G = W_G[i-1] * PearsonConstant.k * T_e
		dW_G = (W_G[i-1]) * PearsonConstant.k * T_e
		W_G[i] = W_G[i - 1] + dW_G
		print("dW_G:{}".format(dW_G))

		# T_ep: effective temperature [Celusius]
		# According to Pearson, S. Hadley, P. Wheldon, A.E. (1993), "A reanalysis of the effects of temperature and irradiance on time to flowering in chrysanthemum
		# (Dendranthema grandiflora)", Effective temperature is the sub-optimum temperature equivalent of a supra-optimum temperature in terms of developmental rate.
		# Also, since Pearson et al. (1997) says "The  effective  temperature  (Tep)  for  photosynthesis  was  determined  with  an  optimum  of  Top  and  the function  had  a  rate  constant phi."
		# it was assumed that T_ep can be derived with the same equation and variables as T_e
		T_ep = PearsonConstant.T_op - abs(PearsonConstant.T_op - T_a[i-1])
		print("T_ep:{}".format(T_ep))

		# the decline in photosynthesis with plant age
		# Pg = PearsonConstant.alpha_m*((1.0-PearsonConstant.beta)/(PearsonConstant.tau*C[i-1]))*J[i-1]*T_ep*PearsonConstant.phi*(PearsonConstant.theta_m-theta[0])/PearsonConstant.theta_m
		Pg = PearsonConstant.alpha_m * ((1.0-PearsonConstant.beta)/ (PearsonConstant.tau * C[i-1]))*J[i-1]*T_ep*PearsonConstant.phi*(PearsonConstant.theta_m-theta[i-1])/PearsonConstant.theta_m
		print("Pg:{}".format(Pg))
		# the relation describing respiration losses
		# print("PearsonConstant.R_G:{}".format(PearsonConstant.R_G))
		# print("PearsonConstant.theta_m:{}".format(PearsonConstant.theta_m))
		# print("PearsonConstant.gamma:{}".format(PearsonConstant.gamma))
		# print("PearsonConstant.epsilon:{}".format(PearsonConstant.epsilon))

		# Rd = PearsonConstant.R_G * ((PearsonConstant.theta_m - theta[0])/PearsonConstant.gamma) / PearsonConstant.theta_m * T_a[i-1] * PearsonConstant.epsilon * dW_G
		# this part was changed from the reference's original formula: theta[0] -> theta[i-1]
		Rd = PearsonConstant.R_G * ((PearsonConstant.theta_m - theta[i-1])/PearsonConstant.gamma) / PearsonConstant.theta_m * T_a[i-1] * PearsonConstant.epsilon * dW_G
		print("Rd:{}".format(Rd))
		dW_S = PearsonConstant.psi * (PearsonConstant.h)**2.0 * (1.0 - math.exp(-PearsonConstant.F_G * W_G[i-1] / ((PearsonConstant.h)**2.0))) * Pg - Rd
		print("dW_S:{}".format(dW_S))

		W_S[i] = W_S[i - 1] + dW_S

		# The plant dry weight (excluding roots) W
		W[i] = W_G[i] + W_S[i]
		print("i:{}, W[i]:{}".format(i, W[i]))

		# accumulate the thermal time
		theta[i] = theta[i - 1] + T_a[i - 1]

		# if the dry weight exceeds the weight for cultimvation, then reset the dryweight
		if W[i] > constant.harvestWeight :

			# It was assumed to take 3 days to the next cultivation cycle assuming "transplanting  shock  prevented growth during the first 48 h", and it takes one day for preparation.
			i += 3 + 1
			if(i >= simulationDaysInt): break

			# reset the weights
			W_S[i-1] = W_G[0]
			W_S[i-2] = W_G[0]
			W_G[i-1] = W_S[0]
			W_G[i-2] = W_S[0]
			# The plant dry weight (excluding roots) W
			W[i-1] = W_S[i-1] + W_G[i-1]
			W[i-2] = W_S[i-2] + W_G[i-2]

			# accumulate the thermal time
			theta[i - 2] = T_a[i-2]
			theta[i-1] = theta[i - 2] +  T_a[i-1]
			theta[i] = theta[i-1] + T_a[i]

		else:

			# increment the counter for one day
			i += 1

	print("theta:{}".format(theta))
	print("W_G:{}".format(W_G))
	print("W_S:{}".format(W_S))
	print("W:{}".format(W))
	# convert the dry weight into fresh weight
	WFresh = constant.DryMassToFreshMass * W
	print("WFresh:{}".format(WFresh))

	# get the fresh weight increase
	WFreshWeightIncrease = getFreshWeightIncrease(WFresh)
	# get the accumulated fresh weight during the simulation period
	WAccumulatedFreshWeight = getAccumulatedFreshWeight(WFresh)
	# get the harvested weight
	WHarvestedFreshWeight = getHarvestedFreshWeight(WFresh)

	return WFresh, WFreshWeightIncrease, WAccumulatedFreshWeight, WHarvestedFreshWeight


def getGreenhouseTemperatureEachDay(simulatorClass):
	# It was assumed the greenhouse temperature was instantaneously adjusted to the set point temperatures at daytime and night time respectively
	hourlyDayOrNightFlag = simulatorClass.hourlyDayOrNightFlag
	greenhouseTemperature = np.array([constant.setPointTemperatureDayTime if i == constant.daytime else constant.setPointTemperatureNightTime for i in hourlyDayOrNightFlag])

	# calc the mean temperature each day
	dailyAverageTemperature = np.zeros(util.getSimulationDaysInt())
	for i in range(0, util.getSimulationDaysInt()):
		dailyAverageTemperature[i] = np.average(greenhouseTemperature[i * constant.hourperDay: (i + 1) * constant.hourperDay])
	return dailyAverageTemperature


def getThermalTime(dailyAverageTemperature):
	'''
	definition of thermal time in plant science reference: http://onlinelibrary.wiley.com/doi/10.1111/j.1744-7348.2005.04088.x/pdf
	:param dailyAverageTemperature: average [Celusius] per day
	:return:
	'''
	thermalTime = np.zeros(dailyAverageTemperature.shape[0])
	for i in range(0, thermalTime.shape[0]):
		thermalTime[i] = sum(dailyAverageTemperature[0:i+1])
	return thermalTime

def getFreshWeightIncrease(WFresh):
	# get the fresh weight increase

	freshWeightIncrease = np.array([WFresh[i] - WFresh[i-1] if WFresh[i] - WFresh[i-1] > 0 else 0.0 for i in range (1, WFresh.shape[0])])
	# insert the value for i == 0
	freshWeightIncrease[0] = 0.0

	return freshWeightIncrease

def getAccumulatedFreshWeight(WFresh):
	# get accumulated fresh weight

	accumulatedFreshWeight = np.array([WFresh[i] + WFresh[i-1] if WFresh[i] - WFresh[0] > 0 else WFresh[i-1] for i in range (1, WFresh.shape[0])])
	# insert the value for i == 0
	accumulatedFreshWeight[0] = WFresh[0]

	return accumulatedFreshWeight


def getHarvestedFreshWeight(WFresh):
	# get the harvested fresh weight

	# record the fresh weight harvested at each harvest date
	harvestedFreshWeight = np.array([WFresh[i-1] if WFresh[i] - WFresh[i-1] < 0 else 0.0 for i in range (1, WFresh.shape[0])])
	# insert the value for i == 0
	harvestedFreshWeight[0] = 0.0

	return harvestedFreshWeight






