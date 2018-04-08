# -*- coding: utf-8 -*-
#######################################################
# author :Kensaku Okada [kensakuokada@email.arizona.edu]
# create date : 15 Jun 2017
# last edit date: 15 Jun 2017
#######################################################

# convert ratio of CO2 into SUgar (CH2O)
c_alpha = 30.0 / 44.0
# respiratory and syntehsis losses of non-structural material due to growth
c_beta = 0.8
# the saturation growth rate at 20[C] [/s]
c_gr_max = {'s-1' :5.0 * 10**(-6)}

c_gamma = 1.0
# Q10 factor for growth
c_Q10_gr = 1.6
# the maintenance respiration coefficient for shoot at 25[C]
c_resp_sht = {'s-1' : 3.47 * 10**(-7)}
# the maintenance respiration coefficient for root  at 25[C]
c_resp_rt = {'s-1' : 1.16 * 10**(-7)}
# Q10 factor of the maintenance respiration
c_Q10_resp = 2.0
# the ratio of the root dry weight to the total crop dry weight
c_tau = 0.15
# extinction coefficient
# c_K = 0.9
# extinction coefficient for 25 heads/m^2 density
c_K = 1.0
# structural leaf area ratio
c_lar = {'m2 g-2' : 75 * 10**(-3)}
# density of CO2
c_omega = {'g m-3' : 1.83 * 10**(-3) }
# the CO2 compensation point at 20[C]
c_upperCaseGamma = {'ppm': 40.0}
# the Q10 value which account for the effect of temperature on upperCaseGamma (Γ)
c_Q10_upperCaseGamma = 2.0
# light use efficiency at very high CO2 concentrations
c_epsilon = {'g J-1' : 17.0 * 10 ** (-6)}
# the boundary layer conductance of lettuce leaves
g_bnd = {'m s-1' : 0.007}
# the stomatal resistance
g_stm = {'m s-1': 0.005 }
# parameters for the carboxylation conductance
c_car1 = -1.32 * 10**(-5)
c_car2 = 5.94 * 10**(-4)
c_car3 = -2.64 * 10**(-3)

canopyTemp = {'celsius': 17.5 }
# canopyTemp = {'celsius': 40 }
# canopyTemp = {'celsius': 5 }

carboxilationConductatnce = c_car1 * canopyTemp['celsius']**2 + c_car1 * canopyTemp['celsius'] + c_car3

print (carboxilationConductatnce)


canopyTemp = {'celsius': 40 }
carboxilationConductatnce = c_car1 * canopyTemp['celsius']**2 + c_car1 * canopyTemp['celsius'] + c_car3
print (carboxilationConductatnce)


canopyTemp = {'celsius': 5 }
carboxilationConductatnce = c_car1 * canopyTemp['celsius']**2 + c_car1 * canopyTemp['celsius'] + c_car3
print (carboxilationConductatnce)










