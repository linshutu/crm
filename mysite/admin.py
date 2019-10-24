from django.contrib import admin
import xadmin

from mysite.models import Campuses,ClassList,Customer,Department,UserInfo
from mysite.models import ContractTemplate,ConsultRecord,Enrollment,PaymentRecord,CourseRecord,StudyRecord

class UserInfo_Model:
	list_display= ['id','username','telephone']

class ConsultRecord_Model:
	list_display= ['customer','note','consultant','date','delete_status']

xadmin.site.register(UserInfo,UserInfo_Model)
xadmin.site.register(Department,)
xadmin.site.register(Customer,)
xadmin.site.register(ClassList,)
xadmin.site.register(Campuses,)

xadmin.site.register(ContractTemplate,)
xadmin.site.register(ConsultRecord,ConsultRecord_Model)
xadmin.site.register(Enrollment,)
xadmin.site.register(PaymentRecord,)
xadmin.site.register(CourseRecord,)
xadmin.site.register(StudyRecord,)

