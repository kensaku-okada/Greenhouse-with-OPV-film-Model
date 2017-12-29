import numpy as np
import matplotlib.pyplot as plt
import math

# dliList = np.array([40,40,40,40,40,40,40,40,40,40,
#                 40,40,40,40,40,40,40,40,40,40,
#                 40,40,40,40,40,40,40,40,40,40,
#                 40,40,40,40,40,])

dliList = np.array([22,22,22,22,22,22,22,22,22,22,
                    22,22,22,22,22,22,22,22,22,22,
                    22,22,22,22,22,22,22,22,22,22,
                    22,22,22,22,22,])

dli = dliList[0]

sdm = 0
d_sdm = 0
sdmAccumulated = 0

a = 0
b = 0.4822
c = -0.006225
t = 35
dt = 1

for t in range(1, 1+len(dliList)):
    a = -8.596 + 0.0743 * dli

    sdm = math.e ** (a + b * t + c * t**2)
    d_sdm = (b + 2 * c * t) * sdm
    sdmAccumulated += d_sdm
    # print "t:{} d_sdm:{}".format(t, d_sdm)
fm = sdm/0.045
print "case1 sdm accumulated version: {}".format(sdmAccumulated)

##########################################################################

dli = dliList[0]

t = 35
a = -8.596 + 0.0743 * dli

sdm = math.e ** (a + b * t + c * t**2)

print "case2 sdm (analytical answer): {}".format(sdm)
##########################################################################
# case 3

# dliList = np.array([22,22,22,22,22,22,22,22,22,22,
#                     22,22,22,22,22,22,22,22,22,22,
#                     22,22,22,22,22,22,22,22,22,22,
#                     22,22,22,22,22,])
dli = dliList[0]

sdmList = np.zeros(len(dliList)+1)
d_sdmList = np.zeros(len(dliList)+1)
dd_sdmList = np.zeros(len(dliList)+1)

d_sdm = 0
sdmAccumulated = 0

a = 0
b = 0.4822
c = -0.006225
t = 35
dt = 1
# sdmInit = math.e ** (a + b * 0 + c * 0 **2)
sdmInit = 0
sdmList[0] = sdmInit

for t in range(1, 1+len(dliList)):
    a = -8.596 + 0.0743 * dli

    sdmList[t] = math.e ** (a + b * t + c * t**2)
    d_sdmList[t] = (b + 2 * c * t) * sdmList[t]
    dd_sdmList[t] = 2*c*sdmList[t] + (b + 2 * c * t)**2 * sdmList[t]
    # print "d_sdmList[{}]:{}".format(t, d_sdmList[t])
    # print "dd_sdmList[{}]:{}".format(t, dd_sdmList[t])

    # taylor expansion: x_0 = 0, h = 1 (source: http://eman-physics.net/math/taylor.html)
    sdmList[t] = sdmList[t-1] + d_sdmList[t-1] * dt + (1.0/(math.factorial(2)))*dd_sdmList[t-1]*((dt)**2)

    # print "t = {} case3 sdmList[len(dliList)]: {}".format(t, sdmList[t])

fm = sdm/0.045

print "t = {} case3 sdm (Taylor expansion 2nd order approximation): {}".format(len(dliList), sdmList[len(dliList)])

##############################################################################
# case4
#
# dliList = np.array([22,22,22,22,22,22,22,22,22,22,
#                     22,22,22,22,22,22,22,22,22,22,
#                     22,22,22,22,22,22,22,22,22,22,
#                     22,22,22,22,22,])
dli = dliList[0]

sdmList = np.zeros(len(dliList)+1)
d_sdmList = np.zeros(len(dliList)+1)
dd_sdmList = np.zeros(len(dliList)+1)
ddd_sdmList = np.zeros(len(dliList)+1)

d_sdm = 0
sdmAccumulated = 0

a = 0
b = 0.4822
c = -0.006225
t = 35
dt = 1
# sdmInit = math.e ** (a + b * 0 + c * 0 **2)
sdmInit = 0.0001
sdmList[0] = sdmInit
# sdmList[0] = math.e ** (a + b * 0.0 + c * 0.0**2)

d_sdmList[0] = (b + 2 * c * 0.0) * sdmList[0]
dd_sdmList[0] = 2 * c * sdmList[0] + (b + 2 * c * 0.0) ** 2 * sdmList[0]
ddd_sdmList[0] = 2 * c * d_sdmList[0] + 4 * c * (b + 2 * c * t) * sdmList[0] + (b + 2 * c * 0.0) ** 2 * d_sdmList[0]



for t in range(1, 1+len(dliList)):
    a = -8.596 + 0.0743 * dli

    sdmList[t] = math.e ** (a + b * t + c * t**2)
    d_sdmList[t] = (b + 2 * c * t) * sdmList[t]
    dd_sdmList[t] = 2*c*sdmList[t] + (b + 2 * c * t)**2 * sdmList[t]
    ddd_sdmList[t] = 2*c*d_sdmList[t] + 4*c*(b + 2 * c * t) * sdmList[t]  + (b + 2 * c * t)**2 * d_sdmList[t]
    # print "d_sdmList[{}]:{}".format(t, d_sdmList[t])
    # print "dd_sdmList[{}]:{}".format(t, dd_sdmList[t])
    # print "ddd_sdmList[t]:{}".format(t, ddd_sdmList[t])
    sdmList[t] = math.e ** (a + b * t + c * t**2)
    d_sdmList[t] = (b + 2 * c * t) * sdmList[t]
    dd_sdmList[t] = 2*c*sdmList[t] + (b + 2 * c * t)**2 * sdmList[t]



    # taylor expansion: x_0 = 0, h = 1 (source: http://eman-physics.net/math/taylor.html)
    sdmList[t] = sdmList[t-1] + \
                 1.0/(math.factorial(1))*d_sdmList[t-1] * dt + \
                 1.0/(math.factorial(2))*dd_sdmList[t-1]*((dt)**2) + \
                 1.0/(math.factorial(3))*ddd_sdmList[t-1]*((dt)**3)

    # sdmList[t] = sdmList[t] + \
    #              1.0/(math.factorial(1))*d_sdmList[t] * dt + \
    #              1.0/(math.factorial(2))*dd_sdmList[t]*((dt)**2) + \
    #              1.0/(math.factorial(3))*ddd_sdmList[t]*((dt)**3)

    # print "t = {} case4 sdmList[len(dliList)]: {}".format(t, sdmList[t])
    # print "t = {} case4 (1/(math.factorial(3)))*ddd_sdmList[t-1]*((dt)**3): {}".format(t, (1.0/(math.factorial(3)))*ddd_sdmList[t-1]*((dt)**3))
    # print "1/(math.factorial(3)):{}".format(1.0/(math.factorial(3)))
    # print "1/(math.factorial(2)):{}".format(1.0/(math.factorial(2)))
    # print "t:{}, sdmList:{}".format(t, sdmList)

fm = sdm/0.045

print "t = {} case4 sdmList (Taylor expansion 3rd order approximation): {}".format(len(dliList), sdmList[len(dliList)])



