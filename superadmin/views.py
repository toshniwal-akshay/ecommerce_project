from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from vendor.models import  Vendor
from accounts.models import User
from products.models import Category,Product
from orders.models import Order,OrderedProduct
from django.db.models import Prefetch
from django.db.models import Count

# Create your views here.
@login_required(login_url='login')
def vendors(request):
    
    allVendors = Vendor.objects.filter(is_approved=True).order_by('-created_at')

    context = {
        'vendors': allVendors,
    }
    return render(request, 'superadmin/vendors.html', context)




def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'products',
            queryset = Product.objects.filter(is_available=True)
        )
    )
    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request,'superadmin/vendor_details.html',context)


def admin_orders_detail(request):
    
    orders = (Order.objects.values('vendors__shop_name','vendors__user__email','vendors__slug').annotate(count=Count('order_number')).order_by())
    context = {
        'orders': orders,
    }
    
    return render(request,'superadmin/order_details.html',context)


def admin_vendor_order_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, slug=vendor_slug)
    
    orders = Order.objects.filter(
        vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    
    context={
        'orders':orders
    }
    return render(request , 'superadmin/vendor_order_details.html',context)



def admin_customer_order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        vendors =  order.vendors.all()
        ordered_product = OrderedProduct.objects.filter(order=order)
        subtotal = 0
        for item in ordered_product:
            subtotal += (item.price * item.quantity)
        context = {
            'order': order,
            'vendors' :vendors,
            'ordered_product': ordered_product,
            'subtotal': subtotal,
        }
        return render(request, 'superadmin/customer_order_details.html', context)
    except:
        return redirect('admin')
    
    
def customers(request):
    
    allCustomer = User.objects.filter(role=2).order_by('-created_date')
    
    context = {
        'customers': allCustomer,
    }
    return render(request, 'superadmin/customers.html', context)
