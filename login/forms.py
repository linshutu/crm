#__*__coding:utf-8__*__
from django import forms
from django.forms import widgets
import re

from login import models


class UserForms(forms.Form):
	"""
	登陆表
	"""
	name = forms.CharField(
		label="用户名",
		max_length=16,
		required=True,
		widget=widgets.TextInput(attrs={'placeholder':"用户名"}),
	)
	pwd = forms.CharField(
		label="密码",
		max_length=128,
		required=True,
		widget=widgets.PasswordInput(attrs={'placeholder': "密码",}),
	)

class RegisterForm(forms.Form):
	"""
	注册表
	"""
	username = forms.CharField(
		min_length=3,
		max_length=8,
		required=True,
		widget=widgets.TextInput(attrs={'placeholder':'输入用户名'}),
		error_messages={
			'min_length': "用户名最少3个字符",
			'max_length': "用户名最多8个字符",
		}
	)

	password = forms.CharField(
		min_length=3,
		max_length=8,
		required=True,
		widget=widgets.PasswordInput(attrs={'placeholder':'输入密码','oncontextmenu':"return false"}),
	)
	re_password = forms.CharField(
		min_length=3,
		max_length=8,
		required=True,
		widget=widgets.PasswordInput(attrs={'placeholder':'再次输入密码','oncontextmenu':"return false"}),
	)
	telephone= forms.CharField(
		max_length=11,
		required=True,
		widget=widgets.TextInput(attrs={'placeholder':'输入手机号码',}),
	)
	email = forms.CharField(
		required=True,
		widget=widgets.EmailInput(attrs={'placeholder':'输入邮箱地址'}),
		error_messages={'invalid':"邮箱的格式不正确"}
	)

	def clean(self):
		"""
		全局钩子，验证数据
		:return:
		"""
		pwd = self.cleaned_data.get('password')
		re_pwd = self.cleaned_data.get('re_password')
		if pwd == re_pwd:
			return self.cleaned_data
		else:
			self.add_error('re_password',"两次密码不一致")

	def clean_phone(self):
		"""
		局部钩子,验证手机号是否正确
		:return:
		"""
		telephone = self.cleaned_data.get("telephone")
		mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
		if not mobile_re.match(telephone):
			self.add_error('telephone','手机号码格式错误')
		else:
			#注意，使用钩子检查数据的时候，数据没有问题，一定把对象返回，否者在view里面是拿不到数据的
			return telephone

class CustomersModelsForm(forms.ModelForm):
	"""
	添加客户
	"""
	class Meta:
		model = models.Customer
		fields = "__all__"

		def __init__(self,*args,**kwargs):
			super().__str__(*args,**kwargs)

			for field_name,field in self.fields.items():
				from multiselectfield.forms.fields import MultiSelectFormField
				if not isinstance(field,MultiSelectFormField):
					field.widget.attrs.update({'class':'form-control'})
