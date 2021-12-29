from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Books(models.Model):
    book_id=models.CharField( max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    number_of_copies=models.IntegerField( )

    def __str__(self):
        return self.user.username

class Store(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    store_name =models.CharField(max_length=50)
    def __str__(self):
        return self.store_name
