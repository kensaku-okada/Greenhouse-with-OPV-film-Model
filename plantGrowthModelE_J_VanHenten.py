# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 15 Jun 2017
# last edit date: 15 Jun 2017
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
import Util as util
import datetime
import Lettuce
import PlantGrowthModelE_J_VanHentenConstant as VanHentenConstant
import PlantGrowthPenaltyByPhotoinhibition as Photoinhibition


def calcUnitDailyFreshWeightE_J_VanHenten1994(simulatorClass):
    '''
    "dt" is 1 second.
    reference: E. J. Van Henten, 1994, "validation of a dynamic lettuce growth model for greenhouse climate control"
    https://www.sciencedirect.com/science/article/pii/S0308521X94902801

    :return:
    '''
    # According to Van Henten (1994), 'With data logging system connected to the greenhouse climate computer, half-hour mean values of the indoor climate data were recorded.'

    # get the simulation days
    simulationDaysInt = util.getSimulationDaysInt()
    # print("simulationDaysInt:{}".format(simulationDaysInt))

    # take date and time
    year = simulatorClass.getYear()
    month = simulatorClass.getMonth()
    day = simulatorClass.getDay()
    # print("year[0]:{}".format(year[0]))

    # get the summer period hours
    summerPeriodDays = datetime.date(year=year[0], month=constant.SummerPeriodEndMM, day=constant.SummerPeriodEndDD) - \
                       datetime.date(year=year[0], month=constant.SummerPeriodStartMM, day=constant.SummerPeriodStartDD)
    # change the data type and unit
    summerPeriodHours = summerPeriodDays.days * constant.hourperDay
    # print("summerPeriodHours:{}".format(summerPeriodHours))

    # [head/m^2]
    plantDensity = constant.plantDensity
    # plantDensity = 18.0

    # it was assumed that the canopy temperature is instantaneously adjusted to the setpoint temperature at each hour.
    U_T = Lettuce.getGreenhouseTemperatureEachHour(simulatorClass)
    # the following definition of U_T is used for validation
    # U_T = simulatorClass.GHAirTemperatureValidationData

    # print("U_T:{}".format(U_T))
    # print("U_T.shape:{}".format(U_T.shape))

    # Horizontal irradiance above the canopy (PAR) [W/m^2]
    directSolarIrradianceToPlants = simulatorClass.directSolarIrradianceToPlants
    diffuseSolarIrradianceToPlants = simulatorClass.diffuseSolarIrradianceToPlants
    totalSolarIrradianceToPlants = directSolarIrradianceToPlants + diffuseSolarIrradianceToPlants
    # By dividing the irradiance by 2, the shortwave radiation is converted into PAR [W/m^2]
    U_par = totalSolarIrradianceToPlants/2.0
    # print("U_par:{}".format(U_par))

    # unit: ppm - pers per million (1/1000000)
    # it is temporarily assumed that all hourly CO2 concentration is 400 ppm
    U_CO2 = np.array([400] * U_T.shape[0])

    # structured dry weight on each day [g / m**2]
    Xsdw = np.zeros(simulationDaysInt*constant.hourperDay)
    # non structured dry weight on each day [g / m**2]
    Xnsdw = np.zeros(simulationDaysInt*constant.hourperDay)
    # total dry weight
    DW = np.zeros(simulationDaysInt*constant.hourperDay)
    # dry weight per head
    DWPerHead = np.zeros(simulationDaysInt*constant.hourperDay)
    # fresh weight per head
    FWPerHead = np.zeros(simulationDaysInt*constant.hourperDay)

    # set the initial values
    # according to the reference, the initial dry weight was 2.7 g/m^2 with the cultivar "Berlo" (started 17 October 1991), and 0.72 g/m^2  with "Norden"(started 21 January 1992)
    # [g / m**2]
    InitialdryWeight = 2.7
    # [g / m**2]
    Xsdw[0] = InitialdryWeight * 0.75
    # [g / m**2]
    Xnsdw[0] = InitialdryWeight * 0.25
    # [g / m**2]
    DW[0] = Xsdw[0] + Xnsdw[0]
    # DWPerHead[0] = DW[0] / plantDensity
    # FWPerHead[0] = DWPerHead[0] * constant.DryMassToFreshMass

    # 1 loop == 1 hour
    i = 1
    while i  < simulationDaysInt * constant.hourperDay:
        # for i in range (1, constant.cultivationDaysperHarvest):

        # if you do not grow plant during the summer period, then skip the period
        # if simulatorClass.getIfGrowForSummerPeriod() is False and \
        if constant.ifGrowForSummerPeriod is False and \
                datetime.date(year[i], month[i], day[i]) >= datetime.date(year[i], constant.SummerPeriodStartMM, constant.SummerPeriodStartDD) and \
            datetime.date(year[i], month[i], day[i]) <= datetime.date(year[i], constant.SummerPeriodEndMM, constant.SummerPeriodEndDD):

            # skip the summer period cultivation cycle
            # It was assumed to take 3 days to the next cultivation cycle assuming "transplanting  shock  prevented growth during the first 48 h", and it takes one day for preparation.
            i += summerPeriodHours + 3 * constant.hourperDay

            # initialize the plant weight for the cultivation soon after the summer period
            Xsdw[i - 2 * constant.hourperDay:i], \
            Xnsdw[i - 2 * constant.hourperDay:i], \
            DW[i - 2 * constant.hourperDay:i] = resetInitialWeights(i, Xsdw[0], Xnsdw[0])
            # print("i:{}, Xsdw[i - 2 * constant.hourperDay:i]:{}, Xnsdw[i - 2 * constant.hourperDay:i]:{}, DW[i - 2 * constant.hourperDay:i]:{}".\
            #     format(i, Xsdw[i - 2 * constant.hourperDay:i], Xnsdw[i - 2 * constant.hourperDay:i], DW[i - 2 * constant.hourperDay:i]))

            continue

        ####################### parameters for calculating f_photo_max start #######################
        # the carboxylation conductance
        g_car = VanHentenConstant.c_car1 * (U_T[i-1])**2 + VanHentenConstant.c_car2 * U_T[i-1] + VanHentenConstant.c_car3
        # print("i:{}, g_car:{}".format(i, g_car))

        # the canopy conductance for diffusion of CO2 from the ambient air to the chloroplast :gross carbon dioxide assimilation rate of the canopy having an effective surface of 1m^2 per square meter soild at complete soil covering.
        g_CO2 = VanHentenConstant.g_bnd['m s-1']*VanHentenConstant.g_stm['m s-1']* g_car / (VanHentenConstant.g_bnd['m s-1'] * VanHentenConstant.g_stm['m s-1'] \
                + VanHentenConstant.g_bnd['m s-1']*g_car + VanHentenConstant.g_stm['m s-1'] * g_car)
        # print("g_CO2:{}".format(g_CO2))

        # CO2 compensation point
        gamma = VanHentenConstant.c_upperCaseGamma['ppm'] * VanHentenConstant.c_Q10_upperCaseGamma ** ((U_T[i-1] -20.0)/10.0)
        # print("gamma:{}".format(gamma))

        # light use efficiency
        epsilon = {'g J-1': VanHentenConstant.c_epsilon['g J-1'] * (U_CO2[i-1] - gamma) / ( U_CO2[i-1]  + 2.0 * gamma)}
        # print("epsilon:{}".format(epsilon))
        ####################### parameters for calculating f_photo_max end #######################

        # the response of canopy photosynthesis
        f_photo_max = {'g m-2 s-2': epsilon['g J-1'] * U_par[i-1] * g_CO2 * VanHentenConstant.c_omega['g m-3'] * (U_CO2[i-1] - gamma) / \
                                    (epsilon['g J-1']* U_par[i-1] + g_CO2 * VanHentenConstant.c_omega['g m-3'] * (U_CO2[i-1] - gamma))}
        # print("f_photo_max:{}".format(f_photo_max))

        # specific growth rate: the transfromation rate of non-structural dry weight to structural dry weight
        r_gr = VanHentenConstant.c_gr_max['s-1'] * Xnsdw[i-1] / (VanHentenConstant.c_gamma * Xsdw[i-1] + Xnsdw[i-1]) * (VanHentenConstant.c_Q10_gr ** ((U_T[i] - 20.0) / 10.0))
        # print("r_gr:{}".format(r_gr))
        # the maintenance respiration rate of the crop
        f_resp = (VanHentenConstant.c_resp_sht['s-1'] * (1 - VanHentenConstant.c_tau) * Xsdw[i-1] + VanHentenConstant.c_resp_rt['s-1'] * VanHentenConstant.c_tau * Xsdw[i-1])\
                 * VanHentenConstant.c_Q10_resp ** ((U_T[i-1] - 25.0)/10.0)
        # print("f_resp:{}".format(f_resp))
        # gross canopy photosynthesis
        f_photo = (1.0 - np.exp( - VanHentenConstant.c_K * VanHentenConstant.c_lar['m2 g-2'] * (1- VanHentenConstant.c_tau) * Xsdw[i-1])) * f_photo_max['g m-2 s-2']
        # print("f_photo:{}".format(f_photo))

        # [g / m ** 2/ sec]
        d_structuralDryWeight = r_gr * Xsdw[i-1]
        # [g / m ** 2/ sec]
        d_nonStructuralDryWeight = VanHentenConstant.c_alpha * f_photo - r_gr * Xsdw[i-1] - f_resp - (1 - VanHentenConstant.c_beta) / VanHentenConstant.c_beta * r_gr * Xsdw[i-1]

        # unit conversion. [g / m ** 2/ sec] -> [g / m ** 2/ hour]
        d_structuralDryWeight = d_structuralDryWeight * constant.secondperMinute * constant.minuteperHour
        d_nonStructuralDryWeight = d_nonStructuralDryWeight * constant.secondperMinute * constant.minuteperHour
        # print("d_structuralDryWeight:{}".format(d_structuralDryWeight))
        # print("d_nonStructuralDryWeight:{}".format(d_nonStructuralDryWeight))

        # increase the plant weight
        Xsdw[i] = Xsdw[i-1] + d_structuralDryWeight
        Xnsdw[i] = Xnsdw[i-1] + d_nonStructuralDryWeight
        DW[i] = Xsdw[i] +  Xnsdw[i]

        # if the dry weight exceeds the weight for cultimvation, then reset the dryweight
        if DW[i] > constant.harvestDryWeight * plantDensity:

            # It was assumed to take 3 days to the next cultivation cycle assuming "transplanting  shock  prevented growth during the first 48 h", and it takes one day for preparation.
            i += 3 * constant.hourperDay
            if (i >= simulationDaysInt * constant.hourperDay): break

            # The plant dry weight (excluding roots) W
            Xsdw[i - 2 * constant.hourperDay:i], \
            Xnsdw[i - 2 * constant.hourperDay:i],\
            DW[i - 2 * constant.hourperDay:i] = resetInitialWeights(i, Xsdw[0], Xnsdw[0])

        else:
            # increment the counter for one hour
            i += 1

    # the plant weight per head
    # Ydw = (Xsdw + Xnsdw) / float(constant.numOfHeadsPerArea)

    DWPerHead = DW / plantDensity
    # print("DWPerHead:{}".format(DWPerHead))

    FWPerHead = DWPerHead * constant.DryMassToFreshMass
    # get the fresh weight increase per head
    WFreshWeightIncrease = Lettuce.getFreshWeightIncrease(FWPerHead)
    # get the accumulated fresh weight per head during the simulation period
    WAccumulatedFreshWeightIncrease = Lettuce.getAccumulatedFreshWeightIncrease(FWPerHead)
    # get the harvested weight per head
    WHarvestedFreshWeight = Lettuce.getHarvestedFreshWeight(FWPerHead)

    # print("FWPerHead.shape:{}".format(FWPerHead.shape))
    # print("WFreshWeightIncrease.shape:{}".format(WFreshWeightIncrease.shape))
    # print("WAccumulatedFreshWeightIncrease.shape:{}".format(WAccumulatedFreshWeightIncrease.shape))
    # print("WHarvestedFreshWeight.shape:{}".format(WHarvestedFreshWeight.shape))

    # np.set_printoptions(threshold=np.inf)
    # print("FWPerHead:{}".format(FWPerHead))
    # print("WHarvestedFreshWeight:{}".format(WHarvestedFreshWeight))
    # np.set_printoptions(threshold=1000)

    return FWPerHead, WFreshWeightIncrease, WAccumulatedFreshWeightIncrease, WHarvestedFreshWeight

    # np.set_printoptions(threshold=np.inf)
    # print("Xsdw:{}".format(Xsdw))
    # print("Xnsdw:{}".format(Xnsdw))
    # print("DW:{}".format(DW))
    # print("FWPerHead:{}".format(FWPerHead))
    # np.set_printoptions(threshold=100)

    ###################################################
    # From here, we consider the summer period ########
    ###################################################

def resetInitialWeights(i, initialXsdw, initialXnsdw):
    # reset the weights
    return initialXsdw * np.ones(2 * constant.hourperDay), initialXnsdw * np.ones(2 * constant.hourperDay),\
            initialXsdw * np.ones(2 * constant.hourperDay) + initialXnsdw * np.ones(2 * constant.hourperDay)
