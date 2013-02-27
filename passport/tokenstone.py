try:
    import cPickle as pickle
except ImportError:
    import pickle
import time
import logging
from uuid import uuid4


class RedisTokenStoneStore(object):
	def __init__(self,redis_connection,**options):
		self.options={
			"key_prefix":"token_stone",
			"expire":60
		}
		self.options.update(options)
		self.redis=redis_connection

	def prefiexed(self,token):
		return '%s:%s' % (self.options['key_prefix'],token)

	def generate_token(self):
		return uuid4().get_hex()

	def get_token(self,token):
		return self.redis.get(self.prefiexed(token))

	def set_token(self,token,data,expiry=None):
		key=self.prefiexed(token)
		#import pdb
		#pdb.set_trace()
		self.redis.set(key,data)
		expiry=expiry or self.options['expire']
		if expiry:
			self.redis.expire(key,expiry)

	def delete_token(self,token):
		self.redis.delete(self.prefiexed(token))


class RedisTokenStone(object):
	def __init__(self,redis_conn,expire=None):
		self._store=RedisTokenStoneStore(redis_conn)
		self._expire=expire
		self._dirty=False

	def new_token(self,data):
		token=self._store.generate_token()
		self._store.set_token(token,data,self._expire)
		return token

	def get_store(self,token):
		data=self._store.get_token(token)
		self.delete(token)
		return data

	def delete(self,token):
		self._store.delete_token(token)


