from django.contrib import admin
from .models import member
# Register your models here.

admin.site.index_title="DASHBOARD"
admin.site.site_title="ADMIN"
admin.site.site_header="Nidaghatta Family-ADMIN"

class memberAdmin(admin.ModelAdmin):
    list_display = ('name',"image")
    list_filter = ('is_requested_to_delete',)

admin.site.register(member,memberAdmin)