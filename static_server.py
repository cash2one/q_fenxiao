# encoding:utf-8
# !/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.options import options
from apps_web.home import HomeHandler
from tornado.web import url

handlers=[url(r'/([\w\W]*)', HomeHandler,name='home')]
import sys,os
from utils.conf_util import parse_config_file
from setting import settings
from raven.contrib.tornado import AsyncSentryClient
from application import Application

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    parse_config_file(os.path.join(os.path.dirname(__file__),'web_conf.conf'))
    tornado.options.parse_command_line()
    try:
        port = int(sys.argv[1])
    except:
        port = 8002
    app = Application(handlers,**settings)

    app.sentry_client = AsyncSentryClient(
         'http://29ec306286ee48c081d5bebb791035ec:d53aa8788702465d863d3943306975d0@logs.gongzhuhao.com/2'
    )
    #for port in [8012,8013,8010,8011]:
    app.listen(port)
    print "Starting development server:",port

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

