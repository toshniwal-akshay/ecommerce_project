from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from marketplace.models import Cart
from products.models import Product



# Create your tests here.


class OrdersTest(TestCase):

    def setUp(self):

        self.user_credentials = {
            'email': 'Dummy@test.com',
            'password': 'abc@test',
            'first_name': 'Dummy',
            'last_name': 'Dummy'}

        self.user_creation = User.objects.create_user(**self.user_credentials)
        self.user_creation.is_active = True
        self.user_creation.role = User.CUSTOMER
        self.user_creation.save()

        self.client.login(email='Dummy@test.com', password="abc@test")



    def test_get_place_order(self):
        response = self.client.get(reverse('place_order'))
        print(response)

    def test_post_place_order(self):
        product = Product.objects.all()
        print(product)

        # response = self.client.post(reverse('place_order'))
        # print(response)
