from passport.session import RedisSession
from passport.tokenstone import RedisTokenStone
from passport.api import keystone
from passport import settings
from passport import exception
from passport import utils
from passport.core.site import SiteManager

class AuthCenter():
	def __init__(self,request,session,token_stone,session_store):
		self._request       =request
		self._session       =session
		self._token_stone   =token_stone
		self._session_store =session_store

	def add_auth_token(self,return_url):
		token        = self._token_stone.new_token(self._session.id)
		site_manager =SiteManager(self._request.application.db)
		site         =site_manager.get_site_by_url(return_url)
		if site:
			print 'site not null'
			if not self._session.__contains__("auth_sites"):
				self._session["auth_sites"]=[]
			if not self._session['auth_sites'].__contains__(site.SiteId):
				self._session['auth_sites'].append(site.SiteId)
			self._session.save()

		return token


	def get_auth_by_token(self,token):
		"""
		get auth user's infomation by user's token,
		if token verify,return user's info
		else return none
		"""
		session_id=self._token_stone.get_store(token)
		
		if session_id:
			return RedisSession(self._session_store,session_id)['user']

		return None


	def login(self,username,password):
		keystone_url="%(protocol)s://%(host)s:%(port)d/%(version)s" % \
						settings.KEYSTONE_API_CONF

		try:
			access=keystone.authenticate(keystone_url,username,password)
		except Exception as e:
			raise exception.LoginError(e.message)

		self._session['user']=access
		return self.add_auth_token(self._request.return_url)

	def logout(self):
		"""
		delete user's info and auth sites
		return user's auth sites or none
		"""
		print self._session.id
		auth_sites=self._session['auth_sites'] \
			if self._session.__contains__("auth_sites") else None

		sites=None
		if auth_sites:
			site_manager =SiteManager(self._request.application.db)
			sites        =site_manager.get_sites_by_id(auth_sites)
			del self._session['auth_sites']
		if self._session.__contains__('user'):
			del self._session['user']
			self._session.save()
		return sites




