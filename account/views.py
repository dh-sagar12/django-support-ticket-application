import uuid
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout


from account.forms import UserCreationForm

from account.models import User

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
                    django_login(request, authUser)
                    return redirect(reverse('home'))
                else:
                    params = {'error': 'Inactive account'}
                return render(request, 'accounts/login.html', params)
                    
                    
            else:
                params = {'error': 'Invalid Credentials'}
                return render(request, 'accounts/login.html', params)
            
    return render(request, 'accounts/login.html')



def logoutView(request):
    django_logout(request)
    return redirect(reverse('login'))




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
        


