from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import *
import requests
from blog.models import *
# Create your views here.
def _cart_id(request):
     cart = request.session.session_key
     if not cart:
         cart = request.session.create()
     return cart




def customerregistration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_nunber = form.cleaned_data['phone_nunber']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_nunber = phone_nunber
            user.save()
            curren_site = get_current_site(request)
            email_subject = 'Please activate your account'
            message = render_to_string("account_verification_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Thankyou for registerring with us. we have send you a verification email to your email address. Please verify it.')
            return redirect('registration')
    else:
        form = RegistrationForm()
    context = {
    'form':form
    }
    return render(request, 'accounts/signup.html',context)

def login(request):
 if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            # try:
            #     post = Post.objects.get(cart_id=_cart_id(request))
            #     is_post_exits = Post.objects.filter(post=post).exists()
            #     if is_post_exits:
            #         posts = Post.objects.filter(post=post)
            # except:
            #     pass
            auth.login(request,user)
            # messages.success(request,'Your Now Logged in')
            url = request.META.get("HTTP_REFERER")
            try:
                    query = requests.utils.urlparse(url).query
                    # print('query ->',query)
                    params = dict(x.split("=") for x in query.split("&"))
                    if 'next' in params:
                        nextpage = params['next']
                        return redirect(nextpage)
                    # print('10*__________',params)
        
            except:
                    return redirect('Blogpage')
        else:
           messages.error(request,'Email or Password not match ')
           return redirect('login')
 return render(request, 'accounts/login.html')

def Logout_view(request):
   auth.logout(request)
   messages.success(request,'Your Now Logged Out')
   return redirect('login')


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations Your Account is Activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            curren_site = get_current_site(request)
            email_subject = 'Reset Your Password'
            message = render_to_string("accounts/reset_password_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password Reset email has been sent to your address .')
            return redirect('login')
        else:
            messages.error(request,'Account does not exit')
            return redirect('forgotpassword')
    return render(request,'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successfull')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')


@login_required(login_url='login')
def change_password(request):
 if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)
    
        if new_password == confirm_password:
            success = user.check_password(current_password)
             
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request,'Password Updated Successfully.')
                return redirect('login')
            else:
                messages.error(request,'Please Enter Valid Password')
                return redirect('changepassword')

        else:
            messages.error(request,'Password does not match')
            return redirect('changepassword')
 return render(request, 'accounts/changepassword.html')
