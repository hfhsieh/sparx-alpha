#! /bin/bash
#
# Usage:
#   1. Configure the paths to the required software
#      --> C compiler (required)
#          MPI compiler (optional, for paralle execution)
#          HDF5 (required)
#          FFTW3 (required)
#          GSL (required, for generating random number)
#          CFITSIO (required)
#          MIRIAD (optional)
#          PGPLOT (required if MIRIAD is enabled)
#   2. For software "X", one can specify the main directory via "X_DIR".
#      The include and library paths will be automatically generated,
#      assuming they are located in the 'include' and 'lib' subdirectories, respectively.
#
#      If this is not the case, use 'X_INC' and 'X_LIB' to specify them manually.
#

### setting the environment variables
## XL
#MPI_DIR=/cluster/gcc-4.8.5/openmpi-4.1.2
#HDF5_DIR=/home/hfhsieh/miniconda3/envs/py39
#FFTW_DIR=/cluster/gcc-4.8.5/fftw-3.3.10_openmpi4
##GSL_DIR=/home/hfhsieh/opt/gsl
#CFITSIO_DIR=/home/hfhsieh/opt/cfitsio

## KAWAS
#MPI_DIR=$OPENMPI_DIR
#HDF5_DIR=$HDF5_DIR
#FFTW_DIR=$FFTW_DIR
#GSL_DIR=/tiara/home/hfhsieh/opt/gsl_2.8
#CFITSIO_DIR=$CFITSIO_DIR
#PGPLOT_DIR=$PGPLOT_DIR

## NCTS
CC_LIB=/cluster/gcc-11.2.0/gcc/lib64
MPI_DIR=/cluster/gcc-11.2.0/openmpi-4.1.2
HDF5_DIR=/home/hfhsieh/miniconda3/envs/py39
FFTW_DIR=/cluster/gcc-11.2.0/fftw-3.3.10_openmpi4
GSL_DIR=/home/hfhsieh/opt/gsl
CFITSIO_DIR=/home/hfhsieh/opt/cfitsio
PGPLOT_DIR=/home/hfhsieh/opt/pgplot
#MIR_INC=/home/hfhsieh/src/miriad/inc
#MIR_LIB=/home/hfhsieh/src/miriad/linux64/lib


### generate setup.py
python configure.py \
--cc-lib=$CCLIB \
--mpi=$MPI_DIR \
--hdf5=$HDF5_DIR \
--fftw=$FFTW_DIR \
--gsl=$GSL_DIR \
--cfitsio=$CFITSIO_DIR \
--pgplot-inc=$PGPLOT_DIR \
--pgplot-lib=$PGPLOT_DIR \
--miriad-inc=$MIRINC \
--miriad-lib=$MIRLIB


### installation
rm -rf build
pip3 install . --user
