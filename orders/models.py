import jsonfield
import json
from django.db import models
from accounts.models import User
from products.models import Product

from vendor.models import Vendor


request_object = ''


class Payment(models.Model):
    PAYMENT_METHOD = (
        ('COD', 'Cash On Delivery'),
        ('PREPAID', 'Pre Paid'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    total_data = jsonfield.JSONField(blank=True, null=True)
    # tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}")
    # total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    
    def order_placed_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])

    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        subtotal = 0
        tax = 0
        if self.total_data:
            total_data = json.loads(self.total_data)
            subtotal = total_data.get(str(vendor.id))
            
        grand_total = float(subtotal) + float(tax)
        context = {
            'subtotal': subtotal,
            'grand_total': grand_total,
        }

        return context


    

    def __str__(self):
        return self.order_number


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title