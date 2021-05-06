from django.db import models

# Create your models here.
from django.db.models import Model



class withdraws(Model):
    txn=(
        ('success','success'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    )
    paypal_email=models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    withdraw_amount = models.FloatField(max_length=100)
    status = models.CharField(max_length=100,blank=True,null=True,choices=txn)
    date_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user_email




class Invest_Detail(Model):
    plan=models.CharField(max_length=100)
    amount=models.FloatField(max_length=250)
    email=models.EmailField(max_length=100)
    invest_id=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now_add=True)
    intrest=models.CharField(max_length=100)
    month=models.CharField(max_length=100)
    invest_type=models.CharField(max_length=100)
    investment=models.CharField(max_length=200,default='running')
    def __str__(self):
        return self.invest_id



class transection(Model):
    txn_id=status=models.CharField(max_length=250,null=True)
    amount=models.FloatField(max_length=250)
    email=models.EmailField(max_length=100)
    status=models.CharField(max_length=250,default='FAILED') #failed or success
    details = models.CharField(max_length=250,null="TRUE") #credit or debit
    message=models.CharField(max_length=100,null=True)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.txn_id


"""
INVT=AMOUNT INVRSTED

"""

