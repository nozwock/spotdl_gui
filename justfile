proj_dir := justfile_directory()
ui_dir := proj_dir / "spotdl_gui" / "views"
rc_path := proj_dir / "spotdl_gui" / "assets" / "resource.qrc"

ui_list := "about.ui mainwindow.ui settings.ui"

default: build-all

@build-all:
    just build-rc {{rc_path}}
    for ui in {{ui_list}}; do just build-ui "{{ui_dir}}/$ui"; done

@build-rc rc:
    echo "Compiling Resource {{rc}}"
    pyside6-rcc "{{rc}}" -o "{{parent_directory(rc) / file_stem(rc) + '.py'}}"

@build-ui ui:
    echo "Compiling Ui {{ui}}"
    pyuic6 "{{ui}}" -o "{{parent_directory(ui) / file_stem(ui) + '.py'}}"
    sed -i "s/PyQt6/PySide6/" "{{parent_directory(ui) / file_stem(ui) + '.py'}}"
