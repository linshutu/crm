#__*__coding:utf-8__*__
from django.shortcuts import render,redirect
from django.http import JsonResponse

from mysite import forms
from utils import hash_pwd
from mysite import models

def login(request):
	"""
	登陆
	:param request:
	:return:
	"""
	form = forms.UserForms()
	return render(request, 'login/login.html', {'form':form})

def is_login(request):
	"""
	处理登陆提交的数据，判断登陆是否成功
	:param request:
	:return:
	"""
	form = forms.UserForms(request.POST)
	if form.is_valid():
		data = form.cleaned_data
		has_password= hash_pwd.has_password(data['pwd'])
		ret = models.UserInfo.objects.filter(password=has_password).first()
		if ret:
			request.session['is_login'] = "user"
			request.session['username'] = form.cleaned_data.get("name")
			status = {"data": 1}
			return JsonResponse(status)
		else:
			status = {"data": 0}
			return JsonResponse(status)
	else:
		return render(request, "login/login.html", {"form": form})

def register(request):
	"""
	注册
	:param request:
	:return:
	"""
	form = forms.RegisterForm()    #注意，request.POST是前台传过来的，我们能如果在这里加的话，前端页面会展示出为空的错误
	return render(request, 'login/register.html', {"form":form})

def add_register(request):
	"""
	处理注册提交的数据，保存到数据库
	:param request:
	:return:
	"""
	form = forms.RegisterForm(request.POST)
	if form.is_valid():
		data = form.cleaned_data
		#清洗数据
		data.pop("re_password")
		data['password'] = hash_pwd.has_password(data.get('password'))
		#添加必要数据
		data['is_active'] = 1
		#格式化储存
		models.UserInfo.objects.create(
			**data
		)
		return redirect('mysite:login')
	else:
		#把前端提交的包含错误信息的对象返回到前端页面
		return render(request, 'login/register.html', {"form":form})

def logout(request):
	"""
	退出登陆
	:param request:
	:return:
	"""
	if request.session.get("is_login"):
		request.session.flush()
	return redirect("mysite:login")