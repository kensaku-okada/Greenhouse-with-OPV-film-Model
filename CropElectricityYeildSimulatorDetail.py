# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 06 Nov 2016
# last edit date: 14 Dec 2016
#######################################################

##########import package files##########
from scipy import stats
import datetime
import sys
import os as os
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
import OPVFilm
import Lettuce
import PlantGrowthModelE_J_VanHenten
import QlearningAgentShadingCurtain as QRLshadingCurtain
from dateutil.relativedelta import *
#######################################################

def calcOPVmoduleSolarIrradianceGHRoof(simulatorClass, roofDirectionNotation=constant.roofDirectionNotation):
    '''
    calculate the every kind of solar irradiance to the OPV film. The tilt angel and direction angle  of OPV panes is
    define in CropElectricityYeildSimulatorConstant.py
    '''

    year = simulatorClass.getYear()
    month = simulatorClass.getMonth()
    day = simulatorClass.getDay()
    hour = simulatorClass.getHour()
    hourlyHorizontalDiffuseOuterSolarIrradiance = simulatorClass.getImportedHourlyHorizontalDiffuseSolarRadiation()
    hourlyHorizontalDirectOuterSolarIrradiance = simulatorClass.getImportedHourlyHorizontalDirectSolarRadiation()


    # [rad] symbol: delta
    hourlyDeclinationAngle = OPVFilm.calcDeclinationAngle(year, month, day)
    # print "hourlyDeclinationAngle:{}".format(np.degrees(hourlyDeclinationAngle))
    # print "hourlyDeclinationAngle:{}".format(hourlyDeclinationAngle)

    # [rad] symbol: omega
    # hourlySolarHourAngle = OPVFilm.getSolarHourAngleKacira2003(hour)
    hourlySolarHourAngle = OPVFilm.getSolarHourAngleYano2009(hour)
    # print "hourlySolarHourAngle:{}".format(np.degrees(hourlySolarHourAngle))

    # [rad] symbol: alpha. elevation angle = altitude angle
    hourlySolarAltitudeAngle = OPVFilm.calcSolarAltitudeAngle(hourlyDeclinationAngle, hourlySolarHourAngle)
    # print "np.degrees(hourlySolarAltitudeAngle):{}".format(np.degrees(hourlySolarAltitudeAngle))
    # print "hourlySolarAltitudeAngle:{}".format(hourlySolarAltitudeAngle)

    # [rad] symbol: beta. azimuth angle
    hourlySolarAzimuthAngle = OPVFilm.calcSolarAzimuthAngle(hourlyDeclinationAngle, hourlySolarAltitudeAngle, hourlySolarHourAngle)
    # print "hourlySolarAzimuthAngle:{}".format(hourlySolarAzimuthAngle)

    # used only in Kacira 2003
    # [rad] symbol: theta_z
    hourlyZenithAngle = math.radians(90.0) - hourlySolarAltitudeAngle
    # print "math.radians(90.0):{}".format(math.radians(90.0))
    # print "hourlyZenithAngle:{}".format(hourlyZenithAngle)

    # used only in kacira 2003
    # since this model is not for two axis tracking panel, this is zero according to the equation (6) of Kacira et al.(2003) [°]
    # [rad] symbol: gamma
    hourlySurfaceAzimuthAngle = math.radians(0.0)


    # if the direction of greenhouse is north-south and the roof tilt direction is east-west
    if roofDirectionNotation == "EastWestDirectionRoof":
        # [rad] symbol: phi_p
        # probably module azimuth angle == surface azimuth angle
        # if the OPV module facing east
        hourlyModuleAzimuthAngleEast = math.radians(-90.0)
        # if the OPV module facing west
        hourlyModuleAzimuthAngleWest = math.radians(90.0)
    # if the direction of greenhouse is east-west and the roof tilt direction is north-south
    elif roofDirectionNotation == "NorthSouthDirectionRoof":
        # TODO: revise in the future project
        hourlyModuleAzimuthAngleNorth = math.radians(180.0)
        # if the OPV module facing west
        hourlyModuleAzimuthAngleSouth = math.radians(0.0)

    # this computation is necessary to calculate the horizontal incidence angle for horizontal direct solar irradiance
    hourlyModuleAzimuthAngleSouth = math.radians(0.0)
    hourlyHorizontalSolarIncidenceAngle = OPVFilm.calcSolarIncidenceAngleYano2009(hourlySolarAltitudeAngle, hourlySolarAzimuthAngle, hourlyModuleAzimuthAngleSouth, 0)
    # print "hourlyHorizontalSolarIncidenceAngle:{}".format(hourlyHorizontalSolarIncidenceAngle)

    if roofDirectionNotation == "EastWestDirectionRoof":
        #The incident angle of the beam sunlight on the module surface. [rad] symbol: theta_I
        hourlySolarIncidenceAngleEastDirection = OPVFilm.calcSolarIncidenceAngleYano2009(hourlySolarAltitudeAngle, hourlySolarAzimuthAngle, hourlyModuleAzimuthAngleEast)
        hourlySolarIncidenceAngleWestDirection = OPVFilm.calcSolarIncidenceAngleYano2009(hourlySolarAltitudeAngle, hourlySolarAzimuthAngle, hourlyModuleAzimuthAngleWest)
        # print "hourlySolarIncidenceAngleEastDirection:{}".format(hourlySolarIncidenceAngleEastDirection)
        # print "hourlySolarIncidenceAngleWestDirection:{}".format(hourlySolarIncidenceAngleWestDirection)
    # if the direction of greenhouse is east-west and the roof tilt direction is north-south
    elif roofDirectionNotation == "NorthSouthDirectionRoof":
        # TODO: revise in the future project
        hourlySolarIncidenceAngleEastDirection = OPVFilm.calcSolarIncidenceAngleYano2009(hourlySolarAltitudeAngle, hourlySolarAzimuthAngle, hourlyModuleAzimuthAngleNorth)
        hourlySolarIncidenceAngleWestDirection = OPVFilm.calcSolarIncidenceAngleYano2009(hourlySolarAltitudeAngle, hourlySolarAzimuthAngle, hourlyModuleAzimuthAngleSouth)
    # print ("hourlySolarIncidenceAngleEastDirection:{}".format(hourlySolarIncidenceAngleEastDirection))
    # print ("hourlySolarIncidenceAngleWestDirection:{}".format(hourlySolarIncidenceAngleWestDirection))

    # np.set_printoptions(threshold=np.inf)
    # print "hourlySolarIncidenceAngle:{}".format(np.degrees(hourlySolarIncidenceAngle))
    # np.set_printoptions(threshold=1000)

    # estimated horizontal solar irradiances [W m^-2]. these values are used only when estimating solar radiations.
    # symbol: I_DH.
    directHorizontalSolarRadiation = OPVFilm.getDirectHorizontalSolarRadiation(hourlySolarAltitudeAngle, hourlyHorizontalSolarIncidenceAngle)
    # print "directHorizontalSolarRadiation:{}".format(directHorizontalSolarRadiation)
    # symbol: I_S
    diffuseHorizontalSolarRadiation = OPVFilm.getDiffuseHorizontalSolarRadiation(hourlySolarAltitudeAngle, hourlyHorizontalSolarIncidenceAngle)
    # print "diffuseHorizontalSolarRadiation:{}".format(diffuseHorizontalSolarRadiation)
    # symbol: I_HT
    totalHorizontalSolarRadiation = directHorizontalSolarRadiation + diffuseHorizontalSolarRadiation
    # print "totalHorizontalSolarRadiation:{}".format(totalHorizontalSolarRadiation)


    # tilted surface  solar radiation [W m^-2], real / estimated value branch is in the functions
    # symbol: I_TD (= H_b at Kacira 2004). direct beam radiation on the tilted surface
    print ("call getDirectTitledSolarRadiation for east direction OPV")
    directTiltedSolarRadiationEastDirection = OPVFilm.getDirectTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, hourlySolarIncidenceAngleEastDirection, \
                                                                                    hourlyHorizontalDirectOuterSolarIrradiance)
    print ("call getDirectTitledSolarRadiation for west direction OPV")
    directTiltedSolarRadiationWestDirection = OPVFilm.getDirectTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, hourlySolarIncidenceAngleWestDirection, \
                                                                                    hourlyHorizontalDirectOuterSolarIrradiance)
    # symbol: I_TS  (= H_d_p at Kacira 2004). diffused radiation on the tilted surface.
    diffuseTiltedSolarRadiation = OPVFilm.getDiffuseTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, diffuseHorizontalSolarRadiation, \
                                                                         hourlyHorizontalDiffuseOuterSolarIrradiance)
    # print "diffuseTiltedSolarRadiation:{}".format(diffuseTiltedSolarRadiation)
    # symbol: I_Trho (= H_gr at Kacira 2004) (albedo radiation = reflectance from the ground)
    albedoTiltedSolarRadiation = OPVFilm.getAlbedoTitledSolarRadiation(simulatorClass, hourlySolarAltitudeAngle, totalHorizontalSolarRadiation, \
                                                                       hourlyHorizontalDirectOuterSolarIrradiance+hourlyHorizontalDiffuseOuterSolarIrradiance)
    directSolarRadiationToOPVEastDirection = directTiltedSolarRadiationEastDirection

    directSolarRadiationToOPVWestDirection = directTiltedSolarRadiationWestDirection
    diffuseSolarRadiationToOPV = diffuseTiltedSolarRadiation
    albedoSolarRadiationToOPV = albedoTiltedSolarRadiation
    # directSolarRadiationToOPVEastDirection = hourlyHorizontalDirectOuterSolarIrradiance
    # directSolarRadiationToOPVWestDirection = hourlyHorizontalDirectOuterSolarIrradiance
    # diffuseSolarRadiationToOPV = hourlyHorizontalDiffuseOuterSolarIrradiance
    # albedoSolarRadiationToOPV = np.zeros(util.calcSimulationDaysInt() * constant.hourperDay)
    # RESULT: the DLI of each tilted roof is almost same

    return directSolarRadiationToOPVEastDirection, directSolarRadiationToOPVWestDirection, diffuseSolarRadiationToOPV, albedoSolarRadiationToOPV

    # ####################################################################################################
    # # Stop execution here...
    # sys.exit()
    # # Move the above line to different parts of the assignment as you implement more of the functionality.
    # ####################################################################################################

def calcDailyElectricityYieldSimulationperArea(hourlyOPVTemperature, directSolarRadiationToOPV, \
                            diffuseSolarRadiationToOPV,groundReflectedSolarradiationToOPV):
    '''
    calculate the daily electricity yield per area (m^2).
    :param hourlyOPVTemperature: [celsius]
    :param directSolarRadiationToOPVEastDirection: [W/m^2]
    :param directSolarRadiationToOPVWestDirection: [W/m^2]
    :param diffuseSolarRadiationToOPV: [W/m^2]
    :param groundReflectedSolarradiationToOPV:[W/m^2]
    :return:
    '''
    # print "total solar irradiance:{}".format(directSolarRadiationToOPV+diffuseSolarRadiationToOPV+groundReflectedSolarradiationToOPV)

    # [W/m^2] == [J/s/m^2] -> [J/m^2] per day
    dailyJopvoutperArea = OPVFilm.calcOPVElectricEnergyperArea(hourlyOPVTemperature, directSolarRadiationToOPV+diffuseSolarRadiationToOPV+groundReflectedSolarradiationToOPV)
    # print "dailyJopvout:{}".format(dailyJopvout)

    return dailyJopvoutperArea

def getTotalDLIToPlants(OPVAreaCoverageRatio, directPPFDToOPV, diffusePPFDToOPV, groundReflectedPPFDToOPV, hasShadingCurtain, ShadingCurtainDeployPPFD, \
                        cropElectricityYieldSimulator1):
    '''
    the daily light integral to plants for the given simulation period.
    :param OPVAreaCoverageRatio:
    :param directPPFDToOPV:
    :param diffusePPFDToOPV:
    :param groundReflectedPPFDToOPV:
    :param hasShadingCurtain:
    :param ShadingCurtainDeployPPFD:
    :param cropElectricityYieldSimulator1: instance
    :return:
    '''
    # calculate the light intensity to plants
    # hourly average PPFD [umol m^-2 s^-1]
    hourlyInnerPPFDToPlants = OPVFilm.calcHourlyInnerLightIntensityPPFD(directPPFDToOPV+diffusePPFDToOPV+groundReflectedPPFDToOPV, \
        OPVAreaCoverageRatio, constant.OPVPARTransmittance, hasShadingCurtain,ShadingCurtainDeployPPFD, cropElectricityYieldSimulator1)

    # convert PPFD to DLI
    innerDLIToPlants = util.convertFromHourlyPPFDWholeDayToDLI(hourlyInnerPPFDToPlants)
    # print "innerDLIToPlants:{}".format(innerDLIToPlants)

    return innerDLIToPlants

def penalizeUnitDailyHarvestedFreshWeight(unitDailyHarvestedFreshWeight, cropElectricityYieldSimulator1):
    '''
    the function was made based on the data of plant fresh weights for 400 600, and 800 PPFD (umiol m^-2, s-1) in the following source:
    "Effects of different light intensities on anti-oxidative enzyme activity, quality and biomass in lettuce, Weiguo Fu, Pingping Li, Yanyou Wu, Juanjuan Tang"

    the parameters were derived with the solver of Excel 2007, the process is written in "penalizePlantYieldBySolarRadiation.xlsx"

    TODO: the cultivar of the data was for Loose  green leaf  lettuce, not Magenta or butterhead, which will probably cause the difference of peak light intensity and plant yield weight.
    We will need some data in each case and tune the parameters for better model.

    :param totalDLItoPlants:
    :param unitDailyHarvestedFreshWeight:
    :param cropElectricityYieldSimulator1:
    :return:
    '''
    penalizedUnitDailyHarvestedFreshWeight = np.zeros(unitDailyHarvestedFreshWeight.shape[0])
    # penalizedUnitDailyHarvestedFreshWeight = unitDailyHarvestedFreshWeight

    # get the average light DLi of each cultivation cycle, the data is stored in the element on the harvest date.
    averageDLIonEachCycle = cropElectricityYieldSimulator1.getAverageDLIonEachCycle()

    # parameters
    photoPriod = {"hour":14.0}
    maximumYieldFW = {"g unit-1": 164.9777479}
    optimumLightIntensityDLI = {"mol m-2 d-1": 26.61516313}
    # convert PPFD to DLI
    # optimumLightIntensityPPFD = {"umol m-2 s-1": 524.1249999}
    # optimumLightIntensityDLI = {"mol m-2 d-1": optimumLightIntensityPPFD["umol m-2 s-1"] * constant.secondperMinute * constant.minuteperHour * photoPriod["hour"] / 1000000.0}

    i = 0
    while i <  unitDailyHarvestedFreshWeight.shape[0]:

        # if the date is not the harvest date, then skip.
        if unitDailyHarvestedFreshWeight[i] == 0.0:
            i += 1
            continue
        else:
            print ("non zero averageDLIonEachCycle:{}".format(averageDLIonEachCycle[i]))
            print ("non zero unitDailyHarvestedFreshWeight:{}".format(unitDailyHarvestedFreshWeight[i]))
            # print("getPenalizedUnitFreshWeight(averageDLIonEachCycle[i]):{}, i:{}".format(getPenalizedUnitFreshWeight(averageDLIonEachCycle[i]), i))

            if averageDLIonEachCycle[i] > optimumLightIntensityDLI["mol m-2 d-1"] and getPenalizedUnitFreshWeight(averageDLIonEachCycle[i]) > 0.0:
                # penalize the plant fresh weight
                print ("penaize the fresh weight, i:{}".format(i))
                penalizedUnitDailyHarvestedFreshWeight[i] = unitDailyHarvestedFreshWeight[i] - unitDailyHarvestedFreshWeight[i] / maximumYieldFW["g unit-1"] * (maximumYieldFW["g unit-1"] - getPenalizedUnitFreshWeight(averageDLIonEachCycle[i]))

                print("penalizedUnitDailyHarvestedFreshWeight[i]:{}".format(penalizedUnitDailyHarvestedFreshWeight[i]))
                print("unitDailyHarvestedFreshWeight[i]:{}".format(unitDailyHarvestedFreshWeight[i]))

            elif averageDLIonEachCycle[i] > optimumLightIntensityDLI["mol m-2 d-1"] and getPenalizedUnitFreshWeight(averageDLIonEachCycle[i]) <= 0.0:
                print ("the light intensity may be too strong. The yield was penalized to zero")
                penalizedUnitDailyHarvestedFreshWeight[i] = 0.0
            # no penalization occured
            else:
                penalizedUnitDailyHarvestedFreshWeight[i] = unitDailyHarvestedFreshWeight[i]
        i += 1

    return penalizedUnitDailyHarvestedFreshWeight

def getPenalizedUnitFreshWeight(lightIntensityDLI):
    a = -0.1563
    b = 8.3199
    c = 54.26
    return a * lightIntensityDLI**2 + b * lightIntensityDLI + c

def calcPlantYieldSimulation(directPPFDToOPV, diffusePPFDToOPV, groundReflectedPPFDToOPV,cropElectricityYieldSimulator1 = None):
    '''
    calculate the daily plant yield

    :param plantGrowthModel: String
    :param cultivationDaysperHarvest: [days / harvest]
    :param OPVAreaCoverageRatio: [-] range(0-1)
    :param directPPFDToOPV: hourly average [umol m^-2 s^-1] == PPFD
    :param diffusePPFDToOPV: hourly average [umol m^-2 s^-1] == PPFD
    :param groundReflectedPPFDToOPV: hourly average [umol m^-2 s^-1] == PPFD
    :param hasShadingCurtain: Boolean
    :param ShadingCurtainDeployPPFD: float [umol m^-2 s^-1] == PPFD
    :param cropElectricityYieldSimulator1: object
    :return:
    '''

    plantGrowthModel = cropElectricityYieldSimulator1.getPlantGrowthModel()
    cultivationDaysperHarvest = cropElectricityYieldSimulator1.getCultivationDaysperHarvest()
    OPVAreaCoverageRatio = cropElectricityYieldSimulator1.getOPVAreaCoverageRatio()
    hasShadingCurtain = cropElectricityYieldSimulator1.getIfhasShadingCurtain()
    ShadingCurtainDeployPPFD = cropElectricityYieldSimulator1.getShadingCurtainDeployPPFD()

    # calculate the light intensity to plants
    # hourly average PPFD [umol m^-2 s^-1]
    hourlyInnerPPFDToPlants = OPVFilm.calcHourlyInnerLightIntensityPPFD(directPPFDToOPV+diffusePPFDToOPV+groundReflectedPPFDToOPV, \
        OPVAreaCoverageRatio, constant.OPVPARTransmittance, hasShadingCurtain,ShadingCurtainDeployPPFD, cropElectricityYieldSimulator1)

    # np.set_printoptions(threshold=np.inf)
    # print "OPVAreaCoverageRatio:{}, directPPFDToOPV+diffusePPFDToOPV+groundReflectedPPFDToOPV:{}".format(OPVAreaCoverageRatio, directPPFDToOPV+diffusePPFDToOPV+groundReflectedPPFDToOPV)
    # np.set_printoptions(threshold=1000)

    # calculate the daily increase of unit fresh weight
    if plantGrowthModel == constant.TaylorExpantionWithFluctuatingDLI:
        # [g]
        shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitHarvestedFreshWeight = \
            Lettuce.calcUnitDailyFreshWeightBoth2003TaylorExpantionWithVaryingDLI(hourlyInnerPPFDToPlants, cultivationDaysperHarvest, cropElectricityYieldSimulator1)
        # print "shootFreshMassList.shape:{}".format(shootFreshMassList.shape)

        return shootFreshMassList, unitDailyFreshWeightIncrease,accumulatedUnitDailyFreshWeightIncrease,unitHarvestedFreshWeight

    elif plantGrowthModel == constant.E_J_VanHenten:
        # [g]
        shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitHarvestedFreshWeight = \
            PlantGrowthModelE_J_VanHenten.py.calcUnitDailyFreshWeightE_J_VanHenten1994(hourlyInnerPPFDToPlants, cropElectricityYieldSimulator1)

        return shootFreshMassList, unitDailyFreshWeightIncrease,accumulatedUnitDailyFreshWeightIncrease,unitHarvestedFreshWeight


    else:
      print ("no valid model name is assigned. Return error. stop the simulation")
      ####################################################################################################
      # Stop execution here...
      sys.exit()
      # Move the above line to different parts of the assignment as you implement more of the functionality.
      ####################################################################################################



def trainWeightsRLShadingCurtainDayStep(hasShadingCurtain, qLearningAgentsShadingCurtain=None, cropElectricityYieldSimulator1 = None):
  '''

  :param hasShadingCurtain:
  :param cropElectricityYieldSimulator1:
  :return:
  '''

  if hasShadingCurtain:

    # # set values necessary for RL training/testing
    # # for dLIEachdayThroughInnerStructure on a certain day
    # hourlyInnerLightIntensityPPFDThroughInnerStructure = cropElectricityYieldSimulator1.getHourlyInnerLightIntensityPPFDThroughInnerStructure()
    # # set dLIThroughInnerStructure to the object
    # dLIThroughInnerStructure = util.convertFromHourlyPPFDWholeDayToDLI(hourlyInnerLightIntensityPPFDThroughInnerStructure)
    # qLearningAgentsShadingCurtain.setDLIThroughInnerStructure(dLIThroughInnerStructure)

    print ("training parameters: epsilon={}, gamma={}, alpha={}, period:{}".format(\
      qLearningAgentsShadingCurtain.epsilon, qLearningAgentsShadingCurtain.gamma, qLearningAgentsShadingCurtain.alpha,  constant.SimulationStartDate + "-" + constant.SimulationEndDate))
    for trainingIteration in range (0, qLearningAgentsShadingCurtain.numTraining):

      if trainingIteration % 100 == 0:
        # print("Iteration checkpoint: datetime.datetime.now():{}. trainingIteration:{}".format(datetime.datetime.now(), trainingIteration ))
        print("trainingIteration: {}, qLearningAgentsShadingCurtain.weights:{}, datetime.datetime.now():{}".format(\
          trainingIteration, qLearningAgentsShadingCurtain.weights, datetime.datetime.now()))

      # training the q value function
      for day in range (0, util.getSimulationDaysInt()):

        state = day

        #########################################################################
        ############# set values necessary for RL training features##############
        #########################################################################
        # set day to the instance
        qLearningAgentsShadingCurtain.setDay(day)
        # dLIEachdayThroughInnerStructure on a certain day, necessary to cal DLI to PLants
        # qLearningAgentsShadingCurtain.setDLIEachDayThroughInnerStructure(dLIThroughInnerStructure[state])

        #set num of days from Jan 1st.
        daysFromJan1st = util.getNumOfDaysFromJan1st(util.getStartDateDateType() + datetime.timedelta(days=day))
        # date on a certain day
        qLearningAgentsShadingCurtain.setDaysFromJan1st(daysFromJan1st)

        # action = "openCurtain" or "closeCurtain"
        # if the state is at the terminal state, action is None.
        action = qLearningAgentsShadingCurtain.getAction(state)

        # if the q value is not initialized, initialize the q value. if initialized, just get the q value given state and action
        # state = qlearningAgentsShadingCurtain.getQValue(day, action)
        approximateQvalue = qLearningAgentsShadingCurtain.getApproximateQValue(state, action)
        # print ("approximateQvalue:{}".format(approximateQvalue))
        # set approximateQvalue to Q
        qLearningAgentsShadingCurtain.setApproximateQValue(approximateQvalue, state, action)


        # approximatedQvalueNextState = []
        # for action in qLearningAgentsShadingCurtain.getLegalActions(day):
        #   approximatedQvalueNextState.append(qLearningAgentsShadingCurtain.getApproximateQValue(day + 1, action))
        # approximateMaxQvalueNextState = max[approximatedQvalueNextState]

        # get the maximum q value in the next state
        if (state+1) == util.getSimulationDaysInt():
          approximateMaxQvalueNextState = 0.0
        else:
          approximateMaxQvalueNextState = qLearningAgentsShadingCurtain.getApproximateValue(state + 1)

        # calc the difference between the current q value and the maximum q value in the next state, which is used for updating weights

        difference = (qLearningAgentsShadingCurtain.getReward(day) + approximateMaxQvalueNextState) - approximateQvalue
        # print ("qLearningAgentsShadingCurtain.getReward(day):{}".format(qLearningAgentsShadingCurtain.getReward(day)))
        # print ("approximateMaxQvalueNextState:{}".format(approximateMaxQvalueNextState))
        # print ("approximateQvalue:{}".format(approximateQvalue))
        # print ("difference:{}".format(difference))

        # update weight of the q learning function
        qLearningAgentsShadingCurtain.updateApproximateWeight(difference)

    # print ("qLearningAgentsShadingCurtain.weights:{}".format(qLearningAgentsShadingCurtain.weights))
    # print ("check trainingIteration:{}".format(trainingIteration))

    # print ("qLearningAgentsShadingCurtain.weights:{}".format(qLearningAgentsShadingCurtain.weights))
    print ("qLearningAgentsShadingCurtain.approximateQ:{}".format(qLearningAgentsShadingCurtain.approximateQ))

    return qLearningAgentsShadingCurtain
    # ####################################################################################################
    # Stop execution here...
    # sys.exit()
    # Move the above line to different parts of the assignment as you implement more of the functionality.
    # ####################################################################################################


def testWeightsRLShadingCurtainDayStep(hasShadingCurtain, qLearningAgentsShadingCurtain = None, cropElectricityYieldSimulator1=None):

  numTesting = qLearningAgentsShadingCurtain.numTesting

  if hasShadingCurtain:

    # change the exploration rate into zero because in testing, RL does not explore
    qLearningAgentsShadingCurtain.epsilon = 0.0
    # array to store the sales price at each iteration
    plantSalesperSquareMeterList = np.zeros(numTesting)

    for testingIteration in range(0, numTesting):

    # get values necessary for RL training, which was done at
    # hourlyInnerLightIntensityPPFDThroughInnerStructure = cropElectricityYieldSimulator1.getHourlyInnerLightIntensityPPFDThroughInnerStructure()
    # dLIThroughInnerStructure = util.convertFromHourlyPPFDWholeDayToDLI(hourlyInnerLightIntensityPPFDThroughInnerStructure)
    # set dLIThroughInnerStructure to the object
    # qLearningAgentsShadingCurtain.setDLIThroughInnerStructure(dLIThroughInnerStructure)

      print("testingIteration: {}, qLearningAgentsShadingCurtain.weights:{}, datetime.datetime.now():{}, period:{}".format( \
        testingIteration, qLearningAgentsShadingCurtain.weights, datetime.datetime.now(), constant.SimulationStartDate + "-" + constant.SimulationEndDate ))

      # training the q value function
      for day in range(0, util.getSimulationDaysInt()):

        state = day
        #########################################################################
        ############# set values necessary for RL training features##############
        #########################################################################
        # set day to the instance
        qLearningAgentsShadingCurtain.setDay(day)
        # dLIEachdayThroughInnerStructure on a certain day, necessary to cal DLI to PLants
        # qLearningAgentsShadingCurtain.setDLIEachDayThroughInnerStructure(dLIThroughInnerStructure[state])

        # set num of days from Jan 1st.
        daysFromJan1st = util.getNumOfDaysFromJan1st(util.getStartDateDateType() + datetime.timedelta(days=day))
        # date on a certain day
        qLearningAgentsShadingCurtain.setDaysFromJan1st(daysFromJan1st)

        # action = "openCurtain" or "closeCurtain"
        # if the state is at the terminal state, action is None.
        action = qLearningAgentsShadingCurtain.getPolicy(state)
        # store the action at each state at tuples in list for a record.
        qLearningAgentsShadingCurtain.policies[state] = action

        ################## calculate the daily plant yield start#####################

        #### calc the DLI on a certain state
        dLIEachDayThroughInnerStructure = qLearningAgentsShadingCurtain.getDLIThroughInnerStructureElement(state)

        dLIEachDayToPlants = 0.0
        if action == constant.openCurtainString:
          dLIEachDayToPlants = dLIEachDayThroughInnerStructure
        elif action == constant.closeCurtainString:
          dLIEachDayToPlants = dLIEachDayThroughInnerStructure * constant.shadingTransmittanceRatio

        #store the DLI ateach state by list for a record. since the sequence is important, not use a dictionary.
        qLearningAgentsShadingCurtain.dLIEachDayToPlants[day] = dLIEachDayToPlants

        ###### calc plant weight increase with a certain DLI
        # num of days from the latest seeding
        daysFromSeeding = state % constant.cultivationDaysperHarvest

        # if the calc method is A.J Both 2003 model
        if qLearningAgentsShadingCurtain.cropElectricityYieldSimulator1.getPlantGrowthModel() == constant.TaylorExpantionWithFluctuatingDLI:
          # daily [g/unit]
          unitDailyFreshWeightIncreaseElement = \
            Lettuce.calcUnitDailyFreshWeightIncreaseBoth2003Taylor(dLIEachDayToPlants, constant.cultivationDaysperHarvest, daysFromSeeding)
          # update the values to the instance
          qLearningAgentsShadingCurtain.setUnitDailyFreshWeightIncreaseElementShadingCurtain(unitDailyFreshWeightIncreaseElement, state)
          # print ("1 unitDailyFreshWeightIncrease [g/unit]:{}, state:{}".format(unitDailyFreshWeightIncreaseElement, state))

        else:
          print ("[test] error: feasture w_2 not considered. choosing un-existing plant growth model")
        ################## calculate the daily plant yield end#####################

      ################## calculate the total plant sales start#####################
      print ("DLI to plants at each day [mol/m^2/m^2]".format(qLearningAgentsShadingCurtain.dLIEachDayToPlants))

      unitPlantWeight = qLearningAgentsShadingCurtain.getUnitDailyFreshWeightIncreaseListShadingCurtain()
      print ("unitPlantWeight [g/unit]:{}".format(unitPlantWeight))
      totalUnitPlantWeight = sum(unitPlantWeight)


      # unit conversion; get the daily plant yield per given period per area: [g/unit] -> [g/m^2]
      unitPlantWeightperArea = util.convertUnitShootFreshMassToShootFreshMassperArea(unitPlantWeight)
      # unit conversion:  [g/m^2] -> [kg/m^2]1
      unitPlantWeightperAreaKg = util.convertFromgramTokilogram(unitPlantWeightperArea)
      # get the sales price of plant [USD/m^2]
      # if the average DLI during each harvest term is more than 17 mol/m^2/day, discount the price
      # TODO may need to improve the affect of Tipburn
      dailyPlantSalesperSquareMeter = getPlantSalesperSquareMeter(\
        cropElectricityYieldSimulator1.getYear(), unitPlantWeightperAreaKg, qLearningAgentsShadingCurtain.dLIEachDayToPlants)
      plantSalesperSquareMeter = sum(dailyPlantSalesperSquareMeter)
      plantSalesperSquareMeterList[testingIteration] = plantSalesperSquareMeter
      # print "dailyPlantSalesperSquareMeter.shape:{}".format(dailyPlantSalesperSquareMeter.shape)

      print ("plantSalesperSquareMeterList[{}]:{}".format(testingIteration, plantSalesperSquareMeterList))

      ################## calculate the total plant sakes end#####################

  else:
    print ("shading curtain assumed not to be given. the function without shading curtain will be made in the future")

  # return the average of testing results
  return plantSalesperSquareMeter


def getWholeElectricityYieldEachOPVRatio(OPVAreaCoverageRatio, dailyJopvout, cropElectricityYieldSimulator1, greenhouseRoofArea = None):
    '''
    return the total electricity yield for a given period by the given OPV area(OPVAreaCoverageRatio * constant.greenhouseRoofArea)
    :param OPVAreaCoverageRatio: [-] proportionOPVAreaCoverageRatio
    :param dailyJopvout: [J/m^2] per day
    :return: dailyJopvout [J/m^2] by whole OPV area
    '''

    # get the OPV coverage ratio changing during the fallow period
    unfixedOPVCoverageRatio = OPVFilm.getDifferentOPVCoverageRatioInFallowPeriod(OPVAreaCoverageRatio, cropElectricityYieldSimulator1)
    # change the num of list from hourly data (365 * 24) to daily data (365)
    unfixedOPVCoverageRatio = unfixedOPVCoverageRatio[::24]

    if greenhouseRoofArea is None:
      return sum(dailyJopvout * unfixedOPVCoverageRatio * constant.greenhouseRoofArea)
    else:
      return sum(dailyJopvout * unfixedOPVCoverageRatio * greenhouseRoofArea)
    # # print "dailyJopvout:{}".format(dailyJopvout)
    # totalJopvout = sum(dailyJopvout)
    # if greenhouseRoofArea is None:
    #     return totalJopvout * unfixedOPVCoverageRatio * constant.greenhouseRoofArea
    # else:
    #     return totalJopvout * unfixedOPVCoverageRatio * greenhouseRoofArea


def getDailyElectricitySalesperArea():
    # todo do later if necessary
    return 0

def getMonthlyElectricitySalesperArea(dailyJopvoutperArea, yearOfeachDay, monthOfeachDay):
    '''

    :param dailyJopvoutperArea:
    :param yearOfeachDay:
    :param monthOfeachDay:
    :return:
    '''
    monthlyElectricityYieldperArea = OPVFilm.getMonthlyElectricityProductionFromDailyData(dailyJopvoutperArea, yearOfeachDay, monthOfeachDay)
    # print "monthlyElectricityYieldperArea:{}".format(monthlyElectricityYieldperArea)

    # import the electricity sales price file
    fileName = "electricityPurchasePriceData.csv"
    # import the file removing the header
    fileData = util.readData(fileName, relativePath="", skip_header=1, d='\t')
    # print "fileData:{}".format(fileData)

    # print "monthlyElectricityYieldperArea.shape[0]:{}".format(monthlyElectricityYieldperArea.shape[0])
    year = np.zeros(monthlyElectricityYieldperArea.shape[0])
    month = np.zeros(monthlyElectricityYieldperArea.shape[0])
    monthlyResidentialElectricityPrice = np.zeros(monthlyElectricityYieldperArea.shape[0])

    index = 0
    for monthlyData in fileData:
        # exclude the data out of the set start month and end month
        if datetime.date(int(monthlyData[0]), int(monthlyData[1]), 1) + relativedelta(months=1) <= util.getStartDateDateType() or \
                datetime.date(int(monthlyData[0]), int(monthlyData[1]), 1) > util.getEndDateDateType():
            continue
        year[index] = monthlyData[0]
        month[index] = monthlyData[1]
        monthlyResidentialElectricityPrice[index] = monthlyData[2]
        # print "monthlyData:{}".format(monthlyData)
        index += 1

    # unit exchange: [J/m^2] -> [wh/m^2]
    monthlyWhopvoutperArea =util.convertFromJouleToWattHour(monthlyElectricityYieldperArea)
    # unit exchange: [wh/m^2] -> [kwh/m^2]
    monthlyKWhopvoutperArea =util.convertWhTokWh(monthlyWhopvoutperArea)
    # [USD/month/m^2]
    monthlyElectricitySalesperArea = OPVFilm.getMonthlyElectricitySalesperArea(monthlyKWhopvoutperArea, monthlyResidentialElectricityPrice)
    # print "monthlyElectricitySalesperArea:{}".format(monthlyElectricitySalesperArea)

    return monthlyElectricitySalesperArea


def getMonthlyElectricitySales(OPVCoverage, monthlyElectricitySalesperArea, greenhouseRoofArea = None):
    '''
    return the monthly electricity saled given a cetain OPV coverage ratio

    :param OPVCoverageList:
    :param monthlyElectricitySalesperArea:
    :return:
    '''
    if greenhouseRoofArea is None:
        return monthlyElectricitySalesperArea * OPVCoverage * constant.greenhouseRoofArea
    else:
        return monthlyElectricitySalesperArea * OPVCoverage * greenhouseRoofArea

def getElectricitySalesperAreaEachOPVRatio():
    return 0

def getElectricityCostperArea():
    return 0


def getResourseUseEfficiency():
    # TODO do later
    return 0


def getPlantSalesperSquareMeter(year, dailyHarvestedFreshWeightListperAreaKg, TotalDLItoPlants):
    """
    return the sales price of lettuce per square meter
    :return:
    """
    # print "dailyHarvestedFreshWeightListperAreaKg:{}".format(dailyHarvestedFreshWeightListperAreaKg)
    # print "dailyHarvestedFreshWeightListperAreaKg.shape:{}".format(dailyHarvestedFreshWeightListperAreaKg.shape)

    # the price of lettuce per hundredweight [cwt]
    priceperCwtEachHour = Lettuce.getLettucePricepercwt(year)

    priceperKgEachHour = priceperCwtEachHour / constant.kgpercwt * constant.plantPriceDiscountRatio_justForSimulation
    # print "harvestedFreshWeightListperAreaKg:{}".format(harvestedFreshWeightListperAreaKg)
    # print "dailyHarvestedFreshWeightListperAreaKg.shape:{}".format(dailyHarvestedFreshWeightListperAreaKg.shape)
    # print "priceperKg:{}".format(priceperKg)

    # convert the price each hour to the price each day
    priceperKgEachDay = priceperKgEachHour[::24]
    # print "priceperKgEachDay:{}".format(priceperKgEachDay)
    # print "priceperKgEachDay.shape:{}".format(priceperKgEachDay.shape)

    plantSalesperSquareMeter = dailyHarvestedFreshWeightListperAreaKg * priceperKgEachDay
    # print "plantSalesperSquareMeter:{}".format(plantSalesperSquareMeter)
    # Tipburn discount
    # TODO: will need to refine more
    plantSalesperSquareMeterTipburnDiscount = Lettuce.discountPlantSalesperSquareMeterByTipburn(plantSalesperSquareMeter, TotalDLItoPlants)

    return plantSalesperSquareMeterTipburnDiscount

def getPlantCostperSquareMeter(simulationDays):
    '''
    calculate the cost for plant cultivation for given period
    :param year:
    :return:
    '''
    # [USD/m^2]
    return constant.plantcostperSquaremeterperYear * simulationDays / constant.dayperYear

################################################# old code below################################

def calcOptimizedOPVAreaMaximizingtotalEconomicProfit(OPVAreaVector, totalEconomicProfitperYearVector):
    '''
    determine the best OPVArea maximizing the economic profit
    param:
        OPVAreaVector
        totalEconomicProfitperYearVector
    return:
        none
    '''
    maxtotalEconomicProfitperYear = np.max(totalEconomicProfitperYearVector)
    bestOPVArea = OPVAreaVector[np.argmax(totalEconomicProfitperYearVector)]
    print "The OPV area maximizing the economic profit is {}m^2 the max economic profit is {}USD/year ".format(bestOPVArea, maxtotalEconomicProfitperYear)
