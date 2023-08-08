# spotDL GUI
Simple GUI wrapper over [**spotDL**](https://github.com/spotDL/spotify-downloader), a Spotify downloader.

![preview](https://github.com/nozwock/spotdl_gui/assets/57829219/0f4f7173-1d65-4ae6-a46f-9f5602d86e81)

## Installation
> **Note**\
> Download the executable from the [GitHub release page](https://github.com/nozwock/spotdl_gui/releases) or install using `pipx`.

1. Install `pipx`.
    ```sh
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```
2. Open a new terminal or re-login.
3. Install `spotdl_gui`
    ```sh
    pipx install git+https://github.com/nozwock/spotdl_gui.git
    ```

- Run with `spotdl-gui`

### Prerequisites
**FFmpeg** is required for the GUI and spotDL to work.

On Windows, Install with:
```console
winget install -e --id Gyan.FFmpeg
```

## Usage
### Searches
You can search for multiple items at a time by separating them with a comma `','`. \
For example: `Aurora, Coolio, Full Confession`.

To use a comma as part of your search term without it acting as a separator, you can escape it with the backslash character `'\'`. \
For example: `This here\, will be escaped` will be treated as a literal string `This here, will be escaped`.

#### Reserved search terms
| Term                 | Description                     |
| -------------------- | ------------------------------- |
| `user:saved-tracks`  | Spotify user's favourite tracks |
| `user:all-playlists` | Spotify user's all playlists    |

#### Search prefixes
| Prefix      | Description        |
| ----------- | ------------------ |
| `album:`    | Search by album    |
| `playlist:` | Search by playlist |
| `artist:`   | Search by artist   |

### Downloads
Upon pressing the Download button, the selected tracks will be downloaded. You can choose all tracks at once with `Ctrl+A`, or individually by holding `Ctrl` and clicking on the desired tracks.

## Building
```sh
git clone https://github.com/nozwock/spotdl_gui.git
cd spotdl_gui
poetry install
poetry run spotdl-gui
```

### Building frozen app 
```powershell
poetry run -- pyinstaller `
    --name 'SpotdlGUI' `
    --noupx `
    --onedir `
    --windowed `
    --noconfirm `
    --collect-data pykakasi `
    --collect-data ytmusicapi `
    --copy-metadata spotdl_gui `
    --copy-metadata spotdl `
    --splash resources\splash.png `
    -i resources\icon.ico `
    spotdl_gui\__main__.py
```

- `--strip` for Unix.

# Credits
## Assets
- https://boxicons.com
- https://www.svgrepo.com