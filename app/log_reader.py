import logging
import time

from app.constants import LINES

logger = logging.getLogger("app")


class LogReader:
    def __init__(self, file_desc):
        self.file_desc = file_desc

    def read_logs(self):
        self.file_desc.seek(0, 2)
        while True:
            lines = self.file_desc.readlines()
            if not lines:
                time.sleep(0.1)
                continue
            yield "\n".join(lines)
