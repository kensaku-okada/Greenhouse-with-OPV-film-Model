# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 12 Dec 2016
# last edit date: 14 Dec 2016
#######################################################

##########import package files##########
from scipy import stats
import os as os
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
import datetime
import sys
#######################################################


def calcDailyInnerLightIntensityPPFDSum (HourlyInnerLightIntensityPPFD, productionCycle, cultivationDaysperHarvest, dayOfCultivation):
    '''
    sum all of the hourly light intensity for a specific cultivation day

    param:HourlyInnerLightIntensityPPFD (μmol/m^2/s)
    param:productionCycle (-)
    param:cultivationDaysperHarvest (days)
    param:dayOfCultivation (th day)

    return:dailyInnerLightIntensityPPFD (μmol/m^2/s)
    '''
    #unit: (μmol/m^2/s)
    dailyInnerLightIntensityPPFDsum = 0.0

    # sum hourly solra radiation to the daily radiation
    for hour in range (0, int(constant.hourperDay)):
        dailyInnerLightIntensityPPFDsum += HourlyInnerLightIntensityPPFD[productionCycle * cultivationDaysperHarvest * int(constant.hourperDay) + dayOfCultivation * int(constant.hourperDay) + hour]

    return dailyInnerLightIntensityPPFDsum


def calcDailyFreshWeightIncreaseByShimizuEtAl2008Revised(dailyInnerLightIntensityDLI, cultivationDaysperHarvest):
    '''
    calculate the fresh weight increase per day based on the revised model of Shimizu et at (2008): Hiroshi SHIMIZU, Megumi KUSHIDA and Wataru FUJINUMA, 2008, “A Growth Model for Leaf Lettuce under Greenhouse Environments”
    The detail is described at ProjectB INFO 521

    param:dailyInnerLightIntensityPPFD [μmol/m^2/s]
    return: dailyFreshWeightIncrease[g/day]
    '''
    print("dailyInnerLightIntensityDLI:{}".format(dailyInnerLightIntensityDLI))
    print("cultivationDaysperHarvest:{}".format(cultivationDaysperHarvest))

    # average the light intensity for the cultivation　by the period of lighting (photoperiod), which is assumed to be 14 hours.
    dailyInnerLightIntensityDLIAverage = dailyInnerLightIntensityDLI / constant.photoperiod
    # print "dailyInnerLightIntensityPPFDAverage:{}".format(dailyInnerLightIntensityPPFDAverage)

    # the expected fresh weight at harvest. the unit is [g] coding Eq. 1-3-2-6 and 1-3-2-7
    # the minimum final weight [g]
    finalWeightperHarvest = 8.72

    if dailyInnerLightIntensityDLIAverage < 1330:
        # finalWeightperHarvest = 0.00000060 * HourlyinnerLightIntensityPPFDAveragePerproductionCycle**3 - 0.00162758 * HourlyinnerLightIntensityPPFDAveragePerproductionCycle**2 + 1.14477896 * HourlyinnerLightIntensityPPFDAveragePerproductionCycle - 46.39100859
        finalWeightperHarvest = 0.00000060 * dailyInnerLightIntensityDLIAverage ** 3 - 0.00162758 * dailyInnerLightIntensityDLIAverage ** 2 + 1.14477896 * dailyInnerLightIntensityDLIAverage - 46.39100859

    # the actual fresh weight of crop per harvest. the unit is g . Eq 1-3-2-4
    dailyFreshWeightIncrease = (9.0977 * finalWeightperHarvest - 17.254) * (7.26 * 10 ** (-5)) ** math.e ** (
    -0.05041 * cultivationDaysperHarvest)

    return dailyFreshWeightIncrease


def calcUnitDailyFreshWeightBoth2003TaylorExpantionWithVaryingDLI(hourlyInnerPPFDToPlants, cultivationDaysperHarvest, cropElectricityYieldSimulator1 = None):
    '''
    calculate the unit fresh weight increase per day based on the revised model of Both (2003):
    Both, A., 2003. Ten years of hydroponic lettuce research. Knowledgecenter.Illumitex.Com 18, 8.

    param:hourlyInnerPPFDToPlants [μmol/m^2/s] per day
    param:cultivationDaysperHarvest [days] per day
    return: dailyFreshWeightIncrease[g/day]
    return: hervestDay[days]: days after seeeding
    '''
    # print "dailyInnerLightIntensityDLI:{}".format(dailyInnerLightIntensityDLI)
    # print "cultivationDaysperHarvest:{}".format(cultivationDaysperHarvest)

    # convert PPFD to DLI
    innerDLIToPlants = util.convertFromHourlyPPFDWholeDayToDLI(hourlyInnerPPFDToPlants)
    # print "innerDLIToPlants:{}".format(innerDLIToPlants)

    shootFreshMassList, unitDailyFreshWeightIncrease,accumulatedUnitDailyFreshWeightIncrease,unitHarvestedFreshWeight = \
      calcUnitDailyFreshWeightBoth2003TaylorExpantionWithVaryingDLIDetail(innerDLIToPlants, cultivationDaysperHarvest, cropElectricityYieldSimulator1)

    return shootFreshMassList, unitDailyFreshWeightIncrease,accumulatedUnitDailyFreshWeightIncrease,unitHarvestedFreshWeight


def calcUnitDailyFreshWeightBoth2003TaylorExpantionWithVaryingDLIDetail(innerDLIToPlants, cultivationDaysperHarvest, cropElectricityYieldSimulator1 = None):
  '''
  calculate the unit fresh weight increase per day based on the revised model of Both (2003):
  Both, A., 2003. Ten years of hydroponic lettuce research. Knowledgecenter.Illumitex.Com 18, 8.

  param:hourlyInnerPPFDToPlants [μmol/m^2/s] per day
  param:cultivationDaysperHarvest [days] per day
  return: dailyFreshWeightIncrease[g/day]
  return: hervestDay[days]: days after seeeding
  '''

  # if you continue to grow plant during the summer period, then this is true
  ifGrowForSummerPeriod = cropElectricityYieldSimulator1.getIfGrowForSummerPeriod()
  # print ("ifGrowForSummerPeriod:{}".format(ifGrowForSummerPeriod))

  # take date and time
  year = cropElectricityYieldSimulator1.getYear()
  month = cropElectricityYieldSimulator1.getMonth()
  day = cropElectricityYieldSimulator1.getDay()

  # change the number of array for DLI
  yearEachDay = year[::24]
  monthEachDay = month[::24]
  dayEachDay = day[::24]

  # define statistics for calculation

  # daily unit plant weight on each cycle [g]
  shootDryMassList = np.zeros(util.calcSimulationDaysInt())
  # d_shootDryMassList = np.zeros(util.calcSimulationDaysInt())
  # dd_shootDryMassList = np.zeros(util.calcSimulationDaysInt())
  # ddd_shootDryMassList = np.zeros(util.calcSimulationDaysInt())

  # daily increase in unit plant weight [g]
  unitDailyFreshWeightIncrease = np.zeros(util.calcSimulationDaysInt())
  # accumulated weight of daily increase in unit plant weight during the whole simulation days [g]
  accumulatedUnitDailyFreshWeightIncrease = np.zeros(util.calcSimulationDaysInt())
  # harvested daily unit plant weight [g]
  unitHarvestedFreshWeight = np.zeros(util.calcSimulationDaysInt())
  # the average light DLi of each cultivation cycle, the data is stored in the element on the harvest date.
  # this data is used to calculate the penalty of plant yield by photo inhibition.
  averageDLIonEachCycle = np.zeros(util.calcSimulationDaysInt())
  # time step[day]
  dt = 1

  shootDryMassInit = 0.0001
  ifharvestedLastDay = False

  # the initial harvest days
  harvestDaysList = np.array(range(cultivationDaysperHarvest - 1, util.getSimulationDaysInt(), cultivationDaysperHarvest))
  # print ("harvestDaysList:{}".format(harvestDaysList))

  # the variable storing the cultivation start day on each cycle
  CultivationCycleStartDay = datetime.date(yearEachDay[0], monthEachDay[0], dayEachDay[0])
  # CultivationCycleEndtDay = datetime.date(yearEachDay[0], monthEachDay[0], dayEachDay[0])

  i = 0
  # print "cycle * cultivationDaysperHarvest -1:{}".format(accumulatedUnitDailyFreshWeightIncrease[0 * cultivationDaysperHarvest -1])
  while i  < util.getSimulationDaysInt():

    DaysperCycle = datetime.timedelta(days = cultivationDaysperHarvest)
    # if ifGrowForSummerPeriod is False the end of the cultivation at a cycle is within the summer period, then skip the cycle (= plus 35 days to index)
    if ifGrowForSummerPeriod is False and i % cultivationDaysperHarvest == 0 and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) + DaysperCycle >= datetime.date(yearEachDay[i], constant.SummerPeriodStartMM, constant.SummerPeriodStartDD) and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) + DaysperCycle <= datetime.date(yearEachDay[i], constant.SummerPeriodEndMM, constant.SummerPeriodEndDD):
      # skip the cultivation cycle
      i += cultivationDaysperHarvest
      continue

    # if ifGrowForSummerPeriod is False, and the end of the cultivation at a cycle is not within the summer period, but the first day is within the summer period, then shift the first day to
    # the next day of the summer period, and shift all of the cultivation days in harvestDaysList
    elif ifGrowForSummerPeriod is False and i % cultivationDaysperHarvest == 0 and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) >= datetime.date(yearEachDay[i], constant.SummerPeriodStartMM, constant.SummerPeriodStartDD) and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) <= datetime.date(yearEachDay[i], constant.SummerPeriodEndMM, constant.SummerPeriodEndDD):
      # shift the first day to the next day of the summer period
      dateDiff = datetime.date(yearEachDay[i], constant.SummerPeriodEndMM, constant.SummerPeriodEndDD) - datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i])
      i += dateDiff.days + 1

      # shift each harvest period by dateDiff to keep the harvest period cultivationDaysperHarvest even after atarting the cultivation next to the summer period.
      harvestDaysList += dateDiff.days + 1

      continue

    # define the initial values on each cycle [g]
    if ifharvestedLastDay == True or i == 0:
    # if i % cultivationDaysperHarvest == 0:
    #   print ("when if ifharvestedLastDay == True, i :{}".format(i))
      # plant the new seed
      shootDryMassList[i] = shootDryMassInit

      CultivationCycleStartDay = datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i])
      # print ("cultivation start date:{}".format(CultivationCycleStartDay))

      ifharvestedLastDay = False

    # calculate the plant weight increase
    else:
      # the additional number 1 indicates the difference from the last cultivation day. The difference calculate the increase in calcUnitDailyFreshWeightIncreaseBoth2003TaylorNotForRL
      # daysFromSeeding = i % cultivationDaysperHarvest + 1
      daysFromSeeding = (datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) - CultivationCycleStartDay).days + 1
      # print("daysFromSeeding:{}".format(daysFromSeeding))

      unitDailyFreshWeightIncrease[i]  = calcUnitDailyFreshWeightIncreaseBoth2003TaylorNotForRL(innerDLIToPlants[i], shootDryMassList[i], dt, daysFromSeeding)

      shootDryMassList[i] = shootDryMassList[i - 1] +  unitDailyFreshWeightIncrease[i]

    # since all of the initial values of accumulatedUnitDailyFreshWeightIncrease is zero, the value becomes zero when index == 0
    accumulatedUnitDailyFreshWeightIncrease[i] = accumulatedUnitDailyFreshWeightIncrease[i - 1] + unitDailyFreshWeightIncrease[i]

    # if it takes 35 days from seedling, harvest the plants!! the harvested fresh weight becomes just zero when index is zero because the initial values are zero.
    # print("i:{}, np.where(harvestDaysList == i)[0].shape[0]:{}".format(i, np.where(harvestDaysList == i)[0].shape[0]))
    if np.where(harvestDaysList == i)[0].shape[0] == 1:
    # since the initial element index starts from zero, cultivationDaysperHarvest is minused by 1.
    # if i % cultivationDaysperHarvest == cultivationDaysperHarvest - 1:
    #   print("harvest plants, i:{}".format(i))

      unitHarvestedFreshWeight[i] = shootDryMassList[i]
      averageDLIonEachCycle[i] = np.mean(innerDLIToPlants[i-(cultivationDaysperHarvest - 1):i+1])

      ifharvestedLastDay = True

      # delete the harvest day from harvestDaysList
      # harvestDaysList = np.array([harvestDaysList[j] for j in range (0, harvestDaysList.shape[0]) if harvestDaysList[j] != i and harvestDaysList[j] > i ])
      harvestDaysList = np.array([harvestDaysList[j] for j in range (0, harvestDaysList.shape[0]) if harvestDaysList[j] > i ])
      # np.delete(harvestDaysList, np.where(harvestDaysList == i)[0][0])
      # print("current harvestDaysList:{}".format(harvestDaysList))

    # increment the counter
    i += 1

  # change dry mass weight into fresh mass weight
  # daily increase in unit plant weight [g]
  unitDailyFreshWeightIncrease = unitDailyFreshWeightIncrease * constant.DryMassToFreshMass
  # accumulated weight of daily increase in unit plant weight during the whole simulation days [g]
  accumulatedUnitDailyFreshWeightIncrease = accumulatedUnitDailyFreshWeightIncrease * constant.DryMassToFreshMass
  # harvested daily unit plant weight [g]
  unitHarvestedFreshWeight = unitHarvestedFreshWeight * constant.DryMassToFreshMass
  # daily unit plant weight on each cycle [g]
  shootFreshMassList = shootDryMassList * constant.DryMassToFreshMass

  # print "shootDryMassList:{}".format(shootDryMassList)
  # print "unitDailyFreshWeightIncrease:{}".format(unitDailyFreshWeightIncrease)
  # print "accumulatedUnitDailyFreshWeightIncrease:{}".format(accumulatedUnitDailyFreshWeightIncrease)
  # print "unitHarvestedFreshWeight:{}".format(unitHarvestedFreshWeight)

  # set the average light DLi of each cultivation cycle, the data is stored in the element on the harvest date.
  cropElectricityYieldSimulator1.setAverageDLIonEachCycle(averageDLIonEachCycle)

  return shootFreshMassList, unitDailyFreshWeightIncrease, accumulatedUnitDailyFreshWeightIncrease, unitHarvestedFreshWeight


def calcUnitDailyFreshWeightIncreaseBoth2003TaylorNotForRL(innerDLIToPlants, shootDryMassList, dt, daysFromSeeding):
  '''
  this function is for general simulation. This is more accurate than calcUnitDailyFreshWeightIncreaseBoth2003Taylor, which should be replaced later.

  :param innerDLIToPlants:
  :param shootDryMassList:
  :param dt:
  :return:
  '''

  # update each statistic each day
  a = -8.596 + 0.0743 * innerDLIToPlants
  b = 0.4822
  c = -0.006225


  shootDryMassList = math.e ** (a + b * daysFromSeeding + c * daysFromSeeding ** 2)
  d_shootDryMassList = (b + 2 * c * daysFromSeeding) * shootDryMassList
  dd_shootDryMassList = 2 * c * shootDryMassList + (b + 2 * c * daysFromSeeding) ** 2 * shootDryMassList
  ddd_shootDryMassList = 2 * c * d_shootDryMassList + 4 * c * (b + 2 * c * daysFromSeeding) * shootDryMassList + (b + 2 * c * daysFromSeeding) ** 2 * d_shootDryMassList

  # Taylor expansion: x_0 = 0, h = 1 (source: http://eman-physics.net/math/taylor.html)
  shootDryMassIncrease =  1.0 / (math.factorial(1)) * d_shootDryMassList * dt + 1.0 / (math.factorial(2)) * dd_shootDryMassList * ((dt) ** 2) + \
                          1.0 / (math.factorial(3)) * ddd_shootDryMassList * ((dt) ** 3)

  return shootDryMassIncrease

# def calcUnitDailyFreshWeightIncreaseBoth2003Taylor(innerDLIToPlants, cultivationDaysperHarvest, daysFromSeeding):
#   '''
#   this function is only for the Q learning reinforcement learning
#   calculate the unit fresh weight increase per day based on the revised model of Both (2003):
#   Both, A., 2003. Ten years of hydroponic lettuce research. Knowledgecenter.Illumitex.Com 18, 8.
#
#   param:innerDLIToPlants [mol/m^2/day] per day
#   param:cultivationDaysperHarvest [days] per day
#   param:daysFromSeeding [days] per day
#
#   return: dailyFreshWeightIncrease[g/day]
#   return: hervestDay[days]: days after seeeding
#   '''
#   # print "dailyInnerLightIntensityDLI:{}".format(dailyInnerLightIntensityDLI)
#   # print "cultivationDaysperHarvest:{}".format(cultivationDaysperHarvest)
#
#   # daily increase in unit plant weight [g]
#   unitDailyFreshWeightIncrease = np.zeros(1)
#   # accumulated weight of daily increase in unit plant weight during the whole simulation days [g]
#   accumulatedUnitDailyFreshWeightIncrease = np.zeros(1)
#   # harvested daily unit plant weight [g]
#   unitHarvestedFreshWeight = np.zeros(1)
#
#   # simulationDaysInt = util.calcSimulationDaysInt()
#   simulationDaysInt = 1
#
#   # num of cultivation cycle
#   NumCultivationCycle = 0
#   # print ("NumCultivationCycle:{}".format(NumCultivationCycle))
#
#   # num of remained days when we cannot finish the cultivation, which is less than the num of cultivation days.
#   CultivationDaysWithNoHarvest = simulationDaysInt - NumCultivationCycle * cultivationDaysperHarvest
#   # print "CultivationDaysWithNoHarvest:{}".format(CultivationDaysWithNoHarvest)
#
#   # define statistics for calculation
#   # daily unit plant weight on each cycle [g]
#   shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
#   d_shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
#   # dd_shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
#   # ddd_shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
#   a = 0
#   b = 0.4822
#   c = -0.006225
#   # time step[day]
#   dt = 1
#
#   # print "cycle * cultivationDaysperHarvest -1:{}".format(accumulatedUnitDailyFreshWeightIncrease[0 * cultivationDaysperHarvest -1])
#
#   for cycle in range(0, NumCultivationCycle + 1):
#
#     # define the initial values on each cycle [g]
#     # shootDryMassInit == the weight on day 0 == weight of seed [g]
#     shootDryMassInit = 0.0001
#     accumulatedUnitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest] = accumulatedUnitDailyFreshWeightIncrease[
#                                                                                    cycle * cultivationDaysperHarvest - 1] + shootDryMassInit
#     shootDryMassList[cycle * cultivationDaysperHarvest] = shootDryMassInit
#     d_shootDryMassList[cycle * cultivationDaysperHarvest] = (b + 2 * c * 0.0) * shootDryMassList[cycle * cultivationDaysperHarvest]
#     # dd_shootDryMassList[cycle * cultivationDaysperHarvest] = 2 * c * shootDryMassList[cycle * cultivationDaysperHarvest] + \
#     #                                                          (b + 2 * c * 0.0) ** 2 * shootDryMassList[cycle * cultivationDaysperHarvest]
#     # ddd_shootDryMassList[cycle * cultivationDaysperHarvest] = 2 * c * d_shootDryMassList[cycle * cultivationDaysperHarvest] + \
#     #                                                           4 * c * (b + 2 * c * 0.0) * shootDryMassList[cycle * cultivationDaysperHarvest] + \
#     #                                                           (b + 2 * c * 0) ** 2 * d_shootDryMassList[cycle * cultivationDaysperHarvest]
#
#     # print "shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(shootDryMassList[cycle*cultivationDaysperHarvest])
#     # print "d_shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(d_shootDryMassList[cycle*cultivationDaysperHarvest])
#     # print "dd_shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(dd_shootDryMassList[cycle*cultivationDaysperHarvest])
#     # print "ddd_shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(ddd_shootDryMassList[cycle*cultivationDaysperHarvest])
#
#
#     # update each statistic each day
#     a = -8.596 + 0.0743 * innerDLIToPlants
#     shootDryMassList = math.e ** (a + b * daysFromSeeding + c * daysFromSeeding ** 2)
#     d_shootDryMassList = (b + 2 * c * daysFromSeeding) * shootDryMassList
#     dd_shootDryMassList = 2 * c * shootDryMassList + (b + 2 * c * daysFromSeeding) ** 2 * shootDryMassList
#     ddd_shootDryMassList = 2 * c * d_shootDryMassList + 4 * c * (b + 2 * c * daysFromSeeding) * shootDryMassList + \
#                            (b + 2 * c * daysFromSeeding) ** 2 * d_shootDryMassList
#
#     # print "day{}, a:{},shootDryMassList[{}]:{}".format(day, a, cycle*cultivationDaysperHarvest+day, shootDryMassList[cycle*cultivationDaysperHarvest+day])
#
#     # Taylor expansion: x_0 = 0, h = 1 (source: http://eman-physics.net/math/taylor.html)
#     # shootDryMassList[cycle * cultivationDaysperHarvest + day] = shootDryMassList[cycle * cultivationDaysperHarvest + day - 1] + \
#     #                                                             1.0 / (math.factorial(1)) * d_shootDryMassList[
#     #                                                               cycle * cultivationDaysperHarvest + day - 1] * dt + \
#     #                                                             1.0 / (math.factorial(2)) * dd_shootDryMassList[
#     #                                                               cycle * cultivationDaysperHarvest + day - 1] * ((dt) ** 2) + \
#     #                                                             1.0 / (math.factorial(3)) * ddd_shootDryMassList[
#     #                                                               cycle * cultivationDaysperHarvest + day - 1] * ((dt) ** 3)
#
#     # unitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest + day] = shootDryMassList[cycle * cultivationDaysperHarvest + day] - \
#     #                                                                         shootDryMassList[cycle * cultivationDaysperHarvest + day - 1]
#     unitDailyFreshWeightIncrease = d_shootDryMassList
#
#     # accumulatedUnitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest + day] = \
#     #   accumulatedUnitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest + day - 1] + unitDailyFreshWeightIncrease[
#     #     cycle * cultivationDaysperHarvest + day]
#
#     # print "day:{}, cycle*cultivationDaysperHarvest+day:{}, shootDryMassList[cycle*cultivationDaysperHarvest + day]:{}".format(
#     #     day, cycle * cultivationDaysperHarvest + day, shootDryMassList[cycle * cultivationDaysperHarvest + day])
#
#   # change dry mass weight into fresh mass weight
#   # daily increase in unit plant weight [g]
#   unitDailyFreshWeightIncrease = unitDailyFreshWeightIncrease * constant.DryMassToFreshMass
#   # accumulated weight of daily increase in unit plant weight during the whole simulation days [g]
#   # accumulatedUnitDailyFreshWeightIncrease = accumulatedUnitDailyFreshWeightIncrease * constant.DryMassToFreshMass
#   # harvested daily unit plant weight [g]
#   # unitHarvestedFreshWeight = unitHarvestedFreshWeight * constant.DryMassToFreshMass
#   # daily unit plant weight on each cycle [g]
#   # shootFreshMassList = shootDryMassList * constant.DryMassToFreshMass
#
#   # print "shootDryMassList:{}".format(shootDryMassList)
#   # print "unitDailyFreshWeightIncrease:{}".format(unitDailyFreshWeightIncrease)
#   # print "accumulatedUnitDailyFreshWeightIncrease:{}".format(accumulatedUnitDailyFreshWeightIncrease)
#   # print "unitHarvestedFreshWeight:{}".format(unitHarvestedFreshWeight)
#
#   return unitDailyFreshWeightIncrease

def getLettucePricepercwt(year):
    '''
    return the lettuce price per cwt based on the year of sales
    :param year:
    :return:
    '''
    return 0.583 * year - 1130


def getRetailPricePerArea(simulatorClass):
    # the source of the romaine lettuce retail price data
    # https://data.bls.gov/timeseries/APU0000FL2101?amp%253bdata_tool=XGtable&output_view=data&include_graphs=true

    # unit: kg/m^2/day
    harvestedShootFreshMassPerAreaKgPerDay = simulatorClass.harvestedShootFreshMassPerAreaKgPerDay
    # print("harvestedShootFreshMassPerAreaKgPerDay:{}".format(harvestedShootFreshMassPerAreaKgPerDay))

    # unit: USD/m^2/day
    harvestedFreshMassPricePerAreaPerDay = np.zeros(harvestedShootFreshMassPerAreaKgPerDay.shape[0])

    # get the month and year lists
    simulationMonthEachDay = simulatorClass.getMonth()[::24]
    simulationYearEachDay = simulatorClass.getYear()[::24]

    # import the price data
    filename = constant.romaineLettceRetailPriceFileName
    relativePath = constant.romaineLettceRetailPriceFilePath
    romaineLettceRetailPricePerMonth = util.readData(filename, relativePath, 0, ',')
    # print("romaineLettceRetailPricePerMonth:{}".format(romaineLettceRetailPricePerMonth))
    # print("type(romaineLettceRetailPricePerMonth):{}".format(type(romaineLettceRetailPricePerMonth)))

    # get the sales price of each harvested lettuce (weight)
    for i in range (0, harvestedShootFreshMassPerAreaKgPerDay.shape[0]):
      # if it is not the harvest date then skip the day
      if harvestedShootFreshMassPerAreaKgPerDay[i] == 0.0: continue

      # get the unit price (USD/pound)
      unitRetailPricePerPound = getUnitRomainLettucePrice(simulationMonthEachDay[i], simulationYearEachDay[i], romaineLettceRetailPricePerMonth)

      # unit conversion: 1USD/pound -> USD/kg
      unitRetailPricePerKg = util.convertPoundToKg(unitRetailPricePerPound)

      # unit: USD/m^2/day
      harvestedFreshMassPricePerAreaPerDay[i] = harvestedShootFreshMassPerAreaKgPerDay[i] * unitRetailPricePerKg


    return harvestedFreshMassPricePerAreaPerDay

def getUnitRomainLettucePrice(month, year, priceInfoList):
  """

  return: the unit price of a given month and year
  """
  # print("priceInfoList:{}".format(priceInfoList))
  # print("priceInfoList.shape:{}".format(priceInfoList.shape))
  # print("type(month):{}".format(type(month)))
  # print("type(year):{}".format(type(year)))

  # assuming the list has the header, so skip the header
  for i in range (1, priceInfoList.shape[0]):
    priceInfo = priceInfoList[i]
    # print("i:{}, priceInfo:{}".format(i, priceInfo))
    # print("year:{}".format(year))
    # print("type(year):{}".format(type(month)))
    # print("month:{}".format(year))
    # print("type(month):{}".format(type(month)))
    # print("priceInfo[1]:{}".format(priceInfo[1]))
    # print("priceInfo[2][0:2]:{}".format(priceInfo[2][1:]))

    if year == int(priceInfo[1]) and month == int(priceInfo[2][1:]):
      # print("priceInfo[3]:{}".format(priceInfo[3]))
      # print("type(priceInfo[3]):{}".format(type(priceInfo[3])))
      return float(priceInfo[3])

  print("The specified simulation period include the term where there is no lettuce unit price information. Simulation stopped.")
  # ####################################################################################################
  # # Stop execution here...
  sys.exit()
  # # Move the above line to different parts of the assignment as you implement more of the functionality.
  # ####################################################################################################


def discountPlantSalesperSquareMeterByTipburn(plantSalesperSquareMeter, TotalDLItoPlants):
    '''

    :param plantSalesperSquareMeter:
    :param TotalDLItoPlants:
    :return:
    '''
    # cultivationDaysWithoutHarvest = getCultivationDaysWithoutHarvest(plantSalesperSquareMeter)
    cultivationDaysWithoutHarvest = int(util.calcSimulationDaysInt() % constant.cultivationDaysperHarvest)
    # print "cultivationDaysWithoutHarvest:{}".format(cultivationDaysWithoutHarvest)

    for cycle in range (0, int(util.calcSimulationDaysInt() / constant.cultivationDaysperHarvest)):
        averageDLIperCycle = sum(TotalDLItoPlants[cycle*constant.cultivationDaysperHarvest:(cycle+1)*constant.cultivationDaysperHarvest]) / constant.cultivationDaysperHarvest
        # print "averageDLIperCycle:{}".format(averageDLIperCycle)
        # if the DLI is more than the amount with which there can be some tipburns, discount the price.
        if averageDLIperCycle > constant.DLIforTipBurn:
            plantSalesperSquareMeter[(cycle+1)*constant.cultivationDaysperHarvest-1] = constant.tipburnDiscountRatio * \
                                        plantSalesperSquareMeter[(cycle+1)*constant.cultivationDaysperHarvest-1]

    return plantSalesperSquareMeter


def getCultivationDaysWithoutHarvest(plantSalesperSquareMeter):
    '''
    num of remained days when we cannot finish the cultivation, which is less than the num of cultivation days.
    :param plantSalesperSquareMeter:
    :return:
    '''
    # num of cultivation cycle
    NumCultivationCycle = int(util.calcSimulationDaysInt() / constant.cultivationDaysperHarvest)
    # print "NumCultivationCycle:{}".format(NumCultivationCycle)

    # num of remained days when we cannot finish the cultivation, which is less than the num of cultivation days.
    CultivationDaysWithNoHarvest = util.calcSimulationDaysInt() - NumCultivationCycle * constant.cultivationDaysperHarvest
    # print "CultivationDaysWithNoHarvest:{}".format(CultivationDaysWithNoHarvest)

    return CultivationDaysWithNoHarvest


def getRevenueOfPlantYieldperHarvest(freshWeightTotalperHarvest):
    '''
    calculate the revenue of plant sales per harvest (USD/harvest)
    param:freshWeightTotalperHarvest: fresh Weight perHarvest (kg/harvest)
    return: revenueOfPlantProductionperHarvest: revenue Of Plant Production per Harvest (USD/harvest)
    '''
    return constant.lantUnitPriceUSDperKilogram * freshWeightTotalperHarvest


def getCostofPlantYieldperYear():
    '''
    calculate the cost of plant sales per harvest (USD/per)
    param: :
    return: : cost Of Plant Production per year (USD/year)
    '''
    return  constant.plantProductionCostperSquareMeterPerYear * constant.greenhouseFloorArea


def getGreenhouseTemperatureEachDay(simulatorClass):
  # It was assumed the greenhouse temperature was instantaneously adjusted to the set point temperatures at daytime and night time respectively
  hourlyDayOrNightFlag = simulatorClass.hourlyDayOrNightFlag
  greenhouseTemperature = np.array([constant.setPointTemperatureDayTime if i == constant.daytime else constant.setPointTemperatureNightTime for i in hourlyDayOrNightFlag])

  # calc the mean temperature each day
  dailyAverageTemperature = np.zeros(util.getSimulationDaysInt())
  for i in range(0, util.getSimulationDaysInt()):
    dailyAverageTemperature[i] = np.average(greenhouseTemperature[i * constant.hourperDay: (i + 1) * constant.hourperDay])
  return dailyAverageTemperature

def getGreenhouseTemperatureEachHour(simulatorClass):
  # It was assumed the greenhouse temperature was instantaneously adjusted to the set point temperatures at daytime and night time respectively
  hourlyDayOrNightFlag = simulatorClass.hourlyDayOrNightFlag
  greenhouseTemperature = np.array(
    [constant.setPointTemperatureDayTime if i == constant.daytime else constant.setPointTemperatureNightTime for i in hourlyDayOrNightFlag])

  return greenhouseTemperature

def getFreshWeightIncrease(FWPerHead):
  # get the fresh weight increase

  # freshWeightIncrease = np.array([WFresh[i] - WFresh[i-1] if WFresh[i] - WFresh[i-1] > 0 else 0.0 for i in range (1, WFresh.shape[0])])
  # # insert the value for i == 0
  # freshWeightIncrease[0] = 0.0
  # it is possible that the weight decreases at E_J_VanHenten1994
  freshWeightIncrease = np.array([0.0 if i == 0 or FWPerHead[i] - FWPerHead[i-1] <= -constant.harvestDryWeight*constant.DryMassToFreshMass/2.0\
                                    else FWPerHead[i] - FWPerHead[i-1] for i in range (0, FWPerHead.shape[0])])

  return freshWeightIncrease


def getAccumulatedFreshWeightIncrease(WFresh):
  # get accumulated fresh weight

  freshWeightIncrease = getFreshWeightIncrease(WFresh)
  accumulatedFreshWeightIncrease = np.zeros(WFresh.shape[0])
  accumulatedFreshWeightIncrease[0] = WFresh[0]
  for i in range(1, freshWeightIncrease.shape[0]):
    # print("i:{}, accumulatedFreshWeightIncrease[i]:{}, accumulatedFreshWeightIncrease[i-1]:{}, freshWeightIncrease[i]:{}".format(i, accumulatedFreshWeightIncrease[i], accumulatedFreshWeightIncrease[i-1], freshWeightIncrease[i]))
    accumulatedFreshWeightIncrease[i] = accumulatedFreshWeightIncrease[i-1] + freshWeightIncrease[i]

  return accumulatedFreshWeightIncrease


def getHarvestedFreshWeight(WFresh):
  # get the harvested fresh weight

  # record the fresh weight harvested at each harvest day or hour
  # harvestedFreshWeight = np.array([WFresh[i] if WFresh[i] > 0.0 and WFresh[i+1] == 0.0 else 0.0 for i in range (0, WFresh.shape[0])])
  harvestedFreshWeight = np.zeros(WFresh.shape[0])
  for i in range (0, WFresh.shape[0]-1):
    # print("i:{}, WFresh[i]:{}".format(i, WFresh[i]))

    if WFresh[i] > 0.0 and WFresh[i+1] == 0.0:
      harvestedFreshWeight[i] = WFresh[i]
    else:
      harvestedFreshWeight[i] = 0.0

  # print("0 harvestedFreshWeight.shape[0]:{}".format(harvestedFreshWeight.shape[0]))

  # if the last hour of the last day is the harvest date
  if WFresh[-1] > constant.harvestDryWeight*constant.DryMassToFreshMass:
    # harvestedFreshWeight = np.append(harvestedFreshWeight, [WFresh[-1]])
    harvestedFreshWeight[-1] = WFresh[-1]
  else:
    harvestedFreshWeight[-1] = WFresh[-1]

  return harvestedFreshWeight


