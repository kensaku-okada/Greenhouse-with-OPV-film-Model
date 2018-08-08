# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 19 Dec 2017
# last edit date: 19 Dec 2017
######################################################

##########import package files##########
# from scipy import stats
import datetime
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulator1 as Simulator1
# import TwoDimLeastSquareAnalysis as TwoDimLS
import Util
import CropElectricityYeildSimulatorConstant as constant
# import importlib

case = "OneCaseSimulation"
# case = "OptimizeOnlyOPVCoverageRatio"
# case = "OptimizationByMINLPSolver"

if case == "OneCaseSimulation":
  print("run OneCaseSimulation")

  # get the 2-D data for least square method
  simulatorClass = Simulator1.simulateCropElectricityYieldProfit1()
  # print "profitVSOPVCoverageData:{}".format(profitVSOPVCoverageData)

  print("OneCaseSimulation finished")

  # ####################################################################################################
  # Stop execution here...
  sys.exit()
  # Move the above line to different parts of the assignment as you implement more of the functionality.
  #  ####################################################################################################


# # Least Square method
# if case == "LeastSquareMethod":
#   print("run LeastSquareMethod")
#
#   # get the 2-D data for least square method
#   simulatorClass = Simulator1.simulateCropElectricityYieldProfit1()
#   # print "profitVSOPVCoverageData:{}".format(profitVSOPVCoverageData)
#
#   # create the instance
#   twoDimLeastSquare = TwoDimLS.TwoDimLeastSquareAnalysis(profitVSOPVCoverageData)
#   # print "twoDimLeastSquare.getXaxis():{}".format(twoDimLeastSquare.getXAxis())
#
#   x = twoDimLeastSquare.getXAxis()
#   y = twoDimLeastSquare.getYAxis()
#
#   ########################### 10-fold CV (Cross Validation)
#   NumOfFold = 10
#   maxorder = 15
#   k10BestPolyOrder, min_log_mean_10cv_loss = twoDimLeastSquare.runCrossValidation(NumOfFold, maxorder, x, y,
#                                           randomize_data=True,
#                                           cv_loss_title='10-fold CV Loss',
#                                           filepath='./exportData/10fold-CV.png')
#
#   # curve fitting (least square method) with given order w
#   w = twoDimLeastSquare.getApproximatedFittingCurve(k10BestPolyOrder)
#
#   # This polyfit is just for generating non-optimal order figure.  Commend out this except debugging or experiment
#   w = np.polyfit(x, y, 15)
#   w = w[::-1]
#
#   # plot the best order curve with the data points
#   Util.plotDataAndModel(x, y, w, filepath='./exportData/bestPolynomialKFold.png')
#   print ('\n======================')
#   print ('10-fold the best order = {0}. loss = {1}, func coefficients w = {2}'.format(k10BestPolyOrder, min_log_mean_10cv_loss, w))
#
#   ########################### LOOCV (Leave One Out Cross Validation)
#   NumOfFold = twoDimLeastSquare.getXAxis().shape[0]
#   loocv_best_poly, min_log_mean_loocv_loss = twoDimLeastSquare.runCrossValidation(NumOfFold, maxorder, x, y,
#                                               randomize_data=True,
#                                               cv_loss_title='LOOCV Loss',
#                                               filepath='./exportData/LOOCV.png')
#
#   # curve fitting (least square method) with given order w
#   wLOOCV = twoDimLeastSquare.getApproximatedFittingCurve(k10BestPolyOrder)
#   # This polyfit is just for generating non-optimal order figure.  Commend out this except debugging or experiment
#   # wLOOCV = np.polyfit(x, y, 8)
#   # wLOOCV = wLOOCV[::-1]
#
#   # plot the best order curve with the data points
#   Util.plotDataAndModel(x, y, wLOOCV, filepath='./exportData/bestPolynomialLOOCV.png')
#   print ('\n======================')
#   print ('\n(LOOCV) the best order = {0}. loss = {1}, func coefficients w = {2}'.format(loocv_best_poly, min_log_mean_loocv_loss, w))

elif case == "OptimizeOnlyOPVCoverageRatio":
  # print ("run Simulator1.simulateCropElectricityYieldProfit1")
  # simulatorClass = Simulator1.simulateCropElectricityYieldProfit1()

  print ("run Simulator1.optimizeOPVCoverageRatio")

  ####################################################################################################
  ################ parameter preparation for optimization of OPV coverage ratio start ################
  ####################################################################################################
  # x-axis
  OPVCoverageDelta = 0.01
  # OPVCoverageDelta = 0.001
  # the array for x-axis (OPV area [m^2])
  OPVCoverages = np.array([i * 0.01 for i in range (0, int(1.0/OPVCoverageDelta)+1)])
  # print("OPVCoverages:{}".format(OPVCoverages))

  # total DLI to plants
  totalDLIstoPlants = np.zeros(OPVCoverages.shape[0], dtype=float)

  # electricity yield for a given period: [kwh] for a given period
  totalkWhopvouts = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalkWhopvoutsPerRoofArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalkWhopvoutsPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)

  # monthly electricity sales per area with each OPV film coverage [USD/month]
  # monthlyElectricitySalesListEastRoof = np.zeros(OPVCoverages.shape[0], Util.getSimulationMonthsInt()), dtype=float)
  # monthlyElectricitySalesListWestRoof = np.zeros(OPVCoverages.shape[0], Util.getSimulationMonthsInt()), dtype=float)

  # electricity sales with each OPV film coverage [USD]
  totalElectricitySales = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalElectricitySalesPerOPVArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalElectricitySalesPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  # electricitySalesListperAreaEastRoof = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)
  # electricitySalesListperAreaWestRoof = np.zeros(int(1.0/OPVCoverageDelta), dtype = float)

  # electricity cost with each OPV film coverage [USD]
  totalElectricityCosts = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalElectricityCostsPerOPVArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalElectricityCostsPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)

  # electricity profit with each OPV film coverage [USD]
  totalElectricityProfits = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalElectricityProfitsPerCultivationFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalElectricityProfitsPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)

  #  plant yield for a given period. unit:
  # totalGrowthFreshWeightsPerHead = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalGrowthFreshWeightsPerCultivationFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalGrowthFreshWeightsPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  # unit harvested fresh mass weight for a whole given period with each OPV film coverage. unit: kg m-2
  totalHarvestedShootFreshMassPerCultivationFloorAreaKgPerDay = np.zeros(OPVCoverages.shape[0], dtype=float)

  # plant sales per square meter with each OPV film coverage: [USD/m^2]  totalPlantSaleses =
  totalPlantSalesesPerCultivationFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  totalPlantSalesesPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)

  # plant cost per square meter with each OPV film coverage: [USD/m^2]
  totalPlantCostsPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype = float)

  # plant profit per square meter with each OPV film coverage: [USD/m^2]
  totalPlantProfitsPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)
  # plant profit with each OPV film coverage: [USD/m^2]
  totalPlantProfits = np.zeros(OPVCoverages.shape[0], dtype=float)

  # economicProfit summing the electricity and plant profit [USD]
  totalEconomicProfits = np.zeros(OPVCoverages.shape[0], dtype=float)
  # economicProfit summing the electricity and plant profit per area [USD m-2]
  economicProfitPerGHFloorArea = np.zeros(OPVCoverages.shape[0], dtype=float)

  ##################################################################################################
  ################ parameter preparation for optimization of OPV coverage ratio end ################
  ##################################################################################################

  for i in range(0, OPVCoverages.shape[0]):
    #set OPV coverage ratio [-]
    constant.OPVAreaCoverageRatio = OPVCoverages[i]
    # constantFilePath = os.path.dirname(__file__).replace('/', os.sep) + '\\' + 'CropElectricityYeildSimulatorConstant.py'
    # os.execv(constantFilePath, [os.path.abspath(constantFilePath)])
    # reload(constant)

    # change the other relevant parameters
    constant.OPVArea = OPVCoverages[i] * constant.greenhouseTotalRoofArea
    constant.OPVAreaFacingEastOrNorthfacingRoof = OPVCoverages[i] * (constant.greenhouseRoofTotalAreaEastOrNorth / constant.greenhouseTotalRoofArea)
    constant.OPVAreaFacingWestOrSouthfacingRoof = OPVCoverages[i] * (constant.greenhouseRoofTotalAreaWestOrSouth / constant.greenhouseTotalRoofArea)
    print("i:{}, constant.OPVArea:{}".format(i, constant.OPVArea))

    # run the simulation
    simulatorClass = Simulator1.simulateCropElectricityYieldProfit1()

    # total DLI to plant during the whole simulation days with each OPV coverage ratio
    totalDLIstoPlants[i] = sum(simulatorClass.totalDLItoPlants)

    # store the data from the simulator
    # unit: kwh
    totalkWhopvouts[i] = sum(simulatorClass.totalkWhopvoutPerday)
    # unit: kwh/m^2
    # print("totalkWhopvoutsPerRoofArea = sum(simulatorClass.totalkWhopvoutPerAreaPerday):{}".format(sum(simulatorClass.totalkWhopvoutPerAreaPerday)))
    totalkWhopvoutsPerRoofArea[i] = sum(simulatorClass.totalkWhopvoutPerAreaPerday)
    totalkWhopvoutsPerGHFloorArea[i] = totalkWhopvouts[i] / constant.greenhouseFloorArea

    # print("simulatorClass.totalElectricitySales:{}".format(simulatorClass.totalElectricitySales))
    # unit:: USD
    totalElectricitySales[i] = simulatorClass.totalElectricitySales
    # print("simulatorClass.totalElectricitySalesPerAreaPerMonth:{}".format(simulatorClass.totalElectricitySalesPerAreaPerMonth))
    # unit: USD/m^2
    totalElectricitySalesPerOPVArea[i] = sum(simulatorClass.totalElectricitySalesPerAreaPerMonth)
    totalElectricitySalesPerGHFloorArea[i] = totalElectricitySales[i] / constant.greenhouseFloorArea
    # unit: USD
    # print("simulatorClass.totalOPVCostUSDForDepreciation:{}".format(simulatorClass.totalOPVCostUSDForDepreciation))
    totalElectricityCosts[i] = simulatorClass.totalOPVCostUSDForDepreciation
    # unit: USD/m^2
    # print("simulatorClass.getOPVCostUSDForDepreciationPerOPVArea:{}".format(simulatorClass.getOPVCostUSDForDepreciationPerOPVArea()))
    totalElectricityCostsPerOPVArea[i] = simulatorClass.getOPVCostUSDForDepreciationPerOPVArea()
    totalElectricityCostsPerGHFloorArea[i] = totalElectricityCosts[i] / constant.greenhouseFloorArea

    # electricity profits
    totalElectricityProfits[i] = totalElectricitySales[i] - totalElectricityCosts[i]
    # electricity profits per greenhouse floor. unit: USD/m^2
    totalElectricityProfitsPerGHFloorArea[i] = totalPlantSalesesPerGHFloorArea[i] - totalElectricityCostsPerGHFloorArea[i]

    #  plant yield for a given period. unit:kg
    # totalGrowthFreshWeightsPerHead[i] =
    totalGrowthFreshWeightsPerCultivationFloorArea[i] = sum(simulatorClass.shootFreshMassPerAreaKgPerDay)
    totalGrowthFreshWeightsPerGHFloorArea[i] = totalGrowthFreshWeightsPerCultivationFloorArea[i] * constant.greenhouseCultivationFloorArea / constant.greenhouseFloorArea

    # unit harvested fresh mass weight for a whole given period with each OPV film coverage. unit: kg m-2
    # totalHarvestedShootFreshMassPerAreaKgPerHead[i] =
    totalHarvestedShootFreshMassPerCultivationFloorAreaKgPerDay[i] = sum(simulatorClass.harvestedShootFreshMassPerAreaKgPerDay)


    # plant sales per square meter with each OPV film coverage: [USD/m^2]
    # print("simulatorClass.totalPlantSalesperSquareMeter:{}".format(simulatorClass.totalPlantSalesperSquareMeter))
    totalPlantSalesesPerCultivationFloorArea[i] = simulatorClass.totalPlantSalesperSquareMeter
    # print("simulatorClass.totalPlantSalesPerGHFloorArea:{}".format(simulatorClass.totalPlantSalesPerGHFloorArea))
    totalPlantSalesesPerGHFloorArea[i] = simulatorClass.totalPlantSalesPerGHFloorArea

    # plant cost per square meter with each OPV film coverage: [USD/m^2]
    # print("simulatorClass.totalPlantProductionCostPerGHFloorArea:{}".format(simulatorClass.totalPlantProductionCostPerGHFloorArea))
    totalPlantCostsPerGHFloorArea[i] = simulatorClass.totalPlantProductionCostPerGHFloorArea

    # plant profit per square meter with each OPV film coverage: [USD/m^2]
    totalPlantProfitsPerGHFloorArea[i] = totalPlantSalesesPerGHFloorArea[i] - totalPlantCostsPerGHFloorArea[i]
    totalPlantProfits[i] = totalPlantProfitsPerGHFloorArea[i] * constant.greenhouseFloorArea

    # plant profit with each OPV film coverage: [USD/m^2]
    totalEconomicProfits[i] = totalElectricityProfits[i] + totalPlantProfitsPerGHFloorArea[i] * constant.greenhouseFloorArea

    economicProfitPerGHFloorArea[i] = simulatorClass.economicProfitPerGHFloorArea

  ######################################################
  ##### display the optimization results start #########
  ######################################################

  # print "plantCostperSquareMeter:{}".format(plantCostperSquareMeter)
  # print "unitDailyHarvestedFreshWeightList:{}".format(unitDailyHarvestedFreshWeightList)
  # print "plantSalesperSquareMeterList:{}".format(plantSalesperSquareMeterList)

  ################# plot the electricity yield with different OPV coverage for given period #################
  title = "total electricity sales per GH floor area vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "electricity sales per GH floor area[USD/m^2]"
  Util.plotData(OPVCoverages, totalElectricitySalesPerGHFloorArea, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  ######################################################################################## #############

  ################# plot the electricity yield with different OPV coverage for given period #################
  title = "harvested plant weights vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "harvested plant weight [kg]"
  Util.plotData(OPVCoverages, totalHarvestedShootFreshMassPerCultivationFloorAreaKgPerDay, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  ######################################################################################## #############

  ################# plot the electricity yield with different OPV coverage for given period #################
  title = "DLI to plants vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "DLI to plants [mol/m^2/day]"
  Util.plotData(OPVCoverages, totalDLIstoPlants, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  ######################################################################################## #############

  ################## plot various sales and cost
  plotDataSet = np.array([totalPlantSalesesPerGHFloorArea, totalPlantCostsPerGHFloorArea, totalElectricitySalesPerGHFloorArea, totalElectricityCostsPerGHFloorArea])
  labelList = np.array(["totalPlantSalesesPerGHFloorArea", "totalPlantCostsPerGHFloorArea", "totalElectricitySalesPerGHFloorArea", "totalElectricityCostsPerGHFloorArea"])
  title = "Various sales and cost"
  xAxisLabel = "time [day]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "Prcie per GH Floor area [USD/m^2]"
  Util.plotMultipleData(np.linspace(0, OPVCoverages.shape[0], OPVCoverages.shape[0]), plotDataSet, labelList, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  #######################################################################

  ################# plot the electricity yield with different OPV coverage for given period #################
  title = "electricity yield with a given area vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "electricity yield [kwh]"
  Util.plotData(OPVCoverages, totalkWhopvouts, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  ######################################################################################## #############

  ################# plot the plant profit with different OPV coverage for given period #################
  title = "plant profit with a given area vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "plant profit for a given period [USD]"
  Util.plotData(OPVCoverages, totalPlantProfitsPerGHFloorArea, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  ######################################################################################## #############

  ######################## plot by two y-axes ##########################
  title = "plant yield per area and electricity yield vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel1 = "plant fresh weight per cultivation floor for given period [kg/m^2]"
  yAxisLabel2 = "Electricity yield [kWh]"
  yLabel1 = "totalGrowthFreshWeights * greenhouseCultivationFloorArea"
  yLabel2 = "electricityYield[Kwh]"
  Util.plotTwoDataMultipleYaxes(OPVCoverages, totalGrowthFreshWeightsPerCultivationFloorArea * constant.greenhouseCultivationFloorArea, \
                                 totalkWhopvouts, title, xAxisLabel, yAxisLabel1, yAxisLabel2, yLabel1, yLabel2)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  #######################################################################

  ######################## plot by two y-axes ##########################
  title = "plant yield per area and electricity yield per foot print vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel1 = "plant fresh weight per foot print for given period [kg/m^2]"
  yAxisLabel2 = "Electricity yield per foot print [kW*h/m^2]"
  yLabel1 = "totalGrowthFreshWeightsPerGHFloorArea"
  yLabel2 = "totalkWhopvoutsPerGHFloorArea"
  Util.plotTwoDataMultipleYaxes(OPVCoverages, totalGrowthFreshWeightsPerGHFloorArea, \
                               totalkWhopvoutsPerGHFloorArea, title, xAxisLabel, yAxisLabel1, yAxisLabel2, yLabel1, yLabel2)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # #######################################################################

  # data export
  Util.exportCSVFile(
    np.array([OPVCoverages, totalkWhopvouts, totalkWhopvoutsPerGHFloorArea, totalGrowthFreshWeightsPerCultivationFloorArea * constant.greenhouseCultivationFloorArea,\
              totalGrowthFreshWeightsPerGHFloorArea,totalHarvestedShootFreshMassPerCultivationFloorAreaKgPerDay ]).T, \
    "PlantAndElectricityYieldWholeAndPerFootPrint")
  Util.exportCSVFile(
    np.array([OPVCoverages, totalElectricitySalesPerGHFloorArea, totalElectricityCostsPerGHFloorArea, totalPlantSalesesPerGHFloorArea, \
              totalPlantCostsPerGHFloorArea,totalEconomicProfits, economicProfitPerGHFloorArea]).T, \
    "SalesAndCostPerFootPrint")

  # plotting this graph is the coal of this simulation!!!
  ################# plot the economic profit with different OPV coverage for given period
  title = "whole economic profit with a given area vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "economic profit for a given period [USD]"
  Util.plotData(OPVCoverages, totalEconomicProfits, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # #######################################################################


  ################# plot the economic profit with different OPV coverage for given period per GH area
  title = "whole economic profit per GH area vs OPV film"
  xAxisLabel = "OPV Coverage Ratio [-]: " + constant.SimulationStartDate + "-" + constant.SimulationEndDate
  yAxisLabel = "economic profit for a given period [USD]"
  Util.plotData(OPVCoverages, economicProfitPerGHFloorArea, title, xAxisLabel, yAxisLabel)
  Util.saveFigure(title + " " + constant.SimulationStartDate + "-" + constant.SimulationEndDate)
  # #######################################################################


  ####################################################################################################
  # Stop execution here...
  # sys.exit()
  # Move the above line to different parts of the assignment as you implement more of the functionality.
  ####################################################################################################


###########################################################################################################
########################### Mixed integer non-liner programming with constraints###########################
###########################################################################################################
elif case == "OptimizationByMINLPSolver":
  print ("run SimulatorMINLPc.py")

  ########################################################################
  #
  #     This is an example call of MIDACO 5.0
  #     -------------------------------------
  #
  #     MIDACO solves Multi-Objective Mixed-Integer Non-Linear Problems:
  #
  #
  #      Minimize     F_1(X),... F_O(X)  where X(1,...N-NI)   is CONTINUOUS
  #                                      and   X(N-NI+1,...N) is DISCRETE
  #
  #      subject to   G_j(X)  =  0   (j=1,...ME)      equality constraints
  #                   G_j(X) >=  0   (j=ME+1,...M)  inequality constraints
  #
  #      and bounds   XL <= X <= XU
  #
  #
  #     The problem statement of this example is given below. You can use
  #     this example as template to run your own problem. To do so: Replace
  #     the objective functions 'F' (and in case the constraints 'G') given
  #     here with your own problem and follow the below instruction steps.
  #
  ########################################################################
  ######################   OPTIMIZATION PROBLEM   ########################
  ########################################################################
  def inputParameters(x):
    '''
    substitute the parameters to the simulator
    return: None
    '''

    # unit: [-]
    OPVAreaCoverageRatio = x[0]
    # set OPV coverage ratio [-]
    constant.OPVAreaCoverageRatio = OPVAreaCoverageRatio
    print("constant.OPVAreaCoverageRatio :{}".format(constant.OPVAreaCoverageRatio ))

    # change the other relevant parameters
    constant.OPVArea = OPVAreaCoverageRatio * constant.greenhouseTotalRoofArea
    constant.OPVAreaFacingEastOrNorthfacingRoof = OPVAreaCoverageRatio * (constant.greenhouseRoofTotalAreaEastOrNorth / constant.greenhouseTotalRoofArea)
    constant.OPVAreaFacingWestOrSouthfacingRoof = OPVAreaCoverageRatio * (constant.greenhouseRoofTotalAreaWestOrSouth / constant.greenhouseTotalRoofArea)

    # unit: [days] <- be careful this!!!!!!!!!! The hour is calculated from the beginning of the year (Jan 1st 0 am)
    shadingCurtainDeployStartDateSpring = x[1]
    shadingCurtainDeployEndDateSpring = x[2]
    shadingCurtainDeployStartDateFall = x[3]
    shadingCurtainDeployEndDateFall = x[4]
    # simulationEndDate = Util.getEndDateDateType()
    year = Util.getStartDateDateType().year


    shadingCurtainDeployStartDateSpring = datetime.date(year=year, month=1, day=1) + datetime.timedelta(days=shadingCurtainDeployStartDateSpring)
    shadingCurtainDeployEndDateSpring = datetime.date(year=year, month=1, day=1) + datetime.timedelta(days=shadingCurtainDeployEndDateSpring)
    shadingCurtainDeployStartDateFall = datetime.date(year=year, month=1, day=1) + datetime.timedelta(days=shadingCurtainDeployStartDateFall)
    shadingCurtainDeployEndDateFall = datetime.date(year=year, month=1, day=1) + datetime.timedelta(days=shadingCurtainDeployEndDateFall)
    print("shadingCurtainDeployStartDateSpring:{}".format(shadingCurtainDeployStartDateSpring))
    print("shadingCurtainDeployEndDateSpring:{}".format(shadingCurtainDeployEndDateSpring))
    print("shadingCurtainDeployStartDateFall:{}".format(shadingCurtainDeployStartDateFall))
    print("shadingCurtainDeployEndDateFall:{}".format(shadingCurtainDeployEndDateFall))

    # set the shading curtain deployment periods
    constant.ShadingCurtainDeployStartMMSpring = shadingCurtainDeployStartDateSpring.month
    constant.ShadingCurtainDeployStartDDSpring = shadingCurtainDeployStartDateSpring.day
    constant.ShadingCurtainDeployEndMMSpring = shadingCurtainDeployEndDateSpring.month
    constant.ShadingCurtainDeployEndDDSpring = shadingCurtainDeployEndDateSpring.day
    constant.ShadingCurtainDeployStartMMFall = shadingCurtainDeployStartDateFall.month
    constant.ShadingCurtainDeployStartDDFall = shadingCurtainDeployStartDateFall.day
    constant.ShadingCurtainDeployEndMMFall = shadingCurtainDeployEndDateFall.month
    constant.ShadingCurtainDeployEndDDFall = shadingCurtainDeployEndDateFall.day
    print("constant.ShadingCurtainDeployStartMMFall:{}".format(constant.ShadingCurtainDeployStartMMFall))
    print("constant.ShadingCurtainDeployStartDDFall:{}".format(constant.ShadingCurtainDeployStartDDFall))
    print("constant.ShadingCurtainDeployEndMMFall:{}".format(constant.ShadingCurtainDeployEndMMFall))
    print("constant.ShadingCurtainDeployEndDDFall:{}".format(constant.ShadingCurtainDeployEndDDFall))

    return None

  def problem_function(x):
    '''
    :param x: decision variables. In this model, the variables are pv module coverage ratio,
    '''

    f = [0.0] * 1  # Initialize array for objectives F(X)
    g = [0.0] * 3  # Initialize array for constraints G(X)

    # input the parameters at each iteration
    inputParameters(x)

    # Objective functions F(X)
    # call the simulator
    simulatorClass = Simulator1.simulateCropElectricityYieldProfit1()
    # print("simulatorClass.economicProfitPerGHFloorArea:{}".format(simulatorClass.economicProfitPerGHFloorArea))
    # since we need to maximize the objective function, the minus sign is added
    f[0] = -simulatorClass.economicProfitPerGHFloorArea

    #  Equality constraints G(X) = 0 MUST COME FIRST in g[0:me-1]
    #   No eauality constraints
    # Inequality constraints G(X) >= 0 MUST COME SECOND in g[me:m-1]
    shadingCurtainDeployStartDateSpring = x[1]
    shadingCurtainDeployEndDateSpring = x[2]
    shadingCurtainDeployStartDateFall = x[3]
    shadingCurtainDeployEndDateFall = x[4]
    g[0] = shadingCurtainDeployEndDateSpring - (shadingCurtainDeployStartDateSpring + 1)
    g[1] = shadingCurtainDeployStartDateFall - (shadingCurtainDeployEndDateSpring + 1)
    g[2] = shadingCurtainDeployEndDateFall - (shadingCurtainDeployStartDateFall + 1)

    # print("f:{}, g:{}".format(f,g))

    return f, g

  ########################################################################
  #########################   MAIN PROGRAM   #############################
  ########################################################################

  key = 'Kensaku_Okada_(University_of_Arizona)_[ACADEMIC-SINGLE-USER]'

  problem = {}  # Initialize dictionary containing problem specifications
  option = {}  # Initialize dictionary containing MIDACO options

  problem['@'] = problem_function  # Handle for problem function name

  ########################################################################
  ### Step 1: Problem definition     #####################################
  ########################################################################

  # STEP 1.A: Problem dimensions
  ##############################
  problem['o'] = 1  # Number of objectives
  problem['n'] = 5  # Number of variables (in total)
  problem['ni'] = 4  # Number of integer variables (0 <= ni <= n)
  problem['m'] = 3  # Number of constraints (in total)
  problem['me'] = 0  # Number of equality constraints (0 <= me <= m)

  # STEP 1.B: Lower and upper bounds 'xl' & 'xu'
  ##############################################
  # get the simulation period by hour [hours]
  numOfSimulationDays = Util.getSimulationDaysInt()-1
  # print("numOfSimulationDays:{}".format(numOfSimulationDays))
  problem['xl'] = [0.0, 1, 1, 1, 1]
  problem['xu'] = [1.0, numOfSimulationDays, numOfSimulationDays, numOfSimulationDays, numOfSimulationDays]

  # STEP 1.C: Starting point 'x'
  ##############################

  # start from the minimum values
  # problem['x'] = problem['xl']  # Here for example: starting point = lower bounds
  # # start from the middle values
  # problem['x'] = [(problem['xl'][i] + problem['xu'][i])/2.0 for i in range(0, len(problem['xl']))   ]  # start from the middle
  # # start from the maximum values
  # problem['x'] = problem['xu']  # Here for example: starting point = lower bounds
  # print("problem['x']:{}".format(problem['x']))
  # start from the minimum values for OPV coverage ratio and middle values for numOfSimulationDays, numOfSimulationDays, numOfSimulationDays, numOfSimulationDays
  # problem['x'] = [0.0, 183, 183, 183, 183]
  # start from the minimum values for numOfSimulationDays, numOfSimulationDays, numOfSimulationDays, numOfSimulationDays and middle value for OPV coverage ratio
  # problem['x'] = [0.5, 1, 1, 1, 1]
  # start from the max values for OPV coverage ratio and middle value for numOfSimulationDays, numOfSimulationDays, numOfSimulationDays, numOfSimulationDays
  problem['x'] = [0.0, 183, 183, 183, 183]


  ########################################################################
  ### Step 2: Choose stopping criteria and printing options    ###########
  ########################################################################

  # STEP 2.A: Stopping criteria
  #############################
  # option['maxeval'] = 10000  # Maximum number of function evaluation (e.g. 1000000), 999999999 (-> disabled)
  option['maxeval'] = 500  # Maximum number of function evaluation (e.g. 1000000), 999999999 (-> disabled)
  option['maxtime'] = 60 * 60 * 24  # Maximum time limit in Seconds (e.g. 1 Day = 60*60*24)

  # STEP 2.B: Printing options
  ############################
  option['printeval'] = 10  # Print-Frequency for current best solution (e.g. 1000)
  option['save2file'] = 1  # Save SCREEN and SOLUTION to TXT-files [0=NO/1=YES]

  ########################################################################
  ### Step 3: Choose MIDACO parameters (FOR ADVANCED USERS)    ###########
  ########################################################################

  # this parameter defines the accuracy for the constraint violation. It is considered an equality constraints (G(X)) to be feasible if |G(X)| <= PARAM(1).
  # An inequality is considered feasible, if G(X) ≥ -PARAM(1). If the user sets PARAM(1) = 0, MIDACO uses a default accuracy of 0.001.
  option['param1'] = 0.0  # ACCURACY
  # this defines the initial seed for MIDACO's internal pseudo random number generator.
  option['param2'] = 0.0  # SEED

  option['param3'] = 0.0  # FSTOP

  option['param4'] = 0.0  # ALGOSTOP

  # option['param5']  = 500.0005  # EVALSTOP
  option['param5'] = 0.0  # EVALSTOP

  # This parameter forces MIDACO to focus its search process around the current best solution and
	# thus makes it more greedy or local. The larger the FOCUS value, the closer MIDACO will focus its search on the current best solution.
	# option['param6'] = 0.0  # FOCUS
  # option['param6'] = 1.0  # FOCUS
  option['param6'] = 10.0  # FOCUS
  # option['param6'] = 20.0  # FOCUS

  option['param7'] = 0.0  # ANTS

  option['param8'] = 0.0  # KERNEL

 # This parameter speciﬁes a user given oracle parameter to the penalty function within MIDACO.
 # This parameter is only relevant for constrained problems.
  option['param9'] = 0.0  # ORACLE

  option['param10'] = 0.0  # PARETOMAX

  option['param11'] = 0.0  # EPSILON

  option['param12'] = 0.0  # CHARACTER

  ########################################################################
  ### Step 4: Choose Parallelization Factor   ############################
  ########################################################################

  # option['parallel'] = 10  # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
  option['parallel'] = 1  # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

  ########################################################################
  ############################ Run MIDACO ################################
  ########################################################################

  # add the directory to import MIDACO files
  sys.path.append("./MIDACO")
  import midaco

  if __name__ == '__main__':
    solution = midaco.run(problem, option, key)

  # print solution['f']
  # print solution['g']
  # print solution['x']

  print("simulation finished.")


########################### Reinforcement learning (q learning)###########################
elif case == "ShadingCurtainReinforcementLearning":
  # run simulateCropElectricityYieldProfit1 to set values to an object of CropElectricityYieldSimulator1
  cropElectricityYieldSimulator1, qLearningAgentsShadingCurtain = Simulator1.simulateCropElectricityYieldProfitRLShadingCurtain()


