import passport.utils

class SiteManager():
	def __init__(self,db):
		self._db=db

	def get_all_site(self):
		return self._db.query('SELECT * FROM site')

	def get_site(self,domain):
		return self._db.get('SELECT * FROM site WHERE SiteUrl= %s',domain)

	def get_site_by_url(self,url):
		return self.get_site(passport.utils.get_domain_from_url(url))

	def get_sites_by_id(self,id_list):
		return self._db.query('SELECT * FROM site WHERE SiteId in (%s)' % \
			','.join(map(str,id_list)))