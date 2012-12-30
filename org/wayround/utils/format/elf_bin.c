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
PyLong_FromPyBytes(PyObject *bytes, PyObject *sign)
{

    PyObject * ret = Py_None;
    char * bytes_as_char;
    Py_ssize_t bytes_size;

    union
    {
        unsigned long ul;
        unsigned long long ull;
        long l;
        long long ll;
    } u;

    u.ull = 0;

    bytes_as_char = PyBytes_AsString(bytes);
    bytes_size = PySequence_Length(bytes);

    if (sign == Py_True)
    {
        if (bytes_size <= sizeof(long))
        {
            memcpy(&u.l, bytes_as_char, bytes_size);
            ret = PyLong_FromLong(u.l);

        }
        else if (bytes_size <= sizeof(long long))
        {
            memcpy(&u.ll, bytes_as_char, bytes_size);
            ret = PyLong_FromLongLong(u.ll);
        }
        else
        {
            ret = Py_None;
        }
    }
    else
    {
        if (bytes_size <= sizeof(unsigned long))
        {
            memcpy(&u.ul, bytes_as_char, bytes_size);
            ret = PyLong_FromUnsignedLong(u.ul);
        }
        else if (bytes_size <= sizeof(unsigned long long))
        {
            memcpy(&u.ull, bytes_as_char, bytes_size);
            ret = PyLong_FromUnsignedLongLong(u.ull);
        }
        else
        {
            ret = Py_None;
        }
    }

    return ret;
}

PyObject *
ExpPyLong_FromPyBytes(PyObject *self, PyObject *args)
{

    PyObject * bytes;
    PyObject * sign;
    PyObject * ret = Py_None;

    if (PyArg_ParseTuple(args, "OO", &bytes, &sign) == 0)
    {
        ret = Py_None;
    }
    else
    {
        ret = PyLong_FromPyBytes(bytes, sign);
    }

    return ret;
}

PyObject *
convert_virtual_to_file(PyObject *self, PyObject *args)
{
    PyObject * ret = Py_None;

    PyObject * program_section_table;
    PyObject * value;

    PyObject * item;

    long i;
    long program_section_table_size;

    unsigned long long long_value;
    unsigned long long p_vaddr;
    unsigned long long shift;

    if (PyArg_ParseTuple(args, "OO", &program_section_table, &value) == 0)
    {
        ret = Py_None;
    }
    else
    {

        long_value = PyLong_AsUnsignedLongLong(value);

        program_section_table_size = PySequence_Length(program_section_table);

        for (i = 0; i != program_section_table_size; i++)
        {
            item = PyList_GetItem(program_section_table, i);

            p_vaddr = PyLong_AsUnsignedLongLong(
                PyLong_FromPyBytes(
                    PyDict_GetItem(item, PyUnicode_FromString("p_vaddr")),
                    Py_False));

            if (long_value >= p_vaddr
                && long_value
                    < (p_vaddr
                        + PyLong_AsUnsignedLongLong(
                            PyLong_FromPyBytes(
                                PyDict_GetItem(
                                    item,
                                    PyUnicode_FromString("p_memsz")),
                                Py_False))))

            {
                shift = long_value - p_vaddr
                    + PyLong_AsUnsignedLongLong(
                        PyLong_FromPyBytes(
                            PyDict_GetItem(
                                item,
                                PyUnicode_FromString("p_offset")),
                            Py_False));

                ret = PyLong_FromUnsignedLongLong(shift);
                break;
            }

        }
    }

    return ret;
}

PyObject *
read_e_ident(PyObject *self, PyObject *args)
{

    PyObject * bytes_data;
    PyObject * ret = Py_None;

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
    PyObject * bytes_data_slice;
    char * bytes_data_c;
    PyObject * ret = Py_False;

    if (PyArg_ParseTuple(args, "O", &bytes_data) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        bytes_data_slice = PySequence_GetSlice(bytes_data, 0, SELFMAG);

        if (PySequence_Length(bytes_data_slice) < SELFMAG)
        {
            ret = PyLong_FromLong(2);
        }
        else
        {
            bytes_data_c = PyBytes_AsString(bytes_data_slice);

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
class_switch(long val)
{
    PyObject * ret;
    switch (val)
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

        ret = class_switch(t[0]);
    }

    return ret;
}

PyObject *
e_ident_dict_bitness(PyObject *self, PyObject *args)
{

    PyObject * ret;

    PyObject * cls;

    char * t;
    PyObject * e_ident_dict;

    if (PyArg_ParseTuple(args, "O", &e_ident_dict) == 0)
    {
        ret = Py_None;
    }
    else
    {
        cls = PyDict_GetItem(e_ident_dict, PyUnicode_FromString("e_i_s_class"));

        t = PyBytes_AsString(cls);

        ret = class_switch(t[0]);
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

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data2, \
        PyLong_AsLong(index)+offsetof(Elf32_Ehdr, v), \
        PyLong_AsLong(index)+offsetof(Elf32_Ehdr, v)+sizeof(t)));

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

        PYDICT_SETITEM(e_type, Elf32_Half)
        PYDICT_SETITEM(e_machine, Elf32_Half)
        PYDICT_SETITEM(e_version, Elf32_Word)
        PYDICT_SETITEM(e_entry, Elf32_Addr)
        PYDICT_SETITEM(e_phoff, Elf32_Off)
        PYDICT_SETITEM(e_shoff, Elf32_Off)
        PYDICT_SETITEM(e_flags, Elf32_Word)
        PYDICT_SETITEM(e_ehsize, Elf32_Half)
        PYDICT_SETITEM(e_phentsize, Elf32_Half)
        PYDICT_SETITEM(e_phnum, Elf32_Half)
        PYDICT_SETITEM(e_shentsize, Elf32_Half)
        PYDICT_SETITEM(e_shnum, Elf32_Half)
        PYDICT_SETITEM(e_shstrndx, Elf32_Half)

    }

    return ret;
}

#undef PYDICT_SETITEM

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data2, \
        PyLong_AsLong(index)+offsetof(Elf64_Ehdr, v), \
        PyLong_AsLong(index)+offsetof(Elf64_Ehdr, v)+sizeof(t)));

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

        PYDICT_SETITEM(e_type, Elf64_Half)
        PYDICT_SETITEM(e_machine, Elf64_Half)
        PYDICT_SETITEM(e_version, Elf64_Word)
        PYDICT_SETITEM(e_entry, Elf64_Addr)
        PYDICT_SETITEM(e_phoff, Elf64_Off)
        PYDICT_SETITEM(e_shoff, Elf64_Off)
        PYDICT_SETITEM(e_flags, Elf64_Word)
        PYDICT_SETITEM(e_ehsize, Elf64_Half)
        PYDICT_SETITEM(e_phentsize, Elf64_Half)
        PYDICT_SETITEM(e_phnum, Elf64_Half)
        PYDICT_SETITEM(e_shentsize, Elf64_Half)
        PYDICT_SETITEM(e_shnum, Elf64_Half)
        PYDICT_SETITEM(e_shstrndx, Elf64_Half)

    }

    return ret;
}

#undef PYDICT_SETITEM

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

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf32_Shdr, v), \
        PyLong_AsLong(index)+offsetof(Elf32_Shdr, v)+sizeof(t)));

PyObject *
shdr32_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret;

    PyObject * data_seq;
    PyObject * index;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        ret = PyDict_New();

        PYDICT_SETITEM(sh_name, Elf32_Word)
        PYDICT_SETITEM(sh_type, Elf32_Word)
        PYDICT_SETITEM(sh_flags, Elf32_Word)
        PYDICT_SETITEM(sh_addr, Elf32_Addr)
        PYDICT_SETITEM(sh_offset, Elf32_Off)
        PYDICT_SETITEM(sh_size, Elf32_Word)
        PYDICT_SETITEM(sh_link, Elf32_Word)
        PYDICT_SETITEM(sh_info, Elf32_Word)
        PYDICT_SETITEM(sh_addralign, Elf32_Word)
        PYDICT_SETITEM(sh_entsize, Elf32_Word)
    }

    return ret;
}

#undef PYDICT_SETITEM
#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf64_Shdr, v), \
        PyLong_AsLong(index)+offsetof(Elf64_Shdr, v)+sizeof(t)));

PyObject *
shdr64_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret;

    PyObject * data_seq;
    PyObject * index;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        ret = PyDict_New();

        PYDICT_SETITEM(sh_name, Elf64_Word)
        PYDICT_SETITEM(sh_type, Elf64_Word)
        PYDICT_SETITEM(sh_flags, Elf64_Word)
        PYDICT_SETITEM(sh_addr, Elf64_Addr)
        PYDICT_SETITEM(sh_offset, Elf64_Off)
        PYDICT_SETITEM(sh_size, Elf64_Word)
        PYDICT_SETITEM(sh_link, Elf64_Word)
        PYDICT_SETITEM(sh_info, Elf64_Word)
        PYDICT_SETITEM(sh_addralign, Elf64_Word)
        PYDICT_SETITEM(sh_entsize, Elf64_Word)
    }

    return ret;
}

#undef PYDICT_SETITEM

PyObject *
read_elf_section_header_table(PyObject *self, PyObject *args)
{

    PyObject * data_seq;
    PyObject * e_ident_dict;
    PyObject * ehdr_dict;

    PyObject * ret = Py_None;

    PyObject * args2;
    PyObject * bits;

    PyObject * sheader_size;
    PyObject * sheaders_count;

    PyObject * td;

    PyObject * index;
    PyObject * offset;

    long i;

    if (PyArg_ParseTuple(args, "OOO", &data_seq, &e_ident_dict, &ehdr_dict)
        == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        args2 = Py_BuildValue("(O)", e_ident_dict);

        bits = e_ident_dict_bitness(self, args2);

        sheader_size = PyLong_FromPyBytes(
            PyDict_GetItem(ehdr_dict, PyUnicode_FromString("e_shentsize")),
            Py_True);

        offset = PyLong_FromPyBytes(
            PyDict_GetItem(ehdr_dict, PyUnicode_FromString("e_shoff")),
            Py_True);

        sheaders_count = PyLong_FromPyBytes(
            PyDict_GetItem(ehdr_dict, PyUnicode_FromString("e_shnum")),
            Py_True);

        ret = PyList_New(0);

        for (i = 0; i != PyLong_AsLong(sheaders_count); i++)
        {
            switch (PyLong_AsLong(bits))
            {

                case 32:
                {
                    index = PyNumber_Add(
                        offset,
                        PyNumber_Multiply(sheader_size, PyLong_FromLong(i)));
                    args2 = Py_BuildValue("OO", data_seq, index);
                    td = shdr32_to_dict(self, args2);
                    break;
                }
                case 64:
                {
                    index = PyNumber_Add(
                        offset,
                        PyNumber_Multiply(sheader_size, PyLong_FromLong(i)));
                    args2 = Py_BuildValue("OO", data_seq, index);
                    td = shdr64_to_dict(self, args2);
                    break;
                }
                default:
                    td = Py_None;
            }

            PyList_Append(ret, td);
        }
    }

    return ret;
}

PyObject *
read_elf_phdr_x(PyObject *self, PyObject *args)
{

    PyObject * data;
    PyObject * index;
    PyObject * x = PyLong_FromLong(0);
    PyObject * ret = Py_None;

    long elf_x_phdr_i_size = 0;

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
                elf_x_phdr_i_size = sizeof(Elf32_Phdr);
                break;
            }
            case 64:
            {
                elf_x_phdr_i_size = sizeof(Elf64_Phdr);
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
                PyLong_AsSize_t(PyLong_FromLong(elf_x_phdr_i_size)));
        }

    }

    return ret;
}

PyObject *
read_elf_phdr(PyObject *self, PyObject *args)
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

        ret = read_elf_phdr_x(self, args2);
    }

    return ret;
}

#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf32_Phdr, v), \
        PyLong_AsLong(index)+offsetof(Elf32_Phdr, v)+sizeof(t)));

PyObject *
phdr32_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret;

    PyObject * data_seq;
    PyObject * index;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        ret = PyDict_New();

        PYDICT_SETITEM(p_type, Elf32_Word)
        PYDICT_SETITEM(p_offset, Elf32_Off)
        PYDICT_SETITEM(p_vaddr, Elf32_Addr)
        PYDICT_SETITEM(p_paddr, Elf32_Addr)
        PYDICT_SETITEM(p_filesz, Elf32_Word)
        PYDICT_SETITEM(p_memsz, Elf32_Word)
        PYDICT_SETITEM(p_flags, Elf32_Word)
        PYDICT_SETITEM(p_align, Elf32_Word)
    }

    return ret;
}

#undef PYDICT_SETITEM
#define PYDICT_SETITEM(v, t) \
PyDict_SetItem( \
    ret, \
    PyUnicode_FromString(#v), \
    PySequence_GetSlice( \
        data_seq, \
        PyLong_AsLong(index)+offsetof(Elf64_Phdr, v), \
        PyLong_AsLong(index)+offsetof(Elf64_Phdr, v)+sizeof(t)));

PyObject *
phdr64_to_dict(PyObject *self, PyObject *args)
{
    PyObject * ret;

    PyObject * data_seq;
    PyObject * index;

    if (PyArg_ParseTuple(args, "OO", &data_seq, &index) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        ret = PyDict_New();

        PYDICT_SETITEM(p_type, Elf64_Word)
        PYDICT_SETITEM(p_offset, Elf64_Off)
        PYDICT_SETITEM(p_vaddr, Elf64_Addr)
        PYDICT_SETITEM(p_paddr, Elf64_Addr)
        PYDICT_SETITEM(p_filesz, Elf64_Word)
        PYDICT_SETITEM(p_memsz, Elf64_Word)
        PYDICT_SETITEM(p_flags, Elf64_Word)
        PYDICT_SETITEM(p_align, Elf64_Word)
    }

    return ret;
}

#undef PYDICT_SETITEM

PyObject *
read_elf_program_header_table(PyObject *self, PyObject *args)
{

    PyObject * data_seq;
    PyObject * e_ident_dict;
    PyObject * ehdr_dict;

    PyObject * ret = Py_None;

    PyObject * args2;
    PyObject * bits;

    PyObject * sheader_size;
    PyObject * sheaders_count;

    PyObject * td;

    PyObject * index;
    PyObject * offset;

    long i;

    if (PyArg_ParseTuple(args, "OOO", &data_seq, &e_ident_dict, &ehdr_dict)
        == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        args2 = Py_BuildValue("(O)", e_ident_dict);

        bits = e_ident_dict_bitness(self, args2);

        sheader_size = PyLong_FromPyBytes(
            PyDict_GetItem(ehdr_dict, PyUnicode_FromString("e_phentsize")),
            Py_True);

        offset = PyLong_FromPyBytes(
            PyDict_GetItem(ehdr_dict, PyUnicode_FromString("e_phoff")),
            Py_True);

        sheaders_count = PyLong_FromPyBytes(
            PyDict_GetItem(ehdr_dict, PyUnicode_FromString("e_phnum")),
            Py_True);

        ret = PyList_New(0);

        for (i = 0; i != PyLong_AsLong(sheaders_count); i++)
        {
            switch (PyLong_AsLong(bits))
            {

                case 32:
                {
                    index = PyNumber_Add(
                        offset,
                        PyNumber_Multiply(sheader_size, PyLong_FromLong(i)));
                    args2 = Py_BuildValue("OO", data_seq, index);
                    td = phdr32_to_dict(self, args2);
                    break;
                }
                case 64:
                {
                    index = PyNumber_Add(
                        offset,
                        PyNumber_Multiply(sheader_size, PyLong_FromLong(i)));
                    args2 = Py_BuildValue("OO", data_seq, index);
                    td = phdr64_to_dict(self, args2);
                    break;
                }
                default:
                    td = Py_None;
            }

            PyList_Append(ret, td);
        }
    }

    return ret;
}

PyObject *
get_ehdr_string_table_slice(PyObject *self, PyObject *args)
{

    PyObject * ret;

    PyObject * data_seq;
    PyObject * elf_section_header_table;
    PyObject * ehdr_dict;
    PyObject * string_table_record;
    PyObject * string_table_offset;
    PyObject * string_table_size;
    PyObject * header_bytes;

    if (PyArg_ParseTuple(
        args,
        "OOO",
        &data_seq,
        &elf_section_header_table,
        &ehdr_dict) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        string_table_record = PySequence_GetItem(
            elf_section_header_table,
            PyLong_AsSsize_t(
                PyLong_FromPyBytes(
                    PyDict_GetItem(
                        ehdr_dict,
                        PyUnicode_FromString("e_shstrndx")),
                    Py_True)));

        string_table_offset = PyLong_FromPyBytes(
            PyDict_GetItem(
                string_table_record,
                PyUnicode_FromString("sh_offset")),
            Py_False);

        string_table_size = PyLong_FromPyBytes(
            PyDict_GetItem(
                string_table_record,
                PyUnicode_FromString("sh_size")),
            Py_False);

        header_bytes = PySequence_GetSlice(
            data_seq,
            PyLong_AsSsize_t(string_table_offset),
            PyLong_AsSsize_t(string_table_offset)
                + PyLong_AsSsize_t(string_table_size));

        ret = header_bytes;
    }

    return ret;
}

PyObject *
get_dyn_string_table_slice(PyObject *self, PyObject *args)
{

    PyObject * ret;
    PyObject * args2;
    PyObject * program_table;

    PyObject * data_seq;
    PyObject * dinamics_table;

    long dinamics_table_size;
    long i;

    unsigned long long strtab = 0;
    unsigned long long strsz = 0;

    unsigned long long long_value;
    PyObject * item;

    if (PyArg_ParseTuple(
        args,
        "OOO",
        &data_seq,
        &program_table,
        &dinamics_table) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {

        dinamics_table_size = PySequence_Length(dinamics_table);

        for (i = 0; i != dinamics_table_size; i++)
        {
            item = PyList_GetItem(dinamics_table, i);

            long_value = PyLong_AsUnsignedLongLong(
                PyDict_GetItem(item, PyUnicode_FromString("d_tag")));

            if (long_value == DT_STRTAB)
            {
                strtab = PyLong_AsUnsignedLongLong(
                    PyDict_GetItem(item, PyUnicode_FromString("d_ptr")));
            }

            if (long_value == DT_STRSZ)
            {
                strsz = PyLong_AsUnsignedLongLong(
                    PyDict_GetItem(item, PyUnicode_FromString("d_val")));
            }
        }

        if (strtab == 0 || strsz == 0)
        {
            ret = PyLong_FromLong(2);
        }
        else
        {

            args2 = Py_BuildValue(
                "OO",
                program_table,
                PyLong_FromUnsignedLongLong(strtab));
            strtab = PyLong_AsUnsignedLongLong(
                convert_virtual_to_file(self, args2));

            ret = PySequence_GetSlice(data_seq, strtab, strtab + strsz);
        }

    }

    return ret;
}

PyObject *
read_elf_section_header_table_names(PyObject *self, PyObject *args)
{
    PyObject * ret;
    PyObject * data_seq;
    PyObject * elf_section_header_table;
    PyObject * ehdr_dict;

    PyObject * section_header;
    PyObject * header_bytes;
    char * header_bytes_char;

    Py_ssize_t table_len;
    long name_offset;
    long i;

    if (PyArg_ParseTuple(
        args,
        "OOO",
        &data_seq,
        &elf_section_header_table,
        &ehdr_dict) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        header_bytes = get_ehdr_string_table_slice(self, args);
        if (PyBytes_Check(header_bytes) == 0)
        {
            ret = PyLong_FromLong(2);
        }
        else
        {
            table_len = PySequence_Length(elf_section_header_table);

            header_bytes_char = PyBytes_AsString(header_bytes);

            ret = PyList_New(0);

            for (i = 0; i != table_len; i++)
            {
                section_header = PySequence_GetItem(
                    elf_section_header_table,
                    i);

                name_offset = PyLong_AsLong(
                    PyLong_FromPyBytes(
                        PyDict_GetItem(
                            section_header,
                            PyUnicode_FromString("sh_name")),
                        Py_True));

                PyList_Append(
                    ret,
                    PyUnicode_FromString(header_bytes_char + name_offset));
            }
        }
    }

    return ret;
}

PyObject *
read_dynamic_section(PyObject *self, PyObject *args)
{
    PyObject * ret;

    PyObject * data_seq;
    PyObject * index;
    PyObject * bitness;

    PyObject * new_dyn_dict;

    PyObject * sub_data;
    char * sub_data_char;

    long current_index;
    long one_value_size;
    long bitness_l;
    long index_l;
    long v1;
    long end;

    union
    {
        Elf32_Dyn u32;
        Elf64_Dyn u64;
    } u;

    if (PyArg_ParseTuple(args, "OOO", &data_seq, &index, &bitness) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        bitness_l = PyLong_AsLong(bitness);

        switch (bitness_l)
        {
            case 32:
                one_value_size = sizeof(Elf32_Dyn);
                break;
            case 64:
                one_value_size = sizeof(Elf64_Dyn);
                break;
            default:
                one_value_size = 0;
                break;
        }

        ret = PyList_New(0);
        current_index = 0;
        index_l = PyLong_AsLong(index);
        end = 0;
        while (1)
        {

            memset(&u, 0, sizeof(Elf64_Dyn));

            new_dyn_dict = Py_None;

            v1 = index_l + (current_index * one_value_size);
            sub_data = PySequence_GetSlice(data_seq, v1, v1 + one_value_size);
            sub_data_char = PyBytes_AsString(sub_data);

            switch (bitness_l)
            {
                case 32:
                    memcpy(&u.u32, sub_data_char, sizeof(Elf32_Dyn));
                    break;
                case 64:
                    memcpy(&u.u64, sub_data_char, sizeof(Elf64_Dyn));
                    break;
            }

            switch (bitness_l)
            {
                case 32:
                    if (u.u32.d_tag == 0)
                    {
                        end = 1;
                    }
                    break;
                case 64:
                    if (u.u64.d_tag == 0)
                    {
                        end = 1;
                    }
                    break;
            }

            if (end == 1)
            {
                break;
            }

            new_dyn_dict = PyDict_New();

            switch (bitness_l)
            {
                case 32:
                    PyDict_SetItem(
                        new_dyn_dict,
                        PyUnicode_FromString("d_tag"),
                        PyLong_FromLong(u.u32.d_tag));
                    PyDict_SetItem(
                        new_dyn_dict,
                        PyUnicode_FromString("d_val"),
                        PyLong_FromLong(u.u32.d_un.d_val));
                    PyDict_SetItem(
                        new_dyn_dict,
                        PyUnicode_FromString("d_ptr"),
                        PyLong_FromLong(u.u32.d_un.d_ptr));
                    break;
                case 64:
                    PyDict_SetItem(
                        new_dyn_dict,
                        PyUnicode_FromString("d_tag"),
                        PyLong_FromLong(u.u64.d_tag));
                    PyDict_SetItem(
                        new_dyn_dict,
                        PyUnicode_FromString("d_val"),
                        PyLong_FromLong(u.u64.d_un.d_val));
                    PyDict_SetItem(
                        new_dyn_dict,
                        PyUnicode_FromString("d_ptr"),
                        PyLong_FromLong(u.u64.d_un.d_ptr));
                    break;
            }

            PyList_Append(ret, new_dyn_dict);

            current_index++;
        }
    }

    return ret;
}

PyObject *
get_dynamic_libs_names(PyObject *self, PyObject *args)
{
    PyObject * ret;

    PyObject * dinamics_table;
    PyObject * data_seq;
    PyObject * elf_section_header_table;
    PyObject * ehdr_dict;
    PyObject * program_table;

    PyObject * args2;
    PyObject * header_bytes;
    char * header_bytes_chars;

    PyObject * item;
    PyObject * name;

    long i;
    long offset;
    long dinamics_table_size;

    if (PyArg_ParseTuple(
        args,
        "OOOOO",
        &data_seq,
        &program_table,
        &dinamics_table,
        &elf_section_header_table,
        &ehdr_dict) == 0)
    {
        ret = PyLong_FromLong(1);
    }
    else
    {
        args2 = Py_BuildValue("OOO", data_seq, program_table, dinamics_table);

        header_bytes = get_dyn_string_table_slice(self, args2);
        header_bytes_chars = PyBytes_AsString(header_bytes);

        if (PyBytes_Check(header_bytes) == 0)
        {
            ret = PyLong_FromLong(2);
        }
        else
        {
            dinamics_table_size = PySequence_Length(dinamics_table);

            ret = PyList_New(0);

            for (i = 0; i != dinamics_table_size; i++)
            {
                item = PySequence_GetItem(dinamics_table, i);

                if (PyLong_AsLong(
                    PyDict_GetItem(item, PyUnicode_FromString("d_tag")))
                    == DT_NEEDED)
                {
                    offset = PyLong_AsLong(
                        PyDict_GetItem(item, PyUnicode_FromString("d_ptr")));

                    name = PyUnicode_FromString(header_bytes_chars + offset);

                    PyList_Append(ret, name);
                }
            }
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
            "read_elf_phdr",
            read_elf_phdr,
            METH_VARARGS,
            "reads elf section header using e_ident to know bitness" },
        {
            "read_elf_phdr_x",
            read_elf_phdr_x,
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

        {
            "shdr32_to_dict",
            shdr32_to_dict,
            METH_VARARGS,
            "Reads header item form header table" },

        {
            "shdr64_to_dict",
            shdr64_to_dict,
            METH_VARARGS,
            "Reads header item form header table" },

        {
            "read_elf_section_header_table",
            read_elf_section_header_table,
            METH_VARARGS,
            "reads header table" },

        {
            "phdr32_to_dict",
            phdr32_to_dict,
            METH_VARARGS,
            "Reads header item from header table" },

        {
            "phdr64_to_dict",
            phdr64_to_dict,
            METH_VARARGS,
            "Reads header item from header table" },

        {
            "read_elf_program_header_table",
            read_elf_program_header_table,
            METH_VARARGS,
            "reads header table" },

        {
            "read_elf_section_header_table_names",
            read_elf_section_header_table_names,
            METH_VARARGS,
            "get section headers names" },
        {
            "PyLong_FromPyBytes",
            ExpPyLong_FromPyBytes,
            METH_VARARGS,
            "convert bytes to PyLong" },
        {
            "read_dynamic_section",
            read_dynamic_section,
            METH_VARARGS,
            "read dynamic section" },

        {
            "get_dynamic_libs_names",
            get_dynamic_libs_names,
            METH_VARARGS,
            "Get dianmic libs names required by elf file" },

        { NULL, NULL, 0, NULL } };

static struct PyModuleDef elf_bin_module =
    { PyModuleDef_HEAD_INIT, "elf_bin", NULL, -1, elf_bin_methods };

PyMODINIT_FUNC
PyInit_elf_bin(void)
{
    return PyModule_Create(&elf_bin_module);
}
