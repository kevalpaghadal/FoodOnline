from django.contrib import admin
from vendor.models import vendor
# Register your models here.

class vendorAdmin(admin.ModelAdmin):
    list_display = ('user' , 'vandor_name' , 'is_approved' , 'created_at')
    list_display_links = ( 'user', 'vandor_name')

admin.site.register(vendor , vendorAdmin)