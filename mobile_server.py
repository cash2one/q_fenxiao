# encoding:utf-8
# !/usr/bin/env python

import tornado.ioloop
import tornado.web
from common.urls import handlers
from apps_mobile import handlers as mobile_handlers
handlers.extend(mobile_handlers)
import sys
from setting import mobile_settings
from application import Application

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 9090
    app = Application(handlers,**mobile_settings)
    app.listen(port)
    print "Starting development server:",port

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

