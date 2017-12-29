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
#import Lettuce
import CropElectricityYeildSimulatorDetail as simulatorDetail
import QlearningAgentShadingCurtain as QRLshadingCurtain
import SimulatorClass as SimulatorClass
#######################################################

def simulateCropElectricityYieldProfitRLShadingCurtain():
  '''

  :return:
  '''
  print ("start modeling: datetime.datetime.now():{}".format(datetime.datetime.now()))

  # declare the class
  cropElectricityYieldSimulator1 = SimulatorClass.CropElectricityYieldSimulator1()

  ##########file import (TucsonHourlyOuterEinvironmentData) start##########
  fileName = "20130101-20170101" + ".csv"
  year, \
  month, \
  day, \
  hour, \
  hourlyHorizontalDiffuseOuterSolarIrradiance, \
  hourlyHorizontalTotalOuterSolarIrradiance,  \
  hourlyHorizontalDirectOuterSolarIrradiance, \
  hourlyHorizontalTotalBeamMeterBodyTemperature, \
  hourlyAirTemperature, cropElectricityYieldSimulator1 = util.getArraysFromData(fileName, cropElectricityYieldSimulator1)
  ##########file import (TucsonHourlyOuterEinvironmentData) end##########

  # set the values to the object
  cropElectricityYieldSimulator1.setYear(year)
  cropElectricityYieldSimulator1.setMonth(month)
  cropElectricityYieldSimulator1.setDay(day)
  cropElectricityYieldSimulator1.setHour(hour)

  ##########solar irradiance to OPV calculation start##########
  # calculate with real data
  # hourly average [W m^-2]
  directSolarRadiationToOPVEastDirection, directSolarRadiationToOPVWestDirection, diffuseSolarRadiationToOPV, albedoSolarRadiationToOPV = \
    simulatorDetail.calcOPVmoduleSolarIrradianceGHRoof(year, month, day, hour, hourlyHorizontalDiffuseOuterSolarIrradiance, \
                                                       hourlyHorizontalDirectOuterSolarIrradiance, "EastWestDirectionRoof")
  # [W m^-2] per hour
  totalSolarRadiationToOPV = (directSolarRadiationToOPVEastDirection + directSolarRadiationToOPVWestDirection) / 2.0 + diffuseSolarRadiationToOPV + albedoSolarRadiationToOPV

  # # calculate without real data.
  # simulatedDirectSolarRadiationToOPVEastDirection, \
  # simulatedDirectSolarRadiationToOPVWestDirection, \
  # simulatedDiffuseSolarRadiationToOPV, \
  # simulatedAlbedoSolarRadiationToOPV = simulatorDetail.calcOPVmoduleSolarIrradianceGHRoof(year, month, day, hour)
  # # [W m^-2] per hour
  # simulatedTotalSolarRadiationToOPV = simulatedDirectSolarRadiationToOPVEastDirection + simulatedDirectSolarRadiationToOPVWestDirection + \
  #                                     simulatedDiffuseSolarRadiationToOPV + simulatedAlbedoSolarRadiationToOPV
  # print "directSolarRadiationToOPV:{}".format(directSolarRadiationToOPV)
  # print "diffuseSolarRadiationToOPV:{}".format(diffuseSolarRadiationToOPV)
  # print "groundReflectedSolarradiationToOPV:{}".format(groundReflectedSolarradiationToOPV)

  # unit change: [W m^-2] -> [umol m^-2 s^-1] == PPFD
  directPPFDToOPVEastDirection = util.convertFromWattperSecSquareMeterToPPFD(directSolarRadiationToOPVEastDirection)
  directPPFDToOPVWestDirection = util.convertFromWattperSecSquareMeterToPPFD(directSolarRadiationToOPVWestDirection)
  diffusePPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(diffuseSolarRadiationToOPV)
  groundReflectedPPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(albedoSolarRadiationToOPV)
  totalPPFDToOPV = directPPFDToOPVEastDirection + directPPFDToOPVWestDirection + diffusePPFDToOPV + groundReflectedPPFDToOPV
  # print"diffusePPFDToOPV.shape:{}".format(diffusePPFDToOPV.shape)
  ########## set the matrix to the object ###########
  cropElectricityYieldSimulator1.setDirectPPFDToOPVEastDirection(directPPFDToOPVEastDirection)
  cropElectricityYieldSimulator1.setDirectPPFDToOPVWestDirection(directPPFDToOPVWestDirection)
  cropElectricityYieldSimulator1.setDiffusePPFDToOPV(diffusePPFDToOPV)
  cropElectricityYieldSimulator1.setGroundReflectedPPFDToOPV(groundReflectedPPFDToOPV)
  ###################################################

  # unit change: hourly [umol m^-2 s^-1] -> [mol m^-2 day^-1] == DLI :number of photons received in a square meter per day
  directDLIToOPVEastDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVEastDirection)
  directDLIToOPVWestDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVWestDirection)
  diffuseDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(diffusePPFDToOPV)
  groundReflectedDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(groundReflectedPPFDToOPV)
  totalDLIToOPV = directDLIToOPVEastDirection + directDLIToOPVWestDirection + diffuseDLIToOPV + groundReflectedDLIToOPV
  # print "directDLIToOPVEastDirection:{}".format(directDLIToOPVEastDirection)
  # print "diffuseDLIToOPV.shape:{}".format(diffuseDLIToOPV.shape)
  # print "groundReflectedDLIToOPV:{}".format(groundReflectedDLIToOPV)
  ########## set the matrix to the object ##########
  cropElectricityYieldSimulator1.setDirectDLIToOPVEastDirection(directDLIToOPVEastDirection)
  cropElectricityYieldSimulator1.setDirectDLIToOPVWestDirection(directDLIToOPVWestDirection)
  cropElectricityYieldSimulator1.setDiffuseDLIToOPV(diffuseDLIToOPV)
  cropElectricityYieldSimulator1.setGroundReflectedDLIToOPV(groundReflectedDLIToOPV)
  ##################################################

  # ################## plot the difference of real data and simulated data start######################
  # Title = "difference of the model output with real data and with no data"
  # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "total Solar irradiance [W m^-2]"
  # util.plotTwoData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), \
  #                  totalSolarRadiationToOPV, simulatedTotalSolarRadiationToOPV ,Title, xAxisLabel, yAxisLabel, "with real data", "wth no data")
  # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # ################## plot the difference of real data and simulated data end######################

  # ################## plot the distribution of direct and diffuse PPFD start######################
  # Title = "TOTAL outer PPFD to OPV"
  # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "PPFD [umol m^-2 s^-1]"
  # util.plotData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), \
  #               directPPFDToOPV + diffusePPFDToOPV + groundReflectedPPFDToOPV, Title, xAxisLabel, yAxisLabel)
  # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # ################## plot the distribution of direct and diffuse PPFD end######################

  # ################## plot the distribution of direct and diffuse solar DLI start######################
  # Title = "direct and diffuse outer DLI to OPV"
  # xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "DLI [mol m^-2 day^-1]"
  # y1Label = "(directDLIToOPVEastDirection+directDLIToOPVWestDirection)/2.0"
  # y2Label = "diffuseDLIToOPV"
  # util.plotTwoData(np.linspace(0, simulationDaysInt, simulationDaysInt), (directDLIToOPVEastDirection+directDLIToOPVWestDirection)/2.0, diffuseDLIToOPV, Title,
  #                  xAxisLabel, yAxisLabel, y1Label, y2Label)
  # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # ################## plot the distribution of direct and diffuse solar DLI end######################

  # ################## plot the distribution of various DLI to OPV film start######################
  # Title = "various DLI to OPV film"
  # plotDataSet = np.array([directDLIToOPVEastDirection, directDLIToOPVWestDirection, diffuseDLIToOPV,
  #                         groundReflectedDLIToOPV])
  # labelList = np.array(["directDLIToOPVEastDirection", "directDLIToOPVWestDirection", "diffuseDLIToOPV",
  #                       "groundReflectedDLIToOPV"])
  # xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "DLI [mol m^-2 day^-1]"
  # util.plotMultipleData(np.linspace(0, simulationDaysInt, simulationDaysInt), plotDataSet, labelList, Title,
  #                       xAxisLabel, yAxisLabel)
  # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # ################## plot the distribution of various DLI to OPV film end######################

  ################## calculate the daily electricity yield per area start#####################
  # TODO maybe we need to consider the tilt of OPV and OPV material for the temperature of OPV film. right now, just use the measured temperature
  # get the daily electricity yield per area per day ([J/m^2] per day) based on the given light intensity ([Celsius],[W/m^2]).
  dailyJopvoutperArea = simulatorDetail.calcDailyElectricityYieldSimulationperArea(hourlyHorizontalTotalBeamMeterBodyTemperature, \
                                                                                   directSolarRadiationToOPVEastDirection + directSolarRadiationToOPVWestDirection,
                                                                                   diffuseSolarRadiationToOPV,
                                                                                   albedoSolarRadiationToOPV)

  # unit Exchange [J/m^2] -> [wh / m^2]
  dailyWhopvoutperArea = util.convertFromJouleToWattHour(dailyJopvoutperArea)
  # unit Exchange [Wh/ m^2] -> [kWh/m^2]
  dailykWhopvoutperArea = util.convertWhTokWh(dailyWhopvoutperArea)
  # ################### plot the electricity yield per area with given OPV film
  # title = "electricity yield per area vs OPV film"
  # xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "Electricity yield per OPV area [kWh/m^2/day]"
  # util.plotData(np.linspace(0, simulationDaysInt, simulationDaysInt), dailykWhopvoutperArea, title, xAxisLabel, yAxisLabel)
  # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  ################### calculate the daily electricity yield per area end#####################

  ################## calculate the daily electricity sales start#####################
  # convert the year of each hour to the year to each day
  yearOfeachDay = year[::24]
  # convert the month of each hour to the month to each day
  monthOfeachDay = month[::24]
  # get the monthly electricity sales per area [USD/month/m^2]
  monthlyElectricitySalesperArea = simulatorDetail.getMonthlyElectricitySalesperArea(dailyJopvoutperArea, yearOfeachDay, monthOfeachDay)
  # set the value to the object
  cropElectricityYieldSimulator1.setMonthlyElectricitySalesperArea(monthlyElectricitySalesperArea)
  # print "cropElectricityYieldSimulator1.getMonthlyElectricitySalesperArea():{}".format(cropElectricityYieldSimulator1.getMonthlyElectricitySalesperArea())
  ################## calculate the daily electricity sales end#####################

  ##################calculate the electricity cost per area start######################################
  if constant.ifConsiderOPVCost is True:
      initialOPVCostUSD = constant.OPVPricePerAreaUSD * OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio)
      # [USD]
      OPVCostUSDForDepreciation = initialOPVCostUSD * (util.getSimulationDaysInt() / constant.OPVDepreciationPeriodDays)
      # set the value to the object
      cropElectricityYieldSimulator1.setOPVCostUSDForDepreciationperArea(
          OPVCostUSDForDepreciation / OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio))
  else:
      # set the value to the object. the value is zero if not consider the purchase cost
      cropElectricityYieldSimulator1.setOPVCostUSDForDepreciationperArea(0.0)
  ##################calculate the electricity cost per area end######################################

  ################## calculate the daily plant yield start#####################
  # [String]
  plantGrowthModel = constant.TaylorExpantionWithFluctuatingDLI
  # cultivation days per harvest [days/harvest]
  cultivationDaysperHarvest = constant.cultivationDaysperHarvest
  # OPV coverage ratio [-]
  OPVCoverage = constant.OPVAreaCoverageRatio
  # boolean
  hasShadingCurtain = constant.hasShadingCurtain
  # PPFD [umol m^-2 s^-1]
  ShadingCurtainDeployPPFD = constant.ShadingCurtainDeployPPFD

  # calculate plant yield given an OPV coverage and model :daily [g/unit]. the shading curtain influence is considered in this function.
  shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitDailyHarvestedFreshWeight = \
  simulatorDetail.calcPlantYieldSimulation(plantGrowthModel, cultivationDaysperHarvest, OPVCoverage, \
                                            (directPPFDToOPVEastDirection + directPPFDToOPVWestDirection) / 2.0, diffusePPFDToOPV, groundReflectedPPFDToOPV,
                                            hasShadingCurtain, ShadingCurtainDeployPPFD, cropElectricityYieldSimulator1)
  # set the values to the instance
  cropElectricityYieldSimulator1.setShootFreshMassList(shootFreshMassList)
  cropElectricityYieldSimulator1.setUnitDailyFreshWeightIncrease(unitDailyFreshWeightIncrease)
  cropElectricityYieldSimulator1.setAccumulatedUnitDailyFreshWeightIncrease(accumulatedUnitDailyFreshWeightIncrease)
  cropElectricityYieldSimulator1.setUnitDailyHarvestedFreshWeight(unitDailyHarvestedFreshWeight)

  # the DLI to plants [mol/m^2/day]
  TotalDLItoPlants = simulatorDetail.getTotalDLIToPlants(OPVCoverage, (directPPFDToOPVEastDirection + directPPFDToOPVWestDirection) / 2.0, diffusePPFDToOPV,
                                                         groundReflectedPPFDToOPV, \
                                                         hasShadingCurtain, ShadingCurtainDeployPPFD, cropElectricityYieldSimulator1)
  # set the value to the instance
  cropElectricityYieldSimulator1.setTotalDLItoPlantsBaselineShadingCuratin(TotalDLItoPlants)

  # print "TotalDLItoPlants:{}".format(TotalDLItoPlants)
  # print "TotalDLItoPlants.shape:{}".format(TotalDLItoPlants.shape)

  # ######################### plot a graph showing only shootFreshMassList per unit
  # title = "plant yield per head vs time (OPV coverage " + str(int(100 * OPVCoverage)) + "%)"
  # xAxisLabel = "time [day]:  " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "plant fresh weight[g/head]"
  # util.plotData(np.linspace(0, util.getSimulationDaysInt(), util.getSimulationDaysInt()), shootFreshMassList, title, xAxisLabel, yAxisLabel)
  # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # #######################################################################

  # # unit conversion; get the plant yield per day per area: [g/unit] -> [g/m^2]
  # shootFreshMassListperArea = util.convertUnitShootFreshMassToShootFreshMassperArea(shootFreshMassList)
  # # unit conversion:  [g/m^2] -> [kg/m^2]
  # shootFreshMassListperAreaKg = util.convertFromgramTokilogram(shootFreshMassListperArea)
  # ######################## plot a graph showing only shootFreshMassList per square meter
  # title = "plant yield per area vs time (OPV coverage " + str(int(100 * OPVCoverage)) + "%)"
  # xAxisLabel = "time [day]:  " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "plant fresh weight[kg/m^2]"
  # util.plotData(np.linspace(0, util.getSimulationDaysInt(), util.getSimulationDaysInt()), shootFreshMassListperAreaKg, title, xAxisLabel, yAxisLabel)
  # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # ######################################################################

  ################## plot various unit Plant Yield vs time
  plotDataSet = np.array([shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitDailyHarvestedFreshWeight])
  labelList = np.array(["shootFreshMassList", "unitDailyFreshWeightIncrease", "accumulatedUnitDailyFreshWeightIncrease", "unitDailyHarvestedFreshWeight"])
  title = "Various unit Plant Yield vs time (OPV coverage " + str(int(100 * OPVCoverage)) + "%)"
  xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "Unit plant Fresh Weight [g/unit]"
  util.plotMultipleData(np.linspace(0, util.getSimulationDaysInt(), util.getSimulationDaysInt()), plotDataSet, labelList, title, xAxisLabel, yAxisLabel)
  util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  ###########################################################################
  ################## calculate the daily plant yield end#####################

  ################## calculate the daily plant sales start#####################
  # unit conversion; get the daily plant yield per given period per area: [g/unit] -> [g/m^2]
  dailyHarvestedFreshWeightperArea = util.convertUnitShootFreshMassToShootFreshMassperArea(unitDailyHarvestedFreshWeight)
  # unit conversion:  [g/m^2] -> [kg/m^2]1
  dailyHarvestedFreshWeightperAreaKg = util.convertFromgramTokilogram(dailyHarvestedFreshWeightperArea)
  # get the sales price of plant [USD/m^2]
  # if the average DLI during each harvest term is more than 17 mol/m^2/day, discount the price
  # TODO may need to improve the affect of Tipburn
  dailyPlantSalesperSquareMeter = simulatorDetail.getPlantSalesperSquareMeter(year, dailyHarvestedFreshWeightperAreaKg, TotalDLItoPlants)

  plantSalesperSquareMeter = sum(dailyPlantSalesperSquareMeter)
  # print "dailyPlantSalesperSquareMeter.shape:{}".format(dailyPlantSalesperSquareMeter.shape)

  print ("(The baseline) plantSalesperSquareMeter [USD/m^2]:{}".format(plantSalesperSquareMeter))
  ################## calculate the daily plant sales end#####################


  ################## calculate the daily plant cost start#####################
  # plant operation cost per square meter for given simulation period [USD/m^2]
  plantCostperSquareMeter = simulatorDetail.getPlantCostperSquareMeter(util.getSimulationDaysInt())
  ################## calculate the daily plant cost end#####################

  ################## calculate the plant profit start#######################
  ###### calculate the plant profit per square meter [USD/m^2]
  plantProfitperSquareMeter = plantSalesperSquareMeter - plantCostperSquareMeter
  # print "plantProfitperSquareMeterList[i]:{}".format(plantProfitperSquareMeterList[i])
  # print "plantProfitperSquareMeterList[{}]:{}".format(i, plantProfitperSquareMeterList[i])
  plantProfit = plantProfitperSquareMeter * constant.greenhouseCultivationFloorArea

  # print "plantCostperSquareMeter:{}".format(plantCostperSquareMeter)
  # print "unitDailyHarvestedFreshWeightList:{}".format(unitDailyHarvestedFreshWeightList)
  # print "plantSalesperSquareMeterList:{}".format(plantSalesperSquareMeterList)

  print ("(The baseline) plantProfit by normal simulation [USD]:{}".format(plantProfit))
  ################## calculate the plant profit end#######################

  #####################################################################################################
  ################## reinforcement learning plant simulation start#####################################
  #####################################################################################################

  ################## calculate the  plant sales with RL shading curtain start##########################
  if constant.isShadingCurtainReinforcementLearning:

    # declare the instance for RL
    # qLearningAgentsShadingCurtain = QRLshadingCurtain.QLearningAgentShadingCurtain(cropElectricityYieldSimulator1, \
    #                                                                                numTraining=1500, numTesting = 1, epsilon=0.18, gamma=0.999, alpha=0.2e-6)
    qLearningAgentsShadingCurtain = QRLshadingCurtain.QLearningAgentShadingCurtain(cropElectricityYieldSimulator1, \
                                                                                   numTraining=1200, numTesting = 1, epsilon=0.18, gamma=0.99, alpha=0.2e-6)


    # set values necessary for RL training/testing
    # for dLIEachdayThroughInnerStructure on a certain day
    hourlyInnerLightIntensityPPFDThroughInnerStructure = simulatorClass.getHourlyInnerLightIntensityPPFDThroughInnerStructure()
    # set dLIThroughInnerStructure to the object
    dLIThroughInnerStructure = util.convertFromHourlyPPFDWholeDayToDLI(hourlyInnerLightIntensityPPFDThroughInnerStructure)
    qLearningAgentsShadingCurtain.setDLIThroughInnerStructure(dLIThroughInnerStructure)

    ################################ Training #################################
    if constant.ifRunTraining:
      #training the approximate q value function. returns the wegiths of q value function
      qLearningAgentsShadingCurtain = simulatorDetail.trainWeightsRLShadingCurtainDayStep(hasShadingCurtain, qLearningAgentsShadingCurtain, simulatorClass)
    # print ("qLearningAgentsShadingCurtain.weights:{}".format(qLearningAgentsShadingCurtain.weights))

    ################################ Save the trained weight #################################
    # save the calculated weight by the training
    if constant.ifSaveCalculatedWeight:
      util.exportDictionaryAsCSVFile(qLearningAgentsShadingCurtain.weights, constant.fileNameQLearningTrainedWeight)

    # load the calculated weight by the training
    if constant.ifLoadWeight:
      qLearningAgentsShadingCurtain.weights = util.importDictionaryAsCSVFile(constant.fileNameQLearningTrainedWeight, relativePath="")
      print ("loaded qLearningAgentsShadingCurtain.weights:{}".format(qLearningAgentsShadingCurtain.weights))

    ################################ Testing ##################################
    # with the trained q value function,
    plantSalesperSquareMeterRLShadingCurtainList = simulatorDetail.testWeightsRLShadingCurtainDayStep(hasShadingCurtain, \
                                                                                                  qLearningAgentsShadingCurtain, simulatorClass)

    print ("(RL) plantSalesperSquareMeterRLShadingCurtain [USD/m^2]:{}".format(plantSalesperSquareMeterRLShadingCurtainList))

    ################## calculate the plant cost start#####################
    # plant operation cost per square meter for given simulation period [USD/m^2]
    # plantCostperSquareMeter = simulatorDetail.getPlantCostperSquareMeter(simulationDaysInt)
    ################## calculate the plant cost end#####################

    ################## calculate the plant economic profit start#######################
    ###### calculate the plant profit per square meter [USD/m^2]
    plantProfitperSquareMeterRLShadingCurtainList = plantSalesperSquareMeterRLShadingCurtainList - plantCostperSquareMeter
    # print "plantProfitperSquareMeterList[i]:{}".format(plantProfitperSquareMeterList[i])
    # print "plantProfitperSquareMeterList[{}]:{}".format(i, plantProfitperSquareMeterList[i])
    plantProfitRLShadingCurtainList = plantProfitperSquareMeterRLShadingCurtainList * constant.greenhouseCultivationFloorArea

    print ("(RL) plantProfitRLShadingCurtainList [USD]:{}".format(plantProfitRLShadingCurtainList))

    # set the result of profits
    qLearningAgentsShadingCurtain.plantProfitRLShadingCurtainList = plantProfitRLShadingCurtainList
    ################## calculate the plant economic profit end#######################

  else:
    print ("reinforcement learning shading curtain waa not assumed. skip the simulation")

  #####################################################################################################
  ################## reinforcement learning plant simulation end#####################################
  #####################################################################################################

  print ("end modeling: datetime.datetime.now():{}".format(datetime.datetime.now()))

  # print actions
  print ("qLearningAgentsShadingCurtain.policies:{}".format(qLearningAgentsShadingCurtain.policies))
  # print DLI to plants
  print ("qLearningAgentsShadingCurtain.dLIEachDayToPlants:{}".format(qLearningAgentsShadingCurtain.dLIEachDayToPlants))



  return simulatorClass, qLearningAgentsShadingCurtain

  # ####################################################################################################
  # Stop execution here...
  # sys.exit()
  # Move the above line to different parts of the assignment as you implement more of the functionality.
  # ####################################################################################################