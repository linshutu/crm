#__*__coding:utf-8__*
from django.conf.urls import url

from mysite.views import auth
from mysite.views import customer

urlpatterns = [
	# 登录注册相关url
	url(r'^login/$', auth.login, name='login'),
	url(r'^register/$', auth.register, name='register'),
	url(r'^is_login/$', auth.is_login, name='is_login'),
	url(r'^add_register/$', auth.add_register, name='add_register'),
	url(r'^logout/$', auth.logout, name='logout'),

	# 后台页面相关url
	url(r'^admin_index/$', customer.admin_index, name='admin_index'),

	#公有客户信息展示
	url(r'^show_customers/', customer.ShowCustomers.as_view(), name='show_customers'),
	#公有客户信息增加和编辑
	url(r'^add_customers/$', customer.add_customers, name='add_customers'),
	url(r'^edit_customers/(\d+)/$', customer.edit_customers, name='edit_customers'),

	# 客户信息查询
	url(r'^search_customers/$', customer.search_customers, name='search_customers'),

	# 私有客户信息展示
	url(r'^show_personal_customers/$', customer.ShowCustomers.as_view(), name='show_personal_customers'),

	#客户跟进信息
	url(r'^consult_record/$', customer.ConsultRecord.as_view(), name='consult_record'),
	#跟进记录增加\编辑
	url(r'^add_consult_record/$', customer.add_edit_consult_record, name='add_consult_record'),
	url(r'^edit_consult_record/(\d+)/$', customer.add_edit_consult_record, name='edit_consult_record'),

	#报名表
	url(r'^show_enrollment_record/$', customer.EnrollmentRecord.as_view(), name='show_enrollment_record'),
	# 报名记录增加\编辑
	url(r'^add_enrollment_record/$', customer.add_edit_enrollment_record, name='add_enrollment_record'),
	url(r'^edit_enrollment_record/(\d+)/$', customer.add_edit_enrollment_record, name='edit_enrollment_record'),

	# 课程记录
	url(r'^show_course_record/$', customer.CourseRecord.as_view(), name='show_course_record'),
	# 课程记录增加\编辑
	url(r'^add_course_record/$', customer.add_edit_course_record, name='add_course_record'),
	url(r'^edit_course_record/(\d+)/$', customer.add_edit_course_record, name='edit_course_record'),

	#批量操作学习记录
	url(r'^study_record/(\d+)/$', customer.study_record, name='study_record'),

]
