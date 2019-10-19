#__*__coding:utf-8__*__
import hashlib

def has_password(password):
	"""
	密码加密(加盐+md5)
	:param password:
	:return:
	"""
	md5 = hashlib.md5(("天王盖地虎").encode('utf-8'))
	md5.update(password.encode('utf-8'))
	return md5.hexdigest()




