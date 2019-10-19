from django.shortcuts import render,redirect
from django.http import JsonResponse

from login import forms
from login import models
from utils import hash_pwd
# Create your views here.

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
		print (data)
		#清洗数据
		data.pop("re_password")
		data['password'] = hash_pwd.has_password(data.get('password'))
		#添加必要数据
		data['is_active'] = 1
		#格式化储存
		models.UserInfo.objects.create(
			**data
		)
		return redirect('login')
	else:
		#把前端提交的包含错误信息的对象返回到前端页面
		return render(request, 'login/register.html', {"form":form})

def admin_index(request):
	"""
	后台主界面
	:param request:
	:return:
	"""
	return render(request, "index.html", )

def show_customers(request):
	"""
	展示客户信息页面
	:param request:
	:return:
	"""
	customers_info = models.Customer.objects.all()
	return render(request,'customers/show_customers.html',{"customers_info":customers_info})

def add_customers(request):
	"""
	增加客户信息页面
	:param request:
	:return:
	"""
	if request.method == "GET":
		form = forms.CustomersModelsForm()
		return render(request,'customers/add_customers.html',{"form":form})
	else:
		form = forms.CustomersModelsForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('show_customers')
		else:
			return render(request,'customers/add_customers.html',{"form":form})

def edit_customers(request,id):
	"""
	修改客户信息页面
	:param request:
	:return:
	"""
	old_obj = models.Customer.objects.filter(pk=id).first()
	if request.method == "GET":
		old_form = forms.CustomersModelsForm(instance=old_obj)
		return render(request,'customers/edit_cumtomers.html',{"form":old_form})
	else:
		new_form = forms.CustomersModelsForm(request.POST,instance=old_obj)
		if new_form.is_valid():
			new_form.save()
			return redirect('show_customers')
		else:
			return render(request,'customers/edit_cumtomers.html',{"form":new_form})

'''
结合add和edit：
def addEditCustomer(request,n=None):
    old_obj = models.Customer.objects.filter(pk=n).first()
    label  = '编辑页面' if n else '添加页面'


    if request.method == 'GET':
        book_form_obj = myforms.CustomerModelForm(instance=old_obj)
        return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})

    else:
        book_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)

        if book_form_obj.is_valid():
            book_form_obj.save()
            return redirect('customers')
        else:

            return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})
'''

def logout(request):
	"""
	退出登陆
	:param request:
	:return:
	"""
	if request.session.get("is_login"):
		request.session.flush()
	return redirect("login")
