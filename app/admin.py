from django.contrib import admin
from .models import Contact
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

class Customized_Admin(ImportExportModelAdmin):
    list_display = ('id','name','gender','email','info','phone')
    list_editable = ('gender',)
    list_per_page = 5
    search_fields = ('name','email','info')
    list_filter = ('gender','email')
    list_display_links=('id','name')
#Register your models here.
admin.site.register(Contact,Customized_Admin)

#THIS WILL NOT SHOW THE MODEL GROUPS IN ADMIN PANNEL
admin.site.unregister(Group)
