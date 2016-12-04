from threading import Timer

import sys


class RepeatingTimer(object):
    """Based on RepeatedTimer in http://stackoverflow.com/a/38317060

    Should not stop if the function raises an error.
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        try:
            self.function(*self.args, **self.kwargs)
        except:
            # Prevents the repeated timer from stopping
            print("RepeatedTimer failed:{}".format(sys.exec_info()[0]))
        finally:
            self.start()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
