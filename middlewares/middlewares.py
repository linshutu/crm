#__*__coding:utf-8__*__
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,render
import re

class IsLogin(MiddlewareMixin):
	"""
	验证用户是否登录
	"""
	def process_request(self,request):
		next_url = request.path_info
		white_list = ['/login/','/is_login/', '/register/','/add_register/','/xadmin/.*']
		for url in white_list:
			ret = re.match(url,next_url)
			if ret or request.session.get("is_login"):
				return
		else:
			return redirect('/login/')
