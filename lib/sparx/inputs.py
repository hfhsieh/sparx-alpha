##
## This module handles most things related to sparx inputs
##

# Some necessary imports
from sparx import MOLEC_LIST
from sparx.grid import GEOM_DICT
from sparx.physics import Const as C, Units as U
from sparx.utils import MPI_RANK, MPI_SIZE
from sys import maxint, modules
from os.path import exists

##
## Global Inputs dictionary
##
INP_DICT = {}

##
## Reset inputs
##
def reset_inputs():
	INP_DICT.clear()
	return

##
## Recursive inputs convertor
##
def convert_input(format, input):
	# This function recursively converts input according to format,
	# which may be a list of types. e.g. [Angle, Length, Velo]
	if type(format) is list:
		# List type, build list
		value = []
		n = len(format)
		if n == 1:
			for i in range(len(input)):
				value.append(convert_input(format[0], input[i]))
		elif n > 1:
			for i in range(n):
				value.append(convert_input(format[i], input[i]))
		else:
			raise Exception, "Length of format list is 0"
	else:
		value = format(input)
	return value

##
## Master type class
##
class KeyType:
	# This class is only meant to be inherited
	pass

##
## Physical values with units
##
class PhysVal(KeyType):
	def __init__(self, name, unit, **convs):
		self.name = name
		self.pattern = "([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]*\.?[0-9]+)?)([a-zA-Z][-+0-9a-zA-Z^]*)"
		self.unit = unit
		self.convs = {}
		for key in convs:
			self.convs[key] = convs[key]

	def __call__(self, string):
		if type(string) is not str:
			raise Exception, "Input value '%s' should be value-unit pair" % string

		from re import match
		# Try to match input to pattern
		m = match(self.pattern, string)
		if m is None:
			raise Exception, "Input value '%s' should be value-unit pair" % string
		else:
			# groups()[0] is number
			# groups()[1] is exponent
			# groups()[2] is unit
			value = float(m.groups()[0])
			unit = m.groups()[2]
			if len(unit) > 0:
				# arg contains unit, see if it is understandable
				if unit in self.convs:
					# Convert to appropriate value
					value *= self.convs[unit]
				else:
					raise Exception, "'%s' is not a valid unit for type '%s'" % (unit, self.name)
			return value

	def __repr__(self):
		return self.name

class Generic(KeyType):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name

class ClassInteger(Generic):
	def __call__(self, arg):
		value = int(arg)
		return value

	__doc__ = "Integers in the range [%d, %d]"%(-maxint, maxint)

class ClassPosInt(Generic):
	def __call__(self, arg):
		value = int(arg)
		if value <= 0:
			raise Exception, "Values must be > 0"
		return value

	__doc__ = "Positive integers in the range [1, %d]"%maxint

class ClassIndex(Generic):
	def __call__(self, arg):
		value = int(arg)
		if value < 0:
			raise Exception, "Values must be >= 0"
		return value

	__doc__ = "Integers in the range [0, %d]"%maxint

class ClassFloat(Generic):
	def __call__(self, arg):
		value = float(arg)
		return value

	__doc__ = "Floating point values in the range (-inf, inf)"

class ClassPosFlt(Generic):
	def __call__(self, arg):
		value = float(arg)
		if value <= 0:
			raise Exception, "Values must be > 0"
		return value

	__doc__ = "Positive floating point values in the range (0, inf)"

class ClassFraction(Generic):
	def __call__(self, arg):
		value = float(arg)
		if value < 0.0 or value > 1.0:
			raise Exception, "Values must be >= 0 and <= 1"
		return value

	__doc__ = "Floating point values in the range [0.0, 1.0]"

class ClassNewFile(Generic):
	def __call__(self, arg):
		'''If arg exists as a file, raise an exception, otherwise return
		arg as a string'''
		if MPI_RANK == 0 and exists(arg):
			raise Exception, "File '%s' already exists" % arg
		else:
			return arg

	__doc__ = "Filename of a new (non-existing) file"

class ClassOldFile(Generic):
	def __call__(self, arg):
		if not exists(arg):
			raise Exception, "File '%s' does not exist" % arg
		else:
			return arg

	__doc__ = "Filename of an existing file"

class ClassMolec(Generic):
	def __call__(self, arg):
		if arg in MOLEC_LIST:
			return arg
		else:
			raise Exception, "Molecular data for '%s' is not available. Try one of the following:\n"%arg+\
					 ", ".join(["'%s'"%i for i in MOLEC_LIST])

class ClassGeom(Generic):
	def __call__(self, arg):
		if arg in GEOM_DICT:
			return arg
		else:
			raise Exception, "'%s' is not a valid coordinate system"

	__doc__ = "Coordinate system of the model, valid options are:\n"+\
		  "\n".join(["  %s"%i for i in GEOM_DICT])

class ClassPowerLaw:
	# y = y0 * (x / x0)**p
	def __init__(self, name, x0f, y0f, pf):
		self.name = str(name)
		self.x0f = x0f
		self.y0f = y0f
		self.pf = pf
		self.__doc__ = \
		"A powerlaw of the form\n\n"+\
		"    y = y0 * (x / x0)**p\n\n"+\
		"which must be specified as\n"+\
		"  [x0, y0, p]\n"+\
		"with units of\n"+\
		"  [%s, %s, %s]"%(str(self.x0f), str(self.y0f), str(pf))

	def __call__(self, arg):
		value = eval(arg)
		x0 = self.x0f(value[0])
		y0 = self.y0f(value[1])
		p = self.pf(value[2])
		return "powerlaw,%10.3e,%10.3e,%10.3e" % (x0, y0, p)

	def __repr__(self):
		return repr(self.format)

class ClassBool(Generic):
	def __call__(self, arg):
		return bool(eval(arg))

	__doc__ = """Boolean truth value (True or False)"""

##
## Type container
##
class Type:
	# Various angular units in radians
	Angle = PhysVal("Angle", "rad")
	Angle.convs = {
		'asec': C.pi / (180.0 * 60.0 * 60.0),
		'amin': C.pi / (180.0 * 60.0),
		'deg': C.pi / 180.0,
		'rad': 1.0,
		'pi': C.pi
	}

	# Various velocity units in m/s
	Velo = PhysVal("Velo", "ms^-1")
	Velo.convs = {
		'cms^-1': 1.0e-2,
		'ms^-1': 1.0,
		'kms^-1': 1.0e3,
		'c': C.c,
	}

	# Length units in meters
	Length = PhysVal("Length", "m")
	Length.convs = {
		'A': 1.0e-10,
		'nm': 1.0e-9,
		'um': 1.0e-6,
		'mm': 1.0e-3,
		'cm': 1.0e-2,
		'm': 1.0,
		'km': 1.0e3,
		'Rearth': U.Rearth,
		'Rsun': U.Rsun,
		'au': U.au,
		'ly': 9.4605284e15,
		'pc': U.pc,
		'kpc': U.pc * 1.0e3,
		'Mpc': U.pc * 1.0e6,
		'Gpc': U.pc * 1.0e9
	}

	# Mass units in kg
	Mass = PhysVal("Mass", "kg")
	Mass.convs = {
		'amu': U.amu,
		'me': C.me,
		'mp': C.mp,
		'g': 1.0e-3,
		'kg': 1.0,
		'Msun': U.Msun,
	}



	# Number density units in m^-3
	NumDens = PhysVal("NumDens", "m^-3")
	NumDens.convs = {
		'cm^-3': 1.0e6,
		'm^-3': 1.0
	}

	# Number density units in m^-3
	Temp = PhysVal("Temp", "K")
	Temp.convs = {
		'K': 1.0
	}

	# Frequency units in Hz
	Freq = PhysVal("Freq", "Hz")
	Freq.convs = {
		'Hz': 1.0,
		'kHz': 1.0e3,
		'MHz': 1.0e6,
		'GHz': 1.0e9,
		'THz': 1.0e12
	}

	# Time units in s
	Time = PhysVal("Time", "s")
	Time.convs = {
		'ns': 1.0e-9,
		'us': 1.0e-6,
		'ms': 1.0e-3,
		's': 1.0,
		'm': U.minute,
		'h': U.hour,
		'day': U.day,
		'yr': U.year,
		'Myr': 1e6 * U.year,
		'Gyr': 1e9 * U.year
	}

	# Opacity units in m^2 kg^-1
	Opacity = PhysVal('Opacity', "m^2kg^-1")
	Opacity.convs = {
		'cm^2g^-1': 0.1,
		'm^2kg^-1': 1.0,
	}

	# Luminosity in Js^-1
	Luminosity = PhysVal('Luminosity', "Js^-1")
	Luminosity.convs = {
		'Js^-1': 1.0,
		'Lsun': U.L_sun
	}

	### Generic types ###
	# Integer type
	Integer = ClassInteger("Integer")

	# Positive integer type
	PosInt = ClassPosInt("PosInt")

	# Index type
	Index = ClassIndex("Index")

	# Floating point type
	Float = ClassFloat("Float")

	# Powerlaw Index type
	PwrIndex = ClassFloat("PwrIndex")

	# Positive floating point type
	PosFlt = ClassPosFlt("PosFlt")

	# Fraction type
	Fraction = ClassFraction("Fraction")

	# NewFile type
	NewFile = ClassNewFile("NewFile")

	# OldFile type
	OldFile = ClassOldFile("OldFile")

	# Molec type
	Molec = ClassMolec("Molec")

	# Geom type
	Geom = ClassGeom("Geom")

	# Option type
	class Option:
		def __init__(self, lst):
			self.opts = convert_input([str], lst)
			self.optlist = " or ".join(["\"%s\""%i for i in self.opts])

		def __call__(self, arg):
			if arg in self.opts:
				return arg
			else:
				raise Exception, "'%s' is not a valid option. Try: "+self.optlist

		def __repr__(self):
			return self.optlist

	# Custom type
	class Custom:
		def __init__(self, format, name=None, doc=None):
			self.name = name
			self.format = format
			self.__doc__ = \
			str(self.format)+"\n"+str(doc)

		def __call__(self, arg):
			value = convert_input(self.format, eval(arg))
			return value

		def __repr__(self):
			return repr(self.format)

	# Frequency powerlaw for opacity
	KappFLaw = ClassPowerLaw("KappFLaw", Freq, Opacity, PwrIndex)

	# Wavelength powerlaw for opacity
	class ClassKappLLaw(ClassPowerLaw):
		def __call__(self, arg):
			value = eval(arg)
			lambda0 = self.x0f(value[0])
			freq0 = C.c / lambda0
			kapp0 = self.y0f(value[1])
			p = self.pf(value[2])
			return "powerlaw,%10.3e,%10.3e,%10.3e" % (freq0, kapp0, p)

	KappLLaw = ClassKappLLaw("KappLLaw", Length, Opacity, PwrIndex)

	# 'Optional' class for defining optional values
	class Optional(KeyType):
		pass

	# Boolean value
	Bool = ClassBool("Bool")


##
## Keyword class
##
class Key:
	def __init__(self, name, typ, deflt, desc):
		# Name of keyword
		self.name = str(name)

		# Convertor for the keyword
		self.typ = typ

		# Description
		self.desc = str(desc)

		# Default value
		self.deflt = deflt

		# If default value is not none nor empty string,
		# test whether the default value can be converted
		if (self.deflt is not Type.Optional) and (self.deflt is not None):
			try:
				dummy = self.typ(self.deflt)
			except:
				raise

	def __call__(self, input):
		# Convert input (usually text) into corresponding value
		try:
			return self.typ(input)
		except:
			raise Exception, "Error processing %s='%s'" % (self.name, input)




