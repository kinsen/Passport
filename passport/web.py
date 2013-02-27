import os.path
import redis
import tornado.web
import tornado.httpserver
import tornado.database
from tornado.options import define, options
import passport.handler.base
from passport.handler.auth import LoginHandler,LogoutHandler,AuthHandler
from passport.session import RedisSessionStore

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="plsql database host")
define("mysql_database", default="passport", help="plsql database name")
define("mysql_user", default="root", help="plsql database user")
define("mysql_password", default="123", help="plsql database pwd")
define("redis_host",default="localhost",help="redis host")
define("redis_port",default=6379,help="run redis on the given port",type=int)

class HomeHandler(passport.handler.base.BaseHandler):
	def get(self):
		self.session['name']='hello'
		self.set_header('xxx-token','good joib')
		self.write(self.return_url)

class HelloHandler(passport.handler.base.BaseHandler):
	def get(self):
		self.write(str(self.is_logged_in))

class LogHandler(passport.handler.base.BaseHandler):
	def get(self):
		from passport.core.authlog import AuthLog
		from passport.enums import AUTH_LOG_TYPE
		log=AuthLog(self.application.db)
		log.add_log(AUTH_LOG_TYPE.LOGIN,'127.0.0.1')

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
			(r"/",HomeHandler),
			(r"/hello",HelloHandler),
			(r"/log",LogHandler),
			(r"/login",LoginHandler),
			(r"/logout",LogoutHandler),
			(r"/auth/(\w+)",AuthHandler)
		]
		self.redis_connection = redis.Redis(host=options.redis_host, port=options.redis_port, db=0)
		self.session_store = RedisSessionStore(self.redis_connection)

		settings=dict(
			title=u"Passport",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies=True,
			permanent_session_lifetime = 1,
			redis_server = True,
			cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)

		self.db=tornado.database.Connection(
			host=options.mysql_host,
			database=options.mysql_database,
			user=options.mysql_user,
			password=options.mysql_password
		)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()