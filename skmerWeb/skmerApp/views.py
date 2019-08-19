from django.shortcuts import render , redirect
from .models import *
from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import skmerUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.

#Home view. Contains the login form page as well.
def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('queryView', skmerUserId = user.pk)
            else:
                messages.error(request, "Invalid username or password.")

        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, 'skmerApp/home.html', {'form': form})


#resources information method
@login_required
def resources(request,skmerUserId):
    try:
        user = skmerUser.objects.get(pk = skmerUserId)
    except skmerUser.DoesNotExist:
        raise Http404("User does not exist")

    context = {
        'userName' : user.username,
        'userId' : skmerUserId
    }
    if str(request.user.pk) != str(skmerUserId):
        return redirect('skmerHome')
    return render(request, 'skmerApp/resources.html', context)


#about information method
@login_required
def about(request,skmerUserId):
    try:
        user = skmerUser.objects.get(pk = skmerUserId)
    except skmerUser.DoesNotExist:
        raise Http404("User does not exist")

    context = {
        'userName' : user.username,
        'userId' : skmerUserId
    }

    if str(request.user.pk) != str(skmerUserId):
        return redirect('skmerHome')
    return render(request, 'skmerApp/about.html',context)


#skmer user register page
def signup(request):
    if request.method == 'POST':
        form = skmerUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created user successfully. Login to begin")
            return redirect('skmerHome')
    else:
        form = skmerUserCreationForm()


    return render(request, 'skmerApp/signup.html', {'form': form})


#logout view
@login_required(login_url="skmerHome")
def logout_request(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('skmerHome')


