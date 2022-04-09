#include "plugin.h"

#include <pygobject.h>
#include <dlfcn.h>
#include <config.h>

static void
sample_py_construct(XfcePanelPlugin *plugin);

XFCE_PANEL_PLUGIN_REGISTER(sample_py_construct);

static SamplePyPlugin *
sample_py_new(XfcePanelPlugin *plugin)
{
    SamplePyPlugin *sample_py;

    PyObject *py_widget_module_name; // Plugin module name as python object to import
    PyObject *py_widget_dict;        // Python context dictionary
    PyObject *py_widget_module;      // Holds the imported widget module
    PyObject *py_widget_class;       // Our plugin class

    // allocating space for out plugin
    sample_py = g_slice_new0(SamplePyPlugin);
    sample_py->plugin = plugin;

    // Need, otherwise giving error undefined PyExc_NotImplemented
    sample_py->library_handler = dlopen("libpython3.10.so", RTLD_LAZY | RTLD_GLOBAL);
    if (sample_py->library_handler == NULL)
    {
        fprintf(stderr, "Error: %s\n", dlerror());
        return NULL;
    }

    // Initializing Python Interpreter
    Py_Initialize();

    // Adding python module search path
    PyObject *sys_path = PySys_GetObject((char *)"path");
    PyList_Append(sys_path, PyUnicode_FromString(PYTHON_SEARCH_PATH));

    // Generating module name as python string
    py_widget_module_name = PyUnicode_FromString(PLUGIN_ID);
    if (py_widget_module_name == NULL)
    {
        PyErr_Print();
        return NULL;
    }

    // Importing python plugin code as module
    py_widget_module = PyImport_Import(py_widget_module_name);
    if (py_widget_module == NULL)
    {
        PyErr_Print();
        return NULL;
    }
    Py_DECREF(py_widget_module_name);

    // Getting python context dictionary
    py_widget_dict = PyModule_GetDict(py_widget_module);
    if (py_widget_dict == NULL)
    {
        PyErr_Print();
        return NULL;
    }
    Py_DECREF(py_widget_module);

    // Getting "PanelPlugin" class from context
    py_widget_class = PyDict_GetItemString(py_widget_dict, "PanelPlugin");
    if (py_widget_class == NULL)
    {
        PyErr_Print();
        return NULL;
    }
    Py_DECREF(py_widget_dict);

    // Verifying class
    if (PyCallable_Check(py_widget_class))
    {
        // creating python object from the initializing class
        sample_py->py_object = PyObject_CallObject(py_widget_class, NULL);
    }
    else
    {
        PyErr_Print();
        fprintf(stderr, "Entry is not Python class");
    }
    Py_DECREF(py_widget_class);

    return sample_py;
}

static void
sample_py_orientation_changed(XfcePanelPlugin *plugin,
                              GtkOrientation orientation,
                              SamplePyPlugin *sample_py)
{
    // TODO: can we pass GtkOrientation as py Gtk.Orientation.<>
    PyObject_CallMethod(sample_py->py_object, "orientation_changed", "(i)", orientation == GTK_ORIENTATION_HORIZONTAL ? 0 : 1);
}

static void
sample_py_free(XfcePanelPlugin *plugin,
               SamplePyPlugin *sample_py)
{

    // calling 'free' method from python object,
    // Most probably ignored if not exist
    PyObject_CallMethod(sample_py->py_object, "free", "");

    // freeing python object and finalizing interpreter
    Py_DECREF(sample_py->py_object);
    Py_Finalize();

    // close the library handler
    dlclose(sample_py->library_handler);

    g_slice_free(SamplePyPlugin, sample_py);
}

static void
sample_py_about(XfcePanelPlugin *plugin,
                SamplePyPlugin *sample_py)
{
    // calling 'about' method from python object,
    PyObject_CallMethod(sample_py->py_object, "about", "");
}

static void
sample_py_construct(XfcePanelPlugin *plugin)
{
    SamplePyPlugin *sample_py;
    GObject *widget;

    sample_py = sample_py_new(plugin);

    // Getting pygobject from python object
    widget = pygobject_get(sample_py->py_object);

    // verifying pygobject
    if (!G_IS_OBJECT(widget))
    {
        printf("Entry is not a python gobject\n");
        return;
    }
    gtk_widget_show_all(GTK_WIDGET(widget));

    // Adding python widget in plugin
    gtk_container_add(GTK_CONTAINER(plugin), GTK_WIDGET(widget));

    xfce_panel_plugin_add_action_widget(plugin, GTK_WIDGET(widget));

    // show the about menue item and connect signal
    xfce_panel_plugin_menu_show_about(plugin);
    g_signal_connect(G_OBJECT(plugin), "about",
                     G_CALLBACK(sample_py_about), sample_py);

    g_signal_connect(G_OBJECT(plugin), "free-data",
                     G_CALLBACK(sample_py_free), sample_py);

    g_signal_connect(G_OBJECT(plugin), "orientation-changed",
                     G_CALLBACK(sample_py_orientation_changed), sample_py);
}