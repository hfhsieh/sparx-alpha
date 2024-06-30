# Model Type : Function / Constant / TABLE / ZEUS
ModelType = 'user_defined'

# Molecule
molec = 'hco+'

# CMB temperature (Kelvin, outer B.C.)
T_cmb = 2.73

# inner Boundary condition
T_in = 0.0

n_H2 = [
2.548344E+11, 2.356551E+11, 2.179171E+11, 2.015157E+11, 1.863490E+11, 1.723241E+11,
1.593541E+11, 1.473597E+11, 1.362689E+11, 1.260124E+11, 1.165283E+11, 1.077577E+11,
9.964752E+10, 9.214758E+10, 8.521217E+10, 7.879855E+10, 7.286777E+10, 6.738348E+10,
6.231184E+10, 5.762191E+10, 5.328508E+10, 4.927460E+10, 4.556591E+10, 4.213643E+10,
3.896503E+10, 3.603232E+10, 3.332036E+10, 3.081251E+10, 2.849341E+10, 2.634885E+10,
2.262470E+10, 1.881360E+10, 1.602180E+10, 1.387110E+10, 1.185840E+10, 1.010000E+10,
8.648850E+09, 7.395170E+09, 6.319050E+09, 5.402330E+09, 4.617710E+09, 3.946950E+09,
3.373380E+09, 2.882940E+09, 2.463690E+09, 2.105340E+09, 1.799070E+09, 1.537290E+09,
1.313610E+09, 1.122970E+09]

T_k = [
1.890000E+01, 1.836352E+01, 1.784226E+01, 1.733580E+01, 1.684372E+01, 1.636560E+01,
1.590106E+01, 1.544970E+01, 1.501115E+01, 1.458505E+01, 1.417105E+01, 1.376880E+01,
1.339650E+01, 1.309480E+01, 1.284920E+01, 1.263430E+01, 1.244060E+01, 1.226860E+01,
1.211470E+01, 1.196620E+01, 1.182410E+01, 1.173050E+01, 1.164030E+01, 1.153480E+01,
1.140280E+01, 1.141230E+01, 1.129260E+01, 1.129980E+01, 1.119581E+01, 1.109880E+01,
1.110150E+01, 1.122620E+01, 1.128450E+01, 1.130700E+01, 1.135870E+01, 1.147290E+01,
1.160570E+01, 1.167560E+01, 1.180180E+01, 1.199910E+01, 1.213550E+01, 1.227160E+01,
1.244650E+01, 1.262950E+01, 1.278760E+01, 1.304070E+01, 1.316610E+01, 1.344790E+01,
1.361030E+01, 1.390000E+01]

Vr = [
-7.659916E+02,-7.274061E+02,-6.896902E+02,-6.528437E+02,-6.168665E+02,-5.817588E+02,
-5.475205E+02,-5.141516E+02,-4.816521E+02,-4.500222E+02,-4.192615E+02,-3.893703E+02,
-3.603486E+02,-3.321962E+02,-3.049133E+02,-2.784998E+02,-2.529557E+02,-2.282811E+02,
-2.044758E+02,-1.815400E+02,-1.594736E+02,-1.382767E+02,-1.179491E+02,-9.849095E+01,
-7.990225E+01,-6.218296E+01,-4.533308E+01,-2.935264E+01,-1.424161E+01, 0.000000E+00,
0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00,
0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00,
0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00, 0.000000E+00,
0.000000E+00, 0.000000E+00]

Vt = [
1.590000E+02, 1.583720E+02, 1.576660E+02, 1.568800E+02, 1.560160E+02, 1.550770E+02,
1.540750E+02, 1.530300E+02, 1.519720E+02, 1.509490E+02, 1.500280E+02, 1.492890E+02,
1.487420E+02, 1.483550E+02, 1.480620E+02, 1.477610E+02, 1.473860E+02, 1.468940E+02,
1.463170E+02, 1.459610E+02, 1.459890E+02, 1.459750E+02, 1.461140E+02, 1.452810E+02,
1.449930E+02, 1.449940E+02, 1.450000E+02, 1.450000E+02, 1.450000E+02, 1.450000E+02,
1.450020E+02, 1.449990E+02, 1.449930E+02, 1.450080E+02, 1.450260E+02, 1.449240E+02,
1.450270E+02, 1.458040E+02, 1.461190E+02, 1.458800E+02, 1.463480E+02, 1.471000E+02,
1.469980E+02, 1.468980E+02, 1.479300E+02, 1.479680E+02, 1.480280E+02, 1.483530E+02,
1.489640E+02, 1.500000E+02]

dust_to_gas = [
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
0.01, 0.01]

X_mol = [
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9, 1E-9, 1E-9, 1E-9, 1E-9,
1E-9, 1E-9]

kapp_d = "table,jena_thin_e5"
