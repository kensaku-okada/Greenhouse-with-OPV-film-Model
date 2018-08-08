# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 06 Nov 2016
# last edit date: 19 Apr 2017
#######################################################

##########import package files##########
import numpy as np
import math
import datetime

# #########################################################################
# ########### Reinforcement Learning (RL) constants start##################
# #########################################################################
# # labels of weights for features
# w_0 = "bias(w_0)"
# ##### 1 DLI to plants with the state and action
# w_1 = "DLIEachDayToPlants(w_1)"
# ##### 2 plant weight increase with the state and action
# w_2 = "unitDailyFreshWeightIncrease(w_2)"
# ##### 3 plant weight at the state
# w_3 = "accumulatedUnitDailyFreshWeightIncrease(w_3)"
# ##### 4 averageDLITillTheDay
# w_4 = "averageDLITillHarvestDay(w_4)"
# ##### 5 season effects (winter) representing dates.
# w_5 = "isSpring(w_5)"
# ##### 6 season effects (spring) representing dates.
# w_6 = "isSummer(w_6)"
# ##### 7 season effects (summer) representing dates.
# w_7 = "isAutumn(w_7)"
# ##### 8 season effects (autumn) representing dates.
# w_8 = "isWinter(w_8)"
#
# # starts from middle of Feb
# daysFromJanStartApril = 45
# # starts from May first
# daysFromJanStartSummer = 121
# # starts from middle of September
# daysFromJanStartAutumn = 259
# # starts from middle of Winter
# daysFromJanStartWinter = 320
#
# fileNameQLearningTrainedWeight = "qLearningTraintedWeights"
#
# ifRunTraining = True
# ifSaveCalculatedWeight = True
# ifLoadWeight = True
# ##############################################
# ########### RL constants end##################
# ##############################################

#####################################################
############ filepath and file name start ###########
#####################################################
environmentData = "20130101-20170101" + ".csv"

romaineLettceRetailPriceFileName = "romaineLettuceRetailPrice.csv"
romaineLettceRetailPriceFilePath = ""

averageRetailPriceOfElectricityMonthly = "averageRetailPriceOfElectricityMonthly.csv"

plantGrowthModelValidationData = "plantGrowthModelValidationData.csv"

# source: https://www.eia.gov/dnav/ng/hist/n3010az3m.htm
ArizonaPriceOfNaturalGasDeliveredToResidentialConsumers = "ArizonaPriceOfNaturalGasDeliveredToResidentialConsumers.csv"

###################################################
############ filepath and file name end ###########
###################################################


###############################################################
####################### If statement flag start ###############
###############################################################
# True: use the real data (the imported data whose source is the local weather station "https://midcdmz.nrel.gov/ua_oasis/),
# False: use the
ifUseOnlyRealData = False
# ifUseOnlyRealData = True

#If True,  export measured horizontal and estimated data when the simulation day is one day.
# ifExportMeasuredHorizontalAndExtimatedData = True

#If True, export measured horizontal and estimated data only on 15th day each month.
ifGet15thDayData = True
# ifGet15thDayData = False

# if consider the photo inhibition by too strong sunlight, True, if not, False
# IfConsiderPhotoInhibition = True
IfConsiderPhotoInhibition = False

# if consider the price discount by tipburn , True, if not, False
IfConsiderDiscountByTipburn = False

# make this false when running optimization algorithm
exportCSVFiles = True
# exportCSVFiles = False

# if you want to export CVS file and figures, then true
ifExportCSVFile = True
# ifExportCSVFile = False
# ifExportFigures = True
ifExportFigures = False


# if you want to refer to the price of lettuce grown at greenhouse (sales per head), True, if you sell lettuce at open field farming price (sales per kg), False
sellLettuceByGreenhouseRetailPrice = True
# sellLettuceByGreenhouseRetailPrice = False
print("sellLettuceByGreenhouseRetailPrice:{}".format(sellLettuceByGreenhouseRetailPrice))

#############################################################
####################### If statement flag end################
#############################################################

########################################
##########other constant start##########
########################################
# day on each month: days of Jan, Feb, ...., December
dayperMonthArray = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
dayperMonthLepArray = np.array([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

# keep them int
secondperMinute = 60
minuteperHour = 60
hourperDay = 24
dayperYear = 365
monthsperYear = 12
dayperLeapYear = 366
noonHour = 12

#the temperature at STC (Standard Test Conditions) unit [Celsius]
STCtemperature = 25.0
# current prepared data range: 20130101-20170101", 20150101 to 20160815 was the only correctly observed period. some 2014 data work too.
# do not choose "20140201 to 20160101" specifically. somehow it does not work.
# do not include 1/19/2014 as start date because 1/19/2014 partially misses its hourly data
# do not include after 8/18/2016 because the dates after 8/18/2016 do not correctly log the body temperature.
SimulationStartDate="20150101"
# SimulationStartDate="20150323"
# SimulationStartDate="20151215"
SimulationEndDate = "20151231"
# SimulationEndDate = "20150419"
# one cultivation cycle
# SimulationEndDate = "20151215"

sunnyDaysList = ["20150115", "20150217", "20150316", "20150413", "20150517", "20150615", "20150711", "20150815", "20150918", "20151013", "20151117", "20151215"]
print("SimulationStartDate:{}, SimulationEndDate:{}".format(SimulationStartDate, SimulationEndDate))

# latitude at Tucson == 32.2800408 N
Latitude = math.radians(32.2800408)
# longitude at Tucson 110.9422745 W
Longitude = math.radians(110.9422745)
# lambda (longitude of the site) = 32.2800408 N: latitude,-110.9422745 W : longitude  [degree]
# lambda_R ( the longitude of the time zone in which the site is situated) = 33.4484, 112.074 [degree]
# J' (the day angle in the year ) =

# John Page, "The Role of Solar-Radiation Climatology in the Design of Photovoltaic Systems", 2nd edition
# there is a equation calculating LAT.

# p618 (46 in pdf file)
# The passage of days is described mathematically by numbering the days continuously through the year to produce a Julian day number, J: 1
# January, J 5 1; 1 February, J 5 32; 1 March, J 5 57 in a nonleap year and 58 in a leap year; and so on. Each day in the year can be then be
# expressed in an angular form as a day angle, J0, in degrees by multiplying
# J by 360/365.25. The day angle is used in the many of the trigonometric expressions that follow.
# EOT (equation of time) =

#watt To PPFD Conversion coefficient for sunlight  (W m^-2) -> (μmol/m^2/s)
# the range of wavelength considered is around from 280 to 2800 (shortwave sunlight), not from 400nm to 700nm (visible sunlight).
wattToPPFDConversionRatio = 2.05
# wattToPPFDConversionRatio = 4.57 <- this ratio is used when the range of wavelength of PAR [W m^-2] is between 400nm and 700nm (visible sunlight)

# [W/m^2]
solarConstant = 1367.0
# ground reflectance of sunlight. source: https://www2.pvlighthouse.com.au/resources/courses/altermatt/The%20Solar%20Spectrum/The%20reflectance%20of%20the%20ground.aspx
groundReflectance = 0.1
# referred from A. Yano et. al., 2009, "Electrical energy generated by photovoltaic modules mounted inside the roof of a north–south oriented greenhouse"
# this number should be carefully definted according to the weather property of the simulation region (very cloudy: 0.0 ~ 1.0: very sunny)
# atmosphericTransmissivity = 0.6
# atmosphericTransmissivity = 0.7
# the reason why this coefficient was changed into this value is described in my paper
atmosphericTransmissivity = 0.643
print("atmosphericTransmissivity:{}".format(atmosphericTransmissivity))

# unit conversion. [cwt] -> [kg] US standard
kgpercwt = 45.3630

# if this is true, then continue to grow plants during the Summer period. the default value is False in the object(instance)
# ifGrowForSummerPeriod = True
ifGrowForSummerPeriod = False
print("ifGrowForSummerPeriod:{}".format(ifGrowForSummerPeriod))
######################################
##########other constant end##########
######################################

#########################################################
##########Specification of the greenhouse start##########
#########################################################

# #########################################################
# # Our real greenhouse specification source:
# # http://www.gpstructures.com/pdfs/Windjammer.pdf
# # We used 6' TALL SIDEWALL HEIGHT 30' width, Free Standing Structures in our project.
# #greenhouse roof type
# greenhouseRoofType = "SimplifiedAFlame"
# #width of the greenhouse (m)
# greenhouseWidth = 9.144 # = 30 [feet]
# #depth of the greenhouse (m)
# greenhouseDepth = 14.6
# #area of the greenhouse (m**2)
# greenhouseFloorArea = greenhouseWidth * greenhouseDepth
# # print("greenhouseFloorArea[m^2]:{}".format(greenhouseFloorArea))
# #width of the greenhouse cultivation area (m)
# greenhouseCultivationFloorWidth = 7.33
# #depth of the greenhouse cultivation area(m)
# greenhouseCultivationFloorDepth = 10.89
# #floor area of greenhouse cultivation area(m**2)
# greenhouseCultivationFloorArea = greenhouseCultivationFloorWidth * greenhouseCultivationFloorDepth
# # greenhouseCultivationFloorArea = greenhouseWidth * greenhouseDepth * 0.9
# # print("greenhouseCultivationFloorArea[m^2]:{}".format(greenhouseCultivationFloorArea))
# # number of roofs. If this is 1, the greenhouse is a single roof greenhouse. If >1, multi-roof greenhouse
# numOfRoofs = 1
# # the type of roof direction
# roofDirectionNotation = "EastWestDirectionRoof"
# #side wall height of greenhouse (m)
# greenhouseHeightSideWall = 1.8288 # = 6[feet]
# #center height of greenhouse (m)
# greenhouseHeightRoofTop = 4.8768 # = 16[feet]
# #width of the rooftop. calculate from the Pythagorean theorem. assumed that the shape of rooftop is straight, not curved.
# greenhouseRoofWidth = math.sqrt((greenhouseWidth/2.0)**2.0 + (greenhouseHeightRoofTop-greenhouseHeightSideWall)**2.0)
# #print ("greenhouseRoofWidth: {}".format(greenhouseRoofWidth))
# #angle of the rooftop (theta θ). [rad]
#
# greenhouseRoofAngle = math.acos((greenhouseWidth/2.0) / greenhouseRoofWidth)
# # print ("greenhouseRoofAngle (rad) : {}".format(greenhouseRoofAngle))
# # the angle of the roof facing north or east [rad]
# roofAngleNorthOrEast = greenhouseRoofAngle
# # the angle of the roof facing south or west [rad]. This should be modified if the roof angle is different from the other side.
# roofAngleWestOrSouth = greenhouseRoofAngle
# #area of the rooftop [m^2]. summing the left and right side of rooftops from the center.
# greenhouseTotalRoofArea = greenhouseRoofWidth * greenhouseDepth * 2.0
# # print ("greenhouseRoofArea[m^2]: {}".format(greenhouseTotalRoofArea))1
# #########################################################


#########################################################
# Virtual greenhouse specification, the multi-roof greenhouse virtually connected 10 of our real greenhouses.
# You can change these numbers according to your greenhouse design and specification
#greenhouse roof type
greenhouseRoofType = "SimplifiedAFlame"
# #width of the greenhouse (m)
# greenhouseWidth = 91.44 #
# #depth of the greenhouse (m)
# greenhouseDepth = 14.6

# the greenhouse floor area was replaced with the following, referring to a common business size greenhouse

# number of roofs (-). If this is 1, the greenhouse is a single roof greenhouse. If >1, multi-roof greenhouse.
numOfRoofs = 10.0
# source: https://www.interempresas.net/FeriaVirtual/Catalogos_y_documentos/1381/Multispan-greenhouse-ULMA-Agricola.pdf,
# source: https://www.alibaba.com/product-detail/Multi-roof-Poly-Film-Tunnel-Greenhouse_60184626287.html
# this should be cahnged depending on the type of greenhouse simulated. (m)
widthPerRoof = 9.6
#total width of the greenhouse (m)
# greenhouseWidth = 91.44
greenhouseWidth = numOfRoofs * widthPerRoof

#depth of the greenhouse (m)
greenhouseDepth = 14.6

#area of the greenhouse (m**2)
greenhouseFloorArea = greenhouseWidth * greenhouseDepth
print("greenhouseFloorArea[m^2]:{}".format(greenhouseFloorArea))
# # the following calculation gives the real cultivation area of our research greenhouse. However, since it has too large vacant space which is unrealistic for business greenhouse, this number was not used.
# #width of the greenhouse cultivation area (m)
# greenhouseCultivationFloorWidth = 73.3
# #depth of the greenhouse cultivation area(m)
# greenhouseCultivationFloorDepth = 10.89
# #floor area of greenhouse cultivation area(m**2)
# greenhouseCultivationFloorArea = greenhouseCultivationFloorWidth * greenhouseCultivationFloorDepth
# Instead, it was assumed the cultivation area is 0.9 time of the total greenhouse floor area
greenhouseCultivationFloorArea = greenhouseFloorArea * 0.9
print("greenhouseCultivationFloorArea[m^2]:{}".format(greenhouseCultivationFloorArea))
# the type of roof direction
roofDirectionNotation = "EastWestDirectionRoof"
# roofDirectionNotation = "NorthSouthDirectionRoof"
#side wall height of greenhouse (m)
greenhouseHeightSideWall = 1.8288 # = 6[feet]
# the total sidewall area
greenhouseSideWallArea = 2.0 * (greenhouseWidth + greenhouseDepth) * greenhouseHeightSideWall
print("greenhouseSideWallArea[m^2]:{}".format(greenhouseSideWallArea))

#center height of greenhouse (m)
greenhouseHeightRoofTop = 4.8768 # = 16[feet]

#width of the rooftop. calculate from the Pythagorean theorem. assumed that the shape of rooftop is straight (not curved), and the top height and roof angels are same at each roof.
greenhouseRoofWidth = math.sqrt((greenhouseWidth/(numOfRoofs*2.0))**2.0 + (greenhouseHeightRoofTop-greenhouseHeightSideWall)**2.0)
print ("greenhouseRoofWidth [m]: {}".format(greenhouseRoofWidth))
# the length of the roof facing east or north
greenhouseRoofWidthEastOrNorth = greenhouseRoofWidth
# the length of the roof facing west or south
greenhouseRoofWidthWestOrSouth = greenhouseRoofWidth

#angle of the rooftop (theta θ). [rad]
greenhouseRoofAngle = math.acos(((greenhouseWidth/(numOfRoofs*2.0)) / greenhouseRoofWidth))
# greenhouseRoofAngle = 0.0
print ("greenhouseRoofAngle (rad) : {}".format(greenhouseRoofAngle))
# the angle of the roof facing north or east [rad]
roofAngleEastOrNorth = greenhouseRoofAngle
# the angle of the roof facing south or west [rad]. This should be modified if the roof angle is different from the other side.
roofAngleWestOrSouth = greenhouseRoofAngle
# area of the rooftop [m^2]. summing the left and right side of rooftops from the center.
greenhouseTotalRoofArea = greenhouseRoofWidth * greenhouseDepth * numOfRoofs * 2.0
print ("greenhouseTotalRoofArea[m^2]: {}".format(greenhouseTotalRoofArea))

greenhouseRoofTotalAreaEastOrNorth = greenhouseRoofWidthEastOrNorth * greenhouseDepth * numOfRoofs
print ("greenhouseRoofTotalAreaEastOrNorth[m^2]: {}".format(greenhouseRoofTotalAreaEastOrNorth))
greenhouseRoofTotalAreaWestOrSouth = greenhouseRoofWidthWestOrSouth * greenhouseDepth * numOfRoofs
print ("greenhouseRoofTotalAreaWestOrSouth[m^2]: {}".format(greenhouseRoofTotalAreaWestOrSouth))
#########################################################

#the proportion of shade made by the greenhouse inner structure, actuator (e.g. sensors and fog cooling systems) and farming equipments (e.g. gutters) (-)
# GreenhouseShadeProportion = 0.1
GreenhouseShadeProportionByInnerStructures = 0.05

# DLI [mol m^-2 day^-1]
DLIForButterHeadLettuceWithNoTipburn = 17.0
# PPFD [umol m^-2 s^-1]
# the PPFD was divided by 2.0 because it was assumed that the time during the day was the half of a day (12 hours)
# OptimumPPFDForButterHeadLettuceWithNoTipburn = DLIForButterHeadLettuceWithNoTipburn * 1000000.0 / float(secondperMinute*minuteperHour*hourperDay)
OptimumPPFDForButterHeadLettuceWithNoTipburn = DLIForButterHeadLettuceWithNoTipburn * 1000000.0 / float(secondperMinute*minuteperHour*hourperDay/2.0)
print("OptimumPPFDForButterHeadLettuceWithNoTipburn (PPFD):{}".format(OptimumPPFDForButterHeadLettuceWithNoTipburn))

# 1.5 is an arbitrary number
# the amount of PPFD to deploy shading curtain
shadingCurtainDeployPPFD = OptimumPPFDForButterHeadLettuceWithNoTipburn * 1.5
print("shadingCurtainDeployPPFD:{}".format(shadingCurtainDeployPPFD))

# The maximum value of m: the number of roofs that incident light penetrating in the model. This value is used at SolarIrradianceMultiroofRoof.py.
# if the angle between the incident light and the horizonta ql axis is too small, the m can be too large, which cause a system error at Util.sigma by iterating too much and make the simulation slow.
# Thus, the upper limit was set.
mMax = numOfRoofs
# defaultIterationLimit = 495
#######################################################
##########Specification of the greenhouse end##########
#######################################################

##################################################################
##########specification of glazing (covering film) start##########
##################################################################
greenhouseGlazingType = "polyethylene (PE) DoubleLayer"

#ratio of visible light (400nm - 750nm) through a glazing material (-)
#source: Nadia Sabeh, "TOMATO GREENHOUSE ROADMAP" https://www.amazon.com/Tomato-Greenhouse-Roadmap-Guide-Production-ebook/dp/B00O4CPO42
# https://www.goodreads.com/book/show/23878832-tomato-greenhouse-roadmap
# singlePEPERTransmittance = 0.875
singlePERTransmittance = 0.85
dobulePERTransmittance = singlePERTransmittance ** 2.0
# reference: https://www.filmetrics.com/refractive-index-database/Polyethylene/PE-Polyethene
PEFilmRefractiveIndex = 1.5
# reference: https://en.wikipedia.org/wiki/Refractive_index
AirRefractiveIndex = 1.000293

# Source of reference https://www.amazon.com/Tomato-Greenhouse-Roadmap-Guide-Production-ebook/dp/B00O4CPO42
singlePolycarbonateTransmittance = 0.91
doublePolycarbonateTransmittance = singlePolycarbonateTransmittance ** 2.0

roofCoveringTransmittance = singlePERTransmittance
sideWallTransmittance = singlePERTransmittance

################################################################
##########specification of glazing (covering film) end##########
################################################################

#####################################################################
##########specification of OPV module (film or panel) start##########
#####################################################################

# [rad]. tilt of OPV module = tilt of the greenhouse roof
# OPVAngle = math.radians(0.0)
OPVAngle = greenhouseRoofAngle

# the coverage ratio of OPV module on the greenhouse roof [-]
# OPVAreaCoverageRatio = 0.20
# OPVAreaCoverageRatio = 0.58
# OPVAreaCoverageRatio = 0.5
OPVAreaCoverageRatio = 0.009090909090909
# print("OPVAreaCoverageRatio:{}".format(OPVAreaCoverageRatio))

# the coverage ratio of OPV module on the greenhouse roof [-]. If you set this value same as OPVAreaCoverageRatio, it assumed that the OPV coverage ratio does not change during the whole period
# OPVAreaCoverageRatioSummerPeriod = 1.0
# OPVAreaCoverageRatioSummerPeriod = 0.5
OPVAreaCoverageRatioSummerPeriod = OPVAreaCoverageRatio
# OPVAreaCoverageRatioSummerPeriod = 0.0
print("OPVAreaCoverageRatioSummerPeriod:{}".format(OPVAreaCoverageRatioSummerPeriod))


#the area of OPV on the roofTop.
OPVArea = OPVAreaCoverageRatio * greenhouseTotalRoofArea
print("OPVArea:{}".format(OPVArea))

# the PV module area facing each angle
OPVAreaFacingEastOrNorthfacingRoof = OPVArea * (greenhouseRoofTotalAreaEastOrNorth/greenhouseTotalRoofArea)
OPVAreaFacingWestOrSouthfacingRoof = OPVArea * (greenhouseRoofTotalAreaWestOrSouth/greenhouseTotalRoofArea)

#the ratio of degradation per day (/day)
# TODO: find a paper describing the general degradation ratio of OPV module
#the specification document of our PV module says that the guaranteed quality period is 1 year.
# reference (degradation ratio of PV module): https://www.nrel.gov/docs/fy12osti/51664.pdf, https://www.solar-partners.jp/pv-eco-informations-41958.html
# It was assumed that inorganic PV module expiration date is 20 years and its yearly degradation rate is 0.8% (from the first reference page 6), which indicates the OPV film degrades faster by 20 times.
PVDegradationRatioPerHour =  20.0 * 0.008 / dayperYear / hourperDay
print("PVDegradationRatioPerHour:{}".format(PVDegradationRatioPerHour))


# the coefficient converting the ideal (given by manufacturers) cell efficiency to the real efficiency under actual conditions
# degradeCoefficientFromIdealtoReal = 0.85
# this website (https://franklinaid.com/2013/02/06/solar-power-for-subs-the-panels/) says "In real-life conditions, the actual values will be somewhat more or less than listed by the manufacturer."
# So it was assumed the manufacture's spec sheet correctly shows the actual power
degradeCoefficientFromIdealtoReal = 1.00


########################################################################################################################
# the following information should be taken from the spec sheet provided by a PV module manufacturer
########################################################################################################################
#unit[/K]. The proportion of a change of voltage which the OPV film generates under STC condition (25°C),
# mentioned in # Table 1-2-1
TempCoeffitientVmpp =  -0.0019

#unit[/K]. The proportion of a change of current which the OPV film generates under STC condition (25°C),
# mentioned in Table 1-2-1
TempCoeffitientImpp =  0.0008

#unit[/K]. The proportion of a change of power which the OPV film generates under STC condition (25°C),
# mentioned in Table 1-2-
TempCoeffitientPmpp =  0.0002

#transmission ratio of VISIBLE sunlight through OPV film.
#OPVPARTransmittance = 0.6
OPVPARTransmittance = 0.3

# unit: [A]
shortCircuitCurrent = 0.72
# unit [V]
openCIrcuitVoltage = 24.0
# unit: [A]
currentAtMaximumPowerPoint = 0.48
# unit [V]
voltageAtMaximumPowerPoint = 16.0
# unit: [watt]
maximumPower = currentAtMaximumPowerPoint * voltageAtMaximumPowerPoint
print("maximumPower:{}".format(maximumPower))
# unit: [m^2]. This is the area per sheet, not roll (having 8 sheets concatenated). This area excludes the margin space of the OPV sheet. THe margin space are made from transparent laminated film with connectors.
OPVAreaPerSheet = 0.849 * 0.66

#conversion efficiency from ligtht energy to electricity
#The efficiency of solar panels is based on standard testing conditions (STC),
#under which all solar panel manufacturers must test their modules. STC specifies a temperature of 25°C (77 F),
#solar irradiance of 1000 W/m2 and an air mass 1.5 (AM1.5) spectrums.
#The STC efficiency of a 240-watt module measuring 1.65 square meters is calculated as follows:
#240 watts ÷ (1.65m2 (module area) x 1000 W/m2) = 14.54%.
#source: http://www.solartown.com/learning/solar-panels/solar-panel-efficiency-have-you-checked-your-eta-lately/
# http://www.isu.edu/~rodrrene/Calculating%20the%20Efficiency%20of%20the%20Solar%20Cell.doc
# unit: -
# OPVEfficiencyRatioSTC = maximumPower / OPVAreaPerSheet / 1000.0

# OPVEfficiencyRatioSTC = 0.2
# this value is the cell efficiency of OPV film purchased at Kacira Lab, CEAC at University of Arizona
# OPVEfficiencyRatioSTC = 0.0137
# source: 19.	Lucera, L., Machui, F., Schmidt, H. D., Ahmad, T., Kubis, P., St  rohm, S., … Brabec, C. J. (2017). Printed semi-transparent large area organic photovoltaic modules with power conversion efficiencies of close to 5 %. Organic Electronics: Physics, Materials, Applications, 45, 41–45. https://doi.org/10.1016/j.orgel.2017.03.013
OPVEfficiencyRatioSTC = 0.043
print("OPVCellEfficiencyRatioSTC:{}".format(OPVEfficiencyRatioSTC))
#what is an air mass??
#エアマスとは太陽光の分光放射分布を表すパラメーター、標準状態の大気（標準気圧１０１３ｈＰａ）に垂直に入射（太陽高度角９０°）した
# 太陽直達光が通過する路程の長さをＡＭ１．０として、それに対する比で表わされます。
#source: http://www.solartech.jp/module_char/standard.html

########################################################################################################################

#source: http://energy.gov/sites/prod/files/2014/01/f7/pvmrw13_ps5_3m_nachtigal.pdf (3M Ultra-Barrier Solar Film spec.pdf)

#the price of OPV per area [EUR/m^2]
# [EUR]
originalOPVPriceEUR = 13305.6
OPVPriceEUR = 13305.6
# [m^2]
OPVSizePurchased = 6.0 * 0.925 * 10.0

# [EUR/m^2]
OPVPriceperAreaEUR = OPVPriceEUR / OPVSizePurchased

#as of 11Nov/2016 [USD/EUR]
CurrencyConversionRatioUSDEUR= 1/1.0850
#the price of OPV per area [USD/m^2]
# OPVPricePerAreaUSD = OPVPriceperAreaEUR*CurrencyConversionRatioUSDEUR
# OPVPricePerAreaUSD = 50.0
OPVPricePerAreaUSD = 0.0
# reference of PV panel purchase cost. 200 was a reasonable price in the US.
# https://www.homedepot.com/p/Grape-Solar-265-Watt-Polycrystalline-Solar-Panel-4-Pack-GS-P60-265x4/206365811?cm_mmc=Shopping%7cVF%7cG%7c0%7cG-VF-PLA%7c&gclid=Cj0KCQjw6pLZBRCxARIsALaaY9YIkZf5W4LESs9HA2RgxsYaeXOfzvMuMCUT9iZ7xU65GafQel6FIY8aApLfEALw_wcB&dclid=CLjZj46A2NsCFYQlfwodGQoKsQ
# https://www.nrel.gov/docs/fy17osti/68925.pdf
# OPVPricePerAreaUSD = 200.0
print("OPVPricePerAreaUSD:{}".format(OPVPricePerAreaUSD))


# True == consider the OPV cost, False == ignore the OPV cost
ifConsiderOPVCost = True
# if you set this 730, you assume the purchase cost of is OPV zero because at the simulator class, this number divides the integer number, which gives zero.
# OPVDepreciationPeriodDays = 730.0
OPVDepreciationPeriodDays = 365.0

OPVDepreciationMethod = "StraightLine"
###################################################################
##########specification of OPV module (film or panel) end##########
###################################################################

##########################################################
##########specification of shading curtain start##########
##########################################################
#the transmittance ratio of shading curtain
shadingTransmittanceRatio = 0.45

isShadingCurtainReinforcementLearning = True

#if True, a black net is covered over the roof for shading in summer
# hasShadingCurtain = False
hasShadingCurtain = True

openCurtainString = "openCurtain"
closeCurtainString = "closeCurtain"

# ######## default setting ########
# ShadingCurtainDeployStartMMSpring = 5
# ShadingCurtainDeployStartDDSpring = 31
# ShadingCurtainDeployEndMMSpring = 5
# ShadingCurtainDeployEndDDSpring = 31
# ShadingCurtainDeployStartMMFall =9
# ShadingCurtainDeployStartDDFall =15
# ShadingCurtainDeployEndMMFall =6
# ShadingCurtainDeployEndDDFall =29

# # # optimzed period on greenhouse retail price, starting from minimum values
# ShadingCurtainDeployStartMMSpring = 1
# ShadingCurtainDeployStartDDSpring = 1
# ShadingCurtainDeployEndMMSpring = 1
# ShadingCurtainDeployEndDDSpring = 4
# ShadingCurtainDeployStartMMFall = 1
# ShadingCurtainDeployStartDDFall = 6
# ShadingCurtainDeployEndMMFall = 1
# ShadingCurtainDeployEndDDFall = 16

# # # optimzed period on greenhouse retail price, starting from middle values
# ShadingCurtainDeployStartMMSpring = 6
# ShadingCurtainDeployStartDDSpring = 19
# ShadingCurtainDeployEndMMSpring = 7
# ShadingCurtainDeployEndDDSpring = 5
# ShadingCurtainDeployStartMMFall = 7
# ShadingCurtainDeployStartDDFall = 14
# ShadingCurtainDeployEndMMFall = 7
# ShadingCurtainDeployEndDDFall = 15

# # # optimzed period on greenhouse retail price, starting from max values
# ShadingCurtainDeployStartMMSpring = 12
# ShadingCurtainDeployStartDDSpring = 24
# ShadingCurtainDeployEndMMSpring = 12
# ShadingCurtainDeployEndDDSpring = 28
# ShadingCurtainDeployStartMMFall = 12
# ShadingCurtainDeployStartDDFall = 30
# ShadingCurtainDeployEndMMFall = 12
# ShadingCurtainDeployEndDDFall = 31

# optimzed period on open field farming retail price, starting from max values
# ShadingCurtainDeployStartMMSpring = 8
# ShadingCurtainDeployStartDDSpring = 28
# ShadingCurtainDeployEndMMSpring = 12
# ShadingCurtainDeployEndDDSpring = 2
# ShadingCurtainDeployStartMMFall = 12
# ShadingCurtainDeployStartDDFall = 12
# ShadingCurtainDeployEndMMFall = 12
# ShadingCurtainDeployEndDDFall = 31

# # # initial date s for optimization
ShadingCurtainDeployStartMMSpring = 5
ShadingCurtainDeployStartDDSpring = 17
ShadingCurtainDeployEndMMSpring = 6
ShadingCurtainDeployEndDDSpring = 12
ShadingCurtainDeployStartMMFall = 6
ShadingCurtainDeployStartDDFall = 23
ShadingCurtainDeployEndMMFall = 7
ShadingCurtainDeployEndDDFall = 2


# Summer period. This should happend soon after ending the shading curtain deployment period.
SummerPeriodStartDate = datetime.date(int(SimulationStartDate[0:4]), ShadingCurtainDeployEndMMSpring, ShadingCurtainDeployEndDDSpring) + datetime.timedelta(days=1)
SummerPeriodEndDate = datetime.date(int(SimulationStartDate[0:4]), ShadingCurtainDeployStartMMFall, ShadingCurtainDeployStartDDFall) - datetime.timedelta(days=1)

SummerPeriodStartMM = int(SummerPeriodStartDate.month)
print("SummerPeriodStartMM:{}".format(SummerPeriodStartMM))
SummerPeriodStartDD = int(SummerPeriodStartDate.day)
print("SummerPeriodStartDD:{}".format(SummerPeriodStartDD))
SummerPeriodEndMM = int(SummerPeriodEndDate.month)
print("SummerPeriodEndMM:{}".format(SummerPeriodEndMM))
SummerPeriodEndDD = int(SummerPeriodEndDate.day)
print("SummerPeriodEndDD:{}".format(SummerPeriodEndDD))

# this is gonna be True when you want to deploy shading curtains only from  ShadigCuratinDeployStartHH to ShadigCuratinDeployEndHH
IsShadingCurtainDeployOnlyDayTime = True
ShadigCuratinDeployStartHH = 10
ShadigCuratinDeployEndHH = 14
IsDifferentShadingCurtainDeployTimeEachMonth = True

# this is gonna be true when you want to control shading curtain opening and closing every hour
IsHourlyShadingCurtainDeploy = False
########################################################
##########specification of shading curtain end##########
########################################################


#################################################
##########Specification of plants start##########
#################################################
#Cost of plant production. the unit is USD/m^2
# the conversion rate was calculated from from University of California Cooperative Extension (UCEC) UC Small farm program (http://sfp.ucdavis.edu/crops/coststudieshtml/lettuce/LettuceTable1/)
plantProductionCostperSquareMeterPerYear = 1.096405

numberOfRidge = 5.0

#unit: m. plant density can be derived from this.
distanceBetweenPlants = 0.2

# plant density (num of heads per area) [head/m^2]
plantDensity = 1.0/(distanceBetweenPlants**2.0)
print("plantDensity:{}".format(plantDensity))

#number of heads
# numberOFheads = int(greenhouseCultivationFloorDepth/distanceBetweenPlants * numberOfRidge)
numberOFheads = int (plantDensity * greenhouseCultivationFloorArea)
print("numberOFheads:{}".format(numberOFheads))

# number of head per cultivation area [heads/m^2]
numberOFheadsPerArea = float(numberOFheads / greenhouseCultivationFloorArea)

#photoperiod (time of lighting in a day). the unit is hour
# TODO: this should be revised so that the photo period is calculated by the sum of PPFD each day or the change of direct solar radiation or the diff of sunse and sunrise
photoperiod = 14.0

#number of cultivation days (days/harvest)
cultivationDaysperHarvest = 35
# cultivationDaysperHarvest = 30

# the constant of each plant growth model
# Source: https://www.researchgate.net/publication/266453402_TEN_YEARS_OF_HYDROPONIC_LETTUCE_RESEARCH
A_J_Both_Modified_TaylorExpantionWithFluctuatingDLI = "A_J_Both_Modified_TaylorExpantionWithFluctuatingDLI"
# Source: https://www.researchgate.net/publication/4745082_Validation_of_a_dynamic_lettuce_growth_model_for_greenhouse_climate_control
E_J_VanHenten1994 = "E_J_VanHenten1994"
# Source: https://www.researchgate.net/publication/286938495_A_validated_model_to_predict_the_effects_of_environment_on_the_growth_of_lettuce_Lactuca_sativa_L_Implications_for_climate_change
S_Pearson1997 = "S_Pearson1997"
plantGrowthModel = E_J_VanHenten1994

# lettuce base temperature [Celusius]
# Reference: A validated model to predict the effects of environment on the growth of lettuce (Lactuca sativa L.): Implications for climate change
# https://www.tandfonline.com/doi/abs/10.1080/14620316.1997.11515538
lettuceBaseTemperature = 0.0
DryMassToFreshMass = 1.0/0.045

# the weight to harvest [g]
harvestDryWeight = 200.0 / DryMassToFreshMass
# harvestDryWeight = 999.0 / DryMassToFreshMass

# operation cost of plants [USD/m^2/year]
plantcostperSquaremeterperYear = 1.096405

# the DLI upper limitation causing some tipburn
DLIforTipBurn = DLIForButterHeadLettuceWithNoTipburn

# the discount ratio when there are some tipburn observed
tipburnDiscountRatio = 0.2

# make this number 1.0 in the end. change this only for simulation experiment
plantPriceDiscountRatio_justForSimulation = 1.0

# the set point temperature during day time [Celusius]
# reference: A.J. Both, TEN YEARS OF HYDROPONIC LETTUCE RESEARCH: https://www.researchgate.net/publication/266453402_TEN_YEARS_OF_HYDROPONIC_LETTUCE_RESEARCH
setPointTemperatureDayTime = 24.0
# setPointTemperatureDayTime = 16.8

# the set point temperature during night time [Celusius]
# reference: A.J. Both, TEN YEARS OF HYDROPONIC LETTUCE RESEARCH: https://www.researchgate.net/publication/266453402_TEN_YEARS_OF_HYDROPONIC_LETTUCE_RESEARCH
setPointTemperatureNightTime = 19.0
# setPointTemperatureNightTime = 16.8

setPointHumidityDayTime = 0.65
# setPointHumidityDayTime = 0.7
setPointHumidityNightTime = 0.8
# setPointHumidityNightTime = 0.7

# the flags indicating daytime or nighttime at each time step
daytime = "daytime"
nighttime = "nighttime"

# sales price of lettuce grown at greenhouses, which is usually higher than that of open field farming grown lettuce
# source
# 1.99 USD head-1 for "Lettuce, Other, Boston-Greenhouse") cited from USDA (https://www.ams.usda.gov/mnreports/fvwretail.pdf)
# other source: USDA, Agricultural, Marketing, Service, National Retail Report - Specialty Crops page 9 and others: https://www.ams.usda.gov/mnreports/fvwretail.pdf
# unit: USD head-1
romainLettucePriceBasedOnHeadPrice = 1.99

###################################################
##########Specification of the plants end##########
###################################################



###################################################
##########Specification of labor cost start########
###################################################
# source: https://onlinelibrary.wiley.com/doi/abs/10.1111/cjag.12161
# unit: people/10000kg yield
necessaryLaborPer10000kgYield = 0.315

# source:https://www.bls.gov/regions/west/news-release/occupationalemploymentandwages_tucson.htm
# unit:USD/person/hour
hourlyWagePerPerson = 12.79

# unit: hour/day
workingHourPerDay = 8.0

###################################################
##########Specification of labor cost end########
###################################################


###################################################
##########Specification of energy cost start#######
###################################################

# energy efficiency of heating equipment [-]
# source: https://www.alibaba.com/product-detail/Natural-gas-fired-hot-air-heater_60369835987.html?spm=a2700.7724838.2017115.1.527251bcQ2pojZ
# source: https://www.aga.org/natural-gas/in-your-home/heating/
heatingEquipmentEfficiency = 0.9

# unit: USD
heatingEquipmentQurchaseCost = 0.0

# source: http://www.world-nuclear.org/information-library/facts-and-figures/heat-values-of-various-fuels.aspx
# source: http://agnatural.pt/documentos/ver/natural-gas-conversion-guide_cb4f0ccd80ccaf88ca5ec336a38600867db5aaf1.pdf
# unit: MJ m-3
naturalGasSpecificEnergy = {"MJ m-3" :38.7}
naturalGasSpecificEnergy["MJ ft-3"] = naturalGasSpecificEnergy["MJ m-3"] / 35.3147
heatOfWaterEcaporation = {"J kg-1" : 2257}


# source: https://www.researchgate.net/publication/265890843_A_Review_of_Evaporative_Cooling_Technologies?enrichId=rgreq-2c40013798cfb3c564cf35844f4947fb-XXX&enrichSource=Y292ZXJQYWdlOzI2NTg5MDg0MztBUzoxNjUxOTgyMjg4OTM2OTdAMTQxNjM5NzczNTk5Nw%3D%3D&el=1_x_3&_esc=publicationCoverPdf
# COP = coefficient of persormance. COP = Q/W
# Q is the useful heat supplied or removed by the considered system. W is the work required by the considered system.
PadAndFanCOP = 15.0
###################################################
##########Specification of energy cost end#########
###################################################


#########################################################################
###########################Global variable end###########################
#########################################################################

class CropElectricityYeildSimulatorConstant:
    """
    a constant class.

    """

    ###########the constractor##################
    def __init__(self):
        print ("call CropElectricityYeildSimulatorConstant")

    ###########the constractor end##################

    ###########the methods##################
    def method(self, val):
        print("call CropElectricityYeildSimulatorConstant method")

    ###########the methods end##################
