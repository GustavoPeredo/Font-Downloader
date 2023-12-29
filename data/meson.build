iconsdir = get_option('datadir') / 'icons' / 'hicolor'
foreach size: ['scalable', 'symbolic']
  install_subdir('icons/hicolor/' + size, install_dir: iconsdir)
endforeach

desktop_file = i18n.merge_file(
  input: 'org.gustavoperedo.FontDownloader.desktop.in',
  output: 'org.gustavoperedo.FontDownloader.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'org.gustavoperedo.FontDownloader.appdata.xml.in',
  output: 'org.gustavoperedo.FontDownloader.appdata.xml',
  type: 'xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'metainfo')
)

appstreamcli = find_program('appstreamcli', required: false)
if appstreamcli.found()
  test('Validate appstream file',
    appstreamcli,
    args: ['validate', '--no-net', '--explain', appstream_file],
    workdir: meson.current_build_dir()
  )
endif

install_data('org.gustavoperedo.FontDownloader.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif
