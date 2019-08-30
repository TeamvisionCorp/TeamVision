#coding=utf-8
# entry point for the websocket loop
import gevent.monkey
gevent.monkey.patch_thread()

import gevent.socket
import redis
import os
redis.connection.socket = gevent.socket
os.environ.update(DJANGO_SETTINGS_MODULE='teamvision.settings')

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()
