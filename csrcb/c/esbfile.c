#include "Python.h"
#include "esb_front_internal.h"

static PyObject * Py_ftpput(PyObject *self, PyObject *args)
{
    const char * localfile;
    const char * remotefile;
    if (!PyArg_ParseTuple(args, "ss", &localfile, &remotefile))
        return NULL;
    int rec = ftpput(remotefile, localfile,0);
    return Py_BuildValue("i", rec);
}

static PyObject * Py_ftpget(PyObject *self, PyObject *args)
{
    const char * localfile;
    const char * remotefile;
    if (!PyArg_ParseTuple(args, "ss", &remotefile, &localfile))
        return NULL;
    int rec = ftpget(remotefile, localfile,0);
    return Py_BuildValue("i", rec);
}

static PyMethodDef Methods[] = {
    {"Py_ftpput", Py_ftpput, METH_VARARGS, "Py_ftpput"},
    {"Py_ftpget", Py_ftpget, METH_VARARGS, "Py_ftpget"},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initesbfile(void)
{
    PyObject *m;
    m = Py_InitModule("esbfile", Methods);
    if (m == NULL)
        return;
}