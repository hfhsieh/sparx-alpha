#! /bin/env python
#
# A configuration script to obtain build parameters from the user
# and dynamically generate setup.py


import os
import sys
import re
from argparse import ArgumentParser

import numpy as np


### default environments
macros = [
    ("SPARXVERSION",  "'\"{}\"'".format("sparx")),
    ("SPARX_VERSION", "'\"{}\"'".format("sparx"))
]

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
    "-Wall",
    "-Wmissing-prototypes",
    "-Wstrict-prototypes",
    "-Wpointer-arith",
    "-Wcast-qual",
    "-Wcast-align",
    "-Wwrite-strings",
    "-Wnested-externs",
    "-ftree-vectorize",
    "-fPIC"
]

include_paths = [
    "src",
    "/usr/include"
]

library_paths = [
    "/usr/lib",
    "/usr/lib64"
]

libs = [
    "X11",
    "m",
    "gsl",
    "gslcblas",
    "fftw3",
    "hdf5",
    "hdf5_hl",
    "cfitsio",
    "gfortran"
]

sources = [
##   base source files
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
##   SPARX related
    "src/sparx-python.c",
#    "src/sparx-test.c",
    "src/sparx-model.c",
    "src/sparx-physics.c",
    "src/sparx-inputs.c",
    "src/sparx-io.c",
    "src/sparx-utils.c",
    "src/sparx-ImageTracing.c",
##   SPARX tasks
    "src/sparx-pyext-_sparx.c",
    "src/sparx-task-amc.c",
    "src/sparx-task-telsim.c",
    "src/sparx-task-contobs.c",
    "src/sparx-task-coldens.c",
    "src/sparx-task-visual.c",
    "src/sparx-task-pops2ascii.c",
#    "src/sparx-task-pygrid.c",
    "src/sparx-task-template.c"
]

headers = [
##   base header files
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
##   SPARX related
    "src/sparx.h"
]


### parser
parser = ArgumentParser(description = "Configuration script for generating setup.py")

parser.add_argument("--cc-lib",      default = "", help = "Path to the compiler library directory")

parser.add_argument("--mpi",         default = "", help = "Path to the MPI directory")
parser.add_argument("--mpi-inc",     default = "", help = "Path to the MPI include directory")
parser.add_argument("--mpi-lib",     default = "", help = "Path to the MPI library directory")

parser.add_argument("--hdf5",        default = "", help = "Path to the HDF5 directory")
parser.add_argument("--hdf5-inc",    default = "", help = "Path to the HDF5 include directory")
parser.add_argument("--hdf5-lib",    default = "", help = "Path to the HDF5 library directory")

parser.add_argument("--fftw",        default = "", help = "Path to the FFTW directory")
parser.add_argument("--fftw-inc",    default = "", help = "Path to the FFTW include directory")
parser.add_argument("--fftw-lib",    default = "", help = "Path to the FFTW library directory")

parser.add_argument("--gsl",         default = "", help = "Path to the GSL directory")
parser.add_argument("--gsl-inc",     default = "", help = "Path to the GSL include directory")
parser.add_argument("--gsl-lib",     default = "", help = "Path to the GSL library directory")

parser.add_argument("--cfitsio",     default = "", help = "Path to the CFITSIO directory")
parser.add_argument("--cfitsio-inc", default = "", help = "Path to the CFITSIO include directory")
parser.add_argument("--cfitsio-lib", default = "", help = "Path to the CFITSIO library directory")

parser.add_argument("--pgplot",      default = "", help = "Path to the PGPLOT directory")
parser.add_argument("--pgplot-inc",  default = "", help = "Path to the PGPLOT include directory")
parser.add_argument("--pgplot-lib",  default = "", help = "Path to the PGPLOT library directory")

parser.add_argument("--miriad",      default = "", help = "Path to the MIRIAD directory")
parser.add_argument("--miriad-inc",  default = "", help = "Path to the MIRIAD include directory")
parser.add_argument("--miriad-lib",  default = "", help = "Path to the MIRIAD library directory")

if len(sys.argv) == 1:
    print("Warning: No additional include and library paths specified")
else:
    args = parser.parse_args()


# update the include and library paths based on the specified arguments
def _update_path(keyword):
    # assume the include and library directories are call "include" and "lib", respectively
    cmd_template = """
if args.{keyword}:
    if not args.{keyword}_inc:
        args.{keyword}_inc = os.path.join(args.{keyword}, "include")

    if not args.{keyword}_lib:
        args.{keyword}_lib = os.path.join(args.{keyword}, "lib")
"""

    cmd = cmd_template.format(keyword = keyword)
    exec(cmd)


for key in ["mpi", "hdf5", "fftw", "gsl", "cfitsio", "pgplot", "miriad"]:
    _update_path(key)


### update the include and library paths
# enviornment variables
LD_LIBRARY_PATH = os.getenv("LD_LIBRARY_PATH")
library_paths += LD_LIBRARY_PATH.split(":")

# Python and Numpy
python_inc = os.path.join(sys.prefix, "include")
python_lib = os.path.join(sys.prefix, "lib")
numpy_inc  = np.get_include()

include_paths += [python_inc, numpy_inc]
library_paths += [python_lib]

# C compiler
if args.cc_lib:
    library_paths += [args.cc_lib]

# MPI
if args.mpi_inc and args.mpi_lib :
    macros        += [("HAVE_MPI", None)]
    libs          += ["mpi"]
    include_paths += [args.mpi_inc]
    library_paths += [args.mpi_lib]

# HDF5
if args.hdf5_inc and args.hdf5_lib:
    include_paths += [args.hdf5_inc]
    library_paths += [args.hdf5_lib]

# FFTW
if args.fftw_inc and args.fftw_lib:
    include_paths += [args.fftw_inc]
    library_paths += [args.fftw_lib]

# GSL
if args.gsl_inc and args.gsl_lib:
    include_paths += [args.gsl_inc]
    library_paths += [args.gsl_lib]

# CFITSIO
if args.cfitsio_inc and args.cfitsio_lib:
    include_paths += [args.cfitsio_inc]
    library_paths += [args.cfitsio_lib]

# MIRIAD
if args.miriad_inc and args.miriad_lib:
    macros        += [("MIRSUPPORT", 1)]
    libs          += ["cpgplot", "pgplot", "mir", "linpack"]
    include_paths += [args.miriad_inc]
    library_paths += [args.miriad_lib]
    sources       += ["src/cpgplot-wrappers.c"]
    headers       += ["src/cpgplot-wrappers.h"]

    # PGPLOT
    if args.pgplot_inc:
        include_paths += [args.pgplot_inc]
    else:
        raise ValueError ("No include path of PGPLOT specified")

    if args.pgplot_lib:
        library_paths += [args.pgplot_lib]
    else:
        raise ValueError ("No library path of PGPLOT specified")

else:
    macros += [("MIRSUPPORT", 0)]


# remove duplicate library paths that are included in LD_LIBRARY_PATH
library_paths = list(set(library_paths))

# reverse the order so that user-defined paths have higher priority
include_paths = include_paths[::-1]
library_paths = library_paths[::-1]


### generate the version.py
version_pattern = r"^version\s*=\s*['\"]([^'\"]*)['\"]"

with open("pyproject.toml", "r") as f:
    version = re.search(version_pattern, f.read(), re.M)

if version:
    fn_version = os.path.join("lib", "sparx", "version.py")

    with open(fn_version, "w") as f:
        f.write("__version__ = \"{}\"".format(version.group(1)))
else:
    raise RuntimeError ("Unable to find version string in pyproject.toml")


### generate setup.py
setup_prologue = """#! /bin/env python
#

from setuptools import setup, Extension

"""


setup_ext_fmt = """
ext_sparx = Extension("sparx._sparx",
                      sources = [{SRC}],
                      depends = [{HEADER}],
                      extra_compile_args = [{CFLAG}],
                      define_macros = [{MACRO}],
                      include_dirs = [{INCPATH}],
                      library_dirs = [{LIBPATH}],
                      libraries = [{LIB}])

"""

setup_install = """
setup(
    ext_modules = [ext_sparx],
    package_data = { "sparx" : ["data/molec/*.dat",   # Molecular data files
                                "data/opacity/*.tab", # Opacity data files
                                "VERSION",            # Program version
                               ]
                   },
    url = "https://sparx.tiara.sinica.edu.tw",
    scripts = ["bin/presparx", # SPARX preprocessor
               "bin/sparx",    # Main sparx command line driver
              ]
)

"""


setup_ext = setup_ext_fmt.format(
    SRC      = ", ".join(["\"{}\"".format(i)  for i in sources]),
    HEADER   = ", ".join(["\"{}\"".format(i)  for i in headers]),
    CFLAG    = ", ".join(["\"{}\"".format(i)  for i in compiler_flags]),
    INCPATH  = ", ".join(["\"{}\"".format(i)  for i in include_paths]),
    LIBPATH  = ", ".join(["\"{}\"".format(i)  for i in library_paths]),
    LIB      = ", ".join(["\"{}\"".format(i)  for i in libs]),
#    MACRO    = ", ".join(["('{}', '{}')".format(str(key), str(val))  for key, val in macros])
    MACRO    = ", ".join(["(\"{}\", {})".format(str(key), str(val))  for key, val in macros])
)


with open("setup.py", "w") as f:
    f.write(setup_prologue)
    f.write(setup_ext)
    f.write(setup_install)
