#! /bin/env python
#
# Python Distutils setup script for SPARX


import os
import sys
import time
from subprocess import call, Popen, PIPE
from setuptools import setup, Extension

import numpy as np


### Setting
# Number of threads per job
ENABLE_MULTITREADING = True

if ENABLE_MULTITREADING:
    from multiprocessing import cpu_count

    NumberOfThread = 2 * cpu_count()
else:
    NumberOfThread = 1

print("Number of Threads per job = {:d}".format(NumberOfThread))


# Verify MPI support by running mpicc
dir_tmp = os.path.join("unit_tests", "tmp")

if not os.path.exists(dir_tmp):
    os.makedirs(dir_tmp)

fn_test_in  = os.path.join("src", "mpi-test.c")
fn_test_out = os.path.join(dir_tmp, "a.out")

cmd      = "mpicc {} -o {}".format(fn_test_in, fn_test_out)
HAVE_MPI = call(cmd, shell=True, stdout=PIPE, stderr=PIPE) == 0

if os.path.isfile(fn_test_out):
    os.system("rm {}".format(fn_test_out))


# Get svn revision and update version
with open("pyproject.toml", "r") as f:
    for line in f:
        if "version =" in line:
            SPARX_VER = line.split()[-1].strip("\"")

p   = Popen("svnversion", shell=True, stdout=PIPE)
REV = p.communicate()[0].strip()

fn_out = os.path.join("lib", "sparx", "VERSION")

with open(fn_out, "w") as f:
    text = "{:s} (r{:s}, {:s})".format(SPARX_VER, str(REV), time.asctime())
    f.write(text)



### Gather information for setting up the package
# Python path
PY_INC = os.path.join(sys.prefix, "include")
PY_LIB = os.path.join(sys.prefix, "lib")

assert os.path.exists(PY_INC), "Cannot locate Python include directory: {}".format(PY_INC)
assert os.path.exists(PY_LIB), "Cannot locate Python library directory: {}".format(PY_LIB)


# Numpy path
NUMPY_INC = np.get_include()


# Check whether MIRIAD is supported and get the path
if os.environ.get("MIRLIB") is not None:
    MIRSUPPORT = True
else:
    MIRSUPPORT = False

if MIRSUPPORT:
    MIR_INC = os.getenv("MIRINC")
    MIR_LIB = os.getenv("MIRLIB")

    assert MIR_INC and MIR_LIB, \
        "MIRIAD environment variables not present, cannot locate Miriad headers or libraries"

    MIR_INC  = os.path.realpath(MIR_INC)
    MIR_INC1 = os.path.join(MIR_INC, "..", "pgplot-miriad-remix")
    MIR_INC2 = os.path.join(MIR_INC, "..", "miriad-c")

    assert os.path.exists(MIR_INC1), "MIRIAD include path not present, cannot continue: {}".format(MIR_INC1)
    assert os.path.exists(MIR_INC2), "MIRIAD include path not present, cannot continue: }".format(MIR_INC2)


# Check for additional search paths specified by user
SPARXVERSION  = "sparx"
SPARX_VERSION = "sparx"

USER_INC = list()
USER_LIB = list()
ARGS     = list()
MPI_LIB  = ["mpi"]

for arg in sys.argv[:]:
    if "--with-include=" in arg:
        path = arg.rsplit("=")[-1]
        path = os.path.expanduser(path)
        USER_INC.append(path)

    elif "--with-lib=" in arg:
        path = arg.rsplit("=")[-1]
        path = os.path.expanduser(path)
        USER_LIB.append(path)

    elif "--no-mpi" in arg:
        HAVE_MPI = False

    elif "--lam" in arg:
        MPI_LIB = ["lammpio", "mpi", "lam"]

    elif "--mpich" in arg:
        MPI_LIB = ["mpich", "pgc", "pgftnrtl", "pgftnrtl", "nspgc", "pgc", "rt"]

    elif "--version" in arg:
        path = arg.rsplit("=")[-1]
        path = os.path.expanduser(path)

        SPARXVERSION  += "-{}".format(path)
        SPARX_VERSION += "_{}".format(path)

    else:
        ARGS.append(arg)

sys.argv = ARGS


### Specify compilation macros, headers, flags, etc.
if not HAVE_MPI:
    print("\n\n\nNO MPI SUPPORT!\n\n\n")
else:
    print("\n\n\nMPI support available\n\n\n")


# Macros
macros = [
    ("NumberOfThread", str(NumberOfThread)),
    ("MIRSUPPORT", MIRSUPPORT),
    ("SPARXVERSION", "\"{}\"".format(SPARXVERSION)),
    ("SPARX_VERSION", "\"{}\"".format(SPARX_VERSION)),
]


# Compiler flags
compiler_flags = [
    "-std=c99",
#    "-pedantic",
    "-fshort-enums",
    "-fno-common",
    "-Dinline=",
    "-g",
    "-rdynamic",
    "-O3",
    "-pthread",
#    "-Werror",
    "-Wall",
#    "-W",
    "-Wmissing-prototypes",
    "-Wstrict-prototypes",
    "-Wpointer-arith",
    "-Wcast-qual",
    "-Wcast-align",
    "-Wwrite-strings",
    "-Wnested-externs",
#    "-finline-limit=600",
#    "-fwhole-program",
    "-ftree-vectorize",
]


# Include directory
include_dirs  = ["src", PY_INC, NUMPY_INC]
include_dirs += USER_INC

if MIRSUPPORT:
    include_dirs.append(MIR_INC1)
    include_dirs.append(MIR_INC2)


# Library directory
library_dirs  = [PY_LIB]
library_dirs += USER_LIB

if MIRSUPPORT:
    library_dirs.append(MIR_LIB)


# Libraries to link to
libs = [
    "X11",
    "m",
    "gsl",
    "gslcblas",
    "fftw3",
    "hdf5",
    "hdf5_hl",
    "cfitsio"
]

if MIRSUPPORT:
    libs += [
        "cpgplot",
        "pgplot",
        "mir",
        "mir_uvio",
        "mir_linpack"
    ]


# Base source files
sources_base = [
    "src/data_structs.c",
    "src/debug.c",
    "src/error.c",
    "src/geometry.c",
    "src/kappa.c",
    "src/memory.c",
    "src/molec.c",
    "src/numerical.c",
    "src/physics.c",
    "src/python-wrappers.c",
    "src/zone.c",
    "src/zone-hdf5.c",
    "src/fits-and-miriad-wrappers.c",
    "src/vtk-wrapper.c",
]

if MIRSUPPORT:
    sources_base.append("src/cpgplot-wrappers.c")


# Base dependencies
depends_base = [
    "src/data_structs.h",
    "src/debug.h",
    "src/error.h",
    "src/geometry.h",
    "src/kappa.h",
    "src/memory.h",
    "src/fits-and-miriad-wrappers.h",
    "src/molec.h",
    "src/numerical.h",
    "src/physics.h",
    "src/python-wrappers.h",
    "src/zone.h",
    "src/zone-hdf5.h",
    "src/vtk-wrapper.h",
]

if MIRSUPPORT:
    depends_base.append("src/cpgplot-wrappers.h")


# SPARX sources files
sources_sparx = [
    "src/sparx-python.c",
#    "src/sparx-test.c",
    "src/sparx-model.c",
    "src/sparx-physics.c",
    "src/sparx-inputs.c",
    "src/sparx-io.c",
    "src/sparx-utils.c",
    "src/sparx-ImageTracing.c",
]


# SPARX dependencies
depends_sparx = ["src/sparx.h"]



### Distutils setup
sources = sources_base \
        + sources_sparx \
        + [
    "src/sparx-pyext-_sparx.c",
    "src/sparx-task-amc.c",
    "src/sparx-task-telsim.c",
    "src/sparx-task-contobs.c",
    "src/sparx-task-coldens.c",
    "src/sparx-task-visual.c",
    "src/sparx-task-pops2ascii.c",
#    "src/sparx-task-pygrid.c",
    "src/sparx-task-template.c",
]

depends = ["setup.py"] + depends_base + depends_sparx

# Things to include if MPI is available
if HAVE_MPI:
    macros.append(("HAVE_MPI", None))
    libs += MPI_LIB


# Definition for the _sparx extension module
ext_sparx = Extension("{}._sparx".format(SPARX_VERSION),
                      sources = sources,
                      depends = depends,
                      extra_compile_args = compiler_flags,
                      define_macros = macros,
                      include_dirs = include_dirs,
                      library_dirs = library_dirs,
                      libraries = libs)


# The main setup call
setup(
    name = "sparx",
    url = "https://github.com/itahsieh/sparx-alpha",
    ext_modules = [ext_sparx],
    package_data = { SPARX_VERSION : ["data/molec/*.dat",   # Molecular data files
                                      "data/opacity/*.tab", # Opacity data files
                                      "VERSION",            # Program version
                                     ]
                   },
    scripts = ["bin/presparx",                 # SPARX preprocessor
               "bin/sparx",                    # Main sparx command line driver
               "bin/sparx-plot",               # Model plotter
               "bin/sparx-plot.py",            # Model plotter
               "bin/sparx-validate-dust.py",   # Script for validating dust radiative transfer
               "bin/sparx-validate-line.py",   # Script for validating line radiative transfer
               "bin/sparx-validate-leiden.py", # Script for validating with the Leiden 2004 benchmark problems
              ],
    zip_safe=False
)
