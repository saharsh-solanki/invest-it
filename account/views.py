from datetime import datetime, timedelta
import random
import string
import stripe
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render

# Create your views here.
#Function for Dashboard
from Investit import settings
from account.models import Invest_Detail, transection, withdraws
from user.models import user_data
stripe.api_key=settings.STRIPE_SECRET_KEY


def dashboard(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
        total_earning=0.00
        user_info = user_data.objects.get(email=email)
        p=cal_user_earning(email)
        inv_det=Invest_Detail.objects.filter(email=email)
        context={
            'name':user_info.real_name,
            'balance':user_info.balance,
            'withdrawable_balance':user_info.withdrawable_balance,
            'total_earning':p['total_earning'],
                }
        return render(request,"user/dashboard.html",context)
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')


def invest(request):
    if 'user_email' in request.session:
        return render(request,"user/invest.html")
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

# function that gen unique order id
def gen_order(size, chars=string.ascii_uppercase + string.digits+string.ascii_lowercase):
   id=''.join(random.choice(chars) for _ in range(size))
  # if transection.objects.filter().exists():
   #    id = ''.join(random.choice(chars) for _ in range(size))
   return id


#Function for Deposit
def deposit(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
        user_info = user_data.objects.get(email=email)
        context = {
            'name': user_info.real_name,
            #    'balance': user_info.balance,
        }
        return render(request, "user/deposit.html", context)
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')
#Function for my_deposit


def my_deposit(request):
    email = request.session['user_email']
    """ deposit_data=transection.objects.filter(email=email,order_for="deposit")
    # code for pagination
    #data = Paginator(deposit_data, 10)
    page = request.GET.get('page')
    try:
        data = data.page(page)
    except:
        data = data.page(1)"""
    return render(request,"user/my_deposit.html")

#Function for my_withdrawals
def my_withdrawals(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
        deposit_data = withdraws.objects.filter(user_email=email).order_by('-id')  # should be changed
        # code for pagination
        data = Paginator(deposit_data, 5)
        page = request.GET.get('page')
        try:
            data = data.page(page)
        except:
            data = data.page(1)
        return render(request,"user/my_withdrawals.html",{'data':data})
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

#Function for my investment
def my_investments(request):
    if 'user_email' in request.session:
        email=request.session['user_email']
        obj=Invest_Detail.objects.filter(email=email).order_by('-id')
        return render(request,"user/my_investments.html",{'obj':obj})
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

#Function for my investment
def withdraw(request):
    if 'user_email' in request.session:
        email=request.session['user_email']
        data=user_data.objects.get(email=email)
        if request.method=="POST":
            paypal_email = request.POST['paypal_email']
            amount = request.POST['amount']
            if float(data.withdrawable_balance) < float(amount) :
                messages.error(request,'Insufficiant Fund !!')
                return redirect('withdraw')
            else:
                add_with=withdraws(paypal_email=paypal_email,user_email=email,withdraw_amount=amount,status='pending')
                add_with.save()
                data.withdrawable_balance=float(data.withdrawable_balance)-float(amount)
                data.balance=float(data.balance)-float(amount)
                data.save()
                txn_id=gen_order(5)
                txns = transection(txn_id=txn_id, amount=amount, email=email, status='SUCCESS', details="DEBITED",
                                   message="WITHDRAW")
                txns.save()
                messages.success(request, 'Withdraw Successfull !! You Will Recive Payment Within ')
                return redirect('withdraw')
        else:
            context={
                'balance':data.balance,
                'withdraw_amount':data.withdrawable_balance,
            }
            return render(request,"user/withdraw.html",context)
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')




#Function for Full investment Details


def full_details(request,id):
    if 'user_email' in request.session:
        obj=Invest_Detail.objects.get(id=id)
        amount=obj.amount
        plan=obj.plan
        plan_det = get_plan(plan)
        interest = plan_det['interest']
        month = plan_det['month']
        type = plan_det['type']
            #calculate interest here

        ppd = cal_interest(plan, amount)
        total_profit=ppd['total_profit']
        profit_day=ppd['profit_day']
        profit_remain=11
        profit_recived=14
        time_remain=20

        context={
            'obj':obj,
            'total_profit':total_profit,
            'profit_remain':profit_remain,
            'profit_day':profit_day,
            'profit_recived':profit_recived,
            'time_remain':time_remain,
        }

        return render(request,"user/full_details.html",context)
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

#Function for Invest
def transection_history(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
        deposit_data = transection.objects.filter(email=email).order_by('-id')  # should be changed
        # code for pagination
        data = Paginator(deposit_data, 5)
        page = request.GET.get('page')
        try:
            data = data.page(page)
        except:
            data = data.page(1)
        return render(request,"user/transection_history.html",{'data':data})
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')


def general_settings(request):
    if 'user_email' in request.session:
        if request.method=="POST":
            email = request.session['user_email']
            password=request.POST['password']
            new_password = request.POST['new_password']
            con_password = request.POST['con_password']
            if user_data.objects.filter(email=email, password=password).exists():
                if new_password != con_password:
                    messages.success(request, "New Password And Confirm Password Is Not Matched")
                else:
                    data = user_data.objects.get(email=email, password=password)
                    data.password = new_password
                    data.save()
                    messages.success(request, "Password Updated Successfully")
                    #for getting current date and time
                    now=datetime.now()
                    time=now.strftime("%Y-%m-%d %H:%M:%S")
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')
                    cont = "This Mail Is Sent To inform That Your Password Has Been Changed On "+time+"<br>And IP ADDREES IS "+ip
                    send_mail(
                        "Password Changed",
                        cont,
                        "Password Changed Successfully",
                        [email],
                        fail_silently=False,
                    )
                    return redirect('general_settings')
            else:
                messages.success(request, "incorrect Password")
                return redirect('general_settings')
        else:
            return render(request, "user/general_settings.html")
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')


#Function for account_settings
def account_settings(request):
    if 'user_email' in request.session:
        return render(request,"user/account_settings.html")
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

#Function for Profile
def profile(request):
    if 'user_email' in request.session:
        email=request.session['user_email']
        obj=user_data.objects.get(email=email)
        return render(request,"user/profile.html",{'data':obj})
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

#Function For felxible Deposite
def flx_deposit(request):
    if 'user_email' in request.session:
       return render(request,'user/flexible_deposit.html')
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')
#Function For Locked Deposite


def lock_deposit(request):
    if 'user_email' in request.session:
        return render(request, 'user/locked_deposit.html')
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

#function for Invest Now
def invest_now(request):
    if 'user_email' in request.session:
        if request.method=="POST":
            plan=request.POST['plan']
            plan_det = get_plan(plan)
            interest = plan_det['interest']
            month = plan_det['month']
            type = plan_det['type']
            context={
                'plan':request.POST['plan'],
                'interest':interest,
                'month': month,
                'type': type,
            }
            return render(request,'user/invest_form.html',context)
        return redirect('dashboard')
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

# function that gen unique order id
def gen_order(size, chars=string.ascii_uppercase + string.digits+string.ascii_lowercase):
   id=''.join(random.choice(chars) for _ in range(size))
  # if transection.objects.filter().exists():
   #    id = ''.join(random.choice(chars) for _ in range(size))
   return id



#function for Make_invest
def make_invest(request):
    if 'user_email' in request.session:
        if request.method=="POST":
                if request.POST['pay'] == 'pay':
                    plan_det = get_plan(request.POST['plan'])
                    interest = plan_det['interest']
                    month = plan_det['month']
                    type = plan_det['type']
                    amount = request.POST['amount']
                    context = {
                        'plan': request.POST['plan'],
                        'amount': amount,
                        'amount_pay': float(amount) * 100,
                        'interest': interest,
                        'month': month,
                        'type': type,
                        'key': settings.STRIPE_PUBLISHABLE_KEY,
                    }
                    return render(request, 'user/pay.html', context)
                else:
                    if request.POST['create_order'] == 'True':
                        email = request.session['user_email']
                        plan = request.POST['plan']
                        amount = request.POST['amount']
                        plan_det = get_plan(plan)
                        interest = plan_det['interest']
                        month = plan_det['month']
                        type = plan_det['type']
                        invest_id = gen_order(15)
                        o = user_data.objects.get(email=email)
                        referbalance = o.refer_balance
                        refbalance = (float(amount) / 100) * 1.5
                        finalreferbalance = referbalance + refbalance
                        refcode = o.refer_code
                        if refcode=="NULL":
                            pass
                        else:
                            oob = user_data.objects.get(id=refcode)
                            oob.refer_balance = finalreferbalance
                            oob.save()
                        try:
                            charges = stripe.Charge.create(
                                shipping={
                                    'name': 'Jenny Rosen',
                                    'address': {
                                        'line1': '510 Townsend St',
                                        'postal_code': '98140',
                                        'city': 'San Francisco',
                                        'state': 'CA',
                                        'country': 'US',
                                    },
                                },
                                amount=int(amount) * 100,
                                currency="usd",
                                source=request.POST['stripeToken'],
                                description="Payment For Plan",
                                metadata={'invest_id': invest_id}
                            )

                            if charges["status"] == "succeeded":
                                txn_id=charges['balance_transaction']
                                obj = Invest_Detail(plan=plan, amount=amount, email=email, invest_id=invest_id,
                                                    intrest=interest,
                                                    month=month, invest_type=type)
                                cont = "Congrates You Have Successfully invested : $"+amount+"Your TXN_ID is "+txn_id
                                send_mail(
                                    "Investment successfull",
                                    cont,
                                    settings.EMAIL_HOST_USER,
                                    [email],
                                    fail_silently=False,
                                )
                                obj.save()
                                # updating balance
                                u = user_data.objects.get(email=email)
                                u.balance = u.balance + float(amount)
                                u.save()
                                txns=transection(txn_id=txn_id,amount=amount,email=email,status='SUCCESS',details="CREDIT",message="INVESTED")
                                txns.save()
                                return render(request, 'user/payment_success.html', {'amount': amount})
                            else:
                                messages.success(request, 'Payment Failed !! Try Again')
                                return redirect('dashboard')
                        except:
                            return redirect('invest')
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')



def add_fund(request):
        for Inv_Detail in Invest_Detail.objects.all():
            if str(Inv_Detail.investment) == "running":
                plan_det = get_plan(Inv_Detail.plan)
                interest = plan_det['interest']
                month = plan_det['month']
                type = plan_det['type']
                if (datetime.now()).strftime("%Y-%m-%d") == ((Inv_Detail.date_time + timedelta(days=month * 30)).date()).strftime("%Y-%m-%d"):
                    xx = Invest_Detail.objects.get(email=Inv_Detail.email,invest_id=Inv_Detail.invest_id)
                    xx.investment="completed"
                    xx.save()
                    print(u.withdrawable_balance, xx.amount)
                    u = user_data.objects.get(email=Inv_Detail.email)
                    u.balance = float(u.balance) + float(xx.amount)
                    u.withdrawable_balance = float(u.withdrawable_balance) + float(xx.amount)

                    u.save()
                else:
                    ppd = cal_interest(Inv_Detail.plan, Inv_Detail.amount)
                    u = user_data.objects.get(email=Inv_Detail.email)
                    u.balance = u.balance + float(ppd['profit_day'])
                    u.withdrawable_balance = u.withdrawable_balance + float(ppd['profit_day'])
                    u.save()
                    txn_id = gen_order(10)
                    txns = transection(txn_id=txn_id, amount=ppd['profit_day'], email=Inv_Detail.email,
                                       status='SUCCESS',
                                       details="CREDIT", message="INTEREST")
                    txns.save()
                    print('The User Email is : ', Inv_Detail.email, 'Will Recived : $', ppd['profit_day'], 'today')
        return HttpResponse('success')


def add_funds(request):
    #user=user_data.objects.all()
    for user in user_data.objects.all():
        email = user.email
        In_det= Invest_Detail.objects.filter(email=email)
        for Inv_Detail in In_det:
            plan_det=get_plan(Inv_Detail.plan)
            interest=plan_det['interest']
            month = plan_det['month']
            type = plan_det['type']
            ppd=cal_interest(Inv_Detail.plan,Inv_Detail.amount)
            u = user_data.objects.get(email=email)
            u.balance = u.balance + float(ppd['profit_day'])
            u.withdrawable_balance = u.withdrawable_balance + float(ppd['profit_day'])
            u.save()
            txn_id=gen_order(10)
            txns = transection(txn_id=txn_id, amount=ppd['profit_day'], email=email, status='SUCCESS', details="CREDIT",message="INTEREST")
            txns.save()
            print('amount',Inv_Detail.amount)
            print('The User Email is : ',email,'Will Recived : $',ppd['profit_day'],'today')
    return HttpResponse('success')




"""Intereset calculating function"""
def cal_interest(plan,amount):
    plan_det = get_plan(plan)
    interest = plan_det['interest']
    month = plan_det['month']
    type = plan_det['type']
    m = month * 30
    t_profit = (float(amount) / 100) * interest
    profit_day = t_profit / m
    context={
        'total_profit':t_profit,
        'profit_day':round(float(profit_day), 6),
    }
    return context



def get_plan(plan_name):
    plan=plan_name
    if plan == "Basic Plan":
        interest = 15
        month = 3
        type = "flexible"
    elif plan == "Pro Plan":
        interest = 20
        month = 6
        type = "flexible"
    elif plan == "Premium Plan":
        interest = 25
        month = 12
        type = "flexible"
    elif plan == "Locked Plan A":
        interest = 30
        month = 12
        type = "locked"
    elif plan == "Locked Plan B":
        interest = 30
        month = 24
        type = "locked"
    context={
        'interest':interest,
        'month':month,
        'type':type,
    }
    return context

def cal_user_earning(email):
    total_earning=0.00
    for x in  transection.objects.filter(email=email,message='INTEREST'):
        total_earning=total_earning+x.amount
    context={
        'total_earning':total_earning
    }
    return context

def add_refer(request):
    if request.method=="POST":
        refer_code=request.POST['rc']
        if user_data.objects.filter(id=refer_code).exists():
            update = user_data.objects.get(email=request.session['user_email'])
            update.refer_code = refer_code
            update.save()
            messages.success(request,'Refer Code Added Successfully')
            email = request.session['user_email']
            obj = user_data.objects.get(email=email)
            id = obj.id
            r = user_data.objects.filter(refer_code=id)
            context = {
                'obj': obj,
                'r': r,
                'refered': obj.refer_code}
            return render(request, 'user/refer.html', context)
        else:
            email = request.session['user_email']
            obj = user_data.objects.get(email=email)
            id = obj.id
            r = user_data.objects.filter(refer_code=id)
            context = {
                'obj': obj,
                'r': r,
                'refered': obj.refer_code}
            return render(request, 'user/refer.html', context)
    email = request.session['user_email']
    obj = user_data.objects.get(email=email)
    id = obj.id
    r = user_data.objects.filter(refer_code=id)
    context = {
        'obj': obj,
        'r': r,
        'refered': obj.refer_code}
    return render(request, 'user/refer.html', context)


#parag
def refer(request):
    if 'user_email' in request.session:
        email=request.session['user_email']
        obj=user_data.objects.get(email=email)
        id=obj.id
        r=user_data.objects.filter(refer_code=id)
        context={
            'obj':obj,
            'r':r,
            'refered':obj.refer_code}
        return render(request,'user/refer.html',context)
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

def refer_withdraw(request):
    if 'user_email' in request.session:
        email=request.session['user_email']
        obj=user_data.objects.get(email=email)
        return render(request,'user/refer_withdraw.html',{'obj':obj})
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')

def refer_withdraw_done(request):
    if 'user_email' in request.session:
        if request.method=="POST":
            withdraw_amount=request.POST['amount']
            paypal_email = request.POST['paypal_email']
            email=request.session['user_email']
            obj=user_data.objects.get(email=email)
            refbalance=obj.refer_balance
            if (float(withdraw_amount) >= 100.00):
                if(float(withdraw_amount)<=float(refbalance)):
                    add_with = withdraws(paypal_email=paypal_email, user_email=email, withdraw_amount=withdraw_amount,
                                         status='pending')
                    add_with.save()
                    txn_id = gen_order(5)
                    txns = transection(txn_id=txn_id, amount=withdraw_amount, email=email, status='SUCCESS', details="DEBITED",
                                       message="WITHDRAW")
                    obj.refer_balance=float(refbalance)-float(withdraw_amount)
                    obj.save()
                    messages.success(request, "Withdraw Successfull !!")
                    return redirect('refer')
                else:
                    messages.error(request, "Insufficiant Fund !!")
                    return redirect('refer_withdraw')
            else:
                messages.error(request, "MINIMUM WTIHDRAW IS $100.")
                return redirect('refer_withdraw')
    else:
        messages.success(request, "Your Session Has Expired Login To Access")
        return redirect('login')
