from django.contrib import admin

from .models import Category,Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',) }
    list_display = ('category_name','vendor','updated_at')
    
    search_fields = ('category_name','vendor__shop_name')
    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',) }
    list_display = ('title','category','vendor','price','is_available','updated_at')
    search_fields = ('title','category__category_name','vendor__shop_name','price')
    list_filter = ('is_available',)
    
    
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)