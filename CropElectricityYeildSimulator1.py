# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 12 Dec 2016
# last edit date: 14 Dec 2016
#######################################################

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
import SimulatorClass
#######################################################


def simulateCropElectricityYieldProfit1():
    '''
    1st simulator of crop and electricity yield and their profit
    :return: profitVSOPVCoverageData
    '''

    print ("start modeling: datetime.datetime.now():{}".format(datetime.datetime.now()))

    # get the num of simulation days
    simulationDaysInt = util.getSimulationDaysInt()

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
    hourlyAirTemperature = util.getArraysFromData(fileName, simulatorClass)
    ##########file import (TucsonHourlyOuterEinvironmentData) end##########

    # set the imported data
    simulatorClass.hourlyHorizontalDirectOuterSolarIrradiance = hourlyHorizontalDirectOuterSolarIrradiance
    simulatorClass.hourlyHorizontalDiffuseOuterSolarIrradiance = hourlyHorizontalDiffuseOuterSolarIrradiance
    simulatorClass.hourlyHorizontalTotalOuterSolarIrradiance = hourlyHorizontalTotalOuterSolarIrradiance
    simulatorClass.hourlyHorizontalTotalBeamMeterBodyTemperature = hourlyHorizontalTotalBeamMeterBodyTemperature
    simulatorClass.hourlyAirTemperature = hourlyAirTemperature

    # ################## plot the imported direct and diffuse solar radiation start######################
    # Title = "imported (measured horizontal) direct and diffuse solar radiation"
    # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "total Solar irradiance [W m^-2]"
    # util.plotTwoData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), \
    #                  simulatorClass.getImportedHourlyHorizontalDirectSolarRadiation(), simulatorClass.getImportedHourlyHorizontalDiffuseSolarRadiation() ,Title, xAxisLabel, yAxisLabel, \
    #                  "hourlyHorizontalDirectOuterSolarIrradiance", "hourlyHorizontalDiffuseOuterSolarIrradiance")
    # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # ################## plot the imported direct and diffuse solar radiation end######################

    print ("hourlyHorizontalDirectOuterSolarIrradiance:{}".format(hourlyHorizontalDirectOuterSolarIrradiance))
    print ("max(simulatorClass.getImportedHourlyHorizontalDirectSolarRadiation()):{}".format(max(simulatorClass.getImportedHourlyHorizontalDirectSolarRadiation())))

    # set new data which can be derived from the imported data
    util.deriveOtherArraysFromImportedData(simulatorClass)

    ################################################################################
    ##########solar irradiance to OPV calculation with imported data start##########
    ################################################################################

    if constant.ifUseOnlyRealData == True:

        # calculate with real data
        # hourly average [W m^-2]
        directSolarRadiationToOPVEastDirection, \
        directSolarRadiationToOPVWestDirection, \
        diffuseSolarRadiationToOPV, \
        albedoSolarRadiationToOPV = simulatorDetail.calcOPVmoduleSolarIrradianceGHRoof(simulatorClass)

        # set the calculated data
        simulatorClass.setDirectSolarRadiationToOPVEastDirection(directSolarRadiationToOPVEastDirection)
        simulatorClass.setDirectSolarRadiationToOPVWestDirection(directSolarRadiationToOPVWestDirection)
        simulatorClass.setDiffuseSolarRadiationToOPV(diffuseSolarRadiationToOPV)
        simulatorClass.setAlbedoSolarRadiationToOPV(albedoSolarRadiationToOPV)

        # [W m^-2] per hour
        totalSolarRadiationToOPV = (simulatorClass.getDirectSolarRadiationToOPVEastDirection() + simulatorClass.getDirectSolarRadiationToOPVWestDirection() ) / 2.0 \
                                   + simulatorClass.getDiffuseSolarRadiationToOPV() + simulatorClass.getAlbedoSolarRadiationToOPV()

        # ##################plot the various real light intensity to OPV film start######################
        # Title = "various real light intensity to OPV film"
        # plotDataSet = np.array([simulatorClass.getDirectSolarRadiationToOPVEastDirection(), simulatorClass.getDirectSolarRadiationToOPVWestDirection(), \
        #                         simulatorClass.getDiffuseSolarRadiationToOPV(), simulatorClass.getAlbedoSolarRadiationToOPV()])
        # labelList = np.array(["direct To East Direction", "direct To West Direction", "diffuse", "albedo"])
        # xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "[W m^-2]"
        # util.plotMultipleData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), plotDataSet, labelList, Title, xAxisLabel, yAxisLabel)
        # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # ##################plot the various real light intensity to OPV film end######################

        ###################data export start##################
        util.exportCSVFile(np.array([simulatorClass.getDirectSolarRadiationToOPVEastDirection(), simulatorClass.getDirectSolarRadiationToOPVWestDirection(), \
                                simulatorClass.getDiffuseSolarRadiationToOPV(), simulatorClass.getAlbedoSolarRadiationToOPV()]).T,
                           "hourlyMeasuredSolarRadiations")
        # util.exportCSVFile(hourlyEstimatedTotalSolarRadiationToOPVOnly15th, "hourlyEstimatedTotalSolarRadiationToOPVOnly15th")
        ###################data export end##################

        # ##################plot the difference of total solar radiation with imported data (radiation to horizontal surface) and simulated data (radiation to tilted surface start######################
        # hourlyHorizontalTotalOuterSolarIrradiance = simulatorClass.getImportedHourlyHorizontalDirectSolarRadiation() + simulatorClass.getImportedHourlyHorizontalDiffuseSolarRadiation()
        # Title = "total solar radiation to OPV with measured data"
        # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "total Solar irradiance [W m^-2]"
        # util.plotTwoData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), \
        #                  hourlyHorizontalTotalOuterSolarIrradiance, totalSolarRadiationToOPV, Title, xAxisLabel, yAxisLabel, "measured horizontal", "tilted with measured")
        # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # ##################plot the difference of total solar radiation with imported data (radiation to horizontal surface) and simulated data (radiation to tilted surface end######################

        ###################data export start##################
        util.exportCSVFile(np.array([hourlyHorizontalTotalOuterSolarIrradiance, totalSolarRadiationToOPV]).T,
                           "hourlyMeasuredSolarRadiationToHorizontalAndTilted")
        # util.exportCSVFile(hourlyEstimatedTotalSolarRadiationToOPVOnly15th, "hourlyEstimatedTotalSolarRadiationToOPVOnly15th")
        ###################data export end##################

        # unit change: [W m^-2] -> [umol m^-2 s^-1] == PPFD
        directPPFDToOPVEastDirection = util.convertFromWattperSecSquareMeterToPPFD(directSolarRadiationToOPVEastDirection)
        directPPFDToOPVWestDirection = util.convertFromWattperSecSquareMeterToPPFD(directSolarRadiationToOPVWestDirection)
        diffusePPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(diffuseSolarRadiationToOPV)
        groundReflectedPPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(albedoSolarRadiationToOPV)
        # print"diffusePPFDToOPV.shape:{}".format(diffusePPFDToOPV.shape)

        # set the matrix to the object
        simulatorClass.setDirectPPFDToOPVEastDirection(directPPFDToOPVEastDirection)
        simulatorClass.setDirectPPFDToOPVWestDirection(directPPFDToOPVWestDirection)
        simulatorClass.setDiffusePPFDToOPV(diffusePPFDToOPV)
        simulatorClass.setGroundReflectedPPFDToOPV(groundReflectedPPFDToOPV)

        # unit change: hourly [umol m^-2 s^-1] -> [mol m^-2 day^-1] == daily light integral (DLI) :number of photons received in a square meter per day
        directDLIToOPVEastDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVEastDirection)
        directDLIToOPVWestDirection = util.convertFromHourlyPPFDWholeDayToDLI(directPPFDToOPVWestDirection)
        diffuseDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(diffusePPFDToOPV)
        groundReflectedDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(groundReflectedPPFDToOPV)
        totalDLIToOPV = (directDLIToOPVEastDirection+directDLIToOPVWestDirection) / 2.0 + diffuseDLIToOPV + groundReflectedDLIToOPV
        # print "directDLIToOPVEastDirection:{}".format(directDLIToOPVEastDirection)
        # print "diffuseDLIToOPV.shape:{}".format(diffuseDLIToOPV.shape)
        # print "groundReflectedDLIToOPV:{}".format(groundReflectedDLIToOPV)

        # set the array to the object
        simulatorClass.setDirectDLIToOPVEastDirection(directDLIToOPVEastDirection)
        simulatorClass.setDirectDLIToOPVWestDirection(directDLIToOPVWestDirection)
        simulatorClass.setDiffuseDLIToOPV(diffuseDLIToOPV)
        simulatorClass.setGroundReflectedDLIToOPV(groundReflectedDLIToOPV)


    ########################################################################################################################
    ################# calculate solar irradiance without real data (estimate solar irradiance) start #######################
    ########################################################################################################################
    elif constant.ifUseOnlyRealData == False:

        # activate the mode to use the formulas for estimation. This is used for branching the solar irradiance to PV module. See OPVFilm.py
        simulatorClass.setEstimateSolarRadiationMode(True)

        # calculate the solar radiation to the OPV film
        # [W m^-2] per hour
        estimatedDirectSolarRadiationToOPVEastDirection, \
        estimatedDirectSolarRadiationToOPVWestDirection, \
        estimatedDiffuseSolarRadiationToOPV, \
        estimatedAlbedoSolarRadiationToOPV = simulatorDetail.calcOPVmoduleSolarIrradianceGHRoof(simulatorClass)

        estimatedTotalSolarRadiationToOPV = (estimatedDirectSolarRadiationToOPVEastDirection + estimatedDirectSolarRadiationToOPVWestDirection) / 2.0 + estimatedDiffuseSolarRadiationToOPV + estimatedAlbedoSolarRadiationToOPV

        # set the calc results
        simulatorClass.setDirectSolarRadiationToOPVEastDirection(estimatedDirectSolarRadiationToOPVEastDirection)
        simulatorClass.setDirectSolarRadiationToOPVWestDirection(estimatedDirectSolarRadiationToOPVWestDirection)
        simulatorClass.setDiffuseSolarRadiationToOPV(estimatedDiffuseSolarRadiationToOPV)
        simulatorClass.setAlbedoSolarRadiationToOPV(estimatedAlbedoSolarRadiationToOPV)
        # # modified not to use the following variables
        # simulatorClass.setEstimatedDirectSolarRadiationToOPVEastDirection(estimatedDirectSolarRadiationToOPVEastDirection)
        # simulatorClass.setEstimatedDirectSolarRadiationToOPVWestDirection(estimatedDirectSolarRadiationToOPVWestDirection)
        # simulatorClass.setEstimatedDiffuseSolarRadiationToOPV(estimatedDiffuseSolarRadiationToOPV)
        # simulatorClass.setEstimatedAlbedoSolarRadiationToOPV(estimatedAlbedoSolarRadiationToOPV)

        # print "estimatedDirectSolarRadiationToOPVEastDirection:{}".format(estimatedDirectSolarRadiationToOPVEastDirection)
        # np.set_printoptions(threshold=np.inf)
        # print "estimatedDirectSolarRadiationToOPVWestDirection:{}".format(estimatedDirectSolarRadiationToOPVWestDirection)
        # np.set_printoptions(threshold=1000)
        # print "estimatedDiffuseSolarRadiationToOPV:{}".format(estimatedDiffuseSolarRadiationToOPV)
        # print "estimatedAlbedoSolarRadiationToOPV:{}".format(estimatedAlbedoSolarRadiationToOPV)

        # ################## plot the distribution of estimated various DLI to OPV film start######################
        # Title = "estimated various light intensity to tilted OPV film"
        # plotDataSet = np.array([estimatedDirectSolarRadiationToOPVEastDirection, estimatedDirectSolarRadiationToOPVWestDirection, estimatedDiffuseSolarRadiationToOPV, estimatedAlbedoSolarRadiationToOPV])
        # labelList = np.array(["Direct To  East Direction", "Direct To West Direction", "Diffuse", "Albedo"])
        # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "[W m^-2]"
        # util.plotMultipleData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), plotDataSet, labelList, Title, xAxisLabel, yAxisLabel)
        # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # ################## plot the distribution of estimated various DLI to OPV film end######################

        # ################## plot the imported horizontal data vs estimated data (the tilt should be zeor) ######################
        # title = "measured and estimated horizontal data (tilt should be zero)"
        # xAxisLabel = "hourly measured horizontal total outer solar radiation [W m^-2]" + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "hourly estimated horizontal Total outer solar radiation [W m^-2]"
        # util.plotData(hourlyHorizontalTotalOuterSolarIrradiance, estimatedTotalSolarRadiationToOPV, title, xAxisLabel, yAxisLabel, None, True, 0.0, 1.0)
        # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # ################### plot the electricity yield per area with given OPV film end######################

        # [estimated data] unit change:
        estimatedDirectPPFDToOPVEastDirection = util.convertFromWattperSecSquareMeterToPPFD(estimatedDirectSolarRadiationToOPVEastDirection)
        estimatedDirectPPFDToOPVWestDirection = util.convertFromWattperSecSquareMeterToPPFD(estimatedDirectSolarRadiationToOPVWestDirection)
        estimatedDiffusePPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(estimatedDiffuseSolarRadiationToOPV)
        estimatedGroundReflectedPPFDToOPV = util.convertFromWattperSecSquareMeterToPPFD(estimatedAlbedoSolarRadiationToOPV)

        # set the variables
        simulatorClass.setDirectPPFDToOPVEastDirection(estimatedDirectPPFDToOPVEastDirection)
        simulatorClass.setDirectPPFDToOPVWestDirection(estimatedDirectPPFDToOPVWestDirection)
        simulatorClass.setDiffusePPFDToOPV(estimatedDiffusePPFDToOPV)
        simulatorClass.setGroundReflectedPPFDToOPV(estimatedGroundReflectedPPFDToOPV)
        # # modified not to use the following variables
        # simulatorClass.setEstimatedDirectPPFDToOPVEastDirection(estimatedDirectPPFDToOPVEastDirection)
        # simulatorClass.setEstimatedDirectPPFDToOPVWestDirection(estimatedDirectPPFDToOPVWestDirection)
        # simulatorClass.setEstimatedDiffusePPFDToOPV(estimatedDiffusePPFDToOPV)
        # simulatorClass.setEstimatedGroundReflectedPPFDToOPV(estimatedGroundReflectedPPFDToOPV)


        # [estimated data] unit change:
        estimatedDirectDLIToOPVEastDirection = util.convertFromHourlyPPFDWholeDayToDLI(estimatedDirectPPFDToOPVEastDirection)
        estimatedDirectDLIToOPVWestDirection = util.convertFromHourlyPPFDWholeDayToDLI(estimatedDirectPPFDToOPVWestDirection)
        estimatedDiffuseDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(estimatedDiffusePPFDToOPV)
        estimatedGroundReflectedDLIToOPV = util.convertFromHourlyPPFDWholeDayToDLI(estimatedGroundReflectedPPFDToOPV)
        # estimatedTotalDLIToOPV = (estimatedDirectDLIToOPVEastDirection + estimatedDirectDLIToOPVWestDirection) / 2.0 + estimatedDiffuseDLIToOPV + estimatedGroundReflectedDLIToOPV
        # set the variables
        # # modified not to use the following variables
        # simulatorClass.setEstimatedDirectDLIToOPVEastDirection(estimatedDirectDLIToOPVEastDirection)
        # simulatorClass.setEstimatedDirectDLIToOPVWestDirection(estimatedDirectDLIToOPVWestDirection)
        # simulatorClass.setEstimatedDiffuseDLIToOPV(estimatedDiffuseDLIToOPV)
        # simulatorClass.setEestimatedGroundReflectedDLIToOPV(estimatedGroundReflectedDLIToOPV)
        simulatorClass.setDirectDLIToOPVEastDirection(estimatedDirectDLIToOPVEastDirection)
        simulatorClass.setDirectDLIToOPVWestDirection(estimatedDirectDLIToOPVWestDirection)
        simulatorClass.setDiffuseDLIToOPV(estimatedDiffuseDLIToOPV)
        simulatorClass.setGroundReflectedDLIToOPV(estimatedGroundReflectedDLIToOPV)

        # deactivate the mode to the default value.
        simulatorClass.setEstimateSolarRadiationMode(False)

        # ##################plot the difference of total solar radiation with imported data and simulated data start######################
        # Title = "total solar radiation to OPV with measured horizontal and estimated tilted"
        # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "total Solar irradiance [W m^-2]"
        # util.plotTwoData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), \
        #                  hourlyHorizontalTotalOuterSolarIrradiance, estimatedTotalSolarRadiationToOPV ,Title, xAxisLabel, yAxisLabel, "measured horizontal", "estimated tilted")
        # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # ##################plot the difference of total solar radiation with imported data and simulated data  end######################

        # ################## plot the difference of total DLI with real data and simulated data start######################
        # Title = "difference of total DLI to tilted OPV with real data and estimation"
        # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "DLI [mol m^-2 day^-1]"
        # util.plotTwoData(np.linspace(0, simulationDaysInt, simulationDaysInt), \
        #                  totalDLIToOPV, estimatedTotalDLIToOPV ,Title, xAxisLabel, yAxisLabel, "with real data", "wth no data")
        # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # ################## plot the difference of total DLI with real data and simulated data  end######################

    ################# calculate solar irradiance without real data (estimate the data) end #######################

    # ##################plot the difference of total solar radiation with real data and simulated data start######################
    # Title = "total solar radiation to OPV with tilted with measured and estimated tilted"
    # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "total Solar irradiance [W m^-2]"
    # util.plotTwoData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), \
    #                  totalSolarRadiationToOPV, estimatedTotalSolarRadiationToOPV ,Title, xAxisLabel, yAxisLabel, "tilted with measured", "estimated tilted")
    # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # ##################plot the difference of total solar radiation with real data and simulated data  end######################

    # data export of solar irradiance
    util.exportCSVFile(np.array([year, month, day, hour, \
                                 simulatorClass.getDirectSolarRadiationToOPVEastDirection(), \
                                 simulatorClass.getDirectSolarRadiationToOPVWestDirection(), \
                                 simulatorClass.getDiffuseSolarRadiationToOPV(), \
                                 simulatorClass.getAlbedoSolarRadiationToOPV(), \
                                 estimatedTotalSolarRadiationToOPV]).T,
                          "SolarIrradianceToHorizontalSurface")

    # If necessary, get the solar radiation data only on 15th day
    if util.getSimulationDaysInt() > 31 and constant.ifGet15thDayData:
        ################## plot the imported horizontal data vs estimated data only with 15th day each month (the tilt should be zero) start ######################
        title = "measured and estimated horizontal data only 15th day (tilt should be zero)"
        # measured horizontal data
        hourlyMeasuredHorizontalTotalSolarRadiationOnly15th = util.getOnly15thDay(hourlyHorizontalTotalOuterSolarIrradiance)
        # estmated data
        hourlyEstimatedTotalSolarRadiationToOPVOnly15th = util.getOnly15thDay(estimatedTotalSolarRadiationToOPV)
        xAxisLabel = "hourly measured horizontal total outer solar radiation [W m^-2]" + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        yAxisLabel = "hourly estimated horizontal Total outer solar radiation [W m^-2]"
        util.plotData(hourlyMeasuredHorizontalTotalSolarRadiationOnly15th, hourlyEstimatedTotalSolarRadiationToOPVOnly15th, title, xAxisLabel, yAxisLabel, None, True, 0.0, 1.0)
        util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        ################## plot the imported horizontal data vs estimated data only with 15th day each month (the tilt should be zero) end ######################

        # data export
        util.exportCSVFile(np.array([hourlyMeasuredHorizontalTotalSolarRadiationOnly15th, hourlyEstimatedTotalSolarRadiationToOPVOnly15th]).T, "hourlyMeasuredHorizontalAndEstimatedTotalSolarRadiationOnly15th")
        # util.exportCSVFile(hourlyEstimatedTotalSolarRadiationToOPVOnly15th, "hourlyEstimatedTotalSolarRadiationToOPVOnly15th")

    # export measured horizontal and estimated data only when the simulation date is 1 day. *Modify the condition if necessary.
    elif constant.ifExportMeasuredHorizontalAndExtimatedData == True and util.getSimulationDaysInt() == 1:
        util.exportCSVFile(np.array([estimatedTotalSolarRadiationToOPV, hourlyHorizontalTotalOuterSolarIrradiance]).T, "hourlyMeasuredHOrizontalAndEstimatedTotalSolarRadiation")

    # ################## plot the distribution of direct and diffuse PPFD start######################
    # Title = "TOTAL outer PPFD to OPV"
    # xAxisLabel = "time [hour]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "PPFD [umol m^-2 s^-1]"
    # util.plotData(np.linspace(0, simulationDaysInt * constant.hourperDay, simulationDaysInt * constant.hourperDay), \
    #               directPPFDToOPV + diffusePPFDToOPV + groundReflectedPPFDToOPV, Title, xAxisLabel, yAxisLabel)
    # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # ################## plot the distribution of direct and diffuse PPFD end######################

    # ################## plot the distribution of direct and diffuse solar DLI with real data start######################
    # Title = "direct and diffuse outer DLI to OPV"
    # xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "DLI [mol m^-2 day^-1]"
    # y1Label = "(directDLIToOPVEastDirection+directDLIToOPVWestDirection)/2.0"
    # y2Label = "diffuseDLIToOPV"
    # util.plotTwoData(np.linspace(0, simulationDaysInt, simulationDaysInt), (directDLIToOPVEastDirection+directDLIToOPVWestDirection)/2.0, diffuseDLIToOPV, Title,
    #                  xAxisLabel, yAxisLabel, y1Label, y2Label)
    # util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # ################## plot the distribution of direct and diffuse solar DLI end######################

    ################## plot the distribution of various DLI to OPV film start######################
    Title = "various DLI to OPV film"
    plotDataSet = np.array([simulatorClass.getDirectDLIToOPVEastDirection(), simulatorClass.getDirectDLIToOPVWestDirection(), simulatorClass.getDiffuseDLIToOPV(), simulatorClass.getGroundReflectedDLIToOPV()])
    labelList = np.array(["directDLIToOPVEastDirection", "directDLIToOPVWestDirection", "diffuseDLIToOPV", "groundReflectedDLIToOPV"])
    xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    yAxisLabel = "DLI [mol m^-2 day^-1]"
    util.plotMultipleData(np.linspace(0, simulationDaysInt,  simulationDaysInt), plotDataSet, labelList, Title, xAxisLabel, yAxisLabel)
    util.saveFigure(Title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    ################## plot the distribution of various DLI to OPV film end######################

    ############################################################################################
    ################## calculate the daily electricity yield per area start#####################
    ############################################################################################
    # TODO: for more accurate modeling, we need actual data for a more detailed model (considering the OPV material) for the temperature of OPV film, but right now, just use the imported body temperature.
    # get the daily electricity yield per area per day ([J/m^2/day]) based on the given light intensity ([Celsius],[W/m^2]).
    # regard the east side and west tilted OPV module differently/
    dailyJopvoutperAreaEastRoof = simulatorDetail.getDailyElectricityYieldperArea(hourlyHorizontalTotalBeamMeterBodyTemperature, \
                                                                                  simulatorClass.getDirectSolarRadiationToOPVEastDirection(),
                                                                                  simulatorClass.getDiffuseSolarRadiationToOPV(),
                                                                                  simulatorClass.getAlbedoSolarRadiationToOPV())
    dailyJopvoutperAreaWestRoof = simulatorDetail.getDailyElectricityYieldperArea(hourlyHorizontalTotalBeamMeterBodyTemperature, \
                                                                                  simulatorClass.getDirectSolarRadiationToOPVWestDirection(),
                                                                                  simulatorClass.getDiffuseSolarRadiationToOPV(),
                                                                                  simulatorClass.getAlbedoSolarRadiationToOPV())
    # print("dailyJopvoutperAreaEastRoof:{}".format(dailyJopvoutperAreaEastRoof))
    # print("dailyJopvoutperAreaWestRoof:{}".format(dailyJopvoutperAreaWestRoof))

    # unit change [J/m^2/day] -> [Wh/m^2/day]
    # dailyWhopvoutperArea = util.convertFromJouleToWattHour(dailyJopvoutperArea)
    dailyWhopvoutperAreaEastRoof = util.convertFromJouleToWattHour(dailyJopvoutperAreaEastRoof)
    dailyWhopvoutperAreaWestRoof = util.convertFromJouleToWattHour(dailyJopvoutperAreaWestRoof)
    # set the variables
    simulatorClass.dailyWhopvoutperAreaEastRoof = dailyWhopvoutperAreaEastRoof
    simulatorClass.dailyWhopvoutperAreaWestRoof = dailyWhopvoutperAreaWestRoof
    # print("dailyWhopvoutperAreaEastRoof:{}".format(dailyWhopvoutperAreaEastRoof))
    # print("dailyWhopvoutperAreaWestRoof:{}".format(dailyWhopvoutperAreaWestRoof ))

    # electricity production  unit Exchange [Wh/m^2/day] -> [kWh/m^2/day]
    # dailykWhopvoutperArea = util.convertWhTokWh(dailyWhopvoutperArea)
    dailykWhopvoutperAreaEastRoof = util.convertWhTokWh(dailyWhopvoutperAreaEastRoof)
    dailykWhopvoutperAreaWestRoof = util.convertWhTokWh(dailyWhopvoutperAreaWestRoof)
    # set the variables
    simulatorClass.dailykWhopvoutperAreaEastRoof = dailykWhopvoutperAreaEastRoof
    simulatorClass.dailykWhopvoutperAreaWestRoof = dailykWhopvoutperAreaWestRoof

    # the total electricity produced (unit exchange: [kWh/m^2/day] -> [kWh/day])
    totalkWhopvoutPerday = dailykWhopvoutperAreaEastRoof * (constant.greenhouseRoofTotalAreaEastOrNorth) + dailykWhopvoutperAreaWestRoof * (constant.greenhouseRoofTotalAreaWestOrSouth)
    totalkWhopvoutPerMeterPerday = totalkWhopvoutPerday/constant.greenhouseTotalRoofArea
    # set the calculated value
    simulatorClass.totalkWhopvoutPerday = totalkWhopvoutPerday
    simulatorClass.totalkWhopvoutPerMeterPerday = totalkWhopvoutPerMeterPerday

    # ################### plot the electricity yield per area with given OPV film
    # title = "electricity yield per area vs OPV film (east_west average)"
    # xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "Electricity yield per OPV area [kWh/m^2/day]"
    # util.plotData(np.linspace(0, simulationDaysInt, simulationDaysInt), (dailykWhopvoutperAreaEastRoof + dailykWhopvoutperAreaWestRoof)/2.0, title, xAxisLabel, yAxisLabel)
    # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # ################### plot the electricity yield per area with given OPV film end

    # data export
    util.exportCSVFile(np.array([year[::24], month[::24], day[::24], dailykWhopvoutperAreaEastRoof, dailykWhopvoutperAreaWestRoof]).T,
                          "dailyElectricEnergyFromRoofsFacingEachDirection")
    ##########################################################################################
    ################## calculate the daily electricity yield per area end#####################
    ##########################################################################################

    ##########################################################################################
    ################## calculate the daily electricity sales per area start###################
    ##########################################################################################
    # convert the year of each hour to the year to each day
    yearOfeachDay = year[::24]
    # convert the month of each hour to the month to each day
    monthOfeachDay = month[::24]
    # get the monthly electricity sales per area [USD/month/m^2]
    monthlyElectricitySalesperAreaEastRoof = simulatorDetail.getMonthlyElectricitySalesperArea(dailykWhopvoutperAreaEastRoof, yearOfeachDay, monthOfeachDay)
    monthlyElectricitySalesperAreaWastRoof = simulatorDetail.getMonthlyElectricitySalesperArea(dailykWhopvoutperAreaWestRoof, yearOfeachDay, monthOfeachDay)
    # set the value to the object
    simulatorClass.setMonthlyElectricitySalesperAreaEastRoof(monthlyElectricitySalesperAreaEastRoof)
    simulatorClass.setMonthlyElectricitySalesperAreaWestRoof(monthlyElectricitySalesperAreaWastRoof)
    # print "simulatorClass.getMonthlyElectricitySalesperArea():{}".format(simulatorClass.getMonthlyElectricitySalesperArea())

    # electricity sales unit Exchange [USD/m^2/month] -> [USD/month]
    totalElectricitySalesPerMonth = monthlyElectricitySalesperAreaEastRoof  * (constant.OPVAreaFacingEastOrNorthfacingRoof) + monthlyElectricitySalesperAreaWastRoof * (constant.OPVAreaFacingWestOrSouthfacingRoof)
    # the averaged electricity sales [USD/m^2/month]
    totalElectricitySalesPerAreaPerMonth = totalElectricitySalesPerMonth/constant.OPVArea
    # set the value to the object
    simulatorClass.totalElectricitySalesPerAreaPerMonth = totalElectricitySalesPerAreaPerMonth
    simulatorClass.totalElectricitySalesPerMonth = totalElectricitySalesPerMonth
    simulatorClass.totalElectricitySales = sum(totalElectricitySalesPerMonth)

    ###########################################################################################
    ################## calculate the daily electricity sales  per area end#####################
    ###########################################################################################

    #####################################################################################################
    ##################calculate the electricity cost per area start######################################
    #####################################################################################################
    if constant.ifConsiderOPVCost is True:
        # get the depreciation price for the whole simulation period
        # it was assumed that the depreciation method is gross average method
        # unit: USD
        initialOPVCostUSD = constant.OPVPricePerAreaUSD * OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio)
        # unit: USD/day
        totalOPVCostUSDForDepreciation = initialOPVCostUSD * (util.getSimulationDaysInt() / constant.OPVDepreciationPeriodDays)
        # set the value to the object
        simulatorClass.setOPVCostUSDForDepreciationPerOPVArea(totalOPVCostUSDForDepreciation / OPVFilm.getOPVArea(constant.OPVAreaCoverageRatio))
        simulatorClass.totalOPVCostUSDForDepreciation = totalOPVCostUSDForDepreciation
        simulatorClass.totalOPVCostUSDForDepreciationPerGHFloorArea = totalOPVCostUSDForDepreciation / constant.greenhouseFloorArea

    else:
        # set the value to the object. the value is zero if not consider the purchase cost
        simulatorClass.setOPVCostUSDForDepreciationPerOPVArea(0.0)
        simulatorClass.totalOPVCostUSDForDepreciation = 0.0
        simulatorClass.totalOPVCostUSDForDepreciationPerGHFloorArea = 0.0

    ###################################################################################################
    ##################calculate the electricity cost per area end######################################
    ###################################################################################################

    ################################################################################
    ################## calculate the electricity production profit/loss start#######
    ################################################################################
    # profit == sales - less(cost)
    electricityProductionProfit = simulatorClass.totalElectricitySales - simulatorClass.totalOPVCostUSDForDepreciation
    electricityProductionProfitPerGHFloorArea = electricityProductionProfit / constant.greenhouseFloorArea

    # set the variable to the object
    simulatorClass.electricityProductionProfit = electricityProductionProfit
    simulatorClass.electricityProductionProfitPerGHFloorArea = electricityProductionProfitPerGHFloorArea
    ################################################################################
    ################## calculate the electricity production profit/loss end#########
    ################################################################################

    ###############################################################################################
    ###################calculate the solar irradiance through multi span roof start################
    ###############################################################################################
    # The calculated irradiance is stored to the object in this function
    simulatorDetail.getDirectSolarIrradianceThroughMultiSpanRoof(simulatorClass)
    # data export
    util.exportCSVFile(np.array([year, month, day, hour, simulatorClass.getHourlyDirectSolarRadiationAfterMultiSpanRoof(),]).T,
                          "directSolarRadiationAfterMultiSpanRoof")
    ###########################################################################################
    ###################calculate the solar irradiance through multi span roof end##############
    ###########################################################################################

    ###########################################################################################
    ###################calculate the solar irradiance to plants start##########################
    ###########################################################################################
    # get/set cultivation days per harvest [days/harvest]
    cultivationDaysperHarvest = constant.cultivationDaysperHarvest
    simulatorClass.setCultivationDaysperHarvest(cultivationDaysperHarvest)

    # get/set OPV coverage ratio [-]
    OPVCoverage = constant.OPVAreaCoverageRatio
    simulatorClass.setOPVAreaCoverageRatio(OPVCoverage)

    # get/set OPV coverage ratio during fallow period[-]
    OPVCoverageSummerPeriod = constant.OPVAreaCoverageRatioSummerPeriod
    simulatorClass.setOPVCoverageRatioSummerPeriod(OPVCoverageSummerPeriod)

    # get if we assume to have shading curtain
    hasShadingCurtain = constant.hasShadingCurtain
    simulatorClass.setIfHasShadingCurtain(hasShadingCurtain)

    # TODO: delete this if it was determined not to use this variable
    # the amount of PPFD to deploy shading curtain PPFD [umol m^-2 s^-1]
    shadingCurtainDeployPPFD = constant.shadingCurtainDeployPPFD
    # this variable is substituted to the object at the declaration
    # simulatorClass.setShadingCurtainDeployPPFD(shadingCurtainDeployPPFD)

    # consider the OPV film, shading curtain, structure,
    simulatorDetail.setSolarIrradianceToPlants(simulatorClass)

    # the DLI to plants [mol/m^2/day]
    # totalDLItoPlants = simulatorDetail.getTotalDLIToPlants(OPVCoverage, importedDirectPPFDToOPV, importedDiffusePPFDToOPV, importedGroundReflectedPPFDToOPV,\
    #                                        hasShadingCurtain, shadingCurtainDeployPPFD, simulatorClass)
    # print "totalDLItoPlants:{}".format(totalDLItoPlants)
    # print "totalDLItoPlants.shape:{}".format(totalDLItoPlants.shape)
    totalDLItoPlants = simulatorClass.directDLIToPlants + simulatorClass.diffuseDLIToPlants
    # unit: DLI/day
    simulatorClass.totalDLItoPlants = totalDLItoPlants
    ########################################################################################
    ###################calculate the solar irradiance to plants end#########################
    ########################################################################################

    # ####################################################################################################
    # # Stop execution here...
    # sys.exit()
    # # Move the above line to different parts of the assignment as you implement more of the functionality.
    # ####################################################################################################

    #############################################################################
    ################## calculate the daily plant yield start#####################
    #############################################################################
    # # On the model, since it was assumed the temperature in the greenhouse is maintained at the set point by cooling system (pad and fan system), this function is not used.
    # # calc/set the thermal time to the object
    # simulatorDetail.setThermalTimeToPlants(simulatorClass)

    # get/set the plant growth model name [String]
    plantGrowthModel = constant.plantGrowthModel
    simulatorClass.setPlantGrowthModel(plantGrowthModel)

    #calculate plant yield given an OPV coverage and model :daily [g/head]
    shootFreshMassList, \
    unitDailyFreshWeightIncrease, \
    accumulatedUnitDailyFreshWeightIncrease, \
    unitDailyHarvestedFreshWeight = simulatorDetail.getPlantYieldSimulation(simulatorClass)
    # np.set_printoptions(threshold=np.inf)
    # print ("shootFreshMassList:{}".format(shootFreshMassList))
    # print ("unitDailyFreshWeightIncrease:{}".format(unitDailyFreshWeightIncrease))
    # print ("accumulatedUnitDailyFreshWeightIncrease:{}".format(accumulatedUnitDailyFreshWeightIncrease))
    # print ("unitDailyHarvestedFreshWeight:{}".format(unitDailyHarvestedFreshWeight))
    # np.set_printoptions(threshold=100)

    # get the penalized plant fresh weight with  too strong sunlight : :daily [g/unit]
    if constant.IfConsiderPhotoInhibition is True:

        # TODO: modify this function to decrease the plant when the average DLI during the cultivation period exceeds 17mol/m^2/day, which is the maximum DLI not causing tipburn
        penalizedUnitDailyHarvestedFreshWeight = simulatorDetail.penalizeUnitDailyHarvestedFreshWeight(unitDailyHarvestedFreshWeight, simulatorClass)

        ######################### plot UnitDailyHarvestedFreshWeight and penalized UnitDailyHarvestedFreshWeight
        # if no penalty occurs, these variables plot the same dots.
        title = "HarvestedFreshWeight and penalized HarvestedFreshWeight "
        xAxisLabel = "time [day]:  " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        yAxisLabel = "plant fresh weight[g/unit]"
        util.plotTwoData(np.linspace(0, util.getSimulationDaysInt(), util.getSimulationDaysInt()), \
                         unitDailyHarvestedFreshWeight, penalizedUnitDailyHarvestedFreshWeight, title, xAxisLabel, yAxisLabel, "real data", "penalized data")
        util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        #######################################################################

    # ######################### plot a graph showing the DLI to plants ######################################
    # title = "DLI to plants (OPV coverage " + str(int(100*OPVCoverage)) + "%)"
    # xAxisLabel = "time [day]:  " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "DLI[mol/m^2/day]"
    # util.plotData(np.linspace(0, simulationDaysInt, simulationDaysInt), totalDLItoPlants, title, xAxisLabel, yAxisLabel)
    # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # #######################################################################################################

    # ######################### plot a graph showing only shootFreshMassList per unit #######################
    # title = "plant yield per head vs time (OPV coverage " + str(int(100*OPVCoverage)) + "%)"
    # xAxisLabel = "time [day]:  " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "plant fresh weight[g/head]"
    # util.plotData(np.linspace(0, simulationDaysInt, simulationDaysInt), shootFreshMassList, title, xAxisLabel, yAxisLabel)
    # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # #######################################################################################################

    # data export
    util.exportCSVFile(np.array([year[::24], month[::24], day[::24], totalDLItoPlants, shootFreshMassList]).T, "shootFreshMassAndDLIToPlants")
    # util.exportCSVFile(hourlyEstimatedTotalSolarRadiationToOPVOnly15th, "hourlyEstimatedTotalSolarRadiationToOPVOnly15th")

    # unit conversion; get the plant yield per day per area: [g/head/day] -> [g/m^2/day]
    shootFreshMassPerAreaPerDay = util.convertUnitShootFreshMassToShootFreshMassperArea(shootFreshMassList)
    # print("shootFreshMassPerAreaPerDay:{}".format(shootFreshMassPerAreaPerDay))
    harvestedShootFreshMassPerAreaPerDay = util.convertUnitShootFreshMassToShootFreshMassperArea(unitDailyHarvestedFreshWeight)
    # print("harvestedShootFreshMassPerAreaPerDay:{}".format(harvestedShootFreshMassPerAreaPerDay))
    # unit conversion:  [g/m^2/day] -> [kg/m^2/day]
    shootFreshMassPerAreaKgPerDay = util.convertFromgramTokilogram(shootFreshMassPerAreaPerDay)
    harvestedShootFreshMassPerAreaKgPerDay = util.convertFromgramTokilogram(harvestedShootFreshMassPerAreaPerDay)

    # set the value to the object
    simulatorClass.shootFreshMassPerAreaKgPerDay = shootFreshMassPerAreaKgPerDay
    simulatorClass.harvestedShootFreshMassPerAreaKgPerDay = harvestedShootFreshMassPerAreaKgPerDay

    # ######################## plot a graph showing only shootFreshMassList per square meter ########################
    # title = "plant yield per area vs time (OPV coverage " + str(int(100*OPVCoverage)) + "%)"
    # xAxisLabel = "time [day]:  " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    # yAxisLabel = "plant fresh weight[kg/m^2]"
    # util.plotData(np.linspace(0, simulationDaysInt, simulationDaysInt), shootFreshMassPerAreaKgPerDay, title, xAxisLabel, yAxisLabel)
    # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    # ###############################################################################################################

    ################## plot various unit Plant Yield vs time
    plotDataSet = np.array([shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitDailyHarvestedFreshWeight])
    labelList = np.array(["shootFreshMassList", "unitDailyFreshWeightIncrease", "accumulatedUnitDailyFreshWeightIncrease", "unitDailyHarvestedFreshWeight"])
    title = "Various unit Plant Yield vs time (OPV coverage " + str(int(100*OPVCoverage)) + "%)"
    xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
    yAxisLabel = "Unit plant Fresh Weight [g/unit]"
    util.plotMultipleData(np.linspace(0, simulationDaysInt, simulationDaysInt), plotDataSet, labelList, title, xAxisLabel, yAxisLabel)
    util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
    #######################################################################
    ##########################################################################
    ################## calculate the daily plant yield end####################
    ##########################################################################

    ##########################################################################
    ################## calculate the daily plant sales start##################
    ##########################################################################
    # get the sales price of plant [USD/m^2]
    # if the average DLI during each harvest term is more than 17 mol/m^2/day, discount the price
    # It was assumed that there is no tipburn.
    # unit: USD/m^2/day
    dailyPlantSalesPerSquareMeter = simulatorDetail.getPlantSalesperSquareMeter(simulatorClass)
    # print ("dailyPlantSalesperSquareMeter.shape:{}".format(dailyPlantSalesperSquareMeter.shape))
    # unit: USD/m^2
    # TODO: this sales is the sales per unit cultivation area, not per the whole greenhouse floor area.
    totalPlantSalesperSquareMeter = sum(dailyPlantSalesPerSquareMeter)
    print ("totalPlantSalesperSquareMeter:{}".format(totalPlantSalesperSquareMeter))
    # unit: USD
    totalplantSales = totalPlantSalesperSquareMeter * constant.greenhouseCultivationFloorArea
    print ("totalplantSales:{}".format(totalplantSales))
    totalPlantSalesPerGHFloorArea = totalplantSales / constant.greenhouseFloorArea

    # set the variable to the object
    simulatorClass.totalPlantSalesperSquareMeter = totalPlantSalesperSquareMeter
    simulatorClass.totalplantSales = totalplantSales
    simulatorClass.totalPlantSalesPerGHFloorArea = totalPlantSalesPerGHFloorArea
    ##########################################################################
    ################## calculate the daily plant sales end####################
    ##########################################################################

    ######################################################################################################
    ################## calculate the daily plant cost (greenhouse operation cost) start###################
    ######################################################################################################
    # it was assumed that the cost for growing plants is significantly composed of labor cost and electricity and fuel energy cost for heating/cooling (including pad and fan syste)

    # TODO: make the functions for fuel and electricity cost
    totalFuelEnergyCost = 0.0
    totalFuelEnergyCostPerGHFloorArea = totalFuelEnergyCost / constant.greenhouseFloorArea
    totalElectricityCost = 0.0
    totalElectricityCostPerGHFloorArea = totalElectricityCost / constant.greenhouseFloorArea

    totalLaborCost = simulatorDetail.getLaborCost(simulatorClass)
    totalLaborCostPerGHFloorArea = totalLaborCost / constant.greenhouseFloorArea
    # set the values to the object
    simulatorClass.totalLaborCost = totalLaborCost
    simulatorClass.totalLaborCostPerGHFloorArea = totalLaborCostPerGHFloorArea

    totalPlantProductionCost = totalFuelEnergyCost + totalElectricityCost + totalLaborCost
    totalPlantProductionCostPerGHFloorArea = totalFuelEnergyCostPerGHFloorArea + totalElectricityCostPerGHFloorArea + totalLaborCostPerGHFloorArea
    # set the values to the object
    simulatorClass.totalPlantProductionCost = totalPlantProductionCost
    simulatorClass.totalPlantProductionCostPerGHFloorArea = totalPlantProductionCostPerGHFloorArea
    ######################################################################################################
    ################## calculate the daily plant cost (greenhouse operation cost) end#####################
    ######################################################################################################

    ################################################################################
    ################## calculate the plant production profit/los start##############
    ################################################################################
    totalPlantProfit = totalplantSales - totalPlantProductionCost
    totalPlantProfitPerGHFloorArea =  totalPlantSalesPerGHFloorArea - totalPlantProductionCostPerGHFloorArea
    # set the values to the object
    simulatorClass.totalPlantProfit = totalPlantProfit
    simulatorClass.totalPlantProfitPerGHFloorArea = totalPlantProfitPerGHFloorArea
    ################################################################################
    ################## calculate the plant production profit/loss end###############
    ################################################################################

    ################################################################################
    ################## calculate the total economic profit/loss start###############
    ################################################################################
    # get the economic profit
    economicProfit = totalPlantProfit + electricityProductionProfit
    economicProfitPerGHFloorArea = totalPlantProfitPerGHFloorArea + electricityProductionProfitPerGHFloorArea
    # set the values to the object
    simulatorClass.economicProfit = economicProfit
    simulatorClass.economicProfitPerGHFloorArea = economicProfitPerGHFloorArea
    ##############################################################################
    ################## calculate the total economic profit/loss end###############
    ##############################################################################

    return simulatorClass

    # ####################################################################################################
    # # Stop execution here...
    sys.exit()
    # # Move the above line to different parts of the assignment as you implement more of the functionality.
    # ####################################################################################################



    ############################################################################################
    ###################Simulation with various opv film coverage ratio start####################
    ############################################################################################
    # Choose the simulation type
    # simulationType = "economicProfitWithRealSolar"
    # simulationType = "plantAndElectricityYieldWithRealSolar"
    # simulationType = "RealSolarAndEstimatedSolarComparison"
    simulationType = "PlantAndElectricityYieldAndProfitOnEachOPVCoverage"
    # simulationType = "stop"


    if simulationType == "PlantAndElectricityYieldAndProfitOnEachOPVCoverage":
        #########initial parameters(statistics) value start##########
        # substitute the constant value here. You do not need to change the values in the constant class when you want to try other variables

        #cultivation days per harvest [days/harvest]
        cultivationDaysperHarvest = constant.cultivationDaysperHarvest
        #the coverage ratio by OPV on the roofTop.
        # OPVAreaCoverageRatio = constant.OPVAreaCoverageRatio
        # #the area of OPV on the roofTop.
        # OPVArea = OPVAreaCoverageRatio * constant.greenhouseRoofArea
        # OPV film unit price[USD/m^2]
        # boolean
        hasShadingCurtain = constant.hasShadingCurtain
        # PPFD [umol m^-2 s^-1]
        shadingCurtainDeployPPFD = constant.shadingCurtainDeployPPFD
        #plant growth model type
        # plantGrowthModel = constant.TaylorExpantionWithFluctuatingDLI
        plantGrowthModel = constant.plantGrowthModel

        #if you continue to grow plants during the fallow period, then True
        ifGrowForFallowPeriod = constant.ifGrowForFallowPeriod
        simulatorClass.setIfGrowForFallowPeriod(ifGrowForFallowPeriod)

        # x-axis
        OPVCoverageDelta = 0.01
        #OPVCoverageDelta = 0.001
        #the array for x-axis (OPV area [m^2])
        OPVCoverageList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        #########initial parameters(statistics) value end##########

        #########define objective functions start################
        # electricity yield for a given period: [J] for a given period
        electricityYield = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # unit plant yield for a given period: [g] for a given period
        unitPlantYield = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # unit total daily plant fresh mass increase for a given period with each OPV film coverage: [g] for a given period
        unitDailyFreshWeightList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # unit harvested fresh mass weight for a given period with each OPV film coverage: [g] for a given period
        unitDailyHarvestedFreshWeightList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # plant sales per square meter with each OPV film coverage: [USD/m^2]
        plantSalesperSquareMeterList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # plant cost per square meter with each OPV film coverage: [USD/m^2]
        # plantCostperSquareMeterList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # plant profit per square meter with each OPV film coverage: [USD/m^2]
        plantProfitperSquareMeterList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # plant profit with each OPV film coverage: [USD/m^2]
        plantProfitList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)

        # monthly electricity sales per area with each OPV film coverage [USD/month]
        monthlyElectricitySalesListEastRoof = np.zeros((int(1.0/OPVCoverageDelta), util.getSimulationMonthsInt()), dtype = float)
        monthlyElectricitySalesListWestRoof = np.zeros((int(1.0/OPVCoverageDelta), util.getSimulationMonthsInt()), dtype = float)

        # electricity sales with each OPV film coverage [USD]
        electricitySalesList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # electricitySalesListperAreaEastRoof = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # electricitySalesListperAreaWestRoof = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)

        # electricity sales with each OPV film coverage [USD]
        electricityProfitList =  np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        # economicProfit summing the electricity and plant profit [USD]
        economicProfitList = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
        #########define objective function end################

        # convert the year of each hour to the year to each day
        yearOfeachDay = year[::24]
        # convert the month of each hour to the month to each day
        monthOfeachDay = month[::24]
        # print "monthOfeachDay:{}".format(monthOfeachDay)
        # print "monthOfeachDay.shape:{}".format(monthOfeachDay.shape)

        # variable = OPV coverage ratio. loop by OPV coverage ratio
        for i in range (0, int(1.0/OPVCoverageDelta)):
            ################## calculate the electricity yield with different OPV coverage for given period start#####################
            OPVCoverageList[i] = i * OPVCoverageDelta

            # [J/m^2] per day -> [J] electricity yield for a given period with a given area.
            # sum the electricity yield of east and west direction roofs
            electricityYield[i] += simulatorDetail.getWholeElectricityYieldEachOPVRatio(OPVCoverageList[i], dailyJopvoutperAreaEastRoof, simulatorClass, constant.greenhouseRoofArea / 2.0)
            electricityYield[i] += simulatorDetail.getWholeElectricityYieldEachOPVRatio(OPVCoverageList[i], dailyJopvoutperAreaWestRoof, simulatorClass, constant.greenhouseRoofArea / 2.0)
            # print("i:{}, electricityYield[i]:{}".format(i, electricityYield[i]))

            # [J] -> [Wh]: divide by 3600
            electricityYield[i] = util.convertFromJouleToWattHour(electricityYield[i])
            # [Wh] -> [kWh]: divide by 1000
            electricityYield[i] = util.convertFromJouleToWattHour(electricityYield[i])
            ################## calculate the electricity yield with different OPV coverage for given period end#####################

            ##################calculate the electricity sales#######################
            # get the monthly electricity sales per area [USD/month/m^2]
            monthlyElectricitySalesperAreaEastRoof = simulatorDetail.getMonthlyElectricitySalesperArea(dailyJopvoutperAreaEastRoof, yearOfeachDay, monthOfeachDay)
            monthlyElectricitySalesperAreaWestRoof = simulatorDetail.getMonthlyElectricitySalesperArea(dailyJopvoutperAreaWestRoof, yearOfeachDay, monthOfeachDay)

            # get the monthly electricity sales per each OPV coverage ratio [USD/month]
            monthlyElectricitySalesListEastRoof[i] = simulatorDetail.getMonthlyElectricitySales(OPVCoverageList[i], monthlyElectricitySalesperAreaEastRoof, constant.greenhouseRoofArea / 2.0)
            monthlyElectricitySalesListWestRoof[i] = simulatorDetail.getMonthlyElectricitySales(OPVCoverageList[i], monthlyElectricitySalesperAreaWestRoof, constant.greenhouseRoofArea / 2.0)

            # get the electricity sales per each OPV coverage ratio for given period [USD], suming the monthly electricity sales.
            electricitySalesList[i] = sum(monthlyElectricitySalesListEastRoof[i]) + sum(monthlyElectricitySalesListWestRoof[i])
            # print"electricitySalesList:{}".format(electricitySalesList)

            ##################calculate the electricity cost######################################
            if constant.ifConsiderOPVCost is True:
                initialOPVCostUSD = constant.OPVPricePerAreaUSD * OPVFilm.getOPVArea(OPVCoverageList[i])
                OPVCostUSDForDepreciation =initialOPVCostUSD * (util.getSimulationDaysInt() / constant.OPVDepreciationPeriodDays)
            else:
                OPVCostUSDForDepreciation = 0.0

            ##################get the electricity profit ######################################
            electricityProfitList[i] = electricitySalesList[i]  - OPVCostUSDForDepreciation
        # print ("electricityYield:{}".format(electricityYield))


        # calc the electricity production per area [kWh/m^2]
        print ("electricity yield per area with 100% coverage ratio [kWh/m^2] was : {}".format(electricityYield[int(1.0/OPVCoverageDelta) -1] / constant.greenhouseRoofArea))

        # ################## plot the electricity yield with different OPV coverage for given period start ################
        # title = "electricity yield with a given area vs OPV film"
        # xAxisLabel = "OPV Coverage Ratio [-]"
        # yAxisLabel = "Electricity yield for a given period [kWh]"
        # util.plotData(OPVCoverageList, electricityYield, title, xAxisLabel, yAxisLabel)
        # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # ################## plot the electricity yield with different OPV coverage for given period end ##################

        # ################## plot the electricity profit with different OPV coverage for given period
        # title = "electricity profit for a given period vs OPV film coverage ratio"
        # xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "Electricity profit for a given period [USD]"
        # util.plotData(OPVCoverageList, electricityProfitList, title, xAxisLabel, yAxisLabel)
        # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)

        ################## calculate the daily plant yield and profit start#####################
        # variable = OPV coverage ratio. loop by OPV coverage ratio
        for i in range (0, int(1.0/OPVCoverageDelta)):

            ##################calculate the plant yield
            # Since the plants are not tilted, do not use the light intensity to the tilted surface, just use the inmported data or estimated data with 0 degree surface.
            # daily [g/unit]
            # shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitDailyHarvestedFreshWeight = \
            #     simulatorDetail.getPlantYieldSimulation(plantGrowthModel, cultivationDaysperHarvest,OPVCoverageList[i], \
            #     (directPPFDToOPVEastDirection + directPPFDToOPVWestDirection)/2.0, diffusePPFDToOPV, groundReflectedPPFDToOPV, hasShadingCurtain, shadingCurtainDeployPPFD, simulatorClass)
            shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitDailyHarvestedFreshWeight = \
                simulatorDetail.getPlantYieldSimulation(plantGrowthModel, cultivationDaysperHarvest,OPVCoverageList[i], \
                importedDirectPPFDToOPV, importedDiffusePPFDToOPV, importedGroundReflectedPPFDToOPV, hasShadingCurtain, shadingCurtainDeployPPFD, simulatorClass)

            # sum the daily increase and get the total increase for a given period with a certain OPV coverage ratio
            unitDailyFreshWeightList[i] =  sum(unitDailyFreshWeightIncrease)
            # sum the daily increase and get the total harvest weight for a given period with a certain OPV coverage ratio
            unitDailyHarvestedFreshWeightList[i] = sum(unitDailyHarvestedFreshWeight)
            # print "unitDailyHarvestedFreshWeight.shape:{}".format(unitDailyHarvestedFreshWeight.shape)

            ##################calculate the plant sales
            # unit conversion; get the daily plant yield per given period per area: [g/unit] -> [g/m^2]
            dailyHarvestedFreshWeightperArea = util.convertUnitShootFreshMassToShootFreshMassperArea(unitDailyHarvestedFreshWeight)
            # unit conversion:  [g/m^2] -> [kg/m^2]1
            dailyHarvestedFreshWeightperAreaKg = util.convertFromgramTokilogram(dailyHarvestedFreshWeightperArea)
            # get the sales price of plant [USD/m^2]
            # if the average DLI during each harvest term is more than 17 mol/m^2/day, discount the price
            # TODO may need to improve the function representing the affect of Tipburn
            dailyPlantSalesperSquareMeter = simulatorDetail.getPlantSalesperSquareMeter(year, dailyHarvestedFreshWeightperAreaKg, totalDLItoPlants)

            plantSalesperSquareMeterList[i] = sum(dailyPlantSalesperSquareMeter)
            # print "dailyPlantSalesperSquareMeter.shape:{}".format(dailyPlantSalesperSquareMeter.shape)

            ##################calculate the plant cost
            # plant operation cost per square meter for given simulation period [USD/m^2]
            plantCostperSquareMeter = simulatorDetail.getPlantCostperSquareMeter(simulationDaysInt)

            ##################plant profit per square meter with each OPV film coverage: [USD/m^2]
            plantProfitperSquareMeterList[i] = plantSalesperSquareMeterList[i] - plantCostperSquareMeter
            # print "plantProfitperSquareMeterList[i]:{}".format(plantProfitperSquareMeterList[i])
            # print "plantProfitperSquareMeterList[{}]:{}".format(i, plantProfitperSquareMeterList[i])
            plantProfitList[i] = plantProfitperSquareMeterList[i] * constant.greenhouseCultivationFloorArea

        # get the economic profit
        economicProfitList = plantProfitList + electricityProfitList

        # print "plantCostperSquareMeter:{}".format(plantCostperSquareMeter)
        # print "unitDailyHarvestedFreshWeightList:{}".format(unitDailyHarvestedFreshWeightList)
        # print "plantSalesperSquareMeterList:{}".format(plantSalesperSquareMeterList)

        # ################# plot the plant profit with different OPV coverage for given period
        # title = "plant profit with a given area vs OPV film"
        # xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel = "plant profit for a given period [USD]"
        # util.plotData(OPVCoverageList, plantProfitList, title, xAxisLabel, yAxisLabel)
        # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # #######################################################################

        # ######################## plot by two y-axes ##########################
        # title = "plant yield per area and electricity yield  vs OPV film"
        # xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel1 = "plant fresh weight for given period [kg/m^2]"
        # yAxisLabel2 = "Electricity yield [kW*h]"
        # yLabel1 = "unitDailyFreshWeightIncrease"
        # yLabel2 = "electricityYield[Kwh]"
        # util.plotTwoDataMultipleYaxes(OPVCoverageList, unitDailyFreshWeightList * constant.numOfHeadsPerArea / 1000.0, \
        #                               electricityYield, title, xAxisLabel, yAxisLabel1, yAxisLabel2, yLabel1, yLabel2)
        # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # #######################################################################

        ######################## plot by two y-axes ##########################
        title = "plant yield per area and electricity yield per foot print vs OPV film"
        xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        yAxisLabel1 = "plant fresh weight for given period [kg/m^2]"
        yAxisLabel2 = "Electricity yield per foot print [kW*h/m^2]"
        yLabel1 = "unitDailyFreshWeightIncrease"
        yLabel2 = "electricityYield[Kwh]"
        util.plotTwoDataMultipleYaxes(OPVCoverageList, unitDailyFreshWeightList * constant.numOfHeadsPerArea / 1000.0, \
                                      electricityYield/constant.greenhouseFloorArea, title, xAxisLabel, yAxisLabel1, yAxisLabel2, yLabel1, yLabel2)
        util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # #######################################################################
        # data export
        util.exportCSVFile(np.array([OPVCoverageList, unitDailyFreshWeightList * constant.numOfHeadsPerArea / 1000.0, electricityYield/constant.greenhouseFloorArea]).T, \
                           "PlantYieldPerAreaAndElectricityPerFootPrint")

        # ######################## plot by two y-axes ##########################
        # title = "plant and electricity yield vs OPV film"
        # xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        # yAxisLabel1 = "plant fresh weight for given period [g/head]"
        # yAxisLabel2 = "Electricity yield [kW*h]"
        # yLabel1 = "unitDailyFreshWeightIncrease"
        # yLabel2 = "electricityYield[Kwh]"
        # util.plotTwoDataMultipleYaxes(OPVCoverageList, unitDailyFreshWeightList, electricityYield ,title, xAxisLabel, yAxisLabel1, yAxisLabel2, yLabel1, yLabel2)
        # util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # #######################################################################

        # plotting this graph is the coal of this simulation!!!
        ################# plot the economic profit with different OPV coverage for given period
        title = "whole economic profit with a given area vs OPV film"
        xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
        yAxisLabel = "economic profit for a given period [USD]"
        util.plotData(OPVCoverageList, economicProfitList, title, xAxisLabel, yAxisLabel)
        util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
        # #######################################################################

        profitVSOPVCoverageData=np.array(zip(OPVCoverageList, economicProfitList))
        # export the OPVCoverageList and economicProfitList [USD]
        util.exportCSVFile(profitVSOPVCoverageData, "OPVCoverage-economicProfit")

        print ("end modeling: datetime.datetime.now():{}".format(datetime.datetime.now()))

        return profitVSOPVCoverageData, simulatorClass

    print("iteration cot conducted")
    return None






                               