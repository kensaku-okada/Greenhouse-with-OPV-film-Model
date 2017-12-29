import midaco
from scipy import stats
import datetime
import sys
import os as os
import numpy as np
# import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulator1 as Simulator1
import CropElectricityYeildSimulatorDetail as simulatorDetail
import CropElectricityYeildSimulatorConstant as constant
# import TwoDimLeastSquareAnalysis as TwoDimLS
import Util as util
import Lettuce


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

# STEP 0: Problem dimensions parametrization so that we can use the same number in problem_function function
##############################
numOfObjectives = 1
numOfVariablesInTotal = 1
numOfIntegerVariables = 0
numOfConstraintsInTotal = 1
numOfEqualityConstraints = 1

########################################################################
######################   OPTIMIZATION PROBLEM   ########################
########################################################################
def problem_function(x):

  # print ("datetime.datetime.now():{}".format(datetime.datetime.now()))

  #######################################################################################
  ########## Objective functions F(X)
  #######################################################################################
  numOfConstraints = problem['m']
  # print ("numOfConstraints:{}".format(numOfConstraints))
  f = [0.0] * numOfObjectives # Initialize array for objectives F(X)
  g = [0.0] * numOfConstraintsInTotal # Initialize array for constraints G(X)

  ##########define the constant values (not define as decision variables)##########
  # run simulateCropElectricityYieldProfit1 to set values to an object of CropElectricityYieldSimulator1
  cropElectricityYieldSimulator1 = Simulator1.simulateCropElectricityYieldProfitForMINLP()

  # get the electricity sales per area for given period [USD/m^2]
  monthlyElectricitySalesperArea = cropElectricityYieldSimulator1.getMonthlyElectricitySalesperArea()
  electricitySalesperArea = sum(monthlyElectricitySalesperArea)

  #TODO for obtaining an interest result by simulation, it is assumed that the cost of OPV is zero. change it when you want to know about the real situation.
  oPVCostUSDForDepreciationperArea = cropElectricityYieldSimulator1.getMonthlyElectricitySalesperArea()
  oPVCostUSDForDepreciationperArea = 0.0
  ##########define the constant values (not define as decision variables) end##########

  #######################################################################################
  ########## [Model of electricity sales]##########
  #######################################################################################
  electricitySales = (x[0] * constant.greenhouseRoofArea) * electricitySalesperArea

  #######################################################################################
  ########## [Model of economic cost of electricity] ##########
  #######################################################################################
  OPVCostUSDForDepreciation = oPVCostUSDForDepreciationperArea * (x[0] * constant.greenhouseRoofArea)

  #######################################################################################
  ########## [Model of economic profit of electricity] start ##########
  #######################################################################################
  # Profit_ele[1] - ( Sales_ele[4] - Cost_ele[5] ) = 0
  electricityProfit = electricitySales - OPVCostUSDForDepreciation
  #######################################################################################
  ########## [Model of economic profit of electricity] end ##########
  #######################################################################################


  # Both of these are done with a function made for the simulation
  #######################################################################################
  ##########  [Model of solar radiation to plants through OPV film and greenhouse glazing film] ##########
  #######################################################################################
  #######################################################################################
  ##########  [Model of plant yield] ##########
  #######################################################################################
  # [String]
  plantGrowthModel = constant.TaylorExpantionWithFluctuatingDLI
  # cultivation days per harvest [days/harvest]
  cultivationDaysperHarvest = constant.cultivationDaysperHarvest
  # boolean
  hasShadingCurtain = constant.hasShadingCurtain
  # PPFD [umol m^-2 s^-1]
  ShadingCurtainDeployPPFD = constant.ShadingCurtainDeployPPFD

  ##################calculate the plant yield
  # calculate plant yield [g/unit]
  _, _, _, unitDailyHarvestedFreshWeight = \
    simulatorDetail.calcPlantYieldSimulation(plantGrowthModel, cultivationDaysperHarvest, x[0], \
         (cropElectricityYieldSimulator1.getDirectPPFDToOPVEastDirection() + cropElectricityYieldSimulator1.getDirectPPFDToOPVWestDirection()) / 2.0, \
          cropElectricityYieldSimulator1.getDiffusePPFDToOPV(), cropElectricityYieldSimulator1.getGroundReflectedPPFDToOPV(), \
          hasShadingCurtain, ShadingCurtainDeployPPFD)
  #######################################################################################
  ##########  [Model of solar radiation to plants through OPV film and greenhouse glazing film] end ##########
  #######################################################################################
  #######################################################################################
  ##########  [Model of plant yield] end ##########
  #######################################################################################

  #######################################################################################
  ##########  [Model of economic sales of plants] start ##########
  #######################################################################################
  # unit conversion; get the daily plant yield per given period per area: [g/unit] -> [g/m^2]
  dailyHarvestedFreshWeightperArea = util.convertUnitShootFreshMassToShootFreshMassperArea(unitDailyHarvestedFreshWeight)
  # unit conversion:  [g/m^2] -> [kg/m^2]1
  dailyHarvestedFreshWeightperAreaKg = util.convertFromgramTokilogram(dailyHarvestedFreshWeightperArea)

  # get the sales price of plant [USD/m^2]
  # if the average DLI during each harvest term is more than 17 mol/m^2/day, discount the price
  # TODO may need to improve the affect of Tipburn
  dailyPlantSalesperSquareMeter = simulatorDetail.getPlantSalesperSquareMeter(cropElectricityYieldSimulator1.getYear(), dailyHarvestedFreshWeightperAreaKg, \
                                                                              cropElectricityYieldSimulator1.getTotalDLItoPlants())
  plantSalesperSquareMeter = sum(dailyPlantSalesperSquareMeter)
  # print "dailyPlantSalesperSquareMeter.shape:{}".format(dailyPlantSalesperSquareMeter.shape)
  #######################################################################################
  ##########  [Model of economic sales of plants] end ##########
  #######################################################################################

  #######################################################################################
  ##########  [Model of economic cost of plants] start ##########
  #######################################################################################
  # plant operation cost per square meter for given simulation period [USD/m^2]
  plantCostperSquareMeter = simulatorDetail.getPlantCostperSquareMeter(util.getSimulationMonthsInt())

  #######################################################################################
  ##########  [Model of economic cost of plants] end ##########
  #######################################################################################

  #######################################################################################
  ##########  [Model of economic profit of plants] start ##########
  #######################################################################################
  ##################plant profit per square meter with each OPV film coverage: [USD/m^2]
  plantProfitperSquareMeter = plantSalesperSquareMeter - plantCostperSquareMeter
  # print "plantProfitperSquareMeterList[i]:{}".format(plantProfitperSquareMeterList[i])
  # print "plantProfitperSquareMeterList[{}]:{}".format(i, plantProfitperSquareMeterList[i])
  plantProfit = plantProfitperSquareMeter * constant.greenhouseCultivationFloorArea

  #######################################################################################
  ##########  [Model of economic profit of plants] end ##########
  #######################################################################################

  # Profit_all = Profit_plantx[0] + Profit_elex[1]. Since we want to maximize the objective function, the minus sign is added.

  f[0] = -(plantProfit + electricityProfit)

  return f,g

########################################################################
#########################   MAIN PROGRAM   #############################
########################################################################

key = 'Kensaku_Okada____[-TRIAL-LICENSE-valid-until-1st-June-2017-]'

problem = {} # Initialize dictionary containing problem specifications
option  = {} # Initialize dictionary containing MIDACO options

problem['@'] = problem_function # Handle for problem function name

########################################################################
### Step 1: Problem definition     #####################################
########################################################################
# STEP 1.A: Problem dimensions
##############################
problem['o']  = numOfObjectives  # Number of objectives
problem['n']  = numOfVariablesInTotal  # Number of variables (in total)
problem['ni'] = numOfIntegerVariables  # Number of integer variables (0 <= ni <= n)
problem['m']  = numOfConstraintsInTotal  # Number of constraints (in total)
problem['me'] = numOfEqualityConstraints  # Number of equality constraints (0 <= me <= m)


# STEP 1.B: Lower and upper bounds 'xl' & 'xu'  
##############################################
# discrete variables come last
problem['xl'] = [ 0.0 ]
problem['xu'] = [ 1.0 ]

# if you want to regard t1 ~ y4 as decision variable (binary variables which decide ), you need to define them for the number of for loop == 24 * simulation days
# e.g. if you simulate for 365 days, the num of each decision variable will be 8760 (= 24 * 365). So, we need to define more than 30000 decision variables.
# problem['xl'] = [ 0.0] +  ([ 0] * constant.hourperDay * util.calcSimulationDaysInt() * 4)
# problem['xu'] = [ 1.0] +  ([ 1] * constant.hourperDay * util.calcSimulationDaysInt() * 4)

# STEP 1.C: Starting point 'x'  
##############################  
problem['x'] = problem['xl'] # Here for example: starting point = lower bounds
    
########################################################################
### Step 2: Choose stopping criteria and printing options    ###########
########################################################################
   
# STEP 2.A: Stopping criteria 
#############################
# option['maxeval'] = 10000     # Maximum number of function evaluation (e.g. 1000000)
# option['maxtime'] = 60*60*24  # Maximum time limit in Seconds (e.g. 1 Day = 60*60*24)
option['maxeval'] = 10000     # Maximum number of function evaluation (e.g. 1000000)
option['maxtime'] = 60*20  # Maximum time limit in Seconds (e.g. 1 Day = 60*60*24)


# STEP 2.B: Printing options  
############################ 
option['printeval'] = 100  # Print-Frequency for current best solution (e.g. 1000)
option['save2file'] = 1     # Save SCREEN and SOLUTION to TXT-files [0=NO/1=YES]

########################################################################
### Step 3: Choose MIDACO parameters (FOR ADVANCED USERS)    ###########
########################################################################

option['param1']  = 0.0  # ACCURACY  
option['param2']  = 0.0  # SEED  
option['param3']  = 0.0  # FSTOP  
option['param4']  = 0.0  # ALGOSTOP  
option['param5']  = 0.0  # EVALSTOP  
option['param6']  = 0.0  # FOCUS  
option['param7']  = 0.0  # ANTS  
option['param8']  = 0.0  # KERNEL  
option['param9']  = 0.0  # ORACLE  
option['param10'] = 0.0  # PARETOMAX
option['param11'] = 0.0  # EPSILON  
option['param12'] = 0.0  # CHARACTER

########################################################################
### Step 4: Choose Parallelization Factor   ############################
########################################################################

option['parallel'] = 0 # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

########################################################################
############################ Run MIDACO ################################
########################################################################

if __name__ == '__main__': 

  solution = midaco.run( problem, option, key )

# print solution['f']
# print solution['g']
# print solution['x']

########################################################################
############################ END OF FILE ###############################
########################################################################
