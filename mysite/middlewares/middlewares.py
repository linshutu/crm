#__*__coding:utf-8__*__
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,render
import re

class IsLogin(MiddlewareMixin):
	"""
	验证用户是否登录
	"""
	def process_request(self,request):
		#指获发来的url
		next_url = request.path_info
		#设置白名
		white_list = ['/mysite/login/','/mysite/is_login/', '/mysite/register/','/mysite/add_register/','/xadmin/.*']
		#过滤白名单和已有session信息的用户
		for url in white_list:
			ret = re.match(url,next_url)
			if ret or request.session.get("is_login"):
				return
		else:
			return redirect('mysite:login')
