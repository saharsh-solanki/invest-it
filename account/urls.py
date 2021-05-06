"""Investit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from account import views


urlpatterns = [

path('Dashboard',views.dashboard,name='dashboard'),
    path('invest',views.invest,name='invest'),
    path('Deposit',views.deposit,name='deposit'),
    path('My_Deposite',views.my_deposit,name='my_deposit'),
    path('My_Withdrawals',views.my_withdrawals,name='my_withdrawals'),
    path('My_Investments',views.my_investments,name='my_investments'),
    path('Transection_History',views.transection_history,name='transection_history'),
    path('General_Settings',views.general_settings,name='general_settings'),
    path('Profile',views.profile,name='profile'),
    path('Account_Settings',views.account_settings,name='account_settings'),
    path('Flx_deposit',views.flx_deposit,name="flx_deposit"),
    path('Lock_deposit', views.lock_deposit, name="lock_deposit"),
    path('Invest_Now', views.invest_now, name="invest_now"),
    path('Make_Invest', views.make_invest, name="make_invest"),
    path('Full_Details/<id>', views.full_details, name="full_details"),
    path('add_fund', views.add_fund, name="add_fund"),
    path('withdraw', views.withdraw, name="withdraw"),
    path('refer', views.refer, name="refer"),
    path('refer_withdraw', views.refer_withdraw, name="refer_withdraw"),
    path('refer_withdraw_done', views.refer_withdraw_done, name="refer_withdraw_done"),
     path('add_refer', views.add_refer ,name="add_refer"),
]
