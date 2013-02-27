from passport.api.http import HTTPClient

def authenticate(keystone_url,username,password,tenant_name=None):
	"""keystone user authenticate"""
	auth_url="%s/tokens" % keystone_url

	body=\
	{
		"auth":
		{
			"passwordCredentials":
			{
				"username":username,
				"password":password
			}
		}
	}

	if tenant_name==None:
		tenant_name=''

	body['auth']['tenantName']=tenant_name

	return HTTPClient().request(auth_url,method="POST",body=body)[1]