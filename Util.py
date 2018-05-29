# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 12 Dec 2016
# last edit date: 14 Dec 2016
#######################################################

##########import package files##########
from scipy import stats
import datetime
import calendar
from textwrap import wrap
import os as os
import numpy as np
import matplotlib.pyplot as plt
# from sklearn import datasets
import math
import CropElectricityYeildSimulatorConstant as constant
import csv
import random
import glob
#######################################################

def flipCoin( p ):
  '''

  :param p:0.0 to 1.0
  :return:
  '''
  r = random.random()
  return r < p


def getStartDateDateType():
    '''
    return the start date as date type
    :return:
    '''
    return datetime.date(int(constant.SimulationStartDate[0:4]), int(constant.SimulationStartDate[4:6]), int(constant.SimulationStartDate[6:8]))

def getEndDateDateType():
    '''
    return the end date as date type
    :return:
    '''
    return datetime.date(int(constant.SimulationEndDate[0:4]), int(constant.SimulationEndDate[4:6]), int(constant.SimulationEndDate[6:8]))


def getSimulationDaysInt():
  '''
  calculate the simulation days.

  :return:  simulationDaysInt
  '''
  # get start date and end date of simulation from constant class as String
  startDateDateType = getStartDateDateType()
  # print "type(startDateDateType):{}".format(type(startDateDateType))
  # print "startDateDateType:{}".format(startDateDateType)
  endDateDateType = getEndDateDateType()
  # print "endDateDateType:{}".format(endDateDateType)
  # print "int(constant.SimulationEndDate[0:4]):{}".format(int(constant.SimulationEndDate[0:4]))
  # print "int(constant.SimulationEndDate[5:6]):{}".format(int(constant.SimulationEndDate[4:6]))
  # print "int(constant.SimulationEndDate[7:8]):{}".format(int(constant.SimulationEndDate[6:8]))
  simulationDays = endDateDateType - startDateDateType
  # print "simulationDays:{}".format(simulationDays)
  # print "type(simulationDays):{}".format(type(simulationDays))
  # convert the data type
  simulationDaysInt = simulationDays.days + 1
  # print "simulationDaysInt:{}".format(simulationDaysInt)
  # print "type(simulationDaysInt):{}".format(type(simulationDaysInt))

  return simulationDaysInt


def calcSimulationDaysInt():
    '''
    calculate the simulation days.

    :return:  simulationDaysInt
    '''
    # get start date and end date of simulation from constant class as String
    startDateDateType = getStartDateDateType()
    # print "type(startDateDateType):{}".format(type(startDateDateType))
    # print "startDateDateType:{}".format(startDateDateType)
    endDateDateType = getEndDateDateType()
    # print "endDateDateType:{}".format(endDateDateType)
    # print "int(constant.SimulationEndDate[0:4]):{}".format(int(constant.SimulationEndDate[0:4]))
    # print "int(constant.SimulationEndDate[5:6]):{}".format(int(constant.SimulationEndDate[4:6]))
    # print "int(constant.SimulationEndDate[7:8]):{}".format(int(constant.SimulationEndDate[6:8]))
    simulationDays = endDateDateType - startDateDateType
    # print "simulationDays:{}".format(simulationDays)
    # print "type(simulationDays):{}".format(type(simulationDays))
    # convert the data type
    simulationDaysInt = simulationDays.days + 1
    # print "simulationDaysInt:{}".format(simulationDaysInt)
    # print "type(simulationDaysInt):{}".format(type(simulationDaysInt))

    return simulationDaysInt


def getSimulationMonthsInt():
    # get start date and end date of simulation from constant class as String
    startDateDateType = getStartDateDateType()
    # print "type(startDateDateType):{}".format(type(startDateDateType))
    # print "startDateDateType:{}".format(startDateDateType)
    endDateDateType = getEndDateDateType()
    return (endDateDateType.year - startDateDateType.year)*12 + endDateDateType.month - startDateDateType.month + 1

def getDaysFirstMonth():
    startDate = getStartDateDateType()
    _, daysFirstMonth = calendar.monthrange(startDate.year, startDate.month)
    # print "month_day:{}".format(month_day)
    return daysFirstMonth

def getDaysLastMonth():
    lastDate = getEndDateDateType()
    _, daysLastMonth = calendar.monthrange(lastDate.year, lastDate.month)
    # print "month_day:{}".format(month_day)
    return daysLastMonth

def getDaysFirstMonthForGivenPeriod():
    daysFirstMonth = getDaysFirstMonth()
    startDate = getStartDateDateType()
    days = startDate.day
    # print "day:{}".format(day)
    # print "type(day):{}".format(type(day))
    daysFirstMonthForGivenPeriod = daysFirstMonth - days + 1

    return daysFirstMonthForGivenPeriod

def getNumOfDaysFromJan1st(date):
  jan1stdate = datetime.date(date.year, 1, 1)
  daysFromJan1st = date - jan1stdate

  return daysFromJan1st.days

def getOnly15thDay(hourlySolarradiation):
    # print (hourlySolarradiation.shape)
    # print (type(hourlySolarradiation.shape))

    # hourlySolarradiationOnly15th = np.array([])
    hourlySolarradiationOnly15th = []

    date = datetime.datetime(getStartDateDateType().year, getStartDateDateType().month, getStartDateDateType().day)

    for i in range (0, hourlySolarradiation.shape[0]):

        # print (date.day)
        if date.day == 15:
            # np.append(hourlySolarradiationOnly15th, hourlySolarradiation[i])
            hourlySolarradiationOnly15th.append(hourlySolarradiation[i])
            # hourlySolarradiationOnly15th.append(hourlySolarradiation[i])

            # print("hourlySolarradiation[i]:{}".format(hourlySolarradiation[i]))
            # print("hourlySolarradiationOnly15th:{}".format(hourlySolarradiationOnly15th))
        # set the date object 1 hour ahead.
        date += datetime.timedelta(hours=1)

    # print ("hourlySolarradiationOnly15th.shape[0]:{}".format(len(hourlySolarradiationOnly15th)))

    return hourlySolarradiationOnly15th

def getSummerDays(year):
  '''

  :param years:
  :return:
  '''
  return datetime.date(year, constant.SummerPeriodEndMM,constant.SummerPeriodEndDD) - datetime.date(year, constant.SummerPeriodStartMM, constant.SummerPeriodStartDD)

def dateFormConversionYyyyMmDdToMnSlashddSlashYyyy(yyyymmdd):
    yyyy = yyyymmdd[0:4]
    mm = yyyymmdd[4:6]
    dd = yyyymmdd[6:8]
    mmSlashddSlashyyyy = mm + "/" + dd + "/" + yyyy

    return mmSlashddSlashyyyy

def readData(fileName, relativePath = "", skip_header=0, d=','):
    '''
    retrieve the data from the file named fileName
    you may have to modify the path below in other OSs.
    in Linux, Mac OS, the partition is "/". In Windows OS, the partition is "\" (backslash).
    os.sep means "\" in windows. So the following path is adjusted for Windows OS

    param filename: filename
    param relativePath: the relative path from "data" folder to the folder where there is a file you want to import
    param d: the type of data separator, which s "," by default
    return: a numpy.array of the data
    '''
    # read a file in "data" folder
    if relativePath == "":
        filePath = os.path.dirname(__file__).replace('/', os.sep) + '\\' + 'data\\' + fileName
        # print "filePath:{}".format(filePath)
    else:
        filePath = os.path.dirname(__file__).replace('/', os.sep) + '\\' + 'data\\' + relativePath + '\\' + fileName
        # print "filePath:{}".format(filePath)

    if skip_header == 0:
        return np.genfromtxt(filePath, delimiter=d, dtype=None)
    else:
        return np.genfromtxt(filePath, delimiter=d, dtype=None, skip_header=skip_header)


def exportCSVFile(dataMatrix, fileName="exportFile", relativePath=""):
  '''
  export dataMatrix
  :param dataMatrix:
  :param path:
  :param fileName:
  :return: None
  '''
  # print (dataMatrix)

  currentDir = os.getcwd()
  # change the directory to export
  if relativePath == "":
    os.chdir(currentDir + "/exportData")
  else:
    os.chdir(currentDir + relativePath)
  # print "os.getcwd():{}".format(os.getcwd())

  f = open(fileName + ".csv", 'w')  # open the file with writing mode
  csvWriter = csv.writer(f, lineterminator="\n")
  # print "dataMatrix:{}".format(dataMatrix)
  for data in dataMatrix:
    csvWriter.writerow(data)
  f.close()  # close the file

  # take back the current directory
  os.chdir(currentDir)
  # print "os.getcwd():{}".format(os.getcwd())

def importDictionaryAsCSVFile(fileName="exportFile", relativePath=""):
  '''
    import the values of dictionary

  :param fileName:
  :param relativePath:
  :return:
  '''
  currentDir = os.getcwd()
  # print ("currentDir:{}".format(currentDir))
  # currentDir = unicode(currentDir, encoding='shift-jis')
  # print ("currentDir:{}".format(currentDir))

  # change the directory to export
  if relativePath == "":
    os.chdir(currentDir + "/exportData")
  else:
    os.chdir(currentDir + relativePath)

  dict = Counter()
  for key, val in csv.reader(open(fileName+".csv")):
    dict[key] = val

  # take back the current directory
  os.chdir(currentDir)
  # print "os.getcwd():{}".format(os.getcwd())

  return dict


def exportDictionaryAsCSVFile(dictionary, fileName="exportFile", relativePath=""):
  '''
    export the values of dictionary

  :param dictionary:
  :param fileName:
  :param relativePath:
  :return:
  '''
  currentDir = os.getcwd()
  # change the directory to export
  if relativePath == "":
    os.chdir(currentDir + "/exportData")
  else:
    os.chdir(currentDir + relativePath)
  # print ("dictionary:{}".format(dictionary))

  w = csv.writer(open(fileName + ".csv", "w"))
  for key, val in dictionary.items():
    w.writerow([key, val])

  # take back the current directory
  os.chdir(currentDir)
  # print "os.getcwd():{}".format(os.getcwd())


def getArraysFromData(fileName, simulatorClass):
  '''
  read data from a file, process the data and return them as arrays
  :param fileName: String
  :return:
  '''

  # get the simulation days set in the constant class
  simulationDaysInt = calcSimulationDaysInt()
  # print "simulationDaysInt:{}".format(simulationDaysInt)
  # get start date and end date of simulation from constant class as String
  startDateDateType = getStartDateDateType()
  # print "startDateDateType:{}".format(startDateDateType)
  # print "type(startDateDateType):{}".format(type(startDateDateType))
  endDateDateType = getEndDateDateType()

  # if there are dates where there are any missing lines, skip the date and subtract the number from the simulation days
  trueSimulationDaysInt = simulationDaysInt
  missingDates = np.array([])

  # automatically changes its length dependent on the amoutn of imported data
  year = np.zeros(simulationDaysInt * constant.hourperDay, dtype=np.int)
  # print "year.shape:{}".format(year.shape)
  month = np.zeros(simulationDaysInt * constant.hourperDay, dtype=np.int)
  # print "month:{}".format(month.shape)
  day = np.zeros(simulationDaysInt * constant.hourperDay, dtype=np.int)
  hour = np.zeros(simulationDaysInt * constant.hourperDay, dtype=np.int)
  # dates = np.chararray(simulationDaysInt * constant.hourperDay)
  dates = [""] * (simulationDaysInt * constant.hourperDay)
  # print "dates:{}".format(dates)

  # [W/m^2]
  hourlyHorizontalDiffuseOuterSolarIrradiance = np.zeros(simulationDaysInt * constant.hourperDay)
  # [W/m^2]
  hourlyHorizontalTotalOuterSolarIrradiance = np.zeros(simulationDaysInt * constant.hourperDay)
  # [W/m^2]
  hourlyHorizontalDirectOuterSolarIrradiance = np.zeros(simulationDaysInt * constant.hourperDay)
  # [deg C]
  hourlyHorizontalTotalBeamMeterBodyTemperature = np.zeros(simulationDaysInt * constant.hourperDay)
  # [deg C]
  hourlyHorizonalDirectBeamMeterBodyTemperature = np.zeros(simulationDaysInt * constant.hourperDay)
  # [deg C]
  hourlyAirTemperature = np.zeros(simulationDaysInt * constant.hourperDay)
  # [%]
  hourlyRelativeHumidity = np.zeros(simulationDaysInt * constant.hourperDay)

  # import the file removing the header
  fileData = readData(fileName, relativePath="", skip_header=1)
  # print "fileData:{}".format(fileData)
  # print "fileData.shape:{}".format(fileData.shape)

  # change the date format
  simulationStartDate = dateFormConversionYyyyMmDdToMnSlashddSlashYyyy(constant.SimulationStartDate)
  simulationEndDate = dateFormConversionYyyyMmDdToMnSlashddSlashYyyy(constant.SimulationEndDate)
  # print ("simulationStartDate:{}".format(simulationStartDate))
  # print ("simulationEndDate:{}".format(simulationEndDate))
  # print ("fileData.shape:{}".format(fileData.shape))

  ########## store the imported data to lists
  # index for data storing
  index = 0
  for hourlyData in fileData:
    # for day in range(0, simulationDaysInt):

    # print"hourlyData:{}".format(hourlyData)
    dateList = hourlyData[0].split("/")
    # print "dateList:{}".format(dateList)
    # print "month:{}".format(month)
    # print "day:{}".format(day)

    # exclude the data out of the set start date and end date
    if datetime.date(int(dateList[2]), int(dateList[0]), int(dateList[1])) < startDateDateType or \
            datetime.date(int(dateList[2]), int(dateList[0]), int(dateList[1])) > endDateDateType:
      continue

    # print "datetime.date(int(dateList[2]), int(dateList[0]), int(dateList[1])):{}".format(datetime.date(int(dateList[2]), int(dateList[0]), int(dateList[1])))
    # print "startDateDateType:{}".format(startDateDateType)
    # print "endDateDateType:{}".format(endDateDateType)

    year[index] = int(dateList[2])
    month[index] = int(dateList[0])
    day[index] = int(dateList[1])
    hour[index] = hourlyData[1]
    dates[index] = hourlyData[0]
    # print "hourlyData[0]:{}".format(hourlyData[0])
    # print "dates:{}".format(dates)
    # print "index:{}, year:{}, hour[index]:{}".format(index, year, hour)
    # print "hourlyData[0]:{}".format(hourlyData[0])
    # print "year[index]:{}".format(year[index])
    # [W/m^2]
    hourlyHorizontalDiffuseOuterSolarIrradiance[index] = hourlyData[4]
    # [W/m^2]
    hourlyHorizontalTotalOuterSolarIrradiance[index] = hourlyData[2]
    # the direct beam solar radiation is not directly got from the file, need to calculate from "the total irradiance - the diffuse irradiance"
    # [W/m^2]
    hourlyHorizontalDirectOuterSolarIrradiance[index] = hourlyHorizontalTotalOuterSolarIrradiance[index] \
                                                        - hourlyHorizontalDiffuseOuterSolarIrradiance[index]
    # unit: [celusis]
    hourlyHorizontalTotalBeamMeterBodyTemperature[index] = hourlyData[7]
    # unit: [celusis]
    hourlyHorizonalDirectBeamMeterBodyTemperature[index] = hourlyData[8]
    # unit: [celusis]
    hourlyAirTemperature[index] = hourlyData[5]
    # print "hourlyAirTemperature:{}".format(hourlyAirTemperature)
    # unit: [-] <- [%]
    hourlyRelativeHumidity = hourlyData[6] * 0.01

    # print "hour[index] - hour[index-1]:{}".format(hourlyData[1] - hour[index-1])
    # print "year[index]:{}, month[index]:{}, day[index]:{}, hour[index]:{}".format(year[index], month[index], day[index], hour[index])
    # print "year[index]:{}, month[index]:{}, day[index]:{}, hour[index]:{}".format(year[index-1], month[index-1], day[index-1], hour[index-1])
    # print "datetime.datetime(year[index], month[index], day[index], hour = hour[index]):{}".format(datetime.datetime(year[index], month[index], day[index], hour = hour[index]))
    # print "datetime.datetime(year[index-1], month[index-1], day[index-1]),hour = hour[index-1]:{}".format(datetime.datetime(year[index-1], month[index-1], day[index-1],hour = hour[index-1]))
    # if index <> 0 and datetime.timedelta(hours=1) <> datetime.datetime(year[index], month[index], day[index], hour = hour[index]) - \
    #     datetime.datetime(year[index-1], month[index-1], day[index-1], hour = hour[index-1]):
    #     missingDates = np.append(missingDates, hourlyData)
    index += 1
  # print "year:{}".format(year)
  # print "month:{}".format(month)
  # print "day:{}".format(day)
  # print "hour:{}".format(hour)
  # print "hourlyHorizontalTotalOuterSolarIrradiance:{}".format(hourlyHorizontalTotalOuterSolarIrradiance)
  # print "hourlyHorizontalTotalBeamMeterBodyTemperature:{}".format(hourlyHorizontalTotalBeamMeterBodyTemperature)
  # print "hourlyHorizontalDirectOuterSolarIrradiance:{}".format(hourlyHorizontalDirectOuterSolarIrradiance)
  # print "hourlyHorizonalDirectBeamMeterBodyTemperature.shape:{}".format(hourlyHorizonalDirectBeamMeterBodyTemperature.shape)
  # print "hourlyAirTemperature:{}".format(hourlyAirTemperature)
  # print "hourlyAirTemperature.shape:{}".format(hourlyAirTemperature.shape)

  # set the values to the object
  simulatorClass.setYear(year)
  simulatorClass.setMonth(month)
  simulatorClass.setDay(day)
  simulatorClass.setHour(hour)
  simulatorClass.setImportedHourlyHorizontalDirectSolarRadiation(hourlyHorizontalDirectOuterSolarIrradiance)
  simulatorClass.setImportedHourlyHorizontalDiffuseSolarRadiation(hourlyHorizontalDiffuseOuterSolarIrradiance)
  simulatorClass.setImportedHourlyHorizontalTotalBeamMeterBodyTemperature(hourlyHorizontalTotalBeamMeterBodyTemperature)
  simulatorClass.setImportedHourlyAirTemperature(hourlyAirTemperature)
  simulatorClass.hourlyRelativeHumidity = hourlyRelativeHumidity


  ##########file import (TucsonHourlyOuterEinvironmentData) end##########

  return year, month, day, hour, hourlyHorizontalDiffuseOuterSolarIrradiance, \
  hourlyHorizontalTotalOuterSolarIrradiance,  \
  hourlyHorizontalDirectOuterSolarIrradiance, \
  hourlyHorizontalTotalBeamMeterBodyTemperature, \
  hourlyAirTemperature


def deriveOtherArraysFromImportedData(simulatorClass):
  # Other data can be added in the future


  # set the the flag indicating daytime or nighttime
  hourlyHorizontalDirectOuterSolarIrradiance = simulatorClass.getImportedHourlyHorizontalDirectSolarRadiation()
  hourlyDayOrNightFlag = np.array([constant.daytime if i > 0.0 else constant.nighttime for i in hourlyHorizontalDirectOuterSolarIrradiance])
  simulatorClass.hourlyDayOrNightFlag = hourlyDayOrNightFlag


def convertFromJouleToWattHour(joule):
    '''
    [J] == [W*sec] -> [W*hour]
    :param joule:
    :return:
    '''
    return joule / constant.minuteperHour /constant.secondperMinute

def convertWattPerSquareMeterEachHourToJoulePerSaureMeterEachDay(hourlySolarIrradiance):
  '''
  Unit conversion: [average W / m^2 each hour] -> [J / m^2 each day]
  '''

  # convert W / m^2 (= J/(s * m^2)) into J/(hour * m^2)
  SolarRadiantEnergyPerHour = hourlySolarIrradiance * constant.secondperMinute * constant.minuteperHour

  dailySolarEnergy = np.zeros(int(SolarRadiantEnergyPerHour.shape[0]/constant.hourperDay))
  for i in range (0, dailySolarEnergy.shape[0]):
    dailySolarEnergy[i] = sum(SolarRadiantEnergyPerHour[i*constant.hourperDay : (i+1)*constant.hourperDay])
  return dailySolarEnergy


def convertFromgramTokilogram(weightg):
    '''
    convert the unit from g to kg

    param: weightg, weight (g)
    return: weight(kg)
    '''
    return weightg/1000.0


def convertWhTokWh(electricityYield):
    '''
    convert the unit from Wh to kWh
    :param electricityYieldkW:
    :return:
    '''
    return electricityYield / 1000.0


def convertFromMJperHourSquareMeterToWattperSecSquareMeter(MJperSquareMeter):
    '''
    change the unit of light intensity from MJ/hour/m^2 to Watt/sec/m^2 (unit of light energy in terms of energy),
    which is for OPV electricity generation

    param: MJperSquareMeter (MJ/hour/m^2)
    return: (Watt/m^2) = (J/sec/m^2)
    '''
    return MJperSquareMeter *10.0**6 / 60.0 / 60.0

def convertFromHourlyPPFDWholeDayToDLI(hourlyPPFDWholePeriod):
    '''
    [umol m^-2 s^-1] -> [mol m^-2 day^-1]
    :param hourlyPPFDWholePeriod:
    :return:DLI
    '''
    DLIWholePeriod = np.zeros(calcSimulationDaysInt())

    # convert the unit: [umol m^-2 s^-1] -> [umol m^-2 day^-1]
    for day in range (0, calcSimulationDaysInt()):
        for hour in range(0, hourlyPPFDWholePeriod.shape[0]/calcSimulationDaysInt()):
            DLIWholePeriod[day] += hourlyPPFDWholePeriod[day * constant.hourperDay + hour] * constant.secondperMinute * constant.minuteperHour

    # convert the unit: [umol m^-2 day^-1] -> [mol m^-2 day^-1]
    DLIWholePeriod = DLIWholePeriod / float(10**6)
    # print "DLIWholePeriod:{}".format(DLIWholePeriod)
    return DLIWholePeriod

# def convertFromJouleperDayperAreaToWattper(hourlyPPFDWholePeriod):
#     '''
#     [umol m^-2 s^-1] -> [mol m^-2 day^-1]
#     :param hourlyPPFDWholePeriod:
#     :return:DLI
#     '''
#     DLIWholePeriod = np.zeros(calcSimulationDaysInt())
#
#     # convert the unit: [umol m^-2 s^-1] -> [umol m^-2 day^-1]
#     for day in range (0, calcSimulationDaysInt()):
#         for hour in range(0, hourlyPPFDWholePeriod.shape[0]/calcSimulationDaysInt()):
#             DLIWholePeriod[day] += hourlyPPFDWholePeriod[day * constant.hourperDay + hour] * constant.secondperMinute * constant.minuteperHour
#
#     # convert the unit: [umol m^-2 day^-1] -> [mol m^-2 day^-1]
#     DLIWholePeriod = DLIWholePeriod / float(10**6)
#     # print "DLIWholePeriod:{}".format(DLIWholePeriod)
#     return DLIWholePeriod

def convertFromWattperSecSquareMeterToPPFD(WattperSquareMeter):
   '''
   change the unit of light intensity from MJ/m^2 to μmol/m^2/s (unit of PPFD in terms of photon desnity for photosynthesis),
   which is for photosynthesis plant production
   source of the coefficient
   http://www.apogeeinstruments.com/conversion-ppf-to-watts/ : 1/0.219 = 4.57
   http://www.egc.com/useful_info_lighting.php: 1/0.327 = 3.058103976

   param: WattperSecSquare (Watt/m^2) = (J/sec/m^2)
   return: (μmol/m^2/s in solar radiation)
   '''
   return WattperSquareMeter * constant.wattToPPFDConversionRatio

def convertUnitShootFreshMassToShootFreshMassperArea(shootFreshMassList):
    '''
    :return:
    '''
    # unit convert [g/head] -> [g/m^2]
    shootFreshMassListPerCultivationFloorArea = shootFreshMassList * constant.plantDensity
    return shootFreshMassListPerCultivationFloorArea

def convertcwtToKg(cwt):
    # unit convert [cwt] -> [kg]
    return cwt * constant.kgpercwt


def convertHourlyTemperatureToDailyAverageTemperature(hourlyTemperature):
  '''
  Unit conversion: [g/head] -> [g/m^2]
  '''
  dailyAverageTemperature = np.zeros(int(hourlyTemperature.shape[0]/constant.hourperDay))
  for i in range (0, hourlyTemperature.shape[0]):
    dailyAverageTemperature[i] = np.average(hourlyTemperature[i*constant.hourperDay : (i+1)*constant.hourperDay])

  return dailyAverageTemperature


def convertPoundToKg(pound):
  return pound * (1.0 / 0.45359237)


def saveFigure (filename):
    '''
    save the figure with given file name at the curent directory
    param: filename: file name
    return: :
    '''
    # (relative to your python current working directory)
    path = os.path.dirname(__file__).replace('/', os.sep)
    os.chdir(path)
    figure_path = './exportData/'
    # figure_path = '../'

    # set to True in order to automatically save the generated plots
    filename = '{}'.format(filename)
    # print "figure_path + filename:{}".format(figure_path + filename)

    plt.savefig(figure_path + filename)

def plotMultipleData(x, yList, yLabelList, title = "data", xAxisLabel = "x", yAxisLabel = "y",  yMin = None, yMax = None):
    '''
    Plot single input feature x data with multiple corresponding response values a scatter plot
    :param x:
    :param yList:
    :param yLabelList:
    :param title:
    :param xAxisLabel:
    :param yAxisLabe:
    :return: None
    '''

    fig = plt.figure()  # Create a new figure object for plotting
    ax = fig.add_subplot(111)

    markerList = np.array([",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "x", "D", "d",])
    markerList = markerList[ 0 : yLabelList.shape[0] ]

    # load iris data
    # iris = datasets.load_iris()
    for i in range (0, yList.shape[0]):
        # plt.scatter(x, yList[i], plt.cm.hot(float(i) / yList.shape[0]),  color=plt.cm.hot(float(i) / yList.shape[0]), marker='o', label = yLabelList[i])
        # for color print
        plt.scatter(x, yList[i], s=8,  color=plt.cm.hot(float(i) / yList.shape[0]), marker='o', label=yLabelList[i])
        # for monochrome print
        # plt.scatter(x, yList[i], s=8, color= str(float(i) / yList.shape[0]*0.80), marker=markerList[i], label=yLabelList[i])

    # add explanatory note
    plt.legend()
    # add labels to each axis
    plt.xlabel(xAxisLabel)
    plt.ylabel(yAxisLabel)
    # add title
    plt.title(title)

    if yMin is not None:
      plt.ylim(ymin = yMin)
    if yMax is not None:
      plt.ylim(ymax = yMax)
    # ax.set_title("\n".join(wrap(title + "OPVPricePerArea: " + str(OPVPricePerAreaUSD), 60)))
    plt.pause(.1)  # required on some systems so that rendering can happen

def plotData(x, t, title = "data", xAxisLabel = "x", yAxisLabel = "t", OPVPricePerAreaUSD = constant.OPVPricePerAreaUSD, arbitraryRegressionLine = False, \
             coeff0 = 0.0, coeff1 = 0.0, coeff2 = 0.0, coeff3 = 0.0, coeff4 = 0.0, coeff5 = 0.0):
    """
    Plot single input feature x data with corresponding response
    values t as a scatter plot
    :param x: sequence of 1-dimensional input data features
    :param t: sequence of 1-dimensional responses
    :param title: the title of the plot
    :param xAxisLabel: x-axix label of the plot
    :param xAxisLabel: y-axix label of the plot
    ;OPVPricePerAreaUSD: the OPV Price Per Area (USD/m^2)
    :return: None
    """
    #print "x:{}".format(x)
    #print "t:{}".format(t)

    #ax.ticklabel_format(style='plain',axis='y')
    fig = plt.figure()  # Create a new figure object for plotting
    ax = fig.add_subplot(111)

    plt.scatter(x, t, edgecolor='b', color='w', s = 8, marker='o')

    plt.xlabel(xAxisLabel)
    plt.ylabel(yAxisLabel)
    #plt.title(title + "OPVPricePerArea: " + OPVPricePerAreaUSD)
    plt.title(title)

    # add the OPV price per area [USD/m^2]
    # ax.set_title("\n".join(wrap(title + " (OPVPricePerArea: " + str(OPVPricePerAreaUSD)+"[USD/m^2])", 60)))

    if arbitraryRegressionLine:
        xLine = np.linspace(0, np.max(x), 100)
        y = coeff0 + coeff1 * xLine + coeff2 * xLine**2 + coeff3 * xLine**3 + coeff4 * xLine**4 + coeff5 * xLine**5
        plt.plot(xLine, y)

    plt.pause(.1)  # required on some systems so that rendering can happen


def plotTwoData(x, y1, y2,  title = "data", xAxisLabel = "x", yAxisLabel = "t", y1Label = "data1", y2Label = "data2"):
    '''
    Plot single input feature x data with two corresponding response values y1 and y2 as a scatter plot
    :param x:
    :param y1:
    :param y2:
    :param title:
    :param xAxisLabel:
    :param yAxisLabel:
    :return: None
    '''

    fig = plt.figure()  # Create a new figure object for plotting
    ax = fig.add_subplot(111)

    # for color printing
    plt.scatter(x, y1, edgecolor='red', color='red', s = 8, marker='o', label = y1Label)
    plt.scatter(x, y2, edgecolor='blue', color='blue', s = 8, marker='o',  label = y2Label)
    # for monochrome printing
    # plt.scatter(x, y1, edgecolor='0.1', color='0.1', s = 8, marker='o', label = y1Label)
    # plt.scatter(x, y2, edgecolor='0.7', color='0.8', s = 8, marker='x',  label = y2Label)

    plt.legend()
    plt.xlabel(xAxisLabel)
    plt.ylabel(yAxisLabel)
    plt.title(title)
    # ax.set_title("\n".join(wrap(title + "OPVPricePerArea: " + str(OPVPricePerAreaUSD), 60)))
    plt.pause(.1)  # required on some systems so that rendering can happen

def plotTwoDataMultipleYaxes(x, y1, y2, title, xAxisLabel, yAxisLabel1, yAxisLabel2, yLabel1, yLabel2):
    '''

    :param OPVCoverageList:
    :param unitDailyFreshWeightIncreaseList:
    :param electricityYield:
    :param title:
    :param xAxisLabel:
    :param yAxisLabel1:
    :param yAxisLabel2:
    :param yLabel1:
    :param yLabel2:
    :return:
    '''

    # Create a new figure object for plotting
    # fig = plt.figure()
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # for color printing
    ax1.scatter(x, y1, edgecolor='red', color='red', s = 8, marker='o', label = yLabel1)
    ax2.scatter(x, y2, edgecolor='blue', color='blue', s = 8, marker='o', label = yLabel2)
    # for monochrome printing
    # ax1.scatter(x, y1, edgecolor='0.1', color='0.1', s = 8, marker='o', label = yLabel1)
    # ax2.scatter(x, y2, edgecolor='0.7', color='0.8', s = 8, marker='x', label = yLabel2)


    # add the explanatory note
    ax1.legend()
    ax2.legend()
    ax1.set_xlabel(xAxisLabel)
    ax1.set_ylabel(yAxisLabel1)
    ax2.set_ylabel(yAxisLabel2)
    plt.title(title)
    # ax.set_title("\n".join(wrap(title + "OPVPricePerArea: " + str(OPVPricePerAreaUSD), 60)))
    plt.pause(.1)  # required on some systems so that rendering can happen


def plotCvResults(cv_loss, train_loss, cv_loss_title, figw=800, figh=420, mydpi=96, filepath=None, ylbl='Log Loss'):

  plt.figure(figsize=(figw / mydpi, figh / mydpi), dpi=mydpi)

  print ('>>>>> cv_loss.shape', cv_loss.shape)

  x = np.arange(0, cv_loss.shape[0])
  # cv_loss = np.mean(cv_loss, 0)
  # train_loss = np.mean(train_loss, 0)

  # put y-axis on same scale for all plots
  min_ylim = min(list(cv_loss) + list(train_loss))
  min_ylim = int(np.floor(min_ylim))
  max_ylim = max(list(cv_loss) + list(train_loss))
  max_ylim = int(np.ceil(max_ylim))

  print ('min_ylim={0}, max_ylim={1}'.format(min_ylim, max_ylim))

  plt.subplot(121)
  plt.plot(x, cv_loss, linewidth=2)
  plt.xlabel('Model Order')
  plt.ylabel(ylbl)
  plt.title(cv_loss_title)
  plt.pause(.1)  # required on some systems so that rendering can happen
  plt.ylim(min_ylim, max_ylim)

  plt.subplot(122)
  plt.plot(x, train_loss, linewidth=2)
  plt.xlabel('Model Order')
  plt.ylabel(ylbl)
  plt.title('Train Loss')
  plt.pause(.1)  # required on some systems so that rendering can happen
  plt.ylim(min_ylim, max_ylim)

  plt.subplots_adjust(right=0.95, wspace=0.25, bottom=0.2)
  plt.draw()

  if filepath:
    # plt.savefig(filepath, format='pdf')
    # print ("filepath:{}".format(filepath))
    plt.savefig(filepath)

def plotDataAndModel(x, y, w, title='Plot of data + appx curve (green curve)',filepath=None):
  plotDataSimple(x, y)
  plt.title(title + "_" + str(len(w)-1) + "th_order")
  plotModel(x, w, color='g')
  if filepath:
      plt.savefig(filepath, format='png')

def plotDataSimple(x, y):
  """
  Plot single input feature x data with corresponding response
  values y as a scatter plot
  :param x: sequence of 1-dimensional input data features
  :param y: sequence of 1-dimensional responses
  :return: None
  """
  plt.figure()  # Create a new figure object for plotting
  plt.scatter(x, y, edgecolor='b', color='w', s = 8, marker='o')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.xlim (min(x)*0.98, max(x)*1.02)
  plt.ylim (min(y)*0.98, max(y)*1.02)
  plt.title('Data')
  plt.pause(.1)  # required on some systems so that rendering can happen


def plotModel(x, w, color='r'):
  """
  Plot the curve for an n-th order polynomial model:
      t = w0*x^0 + w1*x^1 + w2*x^2 + ... wn*x^n
  This works by creating a set of x-axis (plotx) points and
  then use the model parameters w to determine the corresponding
  t-axis (plott) points on the model curve.
  :param x: sequence of 1-dimensional input data features
  :param w: n-dimensional sequence of model parameters: w0, w1, w2, ..., wn
  :param color: matplotlib color to plot model curve
  :return: the plotx and plott values for the plotted curve
  """
  # NOTE: this assumes a figure() object has already been created.
  plotx = np.linspace(min(x) - 0.25, max(x) + 0.25, 100)
  plotX = np.zeros((plotx.shape[0], w.size))
  for k in range(w.size):
      plotX[:, k] = np.power(plotx, k)
  plott = np.dot(plotX, w)
  plt.plot(plotx, plott, color=color, markersize = 10, linewidth=2)
  plt.pause(.1)  # required on some systems so that rendering can happen
  return plotx, plott


def sigma(m, n, func, s=0):
    '''
    calculate the summation for a given function.
    Reference: https://qiita.com/SheepCloud/items/b8bd929c4f35dfd7b1bd
    :param m: initial index
    :param n: final index. The term with the final index is calculated
    :param func: the function
    :param s: the default value before summing f(m). this is usually 0.0
    :return:
    '''
    # print("m:{}, n:{}, s:{}".format(m, n, s))


    if m > n: return s
    return sigma(m + 1, n, func, s + func(m))


class Counter(dict):
  """
  A counter keeps track of counts for a set of keys.

  The counter class is an extension of the standard python
  dictionary type.  It is specialized to have number values
  (integers or floats), and includes a handful of additional
  functions to ease the task of counting data.  In particular,
  all keys are defaulted to have value 0.  Using a dictionary:

  a = {}
  print a['test']

  would give an error, while the Counter class analogue:

  >>> a = Counter()
  >>> print a['test']
  0

  returns the default 0 value. Note that to reference a key
  that you know is contained in the counter,
  you can still use the dictionary syntax:

  >>> a = Counter()
  >>> a['test'] = 2
  >>> print a['test']
  2

  This is very useful for counting things without initializing their counts,
  see for example:

  >>> a['blah'] += 1
  >>> print a['blah']
  1

  The counter also includes additional functionality useful in implementing
  the classifiers for this assignment.  Two counters can be added,
  subtracted or multiplied together.  See below for details.  They can
  also be normalized and their total count and arg max can be extracted.
  """

  def __getitem__(self, idx):
    self.setdefault(idx, 0)
    return dict.__getitem__(self, idx)

  def incrementAll(self, keys, count):
    """
    Increments all elements of keys by the same count.

    >>> a = Counter()
    >>> a.incrementAll(['one','two', 'three'], 1)
    >>> a['one']
    1
    >>> a['two']
    1
    """
    for key in keys:
      self[key] += count

  def argMax(self):
    """
    Returns the key with the highest value.
    """
    if len(self.keys()) == 0: return None
    all = self.items()
    values = [x[1] for x in all]
    maxIndex = values.index(max(values))
    return all[maxIndex][0]

  def sortedKeys(self):
    """
    Returns a list of keys sorted by their values.  Keys
    with the highest values will appear first.

    >>> a = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> a['third'] = 1
    >>> a.sortedKeys()
    ['second', 'third', 'first']
    """
    sortedItems = self.items()
    compare = lambda x, y: sign(y[1] - x[1])
    sortedItems.sort(cmp=compare)
    return [x[0] for x in sortedItems]

  def totalCount(self):
    """
    Returns the sum of counts for all keys.
    """
    return sum(self.values())

  def normalize(self):
    """
    Edits the counter such that the total count of all
    keys sums to 1.  The ratio of counts for all keys
    will remain the same. Note that normalizing an empty
    Counter will result in an error.
    """
    total = float(self.totalCount())
    if total == 0: return
    for key in self.keys():
      self[key] = self[key] / total

  def divideAll(self, divisor):
    """
    Divides all counts by divisor
    """
    divisor = float(divisor)
    for key in self:
      self[key] /= divisor

  def copy(self):
    """
    Returns a copy of the counter
    """
    return Counter(dict.copy(self))

  def __mul__(self, y):
    """
    Multiplying two counters gives the dot product of their vectors where
    each unique label is a vector element.

    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['second'] = 5
    >>> a['third'] = 1.5
    >>> a['fourth'] = 2.5
    >>> a * b
    14
    """
    sum = 0
    x = self
    if len(x) > len(y):
      x, y = y, x
    for key in x:
      if key not in y:
        continue
      sum += x[key] * y[key]
    return sum

  def __radd__(self, y):
    """
    Adding another counter to a counter increments the current counter
    by the values stored in the second counter.

    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> a += b
    >>> a['first']
    1
    """
    for key, value in y.items():
      self[key] += value

  def __add__(self, y):
    """
    Adding two counters gives a counter with the union of all keys and
    counts of the second added to counts of the first.

    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> (a + b)['first']
    1
    """
    addend = Counter()
    for key in self:
      if key in y:
        addend[key] = self[key] + y[key]
      else:
        addend[key] = self[key]
    for key in y:
      if key in self:
        continue
      addend[key] = y[key]
    return addend

  def __sub__(self, y):
    """
    Subtracting a counter from another gives a counter with the union of all keys and
    counts of the second subtracted from counts of the first.

    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> (a - b)['first']
    -5
    """
    addend = Counter()
    for key in self:
      if key in y:
        addend[key] = self[key] - y[key]
      else:
        addend[key] = self[key]
    for key in y:
      if key in self:
        continue
      addend[key] = -1 * y[key]
    return addend
