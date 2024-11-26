from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    userType = models.CharField(max_length=50,)
    viewpassword=models.CharField(max_length=50)
    
    def _str_(self):
        return self.username
    
class user_register(models.Model):
    
    user=models.OneToOneField(Login,on_delete=models.CASCADE)
    user_username=models.TextField(null=True)
    user_email=models.EmailField(null=True)
    user_password=models.TextField(null=True)
    def _str_(self):
        return self.user_username

class Carts(models.Model):

    user_id=models.ForeignKey(user_register,on_delete=models.CASCADE,related_name='added_items')
    book_id = models.CharField(max_length=100, primary_key=True)
    book_cover=models.CharField(max_length=200, null=True)
    book_title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_qty=models.IntegerField()
    
class Order(models.Model):

    user = models.ForeignKey(user_register, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    book_cover=models.CharField(max_length=200)
    book_title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_amount=models.IntegerField()
    order_qty=models.IntegerField()
    ordered_date= models.DateField(auto_now_add=True)

    def __str__(self):
        return "order-{}-{}".format(self.user.user_username)