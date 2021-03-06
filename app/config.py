import os

from tornado.options import define

define("debug", default=True, help="Debug option")
define("port", default=8000, help="Port to run server")

APP_DIR = os.path.dirname(os.path.realpath(__file__))

settings = {
    "template_path": os.path.join(APP_DIR, "templates"),
    "static_path": os.path.join(APP_DIR, "static")
}