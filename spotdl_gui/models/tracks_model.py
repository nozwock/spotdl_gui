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
                return ", ".join(self.tracks[idx.row()].artists)
            elif col == 2:
                return self.tracks[idx.row()].date
            elif col == 3:
                duration = self.tracks[idx.row()].duration
                if duration < 1000:  # Should be in seconds, don't ask how...
                    mins, secs = divmod(duration, 60)
                else:  # ms
                    mins, secs = divmod(duration / 1000, 60)

                return f"{int(mins)}:{int(secs) if secs > 9 else f'0{int(secs)}'}"
            elif col == 4:
                return self.tracks[idx.row()].url
            else:
                raise Exception

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section == 0:
                    return "Name"
                elif section == 1:
                    return "Artists"
                elif section == 2:
                    return "Date"
                elif section == 3:
                    return "Duration"
                elif section == 4:
                    return "Link"
                else:
                    raise Exception

            if orientation == Qt.Orientation.Vertical:
                return section + 1

    def rowCount(self, idx):
        return len(self.tracks)

    def columnCount(self, idx):
        return 5
