#__*__coding:utf-8__*__
from django.shortcuts import render,reverse,redirect,HttpResponse
from django.views import View
import copy
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db import transaction
from django.forms.models import modelformset_factory

from mysite import forms
from mysite import models
from django.conf import settings
from utils.page import Page

"""主页"""
def admin_index(request):
	"""
	后台主界面
	:param request:
	:return:
	"""
	return render(request, "index.html", )

"""客户信息"""
class ShowCustomers(View):
	"""
	展示客户信息页面+分页+站内客户信息搜索+公私户+搜索编辑返回原页面
	:param request:
	:return:
	"""
	def get(self,request):
		recv_data = copy.copy(request.GET)


		current_page_number = request.GET.get("page")  #当前页码
		search_field = request.GET.get('search_field') #所搜条件
		if search_field == None:
			search_field = 'qq__contains'
		keyword = request.GET.get("keyword")
		all_customers = None
		message = None
		if keyword:
			q = Q()
			q.children.append([search_field,keyword])
			all_customers = models.Customer.objects.filter(q)
		else:
			if request.path == reverse('mysite:show_customers'):
				all_customers = models.Customer.objects.filter(consultant__isnull=True)
				message= "公有"
				change_message = "公有客户转私有客户"
			else:
				all_customers = models.Customer.objects.filter(consultant__username=request.session.get("username"))
				message = "私有"
				change_message = "私有客户转公有客户"

		total_count = all_customers.count()
		per_page_count = settings.PER_PAGE_COUNT
		page_number_show = settings.PAGE_NUMBER_SHOW

		page_obj = Page(current_page_number, total_count, page_number_show,per_page_count,recv_data)
		all_customers = all_customers[page_obj.start_data_number:page_obj.end_data_number]
		page_html = page_obj.page_html_func()
		return render(request, 'customers/show_customers.html', {'all_customers': all_customers, "page_html": page_html,"keyword":keyword,'message':message,'search_field':search_field})

	def post(self,request):
		action= request.POST.get('action')
		cids= request.POST.getlist('cids')  #选中的客户
		customer_list = models.Customer.objects.filter(id__in=cids)

		if hasattr(self,action):
			ret = getattr(self,action)(request,customer_list)
			if ret:
				return ret
			else:
				return redirect(request.path)
		else:
			return HttpResponse("你的方法不对")

	def bulk_delete(self,request, customer_list):
		"""
		批量删除选中的客户
		:param self:
		:param request:
		:param customer_list:
		:return:
		"""
		customer_list.delete()
		return redirect(request.path)

	def reverse_gs(self,requset,customer_list):
		"""
		将公有客户批量转换成私有客户
		:param requset:
		:param customer_list:
		:return:
		"""
		user_obj= models.UserInfo.objects.get(username=requset.session.get('username'))
		customer_list.update(consultant_id=user_obj.id)

	def reverse_sg(self,request,customer_list):
		"""
		将客户私有转成公有
		:param request:
		:param customer_list:
		:return:
		"""
		customer_list.update(consultant=None)

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
			return redirect('mysite:show_customers')
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
		# 这个是返回编辑之前的页面，自定义标签reverse_url实现的
		next_path = request.GET.get('next')
		new_form = forms.CustomersModelsForm(request.POST,instance=old_obj)
		if new_form.is_valid():
			new_form.save()
			return redirect(next_path)
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

"""分页"""
def search_customers(request):
	"""
	:param request:
	:return:
	"""
	all_customers = models.Customer.objects.all()
	paginator = Paginator(all_customers,20)

	page = request.GET.get('page')
	contacts = None
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		# 如果请求的页数不是整数，返回第一页。
		contacts = paginator.page(1)
	except EmptyPage:
		# 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
		contacts = paginator.page(paginator.num_pages)
	return render(request,'customers/show_customers.html',{"contacts":contacts,'all_customers':all_customers})

"""客户跟进信息"""
class ConsultRecord(View):

	def get(self,request):
		recv_data = copy.copy(request.GET)
		current_page_number = request.GET.get("page")  # 当前页码
		search_field = request.GET.get('search_field')  # 所搜条件
		if search_field == None:
			search_field = 'customer__name__contains'
		keyword = request.GET.get("keyword")
		all_records = None

		print (request.GET.dict())
		#获取单个客户的id
		customer_id = request.GET.get("customer_id")
		if keyword:
			q = Q()
			q.children.append([search_field, keyword])
			all_records = models.ConsultRecord.objects.filter(q)
		else:
			all_records = models.ConsultRecord.objects.all()
		all_records = all_records.filter(consultant__username=request.session.get('username'),delete_status=False)

		if customer_id:
			all_records = all_records.filter(customer_id=customer_id)

		total_count = all_records.count()
		per_page_count = settings.PER_PAGE_COUNT
		page_number_show = settings.PAGE_NUMBER_SHOW

		page_obj = Page(current_page_number, total_count, page_number_show, per_page_count, recv_data)
		all_records = all_records[page_obj.start_data_number:page_obj.end_data_number]
		page_html = page_obj.page_html_func()
		return render(request, 'consult_record/consult_record.html',
		              {'all_records': all_records, "page_html": page_html, "keyword": keyword,
		               'search_field': search_field})

	def post(self,request):
		action = request.POST.get('action')
		cids = request.POST.getlist("cids")
		consult_record_list = models.ConsultRecord.objects.filter(id__in=cids)

		if hasattr(self, action):
			ret = getattr(self, action)(request, consult_record_list)
			if ret:
				return ret
			else:
				return redirect(request.path)
		else:
			return HttpResponse('你的方法不对!!')

	def bulk_delete(self, request, consult_record_list):
		consult_record_list.update(delete_status=True)
		return redirect(request.path)

def add_edit_consult_record(request,id=None):
	"""
	增加\编辑跟进记录信息
	:param request:
	:return:
	"""
	old_obj = models.ConsultRecord.objects.filter(pk=id).first()
	label = '编辑页面' if id else '添加页面'

	if request.method == "GET":
		record_form_obj = forms.ConsultRecordModelsForm(request,instance=old_obj)
		return render(request, 'consult_record/add_edit_consult_decord.html', {"record_form_obj":record_form_obj,'label':label})
	else:
		# 这个是返回编辑之前的页面，自定义标签reverse_url实现的
		next_path = request.GET.get('next')
		record_form_obj = forms.ConsultRecordModelsForm(request,request.POST,instance=old_obj)
		if record_form_obj.is_valid():
			record_form_obj.save()
			return redirect('mysite:consult_record') if not id else redirect(next_path)
		else:
			return render(request, 'consult_record/add_edit_consult_decord.html', {"record_form_obj":record_form_obj,'label':label})

"""报名记录"""
class EnrollmentRecord(View):
	"""
	报名表
	:param request:
	:return:
	"""
	def get(self,request):
		recv_data = copy.copy(request.GET)
		current_page_number = request.GET.get('page')
		search_field = request.GET.get('search_field')
		if search_field == None:
			search_field = 'customer__name__contains'
		keyword = request.GET.get("keyword")
		all_enrollment = None
		if keyword:
			q = Q()
			q.children.append([search_field, keyword])
			all_enrollment = models.Enrollment.objects.filter(q)
		else:
			all_enrollment = models.Enrollment.objects.all()
		all_enrollment = all_enrollment.filter(delete_status=False)

		total_count = all_enrollment.count()
		per_page_count = settings.PER_PAGE_COUNT
		page_number_show = settings.PAGE_NUMBER_SHOW

		page_obj = Page(current_page_number, total_count, page_number_show, per_page_count, recv_data)
		all_enrollment = all_enrollment[page_obj.start_data_number:page_obj.end_data_number]
		page_html = page_obj.page_html_func()
		return render(request,'enrollment_record/show_enrollment_record.html',{"all_enrollment":all_enrollment,"page_html": page_html, "keyword": keyword,
		               'search_field': search_field})

	def post(self,request):
		action = request.POST.get('action')
		cids = request.POST.getlist("cids")
		print (action,cids)
		enrollment_record_list = models.Enrollment.objects.filter(id__in=cids)

		if hasattr(self, action):
			ret = getattr(self, action)(request, enrollment_record_list)
			if ret:
				return ret
			else:
				return redirect(request.path)
		else:
			return HttpResponse('你的方法不对!!')

	def bulk_delete(self, request, enrollment_record_list):
		enrollment_record_list.update(delete_status=True)
		return redirect(request.path)

def add_edit_enrollment_record(request,id=None):
	"""
	报名记录增加和编辑
	:param request:
	:return:
	"""
	old_obj = models.Enrollment.objects.filter(pk=id).first()
	label="添加页面" if id else "编辑页面"

	if request.method == "GET":
		enrollment_obj = forms.EnrollmentModelsForm(request,instance=old_obj)
		return render(request,'enrollment_record/add_edit_enrollment_record.html',{"enrollment_obj":enrollment_obj,"label":label})
	else:
		#这个是返回编辑之前的页面，自定义标签reverse_url实现的
		next_url = request.GET.get('next')
		enrollment_obj = forms.EnrollmentModelsForm(request,request.POST, instance=old_obj)
		if enrollment_obj.is_valid():
			enrollment_obj.save()
			return redirect('mysite:show_enrollment_record') if not id else redirect(next_url)
		else:
			return render(request, 'enrollment_record/add_edit_enrollment_record.html',
			              {"enrollment_obj": enrollment_obj, "label": label})

"""课程记录"""
class CourseRecord(View):
	def get(self,request):

		all_course_obj = models.CourseRecord.objects.all()
		return render(request, "course_record/show_course_record.html", {"all_course_obj": all_course_obj, })

	def post(self,request):
		action = request.POST.get('action')
		cids = request.POST.getlist('cids')

		if hasattr(self,action):
			getattr(self,action)(request,cids)
			return redirect('mysite:show_course_record')

	def bulk_create_study_record(self,request,cids):
		"""
		批量创建学习记录
		:param request:
		:param cids:
		:return:
		"""
		#先通过课程找到班级
		course_create_list = models.CourseRecord.objects.filter(pk__in=cids)
		for course_record in course_create_list:
			#从班级反向查到已报名的学生
			student_objs = course_record.re_class.customer_set.all().exclude(status='unregistered')
			student_list = []
			for student in student_objs:
				obj= models.StudyRecord(
					course_record=course_record,
					student=student
				)
				student_list.append(obj)
			models.StudyRecord.objects.bulk_create(student_list)

def add_edit_course_record(request,id=None):
	"""
	课程记录添加/编辑
	:param request:
	:return:
	"""
	old_obj = models.CourseRecord.objects.filter(pk=id).first()
	label="添加页面" if id else "编辑页面"

	if request.method == "GET":
		Course_obj = forms.CourseRecodModelForm(request,instance=old_obj)
		return render(request,'course_record/add_edit_course_record.html',{"Course_obj":Course_obj,"label":label})
	else:
		#这个是返回编辑之前的页面，自定义标签reverse_url实现的
		next_url = request.GET.get('next')
		Course_obj = forms.CourseRecodModelForm(request,request.POST, instance=old_obj)
		if Course_obj.is_valid():
			Course_obj.save()
			return redirect('mysite:show_course_record') if not id else redirect(next_url)
		else:
			return render(request, 'course_record/add_edit_course_record.html',
			              {"Course_obj": Course_obj, "label": label})

def study_record(request,course_id):
	"""
	批量操作学习记录
	:param request:
	:return:
	"""
	if request.method == "GET":
		formset_obj = modelformset_factory(model=models.StudyRecord,form=forms.StudyRecordModelForm,extra =0)
		formset= formset_obj(queryset=models.StudyRecord.objects.filter(course_record_id=course_id))
		return render(request, "study_record/study_record.html", {"formset": formset,})
	else:
		formset_obj = modelformset_factory(model=models.StudyRecord,form=forms.StudyRecordModelForm,extra =0)
		formset = formset_obj(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect(request.path)
		else:
			return render(request, 'study_record/study_record.html', {'formset': formset})





