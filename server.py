# encoding:utf-8
# !/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.options import options
from common.urls import handlers
from apps_web import handlers as web_handlers
from apps_api import _handlers as api_handler
handlers.extend(api_handler)
handlers.extend(web_handlers)
import sys
from setting import settings
from raven.contrib.tornado import AsyncSentryClient
from application import Application

if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    # parse_config_file(os.path.join(os.path.dirname(__file__),'web_conf.conf'))
    # tornado.options.parse_command_line()
    try:
        port = int(sys.argv[1])
    except:
        port = 7088
    app = Application(handlers,**settings)
    app.listen(port)
    print "Starting development server:",port

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

