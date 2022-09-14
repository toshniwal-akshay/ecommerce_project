from django.contrib import admin
from .models import Vendor

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('shop_name',) }
    list_display = ('user','shop_name','is_approved','created_at')
    list_display_links = ('user','shop_name')
    list_editable = ('is_approved',)
admin.site.register(Vendor,VendorAdmin)
