# -*- coding: utf-8 -*-

##########import package files##########
from scipy import stats
import sys
import datetime
import os as os
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulatorConstant as constant
import Util as util
#######################################################

def getDirectSolarIrradianceThroughMultiSpanRoof(simulatorClass):
    """

    :param simulatorClass:
    :return:
    """
    1==1

def getAngleBetweenIncientRayAndHorizontalAxisPerpendicularToGHSpan(simulatorClass, hourlyModuleAzimuthAngle):
    # alpha: solar altitude angle
    alpha = simulatorClass.hourlySolarAltitudeAngle
    hourlySolarAzimuthAngle = simulatorClass.hourlySolarAzimuthAngle

    E = np.arcsin( np.sin(alpha) / np.sqrt(np.sin(alpha)**2 + np.cos(alpha)*np.cos(hourlyModuleAzimuthAngle - hourlySolarAzimuthAngle)**2))
    # By definition, E wants to take more than pi/2 [rad] when the sun moves from east to west, which occurs at noon.
    E = np.array([math.pi - E[i] if i!=0 and E[i] > 0.0 and E[i]-E[i-1] < 0.0 else E[i] for i in range (0, E.shape[0])])

    return E

def getAngleBetweenIncientRayAndHorizontalAxisParallelToGHSpan(simulatorClass, hourlyModuleAzimuthAngle):
    # alpha: solar altitude angle
    alpha = simulatorClass.hourlySolarAltitudeAngle
    hourlySolarAzimuthAngle = simulatorClass.hourlySolarAzimuthAngle

    EParallel = np.arcsin( np.sin(alpha) / np.sqrt(np.sin(alpha)**2 + np.cos(alpha)*np.sin(hourlyModuleAzimuthAngle - hourlySolarAzimuthAngle)**2))

    return EParallel






