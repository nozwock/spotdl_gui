import time
import traceback
from multiprocessing import Process, Queue

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from ..spotdl_api import SpotdlApi
from ..utils.splitter import Splitter
from . import EVENT_CHECK_DELAY, MessageType


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(object)


def _search_task(queue: Queue, query: list[str]) -> None:
    try:
        api = SpotdlApi()
        songs = api.simple_search(query)
        queue.put((MessageType.Success, songs))
    except Exception as e:
        queue.put((MessageType.Error, (e, traceback.format_exc())))


class SearchWorker(QRunnable):
    def __init__(self, query: str):
        super().__init__()
        self.query = query
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
            target=_search_task,
            args=[self.queue, [s.strip() for s in Splitter().split(self.query)]],
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
