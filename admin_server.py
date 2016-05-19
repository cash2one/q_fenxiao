# encoding:utf-8
# !/usr/bin/env python

import tornado.ioloop
import tornado.web
import sys
from setting import admin_settings
from application import Application
from common.urls import handlers
from apps_admin import handlers as admin_handlers
handlers.extend(admin_handlers)

from apps_drp import handlers as drp_handlers
handlers.extend(drp_handlers)
from apps_supply import handlers as supply_handlers
handlers.extend(supply_handlers)


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 7788
    app = Application(handlers,**admin_settings)
    app.listen(port)
    print "Starting development server:",port
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)

    tornado.ioloop.IOLoop.instance().start()