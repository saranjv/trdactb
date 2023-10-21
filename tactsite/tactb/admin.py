from django.contrib import admin
from .models import CompanyInfo, FinYear,CompanyCOA, PartyInfo,UserModaccess,Modaccess,AutoNum,DefaultAct,GLHeader,GLDetail,GLSummary,Subscribers
# Register your models here.

admin.site.register(CompanyInfo)
admin.site.register(FinYear)
admin.site.register(CompanyCOA)
admin.site.register(UserModaccess)
admin.site.register(Modaccess)
admin.site.register(PartyInfo)
admin.site.register(AutoNum)
admin.site.register(DefaultAct)
admin.site.register(GLHeader)
admin.site.register(GLDetail)
admin.site.register(GLSummary)
admin.site.register(Subscribers)

admin.site.site_header = "TACT Administration"
admin.site.site_title = "TACTB"
admin.site.index_title = "DB Administrator"