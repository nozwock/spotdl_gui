# spotdl_gui

## Installation
```sh
python -m pip install --user pipx
pipx install git+https://github.com/nozwock/spotdl_gui.git
```

- Run with `spotdl-gui`

## Building frozen app 
```sh
pyinstaller -Fsn 'Spotdl GUI' spotdl_gui/__main__.py --collect-data pykakasi --collect-data ytmusicapi
```

# Credits
## Assets
- https://boxicons.com
- https://www.svgrepo.com