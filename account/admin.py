from django.contrib import admin

# Register your models here.
from account.models import Invest_Detail, transection, withdraws

admin.site.register(Invest_Detail)
admin.site.register(transection)
admin.site.register(withdraws)