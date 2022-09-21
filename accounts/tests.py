from django.core import mail
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from accounts.models import User, UserProfile
from django.test.client import RequestFactory
from django.contrib.messages import get_messages
from django.conf import settings
from vendor.models import Vendor as V
from django.template.defaultfilters import slugify


# Create your tests here.

class ForgotPasswordTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.user_creation = User.objects.create_user(**self.user_credentials)
        self.user_creation.is_active = True
        self.user_creation.save()

    def test_forgot_password_test_for_registered_user(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('forgot_password'), {
                                    'email': 'Dummy@test.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reset Your Password')

    def test_forgot_password_test_for_unregistered_user(self):

        response = self.client.post(reverse('forgot_password'), {
                                    'email': 'Dummy@test1.com'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Account does not exist')


class ResetPasswordTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.login_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
        }

        self.user_creation = User.objects.create_user(**self.user_credentials)
        self.user_creation.is_active = True
        self.user_creation.role = User.CUSTOMER
        self.user_creation.save()
        self.user_id = self.user_creation.id

    def test_password_reset_for_different_password(self):
        self.client.login(email='Dummy@test.com', password='abc@test')
        response = self.client.post(reverse('reset_password'), {
                                    'password': 'abc@test', 'confirm_password': 'abc@test1'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Password do not match!')


class CustomerTest(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.request = HttpRequest()

        self.form_data = {
            'email': 'Dummy@test.com',
            'password1': 'abc@test',
            'password2': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.register_url = reverse('registeruser')

        self.login_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
        }

        self.user_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.user_creation = User.objects.create_user(**self.user_credentials)
        self.user_creation.is_active = True
        self.user_creation.save()

    def test_can_view_user_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        response = self.client.post(self.register_url, self.form_data)
        user = User.objects.get(email='Dummy@test.com')

        self.assertTrue(user)

    def test_form_saves_values_to_instance_user_on_save(self):
        response = self.client.post(self.register_url, self.form_data)
        user = User.objects.get(email='Dummy@test.com')
        self.assertFalse(user.role == 2)
        user.role = User.CUSTOMER
        user.save()
        user = User.objects.get(email='Dummy@test.com')
        self.assertTrue(user.role == 2)

    def test_homepageAccess(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_model(self):
        user = User.objects.get(email="Dummy@test.com")
        self.assertEqual(self.user_creation, user)

    def test_customer_login(self):
        # send login data
        response = self.client.post(
            reverse('login'), self.login_credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_re_login(self):
        # send login data
        response = self.client.post(
            reverse('login'), self.login_credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get('/account/login/')
        self.assertEqual(response.url, reverse('myAccount'))

    def test_inavlid_login(self):
        # send login data
        self.user_credentials['password'] = 'abc@test1'
        response = self.client.post(
            '/account/login/', self.user_credentials, follow=True)
        # should not Log in Now
        self.assertFalse(response.context['user'].is_authenticated)

    def test_customerDashboard(self):
        self.user_creation.role = User.CUSTOMER
        self.user_creation.save()

        response = self.client.login(
            email='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('custDashboard'))
        self.assertEqual(response.status_code, 200)

    def test_access_not_allowed_if_role_is_not_customer(self):
        #self.user_creation.role = User.CUSTOMER
        self.user_creation.is_active = True
        self.user_creation.save()

        response = self.client.login(
            email='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('custDashboard'))
        self.assertEqual(response.status_code, 403)


class VendorRegistrationViewTest(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.request = HttpRequest()

        self.form_data = {
            'email': 'Dummy@test.com',
            'password1': 'abc@test',
            'password2': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy',
            'shop_name': 'DummyShop'}

        self.register_url = reverse('registervendor')

        self.login_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
        }

        self.user_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.user = User.objects.create_user(**self.user_credentials)
        self.user.is_active = True
        self.user.role = User.VENDOR
        self.user.save()
        user_profile = UserProfile.objects.get(user=self.user)

        vendor = V()
        vendor.user = self.user
        vendor.user_profile = user_profile
        vendor.save()

    def test_can_view_vendor_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        response = self.client.post(
            self.register_url, self.form_data, follow=True)
        vendor = V.objects.get(user__email='Dummy@test.com')
        self.assertTrue(vendor)

    def test_form_saves_values_to_instance_user_on_save(self):
        response = self.client.post(self.register_url, self.form_data)
        vendor = V.objects.get(user__email='Dummy@test.com')
        vendor_slug = slugify(
            self.form_data['shop_name'])+'-'+str(vendor.user_id)
        vendor.slug = vendor_slug
        vendor.save()
        vendor = V.objects.get(user__email='Dummy@test.com')

        self.assertEqual(vendor.slug, vendor_slug)

    def test_vendor_login(self):
        # send login data
        response = self.client.post(
            reverse('login'), self.login_credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_re_login(self):
        # send login data
        response = self.client.post(
            reverse('login'), self.login_credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get('/account/login/')
        self.assertEqual(response.url, reverse('myAccount'))

    def test_inavlid_login(self):
        # send login data
        self.user_credentials['password'] = 'abc@test1'
        response = self.client.post(
            '/account/login/', self.user_credentials, follow=True)
        # should not Log in Now
        self.assertFalse(response.context['user'].is_authenticated)

    def test_vendor_dashboard(self):
        response = self.client.login(
            email='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('vendorDashboard'))
        self.assertEqual(response.status_code, 200)

    def test_access_not_allowed_if_role_is_not_vendor(self):
        self.user.role = User.CUSTOMER
        self.user.save()

        response = self.client.login(
            email='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('vendorDashboard'))
        self.assertEqual(response.status_code, 403)


class LogInTest(TestCase):

    def setUp(self):
        self.user_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.admin_credentials = {
            'email': 'DummyAdmin@test.com',
            'password': 'abc@test',
            'first_name': 'DummyAdmin',
            'last_name': 'DummyAdmin',
        }

        self.admin_user = User.objects.create_superuser(
            **self.admin_credentials)

    def test_admin_login(self):
        # send login data
        response = self.client.post(
            '/account/login/', self.admin_credentials, follow=True)
        # should be Admin Login
        self.assertTrue(response.context['user'].is_admin)

    def test_admin_dashboard(self):
        self.admin_user.role = User.ADMIN
        self.admin_user.save()

        response = self.client.login(
            email='DummyAdmin@test.com', password='abc@test')
        response = self.client.get(reverse('adminDashboard'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Log out
        response = self.client.login(
            email='DummyAdmin@test.com', password='abc@test')
        self.assertTrue(response)

        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            reverse('logout'), self.admin_credentials, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)
