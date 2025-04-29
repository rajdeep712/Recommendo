from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import Http404

from .forms import LoginForm,SignupForm
from .models import Profile

# Create your views here.

class Login_page(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"accounts/login.html",{
            "form":form,
        })
    
    def post(self,request):
        my_user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if User.objects.filter(username=request.POST['username']).first():
            user = User.objects.get(username = request.POST['username'])
            profile = user.profile
        if my_user is None:
            form = LoginForm(request.POST)
            messages.error(request,"Either username or password is incorrect")
            return render(request,"accounts/login.html",{
                "form":form,
            })
        elif not profile.is_verified:
            form = LoginForm(request.POST)
            messages.error(request,"Please verify your account first")
            return render(request,"accounts/login.html",{
                "form":form,
            })
        
        login(request,my_user)
        return redirect('auth_home')
    

class Signup_page(View):
    def get(self,request):
        form = SignupForm()
        return render(request,"accounts/signup.html",{
            "form":form,
        })
    
    def post(self,request):
        form = SignupForm(request.POST)
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if(User.objects.filter(username=username).first()):
            messages.error(request,"username Already taken")
            return render(request,"accounts/signup.html",{
                "form":form,
            })
        elif(User.objects.filter(email=email).first()):
            messages.error(request,"Email is already registered")
            return render(request,"accounts/signup.html",{
                "form":form,
            })
        elif(form.is_valid() and pass1==pass2):
            my_user = User(username=username,email = email,first_name=first_name,last_name=last_name)
            my_user.set_password(pass1)
            my_user.save()

            auth_token = str(uuid.uuid4())

            avatar_url = f"https://api.dicebear.com/7.x/initials/svg?seed={first_name}%20{last_name}"

            profile = Profile(user = my_user,auth_token = auth_token,avatar_url = avatar_url)
            profile.save()

            send_mail(email,auth_token,username,"Email Authentication Recommendo","verification")
            return redirect('authenticate')
        elif pass1 != pass2:
            messages.error(request,"Both the passwords should be same")
            return render(request,"accounts/signup.html",{
                "form":form,
            })
        else:
            return render(request,"accounts/signup.html",{
                "form":form,
            })
    

def AccForgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).first():
            user = User.objects.get(email=email)
            name = user.first_name
            my_profile = user.profile
            pass_reset_token = str(uuid.uuid4())
            my_profile.pass_reset_token = pass_reset_token
            my_profile.save()

            send_mail(email,pass_reset_token,name,"Password Reset Recommendo","pass-reset")
            return redirect('authenticate')
        
        else:
            messages.error(request,"Email Is Incorrect")
            return redirect('forget_pass')
        
def AccResetPassword(request,pass_reset_token):
    if request.method == 'POST':
        new_pass = request.POST.get('new-pass')
        conf_pass = request.POST.get('conf-pass')
        if new_pass != conf_pass:
            messages.error(request,"Both the passwords should be same")
            return render(request,"home/resetpass.html")
        elif len(new_pass) < 8 or len(new_pass) > 30:
            messages.error(request,"Your new password must be between 8 to 30 characters")
            return render(request,"home/resetpass.html")
        
        user = Profile.objects.get(pass_reset_token=pass_reset_token).user
        user.set_password(new_pass)
        user.save()
        my_profile = Profile.objects.get(pass_reset_token=pass_reset_token)
        my_profile.pass_reset_token = ''
        my_profile.save()
        messages.success(request,"Password changed successfully")
        return redirect('login')


    if Profile.objects.filter(pass_reset_token=pass_reset_token).first():
        return render(request,"home/resetpass.html")
    else:
        return Http404()

def send_mail(email,token,name,sub,type):
    subject = sub
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    if type == "pass-reset":
        link = f"http://127.0.0.1:8000/accounts/reset-pass/{token}"
    else:
        link = f"http://127.0.0.1:8000/accounts/{token}"

    html_content = render_to_string(f"accounts/{type}.html",{
        "link":link,
        "name":name
    })

    email = EmailMessage(subject,html_content,from_email,recipient_list)
    email.content_subtype = 'html'
    email.send()


def Auth_page(request):
    return render(request,"accounts/authenticate.html")

def email_authentication(request,auth_token):
    if Profile.objects.filter(auth_token=auth_token).first():
        my_profile = Profile.objects.get(auth_token = auth_token)
        if my_profile.is_verified:
            messages.success(request,"Account already verified")
            return redirect('login')
        else:
            my_profile.is_verified = True
            my_profile.save()
            messages.success(request,"Account verified successfully")
            return redirect('login')
        
    else:
        return Http404()
    


@login_required(login_url="/accounts/login/")
def Auth_AccResetPassword(request):
    if request.method == 'POST':
        curr_pass = request.POST.get('curr-pass').strip()
        new_pass = request.POST.get('new-pass').strip()
        conf_pass = request.POST.get('conf-pass').strip()

        if not curr_pass or not new_pass:
            messages.error(request, "None of the fields can be empty")
            return render(request,"home/auth_resetpass.html")
        elif len(new_pass) < 8 or len(new_pass) > 30:
            messages.error(request,"Your new password must be between 8 to 30 characters")
            return render(request,"home/auth_resetpass.html")
        elif new_pass != conf_pass:
            messages.error(request,"New password should be same as confirm password")
            return render(request,"home/auth_resetpass.html")
        elif not request.user.check_password(curr_pass):
            messages.error(request,"Current password is wrong")
            return render(request,"home/auth_resetpass.html")
        elif curr_pass == new_pass:
            messages.error(request, "New password should be different from the current")
            return render(request,"home/auth_resetpass.html")
        else:
            user = request.user
            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Password changed successfully")
            return render(request,"home/auth_resetpass.html")
 
    return render(request,"home/auth_resetpass.html")