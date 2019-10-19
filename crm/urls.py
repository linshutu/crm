"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from xadmin.plugins import xversion
xadmin.autodiscover()
xversion.register_models

from login import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
	url(r'^xadmin/', include(xadmin.site.urls)),

	#登录注册相关url
	url(r'^login/$',views.login,name='login'),
	url(r'^register/$',views.register,name='register'),
	url(r'^is_login/$',views.is_login,name='is_login'),
	url(r'^add_register/$',views.add_register,name='add_register'),
	url(r'^logout/$',views.logout,name='logout'),

	#后台页面相关url
	url(r'^admin_index/$', views.admin_index, name='admin_index'),
	url(r'^show_customers/$', views.show_customers, name='show_customers'),
	url(r'^add_customers/$', views.add_customers, name='add_customers'),
	url(r'^edit_customers/(\d+)/$', views.edit_customers, name='edit_customers'),


]
