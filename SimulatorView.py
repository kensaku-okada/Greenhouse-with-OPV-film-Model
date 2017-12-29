# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 19 Dec 2017
# last edit date: 19 Dec 2017
#######################################################

##########import package files##########
# from scipy import stats
import datetime
import sys
import os as os
import numpy as np
import matplotlib.pyplot as plt
import math
import CropElectricityYeildSimulator1 as Simulator1
import TwoDimLeastSquareAnalysis as TwoDimLS
import Util as util

case = "LeastSquareMethod"
# case = "MINLPc"
# case = "ShadingCurtainReinforcementLearning"

# Least Square method
if case == "LeastSquareMethod":

  # get the 2-D data for least square method
  profitVSOPVCoverageData, _ = Simulator1.simulateCropElectricityYieldProfit1()
  # print "profitVSOPVCoverageData:{}".format(profitVSOPVCoverageData)

  # ####################################################################################################
  # Stop execution here...
  sys.exit()
  # Move the above line to different parts of the assignment as you implement more of the functionality.
  # ####################################################################################################


  # create the instance
  twoDimLeastSquare = TwoDimLS.TwoDimLeastSquareAnalysis(profitVSOPVCoverageData)
  # print "twoDimLeastSquare.getXaxis():{}".format(twoDimLeastSquare.getXAxis())

  x = twoDimLeastSquare.getXAxis()
  y = twoDimLeastSquare.getYAxis()

  ########################### 10-fold CV (Cross Validation)
  NumOfFold = 10
  maxorder = 15
  k10BestPolyOrder, min_log_mean_10cv_loss = twoDimLeastSquare.runCrossValidation(NumOfFold, maxorder, x, y,
                                          randomize_data=True,
                                          cv_loss_title='10-fold CV Loss',
                                          filepath='./exportData/10fold-CV.png')

  # curve fitting (least square method) with given order w
  w = twoDimLeastSquare.getApproximatedFittingCurve(k10BestPolyOrder)

  # This polyfit is just for generating non-optimal order figure.  Commend out this except debugging or experiment
  w = np.polyfit(x, y, 15)
  w = w[::-1]

  # plot the best order curve with the data points
  util.plotDataAndModel(x, y, w, filepath='./exportData/bestPolynomialKFold.png')
  print ('\n======================')
  print ('10-fold the best order = {0}. loss = {1}, func coefficients w = {2}'.format(k10BestPolyOrder, min_log_mean_10cv_loss, w))

  ########################### LOOCV (Leave One Out Cross Validation)
  NumOfFold = twoDimLeastSquare.getXAxis().shape[0]
  loocv_best_poly, min_log_mean_loocv_loss = twoDimLeastSquare.runCrossValidation(NumOfFold, maxorder, x, y,
                                              randomize_data=True,
                                              cv_loss_title='LOOCV Loss',
                                              filepath='./exportData/LOOCV.png')

  # curve fitting (least square method) with given order w
  wLOOCV = twoDimLeastSquare.getApproximatedFittingCurve(k10BestPolyOrder)
  # This polyfit is just for generating non-optimal order figure.  Commend out this except debugging or experiment
  # wLOOCV = np.polyfit(x, y, 8)
  # wLOOCV = wLOOCV[::-1]

  # plot the best order curve with the data points
  util.plotDataAndModel(x, y, wLOOCV, filepath='./exportData/bestPolynomialLOOCV.png')
  print ('\n======================')
  print '\n(LOOCV) the best order = {0}. loss = {1}, func coefficients w = {2}'.format(loocv_best_poly, min_log_mean_loocv_loss, w)


########################### Mixed integer non-liner programming with constraints###########################
elif case == "MINLPc":
 print "run SimulatorMINLPc.py"


########################### Reinforcement learning (q learning)###########################
elif case == "ShadingCurtainReinforcementLearning":
  # run simulateCropElectricityYieldProfit1 to set values to an object of CropElectricityYieldSimulator1
  cropElectricityYieldSimulator1, qLearningAgentsShadingCurtain = Simulator1.simulateCropElectricityYieldProfitRLShadingCurtain()
















