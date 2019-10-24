#__*__coding:utf-8__*__
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register= template.Library()

@register.simple_tag
def show_info(request):
	"""
	自定义前端公私有转换标签
	:param request:
	:return:
	"""
	path = request.path
	if path == reverse('mysite:show_customers'):
		return mark_safe('<option value="reverse_gs">公户转私户</option>')
	else:
		return mark_safe('<option value="reverse_sg">私户转公户</option>')

@register.simple_tag
def reverse_url(url_name,id,request):
	"""
	编辑标签返回当前页
	:param url_name:
	:param id:
	:param request:
	:return:
	"""
	from django.http.request import QueryDict

	path = request.get_full_path()
	query_dict_obj = QueryDict(mutable=True)
	query_dict_obj['next'] = path
	encode_url = query_dict_obj.urlencode()

	prefix_path = reverse(url_name,args=(id,))
	full_path = prefix_path + '?' + encode_url

	return full_path