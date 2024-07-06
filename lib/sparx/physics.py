##
## Various physics consants and routines
##

# Some necessary imports
from math import sqrt, exp, pi
from sparx import MOLEC_LIST, MOLEC_DIR

class Const:
    '''Physical constants'''
    # Physical constants
    pi = pi
    spi = sqrt(pi)
    G = 6.673E-11 # m^3kg^-1s^-2
    c = 2.99792458e8 # m s^-1
    k = 1.3806503e-23 # J K^-1
    h = 6.62606876e-34 # J s
    sigma_sb = 5.67e-8 # W m^-2 K^-4
    me = 9.1093897e-31 # kg
    mp = 1.6726231e-27 # kg

class Units:
    '''Physical units'''
    # Angular units
    deg = Const.pi / 180.0
    amin = deg / 60.0
    asec = amin / 60.0

    # Time units
    minute = 60.0 # s
    hour = 60.0 * minute # s
    day = 24.0 * hour
    year = 365.242199 * day # s

    # Length units
    Rearth = 6.378e6 # m
    Rsun = 6.96e8 # m
    L_sun = 3.839e26 # J s^-1
    au = 1.49598e11 # m
    pc = 3.08568025e16 # m
    percc = 1.0e6 # m^-3
    km = 1.0e3 # m
    cm = 1.0e-2 # m

    # Mass units
    amu = 1.66053873E-27 # kg
    evamu = 96.5e6 # J/kg
    Msun = 1.9891e30 # kg

    # Energy units
    eV = 1.602176487e-19 # J

    # Brightness units
    Jy = 1e-26 # W m^-2 Hz^-1

################################################################################

def StefanBoltzmann_T2F(T_k):
    '''
    The Stefan-Boltzmann law: F = sigma * T**4
    i.e. the total (frequency integrated) flux from a black body at
    thermal temperature T_k
    '''
    return Const.sigma_sb * T_k**4.0

################################################################################

def StefanBoltzmann_F2T(F):
    '''
    Inverse of the Stefan-Boltzmann law: T = (F / sigma)**(1/4)
    i.e. the thermal temperature of a black body emitting a total
    (frequency integrated) flux F
    '''
    return (F / Const.sigma_sb)**0.25

################################################################################

def PlanckLaw(nu, T_k):
    '''
    The Planck function: B_nu(T) = (2 * h * nu**3 / c**2) / (exp(h * nu / (k * T)) - 1)
    CAUTION: exp() diverges VERY QUICKLY and can easily overflow!!!
    Therefore a safer implementation is to use Rayleigh-Jeans' Law
    for h * nu << k * T and Wien's Law otherwise (saved for later).
    '''
    return (2.0 * Const.h * nu**3.0 / Const.c**2.0) / (exp(Const.h * nu / (Const.k * T_k)) - 1.0)

################################################################################

def WienDispLaw_nu(T_k):
    '''
    The Wien displacement law: h * nu_max = 2.82 * k * T
    Calculate at which frequency the black body
    emission should be peaked at.
    '''
    return 2.82 * Const.k * T_k / Const.h

################################################################################

def WienDispLaw_lam(T_k):
    '''
    The Wien displacement law: h * nu_max = 2.82 * k * T
    Calculate at which wavelength the black body
    emission should be peaked at.
    '''
    return Const.c / WienDispLaw_nu(T_k)

################################################################################

def Doppler_vel2frq(f0, v):
    '''
    This function converts frequency to velocity through the
    Doppler effect:
        f = f0 * sqrt((c - v) / (c + v))
    '''
    return f0 * sqrt((Const.c - v) / (Const.c + v))

################################################################################

def Doppler_frq2vel(f0, f):
    '''
    This function converts frequency to velocity through the
    Doppler effect:
        f = f0 * sqrt((c - v) / (c + v))
     => v = c * (1 - (f / f0)**2) / (1 + (f / f0)**2)
    '''
    return Const.c * (1.0 - (f / f0)**2) / (1.0 + (f / f0)**2)

def thermal_vwidth(Tk, m):
    """Thermal velocity width

    Tk: kinetic temperature [K]
    m: molecular mass [kg]
    Note that this is sqrt(2)*sigma where sigma is the half-width of the
    corresponding Gaussian distribution.
    """
    return sqrt(2.0 * Const.k * Tk / m) # [m/s]

def gaussian_fprofile(nu, nu0, delta_nu):
    """Gaussian line profile function

    nu0: line center frequency
    delta_nu: linewidth
    nu: frequency

    Note that delta_nu=sqrt(2)*sigma where sigma is the half-width of the
    corresponding Gaussian distribution.
    see e.g. Rybicki & Lightman (1979) p. 288
    """
    return (1 / (delta_nu * Const.spi)) * exp(-((nu - nu0) / delta_nu)**2.0)

def gaussian_vprofile(vel, delta_vel):
    """
    # vel: velocity
    # delta_vel: linewidth
    #
    # Note that delta_vel=sqrt(2)*sigma where sigma is the half-width of the
    # corresponding Gaussian distribution.
    # see e.g. Rybicki & Lightman (1979) p. 288
    #
    """
    return (1 / (delta_vel * Const.spi)) * exp(-(vel / delta_vel)**2.0)

def Keplerian_velocity(m, r):
    """
    Calculate the Keplerian rotation velocity at radius r with central mass m.
    """
    return (Const.G * m / r)**0.5

################################################################################
# Vector functions

def Vec3_Normalize(a):
    mag = sqrt(a[0]**2 + a[1]**2 + a[2]**2)
    return [a[i] / mag for i in range(3)]

def Vec3_DotProd(a, b):
    return [a[i] * b[i] for i in range(3)]

def Vec3_Scale(a, k):
    return [a[i] * k for i in range(3)]

################################################################################
# Other

class Molecule:
    """
    Molecule class
    """
    def __init__(self, name):
        """
        Constructor for Molecule class
        """
        if name not in MOLEC_LIST:
            raise Exception ("Molecule '%s' is not available"%name)
        self.name = name
        self.path = MOLEC_DIR+"/"+name+".dat"
        self.load_file(self.path)
        return

    def load_file(self, fpath):
        """
        Load molecular data from file at fpath
        """
        # Load molecule from file
        fobj = open(fpath, "r")
        if fobj is None:
            raise Exception ("Unable to access molecular data file '%s'" % (fpath))

        # Lines 1-2: molecule name
        for i in range(2):
            line = fobj.readline()
        self.chemname = line.strip()

        # Lines 3-4: molecular weight
        for i in range(2):
            line = fobj.readline()
        self.weight = float(line.strip()) # amu
        self.mass = self.weight * Units.amu # amu -> kg

        # Lines 5-6: number of energy levels (NLEV)
        for i in range(2):
            line = fobj.readline()
        self.nlev = int(line.strip())

        # Lines 7-7+NLEV: level number, level energy (cm-1), statistical weight
        # Get quantum state label from header
        line = fobj.readline()
        hdrcols = [i.strip() for i in line.split("+")]
        self.qstate = "+".join(hdrcols[3:])

        # Load level data
        self.lev_E = []
        self.lev_g = []
        self.lev_state = []
        for i in range(self.nlev):
            line = fobj.readline()
            cols = line.split()
            if len(cols) < 4:
                raise Exception ("%s: Number of columns in molecular data level table < 4" % name)
            self.lev_E += [float(cols[1]) * (1.0 / Units.cm) * Const.h * Const.c] # cm^-1 -> J
            self.lev_g += [float(cols[2])] # dimensionless
            self.lev_state += [cols[3]] # string

        # Lines 8+NLEV-9+NLEV: number of radiative transitions (NLIN)
        for i in range(2):
            line = fobj.readline()
        self.nline = int(line.strip())

        # Load line data
        fobj.readline() # Skip table header
        self.line_up = []
        self.line_lo = []
        self.line_Aul = []
        self.line_Bul = []
        self.line_Blu = []
        self.line_freq = []
        for i in range(self.nline):
            line = fobj.readline()
            cols = line.split()
            if len(cols) != 6:
                raise Exception ("Number of columns in molecular data line table not eq 6")
            lev_up = int(cols[1]) - 1
            lev_lo = int(cols[2]) - 1
            self.line_up += [lev_up]
            self.line_lo += [lev_lo]

            # Recalculate frequency from energies
            Eu = self.lev_E[self.line_up[i]]
            El = self.lev_E[self.line_lo[i]]
            freq = (Eu - El) / Const.h # Hz
            self.line_freq += [freq]

            # Aul, Bul and Blu
            Aul = float(cols[3]) # s^-1
            Bul = Aul * Const.c**2 / (2.0 * Const.h * freq**3.0) # Inu^-1s^-1
            gu = self.lev_g[lev_up]
            gl = self.lev_g[lev_lo]
            Blu = (gu / gl) * Bul # Inu^-1s^-1
            self.line_Aul += [Aul]
            self.line_Bul += [Bul]
            self.line_Blu += [Blu]
        # Get lowest frequency transition
        self.min_freq = sorted(self.line_freq)[0]

        # Lines 11+NLEV+NLIN-12+NLEV+NLIN: number of collision partners
        for i in range(2):
            line = fobj.readline()
        self.ncol = int(line.strip())
        self.col = []

        class Coll:
            """
            Molecular collisional partner class
            """
            # List of species
            species = ("H2", "p-H2", "o-H2", "e", "H", "He")

            def __init__(self, mol):
                # Pointer to moelcule
                self.mol = mol

                # Lines 13+NLEV+NLIN-14+NLEV+NLIN: collision partner ID and reference.
                # Valid identifications are:
                # 1=H2, 2=para-H2, 3=ortho-H2, 4=electrons, 5=H, 6=He.
                for i in range(2):
                    line = fobj.readline()
                cols = line.strip().split()
                self.id = int(cols[0])
                self.name = self.species[self.id - 1]
                self.ref = " ".join([i.strip() for i in cols[1:]])

                # Lines 15+NLEV+NLIN-16+NLEV+NLIN: number of transitions for which
                # collisional data exist (NCOL)
                for i in range(2):
                    line = fobj.readline()
                self.ntrans = int(line)

                # Lines 17+NLEV+NLIN-18+NLEV+NLIN: number of temperatures for which
                # collisional data exist
                for i in range(2):
                    line = fobj.readline()
                self.ntemp = int(line)

                # Lines 19+NLEV+NLIN-20+NLEV+NLIN: values of temperatures for which
                # collisional data exist
                for i in range(2):
                    line = fobj.readline()
                cols = line.strip().split()
                self.temp = [float(i) for i in cols] # K

                # Lines 21+NLEV+NLIN-21+NLEV+NLIN+NCOL: transition number, upper
                # level, lower level; rate coefficients (cm3s-1) at each temperature.
                # Skip header
                fobj.readline()
                # Read table
                self.trans_up = []
                self.trans_lo = []
                self.trans_Kul = []
                for i in range(self.ntrans):
                    line = fobj.readline()
                    cols = line.strip().split()
                    self.trans_up += [int(cols[1]) - 1]
                    self.trans_lo += [int(cols[2]) - 1]
                    self.trans_Kul += [[float(i) * (Units.cm**3) for i in cols[3:]]] # cm^3 s^-1 -> m^3 s^-1
                return

            def get_boltzmann_ratio(self, itrans, T_k):
                """
                Calculate Boltzmann ratio for transition itrans
                at kinetic temperature T_k
                """
                up = self.trans_up[itrans]
                lo = self.trans_lo[itrans]
                g_u = self.mol.lev_g[up]
                g_l = self.mol.lev_g[lo]
                E_u = self.mol.lev_E[up]
                E_l = self.mol.lev_E[lo]
                return (g_u / g_l) * exp(-(E_u - E_l) / (Const.k * T_k))

            def get_down_rate(self, itrans, T_k):
                """
                Calculate downward collisional rate: linearly interpolate
                if temperature not in given table, but NO extrapolation!
                """
                if T_k < self.temp[0]:
                    return self.trans_Kul[itrans][0]
                elif T_k > self.temp[-1]:
                    return self.trans_Kul[itrans][-1]
                elif self.ntemp > 1:
                    # SciPy interpolation will only work when there is more
                    # than 1 entry
                    from scipy.interpolate import interpolate as interp
                    iobj = interp.interp1d(self.temp, self.trans_Kul[itrans])
                    return iobj(T_k)
                else:
                    return self.trans_Kul[itrans][0]

            def get_up_rate(self, itrans, T_k):
                """
                Calculate upward collisional rate according to
                K_lu / K_ul = (g_u / g_l) * exp(-(E_u - E_l) / (kB * Tk))
                = Boltzmann ratio
                """
                '''Calculate upward collisional rate for itrans at T_k'''
                down_rate = self.get_down_rate(0, T_k)
                return down_rate * self.get_boltzmann_ratio(itrans, T_k)

            def get_crit_dens(self, iline, T_k):
                """
                Calculate critical density for transition iline
                at kinetic temperature T_k
                """
                '''Calculate critical density for itrans at T_k'''
                up = self.mol.line_up[iline]
                lo = self.mol.line_lo[iline]
                found = False # just in case
                for i in range(self.ntrans):
                    if up == self.trans_up[i] and lo == self.trans_lo[i]:
                        Kul = self.get_down_rate(i, T_k)
                        found = True
                        break
                if not found:
                    raise "Radiative transition %d has no counterpart in collision data, something's wrong" % iline
                return self.mol.line_Aul[iline] / Kul

        # Read collisional partners
        for i in range(self.ncol):
            self.col += [Coll(self)]
        return

    def get_partition_func(self, T_k):
        """
        Calculate the partition function at T_k
        """
        terms = [self.lev_g[i] * exp(-self.lev_E[i] / (Const.k * T_k)) for i in range(self.nlev)]
        return sum(terms)

    def get_boltzmann_levels(self, T_k):
        """
        Get Boltzmann distribution of levels
        """
        zt = self.get_partition_func(T_k)
        return [self.lev_g[i] * exp(-self.lev_E[i] / (Const.k * T_k)) / zt for i in range(self.nlev)]

    def get_boltzmann_ratio(self, iline, T_k):
        '''
        Calculate Boltzmann ratio for line transition iline
        at kinetic temperature T_k
        '''
        up = self.line_up[iline]
        lo = self.line_lo[iline]
        g_u = self.lev_g[up]
        g_l = self.lev_g[lo]
        E_u = self.lev_E[up]
        E_l = self.lev_E[lo]
        return (g_u / g_l) * exp(-(E_u - E_l) / (Const.k * T_k))

    def __repr__(self):
        '''
        String to return when being printed
        '''
        return\
            "Name: %s\n" % self.name+\
            "Molecular weight: %g (%g kg, %g eV)\n" % (self.weight, self.mass, self.mass * Const.c**2 / Units.eV)+\
            "Number of levels: %d\n" % self.nlev+\
            "%10s %20s %20s %20s\n" % ("LEVEL", "ENERGY(cm^-1)", "WEIGHT", self.qstate)+\
            "\n".join(["%10d %20g %20g %20s" % (i, self.lev_E[i] / (Const.h * Const.c) * Units.cm, self.lev_g[i], self.lev_state[i]) for i in range(self.nlev)])+"\n"+\
            "\n"+\
            "Number of lines: %d\n" % self.nline+\
            "%10s %10s %10s %20s %20s %20s %20s\n" % ("LINE", "UPPER", "LOWER", "A(s^-1)", "Bul(Inu^-1s^-1)", "Blu(Inu^-1s^-1)", "FREQ(GHz)")+\
            "\n".join(["%10d %10d %10d %20g %20g %20g %20g" % (i, self.line_up[i], self.line_lo[i], self.line_Aul[i], self.line_Bul[i], self.line_Blu[i], self.line_freq[i] / 1e9) for i in range(self.nline)])+"\n"+\
            "\n"+\
            "Total %d collisional partners: "%self.ncol+", ".join([col.name for col in self.col])+"\n"+\
            "\n\n".join([
                "Collisional partner #%d: %s (code=%d)\n" % (i+1, self.col[i].name, self.col[i].id)+\
                "Reference: %s\n" % (self.col[i].ref)+\
                "Number of transitions: %d\n" % (self.col[i].ntrans)+\
                "Downward collisional rate coefficients (cm^3s^-1):\n"+\
                "%5s %5s %5s "%("TRANS", "UPPER", "LOWER")+" ".join(["%11gK" % j for j in self.col[i].temp])+"\n"+\
                "\n".join(["%5d %5d %5d " % (j, self.col[i].trans_up[j], self.col[i].trans_lo[j])+" ".join(["%12.4e"%(K_ul/Units.cm**3) for K_ul in self.col[i].trans_Kul[j]]) for j in range(self.col[i].ntrans)])
            for i in range(self.ncol)])+"\n"

    def get_thermal_fwidth(self, iline, Tk):
        '''
        Calculate thermal line width (frequency width)
        '''
        delta_v = thermal_vwidth(Tk, self.mass)
        delta_nu = abs(Doppler_vel2frq(self.line_freq[iline], delta_v) - self.line_freq[iline])
        return delta_nu

    def get_thermal_vwidth(self, T_k):
        """
        Calculate thermal velocity width
        """
        return thermal_vwidth(T_k, self.mass)

    def get_thermal_sigmanu(self, T_k, iline, vel):
        """
        Calculate absorption cross section for thermal equilibrium
        """
        pops = self.get_boltzmann_levels(T_k)
        up = self.line_up[iline]
        lo = self.line_lo[iline]
        nu = self.line_freq[iline]
        Blu = self.line_Blu[iline]
        Bul = self.line_Bul[iline]
        delta_vel = self.get_thermal_vwidth(T_k)
        return (Const.h * nu) / (4.0 * pi) * (pops[lo] * Blu - pops[up] * Bul) * (Const.c / nu) * gaussian_vprofile(vel, delta_vel)



