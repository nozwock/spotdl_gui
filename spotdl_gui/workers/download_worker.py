import time
from multiprocessing import Process, Queue
from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from ..spotdl_api import DownloaderOptions, Song, SpotdlApi
from . import EVENT_CHECK_DELAY


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(object)


# Should do some abstraction maybe...


def _download_run(
    queue: Queue, songs: list[Song], output_dir: Path | None = None
) -> None:
    api = SpotdlApi()
    if output_dir is not None:
        output = Path(api.downloader.settings["output"])
        api.downloader.settings["output"] = str(
            output_dir.joinpath(output.name).absolute()
        )
    try:
        ret = api.download_songs(songs)
        queue.put(ret)
    except Exception as e:
        queue.put(e)


class DownloadWorker(QRunnable):
    def __init__(self, songs: list[Song], output_dir: Path | None = None):
        super().__init__()
        self.songs = songs
        self.output_dir = output_dir
        self.signals = WorkerSignals()
        self.stopped = False
        self.queue = Queue()  # type: ignore

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
                    v = self.queue.get()
                    if isinstance(v, Exception):
                        self.signals.error.emit(v)
                    else:
                        self.signals.result.emit(v)

                    pkill()
                    break

                if self.stopped and p.is_alive():
                    pkill()
                    break

                time.sleep(EVENT_CHECK_DELAY)
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.queue.close()
