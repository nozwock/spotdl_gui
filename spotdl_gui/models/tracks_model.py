from PySide6 import QtCore
from PySide6.QtCore import Qt

from ..spotdl_api import Song

column_names: dict[int, str] = {
    0: "Album",
    1: "Title",
    2: "Artists",
    3: "Date",
    4: "Duration",
    5: "Link",
}


class TracksModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, tracks: list[Song] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tracks = tracks or []

    def data(self, idx, role):
        if role == Qt.ItemDataRole.DisplayRole:
            col = idx.column()
            if col == 0:
                return self.tracks[idx.row()].album_name
            if col == 1:
                return self.tracks[idx.row()].name
            elif col == 2:
                return ", ".join(self.tracks[idx.row()].artists)
            elif col == 3:
                return self.tracks[idx.row()].date
            elif col == 4:
                duration = self.tracks[idx.row()].duration
                if duration < 1000:  # Should be in seconds, don't ask how...
                    mins, secs = divmod(duration, 60)
                else:  # ms
                    mins, secs = divmod(duration / 1000, 60)

                return f"{int(mins)}:{int(secs) if secs > 9 else f'0{int(secs)}'}"
            elif col == 5:
                return self.tracks[idx.row()].url
            else:
                raise Exception

    def headerData(self, section, orientation, role):
        # NOTE: Section is the index of the column/row being requested.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return column_names[section]

            if orientation == Qt.Orientation.Vertical:
                return section + 1

    def rowCount(self, idx):
        return len(self.tracks)

    def columnCount(self, idx):
        return 6
