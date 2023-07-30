from multiprocessing import Process, Queue

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from spotdl_gui.spotdl_api import SpotdlApi


class WorkerSignals(QObject):
    success = Signal(object)
    error = Signal(object)


class SearchWorker(QRunnable):
    def __init__(self, query):
        super().__init__()
        self.query = query
        self.signals = WorkerSignals()
        self.stopped = False
        self.queue = Queue()

    def kill(self):
        self.stopped = True

    @Slot()
    def run(self):
        def _run():
            api = SpotdlApi(user_auth=True)
            try:
                ret = api.simple_search(self.query)
                self.queue.put(ret)
            except Exception as e:
                self.queue.put(e)

        p = Process(target=_run)
        p.start()

        while ...:
            if not p.is_alive():
                ret = self.queue.get()
                if isinstance(ret, Exception):
                    self.signals.error.emit(ret)
                else:
                    self.signals.success.emit(ret)
                break

            if self.stopped and p.is_alive():
                p.kill()
                break
