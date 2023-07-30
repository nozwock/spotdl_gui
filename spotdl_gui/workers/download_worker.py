import time
from multiprocessing import Process, Queue

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from ..spotdl_api import DownloaderOptions, Song, SpotdlApi
from . import EVENT_CHECK_DELAY


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(object)


# Should do some abstraction maybe...


class DownloadWorker(QRunnable):
    def __init__(
        self,
        songs: list[Song],
    ):
        super().__init__()
        self.songs = songs
        self.signals = WorkerSignals()
        self.stopped = False
        self.queue = Queue()  # type: ignore

    def kill(self):
        self.stopped = True

    @Slot()
    def run(self) -> None:
        def _run(queue: Queue) -> None:
            api = SpotdlApi()
            try:
                ret = api.download_songs(self.songs)
                queue.put(ret)
            except Exception as e:
                queue.put(e)

        def pkill() -> None:
            if p.is_alive():
                p.kill()

        p = Process(target=_run, args=[self.queue])
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

        self.queue.close()
