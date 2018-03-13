import CropElectricityYeildSimulatorConstant as constant

class SimulatorClass:

  # constructor
  def __init__(self):

    self._OPVAreaCoverageRatio = constant.OPVAreaCoverageRatio
    self._OPVCoverageFallowPeriod = constant.OPVAreaCoverageRatioFallowPeriod
    self._plantGrowthModel = constant.E_J_VanHenten
    self._cultivationDaysperHarvest = constant.cultivationDaysperHarvest
    self._hasShadingCurtain = constant.hasShadingCurtain
    self._shadingCurtainDeployPPFD = constant.plantGrowthModel
    self._profitVSOPVCoverageData = None
    self._monthlyElectricitySalesperArea = None
    self._monthlyElectricitySalesperAreaEastRoof = None
    self._monthlyElectricitySalesperAreaWestRoof = None
    self._oPVCostUSDForDepreciationperArea = None

    self._hourlyInnerLightIntensityPPFDThroughGlazing = None
    self._hourlyInnerLightIntensityPPFDThroughInnerStructure = None
    self._directPPFDToOPVEastDirection = None
    self._directPPFDToOPVWestDirection = None
    self._diffusePPFDToOPV = None
    self._groundReflectedPPFDToOPV = None
    self._totalDLItoPlantsBaselineShadingCuratin = None
    self._directDLIToOPVEastDirection = None
    self._directDLIToOPVWestDirection = None
    self._diffuseDLIToOPV = None
    self._groundReflectedDLIToOPV = None
    self._hourlyDirectSolarRadiationToMultiSpanRoof = None
    self._hourlyDiffuseSolarRadiationToMultiSpanRoof = None
    self._groundReflectedRadiationToMultiSpanRoof = None
    self._hourlyDirectPPFDToMultiSpanRoof = None
    self._hourlyDiffusePPFDToMultiSpanRoof = None
    self._groundReflectedPPFDToMultiSpanRoof = None

    self._shootFreshMassList = None
    self._unitDailyFreshWeightIncrease = None
    self._accumulatedUnitDailyFreshWeightIncrease = None
    self._unitDailyHarvestedFreshWeight = None
    self._averageDLIonEachCycle = None
    self._year = None
    self._month = None
    self._day = None
    self._hour = None
    self._importedHourlyHorizontalDirectSolarRadiation = None
    self._importedHourlyHorizontalDiffuseSolarRadiation = None
    self._importedHourlyHorizontalTotalBeamMeterBodyTemperature = None
    self._importedHourlyAirTemperature = None
    self._directSolarRadiationToOPVEastDirection = None
    self._directSolarRadiationToOPVWestDirection = None
    self._diffuseSolarRadiationToOPV = None
    self._albedoSolarRadiationToOPV = None
    self._estimatedDirectSolarRadiationToOPVEastDirection = None
    self._estimatedDirectSolarRadiationToOPVWestDirection = None
    self._estimatedDiffuseSolarRadiationToOPV = None
    self._estimatedAlbedoSolarRadiationToOPV = None

    # the following variables are got/set by property
    self._hourlySolarIncidenceAngleEastDirection = None
    self._hourlySolarIncidenceAngleWestDirection = None

    ############## boolean variables ##############
    self._ifGrowForFallowPeriod = False
    # if you want to calculate the estimated data which does not require the measured data, set this variable True.
    self._estimateSolarRadiationMode = False
    self._ifHasShadingCurtain = None

    self._hourlySolarAltitudeAngle = None
    self._hourlySolarAzimuthAngle = None
    self._hourlyModuleAzimuthAngleEast = None
    self._hourlyModuleAzimuthAngleWest = None


  def setOPVAreaCoverageRatio(self, OPVAreaCoverageRatio):
    self._OPVAreaCoverageRatio = OPVAreaCoverageRatio
  def getOPVAreaCoverageRatio(self):
    return self._OPVAreaCoverageRatio

  def setOPVCoverageRatioFallowPeriod(self, OPVCoverageRatioFallowPeriod):
    self._OPVCoverageRatioFallowPeriod = OPVCoverageRatioFallowPeriod
  def getOPVCoverageRatioFallowPeriod(self):
    return self._OPVCoverageRatioFallowPeriod

  def setPlantGrowthModel(self, plantGrowthModel):
    self._plantGrowthModel = plantGrowthModel
  def getPlantGrowthModel(self):
    return self._plantGrowthModel

  def setCultivationDaysperHarvest(self, cultivationDaysperHarvest):
    self._cultivationDaysperHarvest = cultivationDaysperHarvest
  def getCultivationDaysperHarvest(self):
    return self._cultivationDaysperHarvest

  def setHasShadingCurtain(self, hasShadingCurtain):
    self._hasShadingCurtain = hasShadingCurtain
  def getHasShadingCurtain(self):
    return self.hasShadingCurtain

  def setShadingCurtainDeployPPFD(self, shadingCurtainDeployPPFD):
    self._shadingCurtainDeployPPFD = shadingCurtainDeployPPFD
  def getShadingCurtainDeployPPFD(self):
    return self._shadingCurtainDeployPPFD

  def setProfitVSOPVCoverageData(self,profitVSOPVCoverageData):
    self._profitVSOPVCoverageData = profitVSOPVCoverageData
  def getProfitVSOPVCoverageData(self):
    return self._profitVSOPVCoverageData

  def setMonthlyElectricitySalesperArea(self, monthlyElectricitySalesperArea):
    self._monthlyElectricitySalesperArea = monthlyElectricitySalesperArea
  def getMonthlyElectricitySalesperArea(self):
    return self._monthlyElectricitySalesperArea

  def setMonthlyElectricitySalesperAreaEastRoof(self, monthlyElectricitySalesperAreaEastRoof):
    self._monthlyElectricitySalesperAreaEastRoof = monthlyElectricitySalesperAreaEastRoof
  def getMonthlyElectricitySalesperAreaEastRoof(self):
    return self._monthlyElectricitySalesperAreaEastRoof

  def setMonthlyElectricitySalesperAreaWestRoof(self, monthlyElectricitySalesperAreaWestRoof):
    self._monthlyElectricitySalesperAreaWestRoof = monthlyElectricitySalesperAreaWestRoof

  def getMonthlyElectricitySalesperAreaWestRoof(self):
    return self._monthlyElectricitySalesperAreaWestRoof

  def setOPVCostUSDForDepreciationperArea(self, oPVCostUSDForDepreciationperArea):
    self._oPVCostUSDForDepreciationperArea = oPVCostUSDForDepreciationperArea

  def getOPVCostUSDForDepreciationperArea(self):
    return self._oPVCostUSDForDepreciationperArea



  ######################## measured solar radiation to OPV start ########################
  def setDirectSolarRadiationToOPVEastDirection(self, directSolarRadiationToOPVEastDirection):
    self._directSolarRadiationToOPVEastDirection = directSolarRadiationToOPVEastDirection

  def getDirectSolarRadiationToOPVEastDirection(self):
    return self._directSolarRadiationToOPVEastDirection

  def setDirectSolarRadiationToOPVWestDirection(self, directSolarRadiationToOPVWestDirection):
    self._directSolarRadiationToOPVWestDirection = directSolarRadiationToOPVWestDirection

  def getDirectSolarRadiationToOPVWestDirection(self):
    return self._directSolarRadiationToOPVWestDirection

  def setDiffuseSolarRadiationToOPV(self, diffuseSolarRadiationToOPV):
    self._diffuseSolarRadiationToOPV = diffuseSolarRadiationToOPV

  def getDiffuseSolarRadiationToOPV(self):
    return self._diffuseSolarRadiationToOPV

  def setAlbedoSolarRadiationToOPV(self, albedoSolarRadiationToOPV):
    self._albedoSolarRadiationToOPV = albedoSolarRadiationToOPV

  def getAlbedoSolarRadiationToOPV(self):
    return self._albedoSolarRadiationToOPV
  ######################## measured solar radiation to OPV end ########################

  ######################## estimated solar radiation to OPV start ########################
  def setEstimatedDirectSolarRadiationToOPVEastDirection(self, estimatedDirectSolarRadiationToOPVEastDirection):
    self._estimatedDirectSolarRadiationToOPVEastDirection = estimatedDirectSolarRadiationToOPVEastDirection

  def getEstimatedDirectSolarRadiationToOPVEastDirection(self):
    return self._estimatedDirectSolarRadiationToOPVEastDirection

  def setEstimatedDirectSolarRadiationToOPVWestDirection(self, estimatedDirectSolarRadiationToOPVWestDirection):
    self._estimatedDirectSolarRadiationToOPVWestDirection = estimatedDirectSolarRadiationToOPVWestDirection

  def getEstimatedDirectSolarRadiationToOPVWestDirection(self):
    return self._estimatedDirectSolarRadiationToOPVWestDirection

  def setEstimatedDiffuseSolarRadiationToOPV(self, estimatedDiffuseSolarRadiationToOPV):
    self._albedoSolarRadiationToOPV = estimatedDiffuseSolarRadiationToOPV

  def getEstimatedDiffuseSolarRadiationToOPV(self):
    return self._estimatedDiffuseSolarRadiationToOPV

  def setEstimatedAlbedoSolarRadiationToOPV(self, estimatedAlbedoSolarRadiationToOPV):
    self._estimatedAlbedoSolarRadiationToOPV = estimatedAlbedoSolarRadiationToOPV

  def getEstimatedAlbedoSolarRadiationToOPV(self):
    return self._estimatedAlbedoSolarRadiationToOPV
  ######################## estimated solar radiation to OPV end ########################



  def setHourlyInnerLightIntensityPPFDThroughGlazing(self, hourlyInnerLightIntensityPPFDThroughGlazing):
    self._hourlyInnerLightIntensityPPFDThroughGlazing = hourlyInnerLightIntensityPPFDThroughGlazing
  def getHourlyInnerLightIntensityPPFDThroughGlazing(self):
    return self._hourlyInnerLightIntensityPPFDThroughGlazing

  def setHourlyInnerLightIntensityPPFDThroughInnerStructure(self, hourlyInnerLightIntensityPPFDThroughInnerStructure):
    self._hourlyInnerLightIntensityPPFDThroughInnerStructure = hourlyInnerLightIntensityPPFDThroughInnerStructure
  def getHourlyInnerLightIntensityPPFDThroughInnerStructure(self):
    return self._hourlyInnerLightIntensityPPFDThroughInnerStructure

  def setDirectPPFDToOPVEastDirection(self, directPPFDToOPVEastDirection):
    self._directPPFDToOPVEastDirection = directPPFDToOPVEastDirection
  def getDirectPPFDToOPVEastDirection(self):
    return self._directPPFDToOPVEastDirection

  def setDirectPPFDToOPVWestDirection(self, directPPFDToOPVWestDirection):
    self._directPPFDToOPVWestDirection = directPPFDToOPVWestDirection
  def getDirectPPFDToOPVWestDirection(self):
    return self._directPPFDToOPVWestDirection

  def setDiffusePPFDToOPV(self, diffusePPFDToOPV):
    self._diffusePPFDToOPV = diffusePPFDToOPV
  def getDiffusePPFDToOPV(self):
    return self._diffusePPFDToOPV

  def setGroundReflectedPPFDToOPV(self, groundReflectedPPFDToOPV):
    self._groundReflectedPPFDToOPV = groundReflectedPPFDToOPV
  def getGroundReflectedPPFDToOPV(self):
    return self._groundReflectedPPFDToOPV

  def setTotalDLItoPlantsBaselineShadingCuratin(self, totalDLItoPlantsBaselineShadingCuratin):
    self._totalDLItoPlantsBaselineShadingCuratin = totalDLItoPlantsBaselineShadingCuratin
  def getTotalDLItoPlantsBaselineShadingCuratin(self):
    return self._totalDLItoPlantsBaselineShadingCuratin

  def setDirectDLIToOPVEastDirection(self, directDLIToOPVEastDirection):
    self._directDLIToOPVEastDirection = directDLIToOPVEastDirection
  def getDirectDLIToOPVEastDirection(self):
    return self._directDLIToOPVEastDirection

  def setDirectDLIToOPVWestDirection(self, directDLIToOPVWestDirection):
    self._directDLIToOPVWestDirection = directDLIToOPVWestDirection
  def getDirectDLIToOPVWestDirection(self):
    return self._directDLIToOPVWestDirection

  def setDiffuseDLIToOPV(self, diffuseDLIToOPV):
    self._diffuseDLIToOPV = diffuseDLIToOPV
  def getDiffuseDLIToOPV(self):
    return self._diffuseDLIToOPV

  def setGroundReflectedDLIToOPV(self, groundReflectedDLIToOPV):
    self._groundReflectedDLIToOPV = groundReflectedDLIToOPV
  def getGroundReflectedDLIToOPV(self):
    return self._groundReflectedDLIToOPV


  ##############################solar irradiance to multi span roof start##############################
  def setHourlyDirectSolarRadiationToMultiSpanRoof(self, hourlyDirectSolarRadiationToMultiSpanRoof):
    self._hourlyDirectSolarRadiationToMultiSpanRoof = hourlyDirectSolarRadiationToMultiSpanRoof
  def getHourlyDirectSolarRadiationToMultiSpanRoof(self):
    return self._hourlyDirectSolarRadiationToMultiSpanRoof

  def setHourlyDiffuseSolarRadiationToMultiSpanRoof(self, hourlyDiffuseSolarRadiationToMultiSpanRoof):
    self._hourlyDiffuseSolarRadiationToMultiSpanRoof = hourlyDiffuseSolarRadiationToMultiSpanRoof
  def getHourlyDiffuseSolarRadiationToMultiSpanRoof(self):
    return self._hourlyDiffuseSolarRadiationToMultiSpanRoof

  def setGroundReflectedRadiationToMultiSpanRoof(self, groundReflectedRadiationToMultiSpanRoof):
    self._groundReflectedRadiationToMultiSpanRoof = groundReflectedRadiationToMultiSpanRoof
  def getGroundReflectedRadiationToMultiSpanRoof(self):
    return self._groundReflectedRadiationToMultiSpanRoof

  def setHourlyDirectPPFDToMultiSpanRoof(self, hourlyDirectPPFDToMultiSpanRoof):
    self._hourlyDirectPPFDToMultiSpanRoof = hourlyDirectPPFDToMultiSpanRoof
  def getHourlyDirectPPFDToMultiSpanRoof(self):
    return self._hourlyDirectPPFDToMultiSpanRoof

  def setHourlyDiffusePPFDToMultiSpanRoof(self, hourlyDiffusePPFDToMultiSpanRoof):
    self._hourlyDiffusePPFDToMultiSpanRoof = hourlyDiffusePPFDToMultiSpanRoof
  def getHourlyDiffusePPFDToMultiSpanRoof(self):
    return self._hourlyDiffusePPFDToMultiSpanRoof

  def setGroundReflectedPPFDToMultiSpanRoof(self, groundReflectedPPFDToMultiSpanRoof):
    self._groundReflectedPPFDToMultiSpanRoof = groundReflectedPPFDToMultiSpanRoof
  def getGroundReflectedPPFDToMultiSpanRoof(self):
    return self._groundReflectedPPFDToMultiSpanRoof
  ##############################solar irradiance to multi span roof end##############################

  def setShootFreshMassList(self, shootFreshMassList):
    self._shootFreshMassList = shootFreshMassList
  def getShootFreshMassList(self):
    return self._shootFreshMassList

  def setUnitDailyFreshWeightIncrease(self, setUnitDailyFreshWeightIncrease):
    self._unitDailyFreshWeightIncrease = setUnitDailyFreshWeightIncrease
  def getUnitDailyFreshWeightIncrease(self):
    return self._unitDailyFreshWeightIncrease

  def setAccumulatedUnitDailyFreshWeightIncrease(self, accumulatedUnitDailyFreshWeightIncrease):
    self._accumulatedUnitDailyFreshWeightIncrease = accumulatedUnitDailyFreshWeightIncrease
  def getAccumulatedUnitDailyFreshWeightIncrease(self):
    return self._accumulatedUnitDailyFreshWeightIncrease

  def setUnitDailyHarvestedFreshWeight(self, unitDailyHarvestedFreshWeight):
    self._unitDailyHarvestedFreshWeight = unitDailyHarvestedFreshWeight
  def getUnitDailyHarvestedFreshWeight(self):
    return self._unitDailyHarvestedFreshWeight

  def setAverageDLIonEachCycle(self, averageDLIonEachCycle):
    self._averageDLIonEachCycle = averageDLIonEachCycle
  def getAverageDLIonEachCycle(self):
    return self._averageDLIonEachCycle

  def setYear(self, year):
    self._year = year
  def getYear(self):
    return self._year

  def setMonth(self, month):
    self._month = month
  def getMonth(self):
    return self._month

  def setDay(self, day):
    self._day = day
  def getDay(self):
    return self._day

  def setHour(self, hour):
    self._hour = hour
  def getHour(self):
    return self._hour

  ######################### imported data start #########################
  def setImportedHourlyHorizontalDirectSolarRadiation(self, importedHourlyHorizontalDirectSolarRadiation):
    self._importedHourlyHorizontalDirectSolarRadiation = importedHourlyHorizontalDirectSolarRadiation
  def getImportedHourlyHorizontalDirectSolarRadiation(self):
    return self._importedHourlyHorizontalDirectSolarRadiation

  def setImportedHourlyHorizontalDiffuseSolarRadiation(self, importedHourlyHorizontalDiffuseSolarRadiation):
    self._importedHourlyHorizontalDiffuseSolarRadiation = importedHourlyHorizontalDiffuseSolarRadiation
  def getImportedHourlyHorizontalDiffuseSolarRadiation(self):
    return self._importedHourlyHorizontalDiffuseSolarRadiation

  def setImportedHourlyHorizontalTotalBeamMeterBodyTemperature(self, importedHourlyHorizontalTotalBeamMeterBodyTemperature):
    self._importedHourlyHorizontalTotalBeamMeterBodyTemperature = importedHourlyHorizontalTotalBeamMeterBodyTemperature
  def getImportedHourlyHorizontalTotalBeamMeterBodyTemperature(self):
    return self._importedHourlyHorizontalTotalBeamMeterBodyTemperature

  def setImportedHourlyAirTemperature(self, importedHourlyAirTemperature):
    self._importedHourlyAirTemperature = importedHourlyAirTemperature
  def getImportedHourlyAirTemperature(self):
    return self._importedHourlyAirTemperature
  ######################### imported data end #########################


  def setIfGrowForFallowPeriod(self, ifGrowForFallowPeriod):
    self._ifGrowForFallowPeriod = ifGrowForFallowPeriod
  def getIfGrowForFallowPeriod(self):
    return self._ifGrowForFallowPeriod

  def setEstimateSolarRadiationMode(self, estimateSolarRadiationMode):
    self._estimateSolarRadiationMode = estimateSolarRadiationMode

  def getEstimateSolarRadiationMode(self):
    return self._estimateSolarRadiationMode

  def setIfHasShadingCurtain(self, ifHasShadingCurtain):
    self._ifHasShadingCurtain = ifHasShadingCurtain

  def getIfHasShadingCurtain(self):
    return self._ifHasShadingCurtain

  @property
  def hourlySolarIncidenceAngleEastDirection(self):
    return self._hourlySolarIncidenceAngleEastDirection

  @hourlySolarIncidenceAngleEastDirection.setter
  def hourlySolarIncidenceAngleEastDirection(self, hourlySolarIncidenceAngleEastDirection):
    self._hourlySolarIncidenceAngleEastDirection = hourlySolarIncidenceAngleEastDirection

  @property
  def hourlySolarIncidenceAngleWestDirection(self):
    return self._hourlySolarIncidenceAngleWestDirection

  @hourlySolarIncidenceAngleWestDirection.setter
  def hourlySolarIncidenceAngleWestDirection(self, hourlySolarIncidenceAngleWestDirection):
    self._hourlySolarIncidenceAngleWestDirection = hourlySolarIncidenceAngleWestDirection

  @property
  def hourlySolarAltitudeAngle(self):
    return self._hourlySolarAltitudeAngle

  @hourlySolarAltitudeAngle.setter
  def hourlySolarAltitudeAngle(self, hourlySolarAltitudeAngle):
    self._hourlySolarAltitudeAngle = hourlySolarAltitudeAngle


  @property
  def hourlySolarAzimuthAngle(self):
    return self._hourlySolarAzimuthAngle

  @hourlySolarAzimuthAngle.setter
  def hourlySolarAzimuthAngle(self, hourlySolarAzimuthAngle):
    self._hourlySolarAzimuthAngle = hourlySolarAzimuthAngle


  @property
  def hourlyModuleAzimuthAngleEast(self):
    return self._hourlyModuleAzimuthAngleEast

  @hourlyModuleAzimuthAngleEast.setter
  def hourlyModuleAzimuthAngleEast(self, hourlyModuleAzimuthAngleEast):
    self._hourlyModuleAzimuthAngleEast = hourlyModuleAzimuthAngleEast


  @property
  def hourlyModuleAzimuthAngleWest(self):
    return self._hourlyModuleAzimuthAngleWest

  @hourlyModuleAzimuthAngleWest.setter
  def hourlyModuleAzimuthAngleWest(self, hourlyModuleAzimuthAngleWest):
    self._hourlyModuleAzimuthAngleWest = hourlyModuleAzimuthAngleWest
