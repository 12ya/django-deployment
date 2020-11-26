from django.shortcuts import render
from basicapp.forms import UserProfileInfoForm, UserForm
# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(requst, "urls/index.html")


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_profile = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and user_profile.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile.save(commit = False)

            profile.user = user

            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print(user_form.errors, user_profile.errors)
    else:
        user_form = UserForm()
        user_profile = UserProfileInfoForm()

    return render(request, 'urls/register', {'registered':registered,
                                             'user_form':user_form,
                                             'profile_user':user_profile})





def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

        else:
            print("you are not active or your made mistake in password or username")
            return HttpResponseRedirect(reverse('index'))

    else:
        print('invalid input ma boi')

        return render(request, 'urls/login.html')

@login_required
def user_logout(request):
    logout(request)
    print('you were logged out')
    return HttpResponseRedirect(reverse('index'))
