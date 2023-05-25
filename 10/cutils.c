#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <Python.h>

PyObject* cutils_loads(PyObject* self, PyObject* args){
    PyObject *dict = NULL;
    PyObject *key = NULL;
    PyObject *value = NULL;

    if (!(dict = PyDict_New()))
     {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    char *input_string;
    char *json_string;
    char *pch;
    char *pch2;
    char *pch3;
    char *pointers[100000];
    if(!PyArg_ParseTuple(args, "s", &input_string))
    {
        return NULL;
    }

    json_string = strdup(input_string);
    pch = strtok(json_string,"{},");
    int i = 0;
    int l = 0;
    int k = 0;
    while (pch != NULL)
    {
        pointers[i] = pch;

        pch = strtok(NULL, "{},");
        i++;
    }
    for (int j = 0; j < i; j++)
    {
        pch = strtok(pointers[j],":");
        if (pch == NULL) break;
        k = 0;
        l = strlen(pch);
        pch2 = pch;
        k = k + 2;
        pch2 = pch2 + 2 * sizeof(char);
        if (pch[l-1] == 34)
        {
            k++;
            k++;
            pch2 = pch2 + sizeof(char);
        }
        char buff[50];
        strcpy(buff, "\0");
        strncat(buff, pch2, l-k);
        key = Py_BuildValue("s", buff);
        pch = strtok(NULL, ":");
        if (pch == NULL) break;
        k = 0;
        l = strlen(pch);
        pch2 = pch;
        int isint = 0;
        if (pch[0] == 32)
           {
                k++;
                pch2 = pch2 + sizeof(char);
           }
        if (pch[l-1] == 34)
        {
            k++;
            k++;
            pch2 = pch2 + sizeof(char);
        }
        else isint = 1;
          char buff2[50];
        strcpy(buff2, "\0");
        strncat(buff2, pch2, l-k);

        if (isint)
        {
            value = Py_BuildValue("b", atoi(buff2));
        }
        else
            value = Py_BuildValue("s", buff2);

        PyDict_SetItem(dict, key, value);

    }
    return dict;
}

PyObject* cutils_dumps(PyObject* self, PyObject* args){
    PyObject *key, *value, *json_string;
    PyObject* dict;
    PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict);
    Py_ssize_t pos = 0;

    char *buff;
    int first_entry = 1;
    buff = (char *) malloc(10*sizeof(char));
    strcpy(buff, "{\0");

    while (PyDict_Next(dict, &pos, &key, &value))
    {
        if (PyUnicode_Check(value))
        {
            buff = (char *) realloc(buff, strlen(PyUnicode_AsUTF8(key)) + strlen(PyUnicode_AsUTF8(value)) + strlen(buff) + 10);
            if (first_entry == 1)
                first_entry = 0;
            else strcat(buff,", ");
            strcat(buff,"\"");
            strcat(buff, PyUnicode_AsUTF8(key));
            strcat(buff,"\": \"");
            strcat(buff, PyUnicode_AsUTF8(value));
            strcat(buff,"\"");
        }
        else
        {
            char buff_value[sizeof(int)*8+1];
            itoa(PyLong_AsLong(value), buff_value, 10);
            buff = (char *) realloc(buff, strlen(PyUnicode_AsUTF8(key)) + strlen(buff_value) + strlen(buff) + 10);
            if (first_entry == 1)
                first_entry = 0;
            else strcat(buff,", ");
            strcat(buff,"\"");
            strcat(buff, PyUnicode_AsUTF8(key));
            strcat(buff,"\": ");
            strcat(buff, buff_value);
        }
    }
    strcat(buff,"}");
    json_string = Py_BuildValue("s", buff);
    return json_string;
}

static PyMethodDef methods[] = {
    {"loads", cutils_loads, METH_VARARGS, "loads"},
    {"dumps", cutils_dumps, METH_VARARGS, "dumps"},
    {NULL, NULL, 0, NULL}
};



static struct PyModuleDef cutilsmodule = {
    PyModuleDef_HEAD_INIT,
    "cutils",
    "Module for my first c api code.",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_cutils(void)
{
    return PyModule_Create( &cutilsmodule );
}
