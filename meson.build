project('fontdownloader',
          version: '0.1.0',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
)

i18n = import('i18n')
prefix = get_option('prefix')

localedir = join_paths(prefix, get_option('localedir'))

dependency('libhandy-1', version: '>= 0.90.0')

subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
