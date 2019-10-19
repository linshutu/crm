from django.contrib import admin
import xadmin

from login.models import Campuses,ClassList,Customer,Department,UserInfo

xadmin.site.register(UserInfo,)
xadmin.site.register(Department,)
xadmin.site.register(Customer,)
xadmin.site.register(ClassList,)
xadmin.site.register(Campuses,)