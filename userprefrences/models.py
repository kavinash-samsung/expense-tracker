from locale import currency
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserPrefrences(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True, default="INR")

    def __str__(self):
        return str(self.user)+"s"+"prefrences"

    def currency_name(self):
        return str(self.currency)