project('xfce-py-plugin', 'c', default_options : 'prefix=/usr')

dependencies = [
	dependency('gtk+-3.0'),
	dependency('pygobject-3.0'),
	dependency('libxfce4panel-2.0'),
	meson.get_compiler('c').find_library('dl', required: true),
	dependency('python3-embed')]

plugin_path = get_option('prefix') + '/' + get_option('libdir') + '/xfce4/panel/plugins'
py_plugin_path = plugin_path + '/python'
plugin_id = 'world-clock-plugin'

config = configuration_data()
config.set('PLUGIN_ID', plugin_id)
config.set('PYTHON_SEARCH_PATH', py_plugin_path)
configure_file(input: 'config.h.in',
	output: 'config.h',
	configuration: config)

library('world-clock-plugin', 'src/plugin.c', dependencies: dependencies,
	install: true,
	install_dir: plugin_path)

install_data('src/plugin.py', install_dir: py_plugin_path,
	rename: plugin_id + '.py')

install_data('plugin.desktop', install_dir: get_option('prefix') + '/' + get_option('datadir') + '/xfce4/panel/plugins/', rename: plugin_id + '.desktop')