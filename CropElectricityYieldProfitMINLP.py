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

def simulateCropElectricityYieldProfitForMINLP():
  '''
  1st simulator of crop and electricity yield and their profit
  :return: profitVSOPVCoverageData
  '''

  print ("start modeling: datetime.datetime.now():{}".format(datetime.datetime.now()))

  # declare the class
  simulatorClass = SimulatorClass.SimulatorClass()

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
  hourlyAirTemperature, simulatorClass = util.getArraysFromData(fileName, simulatorClass)
  ##########file import (TucsonHourlyOuterEinvironmentData) end##########

  # set the values to the object
  simulatorClass.setYear(year)
  simulatorClass.setMonth(month)
  simulatorClass.setDay(day)
  simulatorClass.setHour(hour)
  ##########file import (TucsonHourlyOuterEinvironmentData) end##########


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
  # set the matrix to the object
  simulatorClass.setDirectPPFDToOPVEastDirection(directPPFDToOPVEastDirection)
  simulatorClass.setDirectPPFDToOPVWestDirection(directPPFDToOPVWestDirection)
  simulatorClass.setDiffusePPFDToOPV(diffusePPFDToOPV)
  simulatorClass.setGroundReflectedPPFDToOPV(groundReflectedPPFDToOPV)

  # unit change: hourly [umol m^-2 s^-1] -> [mol m^-2 day^-1] == DLI :number of photons received in a square meter per day
  directDLIToOPVEastDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVEastDirection)
  directDLIToOPVWestDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVWestDirection)
  diffuseDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(diffusePPFDToOPV)
  groundReflectedDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(groundReflectedPPFDToOPV)
  totalDLIToOPV = directDLIToOPVEastDirection + directDLIToOPVWestDirection + diffuseDLIToOPV + groundReflectedDLIToOPV
  # print "directDLIToOPVEastDirection:{}".format(directDLIToOPVEastDirection)
  # print "diffuseDLIToOPV.shape:{}".format(diffuseDLIToOPV.shape)
  # print "groundReflectedDLIToOPV:{}".format(groundReflectedDLIToOPV)


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
  # ################## calculate the daily electricity yield per area end#####################

  ################## calculate the daily electricity sales start#####################
  # convert the year of each hour to the year to each day
  yearOfeachDay = year[::24]
  # convert the month of each hour to the month to each day
  monthOfeachDay = month[::24]
  # get the monthly electricity sales per area [USD/month/m^2]
  monthlyElectricitySalesperArea = simulatorDetail.getMonthlyElectricitySalesperArea(dailyJopvoutperArea, yearOfeachDay, monthOfeachDay)
  # set the value to the object
  simulatorClass.setMonthlyElectricitySalesperArea(monthlyElectricitySalesperArea)
  # print "simulatorClass.getMonthlyElectricitySalesperArea():{}".format(simulatorClass.getMonthlyElectricitySalesperArea())
  ################## calculate the daily electricity sales end#####################

  ##################calculate the electricity cost per area start######################################
  # initialOPVCostUSD = constant.OPVPricePerAreaUSD * OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio)
  # # [USD]
  # OPVCostUSDForDepreciation = initialOPVCostUSD * (simulationDaysInt / constant.OPVDepreciationPeriodDays)
  # # set the value to the object
  # simulatorClass.setOPVCostUSDForDepreciationperArea(OPVCostUSDForDepreciation / OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio))
  if constant.ifConsiderOPVCost is True:
      initialOPVCostUSD = constant.OPVPricePerAreaUSD * OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio)
      # [USD]
      OPVCostUSDForDepreciation = initialOPVCostUSD * (util.getSimulationDaysInt() / constant.OPVDepreciationPeriodDays)
      # set the value to the object
      simulatorClass.setOPVCostUSDForDepreciationperArea(
          OPVCostUSDForDepreciation / OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio))
  else:
      # set the value to the object. the value is zero if not consider the purchase cost
      simulatorClass.setOPVCostUSDForDepreciationperArea(0.0)
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

  # calculate plant yield given an OPV coverage and model :daily [g/unit]
  shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitDailyHarvestedFreshWeight = \
    simulatorDetail.calcPlantYieldSimulation(plantGrowthModel, cultivationDaysperHarvest, OPVCoverage, \
                                             (directPPFDToOPVEastDirection + directPPFDToOPVWestDirection) / 2.0, diffusePPFDToOPV, groundReflectedPPFDToOPV,
                                             hasShadingCurtain, ShadingCurtainDeployPPFD, simulatorClass)

  # the DLI to plants [mol/m^2/day]
  TotalDLItoPlants = simulatorDetail.getTotalDLIToPlants(OPVCoverage, (directPPFDToOPVEastDirection + directPPFDToOPVWestDirection) / 2.0, diffusePPFDToOPV,
                                                         groundReflectedPPFDToOPV, \
                                                         hasShadingCurtain, ShadingCurtainDeployPPFD, simulatorClass)
  # print "TotalDLItoPlants:{}".format(TotalDLItoPlants)
  # print "TotalDLItoPlants.shape:{}".format(TotalDLItoPlants.shape)
  # set the value to the instance
  simulatorClass.setTotalDLItoPlantsBaselineShadingCuratin(TotalDLItoPlants)

  # ######################### plot a graph showing only shootFreshMassList per unit
  # title = "plant yield per head vs time (OPV coverage " + str(int(100 * OPVCoverage)) + "%)"
  # xAxisLabel = "time [day]:  " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "plant fresh weight[g/head]"
  # util.plotData(np.linspace(0, simulationDaysInt, simulationDaysInt), shootFreshMassList, title, xAxisLabel, yAxisLabel)
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
  # util.plotData(np.linspace(0, simulationDaysInt, simulationDaysInt), shootFreshMassListperAreaKg, title, xAxisLabel, yAxisLabel)
  # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # ######################################################################

  # ################## plot various unit Plant Yield vs time
  # plotDataSet = np.array([shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitDailyHarvestedFreshWeight])
  # labelList = np.array(["shootFreshMassList", "unitDailyFreshWeightIncrease", "accumulatedUnitDailyFreshWeightIncrease", "unitDailyHarvestedFreshWeight"])
  # title = "Various unit Plant Yield vs time (OPV coverage " + str(int(100 * OPVCoverage)) + "%)"
  # xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  # yAxisLabel = "Unit plant Fresh Weight [g/unit]"
  # util.plotMultipleData(np.linspace(0, simulationDaysInt, simulationDaysInt), plotDataSet, labelList, title, xAxisLabel, yAxisLabel)
  # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # #######################################################################

  ################## calculate the daily plant yield end#####################


  ################## calculate the daily plant sales start#####################

  ################## calculate the daily plant sales end#####################


  ################## calculate the daily plant cost start#####################

  ################## calculate the daily plant cost end#####################


  print ("end modeling: datetime.datetime.now():{}".format(datetime.datetime.now()))

  return simulatorClass


