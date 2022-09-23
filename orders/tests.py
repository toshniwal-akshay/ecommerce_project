from urllib import response
from django.test import TestCase
from django.urls import reverse
from accounts.models import User, UserProfile
from marketplace.models import Cart
from orders.forms import OrderForm
from orders.models import Order, OrderedProduct
from products.models import Category, Product
from django.contrib.messages import get_messages
from vendor.models import Vendor as V
from django.core.files.uploadedfile import InMemoryUploadedFile
# no need of decode here anymore
from io import BytesIO
import base64


TEST_IMAGE = '''
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
'''.strip()


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.user_creation = User.objects.create_user(**self.user_credentials)
        self.user_creation.is_active = True
        self.user_creation.role = User.CUSTOMER
        self.user_creation.save()

        self.form_data = {
            'email': 'DummyShop@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy',
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

        self.client.login(username='DummyShop@test.com', password='abc@test')
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

        self.client.logout()

        return super().setUp()


class OrdersTest(BaseTest):

    def add_product_to_cart(self):
        self.client.login(email='Dummy@test.com', password="abc@test")
        response = self.client.post(reverse('add_to_cart', kwargs={
                                    'product_id': self.p_id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            response.json()['message'], 'Added the product to the cart')

        self.client.logout()

    def test_place_order_with_zero_cart_quantity(self):
        self.client.login(username='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('place_order'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('home'))

    def test_get_place_order(self):
        self.add_product_to_cart()
        self.client.login(username='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('place_order'))
        self.assertTemplateUsed(response, 'orders/place_order.html')

    def test_post_place_order(self):
        self.add_product_to_cart()
        self.client.login(username='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('add_to_cart', kwargs={
                                   'product_id': self.p_id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            response.json()['message'], 'Increased the cart quantity')
        data = {
            'first_name': 'Dummy',
            'last_name': 'Dummy',
            'phone': '325949745412',
            'email': 'Dummy@test.com',
            'address': 'aaskd,test',
            'country': 'India',
            'state': 'MAh',
            'city': 'pune',
            'pin_code': '443302',
            'payment_method': 'Cash On Delivery'
        }
        response = self.client.post(reverse('place_order'), data)
        self.assertIsInstance(response.context['order'], Order)



class PaymentsTest(BaseTest):

    def add_product_to_cart(self):
        self.client.login(email='Dummy@test.com', password="abc@test")
        response = self.client.post(reverse('add_to_cart', kwargs={
                                    'product_id': self.p_id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            response.json()['message'], 'Added the product to the cart')

        self.client.logout()


    def place_order_for_payment(self):
        self.add_product_to_cart()
        self.client.login(username='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('add_to_cart', kwargs={
                                   'product_id': self.p_id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            response.json()['message'], 'Increased the cart quantity')
        data = {
            'first_name': 'Dummy',
            'last_name': 'Dummy',
            'phone': '325949745412',
            'email': 'Dummy@test.com',
            'address': 'aaskd,test',
            'country': 'India',
            'state': 'MAh',
            'city': 'pune',
            'pin_code': '443302',
            'payment_method': 'Cash On Delivery'
        }
        response = self.client.post(reverse('place_order'), data)
        self.assertIsInstance(response.context['order'], Order)
        return response.context['order']


    def test_post_payments(self):
        order_number=self.place_order_for_payment()
        self.client.login(username='Dummy@test.com', password='abc@test')
        data={
            'order_number':order_number,
            'transaction_id':213234324324,
        'payment_method':'COD',
        'status':'SUCCESS'

        }
        response = self.client.post(reverse('payments'),data=data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.json()['order_number'],str(order_number))

    def test_get_payments(self):
        order_number=self.place_order_for_payment()
        self.client.login(username='Dummy@test.com', password='abc@test')
        data={
            'order_number':order_number,
            'transaction_id':213234324324,
        'payment_method':'COD',
        'status':'SUCCESS'

        }
        response = self.client.get(reverse('payments'),data=data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code,200)




class OrderConfirmTest(BaseTest):

    def add_product_to_cart(self):
        self.client.login(email='Dummy@test.com', password="abc@test")
        response = self.client.post(reverse('add_to_cart', kwargs={
                                    'product_id': self.p_id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            response.json()['message'], 'Added the product to the cart')

        self.client.logout()


    def place_order_for_payment(self):
        self.add_product_to_cart()
        self.client.login(username='Dummy@test.com', password='abc@test')
        response = self.client.get(reverse('add_to_cart', kwargs={
                                   'product_id': self.p_id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            response.json()['message'], 'Increased the cart quantity')
        data = {
            'first_name': 'Dummy',
            'last_name': 'Dummy',
            'phone': '325949745412',
            'email': 'Dummy@test.com',
            'address': 'aaskd,test',
            'country': 'India',
            'state': 'MAh',
            'city': 'pune',
            'pin_code': '443302',
            'payment_method': 'Cash On Delivery'
        }
        response = self.client.post(reverse('place_order'), data)
        self.assertIsInstance(response.context['order'], Order)
        return response.context['order']

    def make_payment(self):
        order_number=self.place_order_for_payment()
        self.client.login(username='Dummy@test.com', password='abc@test')
        data={
            'order_number':order_number,
            'transaction_id':213234324324,
        'payment_method':'COD',
        'status':'SUCCESS'

        }
        response = self.client.post(reverse('payments'),data=data,HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code,200)

        return order_number,data['transaction_id']



    def test_confirm_order(self):
        order_number,transaction_id=self.make_payment()
        data={
            'order_no':order_number,
            'trans_id':transaction_id,
        }
        self.client.get(reverse('order_complete'),data=data)
        self.assertTemplateUsed('orders/order_complete.html')
        
    def test_confirm_order_incorrect_order_number(self):
        order_number,transaction_id=self.make_payment()
        data={
            'order_no':"order_number",
            'trans_id':transaction_id,
        }
        response = self.client.get(reverse('order_complete'),data=data)
        self.assertEqual(response.url,reverse('home'))
        