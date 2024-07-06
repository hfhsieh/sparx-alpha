from sympy import Symbol,integrate
from math import pi
from .pre_unit import *

class error:
    def __init__(self,mesh,phys):
        #if phys.model.ModelType == 'Function' and mesh.grid.GridType =='SPH1D':
        if False:
            self.calc_exact_mass(mesh,phys)
            print('Analytical Mass : %e Msun' %self.exact_mass)
            MassError = 100. * ( phys.mass - self.exact_mass ) / self.exact_mass
            print('Mass Error of the Gridding : %e %%' %MassError)
        else:
            print('Total mass = %e MSun' %phys.mass)

        print('Largest Velocity Dispersion to Turbulent Velocity : %e' %phys.MVD2Vt)
        print('Largest Dispersion occurs at spatial index = ', phys.MVD2Vt_index)


    def calc_exact_mass(self,mesh,phys):
        gr = mesh.grid
        md = phys.model

        r_min = gr.Rin
        r_max = gr.Rout
        r = Symbol('r')
        self.exact_mass = integrate(md.Density1D(r) * 4.*pi*r**2,(r,r_min,r_max))
        self.exact_mass *= volume_pc2m * MeanMolecularMass * kg2Msun

