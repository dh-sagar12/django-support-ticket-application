
import datetime
from tokenize import Token
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
import secrets


from account.forms import UserCreationForm

from account.models import Token, User

# Create your views here.

def loginView(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    else:
        if request.method== 'POST':
            print(request)
            email=  request.POST.get('email')
            password=  request.POST.get('password')
            usr = User.objects.filter(email=email).first()
            if usr:
                if usr.is_active:
                    authUser= authenticate(email= usr.email, password=password)
                    if authUser:
                        django_login(request, authUser)
                        return redirect(reverse('home'))
                    else:
                        messages.error(request, 'Invalid Credentials' )
                        return render(request, 'accounts/login.html')

                else:
                    messages.error(request, 'Inactive account')
                    return render(request, 'accounts/login.html')
                        
                    
            else:
                messages.error(request, 'Invalid Credentials' )
                return render(request, 'accounts/login.html')
            
    return render(request, 'accounts/login.html')



def logoutView(request):
    django_logout(request)
    return redirect(reverse('login'))


def invalid_older_token(request):
    validTime = datetime.date.today() - datetime.timedelta(minutes=20)
    old_verification_tokens =  Token.objects.filter(created_on__lte= validTime)
    for i in old_verification_tokens:
        i.is_valid = False
        i.save()
    
def invalid_multiple_token(request, user):
    tokens = Token.objects.filter(user=user, is_valid= True)
    for token in tokens:
        token.is_valid = False
        token.save()

def forgotPassword(request):
    if request.method == 'POST':
        email =  request.POST.get('email')
        try:
            user =  User.objects.get(email=email)
        except:
            messages.error(request, 'User Not found')
            return render(request, 'accounts/forgetpassword.html')
        if  user is not None:
            invalid_multiple_token(request, user)
            token =  secrets.token_urlsafe(20)
            token_value = Token.objects.create(token=token, user= user)
            token_value.save()
            send_password_reset_email(request, user)
            return render(request, 'accounts/forgetpassword_confirm.html')
    return render(request, 'accounts/forgetpassword.html')

def setPassword(request, token):
    try:
        token = Token.objects.get(token=token)
        user =  User.objects.get(id=token.user.id)
        if token.is_valid:
            params = {'token': token, 'user': user}
            return render(request, 'accounts/set_password_form.html', params)

        else:
            messages.error(request, 'Token has been expired! Please try again')
            return redirect(reverse('forgotPassword'))
    except:
        messages.error(request, 'Invalid Token. Please try again')
        return redirect(reverse('forgotPassword'))

def savePassword(request):
    if request.method =='POST':
        password1 =  request.POST.get('password1')
        password2 =  request.POST.get('password2')
        user_id = request.POST.get('user')
        token = request.POST.get('token')
        req_user =  User.objects.get(id= user_id)
        if authenticate(email=req_user.email, password= password1) is not None:
            messages.error(request, 'same as old password!!')
            return redirect(setPassword, token=token)
        else:
            if password1 == password2:
                req_user.set_password(password1)
                req_user.save()
                invalid_multiple_token(request, req_user)
                messages.success(request, 'Password has been changed successfully!!')
                return redirect(reverse('login'))
            
            else:
                messages.error(request, 'Password Mismatched')
                return redirect(setPassword, token=token)
    else:
        return redirect(reverse('login'))
        

def send_password_reset_email(request, user):
    token =  Token.objects.get(user=user, is_valid= True)
    user= user
    base_url = get_current_site(request).domain
    subject = "Change your password"
    message = render_to_string('sendEmails/forget_password_email.html',{
        'user': user,
        'base_url': base_url,
        'token': token
    })
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
    email.fail_silently = True
    email.content_subtype = "html"
    email.send()


def createUser(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    else:
        form = UserCreationForm()
        params = {'form': form}
        
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                email = request.POST.get('email')
                password = request.POST.get('password1')
                user = User.objects.get(email=email)
                print(user.email)
                authUser= authenticate(email= user.email, password=password)
                django_login(request, authUser)
                return redirect(reverse('home'))
            else:
                return render(request, 'accounts/signup.html', {'form': form})
            
        return render(request, 'accounts/signup.html', params )
        


