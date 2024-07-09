#! /bin/bash
#
# Usage:
#   1. Configure the paths to the required software
#      --> C compiler (required)
#          MPI compiler (optional, for parallel execution)
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

### set the environment variables
CCLIB=$GCC_DIR/lib64
MPI_DIR=$OPENMPI_DIR
HDF5_DIR=$HDF5_DIR
FFTW_DIR=$FFTW_DIR
GSL_DIR=/tiara/home/hfhsieh/opt/gsl_2.8
CFITSIO_DIR=$CFITSIO_DIR
PGPLOT_DIR=/tiara/home/hfhsieh/opt/pgplot


### generate setup.py
python3 configure.py \
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
