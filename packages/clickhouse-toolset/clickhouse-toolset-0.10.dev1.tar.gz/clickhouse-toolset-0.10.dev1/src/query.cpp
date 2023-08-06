#include <iostream>
#include <map>
#include <set>
#include <Common/Exception.h>

#include <Python.h>

#include "ClickHouseQuery.h"


static std::string PyObject_AsString(PyObject * obj)
{
    PyObject * o = PyObject_Str(obj);
    PyObject * str = PyUnicode_AsEncodedString(o, "utf-8", "~");
    std::string s = PyBytes_AsString(str);
    Py_DECREF(str);
    Py_DECREF(o);
    return s;
}


static PyObject * format(PyObject *, PyObject * args)
{
    char * query;

    if (!PyArg_ParseTuple(args, "s", &query))
        return NULL;

    try
    {
        auto formattedQuery = ClickHouseQuery::format(query);
        return Py_BuildValue("s", formattedQuery.data());
    }
    catch (DB::Exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.displayText().c_str());
        return NULL;
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject * replaceTables(PyObject *, PyObject * args, PyObject * keywds)
{
    char * query;
    PyObject * replacementsDict;
    char const * default_database = "";
    static const char * kwlist[] = {"query", "replacements", "default_database", NULL};
    if (!PyArg_ParseTupleAndKeywords(
            args, keywds, "sO!|s", const_cast<char **>(kwlist), &query, &PyDict_Type, &replacementsDict, &default_database))
        return NULL;

    std::map<std::pair<std::string, std::string>, std::pair<std::string, std::string>> replacements;
    PyObject *key, *value;
    Py_ssize_t pos = 0;

    while (PyDict_Next(replacementsDict, &pos, &key, &value))
    {
        if (!PyTuple_Check(key))
        {
            PyErr_SetString(PyExc_ValueError, "Key replacement must be a tuple");
            return NULL;
        }
        if (PyTuple_Size(key) != 2)
        {
            PyErr_SetString(PyExc_ValueError, "Key replacement tuple must contain 2 elements");
            return NULL;
        }
        if (!PyTuple_Check(value))
        {
            PyErr_SetString(PyExc_ValueError, "Value replacement must be a tuple");
            return NULL;
        }
        if (PyTuple_Size(value) != 2)
        {
            PyErr_SetString(PyExc_ValueError, "Value replacement tuple must contain 2 elements");
            return NULL;
        }
        replacements.emplace(
            std::make_pair(PyObject_AsString(PyTuple_GetItem(key, 0)), PyObject_AsString(PyTuple_GetItem(key, 1))),
            std::make_pair(PyObject_AsString(PyTuple_GetItem(value, 0)), PyObject_AsString(PyTuple_GetItem(value, 1))));
    }

    try
    {
        auto rewrittenQuery = ClickHouseQuery::replaceTables(default_database, query, replacements);
        return Py_BuildValue("s", rewrittenQuery.data());
    }
    catch (DB::Exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.displayText().c_str());
        return NULL;
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject * tables(PyObject *, PyObject * args, PyObject * keywds)
{
    char * query;
    char const * default_database = "";
    static const char * kwlist[] = {"query", "default_database", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|s", const_cast<char **>(kwlist), &query, &default_database))
        return NULL;

    try
    {
        auto tablesInQuery(ClickHouseQuery::tables(default_database, query));
        PyObject * l = PyList_New(tablesInQuery.size());
        int i = 0;
        for (const auto &table : tablesInQuery)
        {
            PyObject * o = Py_BuildValue("(ss)", table.first.data(), table.second.data());
            PyList_SetItem(l, i++, o);
        }
        return l;
    }
    catch (DB::Exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.displayText().c_str());
        return NULL;
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject * tableIfIsSimpleQuery(PyObject *, PyObject * args, PyObject * keywds)
{
    char * query;
    char const * default_database = "";
    static const char * kwlist[] = {"query", "default_database", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|s", const_cast<char **>(kwlist), &query, &default_database))
        return NULL;

    try
    {
        if (auto table = ClickHouseQuery::tableIfIsSimpleQuery(default_database, query))
        {
            return Py_BuildValue("(ss)", table->first.data(), table->second.data());
        }
        return Py_BuildValue("");
    }
    catch (std::exception & e)
    {
        return Py_BuildValue("");
    }
}

static std::optional<std::vector<std::string>>
parseStringIterable(PyObject *args)
{
    PyObject *obj;
    PyObject *iterator;
    /* We check that the object passed is iterable and explicitly discard strings */
    if (!PyArg_ParseTuple(args, "O", &obj) || PyUnicode_Check(obj) || !(iterator = PyObject_GetIter(obj)))
    {
        PyErr_SetString(PyExc_ValueError, "Input must be an iterable object containing strings");
        return {};
    }

    std::vector<std::string> types;
    while (PyObject *item = PyIter_Next(iterator))
    {
        if (!PyUnicode_Check(item))
        {
            Py_DECREF(item);
            Py_DECREF(iterator);
            PyErr_SetString(PyExc_ValueError, "Input must be an iterable object containing strings");
            return {};
        }
        types.emplace_back(PyObject_AsString(item));
        Py_DECREF(item);
    }
    Py_DECREF(iterator);

    return types;
}

static PyObject *
leastSupertype(PyObject *, PyObject * args)
{
    auto types = parseStringIterable(args);
    if (!types)
    {
        return NULL;
    }

    try
    {
        auto ret = ClickHouseQuery::leastSupertype(*types);
        return Py_BuildValue("s", ret.data());
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject *
mostSubtype(PyObject *, PyObject * args)
{
    auto types = parseStringIterable(args);
    if (!types)
    {
        return NULL;
    }

    try
    {
        auto ret = ClickHouseQuery::mostSubtype(*types);
        return Py_BuildValue("s", ret.data());
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}


static PyMethodDef CHToolsetQueryMethods[]
    = {{"format", format, METH_VARARGS, NULL},
       {"replace_tables", (PyCFunction)replaceTables, METH_VARARGS | METH_KEYWORDS, NULL},
       {"tables", (PyCFunction)tables, METH_VARARGS | METH_KEYWORDS, NULL},
       {"table_if_is_simple_query", (PyCFunction)tableIfIsSimpleQuery, METH_VARARGS | METH_KEYWORDS, NULL},
       {"least_supertype", leastSupertype, METH_VARARGS, NULL},
       {"most_subtype", mostSubtype, METH_VARARGS, NULL},
       {NULL, NULL, 0, NULL}};

static struct PyModuleDef chquerymodule
    = {PyModuleDef_HEAD_INIT,
       "chtoolset._query", /* name of module */
       NULL, /* module documentation, may be NULL */
       -1, /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
       CHToolsetQueryMethods,
       NULL,
       NULL,
       NULL,
       NULL};

PyMODINIT_FUNC PyInit__query(void)
{
    return PyModule_Create(&chquerymodule);
}
