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


def getAngleBetweenIncientRayAndHorizontalAxisPerpendicularToGHSpan(simulatorClass, hourlyModuleAzimuthAngle):
    # alpha: solar altitude angle
    alpha = simulatorClass.hourlySolarAltitudeAngle
    hourlySolarAzimuthAngle = simulatorClass.hourlySolarAzimuthAngle

    E = np.arcsin( np.sin(alpha) / np.sqrt(np.sin(alpha)**2 + np.cos(alpha)*np.cos(hourlyModuleAzimuthAngle - hourlySolarAzimuthAngle)**2))
    # It was interpreted that the reference of the model Soriano et al., 2004,"A Study of Direct Solar Radiation transmittance in Asymmetrical Multi-span Greenhouses using Scale Models and Simulation Models"
    # need the angle E be expressed less than pi/2, when the solar position changes from east to east side in the sky passing meridian

    # By definition, E wants to take more than pi/2 [rad] when the sun moves from east to west, which occurs at noon.
    E = np.array([math.pi - E[i] if i!=0 and E[i] > 0.0 and E[i]-E[i-1] < 0.0 else E[i] for i in range (0, E.shape[0])])

    return E

def getAngleBetweenIncientRayAndHorizontalAxisParallelToGHSpan(simulatorClass, hourlyModuleAzimuthAngle):
    # alpha: solar altitude angle
    alpha = simulatorClass.hourlySolarAltitudeAngle
    hourlySolarAzimuthAngle = simulatorClass.hourlySolarAzimuthAngle

    EParallel = np.arcsin( np.sin(alpha) / np.sqrt(np.sin(alpha)**2 + np.cos(alpha)*np.sin(hourlyModuleAzimuthAngle - hourlySolarAzimuthAngle)**2))

    return EParallel


def getTransmittanceForPerpendicularIrrThroughMultiSpanRoofFacingEastOrNorth(simulatorClass, directSolarRadiationToOPVEastDirection, \
                                                                  EPerpendicularEastOrNorthFacingRoof):
    """

    :param simulatorClass:
    :return:
    """
    alpha = constant.roofAngleWestOrSouth
    beta = constant.roofAngleEastOrNorth
    L_1 = constant.greenhouseRoofWidthWestOrSouth
    L_2 = constant.greenhouseRoofWidthEastOrNorth

    # the transmittance of roof surfaces 1 (facing west or south)
    T_1 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    # the transmittance of roof surfaces 2 (facing east or north)
    T_2 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    # the reflectance of roof surfaces 1 (facing west or south)
    F_1 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    # the reflectance of roof surfaces 2 (facing west or south)
    F_2 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])

    # the transmittance/reflectance of solar irradiance directly transmitted to the soil through roof each direction of roof (surfaces east and west) (A10)
    T_12 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    # the transmittance/reflectance on the roof facing west of solar irradiance reflected by the surface facing west and transmitted to the soil (surfaces west or south)
    T_r11 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    F_r11 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    # the transmittance/reflectance on the roof facing east of solar irradiance reflected by the surface facing west and transmitted to the soil (surfaces east or north)
    T_r12 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    F_r12 = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])

    # transmittance through multispan roof
    T_matPerpendicular = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])
    # T_matParallel = np.zeros(directSolarRadiationToOPVEastDirection.shape[0])

    ##############################################################################################################################
    # calculate the transmittance of perpendicular direction from the EAST facing roof after penetrating multi-span roof per hour
    ##############################################################################################################################
    for i in range(0, directSolarRadiationToOPVEastDirection.shape[0]):

        # print("i:{}".format(i))
        # print("EPerpendicularEastOrNorthFacingRoof[i]:{}".format(EPerpendicularEastOrNorthFacingRoof[i]))
        # print("directSolarRadiationToOPVEastDirection[i]:{}".format(directSolarRadiationToOPVEastDirection[i]))

        # if the solar irradiance at a certain time is zero, then skip the element
        if directSolarRadiationToOPVEastDirection[i] == 0.0: continue

        # case A1: if the roof-slope angle of the west side is greater than the angle E formed by the incident ray with the horizontal axis perpendicular to the greenhouse span
        # It was assumed the direct solar radiation is 0 when math.pi - alpha <= EPerpendicularEastOrNorthFacingRoof[i]:
        elif EPerpendicularEastOrNorthFacingRoof[i] <= alpha:
            # print ("call case A1")

            # the number of intercepting spans, which can very depending on E.
            m = int(1.0 / 2.0 * (1 + math.tan(alpha) / math.tan(EPerpendicularEastOrNorthFacingRoof[i])))
            # print("m:{}".format(m))

            # fraction (percentage) of light which does not pass through the first span [-]
            l_a = m * L_1 * math.sin(alpha + EPerpendicularEastOrNorthFacingRoof[i]) - (m + 1) * L_2 * math.sin(beta - EPerpendicularEastOrNorthFacingRoof[i])
            # fraction (percentage) of light which crosses the first span before continuing on towards the others [-]
            l_b = m * L_2 * math.sin(beta - EPerpendicularEastOrNorthFacingRoof[i]) - (m - 1) * L_1 * math.sin(alpha + EPerpendicularEastOrNorthFacingRoof[i])
            # print("l_a at case A1:{}".format(l_a))
            # print("l_b at case A1:{}".format(l_b))

            # claculate the incidence angle for each facing roof
            incidentAngleForEastOrNorthRoof = getIncidentAngleForEastOrNorthRoof(EPerpendicularEastOrNorthFacingRoof[i], beta)
            incidentAngleForWestOrSouthhRoof = getIncidentAngleForWestOrSouthRoof(EPerpendicularEastOrNorthFacingRoof[i], alpha)
            # print("incidentAngleForEastOrNorthRoof at case A1:{}".format(incidentAngleForEastOrNorthRoof))
            # print("incidentAngleForWestOrSouthhRoof at case A1:{}".format(incidentAngleForWestOrSouthhRoof))

            # calculate the transmittance and reflectance to each roof
            T_2[i], F_2[i] = fresnelEquation(incidentAngleForEastOrNorthRoof)
            T_1[i], F_1[i] = fresnelEquation(incidentAngleForWestOrSouthhRoof)
            # print("T_1[i]:{}, T_2[i]:{}, F_1[i]:{}, F_2[i]:{}".format(T_1[i], T_2[i], F_1[i], F_2[i]))

            T_matPerpendicular[i] = getTransmittanceThroughMultiSpanCoveringCaseA1ForEastOrNorthFacingRoof(l_a, l_b, m, T_1[i], F_1[i], T_2[i], F_2[i])
            # print("T_matPerpendicular[i]:{}".format(T_matPerpendicular[i]))

        # case A2.1: if the angle E is greater than the roof angle of the north side beta (beta < E < 2*beta)
        elif (alpha < EPerpendicularEastOrNorthFacingRoof[i] and EPerpendicularEastOrNorthFacingRoof[i] < 2.0*alpha) or \
            (math.pi - 2.0*alpha < EPerpendicularEastOrNorthFacingRoof[i] and EPerpendicularEastOrNorthFacingRoof[i] < math.pi - alpha):
            # print ("call case A2.1")
            l_1, l_2, T_1[i], F_1[i], T_2[i], F_2[i], T_12[i] = getSolarIrradianceDirectlhyTransmittedToPlants(\
                                                                    alpha, beta, L_1, L_2, EPerpendicularEastOrNorthFacingRoof[i])

            # get the angle E reflected from the west or south facing roof and transmit through multi-span roofs
            reflectedE = getReflectedE(EPerpendicularEastOrNorthFacingRoof[i], alpha)
            # get the incidence angle for each facing roof
            incidentAngleOfReflectedLightForEastOrNorthRoof = getIncidentAngleForEastOrNorthRoof(reflectedE, beta)
            incidentAngleOfReflectedLightForWestOrSouthRoof = getIncidentAngleForWestOrSouthRoof(reflectedE, alpha)

            # get the Transmittance and reflection on each roof from the reflected irradiance
            T_r12[i], F_r12[i] = fresnelEquation(incidentAngleOfReflectedLightForEastOrNorthRoof)
            T_r11[i], F_r11[i] = fresnelEquation(incidentAngleOfReflectedLightForWestOrSouthRoof)

            # the number of intercepting spans, which can very depending on E.
            x = abs(2.0 * alpha - EPerpendicularEastOrNorthFacingRoof[i])
            m = int(1.0 / 2.0 * (1 + math.tan(alpha) / math.tan(x)))
            # print("x:{}, 1 + math.tan(alpha) / math.tan(x):{}".format(x, 1 + math.tan(alpha) / math.tan(x)))


            # l_a: fraction (percentage) of reflected light which does not pass through the first span [-], equation (A14)
            # l_b: fraction (percentage) of reflected light which crosses the first span before continuing on towards the others [-], equation (A15)
            l_a, l_b = getFractionOfTransmittanceOfReflectedSolarIrradiance(alpha, beta, L_1, L_2, m, EPerpendicularEastOrNorthFacingRoof[i])

            T_matPerpendicular[i] = getTransmittanceOfReflectedLightThroughMultiSpanCoveringCaseA2_1ForEastOrNorthFacingRoof(l_a, l_b, m, T_r11[i], T_r12[i], F_r11[i], F_r12[i], F_1[i], l_1, l_2) +\
                                                + T_12[i]
            # print("T_matPerpendicular[i]:{}".format(T_matPerpendicular[i]))

        # case A2.2: if the angle E is greater than the roof angle of the north side beta (2*beta < E < 3*beta)
        elif (2.0*alpha < EPerpendicularEastOrNorthFacingRoof[i] and EPerpendicularEastOrNorthFacingRoof[i] < 3.0*alpha) or \
            (math.pi - 3.0 * alpha < EPerpendicularEastOrNorthFacingRoof[i] and EPerpendicularEastOrNorthFacingRoof[i] < math.pi - 2.0 * alpha):
            # print ("call case A2.2")

            l_1, l_2, T_1[i], F_1[i], T_2[i], F_2[i], T_12[i] = getSolarIrradianceDirectlhyTransmittedToPlants(\
                                                                    alpha, beta, L_1, L_2, EPerpendicularEastOrNorthFacingRoof[i])

            # get the angle E reflected from the west or south facing roof and transmit through multi-span roofs
            reflectedE = getReflectedE(EPerpendicularEastOrNorthFacingRoof[i], alpha)
            # get the incidence angle for each facing roof
            incidentAngleOfReflectedLightForEastOrNorthRoof = getIncidentAngleForEastOrNorthRoof(reflectedE, beta)
            incidentAngleOfReflectedLightForWestOrSouthRoof = getIncidentAngleForWestOrSouthRoof(reflectedE, alpha)

            # get the Transmittance and reflection on each roof from the reflected irradiance
            T_r12[i], F_r12[i] = fresnelEquation(incidentAngleOfReflectedLightForEastOrNorthRoof)
            T_r11[i], F_r11[i] = fresnelEquation(incidentAngleOfReflectedLightForWestOrSouthRoof)

            # the number of intercepting spans, which can very depending on E.
            x = abs(2.0 * alpha - EPerpendicularEastOrNorthFacingRoof[i])
            m = int(1.0 / 2.0 * (1 + math.tan(alpha) / math.tan(x)))

            # l_a: fraction (percentage) of reflected light which does not pass through the first span [-], equation (A14)
            # l_b: fraction (percentage) of reflected light which crosses the first span before continuing on towards the others [-], equation (A15)
            l_a, l_b = getFractionOfTransmittanceOfReflectedSolarIrradiance(alpha, beta, L_1, L_2, m, EPerpendicularEastOrNorthFacingRoof[i])

            T_matPerpendicular[i] = getTransmittanceOfReflectedLightThroughMultiSpanCoveringCaseA2_1ForEastOrNorthFacingRoof(l_a, l_b, m, T_r11[i], T_r12[i], F_r11[i], F_r12[i], F_1[i], l_1, l_2) \
                                                + T_12[i]
            # print("T_matPerpendicular[i]:{}".format(T_matPerpendicular[i]))

        # case A2.3: if 3.0 * alpha < EPerpendicularEastOrNorthFacingRoof[i]
        # since this model assumes north-south direction greenhouse, the E can be more than pi/2.0, and thus the following range was set
        elif 3.0 * alpha < EPerpendicularEastOrNorthFacingRoof[i] and EPerpendicularEastOrNorthFacingRoof[i] < (math.pi - 3.0 * alpha):
            # print ("call case A2.3")
            _, _, _, _, _, _, T_12[i] = getSolarIrradianceDirectlhyTransmittedToPlants(alpha, beta, L_1, L_2, EPerpendicularEastOrNorthFacingRoof[i])
            T_matPerpendicular[i] = T_12[i]
            # print("T_matPerpendicular[i]:{}".format(T_matPerpendicular[i]))

    # print("T_1 :{}".format(T_1))
    # print("F_1 :{}".format(F_1))
    # print("T_2 :{}".format(T_2))
    # print("F_2 :{}".format(F_2))
    # print("T_12 :{}".format(T_12))
    # print("T_r11 :{}".format(T_r11))
    # print("F_r11 :{}".format(F_r11))
    # print("T_r12 :{}".format(T_r12))
    # print("F_r12 :{}".format(F_r12))
    # print("T_matPerpendicular :{}.format(T_matPerpendicular))

    return T_matPerpendicular

def getTransmittanceForPerpendicularIrrThroughMultiSpanRoofFacingWestOrSouth(simulatorClass, directSolarRadiationToOPVWestDirection, \
                                                                  EPerpendicularWestOrSouthFacingRoof):
    """
    :return:
    """
    alpha = constant.roofAngleWestOrSouth
    beta = constant.roofAngleEastOrNorth
    L_1 = constant.greenhouseRoofWidthWestOrSouth
    L_2 = constant.greenhouseRoofWidthEastOrNorth

    # the Transmittances of roof surfaces 1 (facing west or south)
    T_1 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])
    # the Transmittances of roof surfaces 2 (facing east or north)
    T_2 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])
    # the reflectance of roof surfaces 1 (facing west or south)
    F_1 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])
    # the reflectance of roof surfaces 2 (facing west or south)
    F_2 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])

    # the transmittance/reflectance of solar irradiance directly transmitted to the soil through roof each direction of roof (surfaces east and west) (A10)
    T_12 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])

    # the transmittance/reflectance on the roof facing west of solar irradiance reflected by the surface facing east and transmitted to the soil (surfaces west or south)
    T_r21 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])
    F_r21 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])
    # the transmittance/reflectance on the roof facing east of solar irradiance reflected by the surface facing east and transmitted to the soil (surfaces east or north)
    T_r22 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])
    F_r22 = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])

    # transmittance through multispan roof
    T_matPerpendicular = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])
    # T_matParallel = np.zeros(directSolarRadiationToOPVWestDirection.shape[0])


    # calculate the solar irradiacne from the EAST facing roof after penetrating multi-span roof per hour
    for i in range(0, directSolarRadiationToOPVWestDirection.shape[0]):
        # print("i:{}".format(i))
        # print("EPerpendicularWestOrSouthFacingRoof[i]:{}".format(EPerpendicularWestOrSouthFacingRoof[i]))
        # print("directSolarRadiationToOPVWestDirection[i]:{}".format(directSolarRadiationToOPVWestDirection[i]))

        # if the solar irradiance at a certain time is zero, then skip the element
        if directSolarRadiationToOPVWestDirection[i] == 0.0: continue

        # case A1: if the roof-slope angle of the west side is greater than the angle E formed by the incident ray with the horizontal axis perpendicular to the greenhouse span
        # It was assumed the direct solar radiation is 0 when EPerpendicularWestOrSouthFacingRoof[i] <= alpha
        # elif EPerpendicularWestOrSouthFacingRoof[i] <= alpha or  math.pi - alpha <= EPerpendicularWestOrSouthFacingRoof[i]:
        elif math.pi - alpha <= EPerpendicularWestOrSouthFacingRoof[i]:
            # print ("call case A1")

            # since the original model does not suppose EPerpendicular is more than pi/2 (the cause it assume the angle of the greenhouse is east-west, not north-south where the sun croees the greenhouse)
            # EPerpendicular is converted into pi -  EPerpendicular when it is more than pi/2
            if EPerpendicularWestOrSouthFacingRoof[i] > math.pi/2.0:
                EPerpendicularWestOrSouthFacingRoof[i] = math.pi - EPerpendicularWestOrSouthFacingRoof[i]

            # print("EPerpendicularWestOrSouthFacingRoof_CaseA1[i]:{}".format(EPerpendicularWestOrSouthFacingRoof[i]))
            # the number of intercepting spans, which can very depending on E.
            m = int(1.0 / 2.0 * (1 + math.tan(alpha) / math.tan(EPerpendicularWestOrSouthFacingRoof[i])))
            # print("m:{}".format(m))

            # fraction (percentage) of light which does not pass through the first span [-]
            l_a = m * L_1 * math.sin(alpha + EPerpendicularWestOrSouthFacingRoof[i]) - (m + 1) * L_2 * math.sin(beta - EPerpendicularWestOrSouthFacingRoof[i])
            # fraction (percentage) of light which crosses the first span before continuing on towards the others [-]
            l_b = m * L_2 * math.sin(beta - EPerpendicularWestOrSouthFacingRoof[i]) - (m - 1) * L_1 * math.sin(alpha + EPerpendicularWestOrSouthFacingRoof[i])
            # print("l_a at case A1:{}".format(l_a))
            # print("l_b at case A1:{}".format(l_b))

            # the following functions works to if you do not rollback EPerpendicularWestOrSouthFacingRoof
            # claculate the incidence angle for each facing roof
            incidentAngleForEastOrNorthRoof = getIncidentAngleForEastOrNorthRoofWithBeamComingFromWestOrSouth(EPerpendicularWestOrSouthFacingRoof[i], beta)
            incidentAngleForWestOrSouthRoof = getIncidentAngleForWestOrSouthRoofWithBeamComingFromWestOrSouth(EPerpendicularWestOrSouthFacingRoof[i], alpha)
            # print("incidentAngleForEastOrNorthRoof at case A1:{}".format(incidentAngleForEastOrNorthRoof))
            # print("incidentAngleForWestOrSouthRoof at case A1:{}".format(incidentAngleForWestOrSouthRoof))

            # calculate the transmittance and reflectance to each roof
            T_2[i], F_2[i] = fresnelEquation(incidentAngleForEastOrNorthRoof)
            T_1[i], F_1[i] = fresnelEquation(incidentAngleForWestOrSouthRoof)
            # print("T_1[i]:{}, T_2[i]:{}, F_1[i]:{}, F_2[i]:{}".format(T_1[i], T_2[i], F_1[i], F_2[i]))

            T_matPerpendicular[i] = getTransmittanceThroughMultiSpanCoveringCaseA1ForWestOrSouthFacingRoof(l_a, l_b, m, T_1[i], F_1[i], T_2[i], F_2[i])
            # print("T_matPerpendicular[i]:{}".format(T_matPerpendicular[i]))

        # case A2.1: if the angle E is greater than the roof angle of the north side beta (beta < E < 2*beta)
        elif (alpha < EPerpendicularWestOrSouthFacingRoof[i] and EPerpendicularWestOrSouthFacingRoof[i] < 2.0*alpha) or \
            (math.pi - 2.0 * alpha < EPerpendicularWestOrSouthFacingRoof[i] and EPerpendicularWestOrSouthFacingRoof[i] < math.pi - alpha):
            # print ("call case A2.1")

            l_1, l_2, T_1[i], F_1[i], T_2[i], F_2[i], T_12[i] = getSolarIrradianceDirectlhyTransmittedToPlants(\
                                                                    alpha, beta, L_1, L_2, EPerpendicularWestOrSouthFacingRoof[i])

            # get the angle E reflected from the west or south facing roof and transmit through multi-span roofs
            reflectedE = getReflectedE(EPerpendicularWestOrSouthFacingRoof[i], alpha)
            # get the incidence angle for each facing roof
            incidentAngleOfReflectedLightForEastOrNorthRoof = getIncidentAngleForEastOrNorthRoof(reflectedE, beta)
            incidentAngleOfReflectedLightForWestOrSouthRoof = getIncidentAngleForWestOrSouthRoof(reflectedE, alpha)

            # get the Transmittance and reflection on each roof from the reflected irradiance
            T_r22[i], F_r22[i] = fresnelEquation(incidentAngleOfReflectedLightForEastOrNorthRoof)
            T_r21[i], F_r21[i] = fresnelEquation(incidentAngleOfReflectedLightForWestOrSouthRoof)

            # the number of intercepting spans, which can very depending on E.
            x = abs(2.0 * alpha - EPerpendicularWestOrSouthFacingRoof[i])
            m = int(1.0 / 2.0 * (1 + math.tan(alpha) / math.tan(x)))
            # print("x:{}, 1 + math.tan(alpha) / math.tan(x):{}".format(x, 1 + math.tan(alpha) / math.tan(x)))

            # l_a: fraction (percentage) of reflected light which does not pass through the first span [-], equation (A14)
            # l_b: fraction (percentage) of reflected light which crosses the first span before continuing on towards the others [-], equation (A15)
            l_a, l_b = getFractionOfTransmittanceOfReflectedSolarIrradiance(alpha, beta, L_1, L_2, m, EPerpendicularWestOrSouthFacingRoof[i])
            # print("l_a:{}, l_b:{}".format(l_a, l_b))

            # # fraction (percentage) of light which does not pass through the first span [-], equation (A14)
            # l_a = L_2 * m * math.sin(EPerpendicularWestOrSouthFacingRoof[i] - beta) - L_1 * (m - 1) * math.sin(alpha + 2.0 * beta - EPerpendicularWestOrSouthFacingRoof[i])
            # # fraction (percentage) of light which crosses the first span before continuing on towards the others [-], equation (A15)
            # l_b = L_1 * math.sin(alpha + 2.0 * beta - EPerpendicularWestOrSouthFacingRoof[i]) - L_2 * math.sin(EPerpendicularWestOrSouthFacingRoof[i] - beta)

            T_matPerpendicular[i] = getTransmittanceOfReflectedLightThroughMultiSpanCoveringCaseA2_1ForWestOrSouthFacingRoof(l_a, l_b, m, T_r21[i], T_r22[i], F_r21[i], F_r22[i], F_1[i], l_1, l_2)\
                                                + T_12[i]
            # print("T_matPerpendicular[i]:{}".format(T_matPerpendicular[i]))

        # case A2.2: if the angle E is greater than the roof angle of the north side beta (2*beta < E < 3*beta)
        elif (2.0*alpha < EPerpendicularWestOrSouthFacingRoof[i] and EPerpendicularWestOrSouthFacingRoof[i] < 3.0*alpha) or \
            (math.pi - 3.0 * alpha < EPerpendicularWestOrSouthFacingRoof[i] and EPerpendicularWestOrSouthFacingRoof[i] < math.pi - 2.0 * alpha):
            # print ("call case A2.2")

            l_1, l_2, T_1[i], F_1[i], T_2[i], F_2[i], T_12[i] = getSolarIrradianceDirectlhyTransmittedToPlants(\
                                                                    alpha, beta, L_1, L_2, EPerpendicularWestOrSouthFacingRoof[i])

            # get the angle E reflected from the west or south facing roof and transmit through multi-span roofs
            reflectedE = getReflectedE(EPerpendicularWestOrSouthFacingRoof[i], alpha)
            # get the incidence angle for each facing roof
            incidentAngleOfReflectedLightForEastOrNorthRoof = getIncidentAngleForEastOrNorthRoof(reflectedE, beta)
            incidentAngleOfReflectedLightForWestOrSouthRoof = getIncidentAngleForWestOrSouthRoof(reflectedE, alpha)

            # get the Transmittance and reflection on each roof from the reflected irradiance
            T_r22[i], F_r22[i] = fresnelEquation(incidentAngleOfReflectedLightForEastOrNorthRoof)
            T_r21[i], F_r21[i] = fresnelEquation(incidentAngleOfReflectedLightForWestOrSouthRoof)

            # the number of intercepting spans, which can very depending on E.
            x = abs(2.0 * alpha - EPerpendicularWestOrSouthFacingRoof[i])
            m = int(1.0 / 2.0 * (1 + math.tan(alpha) / math.tan(x)))
            # print("x:{}, 1 + math.tan(alpha) / math.tan(x):{}".format(x, 1 + math.tan(alpha) / math.tan(x)))

            # fraction (percentage) of light which does not pass through the first span [-], equation (A16)
            l_a = L_2 * (1-m) * math.sin(EPerpendicularWestOrSouthFacingRoof[i] - beta) + L_1 * m * math.sin(alpha + 2.0 * beta - EPerpendicularWestOrSouthFacingRoof[i])
            # fraction (percentage) of light which crosses the first span before continuing on towards the others [-], equation (A17)
            l_b = L_2 * math.sin(EPerpendicularWestOrSouthFacingRoof[i] - beta) - L_1 * math.sin(alpha + 2.0 * beta - EPerpendicularWestOrSouthFacingRoof[i])
            # print("l_a:{}, l_b:{}".format(l_a, l_b))

            T_matPerpendicular[i] = getTransmittanceOfReflectedLightThroughMultiSpanCoveringCaseA2_1ForWestOrSouthFacingRoof(l_a, l_b, m, T_r21[i], T_r22[i], F_r21[i], F_r22[i], F_1[i], l_1, l_2) \
                                                + T_12[i]
            # print("T_matPerpendicular[i]:{}".format(T_matPerpendicular[i]))

        # case A2.3: if 3.0 * alpha < EPerpendicularEastOrNorthFacingRoof[i]
        # since this model assumes north-south direction greenhouse, the E can be more than pi/2.0, and thus the following range was set
        elif (3.0*alpha < EPerpendicularWestOrSouthFacingRoof[i] and EPerpendicularWestOrSouthFacingRoof[i] < (math.pi - 3.0*alpha)):
            # print ("call case A2.3")
            _, _, _, _, _, _, T_12[i] = getSolarIrradianceDirectlhyTransmittedToPlants(alpha, beta, L_1, L_2, EPerpendicularWestOrSouthFacingRoof[i])
            T_matPerpendicular[i] = T_12[i]

    # print("T_1 :{}".format(T_1))
    # print("F_1 :{}".format(F_1))
    # print("T_2 :{}".format(T_2))
    # print("F_2 :{}".format(F_2))
    # print("T_12 :{}".format(T_12))
    # print("T_r21 :{}".format(T_r21))
    # print("F_r21 :{}".format(F_r21))
    # print("T_r22 :{}".format(T_r22))
    # print("F_r22 :{}".format(F_r22))
    # print("T_matPerpendicular :{}".format(T_matPerpendicular))

    return T_matPerpendicular


def getTransmittanceForParallelIrrThroughMultiSpanRoof(simulatorClass, EParallelEastOrNorthFacingRoof):
    '''
    In the parallel direction to the grenhouse roof, the agle of the roof is 0. There is no reflection transmitted to other part of the roof.
    :return:
    '''
    ##############################################################################################################################
    # calculate the transmittance of perpendicular direction from the EAST facing roof after penetrating multi-span roof per hour
    ##############################################################################################################################
    # the transmittance of roof surfaces
    T = np.zeros(simulatorClass.getDirectSolarRadiationToOPVEastDirection().shape[0])
    # the reflectance of roof surfaces
    F = np.zeros(simulatorClass.getDirectSolarRadiationToOPVEastDirection().shape[0])

    for i in range(0, simulatorClass.getDirectSolarRadiationToOPVEastDirection().shape[0]):

        # calculate the transmittance and reflectance to each roof
        T[i], F[i] = fresnelEquation(EParallelEastOrNorthFacingRoof[i])

    return T

def getIncidentAngleForEastOrNorthRoof(EPerpendicularEastOrNorthFacingRoof, beta):
    # calculate the incident angle [rad]
    # the incident angle should be the angle between the solar irradiance and the normal to the tilted roof
    return abs(math.pi / 2.0 - abs(beta + EPerpendicularEastOrNorthFacingRoof))

    # if beta + EPerpendicularEastOrNorthFacingRoof < math.pi/2.0:
    #     return math.pi/2.0 - abs(beta + EPerpendicularEastOrNorthFacingRoof)
    # # if the angle E + alpha is over pi/2 (the sun pass the normal to the tilted roof )
    # else:
    #     return abs(beta + EPerpendicularEastOrNorthFacingRoof) -  math.pi / 2.0

def getIncidentAngleForWestOrSouthRoof(EPerpendicularWestOrSouthFacingRoof, alpha):
    # calculate the incident angle [rad]
    # the incident angle should be the angle between the solar irradiance and the normal to the tilted roof
    return abs(math.pi/2.0 - abs(alpha - EPerpendicularWestOrSouthFacingRoof))


def getIncidentAngleForEastOrNorthRoofWithBeamComingFromWestOrSouth(EPerpendicularEastOrNorthFacingRoof, beta):
    # calculate the incident angle [rad]
    # the incident angle should be the angle between the solar irradiance and the normal to the tilted roof
    return abs(math.pi / 2.0 - abs(beta - EPerpendicularEastOrNorthFacingRoof))

def getIncidentAngleForWestOrSouthRoofWithBeamComingFromWestOrSouth(EPerpendicularWestOrSouthFacingRoof, alpha):
    # calculate the incident angle [rad]
    # the incident angle should be the angle between the solar irradiance and the normal to the tilted roof
    return abs(math.pi / 2.0 - abs(alpha + EPerpendicularWestOrSouthFacingRoof))


def fresnelEquation(SolarIrradianceIncidentAngle):
    '''
    calculate the transmittance and reflectance for a given incidnet angle and index of reflectances
    reference:
    http://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/freseq.html
    https://www.youtube.com/watch?v=ayxFyRF-SrM
    https://ja.wikipedia.org/wiki/%E3%83%95%E3%83%AC%E3%83%8D%E3%83%AB%E3%81%AE%E5%BC%8F
    :return: transmittance, reflectance
    '''

    # reference: https://www.filmetrics.com/refractive-index-database/Polyethylene/PE-Polyethene
    PEFilmRefractiveIndex = constant.PEFilmRefractiveIndex
    # reference: https://en.wikipedia.org/wiki/Refractive_index
    AirRefractiveIndex = constant.AirRefractiveIndex

    # print("SolarIrradianceIncidentAngle:{}".format(SolarIrradianceIncidentAngle))

    # Snell's law, calculating the transmittance raw after refractance
    transmittanceAngle = math.asin(AirRefractiveIndex/PEFilmRefractiveIndex*math.sin(SolarIrradianceIncidentAngle))

    # S (perpendicular) wave
    perpendicularlyPolarizedTransmittance = 2.0 * AirRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) / \
                                            (AirRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) + PEFilmRefractiveIndex*math.cos(transmittanceAngle))
    perpendicularlyPolarizedReflectance = (AirRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) - PEFilmRefractiveIndex*math.cos(transmittanceAngle)) / \
                                          (AirRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) + PEFilmRefractiveIndex*math.cos(transmittanceAngle))

    # P (parallel) wave
    parallelPolarizedTransmittance = 2.0 * AirRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) / \
                                     (PEFilmRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) + AirRefractiveIndex*math.cos(transmittanceAngle))
    parallelPolarizedReflectance = (PEFilmRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) - AirRefractiveIndex*math.cos(transmittanceAngle)) / \
                                   (PEFilmRefractiveIndex*math.cos(SolarIrradianceIncidentAngle) + AirRefractiveIndex*math.cos(transmittanceAngle))

    # according to https://www.youtube.com/watch?v=ayxFyRF-SrM at around 17:00, the reflection can be negative when the phase of light changes by 180 degrees
    # Here it was assumed the phase shift does not influence the light intensity (absolute stength), and so the negative sign was changed into the positive
    perpendicularlyPolarizedReflectance = abs(perpendicularlyPolarizedReflectance)
    parallelPolarizedReflectance = abs(parallelPolarizedReflectance)


    # Assuming that sunlight included diversely oscilating radiation by 360 degrees, the transmittance and reflectance was averaged with those of parpendicular and parallel oscilation
    transmittanceForSolarIrradiance = (perpendicularlyPolarizedTransmittance + parallelPolarizedTransmittance) / 2.0
    ReflectanceForSolarIrradiance = (perpendicularlyPolarizedReflectance + parallelPolarizedReflectance) / 2.0

    return transmittanceForSolarIrradiance, ReflectanceForSolarIrradiance


def getTransmittanceThroughMultiSpanCoveringCaseA1ForEastOrNorthFacingRoof(l_a, l_b, m, T_1, F_1, T_2, F_2):
    '''
    the equation number in the reference: (A8), page 252
    '''
    transmittanceThroughMultiSpanCoveringCaseA1ForEastOrNorthFacingRoof = (l_a*T_2*(F_1*util.sigma(0, m-2, lambda s: (T_1*T_2)**s,0) + (T_1*T_2)**(m-1)) + \
            l_b*T_2*(F_1*util.sigma(0, m-1, lambda s: (T_1*T_2)**s,0) + (T_1*T_2)**m)) / (l_a + l_b)
    # print("transmittanceThroughMultiSpanCoveringCaseA1ForEastOrNorthFacingRoof:{}".format(transmittanceThroughMultiSpanCoveringCaseA1ForEastOrNorthFacingRoof))
    return transmittanceThroughMultiSpanCoveringCaseA1ForEastOrNorthFacingRoof

def getTransmittanceThroughMultiSpanCoveringCaseA1ForWestOrSouthFacingRoof(l_a, l_b, m, T_1, F_1, T_2, F_2):
    '''
    the equation number in the reference: (A8), page 252
    the content of this function is same as getTransmittanceThroughMultiSpanCoveringCaseA1ForEastOrNorthFacingRoof, but made this just for clarifying the meaning of variables.
    '''

    transmittanceThroughMultiSpanCoveringCaseA1ForWestOrSouthFacingRoof = (l_a*T_1*(F_2*util.sigma(0, m-2, lambda x: (T_1*T_2)**x,0) + (T_1*T_2)**(m-1)) + \
                                                                        l_b*T_1*(F_2*util.sigma(0, m-1, lambda x: (T_1*T_2)**x,0) + (T_1*T_2)**m)) / (l_a + l_b)
    # print("transmittanceThroughMultiSpanCoveringCaseA1ForWestOrSouthFacingRoof:{}".format(transmittanceThroughMultiSpanCoveringCaseA1ForWestOrSouthFacingRoof))
    return transmittanceThroughMultiSpanCoveringCaseA1ForWestOrSouthFacingRoof

def getReflectedE(E, roofAngle):
    incidentAngle = getIncidentAngleForWestOrSouthRoof(E, roofAngle)
    # the reflected incident angle E' is pi - (pi - alpha) - (pi/2.0 - incidentAngle))
    return abs(roofAngle - incidentAngle - math.pi/2.0)


def getFractionOfTransmittanceOfReflectedSolarIrradiance(alpha, beta, L_1, L_2, m, EPerpendicular):

    # The original source G.P.A. Bot 1983, "Greenhouse Climate: from physical processes to a dynamic model" does not seem to suppose EPerpendicular becomes more than pi/2, thus,
    # l_a and l_b became negative when EPerpendicular > pi/2 indeed. Thus it was converted to the rest of the angle
    if EPerpendicular > math.pi/2.0:
        EPerpendicular = math.pi/2.0 - EPerpendicular

    # fraction (percentage) of light which does not pass through the first span [-], equation (A14)
    l_a = L_2 * m * math.sin(EPerpendicular - beta) - L_1 * (m - 1) * math.sin(alpha + 2.0 * beta - EPerpendicular)
    # print("m:{}, L_1:{}, L_2:{}, alpha:{}, beta:{}".format(m, L_1, L_2, alpha, beta))
    # print("EPerpendicular - beta):{}".format(math.sin(EPerpendicular - beta)))
    # print("math.sin(alpha + 2.0*beta - EPerpendicular):{}".format(math.sin(alpha + 2.0 * beta - EPerpendicular)))
    # fraction (percentage) of light which crosses the first span before continuing on towards the others [-], equation (A15)
    l_b = L_1 * math.sin(alpha + 2.0 * beta - EPerpendicular) - L_2 * math.sin(EPerpendicular - beta)
    # print("l_a:{}, l_b:{}".format(l_a, l_b))

    return l_a, l_b

def getTransmittanceOfReflectedLightThroughMultiSpanCoveringCaseA2_1ForEastOrNorthFacingRoof(l_a, l_b, m, T_r11, T_r12, F_r11, F_r12, F_1, l_1, l_2):
    '''
    the equation number in the reference: (A13)
    '''
    # print("T_r11:{}, T_r12:{}, F_r11:{}, F_r12:{}, F_1:{}, l_1:{}, l_2:{}".format(T_r11, T_r12, F_r11, F_r12, F_1, l_1, l_2))

    transmittanceOfReflectedLight = (F_1*l_a*T_r11*(F_r12*util.sigma(2, m-2, lambda s: (T_r11*T_r12)**s,0.0) + (T_r11*T_r12)**(m-1)) + \
        F_1*l_b*T_r11*(F_r12*util.sigma(0, m-3, lambda s: util.sigma(0, s, lambda n: (T_r11*T_r12)**n,0),0.0) + \
                           util.sigma(0, m-2, lambda s: (T_r11 * T_r12)**s, 0.0))) / (l_1 + l_2)

    # print ("transmittanceOfReflectedLight:{}".format(transmittanceOfReflectedLight))

    return transmittanceOfReflectedLight


def getTransmittanceOfReflectedLightThroughMultiSpanCoveringCaseA2_1ForWestOrSouthFacingRoof(l_a, l_b, m, T_r21, T_r22, F_r22, F_r21, F_2, l_1, l_2):
    '''
    the content of this function is same as getTransmittanceThroughMultiSpanCoveringCaseA2_1ForEastOrNorthFacingRoof, but made this just for clarifying the meaning of variables.
    '''
    # print("T_r21:{}, T_r22:{}, F_r21:{}, F_r22:{}, F_2:{}, l_1:{}, l_2:{}".format(T_r21, T_r22, F_r21, F_r22, F_2, l_1, l_2))

    return (F_2*l_a*T_r21*(F_r22*util.sigma(2, m-2, lambda s: (T_r21*T_r22)**s,0) + (T_r21*T_r22)**(m-1)) + \
            F_2*l_b*T_r21*(F_r22*util.sigma(0, m-3, lambda s: util.sigma(0, s, lambda n: (T_r21*T_r22)**n,0),0) + \
                           util.sigma(0, m-2, lambda s: (T_r21 * T_r22)**s, 0))) / (l_1 + l_2)


def getTransmittanceThroughMultiSpanCoveringCaseA2_2ForEastOrNorthFacingRoof(l_a, l_b, m, T_r11, T_r12, F_r11, F_r12, F_1, l_1, l_2):
    '''
    the equation number in the reference: (A18)
    '''
    return (l_a*F_1 + T_r11*F_r12*util.sigma(0, m-1, lambda s: (T_r11*T_r12)**s,0) + \
            l_b*F_1*T_r11*T_r12*util.sigma(0, m - 2, lambda s: util.sigma(0, s, lambda n: (T_r11 * T_r12)**n, 0), 0))/(l_1+l_2)

def getTransmittanceThroughMultiSpanCoveringCaseA2_2ForWestOrSouthFacingRoof(l_a, l_b, m, T_r21, T_r22, F_r21, F_r22, F_2, l_1, l_2):
    '''
    the equation number in the reference: (A18)
    the content of this function is same as getTransmittanceThroughMultiSpanCoveringCaseA2_2ForEastOrNorthFacingRoof, but made this just for clarifying the meaning of variables.
    '''
    return (l_a*F_2 + T_r21*F_r22*util.sigma(0, m-1, lambda s: (T_r21*T_r22)**s,0) + \
            l_b*F_2*T_r21*T_r22*util.sigma(0, m - 2, lambda s: util.sigma(0, s, lambda n: (T_r21 * T_r22)**n, 0), 0))/(l_1+l_2)


def getSolarIrradianceDirectlhyTransmittedToPlants(alpha, beta, L_1, L_2, EPerpendicular):
    '''
    get direct radiation directly transmitted to the soil through roof surfaces
    :return:
    '''
    # the portion of the beam of incident light that travels through the ﬁrst side (west or south side) of the roof
    # the following formula is from Soriano et al. (2004), but this seems to be wrong
    # l_1 = L_1 * math.cos(alpha - EPerpendicular)
    # the following formula was cited from the original source of this model: G. P. A. Bot, 1983 "Greenhouse Climate: from physical processes to a dynamic model", page 90
    # l_1 = L_1 * math.sin(alpha + EPerpendicular)
    # In addition, the difference of greenhouse direction was considered (l_1 is for west facing roof, and l_2 is for east facing roof. The solar radiation comes from the east in the morning)
    # if the sunlight comes from east (right side in the figure)
    if EPerpendicular < math.pi:
        l_1 = L_1 * math.sin(EPerpendicular - alpha)
        # the portion of the beam of incident light that travels through the second side (east or north side) of the roof.
        l_2 = L_2 * math.sin(EPerpendicular + beta)
    # if the sunlight comes from west (right side in the figure)
    else:
        l_1 = L_1 * math.sin(EPerpendicular + alpha)
        # the portion of the beam of incident light that travels through the second side (east or north side) of the roof.
        l_2 = L_2 * math.sin(EPerpendicular - beta)
    # print("l_1:{}".format(l_1))
    # print("l_2:{}".format(l_2))

    # get the incidence angle for each facing roof
    incidentAngleForEastOrNorthRoof = getIncidentAngleForEastOrNorthRoof(EPerpendicular, beta)
    incidentAngleForWestOrSouthRoof = getIncidentAngleForWestOrSouthRoof(EPerpendicular, alpha)
    # print("incidentAngleForEastOrNorthRoof :{}".format(incidentAngleForEastOrNorthRoof))
    # print("incidentAngleForWestOrSouthRoof :{}".format(incidentAngleForWestOrSouthRoof))


    # get the transmittance
    T_2, F_2 = fresnelEquation(incidentAngleForEastOrNorthRoof)
    T_1, F_1 = fresnelEquation(incidentAngleForWestOrSouthRoof)
    # print("T_1:{}, F_1:{}, T_2:{}, F_2:{}".format(T_1, F_1, T_2, F_2))

    # the transmittance of solar irradiance directly transmitted to the soil through roof each direction of roof (surfaces east and west) (A10)
    T_12 = (T_1 * l_1 + T_2 * l_2) / (l_1 + l_2)
    # print("T_12:{}".format(T_12))

    return l_1, l_2, T_1, F_1, T_2, F_2, T_12


def getIntegratedT_matFromBothRoofs(T_matForPerpendicularIrrEastOrNorthFacingRoof, T_matForPerpendicularIrrWestOrSouthFacingRoof):
    '''
    :return: integratedT_mat
    '''
    integratedT_mat = np.zeros(T_matForPerpendicularIrrEastOrNorthFacingRoof.shape[0])

    for i in range (0, integratedT_mat.shape[0]):
        if T_matForPerpendicularIrrEastOrNorthFacingRoof[i] == 0.0 and T_matForPerpendicularIrrWestOrSouthFacingRoof[i] == 0.0: continue
        elif T_matForPerpendicularIrrEastOrNorthFacingRoof[i] != 0.0 and T_matForPerpendicularIrrWestOrSouthFacingRoof[i] == 0.0:
            integratedT_mat[i] = T_matForPerpendicularIrrEastOrNorthFacingRoof[i]
        elif T_matForPerpendicularIrrEastOrNorthFacingRoof[i] == 0.0 and T_matForPerpendicularIrrWestOrSouthFacingRoof[i] != 0.0:
            integratedT_mat[i] = T_matForPerpendicularIrrWestOrSouthFacingRoof[i]
        # if both t_mat are not 0
        else:
            integratedT_mat[i] = (T_matForPerpendicularIrrEastOrNorthFacingRoof[i] + T_matForPerpendicularIrrWestOrSouthFacingRoof[i]) / 2.0

    return integratedT_mat

