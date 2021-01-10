import asyncio
import json
import logging
from typing import Union

import tornado
from tornado import httputil
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError

from app.constants import OPEN, OPEN_MESSAGE, LOG_FILE_NAME, MESSAGE
# from app.log_reader import LogReader
from typing import Optional, Awaitable

logger = logging.getLogger("app")


class IndexHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        logger.info("New request")
        self.render("index.html")


class SocketHandler(WebSocketHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        pass

    def __init__(
            self,
            application: tornado.web.Application,
            request: httputil.HTTPServerRequest,
    ):
        super().__init__(application, request)
        logger.info("New socket")
        self.conn_open = True

    def initialize(self):
        pass

    async def read_logs(self, file_desc):
        file_desc.seek(0, 2)
        while self.conn_open:
            lines = file_desc.readlines()
            if not lines:
                await asyncio.sleep(0.1)
                continue
            yield "\n".join(lines)

    async def start_logging(self):
        with open(LOG_FILE_NAME, 'r') as file:
            file_size = file.tell()
            file.seek(max(file_size - 1024, 0), 0)
            lines = file.readlines()
            if len(lines) >= 10:
                lines = lines[-10:]
            self.send_message(action=MESSAGE, message="\n".join(lines))
            # log_reader = LogReader(file)
            while self.conn_open:
                async for log in self.read_logs(file):
                    self.send_message(action=MESSAGE, message=log)

    async def open(self, *args: str, **kwargs: str):
        self.send_message(action=OPEN, message=OPEN_MESSAGE)
        logger.info("Open")
        # asyncio.run(self.start_logging())
        await self.start_logging()

    def on_close(self):
        self.conn_open = False
        logger.info("Closed ws")
        logger.warning("WS_CLOSED")

    def send_message(self, action, **data):
        message = {
            "action": action,
            "data": data
        }

        try:
            self.write_message(json.dumps(message))
        except WebSocketClosedError:
            self.conn_open = False
            logger.warning("WS_CLOSED" + "Could Not send Message: " + json.dumps(message))
            self.close()
