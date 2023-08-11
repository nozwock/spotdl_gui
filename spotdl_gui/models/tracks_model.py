from dataclasses import dataclass
from typing import Any, Callable

from PySide6 import QtCore
from PySide6.QtCore import Qt

from ..spotdl_api import Song


class TracksModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, tracks: list[Song] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tracks: list[Song] = tracks or []

        def _get_duration(row: int):
            duration = self.tracks[row].duration
            if duration < 1000:  # Should be in seconds, don't ask how...
                mins, secs = divmod(duration, 60)
            else:  # ms
                mins, secs = divmod(duration / 1000, 60)
            return f"{int(mins)}:{int(secs) if secs > 9 else f'0{int(secs)}'}"

        @dataclass
        class DataMapValue:
            column_name: str
            get_data: Callable[[int], Any]

        self.data_map: dict[int, DataMapValue] = {
            0: DataMapValue("Album", lambda row: self.tracks[row].album_name),
            1: DataMapValue("Title", lambda row: self.tracks[row].name),
            2: DataMapValue("Artists", lambda row: ", ".join(self.tracks[row].artists)),
            3: DataMapValue("Date", lambda row: self.tracks[row].date),
            4: DataMapValue("Duration", lambda row: _get_duration(row)),
            5: DataMapValue("Link", lambda row: self.tracks[row].url),
        }

    def data(  # type: ignore[override]
        self, idx: QtCore.QModelIndex | QtCore.QPersistentModelIndex, role: int
    ) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data_map[idx.column()].get_data(idx.row())

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.data_map[section].column_name

            if orientation == Qt.Orientation.Vertical:
                return section + 1

    def rowCount(self, idx):
        return len(self.tracks)

    def columnCount(self, idx):
        return len(self.data_map)
