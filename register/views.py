from django.shortcuts import render

from register.forms import UserForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("your account is not active.")
        else:
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'index.html')

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    context = {'user_form': user_form, 'registered': registered}

    return render(request, 'register.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



