from django.contrib import admin
from .models import User , userprofile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CusotmUserAdmin(UserAdmin):
    list_display = ('email' , 'first_name' , 'last_name' , 'username' , 'role' , 'is_active')
    # '-date_joined' and (   -   ) <- use of this is desendign order
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter =()
    fieldsets = ()

admin.site.register(User , CusotmUserAdmin)

# register userprofile
admin.site.register(userprofile)