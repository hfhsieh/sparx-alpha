#!/usr/bin/env python3

import matplotlib
matplotlib.use("Agg")

import numpy as np
from matplotlib import pyplot as plt


plt.rcParams["font.size"] = 14


### Model
data = np.genfromtxt("model_1.d", usecols = [0, 1, 3, 4, 5])

xlabel  = "Radius [cm]"
ylabels = (r"H$_{2}$ Number Density [cc$^{-1}]$",
           r"Gas Temperature, T [k]",
           r"Radial Velocity, $V_r$ [km s$^{-1}$]",
           r"Turbulent Velocity, $V_\mathrm{tur}$ [km s$^{-1}$]")


fig, axes = plt.subplots(figsize = (9.6, 7.2), nrows = 2, ncols = 2)
axes_ravel = axes.ravel()

for idx, ax in enumerate(axes_ravel, 1):
    ax.semilogx(data[:, 0], data[:, idx])


for ax, ylabel in zip(axes_ravel, ylabels):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params("both", length = 6, width = 1, which = "major", direction = "in")
    ax.tick_params("both", length = 3, width = 1, which = "minor", direction = "in")
    ax.minorticks_on()

axes_ravel[0].set_yscale("log")

fig.tight_layout()
plt.savefig("P2A_model.png", dpi = 120, bbox_inches = "tight")
plt.close(fig)


### Populations
PC2CM = 30.857 * 1e17

data_sparx  = np.genfromtxt("pops_sparx.dat")
data_ratran = np.genfromtxt("pops_ratran.dat")

rad_sparx  = data_sparx[:, 0] * PC2CM
rad_ratran = 0.5 * (data_ratran[:, 1] + data_ratran[:, 2]) * 1.0e2

offset_sparx  = 1
offset_ratran = 9


fig, axes = plt.subplots(figsize = (14.0, 7.2), nrows = 3, ncols = 4, sharex = True)
axes_ravel = axes.ravel()

for idx, ax in enumerate(axes_ravel[:-2]):
    ax.loglog(rad_sparx, data_sparx[:, idx + offset_sparx],
              ls = "solid", c = "C0", alpha = 0.7, label = "SPARX 1D", lw = 3)
    ax.loglog(rad_ratran, data_ratran[:, idx + offset_ratran],
              ls = "dashed", c = "C1", label = "RATRAN", lw = 3)

    if idx < 2:
        ax.text(0.1, 0.85, "HCO$^{+}$" + " J={}".format(idx),
                transform = ax.transAxes)
    else:
        ax.text(0.9, 0.85, "HCO$^{+}$" + " J={}".format(idx),
                transform = ax.transAxes, ha = "right")


for ax in axes[-1]:
    ax.set_xlabel("Radius [cm]")

for ax in axes[:, 0]:
    ax.set_ylabel("Frac. Population")

for ax in axes_ravel:
    ax.tick_params("both", length = 6, width = 1, which = "major", direction = "in")
    ax.tick_params("both", length = 3, width = 1, which = "minor", direction = "in")
    ax.minorticks_on()


fig.delaxes(axes_ravel[-2])
fig.delaxes(axes_ravel[-1])
fig.tight_layout()

axes_ravel[-3].legend(loc = "upper right", bbox_to_anchor = (2.2, 1.0), framealpha = 0)

plt.savefig("P2A_pops.png", dpi = 120, bbox_inches = "tight")
plt.close(fig)
