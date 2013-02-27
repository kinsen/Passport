
class AuthLog():
	def __init__(self,db):
		self._db=db

	def add_log(self,log_type,ip_address,tenant_id=None,email=None,remark=None):
		self._db.execute(
			'INSERT INTO auth_log'
			'(TenantId,Email,LogType,Remark,IPAddress,CreateTime)'
			'VALUES (%s,%s,%s,%s,%s,now())',
			tenant_id,email,log_type,remark,ip_address)