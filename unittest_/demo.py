#encoding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.web
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
application = tornado.web.Application([(r"/", MainHandler),])
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(1081)
    tornado.ioloop.IOLoop.instance().start()