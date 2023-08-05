import time
import traceback
from multiprocessing import Process, Queue
from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from ..spotdl_api import DownloaderOptions, Song, SpotdlApi
from . import EVENT_CHECK_DELAY, MessageType


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(object)


# Should do some abstraction maybe...


def _download_run(
    queue: Queue, songs: list[Song], output_dir: Path | None = None
) -> None:
    try:
        api = SpotdlApi()
        if output_dir is not None:
            output = Path(api.downloader.settings["output"])
            api.downloader.settings["output"] = str(
                output_dir.joinpath(output.name).absolute()
            )
        downloaded_songs = api.download_songs(songs)
        api.downloader.progress_handler.close()
        queue.put((MessageType.Success, downloaded_songs))
    except Exception as e:
        queue.put((MessageType.Error, (e, traceback.format_exc())))


class DownloadWorker(QRunnable):
    def __init__(self, songs: list[Song], output_dir: Path | None = None):
        super().__init__()
        self.songs = songs
        self.output_dir = output_dir
        self.signals = WorkerSignals()
        self.stopped = False
        self.queue: Queue[tuple[MessageType, object]] = Queue()

    def kill(self):
        self.stopped = True

    @Slot()
    def run(self) -> None:
        def pkill() -> None:
            if p.is_alive():
                p.kill()

        p = Process(
            target=_download_run, args=[self.queue, self.songs, self.output_dir]
        )
        try:
            p.start()

            while ...:
                if not p.is_alive() or not self.queue.empty():
                    typ, v = self.queue.get()
                    match typ:
                        case MessageType.Success:
                            self.signals.result.emit(v)
                        case MessageType.Error:
                            self.signals.error.emit(v)
                    break

                if self.stopped and p.is_alive():
                    break

                time.sleep(EVENT_CHECK_DELAY)
        except Exception as e:
            self.signals.error.emit((e, traceback.format_exc()))
        finally:
            self.queue.close()
            pkill()
