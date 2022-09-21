"Custom Import"
from django import forms
from django.template.defaultfilters import slugify
from allauth.account.forms import SignupForm
from .models import User, UserProfile
from vendor.models import Vendor

from .utils import send_verification_email

MALE = 1
FEMALE = 2
OTHER = 3

GENDER_CHOICE = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),

)


class UserSignupForm(SignupForm):
    "User Signup Form Extended from allauth SignUp form"
    first_name = forms.CharField(max_length=25, label='First Name')
    last_name = forms.CharField(max_length=25, label='Last Name')

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = User.CUSTOMER
        user.set_password(self.cleaned_data['password1'])
        user.save()
        mail_subject = "Activate Your Account"
        email_template = 'accounts/emails/account_verification_email.html'
        send_verification_email(request, user, mail_subject, email_template)
        return user


class VendorSignupForm(SignupForm):
    "User Signup Form Extended from allauth SignUp form"
    first_name = forms.CharField(max_length=25, label='First Name')
    last_name = forms.CharField(max_length=25, label='Last Name')
    shop_name = forms.CharField(max_length=20, label="Shop Name")

    def save(self, request):
        user = super(VendorSignupForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = User.VENDOR
        user.is_staff= True
        user.set_password(self.cleaned_data['password1'])
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        vendor = Vendor()
        vendor.user = user
        vendor.user_profile = user_profile
        vendor.shop_name = self.cleaned_data['shop_name']
        vendor.slug = slugify(vendor.shop_name)+'-'+str(user.id)
        vendor.save()
        mail_subject = "Activate Your Account"
        email_template = 'accounts/emails/account_verification_email.html'
        send_verification_email(request, user, mail_subject, email_template)

        return user


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Address', 'required': 'required'}))

    class Meta:
        model = UserProfile
        fields = ['gender', 'dob', 'address',
                  'country', 'state', 'city', 'pin_code']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']