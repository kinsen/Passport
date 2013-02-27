import sys
import traceback
from tornado.web import RequestHandler
from passport.session import RedisSession, Session
from passport.tokenstone import RedisTokenStone
from passport import settings

def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "<br/>".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str

class BaseHandler(RequestHandler):
	def _handle_request_exception(self, e):
		self.finish(format_exception(e))


	@property
	def session(self):
		if hasattr(self,'_session'):
			return self._session
		else:
			self.require_setting('permanent_session_lifetime','session')
			expires=self.settings['permanent_session_lifetime'] or None

			if 'redis_server' in self.settings and self.settings['redis_server']:
				sessionid=self.get_secure_cookie('sid')
				self._session=RedisSession(self.application.session_store,
					sessionid,expires_days=expires)

				if not sessionid:
					self.set_secure_cookie('sid',self._session.id,
											expires_days=expires)
			else:
				self._session=Session(self.get_secure_cookie,
										self.set_secure_cookie,
										expires_days=expires)
		return self._session


	@property
	def auth_token(self):
		if hasattr(self,'_auth_token'):
			return self._auth_token
		else:
			expires=self.settings.get('authencation_token_lifetime',None)
			self._auth_token=RedisTokenStone(self.application.redis_connection,expires)

		return self._auth_token


	@property
	def auth_center(self):
		if hasattr(self,'_auth_center'):
			return self._auth_center
		else:
			from passport.authcenter import AuthCenter
			self._auth_center=AuthCenter(self,self.session,
				self.auth_token,self.application.session_store)

		return self._auth_center

	@property
	def return_url(self):
		return self.get_argument('return_url',settings.DEFAULT_RETURN_URL)

	@property
	def is_logged_in(self):
		return 'user' in self.session