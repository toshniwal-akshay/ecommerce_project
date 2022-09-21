from multiprocessing import context
from urllib import response
from django.test import TestCase, override_settings
from django.urls import reverse
from accounts.models import User, UserProfile
from django.test.client import RequestFactory
from django.contrib.messages import get_messages
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
# no need of decode here anymore
from io import BytesIO

from vendor.views import order_detail

from .models import Vendor as V
from django.template.defaultfilters import slugify
import tempfile             # for setting up tempdir for media
import base64


TEST_IMAGE = '''
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
'''.strip()


class VendorProfileTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.form_data = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy',
        }

        self.register_url = reverse('registervendor')

        self.login_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
        }

        self.user = User.objects.create_user(**self.form_data)
        self.user.is_active = True
        self.user.role = User.VENDOR
        self.user.save()
        user_profile = UserProfile.objects.get(user=self.user)

        vendor = V()
        vendor.user = self.user
        vendor.user_profile = user_profile
        vendor.shop_name = 'DummyShop'+'-'+str(self.user.id)
        vendor.save()

    def test_get_vendor_profile(self):
        response = self.client.get(reverse('vprofile'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('vprofile'))
        self.assertEqual(response.status_code, 200)

    def test_vendor_profile_valid_from(self):
        self.client.login(username='Dummy@test.com', password='abc@test')

        response = self.client.get(reverse('vprofile'))
        shop_form = response.context['vendor_form']
        profile_form = response.context['profile_form']

        data = profile_form.initial
        data.update(shop_form.initial)

        data['address'] = 'Update Address'
        data['gender'] = 1
        data['dob'] = '06/05/2000'
        data['country'] = "India"
        data['state'] = "mahsj"
        data['city'] = "test"
        data['pin_code'] = "443302"

        response = self.client.post(reverse('vprofile'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Settings updated.')


class CategoriesTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.form_data = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy',
        }

        self.register_url = reverse('registervendor')

        self.login_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
        }

        self.user = User.objects.create_user(**self.form_data)
        self.user.is_active = True
        self.user.role = User.VENDOR
        self.user.save()
        user_profile = UserProfile.objects.get(user=self.user)

        vendor = V()
        vendor.user = self.user
        vendor.user_profile = user_profile
        vendor.shop_name = 'DummyShop'+'-'+str(self.user.id)
        vendor.save()

        self.client.login(username='Dummy@test.com', password='abc@test')
        data = {
            'category_name': 'bag',
            'description': 'Dummy'
        }
        response = self.client.post(reverse('add_category'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Category added successfully!')

        response = self.client.get(reverse('productbuilder'))
        self.assertEqual(response.status_code, 200)
        category = response.context['categories']
        self.category_id = category[0].id

    def test_get_categories(self):

        response = self.client.get(reverse('productbuilder'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['categories'][0]), 'Bag')

    def test_add_categories(self):
        response = self.client.get(reverse('add_category'))
        self.assertEqual(response.status_code, 200)

        data = {
            'category_name': 'shoes',
            'description': 'Dummy'
        }
        response = self.client.post(reverse('add_category'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Category added successfully!')

    def test_get_product_by_category(self):

        response = self.client.get(
            reverse('productitems_by_category', kwargs={'pk': self.category_id}))
        self.assertEqual(response.status_code, 200)

    def test_edit_category(self):

        data = {
            'category_name': 'shoes_edited',
        }
        response = self.client.get(
            reverse('edit_category', kwargs={'pk': self.category_id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('edit_category', kwargs={'pk': self.category_id}), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Category updated successfully!')

    def test_delete_category(self):

        response = self.client.post(
            reverse('delete_category', kwargs={'pk': self.category_id}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Category has been deleted successfully!')


class ProdcutsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.form_data = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy',
        }

        self.register_url = reverse('registervendor')

        self.login_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
        }

        self.user = User.objects.create_user(**self.form_data)
        self.user.is_active = True
        self.user.role = User.VENDOR
        self.user.save()
        user_profile = UserProfile.objects.get(user=self.user)

        vendor = V()
        vendor.user = self.user
        vendor.user_profile = user_profile
        vendor.shop_name = 'DummyShop'+'-'+str(self.user.id)
        vendor.save()

        self.client.login(username='Dummy@test.com', password='abc@test')
        data = {
            'category_name': 'bag',
            'description': 'Dummy'
        }
        response = self.client.post(reverse('add_category'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Category added successfully!')

        response = self.client.get(reverse('productbuilder'))
        self.assertEqual(response.status_code, 200)
        self.category = response.context['categories']
        self.category_id = self.category[0].id

        image = InMemoryUploadedFile(
            # use io.BytesIO
            BytesIO(base64.b64decode(TEST_IMAGE)),
            field_name='tempfile',
            name='tempfilesetup.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        data = {
            'category': 1,
            'title': 'Dummy Bag',
            'price': 500,
            'image': image,
            'is_available': True
        }

        response = self.client.post(reverse('add_product'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Product Item added successfully!')

        response = self.client.get(
            reverse('productitems_by_category', kwargs={'pk': self.category_id}))
        self.p_id = response.context['products'][0].id

    def test_get_add_product(self):

        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)

    # override settings for media dir to avoid filling up your disk

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_post_add_product(self):
        image = InMemoryUploadedFile(
            # use io.BytesIO
            BytesIO(base64.b64decode(TEST_IMAGE)),
            field_name='tempfile',
            name='tempfileaddproduct.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )

        data = {
            'category': 1,
            'title': 'Dummy Bag 4',
            'price': 5000,
            'image': image,
            'is_available': True
        }

        response = self.client.post(reverse('add_product'), data)
        print(response)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Product Item added successfully!')

    def test_get_edit_products(self):

        response = self.client.get(
            reverse('edit_product', kwargs={'pk': self.p_id}))
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_post_edit_product(self):
        image = InMemoryUploadedFile(
            # use io.BytesIO
            BytesIO(base64.b64decode(TEST_IMAGE)),
            field_name='tempfile',
            name='tempfileedit.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        data = {
            'category': 1,
            'title': 'Dummy Bag Edit',
            'price': 500,
            'image': image,
            'is_available': True
        }

        response = self.client.post(
            reverse('edit_product', kwargs={'pk': self.p_id}), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Product Item updated successfully!')

    def test_delete_product(self):
        response = self.client.post(
            reverse('delete_product', kwargs={'pk': self.p_id}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Product  has been deleted successfully!')
