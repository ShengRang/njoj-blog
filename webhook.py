#!/usr/bin/env python
# encoding: utf-8

import os
import hmac

import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import tornado.autoreload
from tornado.options import define, options

define('port', default=8080, help='tornado webhook port', type=int)
define('secret', default='njoj-blog', help='hook\'s secret')

def hook():
    os.system('git pull')
    os.system('hexo g')

class WebHookHandler(tornado.web.RequestHandler):
    def post(self):
        hub_signature = self.request.headers.get('X-Hub-Signature')
        github_event = self.request.headers.get('X-Github-Event')
        delivery_id = self.request.headers.get('X-Github-Delivery')
        payload = self.request.body
        print hub_signature
        print github_event
        print delivery_id
        print payload
        if hmac.new(payload, options.secret) != hub_signature:
            raise tornado.web.HTTPError(403)
        else:
            hook()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r'/refresh', ),
                ]
        settings = dict(
                debug = False
                )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application)
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()
