#include "sparx.h"
#include "debug.h"
#include <stdarg.h>
#include <memory.h>
#include "task.h"

#define PYMAIN\
	PyImport_AddModule("__main__")

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_PyObj(const char *name, PyObject **obj)
/* Get user input as Python object, returns a NEW reference which
 * must be DECREF'd */
{
	int sts = 0;
	PyObject *inputs = NULL, *INP_DICT = NULL, *keyobj = NULL;

	/* Import sparx.inputs (new ref) */
        char static_library[] = ".inputs";

        char *static_library_path =
          malloc(1+ strlen(Sp_SPARX_VERSION) + strlen(static_library) );
        //char static_library_path[16];
        strcpy(static_library_path, Sp_SPARX_VERSION);
        strcat(static_library_path, static_library);
	if(!(inputs = PyImport_ImportModule(static_library_path))) {
		PyWrErr_SetString(PyExc_Exception, "Error importing sparx.inputs");
		sts = 1;
	}
#if 0
printf("name=%s sts=%d\n", name, sts);
printf("path=%s len=%d\n", static_library_path, strlen(static_library_path));
printf("library=%s len=%d\n", static_library, strlen(static_library));
printf("version=%s len=%d\n", Sp_SPARX_VERSION, strlen(Sp_SPARX_VERSION));
#endif
        free(static_library_path);
	/* Get INP_DICT dictionary (new ref) */
	if(!sts) {
		INP_DICT = PyObject_GetAttrString(inputs, "INP_DICT");
		if(!INP_DICT) {
			PyWrErr_SetString(PyExc_Exception, "Error retrieving sparx.inputs.INP_DICT", name);
			sts = 1;
		}
	}

	/* Get input keyword from dictionary (new ref) */
	if(!sts) {
		*obj = keyobj = PyDict_GetItemString(INP_DICT, name);
		if(keyobj) {
			/* VERY IMPORTANT! */
			Py_INCREF(keyobj);
		}
		else {
			PyWrErr_SetString(PyExc_Exception, "Keyword '%s' not set", name);
			sts = 1;
		}
	}

	/* Cleanup */
	Py_XDECREF(INP_DICT);
	Py_XDECREF(inputs);

	return sts;
}

/*----------------------------------------------------------------------------*/

int SpPy_CheckOptionalInput(const char *name)
/* Check whether key 'name' exists and is not none. If any error occurrs or
 * the key is none, return 0; otherwise return 1 */
{
	int sts = 0, exists = 0;
	PyObject *obj = 0;

	sts = SpPy_GetInput_PyObj(name, &obj);

	if(!sts) {
		if(obj != Py_None) exists = 1;
		Py_DECREF(obj);
	}

	return exists;
}

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_int(const char *name, int *value)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *obj;

	status = SpPy_GetInput_PyObj(name, &obj);
	if(!status) {
		*value = (int)PyInt_AsLong(obj);
		Py_DECREF(obj);
	}

	return status;
}

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_sizt(const char *name, size_t *value)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *obj;

	status = SpPy_GetInput_PyObj(name, &obj);
	if(!status) {
		*value = (size_t)PyInt_AsLong(obj);
		Py_DECREF(obj);
	}

	return status;
}

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_dbl(const char *name, double *value)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *obj;

	status = SpPy_GetInput_PyObj(name, &obj);
	if(!status) {
		*value = PyFloat_AsDouble(obj);
		Py_DECREF(obj);
	}

	return status;
}

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_bool(const char *name, int *value)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *obj;

	status = SpPy_GetInput_PyObj(name, &obj);
	if(!status) {
		*value = PyObject_IsTrue(obj);
		Py_DECREF(obj);
	}

	return status;
}

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_model(const char *Source,const char *Pops, SpModel *model, int *read_pops, const int task_id)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *SourceObj;
	PyObject *PopsObj;

	status = SpPy_GetInput_PyObj(Source, &SourceObj);
	status = SpPy_GetInput_PyObj(Pops,   &PopsObj  );

        const char * sourcefname = Sp_PYSTR(SourceObj);
        const char * popsfname   = Sp_PYSTR(PopsObj);

        if ( task_id == TASK_AMC ){
                if ( popsfname == 0)
                        *read_pops = 0;
                else
                        *read_pops = 1;
        }
	if(!status) {
		if ( status = SpIO_OpenModel(sourcefname, popsfname, model, read_pops) )
			PyWrErr_SetString(PyExc_Exception, "Error opening model '%s'", sourcefname);
		Py_DECREF(SourceObj);
		Py_DECREF(PopsObj);
	}

	return status;
}

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_molec(const char *name, Molec **molec)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *obj;

	status = SpPy_GetInput_PyObj(name, &obj);
	if(!status) {
		if(!(*molec = SpIO_FreadMolec(Sp_PYSTR(obj)))) {
			PyWrErr_SetString(PyExc_Exception, "Error opening molecule '%s'", Sp_PYSTR(obj));
			status = 1;
		}
		Py_DECREF(obj);
	}

	return status;
}



/*----------------------------------------------------------------------------*/
int SpPy_GetInput_spfile(const char *name, SpFile **fp, int mode)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *obj;

	status = SpPy_GetInput_PyObj(name, &obj);
	if(!status) {
		*fp = SpIO_OpenFile(Sp_PYSTR(obj), mode);
		if(!*fp) {
			PyWrErr_SetString(PyExc_Exception, "Error opening SPARX file '%s'", Sp_PYSTR(obj));
			status = 1;
		}
		Py_DECREF(obj);
	}

	return status;
}

/*----------------------------------------------------------------------------*/

int SpPy_GetInput_mirxy_new(const char *name, size_t nx, size_t ny, size_t nv, MirFile **fp)
/* Get user input as size_t and return error status */
{
	int status = 0;
	PyObject *obj;

	status = SpPy_GetInput_PyObj(name, &obj);

	if(!status) {
		*fp = MirXY_Open_new(Sp_PYSTR(obj), nx, ny, nv);
		if(!*fp) {
			PyWrErr_SetString(PyExc_Exception, "Error opening Miriad XYV file '%s'", Sp_PYSTR(obj));
			status = 1;
		}
		Py_DECREF(obj);
	}


	return status;
}

/*----------------------------------------------------------------------------*/

void SpPy_CallVoidFunc(const char *func)
{
	PyObject *o;

	o = SpPy_GETMAIN(func);
	Deb_ASSERT(o != NULL);

	PyObject_CallFunction(o, NULL);
	Py_DECREF(o);

	if(PyErr_Occurred())
		Err_SETSTRING("Internal Python error");

	return;
}

/*----------------------------------------------------------------------------*/

int SpPy_Initialize(void)
/* Initialize external Python resources */
{
	int status = 0;
	size_t i;
	FILE *fp = 0;
	const char *files[] = {
		"pysparx-module.py",
		"pysparx-inputs.py",
		"pysparx-tasks.py",
		"pysparx-main.py",
		0
	};
	char *string;

	/* Init program path */
	if(!status)
		status = PyWrRun_SimpleString("Sp_ROOT='%s'", Sp_ROOT);

	if(!status)
		status = PyWrRun_SimpleString("Sp_MPIRANK=%d", Sp_MPIRANK);

	/* Init geomtry types */
	if(!status)
		status = PyWrRun_SimpleString("GEOM_TYPES={}");

	for(i = 0; GEOM_TYPES[i].name; i++) {
		if(!status)
			status = PyWrRun_SimpleString("GEOM_TYPES['%s']=%d", GEOM_TYPES[i].name, GEOM_TYPES[i].idx);
	}

	for(i = 0; files[i] && !status; i++) {
		/* Load input related routines */
		string = Mem_Sprintf("%s/%s", Sp_ROOT, files[i]);
		if(!(fp = fopen(string, "r"))) {
			status = Err_SETSTRING("Could not open file `%s'", string);
		}
		else {
			status = PyRun_SimpleFile(fp, string);
			if(status)
				Err_SETSTRING("Python error in file `%s'", string);

			fclose(fp);
		}
		free(string);
	}

	return status;
}

/*----------------------------------------------------------------------------*/

PyObject *SpPy_GetMain(const char *symb, const char *file, int line, const char *func)
/* Retrieve a Python object from the __main__ module.
 * This returns a NEW reference to PyObject *.
 */
{
	int status = 0;
	static PyObject *__main__ = 0;
	PyObject *op = 0;

	/* Get borrowed reference to __main__ */
	if(!__main__)
		__main__ = PYMAIN;

	/* Check if symb has been set in __main__ */
	if(!status && PyObject_HasAttrString(__main__, symb))
		op = PyObject_GetAttrString(__main__, symb);
	else
		Err_SetString(file, line, func, "Error retrieving Python object `%s' from __main__.", symb);

	return op;
}



