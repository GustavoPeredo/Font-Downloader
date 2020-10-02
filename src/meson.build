pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'fontdownloader')
gnome = import('gnome')

gnome.compile_resources('fontdownloader',
  'fontdownloader.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

dependency('libhandy-1', version: '>= 0.90.0')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'fontdownloader.in',
  output: 'fontdownloader',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

fontdownloader_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'webfonts.json',
]

install_data(fontdownloader_sources, install_dir: moduledir)
