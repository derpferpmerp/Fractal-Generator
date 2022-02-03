import os

import numpy as np
from matplotlib import pyplot as plt
from numpy import cos
from scipy.integrate import odeint


fig, ax = plt.subplots(1, 1, figsize=(20, 20))

# CONSTANTS
DELTA = 0.3  # Damping
BETA = 0.5  # Restoring Force
ALPHA = 1  # Stiffness
GAMMA = 1  # Driving Force Amplitude
OMEGA = 3  # Angular Frequency
X_0 = 1  # Initial Displacement
V_0 = 2  # Initial Velocity


def derive(z, t, OMGA):
    tmp_dxdt, tmp_x = z
    return np.array([
        (GAMMA*cos(OMGA*t)) - (DELTA*tmp_dxdt) -
        (ALPHA*tmp_x) - (BETA*pow(tmp_x, 3)),
        tmp_dxdt,
    ])


tmax, dt = 10, 0.01
OMEGA_RANGE = np.linspace(0, 10, 100)

t = np.arange(0, tmax, dt)
SOLS = []
MN = None
MX = 0
for omega in OMEGA_RANGE:
    sol = odeint(derive, [X_0, V_0], t, args=(omega,))[..., 0]
    mn, mx = [ min(sol), max(sol)]
    plt.plot(t, sol)

plt.savefig(os.path.join(os.path.dirname(__file__), "MESS.png"))
