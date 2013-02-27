import json
from passport.handler.base import BaseHandler
import pdb

def get_return_url(request,token):
	url=request.return_url
	pos=url.find('?')

	if pos>0:
		url=url[0:pos]
		url+='?token=%s' % token
		queryparams=request.return_url[pos+1:].split('&')
		for item in queryparams:
			param=item.split('=',2)
			if param[0]=='token':
				continue
			url+='&'
			url+='%s=%s' % (param[0],param[1])
	else:
		url+='?token=%s' % token
	return url





class AuthHandler(BaseHandler):
	def get(self,token):
		access =self.auth_center.get_auth_by_token(token)
		result ={"result": True if access else False,"access":access}
		self.set_header('auth_result',json.dumps(result))



class LoginHandler(BaseHandler):
	def get(self):
		if self.is_logged_in:
			token=self.auth_center.add_auth_token(self.return_url)
			self.redirect(get_return_url(self,token))
		else:
			self.render("login.html")

	def post(self):
		email=self.get_argument('email',None)
		password=self.get_argument('password',None)
		token=self.auth_center.login(email,password)
		self.redirect(get_return_url(self,token))

class LogoutHandler(BaseHandler):
	def get(self):
		sites=self.auth_center.logout()
		self.render('logout.html',sites=sites)
