from PySide6 import QtCore
from PySide6.QtCore import Qt

from spotdl_gui.spotdl_api import Song


class TracksModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, tracks: list[Song] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tracks = tracks or []

    def data(self, idx, role):
        if role == Qt.ItemDataRole.DisplayRole:
            col = idx.column()
            if col == 0:
                return self.tracks[idx.row()].name
            elif col == 1:
                return self.tracks[idx.row()].url
            else:
                raise Exception

    def rowCount(self, idx):
        return len(self.tracks)

    def columnCount(self, idx):
        return 2
