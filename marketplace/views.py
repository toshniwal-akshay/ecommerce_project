from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile
from products.models import Product
from orders.forms import OrderForm


from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.shortcuts import HttpResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



# def marketplace(request):
#     vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
#     vendor_count = vendors.count()
#     context = {
#         'vendors': vendors,
#         'vendor_count': vendor_count,
#     }
#     return render(request, 'marketplace/listings.html', context)


# def vendor_detail(request, vendor_slug):
#     vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

#     categories = Category.objects.filter(vendor=vendor).prefetch_related(
#         Prefetch(
#             'product',
#             queryset = Product.objects.filter(is_available=True)
#         )
#     )

#     if request.user.is_authenticated:
#         cart_items = Cart.objects.filter(user=request.user)
#     else:
#         cart_items = None
#     context = {
#         'vendor': vendor,
#         'categories': categories,
#         'cart_items': cart_items,
#     }
#     return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            # Check if the product item exists
            try:
                product = Product.objects.get(id=product_id)
                # Check if the user has already added that product to the cart
                try:
                    chkCart = Cart.objects.get(
                        user=request.user, product=product)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(
                        user=request.user, product=product, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the product to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            # Check if the product item exists
            try:
                product = Product.objects.get(id=product_id)
                # Check if the user has already added that product to the cart
                try:
                    chkCart = Cart.objects.get(
                        user=request.user, product=product)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})



@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')

    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)
