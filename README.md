# spotdl_gui

![preview](https://github.com/nozwock/spotdl_gui/assets/57829219/0f4f7173-1d65-4ae6-a46f-9f5602d86e81)

### Reserved search terms

| Term                 | Description                     |
| -------------------- | ------------------------------- |
| `user:saved-tracks`  | Spotify user's favourite tracks |
| `user:all-playlists` | Spotify user's all playlists    |

### Search prefixes

| Prefix      | Description        |
| ----------- | ------------------ |
| `album:`    | Search by album    |
| `playlist:` | Search by playlist |
| `artist:`   | Search by artist   |

## Installation
1. Install `pipx`.
    ```sh
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```
2. Re-login if on Windows, else open a new terminal.
3. Install `spotdl_gui`
    ```sh
    pipx install git+https://github.com/nozwock/spotdl_gui.git
    ```

- Run with `spotdl-gui`

## Building frozen app 
```console
pyinstaller -Fn 'Spotdl GUI' spotdl_gui\__main__.py --collect-data pykakasi --collect-data ytmusicapi --copy-metadata spotdl_gui --copy-metadata spotdl
```

- `pyinstaller -Fsn` for Unix.

# Credits
## Assets
- https://boxicons.com
- https://www.svgrepo.com