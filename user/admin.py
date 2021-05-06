from django.contrib import admin

# Register your models here.
from user.models import user_data

admin.site.register(user_data)