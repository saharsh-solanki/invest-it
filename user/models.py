from django.db import models

# Create your models here.
#models for user_data
class user_data(models.Model):
    real_name=models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    balance=models.FloatField(max_length=250,default=0.00)
    withdrawable_balance=models.FloatField(max_length=250,default=0.00)
    refer_code = models.CharField(max_length=100, default='NULL')
    refer_balance = models.FloatField(max_length=100, default=0.00)
    def __str__(self):
        return self.email