# spotdl_gui

## Installation
```sh
pipx install git+https://github.com/nozwock/spotdl_gui.git
```

## Building frozen app 
```sh
pyinstaller -Fsn 'Spotdl GUI' spotdl_gui/__main__.py --collect-data pykakasi --collect-data ytmusicapi
```