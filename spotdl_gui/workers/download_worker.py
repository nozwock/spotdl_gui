import logging
import os
import tempfile
import time
import traceback
from multiprocessing import Process, Queue
from pathlib import Path
from threading import Thread

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from ..spotdl_api import Song, SpotdlApi
from . import EVENT_CHECK_DELAY, MessageType


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(object)
    progress = Signal(object)


# Should do some abstraction maybe...


def _download_run(
    queue: Queue,
    songs: list[Song],
    output_dir: Path,
    log_level: int = logging.DEBUG,
) -> None:
    try:

        def _task() -> None:
            handler = api.downloader.progress_handler
            while ...:
                progress, total = handler.overall_progress, handler.overall_total
                queue.put(
                    (
                        MessageType.Progress,
                        (progress, total),
                    )
                )

                if progress >= total:
                    break

                time.sleep(EVENT_CHECK_DELAY)

        _log_fd, log_path = tempfile.mkstemp()
        os.fdopen(_log_fd).close()

        # Setup logger
        logger = logging.getLogger("spotdl")
        logger.setLevel(log_level)
        fh = logging.FileHandler(log_path, "w")
        fh.setLevel(log_level)
        logger.addHandler(fh)

        api = SpotdlApi()
        output = Path(api.downloader.settings["output"])
        api.downloader.settings["output"] = str(
            output_dir.joinpath(output.name).absolute()
        )

        progress_thread = Thread(target=_task)
        progress_thread.start()

        from ..utils import pythonw_patches  # noqa: F401

        downloaded_songs = api.download_songs(songs)
        # Don't send the return value to the main GUI thread as we aren't making full use of it.
        api.downloader.progress_handler.close()

        queue.put(
            (
                MessageType.Success,
                (
                    sum(
                        1 for _, path in downloaded_songs if path is not None
                    ),  # Number of succesfully downloaded songs
                    output_dir.absolute(),
                    log_path,
                ),
            )
        )

    except Exception as e:
        os.remove(log_path)

        queue.put((MessageType.Error, (e, traceback.format_exc())))
    finally:
        progress_thread.join()


class DownloadWorker(QRunnable):
    def __init__(
        self,
        songs: list[Song],
        output_dir: Path,
        log_level: int = logging.DEBUG,
    ):
        super().__init__()
        self.songs = songs
        self.output_dir = output_dir
        self.log_level = log_level
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
            target=_download_run,
            args=[self.queue, self.songs, self.output_dir, self.log_level],
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
                        case MessageType.Progress:
                            self.signals.progress.emit(v)
                            continue
                    break

                if self.stopped and p.is_alive():
                    break

                time.sleep(EVENT_CHECK_DELAY)
        except Exception as e:
            self.signals.error.emit((e, traceback.format_exc()))
        finally:
            self.queue.close()
            pkill()
