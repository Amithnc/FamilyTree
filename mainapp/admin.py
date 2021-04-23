from django.contrib import admin
from .models import member
# Register your models here.

admin.site.index_title="DASHBOARD"
admin.site.site_title="ADMIN"
admin.site.site_header="Nidaghatta Family-ADMIN"
admin.site.register(member)