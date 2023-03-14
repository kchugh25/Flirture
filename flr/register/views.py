from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from flr import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "register/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password0 = request.POST['password0']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists. Please try other username")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "email already exist")

        if len(username)>10:
            messages.error(request, "Username should be less than 10 character")   

        myuser = User.objects.create_user(username, email, password0)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()

        messages.success(request, "Your account is created successfully. We have sent you a confirmation email, please check and confirm")

        # Welcome email

        subject = "Welcome to flirture"
        message  = "Hello" + myuser.first_name + "!!\n" + "Welcome to flirture.\n We have sent you a confirmation email, please confirm your email address.\n\n Thank you"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # activation email
        current_site = get_current_site()

        return redirect('signin')
    else:
        return render(request, "register/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password0 = request.POST['password0']

        user = authenticate(username=username, password=password0)

        if user is not None:
            login(request, user)
            return render(request, "register/index.html", {"fname" : user.first_name})

        else:
            messages.error(request, "bad credentials")
            return redirect('signin')

    return render(request, "register/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "You are logged out successfully")
    return redirect('home')