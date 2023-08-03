import time
from multiprocessing import Process, Queue

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from ..spotdl_api import SpotdlApi
from ..utils.splitter import Splitter
from . import EVENT_CHECK_DELAY


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(object)


def _search_run(queue: Queue, query: list[str]) -> None:
    api = SpotdlApi()
    try:
        ret = api.simple_search(query)
        queue.put(ret)
    except Exception as e:
        queue.put(e)


class SearchWorker(QRunnable):
    def __init__(self, query: str):
        super().__init__()
        self.query = query
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
            target=_search_run,
            args=[self.queue, [s.strip() for s in Splitter().split(self.query)]],
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
