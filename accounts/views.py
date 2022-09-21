from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from allauth.account.views import SignupView
import datetime

from orders.models import Order
from products.models import Product
from vendor.models import Vendor

from .models import User
from .forms import UserSignupForm, VendorSignupForm
from accounts.utils import detectUser, send_verification_email


# Create your views here.

# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_admin(user):
    if user.role == 3:
        return True
    else:
        raise PermissionDenied


class UserSignupView(SignupView):
    "Signup View extended"
    template_name = "accounts/registerUser.html"

    form_class = UserSignupForm

    def get_context_data(self, **kwargs):

        context = super(UserSignupView, self).get_context_data(**kwargs)
        context['redirect_field_value'] = '/account/login'
        context.update(self.kwargs)

        userSignUpForm = UserSignupForm(self.request.POST or None)

        context['form'] = userSignUpForm
        return context


registeruser = UserSignupView.as_view()


class VendorSignupView(SignupView):
    "Signup View extended"
    template_name = "accounts/registerVendor.html"

    form_class = VendorSignupForm

    def get_context_data(self, **kwargs):
        context = super(VendorSignupView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        vendorSignUpForm = VendorSignupForm(self.request.POST or None)

        context['form'] = vendorSignUpForm
        return context


registervendor = VendorSignupView.as_view()


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            if user.is_admin:
                return redirect('admindashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/custDashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):

    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(
        vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    recent_orders = orders[:10]

    # current month's revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(
        vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']

    # total revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    return render(request, 'accounts/vendorDashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(
                request, user, mail_subject, email_template)

            messages.success(
                request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def adminDashboard(request):
    totalOrders = Order.objects.filter(is_ordered=True)
    totalCustomers = User.objects.filter(role=2, is_active=True)
    totalVendors = Vendor.objects.filter(is_approved=True)
    totalProducts = Product.objects.filter(is_available=True)

    context = {
        'totalOrders': totalOrders.count(),
        'totalCustomers': totalCustomers.count(),
        'totalVendors': totalVendors.count(),
        'totalProducts': totalProducts.count(),
    }

    return render(request, 'superadmin/adminDashboard.html', context)
