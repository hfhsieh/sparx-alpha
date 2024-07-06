#!/usr/bin/env python
###############################################################################
# This script intends to create a model of disk and envelope (Keto&Zhang 2010)#
# And would produce SPARX compatible HDF and VTK file used for visualization  #
###############################################################################


from tables import *
from numpy import *
from math import *
from scipy import optimize

disk=1
env=1
writevtk=1

# unit converter
Msun2MKS=(6.022E23/0.0028)*0.19889E+31/(100*0.14960E+12)**3
Au2MKS=100*0.14960E+12/(100*365.25*24*60*60)
Au2pc=100./206260
km2m=1e3
pc2m=30.857e15
pc2km=30.857e12
mean_molecular_mass = 2*1.67*1.67e-27 # kg

# resolution and domain size
R_out=0.05 #pc
R_in=26.*0.0046491/206260 #pc
stretch_ratior=1.02
stretch_ratiot=1.02
nr=64
nt=50
np=1

# Physical parameter
#parameters from Keto&Zhang
rho_e0=7.9e4 *1e6 # Envelope density at Rd (m^-3)
Rd_int=6900 # (AU)
Ap=5.1
Mt=10.7 # stellar mass (Msun)
Rt=26.*0.0046491/206260
p=-1
BT=15.0
vk= 1.2 # Keplerian velocity (km/s)

Rd=float(Rd_int)/206260. # Centrifugal Radius (pc)
rho_d0=Ap*rho_e0
H0=0.01*Rt
Tt=30000.
Mar = rho_e0*4.*pi*Rd*Rd*vk*(mean_molecular_mass*pc2m**2*km2m) # mass accretion rate (kg/s)
G=4.302e-3 # gravitational constant (pc Msun^-1 (km/s)^2)
sigma=5.67037321e-8 # Stefan-Boltzmann constant (W m^-2 K^-4)

X_mol=3e-8
X_mol2=3e-10
V_t=3000.
#kapp_d="powerlaw, 1.199e+12, 1.000e+04, 1.500e+00"
kapp_d="table,jena_bare_e6"
T_cmb=2.73
gas_to_dust=100.0
molec=""
geom='sph3d'
root="/"

if (disk==1 and env==1):
    vtkfilea='2Denv_disk_Rd'+str(Rd_int)+'.vtk'
    vtkfileb='2Denv_disk_vel_Rd'+str(Rd_int)+'.vtk'
elif(disk==0 and env==1):
    vtkfilea='2Denv_Rd'+str(Rd_int)+'.vtk'
    vtkfileb='2Denv_vel_Rd'+str(Rd_int)+'.vtk'
elif(disk==1 and env==0):
    vtkfilea='2Ddisk_Rd'+str(Rd_int)+'.vtk'
    vtkfileb='2Ddisk_vel_Rd'+str(Rd_int)+'.vtk'


def CubicEq(xx):
    global pp,qq
    return xx*xx*xx+pp*xx+qq



# Define a user record to characterize some kind of particles
class Particle(IsDescription):
    LEVEL=Int32Col(pos=0)
    POS=Int64Col(pos=1)
    geom=StringCol(itemsize=6,pos=2)
    X_max=Float64Col(shape=3,pos=3)
    X_min=Float64Col(shape=3,pos=4)
    X_cen=Float64Col(shape=3,pos=5)
    n_H2=Float64Col(pos=6)
    T_k=Float64Col(pos=7)
    X_mol=Float64Col(pos=8)
    X_pH2=Float64Col(pos=9)
    X_oH2=Float64Col(pos=10)
    X_e=Float64Col(pos=11)
    X_H=Float64Col(pos=12)
    X_He=Float64Col(pos=13)
    V_t=Float64Col(pos=14)
    V_edge=FloatCol(shape=(6,3),pos=15)
    V_cen=FloatCol(shape=3,pos=16)
    B_cen=FloatCol(shape=3,pos=17)
    ds=FloatCol(pos=18)
    NCHILDREN=Int64Col(pos=19)
    NAXES=Int64Col(shape=3,pos=20)
    T_d=Float64Col(pos=21)
    kapp_d=StringCol(itemsize=64,pos=22)
    T_ff=Float64Col(pos=23)
    kapp_ff=StringCol(itemsize=64,pos=24)
    T_bb=Float64Col(pos=25)

def writezone(direc,lev,position,xmax,xmin,naxes):
    # Create ZONE table
    table = h5file.createTable(direc, 'ZONE', Particle, "Grid table")
    particle = table.row
    particle['LEVEL']  = lev
    particle['POS'] = position
    particle['geom'] = geom
    particle['X_max'] =[ xmax[0],xmax[1],xmax[2] ]
    particle['X_min'] =[ xmin[0],xmin[1],xmin[2] ]
    particle['X_cen'] =[ 0.5*(xmin[0]+xmax[0]),0.5*(xmin[1]+xmax[1]),0.5*(xmin[2]+xmax[2]) ]
    particle['NCHILDREN'] =naxes[0]*naxes[1]*naxes[2]
    particle['NAXES'] =naxes
    #Insert a new particle record
    particle.append()
    table.flush()
    del table.attrs.FIELD_0_FILL
    del table.attrs.FIELD_1_FILL
    del table.attrs.FIELD_2_FILL
    del table.attrs.FIELD_3_FILL
    del table.attrs.FIELD_4_FILL
    del table.attrs.FIELD_5_FILL
    del table.attrs.FIELD_6_FILL
    del table.attrs.FIELD_7_FILL
    del table.attrs.FIELD_8_FILL
    del table.attrs.FIELD_9_FILL
    del table.attrs.FIELD_10_FILL
    del table.attrs.FIELD_11_FILL
    del table.attrs.FIELD_12_FILL
    del table.attrs.FIELD_13_FILL
    del table.attrs.FIELD_14_FILL
    del table.attrs.FIELD_15_FILL
    del table.attrs.FIELD_16_FILL
    del table.attrs.FIELD_17_FILL
    del table.attrs.FIELD_18_FILL
    del table.attrs.FIELD_19_FILL
    del table.attrs.FIELD_20_FILL
    del table.attrs.FIELD_21_FILL
    del table.attrs.FIELD_22_FILL
    del table.attrs.FIELD_23_FILL
    del table.attrs.FIELD_24_FILL
    del table.attrs.FIELD_25_FILL
    del table.attrs.NROWS

def writegrid(direc,lev,naxes,Raxis,Taxis,Paxis,nc):
    global pp,qq
    # Create GRID table
    table = h5file.createTable(direc, 'GRID', Particle, "Grid table")
    particle = table.row
    density=zeros(naxes)
    temperature=zeros(naxes)
    Vx=zeros(naxes)
    Vy=zeros(naxes)
    Vz=zeros(naxes)
    mass_env=0.
    mass_disc=0.
    total_volume = 0.

    for i in range(naxes[0]):
        for j in range(naxes[1]):
            for k in range(naxes[2]):
                # write a row of grid table
                particle['LEVEL']  = lev+1
                particle['POS'] = naxes[1]*naxes[2]*i+naxes[2]*j+k
                particle['geom'] = geom
                particle['X_max'] =[ Raxis[i+1],Taxis[j+1],Paxis[k+1] ]
                particle['X_min'] =[ Raxis[i]  ,Taxis[j]  ,Paxis[k]   ]
                particle['X_cen'] =[ 0.5*(Raxis[i]+Raxis[i+1]),0.5*(Taxis[j]+Taxis[j+1]),0.5*(Paxis[k]+Paxis[k+1]) ]
                # write out the non-empty-leaf zone
                r=particle['X_cen'][0]
                theta=particle['X_cen'][1]
                R=r*sin(theta)
                phi=particle['X_cen'][2]

                pp=r/Rd-1.
                qq=-cos(theta)*r/Rd

                cos_theta0 = optimize.brentq(CubicEq, -1.,1.)
                #if j == 25:
                #        print(cos_theta0)
                if (cos_theta0>1. or cos_theta0<-1.):
                    print(cos_theta0,pp,qq)

                volume = -2. * pi / 3. * ( Raxis[i+1]**3 - Raxis[i]**3 ) * ( cos(Taxis[j+1]) - cos(Taxis[j]) )
                total_volume = total_volume + volume

                if(env==1):
                    density_env = rho_e0 * ((r/Rd)**(-1.5))*((1+cos(theta)/cos_theta0)**(-0.5))*((1 + ((r/Rd)**(-1)) * (3*cos_theta0**2-1.0))**(-1))
                    mass_env += density_env*volume
                else:
                    density_env = 0.0

                if (r<=Rd and disk==1):
                    rho_0 = rho_d0*(Rd/R)**2.25
                    H=H0*(R/Rt)**1.25
                    density_disc = rho_0*exp(-(r*r-R*R)/(2.*H*H))
                    mass_disc += density_disc*volume
                else:
                    density_disc =0.

                density[i,j,k]=density_env+density_disc
                Vkep = sqrt(G*Mt/r)
                Vp_disc = sqrt(G*Mt/R)
                Vr_env = -Vkep*sqrt(1.+cos(theta)/cos_theta0)
                Vt_env = Vkep*((cos_theta0-cos(theta))/sin(theta))*sqrt(1.+cos(theta)/cos_theta0)
                Vp_env = Vkep*(sqrt(1.-cos_theta0*cos_theta0)/sin(theta))*sqrt(1.+cos(theta)/cos_theta0)

                if(density[i,j,k]!=0.0):
                    Vr = (density_env*Vr_env)/density[i,j,k]
                    Vt = (density_env*Vt_env)/density[i,j,k]
                    Vp = (density_env*Vp_env+density_disc*Vp_disc)/density[i,j,k]
                    T_env = Tt*(Rt/(2.*r))**(2./(4+p))

                    T_disc = BT * ( (3.*G*Mt*Mar/(4.*pi*pc2km*pc2km*R*R*R*sigma)) * (1.-sqrt(Rt/R)) )**0.25
                    temperature[i,j,k]=(density_disc*T_disc+density_env*T_env)/density[i,j,k]
                else:
                    Vr = 0.0
                    Vt = 0.0
                    Vp = 0.0
                    temperature[i,j,k] = 0.0

                if(writevtk):
                    Vx[i,j,k] = cos(phi)*sin(theta)*Vr + cos(phi)*cos(theta)*Vt -sin(phi)*Vp
                    Vy[i,j,k] = sin(phi)*sin(theta)*Vr + sin(phi)*cos(theta)*Vt +cos(phi)*Vp
                    Vz[i,j,k] = cos(theta)*Vr - sin(theta)*Vt


                particle['n_H2'] = density[i,j,k]
                particle['V_cen'] = [km2m*Vr,km2m*Vt,km2m*Vp]
                particle['T_k'] = temperature[i,j,k]
                if ( temperature[i,j,k] >= 90.0 ):
                    particle['X_mol'] = X_mol
                else:
                    particle['X_mol'] = X_mol2
                #particle['X_mol'] = X_mol
                particle['V_t'] = V_t
                particle['T_d'] = particle['T_k']
                particle['kapp_d'] = kapp_d
                nc=nc+1

                # Insert a new particle record
                particle.append()

        mass_env=mass_env*pc2m**3*mean_molecular_mass/0.19889E+31
        mass_disc=mass_disc*pc2m**3*mean_molecular_mass/0.19889E+31
        print('Total envelope mass =',mass_env,'(solar mass)')
        print('Total disc mass     =',mass_disc,'(solar mass)')
        print('Total mass          =',mass_env+mass_disc,'(solar mass)')
        print('Total volume          =',total_volume,'(pc^3)')
        if (writevtk):
            fvtk1=open(vtkfilea, mode = "w")
            print('# vtk DataFile Version 3.0', file=fvtk1)
            print('ENV_DISK', file=fvtk1)
            print('ASCII', file=fvtk1)
            print('DATASET STRUCTURED_GRID', file=fvtk1)
            print('DIMENSIONS %(0)d %(1)d %(2)d'%{'0':nr+1,'1':nt+1,'2':np+1}, file=fvtk1)
            print('POINTS %(0)d float'%{'0':(nr+1)*(nt+1)*(np+1)}, file=fvtk1)
            for k in range(np+1):
                for j in range(nt+1):
                    for i in range(nr+1):
                        if(k==0):
                            print('%(0)e %(1)d %(2)e'%{'0':Rp[i]*sin(thetap[j]),'1':0,'2':Rp[i]*cos(thetap[j])}, file=fvtk1)
                        elif(k==1):
                            print('%(0)e %(1)e %(2)e'%{'0':Rp[i]*sin(thetap[j]),'1':1e-6,'2':Rp[i]*cos(thetap[j])}, file=fvtk1)
            print('CELL_DATA %(0)d'%{'0':naxes[0]*naxes[1]*naxes[2]}, file=fvtk1)
            print('SCALARS density float 1', file=fvtk1)
            print('LOOKUP_TABLE default', file=fvtk1)

            text = ["{:8.2e}".format(density[i, j, k])
                    for i in range(naxes[0])
                    for j in range(naxes[1])
                    for k in range(naxes[2])]
            text = " ".join(text)
            print(text, file=fvtk1)

            print('SCALARS temperature float 1', file=fvtk1)
            print('LOOKUP_TABLE default', file=fvtk1)

            text = ["{:8.2e}".format(temperature[i, j, k])
                    for i in range(naxes[0])
                    for j in range(naxes[1])
                    for k in range(naxes[2])]
            text = " ".join(text)
            print(text, file=fvtk1)

            fvtk1.close()
            fvtk2=open(vtkfileb, mode = "w")
            print('# vtk DataFile Version 3.0', file=fvtk2)
            print('ENV_DISK', file=fvtk2)
            print('ASCII', file=fvtk2)
            print('DATASET STRUCTURED_GRID', file=fvtk2)
            print('DIMENSIONS %(0)d %(1)d %(2)d'%{'0':nr,'1':nt,'2':np}, file=fvtk2)
            print('POINTS %(0)d float'%{'0':nr*nt*np}, file=fvtk2)
            for j in range(nt):
                for i in range(nr):
                    print('%(0)e %(1)d %(2)e'%{'0':0.5*(Rp[i]+Rp[i+1])*sin(0.5*(thetap[j]+thetap[j+1])),'1':0,'2':Rp[i]*cos(thetap[j])}, file=fvtk2)
            print('POINT_DATA %(0)d'%{'0':naxes[0]*naxes[1]*naxes[2]}, file=fvtk2)
            print('VECTORS velocity float', file=fvtk2)
            for k in range(naxes[2]):
                for j in range(naxes[1]):
                    for i in range(naxes[0]):
                        print('%(0)e %(1)e %(2)e'%{'0':-Vx[i,j,k],'1':-Vy[i,j,k],'2':Vz[i,j,k]}, file=fvtk2)
            fvtk2.close()
            print("Wrote out",vtkfilea,vtkfileb)


    table.flush()
    del table.attrs.FIELD_0_FILL
    del table.attrs.FIELD_1_FILL
    del table.attrs.FIELD_2_FILL
    del table.attrs.FIELD_3_FILL
    del table.attrs.FIELD_4_FILL
    del table.attrs.FIELD_5_FILL
    del table.attrs.FIELD_6_FILL
    del table.attrs.FIELD_7_FILL
    del table.attrs.FIELD_8_FILL
    del table.attrs.FIELD_9_FILL
    del table.attrs.FIELD_10_FILL
    del table.attrs.FIELD_11_FILL
    del table.attrs.FIELD_12_FILL
    del table.attrs.FIELD_13_FILL
    del table.attrs.FIELD_14_FILL
    del table.attrs.FIELD_15_FILL
    del table.attrs.FIELD_16_FILL
    del table.attrs.FIELD_17_FILL
    del table.attrs.FIELD_18_FILL
    del table.attrs.FIELD_19_FILL
    del table.attrs.FIELD_20_FILL
    del table.attrs.FIELD_21_FILL
    del table.attrs.FIELD_22_FILL
    del table.attrs.FIELD_23_FILL
    del table.attrs.FIELD_24_FILL
    del table.attrs.FIELD_25_FILL
    del table.attrs.NROWS
    return nc



#### GRID GENERATION ####
# Coordinate : RADIUS points (streching)
r0 = (R_out-R_in)*(stretch_ratior-1.)/(stretch_ratior**(nr)-1.)
Rp = zeros(nr+1)
for i in range(nr+1):
    if (i==0):
        Rp[i]=R_in
        dr = r0
    else:
        Rp[i]=Rp[i-1]+dr
        dr=dr*stretch_ratior
# Coordinate : THETA points (streching)
t0 = 0.5*pi*(stretch_ratiot-1.)/(stretch_ratiot**(nt/2)-1.)
thetap = zeros(nt+1)
for j in range(nt+1):
    if (j==0):
        thetap[j]=0.0
        dt=t0*stretch_ratiot**(nt/2-1)
    elif (j<nt/2):
        thetap[j]=thetap[j-1]+dt
        dt=dt/stretch_ratiot
    elif (j==nt/2):
        thetap[j]=0.5*pi
        dt=t0
    elif (j>nt/2):
        thetap[j]=thetap[j-1]+dt
        dt=dt*stretch_ratiot
    elif (j==nt):
        thetap[j]=pi
# Coordinate : PHI points (phi symmetric, np=1)
phip = zeros(np+1)
phip[0]=0.0
phip[np]=2.0*pi
########################


filename = "model_env_disk"
h5file = openFile(filename, mode = "w", title = "Test file")
h5file.delNodeAttr("/", "TITLE", name=None)
h5file.delNodeAttr("/", "CLASS", name=None)
h5file.delNodeAttr("/", "VERSION", name=None)
h5file.delNodeAttr("/", "PYTABLES_FORMAT_VERSION", name=None)
h5file.setNodeAttr("/", "molec", molec, name=None)
h5file.setNodeAttr("/", "T_cmb", T_cmb, name=None)
h5file.setNodeAttr("/", "gas_to_dust", gas_to_dust, name=None)
h5file.setNodeAttr("/", "velfield", "grid ", name=None)
writezone(root,-1,0,[Rp[nr],thetap[nt],phip[np]],[Rp[0],thetap[0],phip[0]],[nr,nt,np])
ncell=writegrid(root,-1,[nr,nt,np],Rp,thetap,phip,0)
h5file.close()


print('Total cells=',ncell)



