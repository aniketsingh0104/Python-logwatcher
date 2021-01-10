import tornado.web
import logging
import logging.config

import tornado.ioloop
from tornado.options import options

from app.config import settings
from app.handlers import IndexHandler, SocketHandler


def main():
    # setup logger
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    # set log format
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)

    urls = [
        (r'/', IndexHandler),
        (r'/ws', SocketHandler)
    ]

    application = tornado.web.Application(
        urls,
        debug=options.debug,
        autoreload=options.debug,
        **settings
    )

    # Start Server with options
    logger.info(f"Starting App on Port: {options.port} with Debug Mode: {options.debug}")

    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


