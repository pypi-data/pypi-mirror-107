""" Вспомогательные функции

"""

import multiprocessing as _M
import time


class SubProcessMixing(object):
    """ Миксин для инициализации доп процесса внутри класса """

    _started: bool

    _queue: _M.Queue
    _process: _M.Process

    def start(self):
        if self._started:
            self.stop()

        self._queue = _M.Queue(-1)
        self._process = _M.Process(target=self.on_process)
        self._process.start()

        self._started = True

    def stop(self):
        self._queue.put(None)
        while not self._queue.empty():
            time.sleep(0.1)

        self._process.join()
        self._process.terminate()

        self._queue.close()
        self._queue.join_thread()

        self._started = False
