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

  # if you continue to grow plant during the fallow period, then this is true
  ifGrowForFallowPeriod = cropElectricityYieldSimulator1.getIfGrowForFallowPeriod()
  # print ("ifGrowForFallowPeriod:{}".format(ifGrowForFallowPeriod))

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

    # print ("i : {}".format(i))

    DaysperCycle = datetime.timedelta(days = cultivationDaysperHarvest)
    # if ifGrowForFallowPeriod is False the end of the cultivation at a cycle is within the fallow period (constant.FallowPeriodStart*), then skip the cycle (= plus 35 days to index)
    if ifGrowForFallowPeriod is False and i % cultivationDaysperHarvest == 0 and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) + DaysperCycle >= datetime.date(yearEachDay[i], constant.FallowPeriodStartMM, constant.FallowPeriodStartDD) and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) + DaysperCycle <= datetime.date(yearEachDay[i], constant.FallowPeriodEndMM, constant.FallowPeriodEndDD):
      # skip the cultivation cycle
      i += cultivationDaysperHarvest
      continue

    # if ifGrowForFallowPeriod is False, and the end of the cultivation at a cycle is not within the fallow period (constant.FallowPeriodStart*), but the first day is within the fallow period, then shift the first day to
    # the next day of the fallow period, and shift all of the cultivation days in harvestDaysList
    elif ifGrowForFallowPeriod is False and i % cultivationDaysperHarvest == 0 and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) >= datetime.date(yearEachDay[i], constant.FallowPeriodStartMM, constant.FallowPeriodStartDD) and \
        datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i]) <= datetime.date(yearEachDay[i], constant.FallowPeriodEndMM, constant.FallowPeriodEndDD):
      # shift the first day to the next day of the fallow period
      dateDiff = datetime.date(yearEachDay[i], constant.FallowPeriodEndMM, constant.FallowPeriodEndDD) - datetime.date(yearEachDay[i], monthEachDay[i], dayEachDay[i])
      i += dateDiff.days + 1

      # shift each harvest period by dateDiff to keep the harvest period cultivationDaysperHarvest even after atarting the cultivation next to the fallow period.
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

def calcUnitDailyFreshWeightIncreaseBoth2003Taylor(innerDLIToPlants, cultivationDaysperHarvest, daysFromSeeding):
  '''
  this function is only for the Q learning reinforcement learning
  calculate the unit fresh weight increase per day based on the revised model of Both (2003):
  Both, A., 2003. Ten years of hydroponic lettuce research. Knowledgecenter.Illumitex.Com 18, 8.

  param:innerDLIToPlants [mol/m^2/day] per day
  param:cultivationDaysperHarvest [days] per day
  param:daysFromSeeding [days] per day

  return: dailyFreshWeightIncrease[g/day]
  return: hervestDay[days]: days after seeeding
  '''
  # print "dailyInnerLightIntensityDLI:{}".format(dailyInnerLightIntensityDLI)
  # print "cultivationDaysperHarvest:{}".format(cultivationDaysperHarvest)

  # daily increase in unit plant weight [g]
  unitDailyFreshWeightIncrease = np.zeros(1)
  # accumulated weight of daily increase in unit plant weight during the whole simulation days [g]
  accumulatedUnitDailyFreshWeightIncrease = np.zeros(1)
  # harvested daily unit plant weight [g]
  unitHarvestedFreshWeight = np.zeros(1)

  # simulationDaysInt = util.calcSimulationDaysInt()
  simulationDaysInt = 1

  # num of cultivation cycle
  NumCultivationCycle = 0
  # print ("NumCultivationCycle:{}".format(NumCultivationCycle))

  # num of remained days when we cannot finish the cultivation, which is less than the num of cultivation days.
  CultivationDaysWithNoHarvest = simulationDaysInt - NumCultivationCycle * cultivationDaysperHarvest
  # print "CultivationDaysWithNoHarvest:{}".format(CultivationDaysWithNoHarvest)

  # define statistics for calculation
  # daily unit plant weight on each cycle [g]
  shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
  d_shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
  # dd_shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
  # ddd_shootDryMassList = np.zeros(len(unitDailyFreshWeightIncrease))
  a = 0
  b = 0.4822
  c = -0.006225
  # time step[day]
  dt = 1

  # print "cycle * cultivationDaysperHarvest -1:{}".format(accumulatedUnitDailyFreshWeightIncrease[0 * cultivationDaysperHarvest -1])

  for cycle in range(0, NumCultivationCycle + 1):

    # define the initial values on each cycle [g]
    # shootDryMassInit == the weight on day 0 == weight of seed [g]
    shootDryMassInit = 0.0001
    accumulatedUnitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest] = accumulatedUnitDailyFreshWeightIncrease[
                                                                                   cycle * cultivationDaysperHarvest - 1] + shootDryMassInit
    shootDryMassList[cycle * cultivationDaysperHarvest] = shootDryMassInit
    d_shootDryMassList[cycle * cultivationDaysperHarvest] = (b + 2 * c * 0.0) * shootDryMassList[cycle * cultivationDaysperHarvest]
    # dd_shootDryMassList[cycle * cultivationDaysperHarvest] = 2 * c * shootDryMassList[cycle * cultivationDaysperHarvest] + \
    #                                                          (b + 2 * c * 0.0) ** 2 * shootDryMassList[cycle * cultivationDaysperHarvest]
    # ddd_shootDryMassList[cycle * cultivationDaysperHarvest] = 2 * c * d_shootDryMassList[cycle * cultivationDaysperHarvest] + \
    #                                                           4 * c * (b + 2 * c * 0.0) * shootDryMassList[cycle * cultivationDaysperHarvest] + \
    #                                                           (b + 2 * c * 0) ** 2 * d_shootDryMassList[cycle * cultivationDaysperHarvest]

    # print "shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(shootDryMassList[cycle*cultivationDaysperHarvest])
    # print "d_shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(d_shootDryMassList[cycle*cultivationDaysperHarvest])
    # print "dd_shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(dd_shootDryMassList[cycle*cultivationDaysperHarvest])
    # print "ddd_shootDryMassList[cycle*cultivationDaysperHarvest]:{}".format(ddd_shootDryMassList[cycle*cultivationDaysperHarvest])


    # update each statistic each day
    a = -8.596 + 0.0743 * innerDLIToPlants
    shootDryMassList = math.e ** (a + b * daysFromSeeding + c * daysFromSeeding ** 2)
    d_shootDryMassList = (b + 2 * c * daysFromSeeding) * shootDryMassList
    dd_shootDryMassList = 2 * c * shootDryMassList + (b + 2 * c * daysFromSeeding) ** 2 * shootDryMassList
    ddd_shootDryMassList = 2 * c * d_shootDryMassList + 4 * c * (b + 2 * c * daysFromSeeding) * shootDryMassList + \
                           (b + 2 * c * daysFromSeeding) ** 2 * d_shootDryMassList

    # print "day{}, a:{},shootDryMassList[{}]:{}".format(day, a, cycle*cultivationDaysperHarvest+day, shootDryMassList[cycle*cultivationDaysperHarvest+day])

    # Taylor expansion: x_0 = 0, h = 1 (source: http://eman-physics.net/math/taylor.html)
    # shootDryMassList[cycle * cultivationDaysperHarvest + day] = shootDryMassList[cycle * cultivationDaysperHarvest + day - 1] + \
    #                                                             1.0 / (math.factorial(1)) * d_shootDryMassList[
    #                                                               cycle * cultivationDaysperHarvest + day - 1] * dt + \
    #                                                             1.0 / (math.factorial(2)) * dd_shootDryMassList[
    #                                                               cycle * cultivationDaysperHarvest + day - 1] * ((dt) ** 2) + \
    #                                                             1.0 / (math.factorial(3)) * ddd_shootDryMassList[
    #                                                               cycle * cultivationDaysperHarvest + day - 1] * ((dt) ** 3)

    # unitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest + day] = shootDryMassList[cycle * cultivationDaysperHarvest + day] - \
    #                                                                         shootDryMassList[cycle * cultivationDaysperHarvest + day - 1]
    unitDailyFreshWeightIncrease = d_shootDryMassList

    # accumulatedUnitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest + day] = \
    #   accumulatedUnitDailyFreshWeightIncrease[cycle * cultivationDaysperHarvest + day - 1] + unitDailyFreshWeightIncrease[
    #     cycle * cultivationDaysperHarvest + day]

    # print "day:{}, cycle*cultivationDaysperHarvest+day:{}, shootDryMassList[cycle*cultivationDaysperHarvest + day]:{}".format(
    #     day, cycle * cultivationDaysperHarvest + day, shootDryMassList[cycle * cultivationDaysperHarvest + day])

  # change dry mass weight into fresh mass weight
  # daily increase in unit plant weight [g]
  unitDailyFreshWeightIncrease = unitDailyFreshWeightIncrease * constant.DryMassToFreshMass
  # accumulated weight of daily increase in unit plant weight during the whole simulation days [g]
  # accumulatedUnitDailyFreshWeightIncrease = accumulatedUnitDailyFreshWeightIncrease * constant.DryMassToFreshMass
  # harvested daily unit plant weight [g]
  # unitHarvestedFreshWeight = unitHarvestedFreshWeight * constant.DryMassToFreshMass
  # daily unit plant weight on each cycle [g]
  # shootFreshMassList = shootDryMassList * constant.DryMassToFreshMass

  # print "shootDryMassList:{}".format(shootDryMassList)
  # print "unitDailyFreshWeightIncrease:{}".format(unitDailyFreshWeightIncrease)
  # print "accumulatedUnitDailyFreshWeightIncrease:{}".format(accumulatedUnitDailyFreshWeightIncrease)
  # print "unitHarvestedFreshWeight:{}".format(unitHarvestedFreshWeight)

  return unitDailyFreshWeightIncrease



def getLettucePricepercwt(year):
    '''
    return the lettuce price per cwt based on the year of sales
    :param year:
    :return:
    '''
    return 0.583 * year - 1130

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


def calcRevenueOfPlantYieldperHarvest(freshWeightTotalperHarvest):
    '''
    calculate the revenue of plant sales per harvest (USD/harvest)
    param:freshWeightTotalperHarvest: fresh Weight perHarvest (kg/harvest)
    return: revenueOfPlantProductionperHarvest: revenue Of Plant Production per Harvest (USD/harvest)
    '''
    return constant.lantUnitPriceUSDperKilogram * freshWeightTotalperHarvest


def calcCostofPlantYieldperYear():
    '''
    calculate the cost of plant sales per harvest (USD/per)
    param: :
    return: : cost Of Plant Production per year (USD/year)
    '''
    return  constant.plantProductionCostperSquareMeterPerYear * constant.greenhouseFloorArea

