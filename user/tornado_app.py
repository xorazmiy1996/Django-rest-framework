import os
import django
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")
django.setup()

from tutorial.wsgi import application

if __name__ == "__main__":
    http_server = HTTPServer(WSGIContainer(application))
    http_server.listen(8000)
    IOLoop.current().start()