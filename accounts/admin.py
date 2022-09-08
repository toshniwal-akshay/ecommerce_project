from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,UserProfile


# Register your models here.

class CustomUserAdmin(UserAdmin):
    
    list_display = ('email','username','first_name','last_name','role','is_staff','is_admin','is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User,CustomUserAdmin)

admin.site.register(UserProfile)
