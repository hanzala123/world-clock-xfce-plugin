#ifndef _SAMPLE_PY_PLUGIN_
#define _SAMPLE_PY_PLUGIN_

#include <gtk/gtk.h>
#include <libxfce4panel/libxfce4panel.h>
#include <Python.h>

G_BEGIN_DECLS
typedef struct
{
    XfcePanelPlugin *plugin;
    PyObject* py_object;
    void* library_handler;
    
} SamplePyPlugin;

G_END_DECLS
#endif