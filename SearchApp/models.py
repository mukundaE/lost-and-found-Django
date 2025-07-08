from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Reg(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)

class FoundItem(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    found_location = models.CharField(max_length=100)
    found_date = models.DateField()
    image = models.ImageField(upload_to='found_images/', blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_claimed = models.BooleanField(default=False)
    def __str__(self):
        return self.item_name


class LostItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField(max_length=50)
    date_lost = models.DateField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    is_matched = models.BooleanField(default=False)  
    def __str__(self):
        return self.item_name