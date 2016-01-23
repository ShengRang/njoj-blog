#!/usr/bin/env python
# encoding: utf-8

import os
import hmac
from hashlib import sha1

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
        digestmod, hexdigest = hub_signature.split('=')
        if digestmod != 'sha1':
            raise tornado.web.HTTPError(404)
        github_event = self.request.headers.get('X-Github-Event')
        delivery_id = self.request.headers.get('X-Github-Delivery')
        payload = self.request.body
        print hub_signature
        print github_event
        print delivery_id
        print payload
        if hmac.new(options.secret, payload, sha1).hexdigest() != hexdigest:
            raise tornado.web.HTTPError(403)
        else:
            hook()
    def get(self):
        self.write('hello')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/refresh', WebHookHandler),
        ]
        settings = dict(
            debug = True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()
