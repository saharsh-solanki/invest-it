import random
from datetime import datetime
import random
import string

from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template

from Investit import settings
from user.models import user_data


def register(request):
    #checking is method is POST or Not and if We Click On The Register Button Then This Code Run
    if 'user_email' in request.session:
        messages.success(request, "Already Logged In")
        return redirect('dashboard')
    else:
        if request.method=="POST":
            #Fetching Data From Form
            name=request.POST['name']
            mobile_no = request.POST['mobile_no']
            email=request.POST['email']
            password = request.POST['password']
            #cheching is email is already registered or not
            if user_data.objects.filter(email=email).exists():
                msg="Email Is Already Registered"
                return render(request, "forms/registration_form.html",{'msg':msg})
            else:
                #now We Need To Genrate 4 Digit Random Number And Send It To Mail
                #to genrate random number
                otp=random.randint(1000,9999)
                #code To Send Otp To Email
                subject = "ONE TIME PASSWORD VERIFCTAION CODE"
                sender = settings.EMAIL_HOST_USER
                to = email
                title="OTP FOR EMAIL VERIFCATION "
                message="One Time Password For Your Account Regitration"
                ctx = {
                    'title':title,
                    'otp':otp,
                    'content': message,
                }
                message = get_template('email.html').render(ctx)
                msg = EmailMessage(
                    subject,
                    message,
                    sender,
                    [to],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                request.session['otp_from_server']=otp
                request.session['name'] = name
                request.session['mobile_no'] = mobile_no
                request.session['email'] = email
                request.session['password'] = password
                msag="OTP Sended To Your Email !! Check Span Folder Also"
                return render(request, "forms/varify-otp.html",{'msg':msag})
        else:
            return render(request,"forms/registration_form.html")


#function for Otp Varification
def varify_otp(request):
    # checking is method is POST or Not and if We Click On The Register Button Then This Code Run
    if request.method == "POST":
        # Fetching Data From Form
        name = request.session['name']
        mobile_no = request.session['mobile_no']
        email = request.session['email']
        password = request.session['password']
        otp_by_user=str(request.POST['otp_from_user'])
        otp_by_server=str(request.session['otp_from_server'])
        if otp_by_user!=otp_by_server:
            msg="incorrect Otp"
            return render(request,"forms/varify-otp.html",{'msg':otp_by_server})
        else:
            user=user_data(real_name=name,email=email,password=password,mobile_no=mobile_no)
            user.save()
            cont="Congratulation You Have Successfully registered"
            send_mail(
                "Registration Successfull",
                cont,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            #request.session['user_email']=email
            msg="Registered Successfully"
            #request.session.flush()
            messages.success(request,"You Have Successfully Register You Can Login !!")
            return redirect('login')


def resend_reg_otp(request):
    #checking is method is POST or Not and if We Click On The Register Button Then This Code Run

        #now We Need To Genrate 4 Digit Random Number And Send It To Mail
        #to genrate random number
            otp = random.randint(1000, 9999)
            # code To Send Otp To Email
            subject = "Crack_It "
            sender = settings.EMAIL_HOST_USER
            to = request.session['email']
            title = "Email Varification"
            message = "One Time Password For Your Account Regitration"
            ctx = {
                'title': title,
                'otp': otp,
                'content': message,
            }
            message = get_template('email.html').render(ctx)
            msg = EmailMessage(
                subject,
                message,
                sender,
                [to],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            request.session['otp_from_server'] = otp
            return render(request, "form/varify-otp.html", {'msg': 'OTP Reseneded !!Check Spam Folder Also'})


def reset_password(request):
    #checking is method is POST or Not and if We Click On The Register Button Then This Code Run
    if request.method=="POST":
        #Fetching Data From Form
        email=request.POST['email']
        if user_data.objects.filter(email=email).exists():
            #send mail
            otp = random.randint(1000, 9999)
            # code To Send Otp To Email
            subject = "One Time Password To Reset Password"
            sender = settings.EMAIL_HOST_USER
            to = email
            title = "Email Varification"
            message = "One Time Password For Your Account Regitration"
            ctx = {
                'title': title,
                'otp': otp,
                'content': message,
            }
            message = get_template('email.html').render(ctx)
            msg = EmailMessage(
                subject,
                message,
                sender,
                [to],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            request.session['otp_from_server'] = otp
            request.session['email'] = email
            msg="OTP Sended Successfully"
            return render(request, "forms/reset_password_varify_otp.html",{'msg':"OTP Re-sended !! Check Spam Folder In Case Do Not Recive"})
        else:
            #now We Need To Genrate 4 Digit Random Number And Send It To Mail
            msg = "Email Not Registered "
            return render(request, "forms/reset_password_form.html", {'msg': msg})
    else:
        return render(request,"forms/reset_password_form.html")

def varify_reset_password_otp(request):
    # checking is method is POST or Not and if We Click On The Register Button Then This Code Run
    if request.method == "POST":
        # Fetching Data From Form
        email = request.session['email']
        password = request.POST['password']
        otp_by_user= str(request.POST['otp'])
        otp_by_server = str(request.session['otp_from_server'])
        if otp_by_user != otp_by_server:
            msg="incorrect Otp"
            return render(request,"form/reset_password_form.html",{'msg':msg})
        else:
            user=user_data.objects.get(email=email)
            user.password=password
            user.save()
            request.session.flush()
            msg="Password Updated Successfully"
            return render(request,"forms/login.html",{'msg':msg})

def resend_reset_password_otp(request):
    otp = random.randint(1000, 9999)
    # code To Send Otp To Email
    subject = "Crack_It OTP Varification"
    sender = settings.EMAIL_HOST_USER
    to = request.session['email']
    title = "Email Varification"
    message = "One Time Password For Your Account Regitration"
    ctx = {
        'title': title,
        'otp': otp,
        'content': message,
    }
    message = get_template('email.html').render(ctx)
    msg = EmailMessage(
        subject,
        message,
        sender,
        [to],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    request.session['otp_from_server'] = otp
    return render(request, "form/reset_password_varify_otp.html", {'msg':'otp resended Check Email !!'})



# login Form
def login(request):
    if 'user_email' in request.session:
        return redirect('dashboard')
    else:
            if request.method == "POST":
                # Fetching Data From Form
                email = request.POST['email']
                password = request.POST['password']
                if user_data.objects.filter(email=email).exists():
                    if user_data.objects.filter(email=email, password=password).exists():
                        msg = "Login In Successfuly"
                        user = user_data.objects.get(email=email)
                        request.session['user_email'] = email
                        request.session['user_name'] = user.real_name
                        #pp=str(user.profile)
                        #request.session['profile_image'] = pp
                        return redirect('dashboard')
                        #return render(request, "user/dashboard.html", {'msg': msg,'user_email':user.email,'user_name':user.real_name,'balance':user.balance})
                    else:
                        # now We Need To Genrate 4 Digit Random Number And Send It To Mail
                        msg = "Inccorect Password "
                        return render(request, "forms/login.html", {'msg': msg})
                else:
                    msg = "Email Is Not Registered "
                    return render(request, "forms/login.html", {'msg': msg})
            else:
                return render(request, "forms/login.html")


#Function for Dashboard
def dashboard(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
        user_info = user_data.objects.get(email=email)
        context = {
            'name': user_info.real_name,
            'balance': user_info.balance,
        }
        return render(request, "user/dashboard.html", context)
    else:
        return redirect('login')

def logout(request):
    request.session.flush()
    msg="logout Successfully"
    return render(request,'index.html',{'msg':msg})
