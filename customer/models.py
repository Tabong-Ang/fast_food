from django.db import models

# Create your models here.
class MenuItem(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.IntegerField()
    category = models.ManyToManyField('Category', related_name='item')

class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    tel = models.CharField(max_length=9)
    email = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p ")}'
