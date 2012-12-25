#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <elf.h>

#include "Python.h"

char *e_indent_names[] =
    {
        "e_i_s_mag0",
        "e_i_s_mag1",
        "e_i_s_mag2",
        "e_i_s_mag3",
        "e_i_s_class",
        "e_i_s_data",
        "e_i_s_version",
        "e_i_s_osabi",
        "e_i_s_abiversion",
        "e_i_s_pad",
        "e_i_s_r10",
        "e_i_s_r11",
        "e_i_s_r12",
        "e_i_s_r13",
        "e_i_s_r14",
        "e_i_s_r15",
        NULL };

PyObject *
read_e_ident(PyObject *self, PyObject *args)
{

    PyObject * bytes_data;
    PyObject * ret;

    ret = Py_None;

    if (PyArg_ParseTuple(args, "O", &bytes_data) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {

        if (PySequence_Check(bytes_data) != 1)
        {
            ret = PyLong_FromLong(2);
        }
        else
        {
            if (PySequence_Length(bytes_data) < EI_NIDENT)
            {
                ret = PyLong_FromLong(3);
            }
            else
            {
                ret = PySequence_GetSlice(
                    bytes_data,
                    PyLong_AsSize_t(PyLong_FromLong(0)),
                    PyLong_AsSize_t(PyLong_FromLong(EI_NIDENT)));
            }
        }
    }

    return ret;
}

PyObject *
is_elf(PyObject *self, PyObject *args)
{
    PyObject * bytes_data;
    char * bytes_data_c;
    PyObject * ret = Py_False;

    if (PyArg_ParseTuple(args, "O", &bytes_data) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        if (PySequence_Length(bytes_data) < SELFMAG)
        {
            ret = PyLong_FromLong(2);
        }
        else
        {
            bytes_data_c = PyBytes_AsString(bytes_data);
            if (bytes_data_c[0] != ELFMAG0 || bytes_data_c[1] != ELFMAG1
                || bytes_data_c[2] != ELFMAG2 || bytes_data_c[3] != ELFMAG3)
            {
                ret = Py_False;
            }
            else
            {
                ret = Py_True;
            }
        }
    }

    return ret;
}

PyObject *
e_ident_bitness(PyObject *self, PyObject *args)
{

    PyObject * ret;

    char * t;
    PyObject * e_ident;

    if (PyArg_ParseTuple(args, "O", &e_ident) == 0)
    {
        ret = Py_None;
    }
    else
    {
        t = PyBytes_AsString(
            PySequence_GetSlice(
                e_ident,
                PyLong_AsSize_t(PyLong_FromLong(EI_CLASS)),
                PyLong_AsSize_t(PyLong_FromLong(EI_CLASS + 1))));
        switch (t[0])
        {
            case ELFCLASS32:
                ret = PyLong_FromLong(32);
                break;
            case ELFCLASS64:
                ret = PyLong_FromLong(64);
                break;
            default:
                ret = Py_None;
                break;
        }

    }

    return ret;
}

PyObject *
e_ident_to_dict(PyObject *self, PyObject *args)
{
    PyObject * e_ident_bytes;
    PyObject * ret;

    int i;

    e_ident_bytes = read_e_ident(self, args);

    if (PySequence_Check(e_ident_bytes) == 0)
    {
        ret = e_ident_bytes;
    }
    else
    {

        ret = PyDict_New();

        i = 0;
        while (1)
        {
            if (e_indent_names[i] == NULL)
            {
                break;
            }

            PyDict_SetItem(
                ret,
                PyUnicode_FromString(e_indent_names[i]),
                PySequence_GetSlice(
                    e_ident_bytes,
                    PyLong_AsSize_t(PyLong_FromLong(i)),
                    PyLong_AsSize_t(PyLong_FromLong(i + 1))));

            i++;
        }
    }
    return ret;
}

PyObject *
read_elf_ehdr_x(PyObject *self, PyObject *args)
{

    PyObject * data;
    PyObject * index;
    PyObject * x = PyLong_FromLong(0);
    PyObject * ret = Py_None;

    long elf_x_ehdr_i_size = 0;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &x) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {

        switch (PyLong_AsLong(x))
        {
            case 32:
            {
                elf_x_ehdr_i_size = sizeof(Elf32_Ehdr);
                break;
            }
            case 64:
            {
                elf_x_ehdr_i_size = sizeof(Elf64_Ehdr);
                break;
            }
            default:
                ret = PyLong_FromLong(2);
                break;
        }

        if (PyLong_Check(ret) == 0)
        {
            ret = PySequence_GetSlice(
                data,
                PyLong_AsSize_t(index),
                PyLong_AsSize_t(PyLong_FromLong(elf_x_ehdr_i_size)));
        }

    }

    return ret;
}

PyObject *
read_elf_ehdr(PyObject *self, PyObject *args)
{

    PyObject * data;
    PyObject * e_ident;
    PyObject * x;
    PyObject * args2;
    PyObject * ret;
    PyObject * index;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &e_ident) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        args2 = Py_BuildValue("(O)", e_ident);

        x = e_ident_bitness(self, args2);

        args2 = Py_BuildValue("(OOO)", data, index, x);

        ret = read_elf_ehdr_x(self, args2);
    }

    return ret;
}

//PyObject * elf_x_ehdr_to_dict(PyObject *self, PyObject *args) {
//	PyObject * ret;
//	if (PyArg_ParseTuple(args, "OOO", &data, &index, &x) == 0) {
//		ret = PyLong_FromLong(1);
//	} else {
//	}
//	return ret;
//}

//PyObject * elf_ehdr_to_dict(PyObject *self, PyObject *args) {
//
//	PyObject * elf_hdr;
//	PyObject * e_ident;
//	PyObject * x;
//	PyObject * args2;
//	PyObject * ret;
//	PyObject * index;
//
//	if (PyArg_ParseTuple(args, "O", &e_ident, &elf_hdr) == 0) {
//		ret = PyLong_FromLong(1);
//	} else {
//		args2 = Py_BuildValue("(O)", e_ident);
//
//		x = e_ident_bitness(self, args2);
//
//		args2 = Py_BuildValue("(OOO)", data, index, x);
//
//		ret = read_elf_ehdr_x(self, args2);
//	}
//
//	return ret;
//}

PyObject *
read_elf_shdr_x(PyObject *self, PyObject *args)
{

    PyObject * data;
    PyObject * index;
    PyObject * x = PyLong_FromLong(0);
    PyObject * ret = Py_None;

    long elf_x_shdr_i_size = 0;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &x) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {

        switch (PyLong_AsLong(x))
        {
            case 32:
            {
                elf_x_shdr_i_size = sizeof(Elf32_Shdr);
                break;
            }
            case 64:
            {
                elf_x_shdr_i_size = sizeof(Elf64_Shdr);
                break;
            }
            default:
                ret = PyLong_FromLong(2);
                break;
        }

        if (PyLong_Check(ret) == 0)
        {
            ret = PySequence_GetSlice(
                data,
                PyLong_AsSize_t(index),
                PyLong_AsSize_t(PyLong_FromLong(elf_x_shdr_i_size)));
        }

    }

    return ret;
}

PyObject *
read_elf_shdr(PyObject *self, PyObject *args)
{

    PyObject * data;
    PyObject * e_ident;
    PyObject * x;
    PyObject * args2;
    PyObject * ret;
    PyObject * index;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &e_ident) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        args2 = Py_BuildValue("(O)", e_ident);

        x = e_ident_bitness(self, args2);

        args2 = Py_BuildValue("(OOO)", data, index, x);

        ret = read_elf_shdr_x(self, args2);
    }

    return ret;
}

#define PYDICT_SETITEM1(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data2, \
        offsetof(Elf32_Ehdr, v), \
        offsetof(Elf32_Ehdr, v)+sizeof(t)));

PyObject *
elf32_ehdr_to_dict(PyObject *self, PyObject *args)
{
    PyObject * data;
    PyObject * index;

    PyObject * data2;
    PyObject * ret = Py_None;

    if (PyArg_ParseTuple(args, "OO", &data, &index) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        data2 = PySequence_GetSlice(
            data,
            PyLong_AsLong(index),
            PyLong_AsLong(index) + sizeof(Elf32_Ehdr));

        ret = PyDict_New();

        PyDict_SetItem(
            ret,
            PyUnicode_FromString("e_ident"),
            PySequence_GetSlice(
                data2,
                offsetof(Elf32_Ehdr, e_ident),
                offsetof(Elf32_Ehdr, e_ident) + EI_NIDENT));

        PYDICT_SETITEM1(e_type, Elf32_Half)
        PYDICT_SETITEM1(e_machine, Elf32_Half)
        PYDICT_SETITEM1(e_version, Elf32_Word)
        PYDICT_SETITEM1(e_entry, Elf32_Addr)
        PYDICT_SETITEM1(e_phoff, Elf32_Off)
        PYDICT_SETITEM1(e_shoff, Elf32_Off)
        PYDICT_SETITEM1(e_flags, Elf32_Word)
        PYDICT_SETITEM1(e_ehsize, Elf32_Half)
        PYDICT_SETITEM1(e_phentsize, Elf32_Half)
        PYDICT_SETITEM1(e_phnum, Elf32_Half)
        PYDICT_SETITEM1(e_shentsize, Elf32_Half)
        PYDICT_SETITEM1(e_shnum, Elf32_Half)
        PYDICT_SETITEM1(e_shstrndx, Elf32_Half)

    }

    return ret;
}

#undef PYDICT_SETITEM1

#define PYDICT_SETITEM1(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data2, \
        offsetof(Elf64_Ehdr, v), \
        offsetof(Elf64_Ehdr, v)+sizeof(t)));

PyObject *
elf64_ehdr_to_dict(PyObject *self, PyObject *args)
{
    PyObject * data;
    PyObject * index;

    PyObject * data2;
    PyObject * ret = Py_None;

    if (PyArg_ParseTuple(args, "OO", &data, &index) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {

        data2 = PySequence_GetSlice(
            data,
            PyLong_AsLong(index),
            PyLong_AsLong(index) + sizeof(Elf64_Ehdr));

        ret = PyDict_New();

        PyDict_SetItem(
            ret,
            PyUnicode_FromString("e_ident"),
            PySequence_GetSlice(
                data2,
                offsetof(Elf64_Ehdr, e_ident),
                offsetof(Elf64_Ehdr, e_ident) + EI_NIDENT));

        PYDICT_SETITEM1(e_type, Elf64_Half)
        PYDICT_SETITEM1(e_machine, Elf64_Half)
        PYDICT_SETITEM1(e_version, Elf64_Word)
        PYDICT_SETITEM1(e_entry, Elf64_Addr)
        PYDICT_SETITEM1(e_phoff, Elf64_Off)
        PYDICT_SETITEM1(e_shoff, Elf64_Off)
        PYDICT_SETITEM1(e_flags, Elf64_Word)
        PYDICT_SETITEM1(e_ehsize, Elf64_Half)
        PYDICT_SETITEM1(e_phentsize, Elf64_Half)
        PYDICT_SETITEM1(e_phnum, Elf64_Half)
        PYDICT_SETITEM1(e_shentsize, Elf64_Half)
        PYDICT_SETITEM1(e_shnum, Elf64_Half)
        PYDICT_SETITEM1(e_shstrndx, Elf64_Half)

    }

    return ret;
}

#undef PYDICT_SETITEM1

PyObject *
elf_ehdr_to_dict(PyObject *self, PyObject *args)
{

    PyObject * data;
    PyObject * e_ident;
    PyObject * x;
    PyObject * args2;
    PyObject * ret = Py_None;
    PyObject * index;

    if (PyArg_ParseTuple(args, "OOO", &data, &index, &e_ident) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {

        args2 = Py_BuildValue("(O)", e_ident);

        x = e_ident_bitness(self, args2);

        args2 = Py_BuildValue("OO", data, index);

        switch (PyLong_AsLong(x))
        {
            case 32:
            {
                ret = elf32_ehdr_to_dict(self, args2);
                break;
            }
            case 64:
            {
                ret = elf64_ehdr_to_dict(self, args2);
                break;
            }
            default:
                ret = PyLong_FromLong(2);
                break;
        }

    }

    return ret;
}

static PyMethodDef elf_bin_methods[] =
    {
        {
            "read_e_ident",
            read_e_ident,
            METH_VARARGS,
            "read e_ident from bytes object" },
        {
            "is_elf",
            is_elf,
            METH_VARARGS,
            "check is bytes varibale is elf. var length must be == 4 bytes" },
        {
            "e_ident_bitness",
            e_ident_bitness,
            METH_VARARGS,
            "return elf bitness by e_ident" },
        {
            "e_ident_to_dict",
            e_ident_to_dict,
            METH_VARARGS,
            "convert e_ident to Python dict" },
        {
            "read_elf_ehdr",
            read_elf_ehdr,
            METH_VARARGS,
            "reads elf header using e_ident to know bitness" },
        {
            "read_elf_ehdr_x",
            read_elf_ehdr_x,
            METH_VARARGS,
            "read elf section header by given bitness" },
        {
            "read_elf_shdr",
            read_elf_shdr,
            METH_VARARGS,
            "reads elf section header using e_ident to know bitness" },
        {
            "read_elf_shdr_x",
            read_elf_shdr_x,
            METH_VARARGS,
            "read elf header by given bitness" },

        {
            "elf32_ehdr_to_dict",
            elf32_ehdr_to_dict,
            METH_VARARGS,
            "convert Elf32_Ehdr to dict" },

        {
            "elf64_ehdr_to_dict",
            elf64_ehdr_to_dict,
            METH_VARARGS,
            "convert Elf64_Ehdr to dict" },

        {
            "elf_ehdr_to_dict",
            elf_ehdr_to_dict,
            METH_VARARGS,
            "Split elf ehdr to Python dict by knowing bitness from e_ident" },

        { NULL, NULL, 0, NULL } };

static struct PyModuleDef elf_bin_module =
    { PyModuleDef_HEAD_INIT, "elf_bin", NULL, -1, elf_bin_methods };

PyMODINIT_FUNC
PyInit_elf_bin(void)
{
    return PyModule_Create(&elf_bin_module);
}
