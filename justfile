proj_dir := justfile_directory()
ui_dir := proj_dir / "spotdl_gui" / "views"
rc_path := proj_dir / "spotdl_gui" / "assets" / "resource.qrc"

default: build-all

build-all:
    just build-rc {{rc_path}}
    just build-ui {{ui_dir / "about.ui" }}
    just build-ui {{ui_dir / "mainwindow.ui" }}

build-rc rc:
    pyside6-rcc "{{rc}}" -o "{{parent_directory(rc) / file_stem(rc) + '.py'}}"

build-ui ui:
    pyuic6 "{{ui}}" -o "{{parent_directory(ui) / file_stem(ui) + '.py'}}"
    sed -i "s/PyQt6/PySide6/" "{{parent_directory(ui) / file_stem(ui) + '.py'}}"
